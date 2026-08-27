import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const defaultRoot = resolve(import.meta.dirname, "..");
const root = resolve(process.env.R072N_RELEASE_ROOT ?? defaultRoot);
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const snapshotPath = resolve(
  root,
  "scripts/i18n-snapshots/r072n-missing.json",
);
const checkOnly = process.argv.includes("--check-only");

const englishByChinese = new Map([
  ["研究笔记 R0.72N：耗散一载波 action-poor 路线失效；Coble–He 映射给出本站的次线性 cubic 推论。", "Research note R0.72N: the action-poor route fails for the dissipative one-carrier chain, while the Coble–He mapping yields the project-specific sublinear cubic corollary."],
  ["一般 Navier–Stokes 问题仍未解决", "The general Navier–Stokes problem remains unsolved"],
  ["R0.72N｜耗散 action no-go 与次线性 cubic", "R0.72N｜Dissipative action no-go and sublinear cubic"],
  ["完整耗散链的矩障碍、action 下界、时变剪切映射与开放的 logarithmic sharpen。", "The moment barrier and action lower bound for the complete dissipative chain, the time-dependent-shear mapping, and the open logarithmic sharpen."],
  ["研究笔记 R0.72N · DISSIPATIVE CHAIN · ENHANCED DISSIPATION", "Research note R0.72N · DISSIPATIVE CHAIN · ENHANCED DISSIPATION"],
  ["action-poor 路线在耗散链上失效；", "The action-poor route fails for the dissipative chain;"],
  ["true cubic 仍保持次线性", "the true cubic remains sublinear"],
  ["我回到带 diagonal heat 的完整一载波链。能量与二阶矩账本给 \\(K_\\sigma\\lesssim1+\\sigma^{2/3}\\)，首耦合层却给 \\(x_\\sigma\\gtrsim\\sigma^{4/3}\\log\\sigma\\)，所以声明 launch 上的 action-poor 条件不成立。把生成函数映到 Coble–He 的时变剪切方程后，我再由其 \\(L^2\\) 衰减推出本站推论 \\(\\mathcal C_{\\rm diss}=O(a^2\\sqrt\\sigma)\\)。对数 sharpen、多载波和一般三维问题仍开放。", "I return to the complete one-carrier chain with diagonal heat. The energy and second-moment ledger gives \\(K_\\sigma\\lesssim1+\\sigma^{2/3}\\), while the first coupling layer gives \\(x_\\sigma\\gtrsim\\sigma^{4/3}\\log\\sigma\\), so the action-poor condition fails for the stated launch. After mapping the generating function to the Coble–He time-dependent-shear equation, I use its \\(L^2\\) decay to derive the project-specific corollary \\(\\mathcal C_{\\rm diss}=O(a^2\\sqrt\\sigma)\\). The logarithmic sharpen, multiple carriers, and the general three-dimensional problem remain open."],
  ["状态 · R0.72N 定理完成", "Status · R0.72N theorem complete"],
  ["版本 v0.72N · 2026-08-27", "Version v0.72N · 2026-08-27"],
  ["同一个耗散 launch 给出一项否定和一项正面结论", "The same dissipative launch gives one negative and one positive decision"],
  ["对声明的 row-aligned launch，\\(\\sigma^{1/3}x_\\sigma/K_\\sigma\\gtrsim\\sigma\\log\\sigma\\to\\infty\\)。R0.72M 提出的 action-poor 充分路线在这个耗散族上不成立。", "For the stated row-aligned launch, \\(\\sigma^{1/3}x_\\sigma/K_\\sigma\\gtrsim\\sigma\\log\\sigma\\to\\infty\\). The sufficient action-poor route proposed in R0.72M fails for this dissipative family."],
  ["完整无限链满足 \\(E'=-2D\\) 与 \\(D'\\le-2D^2+4\\sigma\\sqrt D\\)，从而 \\(\\sup D\\le\\max\\{1,(2\\sigma)^{2/3}\\}\\)。", "The complete infinite chain satisfies \\(E'=-2D\\) and \\(D'\\le-2D^2+4\\sigma\\sqrt D\\), hence \\(\\sup D\\le\\max\\{1,(2\\sigma)^{2/3}\\}\\)."],
  ["Coble–He 的时变剪切半群定理应用于重标度生成函数；坐标投影与时间积分再给本站推论 \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sigma^{1/2}=o(\\sigma a^2)\\)。", "The Coble–He time-dependent-shear semigroup theorem applies to the rescaled generating function; coordinate projection and time integration then give the project-specific corollary \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sigma^{1/2}=o(\\sigma a^2)\\)."],
  ["有限曲线与 \\(O(a^2\\log\\sigma)\\) 相容，但没有证明该 sharpen。多载波交叉项和 multiscale physical absorption 也未闭合。", "Finite curves are compatible with \\(O(a^2\\log\\sigma)\\), but they do not prove that sharpen. Multi-carrier cross terms and multiscale physical absorption also remain open."],
  ["证明对象保留完整格点和 diagonal heat", "The proof object retains the complete lattice and diagonal heat"],
  ["在 \\(0\\le y\\le1\\) 上取", "On \\(0\\le y\\le1\\), take"],
  ["并固定 \\(f_1^\\sigma(0)=2^{-1/2}\\)、\\(f_{-1}^\\sigma(0)=-2^{-1/2}\\)，其余行初值为零。这里没有删除 \\(-n^2f_n\\)，也没有把无限链换成有限 Galerkin 轨道。", "Fix \\(f_1^\\sigma(0)=2^{-1/2}\\) and \\(f_{-1}^\\sigma(0)=-2^{-1/2}\\), with zero initial data on every other row. This keeps \\(-n^2f_n\\) and does not replace the infinite chain by a finite Galerkin orbit."],
  ["skew coupling 不改变能量，但会抬高二阶矩", "The skew coupling preserves energy but raises the second moment"],
  ["令 \\(E=\\sum_n|f_n|^2\\)、\\(D=\\sum_n n^2|f_n|^2\\)、\\(P=\\sum_n n^4|f_n|^2\\)。Galerkin 恒等式经抛物光滑极限给出", "Let \\(E=\\sum_n|f_n|^2\\), \\(D=\\sum_n n^2|f_n|^2\\), and \\(P=\\sum_n n^4|f_n|^2\\). The Galerkin identities pass to the parabolic-smoothing limit and give"],
  ["加入 R0.72L 的固定解耦背景后，实际 enstrophy contrast 满足 \\(K_\\sigma\\lesssim1+\\sigma^{2/3}\\)。这是上界，不是匹配渐近。", "After adding the fixed decoupled background from R0.72L, the actual enstrophy contrast satisfies \\(K_\\sigma\\lesssim1+\\sigma^{2/3}\\). This is an upper bound, not a matching asymptotic."],
  ["首耦合层已经排除 action-poor 条件", "The first coupling layer already excludes the action-poor condition"],
  ["对 R0.72F 的 critical-log weight，短时间 Duhamel 极限和全局能量界分别给", "For the R0.72F critical-log weight, the short-time Duhamel limit and the global energy bound respectively give"],
  ["这个 no-go 只覆盖声明的固定频带、row-aligned、one-carrier launch；它不是所有耗散数据的分类。", "This no-go covers only the stated fixed-band, row-aligned, one-carrier launch; it is not a classification of all dissipative data."],
  ["实际 action 落入 R0.72M 的危险窗", "The actual action enters the R0.72M danger window"],
  ["代入 \\(U_\\sigma\\asymp\\sigma^{7/3}\\)、\\(V_\\sigma\\asymp\\sigma^{1/3}\\) 后，两个 reciprocal branches 给出", "After substituting \\(U_\\sigma\\asymp\\sigma^{7/3}\\) and \\(V_\\sigma\\asymp\\sigma^{1/3}\\), the two reciprocal branches give"],
  ["所以 action denominator 不能关闭这个 launch。否定一条付款路线，不等于否定原始不等式或构造奇性。", "The action denominator therefore cannot close this launch. Excluding one payment route neither disproves the original inequality nor constructs a singularity."],
  ["时间重标度把链变成时变剪切的一个 Fourier mode", "Time rescaling turns the chain into one Fourier mode of a time-dependent shear"],
  ["令 \\(\\nu=\\sigma^{-1}\\)、\\(t=\\sigma y\\)，并以 \\(F(t,\\theta)=\\sum_n f_n^\\sigma(\\nu t)e^{in\\theta}\\) 生成函数编码全链，则", "Let \\(\\nu=\\sigma^{-1}\\) and \\(t=\\sigma y\\), and encode the full chain by the generating function \\(F(t,\\theta)=\\sum_n f_n^\\sigma(\\nu t)e^{in\\theta}\\). Then"],
  ["它对应 Coble–He 方程的 \\(k=-2\\)、horizontal diffusion switch \\(=0\\) 和 \\(V(t,\\theta)=e^{-\\nu t}\\sin\\theta\\)。在 \\(0\\le t\\le\\nu^{-1}\\) 上，临界点固定、振幅在 \\([e^{-1},1]\\) 内，Theorem 1.2 的非退化常数可统一选择。", "It matches the Coble–He equation with \\(k=-2\\), horizontal diffusion switch \\(=0\\), and \\(V(t,\\theta)=e^{-\\nu t}\\sin\\theta\\). On \\(0\\le t\\le\\nu^{-1}\\), the critical points are fixed, the amplitude lies in \\([e^{-1},1]\\), and the nondegeneracy constants in Theorem 1.2 can be chosen uniformly."],
  ["published semigroup estimate 与本站 cubic 推论必须分开署名", "The published semigroup estimate and the project cubic corollary require separate attribution"],
  ["给出声明时段内的半群衰减", "gives the semigroup decay on the stated time interval"],
  ["再用 \\(|f_1(f_0-f_2)|\\le\\sqrt2\\sum_n|f_n|^2\\) 投影并积分，得到", "Project with \\(|f_1(f_0-f_2)|\\le\\sqrt2\\sum_n|f_n|^2\\) and integrate to obtain"],
  ["最后一式是我在本站完成的 corollary，不是 Coble–He 原论文中的定理或原句。", "The last estimate is a corollary I derive on this site, not a theorem or sentence stated in the Coble–He paper."],
  ["有限曲线只保留为 sharpen 线索", "Finite curves remain only as a clue for sharpening"],
  ["producer 与 independent route 在声明截断、步长和 \\(\\sigma\\) 网格上互相吻合，并与 \\(O(a^2\\log\\sigma)\\) 曲线相容。这只能说明有限离散没有暴露冲突；它不证明 continuum logarithmic bound，也不决定尖锐常数。", "The producer and independent routes agree on the stated truncations, step sizes, and \\(\\sigma\\) grid, and are compatible with an \\(O(a^2\\log\\sigma)\\) curve. This only shows that the finite discretizations reveal no conflict; it proves neither a continuum logarithmic bound nor a sharp constant."],
  ["附图把 action no-go、published decay 和本站 corollary 分开", "The figure separates the action no-go, published decay, and project corollary"],
  ["彩图中的有限量是 fixed-geometry proxies：\\(K_{\\rm proxy}=1+D_{\\max}\\)、\\(x_{\\rm proxy}=\\sigma^2\\mathscr A_\\sigma\\)、\\(U=\\sigma^{7/3}\\)、\\(V=\\sigma^{1/3}\\)，并取 \\(\\mu=a=1\\)，固定几何常数已压掉。它们不是实际物理常数；\\(T/V\\le1\\) 是解析 ceiling。图中的 \\(\\sqrt\\sigma\\) 上界是本站从 Coble–He Theorem 1.2 推出的 corollary。", "The finite quantities in the color figure are fixed-geometry proxies: \\(K_{\\rm proxy}=1+D_{\\max}\\), \\(x_{\\rm proxy}=\\sigma^2\\mathscr A_\\sigma\\), \\(U=\\sigma^{7/3}\\), and \\(V=\\sigma^{1/3}\\), with \\(\\mu=a=1\\) and fixed geometric constants suppressed. They are not the actual physical constants; \\(T/V\\le1\\) is the analytic ceiling. The \\(\\sqrt\\sigma\\) upper bound in the figure is a project corollary of Coble–He Theorem 1.2."],
  ["published theorem、project corollary 与开放 sharpen 是三层结论", "The published theorem, project corollary, and open sharpen are three distinct claims"],
  ["直接支持非退化时变剪切的 \\(L^2\\) enhanced dissipation。它不陈述本站 cubic functional、\\(O(a^2\\sigma^{1/2})\\) 推论或 logarithmic rowwise variation。", "directly supports \\(L^2\\) enhanced dissipation for a nondegenerate time-dependent shear. It does not state the project cubic functional, the \\(O(a^2\\sigma^{1/2})\\) corollary, or logarithmic rowwise variation."],
  ["给出 mixing 到 enhanced dissipation 的抽象方向；", "gives an abstract route from mixing to enhanced dissipation;"],
  ["的 fixed-shear sharp mixing 为 logarithmic sharpen 提供相邻线索。两者都不直接覆盖这里的时变振幅与 first-row total variation。限定检索不构成新颖性或优先权证明。", "provides adjacent evidence for a logarithmic sharpen through sharp fixed-shear mixing. Neither source directly covers the time-dependent amplitude or first-row total variation here. A bounded search does not establish novelty or priority."],
  ["价值是关闭错误分支，并留下一个可移植的次线性机制", "The value is to close a false branch and retain a portable sublinear mechanism"],
  ["R0.72N 严格排除了“耗散会自动把 action 压到 danger window 下方”的想法，同时把 raw \\(O(\\sigma a^2)\\) cubic estimate 改进为一载波类中的 \\(O(a^2\\sqrt\\sigma)\\)。这比有限拟合更弱，但已是连续方程上的统一次线性结论。", "R0.72N rigorously excludes the idea that dissipation automatically pushes the action below the danger window, while improving the raw \\(O(\\sigma a^2)\\) cubic estimate to \\(O(a^2\\sqrt\\sigma)\\) in the one-carrier class. This is weaker than the finite-data fit but is already a uniform sublinear statement for the continuum equation."],
  ["它没有闭合 R0.72L 的完整物理 ledger，也没有产生一般三维 continuation criterion。对 Clay 问题的作用仍是筛选机制和缩小接口，原问题保持开放。", "It does not close the complete R0.72L physical ledger or produce a continuation criterion for general three-dimensional flows. Its role for the Clay problem remains mechanism screening and interface reduction; the original problem remains open."],
  ["R0.72O：回填物理账本并检查多载波稳定性", "R0.72O: reinsert the physical ledger and test multi-carrier stability"],
  ["下一节先把 \\(O(a^2\\sqrt\\sigma)\\) 重新代入 R0.72L 的 normalized physical ledger，确定一载波强耦合窗口；随后检查有限或 common-band 多载波叠加是否因 cross terms 丢失 \\(\\sigma^{1/2}\\) 增益。logarithmic BV sharpen 保留为可并行但非必需的目标。", "The next section first reinserts \\(O(a^2\\sqrt\\sigma)\\) into the normalized R0.72L physical ledger to determine the one-carrier strong-coupling window, then checks whether finite or common-band multi-carrier superposition loses the \\(\\sigma^{1/2}\\) gain through cross terms. The logarithmic BV sharpen remains a parallel but nonessential target."],
  ["本节没有证明 matching asymptotic、logarithmic cubic、多载波、multiscale physical absorption、任意三维继续性、有限时奇性或全局光滑性。Clay 千禧年问题仍未解决。", "This section proves no matching asymptotic, logarithmic cubic bound, multi-carrier theorem, multiscale physical absorption, continuation result for arbitrary three-dimensional flows, finite-time singularity, or global smoothness. The Clay Millennium Problem remains unsolved."],
  ["报告、主张矩阵、文献审计和双路证书", "Report, claim matrix, literature audit, and two-route certificates"],
  ["研究笔记 R0.72N · 2026-08-27", "Research note R0.72N · 2026-08-27"],
  ["耗散链", "Dissipative chain"],
  ["矩账本", "Moment ledger"],
  ["剪切映射", "Shear mapping"],
  ["诊断", "Diagnostics"],
  ["01 · 完整耗散链", "01 · Complete dissipative chain"],
  ["02 · 能量与二阶矩", "02 · Energy and second moment"],
  ["03 · critical-log action", "03 · Critical-log action"],
  ["04 · scalar screen", "04 · Scalar screen"],
  ["05 · 时变剪切映射", "05 · Time-dependent-shear mapping"],
  ["06 · 本站推论", "06 · Project corollary"],
  ["07 · 有限诊断", "07 · Finite diagnostics"],
  ["08 · 正式附图", "08 · Formal figure"],
  ["09 · 文献边界", "09 · Literature boundary"],
  ["10 · 研究价值", "10 · Research value"],
  ["11 · R0.72O", "11 · R0.72O"],
  ["12 · 主张边界", "12 · Claim boundary"],
  ["13 · 复现入口", "13 · Reproduction"],
  ["R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72N 的 104 个研究节点；最新一节排除 action-poor 路线并证明一载波 true cubic 次线性。", "Research recap after R0.60: complete coverage from R0.61 through R0.72N, totaling 104 research nodes; the latest section excludes the action-poor route and proves a sublinear one-carrier true cubic."],
  ["二十八个阶段、104 个节点：从约化递推和时间迹账本，到 critical-log action、耗散链与 enhanced-dissipation corollary。", "Twenty-eight phases and 104 nodes: from reduced recurrences and temporal-trace ledgers to the critical-log action, dissipative chain, and enhanced-dissipation corollary."],
  ["R0.61–R0.72N｜R0.60 之后的研究回顾", "R0.61–R0.72N｜Research recap after R0.60"],
  ["累计回顾 · R0.61–R0.72N · 2026-08-27", "Cumulative recap · R0.61–R0.72N · 2026-08-27"],
  ["这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72N 的 104 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。这里的节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。", "This page follows the phase recap for R0.00–R0.60 and organizes R0.61 through R0.72N into 104 research nodes. I record chronologically what each segment actually proves, which proposals are excluded by concrete counterexamples or scaling analysis, and which conditions have not been derived from the Navier–Stokes equations. Node status describes the type of evidence and does not misstate release archiving as completion of a phase objective."],
  ["R0.61–R0.72N", "R0.61–R0.72N"],
  ["收录节点：104", "Nodes included: 104"],
  ["回顾截止时公开笔记：164", "Public notes at recap endpoint: 164"],
  ["回顾截止节点：R0.72N", "Recap endpoint: R0.72N"],
  ["02 · 104 节完整索引", "02 · Complete 104-note index"],
  ["R0.61–R0.72N 研究节点", "R0.61–R0.72N research nodes"],
  ["R0.70A–R0.72N 已公开版本", "Published releases from R0.70A–R0.72N"],
  ["R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 104 个节点沿着这个缺口推进；R0.70A–R0.72N 的 66 个版本已经公开；其中 42 个满足当前 formal-figure 完整封存合同，但其中仍包含条件定理、反例、有限诊断和开放缺口。", "The material from R0.00–R0.60 remains in the previous phase recap. The conclusion at R0.60 is that the complete Fourier–Leray structure and higher-order computations can continue, but the critical quantity for general three-dimensional solutions is not yet controlled. The subsequent 104 nodes advance along this gap; the releases from R0.70A–R0.72N, 66 in total, are public, and 42 satisfy the current formal-figure complete-archive contract, while still including conditional theorems, counterexamples, finite diagnostics, and open gaps."],
  ["R0.72L–R0.72N · strong-coupling screen 与耗散决策", "R0.72L–R0.72N · Strong-coupling screen and dissipative decision"],
  ["R0.72L 保留 actual \\(K\\) 与 \\(x\\)，R0.72M 把 scalar danger window 精确化。R0.72N 回到完整耗散一载波链，证明 \\(K_\\sigma\\lesssim1+\\sigma^{2/3}\\) 而 \\(x_\\sigma\\gtrsim\\sigma^{4/3}\\log\\sigma\\)，从而排除声明 launch 上的 action-poor route。", "R0.72L retains the actual \\(K\\) and \\(x\\), and R0.72M makes the scalar danger window exact. R0.72N returns to the complete dissipative one-carrier chain and proves \\(K_\\sigma\\lesssim1+\\sigma^{2/3}\\) while \\(x_\\sigma\\gtrsim\\sigma^{4/3}\\log\\sigma\\), thereby excluding the action-poor route for the stated launch."],
  ["Coble–He 的时变剪切 \\(L^2\\) 衰减经坐标投影和时间积分给本站 corollary \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\)。logarithmic sharpen、多载波稳定性和物理账本回填仍开放。", "Coordinate projection and time integration turn the Coble–He time-dependent-shear \\(L^2\\) decay into the project-specific corollary \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\). The logarithmic sharpen, multi-carrier stability, and physical-ledger reinsertion remain open."],
  ["R0.72N 附图", "R0.72N figure"],
  ["R0.72N 证书", "R0.72N certificates"],
  ["R0.61–R0.72N 的 104 节公开笔记", "Public research notes from R0.61–R0.72N: 104"],
  ["R0.72N 的 dissipative one-carrier theorem：声明 launch 上 \\(K_\\sigma\\lesssim1+\\sigma^{2/3}\\)、\\(x_\\sigma\\gtrsim\\sigma^{4/3}\\log\\sigma\\)，故 action-poor route 失效；Coble–He 的 published \\(L^2\\) decay 经本站投影给 \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma=o(\\sigma a^2)\\)。后者是本站 corollary；logarithmic rate 与多载波仍开放。", "R0.72N dissipative one-carrier theorem: for the stated launch, \\(K_\\sigma\\lesssim1+\\sigma^{2/3}\\) and \\(x_\\sigma\\gtrsim\\sigma^{4/3}\\log\\sigma\\), so the action-poor route fails; projecting the published Coble–He \\(L^2\\) decay gives the project-specific estimate \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma=o(\\sigma a^2)\\). The latter is a project corollary; the logarithmic rate and multiple carriers remain open."],
  ["action-poor 分支已排除，一载波 true cubic 已统一次线性", "The action-poor branch is excluded, and the one-carrier true cubic is uniformly sublinear"],
  ["截至 R0.72N，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 104 个节点或 66 个公开版本解释成对千禧年问题完成了某个比例。", "As of R0.72N, there is no new unconditional continuation criterion, no reduction of the set of all possible singular solutions, and no proof of finite-time breakdown. The 104 nodes or 66 public releases cannot be interpreted as a completion percentage for the Millennium Problem."],
  ["新的严格结果是耗散链的 energy/moment barrier、critical-log action lower bound、action-poor no-go 和 \\(T_\\sigma\\asymp\\sigma^{1/3}\\)。", "The new rigorous results are the energy and moment barrier for the dissipative chain, the critical-log action lower bound, the action-poor no-go, and \\(T_\\sigma\\asymp\\sigma^{1/3}\\)."],
  ["Coble–He published theorem 经本站坐标投影给 \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\)。logarithmic sharpen、物理回填和多载波 cross terms 仍开放。", "Project coordinate projection turns the published Coble–He theorem into \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\). The logarithmic sharpen, physical reinsertion, and multi-carrier cross terms remain open."],
  ["R0.72O 回填物理账本并测试多载波", "R0.72O reinserts the physical ledger and tests multiple carriers"],
  ["先把 \\(O(a^2\\sqrt\\sigma)\\) 代回 R0.72L normalized physical ledger，确定一载波强耦合窗口。", "First reinsert \\(O(a^2\\sqrt\\sigma)\\) into the normalized R0.72L physical ledger and determine the one-carrier strong-coupling window."],
  ["随后检查有限或 common-band 多载波叠加中的 cross terms；logarithmic BV sharpen 保留为并行目标。", "Then check cross terms in finite or common-band multi-carrier superposition; retain the logarithmic BV sharpen as a parallel target."],
  ["R0.70A–R0.72N 的 66 节 HTML/PDF 与研究源稿列入公开路线。按当前 formal-figure 合同，42 节完整封存；24 节较早版本仍列入可审计的旧档回补清单。", "The HTML/PDF releases and research sources from R0.70A–R0.72N, 66 in total, are on the public route. Under the current formal-figure contract, 42 releases are fully archived; 24 earlier releases remain on the auditable legacy-backfill list."],
  ["R0.72N 只覆盖声明的 fixed-band、row-aligned、one-carrier chain。\\(O(a^2\\sqrt\\sigma)\\) 是本站从 Coble–He 半群估计推出的 corollary，不是原论文定理；有限 log 曲线不是证明，Clay 正式问题仍然开放。", "R0.72N covers only the stated fixed-band, row-aligned, one-carrier chain. The estimate \\(O(a^2\\sqrt\\sigma)\\) is a project corollary derived from the Coble–He semigroup estimate, not a theorem in the source paper; finite logarithmic curves are not a proof, and the official Clay problem remains open."],
  ["保留 R0.72M 历史回顾", "Retain the R0.72M historical recap"],
  ["打开最新节点 R0.72N", "Open the latest node R0.72N"],
  ["查看 R0.72N 双路证书", "View the R0.72N two-route certificates"],
  ["R0.61–R0.72N 回顾 · 2026-08-27", "R0.61–R0.72N recap · 2026-08-27"],
  ["我目前关注", "My current focus"],
  ["R0.72N 已排除声明耗散 launch 上的 action-poor 路线，并由 Coble–He 时变剪切衰减推出本站的 \\(O(a^2\\sqrt\\sigma)\\) cubic corollary；物理回填、多载波和 logarithmic sharpen 仍开放。", "R0.72N excludes the action-poor route for the stated dissipative launch and turns the Coble–He time-dependent-shear decay into the project-specific \\(O(a^2\\sqrt\\sigma)\\) cubic corollary; physical reinsertion, multiple carriers, and the logarithmic sharpen remain open."],
  ["从 exact action screen 走到 dissipative one-carrier decision", "From the exact action screen to the dissipative one-carrier decision"],
  ["把 \\(O(a^2\\sqrt\\sigma)\\) 回填 R0.72L 的 normalized physical ledger，并检查有限或 common-band 多载波 cross terms 是否保留次线性增益。", "Reinsert \\(O(a^2\\sqrt\\sigma)\\) into the normalized R0.72L physical ledger and check whether finite or common-band multi-carrier cross terms retain the sublinear gain."],
  ["累计回顾 R0.61–R0.72N · 2026-08-27", "Cumulative recap R0.61–R0.72N · 2026-08-27"],
  ["R0.60 recap 之后的累计回顾收录 104 个节点；全站现有 164 篇公开研究笔记", "The cumulative recap after R0.60 contains 104 nodes; the site now has 164 public research notes"],
  ["累计回顾保持二十八个问题阶段，完整覆盖 R0.61–R0.72N。R0.72N 证明 action-poor 路线对声明耗散 launch 失效，并把 Coble–He 时变剪切衰减转成本站的 \\(O(a^2\\sqrt\\sigma)\\) cubic corollary。R0.70A–R0.72N 共 66 个版本已公开；42 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。", "The cumulative recap retains twenty-eight problem phases and completely covers R0.61–R0.72N. R0.72N proves that the action-poor route fails for the stated dissipative launch and turns the Coble–He time-dependent-shear decay into the project-specific \\(O(a^2\\sqrt\\sigma)\\) cubic corollary. Across R0.70A–R0.72N, 66 releases are public; 42 satisfy the current formal-figure complete-archive contract, while 24 older figure archives remain on the backfill list."],
  ["一载波 true cubic 已统一次线性；logarithmic sharpen、物理回填和多载波稳定性仍开放。", "The one-carrier true cubic is uniformly sublinear; the logarithmic sharpen, physical reinsertion, and multi-carrier stability remain open."],
  ["R0.72N 已完成：", "R0.72N complete:"],
  ["action-poor route 对声明耗散 launch 失效；one-carrier true cubic 已得到统一次线性上界。", "The action-poor route fails for the stated dissipative launch; the one-carrier true cubic now has a uniform sublinear upper bound."],
  ["耗散 action 不在安全分支；时变剪切仍给次线性 cubic", "The dissipative action is not on the safe branch; the time-dependent shear still gives a sublinear cubic"],
  ["我证明 \\(K_\\sigma\\lesssim1+\\sigma^{2/3}\\) 而 \\(x_\\sigma\\gtrsim\\sigma^{4/3}\\log\\sigma\\)，所以 \\(\\sigma^{1/3}x_\\sigma/K_\\sigma\\gtrsim\\sigma\\log\\sigma\\)。action-poor 路线在声明 launch 上失效，scalar screen 为 \\(\\sigma^{1/3}\\) 量级。", "I prove \\(K_\\sigma\\lesssim1+\\sigma^{2/3}\\) while \\(x_\\sigma\\gtrsim\\sigma^{4/3}\\log\\sigma\\), hence \\(\\sigma^{1/3}x_\\sigma/K_\\sigma\\gtrsim\\sigma\\log\\sigma\\). The action-poor route fails for the stated launch, and the scalar screen has order \\(\\sigma^{1/3}\\)."],
  ["Coble–He Theorem 1.2 应用于重标度生成函数；坐标投影与时间积分再给本站 corollary \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma=o(\\sigma a^2)\\)。这不是原论文原句；logarithmic rate 仍未证明。", "Coble–He Theorem 1.2 applies to the rescaled generating function; coordinate projection and time integration then give the project-specific corollary \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma=o(\\sigma a^2)\\). This is not a sentence from the source paper, and the logarithmic rate remains unproved."],
  ["多载波、multiscale physical absorption 与一般三维正则性仍开放。", "Multiple carriers, multiscale physical absorption, and general three-dimensional regularity remain open."],
  ["阅读 R0.72N 研究笔记 →", "Read the R0.72N research note →"],
  ["下一步 R0.72O：", "Next R0.72O:"],
  ["回填 normalized physical ledger，并检查多载波 cross terms。", "Reinsert the normalized physical ledger and check multi-carrier cross terms."],
  ["综述 v1.27 · 2026-08-27", "Review v1.27 · 2026-08-27"],
  ["上次综述 v1.26 · 2026-08-27", "Previous review v1.26 · 2026-08-27"],
  ["我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.72N 只列为研究笔记。我不把计算或笔记外推成正则性定理。", "I list published theorems as known results, mark 2026 preprints separately, and list R0.69P–R0.72N on this site only as research notes. I do not extrapolate computations or notes into regularity theorems."],
  ["累计回顾与 104 节索引", "Cumulative recap and 104-note index"],
  ["打开 104 节完整索引", "Open the complete 104-note index"],
  ["声明 launch 上 action-poor route 失效；Coble–He published \\(L^2\\) decay 经本站投影给 \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\)。logarithmic rate 仍开放。", "The action-poor route fails for the stated launch; projecting the published Coble–He \\(L^2\\) decay gives \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\). The logarithmic rate remains open."],
  ["开放接口 · R0.72O", "Open interface · R0.72O"],
  ["把一载波次线性 cubic 回填 normalized physical ledger，并检查多载波 cross terms 是否保留 \\(\\sigma^{1/2}\\) 增益。", "Reinsert the sublinear one-carrier cubic into the normalized physical ledger and check whether multi-carrier cross terms retain the \\(\\sigma^{1/2}\\) gain."],
  ["R0.72N 的时变剪切映射与 cubic 署名边界", "R0.72N boundary for the time-dependent-shear mapping and cubic attribution"],
  ["对非退化 time-dependent shear 给 \\(L^2\\) decay \\(e^{-c\\nu^{1/2}|k|^{1/2}t}\\)。R0.72N 直接核对 \\(k=-2\\)、horizontal diffusion switch \\(=0\\)、\\(V(t,\\theta)=e^{-\\nu t}\\sin\\theta\\) 及 \\(0\\le t\\le\\nu^{-1}\\) 上的统一常数。", "gives \\(L^2\\) decay \\(e^{-c\\nu^{1/2}|k|^{1/2}t}\\) for a nondegenerate time-dependent shear. R0.72N directly verifies \\(k=-2\\), horizontal diffusion switch \\(=0\\), \\(V(t,\\theta)=e^{-\\nu t}\\sin\\theta\\), and uniform constants on \\(0\\le t\\le\\nu^{-1}\\)."],
  ["由坐标估计、Parseval 和时间积分得到 \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sigma^{1/2}\\)，这是本站从 published semigroup estimate 推出的 corollary，不是 Coble–He 原论文的定理或原句。", "The coordinate estimate, Parseval, and time integration give \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sigma^{1/2}\\). This is a project corollary of the published semigroup estimate, not a theorem or sentence in the Coble–He paper."],
  ["的 mixing-to-dissipation 框架与", "mixing-to-dissipation framework and"],
  ["的 fixed-shear sharp mixing 都不直接给这里的 logarithmic first-row variation。", "fixed-shear sharp mixing do not directly give the logarithmic first-row variation here."],
  ["R0.72N 的主张边界", "Claim boundary for R0.72N"],
  ["action-poor no-go 只覆盖声明的 fixed-band、row-aligned、one-carrier launch；\\(O(a^2\\log\\sigma)\\) 仍是有限诊断支持的开放 sharpen。matching asymptotic、多载波、multiscale physical absorption 和一般三维继续性均未闭合；限定检索不构成新颖性或优先权证明。", "The action-poor no-go covers only the stated fixed-band, row-aligned, one-carrier launch; \\(O(a^2\\log\\sigma)\\) remains an open sharpen supported only by finite diagnostics. Matching asymptotics, multiple carriers, multiscale physical absorption, and general three-dimensional continuation all remain open; a bounded search does not establish novelty or priority."],
  ["文献综述 v1.27 · 2026-08-27", "Literature review v1.27 · 2026-08-27"],
]);

const exactDerivations = [
  {
    newZh: "R0.72N 回到耗散链，证明 action-poor route 对声明 launch 失效；再把 Coble–He 的时变剪切衰减转成本站的 \\(O(a^2\\sqrt\\sigma)\\) cubic corollary。",
    en: "R0.72N returns to the dissipative chain, proves that the action-poor route fails for the stated launch, and turns the Coble–He time-dependent-shear decay into the project-specific \\(O(a^2\\sqrt\\sigma)\\) cubic corollary.",
  },
  {
    newZh: "R0.72N 在完整耗散链上排除声明 launch 的 action-poor route，并由 Coble–He 时变剪切衰减推出本站 corollary \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\)；logarithmic rate 与多载波仍开放。",
    en: "R0.72N excludes the action-poor route for the stated launch on the complete dissipative chain and derives the project-specific corollary \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\) from the Coble–He time-dependent-shear decay; the logarithmic rate and multiple carriers remain open.",
  },
];

function numericTokens(value) {
  return [...value.matchAll(/\p{N}+(?:[.,]\p{N}+)*/gu)].map(
    (match) => match[0],
  );
}

function sameTokens(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

function fallbackEnglish(zh) {
  const stripped = zh
    .replace(/[\u3400-\u9fff\uf900-\ufaff]+/gu, " ")
    .replace(/[，。：；！？“”《》【】]/gu, " ")
    .replace(/\s+/g, " ")
    .trim();
  const prefix = zh.includes("我") ? "I record: " : "Release statement: ";
  return prefix + (stripped || "this release statement.");
}

const expectedFiles = [
  "literature-review.html",
  "notes/r0-72n.html",
  "recap-r0-61-r0-72n.html",
  "research-review.html",
];
for (const relative of expectedFiles) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.27')) {
    throw new Error(relative + ": expected i18n cache version v1.27");
  }
}

const source = await collectSiteStrings(publicDirectory);
const translations = JSON.parse(await readFile(translationPath, "utf8"));
const batchId = /^r072n\d+$/;
const retained = translations.filter((entry) => !batchId.test(entry.id));
const retainedByChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (retainedByChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.72N batch");
}

const missing = source.filter((entry) => !retainedByChinese.has(entry.zh));
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))].sort();
if (!sameTokens(missingFiles, expectedFiles)) {
  throw new Error("Unexpected R0.72N source files: " + JSON.stringify(missingFiles));
}

const simpleTransforms = [
  ["R0.72N", "R0.72M"],
  ["R0.72O", "R0.72N"],
  ["v1.27", "v1.26"],
  ["104", "103"],
  ["164", "163"],
  ["66", "65"],
  ["42", "41"],
  ["74", "73"],
];

function deriveFromRetained(zh) {
  const queue = [{ value: zh, applied: [] }];
  const seen = new Set([zh]);
  while (queue.length) {
    const current = queue.shift();
    const retainedEntry = retainedByChinese.get(current.value);
    if (retainedEntry) {
      let en = retainedEntry.en;
      for (const [newValue, oldValue] of current.applied.toReversed()) {
        en = en.replaceAll(oldValue, newValue);
      }
      return en;
    }
    if (current.applied.length >= 4) continue;
    for (const [newValue, oldValue] of simpleTransforms) {
      if (!current.value.includes(newValue)) continue;
      const candidate = current.value.replaceAll(newValue, oldValue);
      if (seen.has(candidate)) continue;
      seen.add(candidate);
      queue.push({
        value: candidate,
        applied: [...current.applied, [newValue, oldValue]],
      });
    }
  }
  return null;
}

function deriveComposite(zh) {
  const homeAddition = exactDerivations[0];
  if (zh.includes(homeAddition.newZh)) {
    const oldZh = zh.replace(homeAddition.newZh, "");
    const retainedEntry = retainedByChinese.get(oldZh);
    if (retainedEntry) return retainedEntry.en + homeAddition.en;
  }
  const literatureAddition = exactDerivations[1];
  if (zh.includes(literatureAddition.newZh)) {
    const oldZh = zh.replace(literatureAddition.newZh, "");
    const retainedEntry = retainedByChinese.get(oldZh);
    if (retainedEntry) {
      return retainedEntry.en.replace(
        "General Navier–Stokes regularity remains open.",
        literatureAddition.en +
          " General Navier–Stokes regularity remains open.",
      );
    }
  }
  const newSuffix =
    " → exact action danger window → dissipative one-carrier decision → physical reinsertion and multi-carrier gate";
  const oldSuffix =
    " → exact action danger window → dissipative one-carrier gate";
  if (zh.endsWith(newSuffix)) {
    const oldZh = zh.slice(0, -newSuffix.length) + oldSuffix;
    const retainedEntry = retainedByChinese.get(oldZh);
    if (retainedEntry) {
      return retainedEntry.en.slice(0, -oldSuffix.length) + newSuffix;
    }
  }
  return null;
}

let fallbackCount = 0;
const translatedEntries = missing.map((entry, index) => {
  let en =
    englishByChinese.get(entry.zh) ??
    deriveComposite(entry.zh) ??
    deriveFromRetained(entry.zh);
  if (!en) {
    en = fallbackEnglish(entry.zh);
    fallbackCount += 1;
  }
  if (!en.trim() || containsChinese(en)) {
    throw new Error("Blank or Chinese-containing English for: " + entry.zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("Collective English voice remains in: " + entry.zh);
  }
  if (entry.zh.includes("我") && !/\bI\b/.test(en)) {
    throw new Error("First-person singular English is missing for: " + entry.zh);
  }
  if (!sameTokens(extractProtectedTokens(entry.zh), extractProtectedTokens(en))) {
    throw new Error(
      "Protected-token mismatch for:\n" +
        entry.zh +
        "\nZH " +
        JSON.stringify(extractProtectedTokens(entry.zh)) +
        "\nEN " +
        JSON.stringify(extractProtectedTokens(en)),
    );
  }
  if (!sameTokens(numericTokens(entry.zh), numericTokens(en))) {
    throw new Error(
      "Numeric-token mismatch for:\n" +
        entry.zh +
        "\nZH " +
        JSON.stringify(numericTokens(entry.zh)) +
        "\nEN " +
        JSON.stringify(numericTokens(en)),
    );
  }
  return {
    ...entry,
    id: "r072n" + String(index + 1).padStart(3, "0"),
    en,
  };
});

if (fallbackCount !== 0) {
  throw new Error(`R0.72N translation batch used ${fallbackCount} fallback rows`);
}

const finalTranslations = [...retained, ...translatedEntries];
for (const field of ["id", "zh"]) {
  const values = finalTranslations.map((entry) => entry[field]);
  if (new Set(values).size !== values.length) {
    throw new Error("Duplicate final translation " + field);
  }
}

const snapshot = missing.map(({ zh, count, files }) => ({ zh, count, files }));
if (checkOnly) {
  const currentSnapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
  if (JSON.stringify(currentSnapshot) !== JSON.stringify(snapshot)) {
    throw new Error("R0.72N missing-string snapshot is stale");
  }
  if (JSON.stringify(translations) !== JSON.stringify(finalTranslations)) {
    throw new Error("R0.72N translations/en.json batch is stale");
  }
} else {
  await writeFile(snapshotPath, JSON.stringify(snapshot, null, 2) + "\n");
  await writeFile(
    translationPath,
    JSON.stringify(finalTranslations, null, 2) + "\n",
  );
}

console.log(
  JSON.stringify({
    checkOnly,
    added: translatedEntries.length,
    fallback: fallbackCount,
    total: finalTranslations.length,
    liveStrings: source.length,
    missingBefore: missing.length,
    missingAfter: 0,
    files: missingFiles,
  }),
);
