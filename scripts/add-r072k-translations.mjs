import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const snapshotPath = resolve(
  root,
  "scripts/i18n-snapshots/r072k-missing.json",
);
const checkOnly = process.argv.includes("--check-only");

const translationRows = String.raw`
打开 101 节完整索引 ||| Open the complete 101-note index
的 complex Rolle framework 和 analytic zero-counting theories 使用复增长或方程结构；R0.72K 不寻找复导数零点，而是对每个实时间根隙单独投影。Navier–Stokes time analyticity 也不支付 mixed row 或 true cubic。 ||| 's complex Rolle framework and analytic zero-counting theories use complex growth or equation structure; R0.72K does not seek zeros of the complex derivative, but projects separately on each real-time root gap. Navier–Stokes time analyticity likewise does not pay for the mixed row or true cubic.
的 scattered-zero estimate 需要 fill distance。它们都不直接给出 fixed endogenous zero level 上的 squared endpoint-derivative sum。 ||| 's scattered-zero estimate requires a fill distance. Neither directly gives the squared endpoint-derivative sum on a fixed endogenous zero level.
方向引理的证明完整写出；限定检索未发现同一 fixed-level endpoint-slope packing 公式，但不据此主张新颖性或优先权。complete-root consequence 限于 finite triangular class，common-band decay 还保留 perturbative assumptions。 ||| The directional lemma is proved in full. The bounded search found no identical fixed-level endpoint-slope packing formula, but this does not support a claim of novelty or priority. The complete-root consequence is limited to the finite triangular class, and the common-band decay retains perturbative assumptions.
检查离开 \(gB/R^2\le\gamma_0\) 后的 mixed-row 与 true-cubic payment；multiscale heat windows 保留为并列后续接口。 ||| Test the mixed-row and true-cubic payment after leaving \(gB/R^2\le\gamma_0\); retain multiscale heat windows as a parallel subsequent interface.
开放接口 · R0.72L ||| Open interface · R0.72L
控制端点条件下的积分乘积； ||| control integral products under endpoint conditions;
累计回顾与 101 节索引 ||| Cumulative recap and 101-note index
每个根隙使用右端导数的 norming direction，把复目标的全部 derivative mass 支付到 mixed row 与 true cubic；common-band complete ledger 在物理 critical-log 归一化后统一衰减。 ||| A norming direction for the right-endpoint derivative on each root gap pays the full derivative mass of the complex target into the mixed row and true cubic; the common-band complete ledger decays uniformly after physical critical-log normalization.
文献综述 v1.24 · 2026-08-27 ||| Literature review v1.24 · 2026-08-27
我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.72K 只列为研究笔记。我不把计算或笔记外推成正则性定理。 ||| I list published theorems as known results, mark 2026 preprints separately, and list R0.69P–R0.72K on this site only as research notes. I do not extrapolate computations or notes into regularity theorems.
用线性泛函表述 vector-valued mean-value conclusions； ||| formulate vector-valued mean-value conclusions through linear functionals;
与 Banach indicatrix 理论处理 level crossings； ||| and Banach indicatrix theory treats level crossings;
中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–U 给出 conditional incidence、genuine internal-entry、second-time-jet 与 finite recurrence 边界。R0.71V–W 分离 fixed zero-level trace 并排除 data-uniform complete first-row ledger。R0.71X 在 fixed-dimensional small-coupling family 内达到 one-third endpoint；R0.71Y 处理 selected roots；R0.71Z 给出 all-root slope-mass bound 和 launch-inclusive floor cancellation；R0.72A 把 strong-coupling loss 局部化到实际观察层，R0.72B 保留 exact target-row participation，R0.72C 得到 phase-uniform exact-launch \(M^{-8/3}\) 与 fixed-positive tail \(M^{-3}\) 的 sharp algebraic scales。R0.72D 在 shifted Rudin–Shapiro family 上构造 positive-time exact root，保留 full rotational charge，并得到非消失但不发散的 normalized complete-root ledger。R0.72E 回到 fixed-carrier Bessel family，以定量 negative-Sobolev action 证明 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。R0.72F 再用 regularly varying initial-layer weights 分离 selected-root 的 \(1/3\) 阈值与 Leray payment 的 \(1/2\) 阈值，并选出 critical-log 最小边界。R0.72G 在 exact real one-carrier lattice 上用 phase gauge、目标行恒等式与 Rolle–BV 归约证明完整根质量恰为对数量级，并得到 critical-log complete-root sharp saturation。R0.72H 在有限共轭配对多载波系统中证明 mixed row 的载波数无关 moment-resolved payment；全奇数 Rudin–Shapiro 族排除 action-only 版本，并使该 moment 所编码的载波幂次达到同阶。R0.72I 证明分离的 \(B_AQ_*\) 正项不能逐项物理吸收，同时用 joint exposure 和 odd-carrier parity 证明真实 complete ledger 统一衰减。R0.72J 完成 gcd-reduced Cayley graph 的二分分类，区分 odd cycle 与 triangle return，并证明 common-band coherent mixed-parity cubic 在物理归一化后仍衰减。R0.72K 通过逐根隙 norming direction 闭合 complete complex-target ledger，并证明其 common-band 物理归一化比仍统一衰减。一般 Navier–Stokes 正则性仍开放。 ||| . R0.69P–R0.71P reaches the positive-entry temporal-packing boundary, and R0.71Q–U gives the boundaries for conditional incidence, genuine internal entry, the second-time jet, and finite recurrence. R0.71V–W separates the fixed zero-level trace and excludes a data-uniform complete first-row ledger. R0.71X reaches the one-third endpoint in a fixed-dimensional small-coupling family; R0.71Y treats selected roots; R0.71Z gives an all-root slope-mass bound and launch-inclusive floor cancellation. R0.72A localizes the strong-coupling loss to the actual observation layer, R0.72B retains exact target-row participation, and R0.72C obtains the sharp algebraic scales \(M^{-8/3}\) for phase-uniform exact launch and \(M^{-3}\) for the fixed-positive tail. R0.72D constructs a positive-time exact root in a shifted Rudin–Shapiro family, retains the full rotational charge, and obtains a nonvanishing but nondivergent normalized complete-root ledger. R0.72E returns to a fixed-carrier Bessel family and uses a quantitative negative-Sobolev action estimate to make the complete-root ledger relative to the candidate \(D^{1/3}\Lambda_1\) payment diverge like \(R^{4/3}\). R0.72F then uses regularly varying initial-layer weights to separate the selected-root threshold \(1/3\) from the Leray-payment threshold \(1/2\), selecting the minimal critical-log boundary. On the exact real one-carrier lattice, R0.72G uses a phase gauge, target-row identities, and the Rolle–BV reduction to prove that the complete root mass has exactly logarithmic order and obtains sharp critical-log complete-root saturation. In a finite conjugate-paired multi-carrier system, R0.72H proves a carrier-count-independent moment-resolved payment for the mixed row; an all-odd Rudin–Shapiro family excludes the action-only version and attains the carrier power encoded by that moment. R0.72I proves that the separated positive \(B_AQ_*\) term cannot be absorbed physically term by term, while joint exposure and odd-carrier parity prove that the true complete ledger decays uniformly. R0.72J completes the bipartite classification of the gcd-reduced Cayley graph, distinguishes an odd cycle from a triangle return, and proves that a common-band coherent mixed-parity cubic still decays after physical normalization. R0.72K closes the complete complex-target ledger by assigning a norming direction to each root gap and proves that its common-band physically normalized ratio still decays uniformly. General Navier–Stokes regularity remains open.
directional zero sampling 与 complete complex-target ledger ||| directional zero sampling and the complete complex-target ledger
R0.72K 的 directional sampling 与 complex-root 边界 ||| Directional sampling and complex-root boundary of R0.72K
R0.72K 的主张边界 ||| Claim boundary for R0.72K
\(X(t)=t\) 在零点有单位斜率而 \(X''=0\)，所以首个所选根必须另付。另一方面，\(N^{-3}(e^{2\pi iNt}-1)\) 可以有 \(N+1\) 个根而总斜率平方质量趋零；定理控制的是 derivative mass，不是 raw root count。 ||| \(X(t)=t\) has unit slope at its zero while \(X''=0\), so the first selected root requires a separate payment. On the other hand, \(N^{-3}(e^{2\pi iNt}-1)\) can have \(N+1\) roots while its total squared slope mass tends to zero; the theorem controls derivative mass, not raw root count.
01 · 方向根隙定理 ||| 01 · Directional root-gap theorem
02 · 实投影证明 ||| 02 · Real-projection proof
03 · 尖锐边界 ||| 03 · Sharp boundary
06 · 物理归一化 ||| 06 · Physical normalization
07 · 双路审计 ||| 07 · Two-route audit
12 · 复现入口 ||| 12 · Reproduction
版本 v0.72K · 2026-08-27 ||| Version v0.72K · 2026-08-27
本节没有证明 multiscale 或 strong-coupling physical inequality，没有给出一般三维 Navier–Stokes 的新继续性判据，没有构造有限时奇性，也没有证明全局光滑性。Clay 千禧年问题仍未解决。 ||| This section proves no multiscale or strong-coupling physical inequality, gives no new continuation criterion for general three-dimensional Navier–Stokes, constructs no finite-time singularity, and proves no global smoothness. The Clay Millennium Problem remains unsolved.
抽象方向恒等式和继承账本由两条实现核对 ||| Two implementations check the abstract directional identity and inherited ledger
此前的 continuous-row 上界现在覆盖全部复根 ||| The previous continuous-row bound now covers all complex roots
代入 R0.72H 的 mixed-row payment 和 R0.72J 的 true-cubic minimum，可得 carrier-count-independent finite-row corollary。对 common-band aligned perturbative family，单个已构造复根给下界，而新定理给匹配上界： ||| Substituting the mixed-row payment from R0.72H and the true-cubic minimum from R0.72J gives a carrier-count-independent finite-row corollary. For the common-band aligned perturbative family, the single constructed complex root gives the lower bound and the new theorem gives the matching upper bound:
独立路线改用不同 sharpness 参数和复二维 Hilbert 曲线，并从独立 R0.72J 行数据重建物理账本；它不导入生产代码或结果。 ||| The independent route uses different sharpness parameters and a complex two-dimensional Hilbert curve, then reconstructs the physical ledger from independent R0.72J row data; it imports neither production code nor production results.
对 \(X_0(x)=e^{\lambda_0(x-A)}F_0(x)\) 应用方向定理。因为根隙内 \(x\le\tau_j\)，反向指数核不超过一。对所有有限根子集取上确界后得到 ||| Apply the directional theorem to \(X_0(x)=e^{\lambda_0(x-A)}F_0(x)\). Because \(x\le\tau_j\) within each root gap, the backward exponential kernel is at most one. Taking the supremum over all finite root subsets gives
对 R0.72J 的相干 mixed-parity block，完整 raw root mass 为 \(R^2\) 量级、物理 root ledger 为 \(R\) 量级，归一化比仍为 \(R^{-2/3}\)。因此 cubic no-go 后面没有隐藏一批失控的复根。 ||| For the coherent mixed-parity block of R0.72J, the complete raw root mass has order \(R^2\), the physical root ledger has order \(R\), and the normalized ratio remains \(R^{-2/3}\). Thus the cubic no-go does not conceal an uncontrolled collection of complex roots.
对任意有限 triangular carrier set 和 \(\delta\ne0\)，完整扩展根质量由首根、mixed row 与 true cubic 三项统一控制，不再要求固定实 gauge。 ||| For any finite triangular carrier set and \(\delta\ne0\), the complete extended root mass is controlled uniformly by the first root, mixed row, and true cubic, with no fixed real gauge required.
对实或复 Banach 空间中的 \(X\in W^{2,1}(I;B)\)，除第一个所选根外，全部根上的导数平方质量由 \(2\int_I\|X'\|\|X''\|\) 支付。 ||| For \(X\in W^{2,1}(I;B)\) in a real or complex Banach space, the squared derivative mass at every root except the first selected root is paid by \(2\int_I\|X'\|\|X''\|\).
反例 \(X(t)=e^{2\pi it}-1\) 的导数从不为零，说明 literal complex Rolle 不成立；本节没有声称它成立。 ||| The derivative of the counterexample \(X(t)=e^{2\pi it}-1\) never vanishes, showing that literal complex Rolle is false; this section does not claim otherwise.
方向采样本身已经与 carrier 数和根数解耦。下一节应检查 continuous-row bounds 在 \(gB/R^2\not\ll1\) 时是否仍能由完整能量与 critical-log action 支付；若 strong coupling 不闭合，再进入 separated heat windows 的 multiscale sum。 ||| Directional sampling itself is independent of both carrier count and root count. The next section should test whether the continuous-row bounds can still be paid by the full energy and critical-log action when \(gB/R^2\not\ll1\); if strong coupling does not close, the analysis should then pass to the multiscale sum over separated heat windows.
方向定理 ||| Directional theorem
方向投影替代 literal complex Rolle；完整 common-band complex-root ledger 在物理 critical-log 归一化后仍衰减。 ||| Directional projection replaces literal complex Rolle; the complete common-band complex-root ledger still decays after physical critical-log normalization.
复 Rolle 是假的，但完整复目标根账本仍可闭合 ||| Complex Rolle is false, but the complete complex-target root ledger still closes
复轨道不需要复 Rolle； ||| Complex trajectories do not require complex Rolle;
关闭的是一个真正的量词缺口，而不是把复目标强行实化 ||| A genuine quantifier gap is closed without forcing the complex target to be real
积分因子把根隙付款准确送到 mixed row 与 true cubic ||| The integrating factor sends each root-gap payment exactly to the mixed row and true cubic
连续分段线性导数的 plateau–ramp family 满足两端同为根，并使 ||| A plateau–ramp family with continuous piecewise-linear derivative has roots at both endpoints and makes
连续实函数 \(\phi_j\) 在根隙内至少有一个零点 \(c_j\)。从 \(c_j\) 积分到右端并使用链式法则，就得到该根隙的系数 2 估计。不同根隙互不重叠，所以可以直接求和。 ||| The continuous real function \(\phi_j\) has at least one zero \(c_j\) inside the root gap. Integrating from \(c_j\) to the right endpoint and using the chain rule gives the factor 2 estimate for that gap. Distinct root gaps are disjoint, so the estimates can be summed directly.
零平均的是方向投影，不是复导数 ||| The directional projection has zero mean, not the complex derivative
令 \(\phi_j(t)=\operatorname{Re}\ell_j(X'(t))\)。相邻端点都是根，因此 ||| Set \(\phi_j(t)=\operatorname{Re}\ell_j(X'(t))\). Both adjacent endpoints are roots, hence
每个根隙单独选择右端导数的 norming direction ||| Choose a norming direction for the right-endpoint derivative on each root gap
每个根隙只需要自己的实方向 ||| Each root gap needs only its own real direction
设 \(t_1<\cdots<t_m\) 且 \(X(t_j)=0\)。对每个 \(j\ge2\)，用 Hahn–Banach 选择 \(\ell_j\in B^*\)，使 \(\|\ell_j\|=1\) 且 \(\ell_j(X'(t_j))=\|X'(t_j)\|_B>0\)。复情形只需乘一个单位相位。 ||| Let \(t_1<\cdots<t_m\) and \(X(t_j)=0\). For every \(j\ge2\), use Hahn–Banach to choose \(\ell_j\in B^*\) such that \(\|\ell_j\|=1\) and \(\ell_j(X'(t_j))=\|X'(t_j)\|_B>0\). In the complex case, multiplication by a unit phase suffices.
生产路线核对 plateau–ramp sharpness、复圆周曲线、方向零点、R0.72J lineage hash，以及 complete-root measured/theorem ledgers。 ||| The production route checks plateau–ramp sharpness, the complex circular curve, directional zeros, the R0.72J lineage hash, and the measured and theorem complete-root ledgers.
声明的 perturbative common-band class 中，完整复根账本虽为 \(a^2N^2\) 量级，物理 critical-log 归一化后仍一致趋零。 ||| In the stated perturbative common-band class, the complete complex-root ledger has order \(a^2N^2\), yet still tends uniformly to zero after physical critical-log normalization.
完整根账本没有在 critical-log 尺度上存活 ||| The complete root ledger does not survive at the critical-log scale
系数 2、首根付款和“质量不等于根数”都有独立边界 ||| The factor 2, the first-root payment, and “mass is not root count” each have a separate boundary
研究笔记 R0.72K · DIRECTIONAL ZERO SAMPLING · COMPLEX ROOT LEDGER ||| Research note R0.72K · DIRECTIONAL ZERO SAMPLING · COMPLEX ROOT LEDGER
研究笔记 R0.72K：方向零点采样引理把 real/complex Banach-valued roots 的导数质量装入零计数无关的连续账本，并闭合 finite triangular class 的 complete complex-target root ledger。 ||| Research note R0.72K: the directional zero-sampling lemma places the derivative mass at real or complex Banach-valued roots into a continuous ledger independent of zero count and closes the complete complex-target root ledger for the finite triangular class.
因此未枚举的其他复根也必须装进同一个 \(a^2N^2\) 预算；这不是通过假设根数有限得到的。 ||| Therefore every unenumerated complex root must also fit within the same \(a^2N^2\) budget; this is not obtained by assuming that the root set is finite.
有限计算不枚举完整复根集，也不证明渐近率。证明来自方向采样引理、精确目标行和已经封闭的 continuous-row estimates。 ||| The finite computation neither enumerates the complete complex root set nor proves the asymptotic rate. The proof comes from the directional sampling lemma, the exact target row, and the already closed continuous-row estimates.
长浅负平台接短斜坡的标量族使比值趋于一，所以系数 2 在声明的正则性类中不能减小；单根仿射函数又说明首根付款不能删除。 ||| A scalar family with a long shallow negative plateau followed by a short ramp makes the ratio tend to one, so the factor 2 cannot be reduced in the stated regularity class; a one-root affine function also shows that the first-root payment cannot be removed.
这个结果把 common-band 反族路线从“单个复根与 cubic 被控制”提升为“完整复根账本被控制”。它仍不触及多尺度 heat windows 或 strong coupling。 ||| This result upgrades the common-band counterfamily route from “one complex root and the cubic are controlled” to “the complete complex-root ledger is controlled.” It still does not reach multiscale heat windows or strong coupling.
这个结论与根数和最小间距无关。对任意根集，以有限子集上确界定义 extended nonnegative sum；首个所选根可由 \(\sup_{X(t)=0}\|X'(t)\|_B^2\) 统一支付，若根集有最小元则可固定支付该根。 ||| This conclusion is independent of root count and minimum separation. For an arbitrary root set, define the extended nonnegative sum as the supremum over finite subsets; the first selected root can be paid uniformly by \(\sup_{X(t)=0}\|X'(t)\|_B^2\), and if the root set has a least element, that root can be paid as a fixed term.
这里 \(\mathcal E_Q=\int_I|hQF|\)，\(\mathcal C_\times=|\delta|\int_I|hP_0V^2F|\)。结论不使用 root count、root separation、复解析锚点或统一相位；\(\delta=0\) 不在定理量词内。 ||| Here \(\mathcal E_Q=\int_I|hQF|\) and \(\mathcal C_\times=|\delta|\int_I|hP_0V^2F|\). The conclusion uses no root count, root separation, complex-analytic anchor, or common phase; \(\delta=0\) lies outside the theorem's quantifiers.
正式附图分开展示方向投影、sharpness 与完整物理衰减 ||| The formal figure separately shows directional projection, sharpness, and complete physical decay
状态 · R0.72K 定理完成 ||| Status · R0.72K theorem complete
Banach-valued directional lemma 是抽象解析定理；complete-root consequence 限于 exact finite triangular 2.5D class，common-band no-go 还要求 row alignment、heat-stable multiplier 与 \(gB/R^2\le\gamma_0\)。 ||| The Banach-valued directional lemma is an abstract analytic theorem; the complete-root consequence is limited to the exact finite triangular 2.5D class, and the common-band no-go additionally requires row alignment, a heat-stable multiplier, and \(gB/R^2\le\gamma_0\).
R0.72J 已经控制 mixed row 与 true cubic，却没有把复值目标的全部时间根装进一个账本。我在每个相邻根隙末端选择导数的 norming functional；它的实投影在该根隙上的平均值为零，因此可以用一次实中值论证支付右端根斜率。这个方向随根隙改变，不要求复导数本身消失，也不要求统一相位、根分离或根数上界。 ||| R0.72J already controls the mixed row and true cubic, but does not place all time roots of the complex-valued target into one ledger. At the end of each adjacent root gap, I choose a norming functional for the derivative. Its real projection has zero mean on that gap, so one real mean-value argument pays the slope at the right-hand root. The direction varies from gap to gap and requires neither a vanishing complex derivative nor a common phase, root separation, or a bound on root count.
R0.72J 只控制 continuous cubic row，不能据此声称全部 complex roots 已被支付。本节提供一个 root-count-independent 抽象引理，并把它精确接到 triangular row equations，所以 complete-root 结论现在覆盖任意物理相位。 ||| R0.72J controls only the continuous cubic row, so it cannot by itself show that all complex roots are paid. This section gives an abstract lemma independent of root count and connects it exactly to the triangular row equations, so the complete-root conclusion now covers arbitrary physical phases.
R0.72K｜每个复根隙只需要自己的实方向 ||| R0.72K | Each complex root gap needs only its own real direction
R0.72L：离开 perturbative common band，先检查 strong coupling ||| R0.72L: Leave the perturbative common band and test strong coupling first
triangular target 的两个精确行方程为 ||| The two exact row equations for the triangular target are
01 · 二十七个研究阶段 ||| 01 · Twenty-seven research phases
02 · 101 节完整索引 ||| 02 · Complete 101-note index
把引理用于 \(e^{\lambda_0(x-A)}F_0\)，得到 \(G_{\rm all}^{\rm ex}\le E_A\rho_A^2+2\mathcal E_Q+2\mathcal C_\times\)。common-band mixed-parity class 中 \(G_{\rm all}^{\rm ex}\asymp a^2N^2\)、\(\mathcal J_{\rm all}\asymp g^2N/R^2\)，完整物理归一化比仍至多为 \(CR^{-4/9}(1+\log R)^{-2/3}\)。 ||| Applying the lemma to \(e^{\lambda_0(x-A)}F_0\) gives \(G_{\rm all}^{\rm ex}\le E_A\rho_A^2+2\mathcal E_Q+2\mathcal C_\times\). In the common-band mixed-parity class, \(G_{\rm all}^{\rm ex}\asymp a^2N^2\) and \(\mathcal J_{\rm all}\asymp g^2N/R^2\), while the fully physically normalized ratio remains at most \(CR^{-4/9}(1+\log R)^{-2/3}\).
保留 R0.72J 历史回顾 ||| Retain the R0.72J historical recap
查看 R0.72K 双路证书 ||| View the R0.72K two-route certificate
打开最新节点 R0.72K ||| Open the latest node, R0.72K
二十七个阶段、101 个节点：从约化递推和时间迹账本，到 critical-log candidate，再到 complete complex-target root ledger。 ||| Twenty-seven phases and 101 nodes: from reduced recurrences and temporal-trace ledgers to the critical-log candidate and then the complete complex-target root ledger.
方向采样已经脱离根数和 carrier 数。下一步应测试 \(gB/R^2\not\ll1\) 时，mixed row 与 true cubic 是否仍能由完整能量和 critical-log action 支付。 ||| Directional sampling is now independent of root count and carrier count. The next step should test whether the mixed row and true cubic can still be paid by the full energy and critical-log action when \(gB/R^2\not\ll1\).
复目标根的量词缺口已经闭合，common-band 完整反族路线被排除 ||| The quantifier gap for complex-target roots is closed, and the complete common-band counterfamily route is excluded
回顾截止节点：R0.72K ||| Recap endpoint: R0.72K
回顾截止时公开笔记：161 ||| Public notes at the recap endpoint: 161
截至 R0.72K，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 101 个节点或 63 个公开版本解释成对千禧年问题完成了某个比例。 ||| Through R0.72K, there is no new unconditional continuation criterion, no reduction of the set of all potential singular solutions, and no proof of finite-time breakdown. The 101 nodes or 63 public releases cannot be interpreted as a percentage completion of the Millennium Problem.
累计回顾 · R0.61–R0.72K · 2026-08-27 ||| Cumulative recap · R0.61–R0.72K · 2026-08-27
若 strong coupling 不能闭合，再把 joint heat exposure 展开到多个 separated shells；不能把 common-band 结论直接外推到多尺度。 ||| If strong coupling does not close, expand the joint heat exposure across multiple separated shells; the common-band conclusion cannot be extrapolated directly to multiple scales.
收录节点：101 ||| Included nodes: 101
我没有把 complex Rolle 当作前提。对每个相邻根隙，我在右端导数方向上选一个 norming functional；其实值投影的平均值为零，因此 \(\sum_{j=2}^m\|X'(t_j)\|^2\le2\int\|X'\|\|X''\|\)。系数 2 在 \(W^{2,1}\) 类中尖锐，首个所选根必须另付。 ||| I do not assume complex Rolle. On each adjacent root gap, I choose a norming functional in the direction of the right-endpoint derivative. Its real projection has zero mean, hence \(\sum_{j=2}^m\|X'(t_j)\|^2\le2\int\|X'\|\|X''\|\). The factor 2 is sharp in the \(W^{2,1}\) class, and the first selected root requires a separate payment.
新的可复用结果是 zero-count-independent directional derivative-mass theorem。它不依赖复导数零点，并把 finite triangular class 的 mixed row 与 true cubic 付款扩展到全部 complex target roots。 ||| The new reusable result is a directional derivative-mass theorem independent of zero count. It does not rely on zeros of the complex derivative and extends the mixed-row and true-cubic payment in the finite triangular class to every complex target root.
这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72K 的 101 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。这里的节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。 ||| This page follows the phase recap for R0.00–R0.60 and organizes the research nodes from R0.61 through R0.72K, 101 in total. I record chronologically what each segment actually proves, which proposals are excluded by concrete counterexamples or scaling analysis, and which conditions have not been derived from the Navier–Stokes equations. Node status describes the type of evidence and does not misstate release archiving as completion of a phase objective.
common-band coherent block 的完整根账本没有存活。下一障碍是 strong coupling；multiscale separated heat windows 保留为并列后续接口。 ||| The complete root ledger of the common-band coherent block does not survive. The next obstruction is strong coupling; multiscale separated heat windows remain a parallel subsequent interface.
R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 101 个节点沿着这个缺口推进；R0.70A–R0.72K 的 63 个版本已经公开；其中 39 个满足当前 formal-figure 完整封存合同，但其中仍包含条件定理、反例、有限诊断和开放缺口。 ||| The material from R0.00–R0.60 remains in the previous phase recap. The conclusion at R0.60 is that the full Fourier–Leray structure and higher-order computations can continue, but the critical quantity for general three-dimensional solutions is not yet controlled. The subsequent 101 nodes advance along this gap; from R0.70A–R0.72K, 63 releases are public, and 39 satisfy the current formal-figure complete-archive contract, while still including conditional theorems, counterexamples, finite diagnostics, and open gaps.
R0.60 之后的路线分成二十七个阶段 ||| The route after R0.60 divides into twenty-seven phases
R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72K 的 101 个研究节点；最新一节以 directional zero sampling 闭合 complete complex-target root ledger。 ||| Research recap after R0.60: complete coverage from R0.61 through R0.72K, totaling 101 research nodes; the latest section closes the complete complex-target root ledger through directional zero sampling.
R0.61–R0.72K 的 101 节公开笔记 ||| Public notes from R0.61–R0.72K: 101
R0.61–R0.72K 回顾 · 2026-08-27 ||| R0.61–R0.72K recap · 2026-08-27
R0.61–R0.72K 研究节点 ||| R0.61–R0.72K research nodes
R0.61–R0.72K｜R0.60 之后的研究回顾 ||| R0.61–R0.72K | Research recap after R0.60
R0.70A–R0.72K 的 63 节 HTML/PDF 与研究源稿列入公开路线。按当前 formal-figure 合同，39 节完整封存；24 节较早版本仍列入可审计的旧档回补清单。 ||| From R0.70A–R0.72K, 63 HTML/PDF releases and research source drafts are on the public route. Under the current formal-figure contract, 39 are fully archived; 24 earlier releases remain on the auditable legacy-backfill list.
R0.70A–R0.72K 已公开版本 ||| Published releases from R0.70A–R0.72K
R0.72K · 方向零点采样与完整复目标根账本 ||| R0.72K · Directional zero sampling and the complete complex-target root ledger
R0.72K 的 complete-root theorem 限于 exact finite triangular 2.5D class；物理 no-go 还限于 perturbative common-band assumptions。它没有证明 multiscale、strong coupling 或一般三维 Navier–Stokes 的全局光滑性；Clay 正式问题仍然开放。 ||| The complete-root theorem of R0.72K is limited to the exact finite triangular 2.5D class; the physical no-go is further limited to perturbative common-band assumptions. It proves neither multiscale or strong-coupling control nor global smoothness for general three-dimensional Navier–Stokes; the official Clay problem remains open.
R0.72K 的 directional root-slope theorem：对实或复 Banach-valued \(W^{2,1}\) 曲线，每个根隙使用自己的 norming direction，全部右端根的 derivative mass 由 \(2\int\|X'\|\|X''\|\) 支付；系数 2 尖锐，首根项必要。这个引理把 R0.72H–J 的 continuous-row bounds 升级成 complete complex-target ledger，并在 common band 内给出统一物理衰减。 ||| The directional root-slope theorem of R0.72K: for a real or complex Banach-valued \(W^{2,1}\) curve, each root gap uses its own norming direction, and the derivative mass at all right-endpoint roots is paid by \(2\int\|X'\|\|X''\|\); the factor 2 is sharp and the first-root term is necessary. This lemma upgrades the continuous-row bounds of R0.72H–J to a complete complex-target ledger and gives uniform physical decay in the common band.
R0.72K 附图 ||| R0.72K figure
R0.72K 证书 ||| R0.72K certificate
R0.72L 先检查 strong coupling 的 continuous-row ledger ||| R0.72L first tests the continuous-row ledger under strong coupling
从 cubic no-go 走到 directional sampling 与 complete complex-root closure ||| From the cubic no-go to directional sampling and complete complex-root closure
定理限于 exact finite triangular class；strong coupling、multiscale 与一般三维正则性仍然开放。 ||| The theorem is limited to the exact finite triangular class; strong coupling, multiple scales, and general three-dimensional regularity remain open.
对 \(X\in W^{2,1}(I;B)\) 的每个相邻根隙，我用右端导数的 norming functional 定义实投影。零端点使投影导数的平均值为零，由此得到 \(\sum_{j=2}^m\|X'(t_j)\|^2\le2\int\|X'\|\|X''\|\)。系数 2 尖锐，首根项必要。 ||| On each adjacent root gap of \(X\in W^{2,1}(I;B)\), I define a real projection using a norming functional for the right-endpoint derivative. The zero endpoints make the projected derivative have zero mean, yielding \(\sum_{j=2}^m\|X'(t_j)\|^2\le2\int\|X'\|\|X''\|\). The factor 2 is sharp and the first-root term is necessary.
方向零点采样闭合 complete complex-target ledger；common-band 完整物理根账本统一衰减。 ||| Directional zero sampling closes the complete complex-target ledger; the complete common-band physical root ledger decays uniformly.
复导数不必为零；每个根隙只需要自己的实投影 ||| The complex derivative need not vanish; each root gap needs only its own real projection
环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \(M^{-2}\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → phase-uniform \(M^{-8/3}\) sharp algebraic prefactor → shifted Rudin–Shapiro heat pulse → positive-time simple root → full-charge normalized order-one saturation → fixed-carrier shell isolation → negative-Sobolev action decay → candidate D^{1/3}Λ₁ payment failure → critical-log repair → selected-family frontier → complete-root Rolle–BV closure → sharp critical-log saturation → carrier-free mixed-row payment → action-only no-go → termwise physical-absorption no-go → parity repair → gcd-reduced Cayley classification → triangle-return criterion → common-band cubic no-go → directional zero sampling → complete complex-root ledger ||| Annular exclusion → source-kernel ledger → covariance-spectrum stratification → all-frequency conditional bridge → response-slope chord gain → common-response order-one channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \(M^{-2}\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → phase-uniform \(M^{-8/3}\) sharp algebraic prefactor → shifted Rudin–Shapiro heat pulse → positive-time simple root → full-charge normalized order-one saturation → fixed-carrier shell isolation → negative-Sobolev action decay → candidate D^{1/3}Λ₁ payment failure → critical-log repair → selected-family frontier → complete-root Rolle–BV closure → sharp critical-log saturation → carrier-free mixed-row payment → action-only no-go → termwise physical-absorption no-go → parity repair → gcd-reduced Cayley classification → triangle-return criterion → common-band cubic no-go → directional zero sampling → complete complex-root ledger
检查 strong-coupling continuous-row ledger，并保留 multiscale heat windows 为后续接口。 ||| Test the strong-coupling continuous-row ledger and retain multiscale heat windows as a subsequent interface.
静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71U–Z 依次处理 second-time jet、complete first row、fixed-small-coupling endpoint、selected roots 与 complete roots。R0.72A–C 建立 Bessel lower family、target-row participation 与 physical-phase sharp scales；R0.72D 再实现 positive-time root 与 full-charge order-one saturation。R0.72E 固定 \(q_0>R_*\)，用 Feynman–Kac、驻相和定量 Hörmander density 控制完整 \(H^{-1}\) action；exact one-carrier family 最终使 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。R0.72F 随后证明 selected roots 强制 \(1/3\) 下端点，而 Leray energy 只支付到 \(1/2\)；最小边界修正是 \(s^{-1/3}[1+\log(1/s)]\)。R0.72G 固定这一候选，用实相位 gauge、目标行恒等式与 Rolle–BV 归约证明完整根质量 \(G_{\rm all}\asymp\log\delta\)，并在原始幅度序列上得到 complete-root sharp saturation。R0.72H 转入有限共轭配对多载波 mixed row，证明载波数无关的 moment-resolved 上界；全奇数 Rudin–Shapiro 族排除 action-only payment，并使所需 \(M\)-幂次达到同阶。R0.72I 逐项换回物理量，证明分离的 \(B_AQ_*\) 项不能统一吸收；joint exposure 与 odd-carrier parity 又证明真实 complete ledger 统一衰减。R0.72J 把 parity 修复提升为 gcd-reduced Cayley 图二分定理，区分 odd cycle 与 triangle return，并排除 common-band coherent cubic 反族。R0.72K 再对每个复根隙选择独立 norming direction，把 mixed row 与 true cubic 转成 complete complex-target ledger，并证明其 common-band 物理归一化比统一衰减。 ||| After the static annular family is rigorously excluded, the main line turns to covariance-rank stratification and the all-frequency projection bridge. R0.71U–Z successively treats the second-time jet, the complete first row, the fixed-small-coupling endpoint, selected roots, and complete roots. R0.72A–C establishes the Bessel lower family, target-row participation, and sharp physical-phase scales; R0.72D then realizes a positive-time root and full-charge order-one saturation. R0.72E fixes \(q_0>R_*\) and controls the complete \(H^{-1}\) action using Feynman–Kac, stationary phase, and a quantitative Hörmander density; the exact one-carrier family ultimately makes the complete-root ledger relative to the candidate \(D^{1/3}\Lambda_1\) payment diverge like \(R^{4/3}\). R0.72F then proves that selected roots force the lower endpoint \(1/3\), while Leray energy pays only up to \(1/2\); the minimal boundary repair is \(s^{-1/3}[1+\log(1/s)]\). R0.72G fixes this candidate and uses a real phase gauge, target-row identities, and the Rolle–BV reduction to prove that the complete root mass satisfies \(G_{\rm all}\asymp\log\delta\), obtaining sharp complete-root saturation for the critical log on the original amplitude sequence. R0.72H moves to the mixed row in a finite conjugate-paired multi-carrier system and proves a carrier-count-independent moment-resolved upper bound; an all-odd Rudin–Shapiro family excludes the action-only payment and attains the required \(M\)-power. R0.72I converts each term back to physical quantities, proves that the separated \(B_AQ_*\) term cannot be absorbed uniformly, and then uses joint exposure and odd-carrier parity to prove uniform decay of the true complete ledger. R0.72J upgrades the parity repair to a gcd-reduced Cayley-graph bipartiteness theorem, distinguishes an odd cycle from a triangle return, and excludes the common-band coherent cubic counterfamily. R0.72K then assigns an independent norming direction to each complex root gap, converts the mixed row and true cubic into a complete complex-target ledger, and proves uniform decay after common-band physical normalization.
累计回顾 R0.61–R0.72K · 2026-08-27 ||| Cumulative recap R0.61–R0.72K · 2026-08-27
累计回顾现在分为二十七个问题阶段，完整覆盖 R0.61–R0.72K。我保留了 R0.72E 的 unweighted-payment no-go、R0.72F 的 critical-log boundary、R0.72G–J 的 finite-carrier root/cubic 路线，并追加 R0.72K 的 directional zero sampling 与 complete complex-target ledger。R0.70A–R0.72K 共 63 个版本已公开；39 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。 ||| The cumulative recap now has twenty-seven problem phases and completely covers R0.61–R0.72K. It retains the unweighted-payment no-go of R0.72E, the critical-log boundary of R0.72F, and the finite-carrier root/cubic route of R0.72G–J, and adds the directional zero sampling and complete complex-target ledger of R0.72K. Across R0.70A–R0.72K, 63 releases are public; 39 satisfy the current formal-figure complete-archive contract, while 24 older figure archives remain on the backfill list.
离开 \(gB/R^2\le\gamma_0\) 的 perturbative window，检查 mixed row 与 true cubic 能否继续由完整能量和 critical-log action 支付；multiscale separated heat windows 保留为并列后续接口。 ||| Leave the perturbative window \(gB/R^2\le\gamma_0\) and test whether the mixed row and true cubic can still be paid by the full energy and critical-log action; retain multiscale separated heat windows as a parallel subsequent interface.
上次综述 v1.23 · 2026-08-27 ||| Previous review v1.23 · 2026-08-27
我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.72K 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。 ||| I also prepared a systematic review that places the classical theory, five literature strands, the candidate-elimination tree, progress from 2019—2026, and this site's R0.69P–R0.72K route on one diagram. The historical nodes R0.61–R0.69O remain in the cumulative recap.
下一步 R0.72L： ||| Next R0.72L:
研究笔记 R0.72K · 2026-08-27 ||| Research note R0.72K · 2026-08-27
应用于 integrating-factor target 后，\(G_{\rm all}^{\rm ex}\le E_A\rho_A^2+2\mathcal E_Q+2\mathcal C_\times\)。common-band complete root mass 为 \(a^2N^2\) 量级，完整 physical ratio 仍按 \(R^{-4/9}(1+\log R)^{-2/3}\) 统一衰减。 ||| Applied to the integrating-factor target, the theorem gives \(G_{\rm all}^{\rm ex}\le E_A\rho_A^2+2\mathcal E_Q+2\mathcal C_\times\). The common-band complete root mass has order \(a^2N^2\), while the full physical ratio still decays uniformly like \(R^{-4/9}(1+\log R)^{-2/3}\).
阅读 R0.72K 研究笔记 → ||| Read the R0.72K research note →
展开 71 篇公开笔记 ||| Expand 71 public notes
综述 v1.24 · 2026-08-27 ||| Review v1.24 · 2026-08-27
common-band 完整复根账本已经闭合并统一衰减；下一障碍是 strong coupling，随后才是 multiscale heat-window summation。 ||| The complete common-band complex-root ledger is closed and decays uniformly; the next obstruction is strong coupling, followed by multiscale heat-window summation.
R0.60 recap 之后的累计回顾收录 101 个节点；全站现有 161 篇公开研究笔记 ||| The cumulative recap after R0.60 contains 101 nodes; the site now has 161 public research notes
R0.70A–R0.72K：63 节已公开，39 节完整封存 ||| R0.70A–R0.72K: 63 published, 39 fully archived
R0.72K 已完成： ||| R0.72K complete:
R0.72K 已用逐根隙 directional projection 闭合 complete complex-target ledger；common-band 完整根质量虽为 \(a^2N^2\) 量级，物理 critical-log 归一化后仍统一衰减。 ||| R0.72K closes the complete complex-target ledger using a separate directional projection on each root gap; although the complete common-band root mass has order \(a^2N^2\), it still decays uniformly after physical critical-log normalization.
`;

const rawRows = translationRows
  .trim()
  .split("\n")
  .filter((row) => row.length > 0);
const additions = new Map(
  rawRows.map((row) => {
    const separator = " ||| ";
    const index = row.indexOf(separator);
    if (index < 1) throw new Error("Invalid translation row: " + row);
    return [row.slice(0, index), row.slice(index + separator.length)];
  }),
);
if (additions.size !== rawRows.length) {
  throw new Error("Duplicate Chinese keys in R0.72K translation rows");
}

function numericTokens(value) {
  return [...value.matchAll(/\p{N}+(?:[.,]\p{N}+)*/gu)].map(
    (match) => match[0],
  );
}

function sameTokens(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

const expectedFiles = [
  "literature-review.html",
  "notes/r0-72k.html",
  "recap-r0-61-r0-72k.html",
  "research-review.html",
];
for (const relative of expectedFiles) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.24')) {
    throw new Error(relative + ": expected i18n cache version v1.24");
  }
}

const source = await collectSiteStrings(publicDirectory);
const translations = JSON.parse(await readFile(translationPath, "utf8"));
const batchId = /^r072k\d+$/;
const retained = translations.filter((entry) => !batchId.test(entry.id));
const retainedByChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (retainedByChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.72K batch");
}

const missing = source.filter((entry) => !retainedByChinese.has(entry.zh));
const missingKeys = new Set(missing.map((entry) => entry.zh));
const uncovered = missing.filter((entry) => !additions.has(entry.zh));
const stale = [...additions.keys()].filter((zh) => !missingKeys.has(zh));
if (uncovered.length || stale.length || additions.size !== missing.length) {
  throw new Error(
    `R0.72K translation batch does not equal active missing set (${missing.length}):\n` +
      "UNCOVERED:\n" +
      uncovered.map((entry) => entry.zh).join("\n---\n") +
      "\nSTALE:\n" +
      stale.join("\n---\n"),
  );
}
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))];
if (!sameTokens(missingFiles, expectedFiles)) {
  throw new Error("Unexpected R0.72K source files: " + JSON.stringify(missingFiles));
}

const translatedEntries = missing.map((entry, index) => {
  const en = additions.get(entry.zh);
  if (!en.trim() || containsChinese(en)) {
    throw new Error("Blank or Chinese-containing English for: " + entry.zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("Collective English voice remains in: " + entry.zh);
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
    id: "r072k" + String(index + 1).padStart(3, "0"),
    en,
  };
});

const finalTranslations = [...retained, ...translatedEntries];
for (const field of ["id", "zh"]) {
  const values = finalTranslations.map((entry) => entry[field]);
  if (new Set(values).size !== values.length) {
    throw new Error("Duplicate final translation " + field);
  }
}

if (!checkOnly) {
  await writeFile(
    snapshotPath,
    JSON.stringify(
      missing.map(({ zh, count, files }) => ({ zh, count, files })),
      null,
      2,
    ) + "\n",
  );
  await writeFile(
    translationPath,
    JSON.stringify(finalTranslations, null, 2) + "\n",
  );
}
console.log(
  JSON.stringify({
    checkOnly,
    added: translatedEntries.length,
    total: finalTranslations.length,
    liveStrings: source.length,
    missingBefore: missing.length,
    missingAfter: 0,
    files: missingFiles,
  }),
);
