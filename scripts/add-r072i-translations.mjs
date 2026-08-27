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
  "scripts/i18n-snapshots/r072i-missing.json",
);

const translationRows = String.raw`
处理临界 Carleson/Besov 空间，不把本站 solution-dependent Lamb action 直接变成 \(B_A\) payment。 ||| treats critical Carleson/Besov spaces, but does not directly convert this site's solution-dependent Lamb action into a \(B_A\) payment.
打开 99 节完整索引 ||| Open the complete 99-note index
的 Couette threshold 与本节 arbitrary finite-carrier root sampling 量词不同。 ||| 's Couette threshold has different quantifiers from the arbitrary finite-carrier root sampling in this section.
的 helicity coercivity 需要 sign/sector 条件；arithmetic odd/even carrier parity 不是 helical sign。 ||| 's helicity coercivity requires sign/sector conditions; arithmetic odd/even carrier parity is not a helical sign.
的 time analyticity 不能支付 complete zero-slope sum。 ||| 's time analyticity does not pay for the complete zero-slope sum.
的固定 observation admissibility 也不能消去时变 shear-row norm。 ||| 's fixed-observation admissibility likewise cannot remove the time-dependent shear-row norm.
开放接口 · R0.72J ||| Open interface · R0.72J
累计回顾与 99 节索引 ||| Cumulative recap and 99-note index
全奇 \(\delta=M\) 族使分离 \(B_AQ_*\) 正项的 normalized ratio 按 \(M^{1/2}\log M\) 发散；joint exposure 与 parity refinement 却给真实 \(G_{\rm all}^{\rm ex}\asymp M^2\) 和统一衰减的 physical ratio。 ||| In the all-odd \(\delta=M\) family, the normalized ratio of the separated positive \(B_AQ_*\) term diverges like \(M^{1/2}\log M\); joint exposure and parity refinement instead give the true \(G_{\rm all}^{\rm ex}\asymp M^2\) and a uniformly decaying physical ratio.
文献综述 v1.22 · 2026-08-27 ||| Literature review v1.22 · 2026-08-27
我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.72I 只列为研究笔记。我不把计算或笔记外推成正则性定理。 ||| I list published theorems as known results, mark 2026 preprints separately, and list R0.69P–R0.72I on this site only as research notes. I do not extrapolate computations or notes into regularity theorems.
限定一手来源检索未发现同时给出 carrier-uniform \(B_A\) absorption、endogenous complete-root sampling 和 all-odd parity repair 的定理。本节只证明 exact triangular 2.5D class 内的 method obstruction 与 special-family repair；这是 bounded non-collision check，不是原创性、优先权或穷尽性声明。 ||| The bounded primary-source search found no theorem simultaneously giving carrier-uniform \(B_A\) absorption, endogenous complete-root sampling, and an all-odd parity repair. This section proves only a method obstruction and a special-family repair within the exact triangular 2.5D class; this is a bounded non-collision check, not a claim of novelty, priority, or exhaustiveness.
直接检查 \(|\delta|\int|hP_0V^2F|\) 的 carrier graph、hybrid payment 与 actual normalized counterfamily。 ||| Directly test the carrier graph, hybrid payment, and actual normalized counterfamily for \(|\delta|\int|hP_0V^2F|\).
中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–U 给出 conditional incidence、genuine internal-entry、second-time-jet 与 finite recurrence 边界。R0.71V–W 分离 fixed zero-level trace 并排除 data-uniform complete first-row ledger。R0.71X 在 fixed-dimensional small-coupling family 内达到 one-third endpoint；R0.71Y 处理 selected roots；R0.71Z 给出 all-root slope-mass bound 和 launch-inclusive floor cancellation；R0.72A 把 strong-coupling loss 局部化到实际观察层，R0.72B 保留 exact target-row participation，R0.72C 得到 phase-uniform exact-launch \(M^{-8/3}\) 与 fixed-positive tail \(M^{-3}\) 的 sharp algebraic scales。R0.72D 在 shifted Rudin–Shapiro family 上构造 positive-time exact root，保留 full rotational charge，并得到非消失但不发散的 normalized complete-root ledger。R0.72E 回到 fixed-carrier Bessel family，以定量 negative-Sobolev action 证明 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。R0.72F 再用 regularly varying initial-layer weights 分离 selected-root 的 \(1/3\) 阈值与 Leray payment 的 \(1/2\) 阈值，并选出 critical-log 最小边界。R0.72G 在 exact real one-carrier lattice 上用 phase gauge、目标行恒等式与 Rolle–BV 归约证明完整根质量恰为对数量级，并得到 critical-log complete-root sharp saturation。R0.72H 在有限共轭配对多载波系统中证明 mixed row 的载波数无关 moment-resolved payment；全奇数 Rudin–Shapiro 族排除 action-only 版本，并使该 moment 所编码的载波幂次达到同阶。R0.72I 证明分离的 \(B_AQ_*\) 正项不能逐项物理吸收，同时用 joint exposure 和 odd-carrier parity 证明真实 complete ledger 统一衰减。一般 Navier–Stokes 正则性仍开放。 ||| . R0.69P–R0.71P reaches the positive-entry temporal-packing boundary, and R0.71Q–U gives the boundaries for conditional incidence, genuine internal entry, the second-time jet, and finite recurrence. R0.71V–W separates the fixed zero-level trace and excludes a data-uniform complete first-row ledger. R0.71X reaches the one-third endpoint in a fixed-dimensional small-coupling family; R0.71Y treats selected roots; R0.71Z gives an all-root slope-mass bound and launch-inclusive floor cancellation. R0.72A localizes the strong-coupling loss to the actual observation layer, R0.72B retains exact target-row participation, and R0.72C obtains the sharp algebraic scales \(M^{-8/3}\) for phase-uniform exact launch and \(M^{-3}\) for the fixed-positive tail. R0.72D constructs a positive-time exact root in a shifted Rudin–Shapiro family, retains the full rotational charge, and obtains a nonvanishing but nondivergent normalized complete-root ledger. R0.72E returns to a fixed-carrier Bessel family and uses a quantitative negative-Sobolev action estimate to make the complete-root ledger relative to the candidate \(D^{1/3}\Lambda_1\) payment diverge like \(R^{4/3}\). R0.72F then uses regularly varying initial-layer weights to separate the selected-root threshold \(1/3\) from the Leray-payment threshold \(1/2\), selecting the minimal critical-log boundary. On the exact real one-carrier lattice, R0.72G uses a phase gauge, target-row identities, and the Rolle–BV reduction to prove that the complete root mass has exactly logarithmic order and obtains sharp critical-log complete-root saturation. In a finite conjugate-paired multi-carrier system, R0.72H proves a carrier-count-independent moment-resolved payment for the mixed row; an all-odd Rudin–Shapiro family excludes the action-only version and attains the carrier power encoded by that moment. R0.72I proves that the separated positive \(B_AQ_*\) term cannot be absorbed physically term by term, while joint exposure and odd-carrier parity prove that the true complete ledger decays uniformly. General Navier–Stokes regularity remains open.
R0.72I 的 physical absorption 与 parity 边界 ||| Physical-absorption and parity boundary of R0.72I
R0.72I 的主源边界 ||| Primary-source boundary for R0.72I
termwise physical-absorption no-go 与 odd-carrier repair ||| Termwise physical-absorption no-go and odd-carrier repair
· common-size 最大相对差 \(1.61\times10^{-4}\) ||| · maximum common-size relative difference \(1.61\times10^{-4}\)
“termwise absorption is false” 与 “the physical inequality is false” 是两句话。当前只证明第一句。对本页全奇数族，第二句恰好不成立：实际归一化账本趋于零。 ||| “Termwise absorption is false” and “the physical inequality is false” are two different statements. Only the first is proved here. For the all-odd family on this page, the second is actually false: the genuinely normalized ledger tends to zero.
\(V\) 交换奇偶，\(V^2\) 保持奇偶 ||| \(V\) swaps parity; \(V^2\) preserves it
00 · 两句判断 ||| 00 · Two conclusions
01 · 全奇数物理族 ||| 01 · All-odd physical family
02 · 物理 lift 与 action ||| 02 · Physical lift and action
03 · 逐项吸收失败 ||| 03 · Failure of termwise absorption
04 · 联合暴露修复 ||| 04 · Joint-exposure repair
05 · 奇偶分裂修复 ||| 05 · Parity-splitting repair
06 · 完整物理定理 ||| 06 · Complete physical theorem
07 · 有限审计 ||| 07 · Finite audit
13 · 复现入口 ||| 13 · Reproduction
把 (H.6.5) 的四项记为 ||| Denote the four terms in (H.6.5) by
版本 v0.72I · 2026-08-27 ||| Version v0.72I · 2026-08-27
本节定位了损失发生在哪一步，而不是只得到一个失败符号 ||| This section locates the step where the loss occurs, instead of merely recording a failed inequality
不等于真实账本很大 ||| does not mean the true ledger is large
不要把短时同时暴露拆成两个全局范数 ||| Do not split simultaneous short-time exposure into two global norms
查看数据、代码、QA、manifest 与 SHA-256 ||| View the data, code, QA, manifest, and SHA-256
抽象根质量先经过一个精确物理换算 ||| The abstract root mass first undergoes an exact physical conversion
处理 helical symmetry 或单方向慢变的特殊大数据类。这些结构都不直接推出本页的 all-odd complete-root theorem，更不解决混合 parity 的 generic \(B_A\) replacement。 ||| treat special large-data classes with helical symmetry or slow variation in one direction. None of these structures directly implies the all-odd complete-root theorem on this page, still less the generic \(B_A\) replacement for mixed parity.
处理固定 observation 的 square function 与 Laplace–Carleson admissibility。这里的行由时变 \(V_M,V_M'\) 生成，采样点还是被观测坐标自己的零点。抽象 observation norm 只会重新容纳 \(B_A\)，不会自动消掉它。 ||| treat square functions and Laplace–Carleson admissibility for a fixed observation. Here the row is generated by time-dependent \(V_M,V_M'\), and the sampling points are the zeros of the observed coordinate itself. An abstract observation norm merely accommodates \(B_A\) again; it does not remove it automatically.
打开 SVG ||| Open SVG
大物理振幅与小总暴露可以同时存在 ||| Large physical amplitude and small total exposure can coexist
当 \(g_M\le\gamma_0M^{3/2}\) 时，右边至多为 \(Cg_M^2/M\le CM^2\)。对 \(g_M=M\)，真实 cubic payment 只有 \(O(M)\)；分离后的 \(g_MB_0Q_*\) 却是 \(\asymp M^{19/6}\log M\)。这里量化了 Cauchy–Schwarz 丢掉的结构。 ||| When \(g_M\le\gamma_0M^{3/2}\), the right side is at most \(Cg_M^2/M\le CM^2\). For \(g_M=M\), the true cubic payment is only \(O(M)\), whereas the separated \(g_MB_0Q_*\) is \(\asymp M^{19/6}\log M\). This quantifies the structure lost by Cauchy–Schwarz.
的 \(BMO^{-1}\) heat-extension tent norm，以及 ||| 's \(BMO^{-1}\) heat-extension tent norm, and
的 Couette threshold 固定背景剪切，并要求高 Sobolev 小扰动。 ||| 's Couette threshold fixes a background shear and requires a small perturbation in high Sobolev regularity.
的 helicity 控制需要 sector dominance 或 helical decimation；一般 helicity 不正定，也不同于本页的奇偶载波 parity。 ||| 's helicity control requires sector dominance or helical decimation; general helicity is not positive definite and also differs from the odd/even carrier parity on this page.
的 negative-Besov self-improvement，说明临界热尺度和时间加权估计是严格工具。它们没有把本页的 solution-dependent quotient action 变成标准 Besov norm，也不支付 \(B_A\)。 ||| 's negative-Besov self-improvement shows that critical heat scales and time-weighted estimates are rigorous tools. They do not turn the solution-dependent quotient action on this page into a standard Besov norm, nor do they pay for \(B_A\).
的时间解析性只能使非平凡内点根孤立，不能给出无分离的平方斜率总和。 ||| 's time analyticity only makes nontrivial interior roots isolated; it does not give an unseparated sum of squared slopes.
第一条修复保留真实联合暴露： ||| The first repair retains the true joint exposure:
定义 canonical lift ||| Define the canonical lift
动态生成的偶分量满足 ||| The dynamically generated even component satisfies
都满足 ||| all satisfy
独立路线改用 binary-\(11\) parity generator、real-gauge RK45 与 Gauss–Legendre 积分。\(M=64\) 时 \(Q_*=57.3302314\)、\(\delta\int|hb|=0.1646408965\)，实测 cubic 归一化比为 \(1.13\times10^{-7}\)，根残差为 \(1.13\times10^{-16}\)。 ||| The independent route instead uses a binary-\(11\) parity generator, real-gauge RK45, and Gauss–Legendre integration. At \(M=64\), \(Q_*=57.3302314\), \(\delta\int|hb|=0.1646408965\), the measured normalized cubic ratio is \(1.13\times10^{-7}\), and the root residual is \(1.13\times10^{-16}\).
而 \(D_M^{1/3}\Lambda_{1,*}\asymp M^{5/3}\)。前三项的归一化比都趋于零。最后一项满足 ||| while \(D_M^{1/3}\Lambda_{1,*}\asymp M^{5/3}\). The normalized ratios of the first three terms all tend to zero. The final term satisfies
而不是只测它的 \(B_AQ_*\) 分离上界。只有真实 cubic row 在物理归一化后仍然存活，才构成新的负结果。 ||| rather than measuring only its separated \(B_AQ_*\) upper bound. A new negative result requires the true cubic row itself to survive physical normalization.
而对角耗散 \(D\) 保持 parity。目标指标是偶数。于是 ||| while the diagonal dissipation \(D\) preserves parity. The target index is even. Therefore
返回 R0.72H ||| Return to R0.72H
分离 \(B_AQ_*\) 归一化比 ||| Normalized separated \(B_AQ_*\) ratio
固定区间、目标 multiplier、背景和几何。存在 \(\gamma_0>0\)，使所有 ||| Fix the interval, target multiplier, background, and geometry. There exists \(\gamma_0>0\) such that every
截至 2026-08-27 的限定一手来源检索中，我没有找到同时完成上述两件事的定理。这是 bounded non-collision check，不是原创性、优先权或穷尽性声明。 ||| In the bounded primary-source search through 2026-08-27, I found no theorem that simultaneously accomplishes the two tasks above. This is a bounded non-collision check, not a claim of novelty, priority, or exhaustiveness.
精确内点根给出反向下界。于是 \(G_{{\rm all},M}^{\rm ex}\asymp M^2\)。旧公式的发散来自把短 joint exposure 拆成 \(B_0Q_*\)，不是来自真实根质量。 ||| The exact interior root gives the reverse lower bound. Hence \(G_{{\rm all},M}^{\rm ex}\asymp M^2\). The divergence in the old formula comes from splitting the short joint exposure into \(B_0Q_*\), not from the true root mass.
两条独立实现都通过，并保留有限计算的边界 ||| Both independent implementations pass, with the limits of the finite computation retained
两条修复给出同一答案。联合暴露路线保留 \(\rho(x)\|V(x)\|\) 的短时重叠。parity 路线识别 \(h\) 与 \(P_0V^2F\) 实际读取不同格点颜色。它们都解释了为什么正项 Cauchy–Schwarz 分解会多付巨大代价。 ||| The two repairs give the same answer. The joint-exposure route retains the short-time overlap of \(\rho(x)\|V(x)\|\). The parity route recognizes that \(h\) and \(P_0V^2F\) actually read different lattice colors. Both explain why the positive-term Cauchy–Schwarz decomposition overpays by a large amount.
邻近理论没有直接给出 parity repair 或一般 \(B_A\) 吸收 ||| Nearby theories do not directly provide the parity repair or general \(B_A\) absorption
令 \(z=g_M^2M^{-7/3}\log M\)。因为 \(z^{2/3}/(1+z)\) 有界，得到统一上界 ||| Set \(z=g_M^2M^{-7/3}\log M\). Since \(z^{2/3}/(1+z)\) is bounded, this gives the uniform upper bound
没有证明 ||| Not proved
模型 ||| Model
取 \(g_M=M\)。四个物理 lift 的量级依次为 ||| Take \(g_M=M\). The four physical lifts have respective orders
取 \(M=2^n\)，把 Rudin–Shapiro 符号放在全奇数块 ||| Take \(M=2^n\) and place the Rudin–Shapiro signs on an all-odd block
全频 projected-Lamb action 不是只看目标坐标。对当前族，完整量仍有同一尺度： ||| The full-frequency projected-Lamb action does not inspect only the target coordinate. For the present family, the complete quantity still has the same scale:
全奇数扰动分支的完整归一化账本一致趋零 ||| The complete normalized ledger on the all-odd perturbative branch tends uniformly to zero
任意载波集上的 generic \(B_AQ_*\) replacement；所有有限三角形流的 physical critical-log inequality；该物理不等式的反例；非三角形 restart covering；一般三维 continuation criterion；有限时奇性或千禧年问题解答。 ||| a generic \(B_AQ_*\) replacement on arbitrary carrier sets; the physical critical-log inequality for every finite triangular flow; a counterexample to that physical inequality; non-triangular restart covering; a general three-dimensional continuation criterion; finite-time singularity; or a solution of the Millennium Problem.
失败只来自分离后的 \(B_AQ_*\) 正项 ||| The failure comes only from the separated positive \(B_AQ_*\) term
随后比较两条路线：一条寻找 critical action 与 joint exposure 的 hybrid minimum bound；另一条构造 mixed-parity block，直接测量 ||| I will then compare two routes: one seeks a hybrid minimum bound between critical action and joint exposure; the other constructs a mixed-parity block and directly measures
所以在扰动窗口内 ||| Therefore, throughout the perturbative window,
所有载波都是奇数。因此 ||| Every carrier is odd. Therefore
特殊全奇数分支已闭合，一般载波仍开放 ||| The special all-odd branch is closed; general carriers remain open
同一张图分开显示“发散上界”和“衰减实量” ||| One figure separately shows the “divergent upper bound” and the “decaying true quantity”
同一族的真实完整账本满足 \(\mathcal J_{\rm all}/(D^{1/3}\Lambda_{1,*})\asymp M^{-2/3}\)。在整个扰动窗口内还有统一趋零率。 ||| The true complete ledger of the same family satisfies \(\mathcal J_{\rm all}/(D^{1/3}\Lambda_{1,*})\asymp M^{-2/3}\). It also has a uniform decay rate throughout the perturbative window.
图 R0.72I-1。A：四个 lifted 正项中只有 generic \(B_A\) 项越过候选支付并增长；B：分离的 generic \(B_AQ_*\) 比实测 cubic exposure 粗至 \(2.06\times10^8\) 倍；C：parity-resolved BV 上账本和单个精确根 atom 都不继承这项损失；D：对完整 coupling window 优化后仍按 \(M^{-4/9}(\log M)^{-2/3}\) 衰减。实心圆为 producer，空心方块为 independent；有限点用于实现审计，解析结论来自 joint-exposure 与 parity 估计。 ||| Figure R0.72I-1. A: Among the four lifted positive terms, only the generic \(B_A\) term exceeds the candidate payment and grows. B: The separated generic \(B_AQ_*\) bound is up to \(2.06\times10^8\) times coarser than the measured cubic exposure. C: Neither the parity-resolved BV ledger nor the single exact-root atom inherits this loss. D: Optimization over the complete coupling window still decays like \(M^{-4/9}(\log M)^{-2/3}\). Filled circles denote the producer and open squares the independent route; the finite points audit the implementation, while the analytic conclusions follow from the joint-exposure and parity estimates.
完整数学源稿 ||| Complete mathematical source report
完整物理根账本与抽象根质量满足 ||| The complete physical root ledger and abstract root mass satisfy
我继续使用精确三角形 2.5D 类 ||| I continue to use the exact triangular 2.5D class
物理尺度 ||| Physical scale
物理振幅按 \(S_M^2K_{f,M}=3P_M^2K_v\)、\(P_M=g_M=|\delta_M|\) 平衡。于是 ||| Balance the physical amplitudes by \(S_M^2K_{f,M}=3P_M^2K_v\) and \(P_M=g_M=|\delta_M|\). Then
下一关要离开单一 parity coset ||| The next gate must leave a single parity coset
下载期刊 PDF ||| Download journal PDF
先拒绝一种证明路线，再保住真实完整账本 ||| First reject one proof route, then retain the true complete ledger
修复二 ||| Repair two
修复一 ||| Repair one
研究笔记 R0.72I · PHYSICAL ABSORPTION · PARITY REPAIR · COMPLETE ROOTS ||| Research note R0.72I · PHYSICAL ABSORPTION · PARITY REPAIR · COMPLETE ROOTS
研究笔记 R0.72I：R0.72H (6.5) 的正项上界不能逐项吸收到物理尺度，但同一全奇数 Rudin–Shapiro 族的真实完整根账本在 critical-log 归一化后趋于零。 ||| Research note R0.72I: the positive-term upper bound in R0.72H (6.5) cannot be absorbed term by term into the physical scale, but the true complete-root ledger of the same all-odd Rudin–Shapiro family tends to zero after critical-log normalization.
一个上界不能吸收， ||| An upper bound cannot be absorbed,
因此真实 cubic row 只有 ||| Therefore the true cubic row is only
因此最终物理支付量是 ||| Therefore the final physical payment is
有限格点覆盖 \(M=4,8,16,32,64,128\)。\(M=128\) 时，分离 \(B_AQ_*\) 的归一化比为 8.69826，而实测 parity-resolved BV 上账本比为 0.00356315。精确根残差为 \(6.77\times10^{-17}\)。 ||| The finite lattice covers \(M=4,8,16,32,64,128\). At \(M=128\), the normalized ratio of the separated \(B_AQ_*\) term is 8.69826, while the measured parity-resolved BV ledger ratio is 0.00356315. The exact-root residual is \(6.77\times10^{-17}\).
有限计算检查 scaling、parity exposure、精确根和物理 lift。它不枚举或认证完整根集，也不能替代解析 parity lemma。 ||| The finite computation checks scaling, parity exposure, the exact root, and the physical lift. It neither enumerates nor certifies the complete root set, and cannot replace the analytic parity lemma.
有限证书、配置、数据与运行日志 ||| Finite certificates, configuration, data, and run logs
源稿、证书、附图和累计回顾分别保留入口 ||| The source report, certificates, figure, and cumulative recap retain separate entry points
在诊断族 \(g_M=|\delta_M|=M\) 上，\(B_AQ_*\) 的物理 lift 除以 \(D^{1/3}\Lambda_{1,*}\) 按 \(M^{1/2}\log M\) 发散。公式 (H.6.5) 不能逐项闭合。 ||| On the diagnostic family \(g_M=|\delta_M|=M\), the physical lift of \(B_AQ_*\), divided by \(D^{1/3}\Lambda_{1,*}\), diverges like \(M^{1/2}\log M\). Formula (H.6.5) cannot be closed term by term.
这拒绝的是“把旧右端四项逐项吸收”的方法。它没有给出 \(\mathcal J_{\rm all}\) 的下界，也没有推翻物理 critical-log 候选。 ||| This rejects the method of “absorbing the four old right-hand terms one by one.” It gives no lower bound for \(\mathcal J_{\rm all}\) and does not overturn the physical critical-log candidate.
这里要避免一个逻辑错误。正项上界中的某一项很大，只能说明这个上界太粗。它不能推出左边也很大。 ||| A logical error must be avoided here. A large term in a positive upper bound only shows that the bound is too coarse. It does not imply that the left side is also large.
这仍是精确、全局光滑的三角形 2.5D 测试类。它没有证明一般三维物理不等式，也没有排除或构造 Navier–Stokes 奇性。 ||| This remains an exact, globally smooth triangular 2.5D test class. It neither proves the general three-dimensional physical inequality nor excludes or constructs a Navier–Stokes singularity.
这些比较在 \(0<g_M\le\gamma_0M^{3/2}\) 内对 \(M\) 和 \(g_M\) 一致。常数仍可依赖固定区间、几何、黏性和目标 multiplier。 ||| Within \(0<g_M\le\gamma_0M^{3/2}\), these comparisons are uniform in \(M\) and \(g_M\). The constants may still depend on the fixed interval, geometry, viscosity, and target multiplier.
诊断选择 \(g_M=M\) 虽然使物理能量增长，却有 \(\epsilon_M=M^{-1/2}\to0\)。所以它仍处在统一 Duhamel 扰动窗口内。 ||| Although the diagnostic choice \(g_M=M\) makes the physical energy grow, it has \(\epsilon_M=M^{-1/2}\to0\). It therefore remains inside the uniform Duhamel perturbative window.
诊断子族 \(g_M=M\) 的实际量级是 \(M^{-2/3}\)。这与上一节的 \(M^{1/2}\log M\) 发散发生在完全相同的参数上。二者比较，正是本节的主要结论。 ||| The actual scale of the diagnostic subfamily \(g_M=M\) is \(M^{-2/3}\). This occurs at exactly the same parameters as the \(M^{1/2}\log M\) divergence from the preceding section. Their comparison is the main conclusion of this section.
正式附图归档 ||| Formal figure archive
直接吸收失败说明 R0.72H (6.5) 不能原样成为物理定理。更重要的是，同一个族又证明真实账本很小。于是问题不再是“是否需要更大物理能量”，而是“怎样保留 cubic interaction 的共同时间暴露”。 ||| Failure of direct absorption shows that R0.72H (6.5) cannot become a physical theorem unchanged. More importantly, the same family proves that the true ledger is small. The question is therefore no longer “whether more physical energy is needed,” but “how to retain the common temporal exposure of the cubic interaction.”
状态 · R0.72I 解析结果完成 ||| Status · R0.72I analytic result complete
B_AQ_* 的分离上界太粗；保留联合暴露或利用奇偶分裂后，真实全奇数 complete-root ledger 反而衰减。 ||| The separated B_AQ_* upper bound is too coarse; after retaining joint exposure or using parity splitting, the true all-odd complete-root ledger instead decays.
complete-root Rolle 步仍要求兼容实 gauge 与 \(\delta_M\ne0\)。本定理用 \(g_M=|\delta_M|>0\) 明确保留这项条件。\(\delta_M=0\) 时物理 slope ledger 为零，但除去 \(\delta_M^2\) 后的 raw \(h\)-ledger 不是这里的对象。 ||| The complete-root Rolle step still requires a compatible real gauge and \(\delta_M\ne0\). The theorem explicitly retains this condition through \(g_M=|\delta_M|>0\). When \(\delta_M=0\), the physical slope ledger is zero, but after division by \(\delta_M^2\), the raw \(h\)-ledger is not the object considered here.
independent 源码 ||| Independent source code
parity-resolved BV 上账本比 ||| Parity-resolved BV ledger ratio
producer 源码 ||| Producer source code
R0.60 之后累计回顾 ||| Cumulative recap after R0.60
R0.72H (6.5) 的 \(B_AQ_*\) 正项不能逐项物理吸收；其余三项不是诊断族上的损失源；joint exposure 为 \(O(M^{-2})\)；在兼容实 gauge、\(\delta_M\ne0\) 下，全奇数 parity 给出真实 cubic-row 改进；完整 raw root mass 为 \(\asymp M^2\)；完整物理账本在整个扰动窗口内一致趋零。 ||| The positive \(B_AQ_*\) term in R0.72H (6.5) cannot be physically absorbed term by term; the other three terms are not the loss source on the diagnostic family; the joint exposure is \(O(M^{-2})\); under a compatible real gauge and \(\delta_M\ne0\), all-odd parity gives the true cubic-row improvement; the complete raw root mass is \(\asymp M^2\); and the complete physical ledger tends uniformly to zero throughout the perturbative window.
R0.72H 留下四个正项。我在同一个全奇数 Rudin–Shapiro 族上检查它们。结果分成两句。第一句：旧公式中的 \(B_AQ_*\) 项不能逐项吸收到 \(D^{1/3}\Lambda_{1,*}\)。第二句：这不是物理反例。保留真实联合暴露，或直接使用奇偶格点分裂后，完整物理根账本反而趋于零。当前剩余问题已经变成任意载波、尤其混合奇偶载波下的真实 cubic row。 ||| R0.72H leaves four positive terms. I test them on the same all-odd Rudin–Shapiro family. The result has two parts. First, the \(B_AQ_*\) term in the old formula cannot be absorbed term by term into \(D^{1/3}\Lambda_{1,*}\). Second, this is not a physical counterexample. After retaining the true joint exposure or directly using odd/even lattice splitting, the complete physical root ledger instead tends to zero. The remaining problem is now the true cubic row for arbitrary carriers, especially carriers of mixed parity.
R0.72H 已构造兼容实 gauge 的精确正时刻根： ||| R0.72H already constructs an exact positive-time root with a compatible real gauge:
R0.72H 在兼容实目标 sector 中得到 ||| R0.72H obtains, in a compatible real target sector,
R0.72I · 2026-08-27 · 个人数学研究日志 ||| R0.72I · 2026-08-27 · Personal mathematics research log
R0.72I｜吸收失败不等于物理反例 ||| R0.72I | Failure of absorption is not a physical counterexample
R0.72J 应先把任意载波集写成 residue graph。需要判断 \(V^2\) 何时把质量送回目标 sector，以及哪些 carrier combinations 破坏两色分裂。 ||| R0.72J should first write an arbitrary carrier set as a residue graph. It must determine when \(V^2\) returns mass to the target sector and which carrier combinations break the two-color splitting.
Rudin–Shapiro 热包络给 ||| The Rudin–Shapiro heat envelope gives
01 · 二十五个研究阶段 ||| 01 · Twenty-five research phases
02 · 99 节完整索引 ||| 02 · Complete 99-note index
保留 R0.72H 历史回顾 ||| Retain the historical R0.72H recap
查看 R0.72I 双路证书 ||| View the R0.72I dual-path certificates
打开最新节点 R0.72I ||| Open the latest node R0.72I
二十五个阶段、99 个节点：从约化递推和时间迹账本，到 unweighted payment 失效，再到 physical absorption no-go 与 odd-carrier repair。 ||| Twenty-five phases and 99 nodes: from reduced recurrences and the temporal-trace ledger, through failure of the unweighted payment, to the physical-absorption no-go and odd-carrier repair.
回顾截止节点：R0.72I ||| Recap endpoint: R0.72I
回顾截止时公开笔记：159 ||| Public notes at the recap endpoint: 159
截至 R0.72I，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 99 个节点或 61 个公开版本解释成对千禧年问题完成了某个比例。 ||| Through R0.72I, there is no new unconditional continuation criterion, no reduction of the full set of potential singular solutions, and no proof of finite-time breakdown. The 99 nodes or 61 published releases cannot be interpreted as a percentage completion of the Millennium Problem.
累计回顾 · R0.61–R0.72I · 2026-08-27 ||| Cumulative recap · R0.61–R0.72I · 2026-08-27
收录节点：99 ||| Included nodes: 99
同一全奇族的真实 complete ledger 已由 joint exposure 和 parity 两条路线封闭，并在完整 critical-log normalization 下统一衰减。当前障碍因此转到 mixed-parity carrier graph 的真实 cubic row，不是继续放大这个已经证伪的上界项。 ||| The true complete ledger of the same all-odd family is closed by both the joint-exposure and parity routes and decays uniformly under the full critical-log normalization. The present obstruction therefore moves to the true cubic row of the mixed-parity carrier graph, not to further amplification of the already-refuted upper-bound term.
我把 R0.72H 的四个正项逐一换回物理量。取全奇 Rudin–Shapiro 载波与 \(\delta=M\) 时，前三项都能支付；分离的 \(B_AQ_*\) 项却比 \(D^{1/3}\Lambda_{1,*}\) 多出 \(M^{1/2}\log M\)。因此固定 corollary 不能靠逐项吸收闭合。 ||| I convert the four positive terms from R0.72H back to physical quantities one by one. With all-odd Rudin–Shapiro carriers and \(\delta=M\), the first three terms are paid, but the separated \(B_AQ_*\) term exceeds \(D^{1/3}\Lambda_{1,*}\) by \(M^{1/2}\log M\). Thus the fixed corollary cannot be closed by termwise absorption.
下一步不再尝试吸收分离的 \(B_AQ_*\)。我会按载波的模二 residue graph 分解 \(V^2\) 返回目标行的路径，并直接估计 \(|\delta|\int|hP_0V^2F|\)。 ||| The next step will no longer try to absorb the separated \(B_AQ_*\). I will decompose the paths by which \(V^2\) returns to the target row according to the carriers' residue graph modulo two, and directly estimate \(|\delta|\int|hP_0V^2F|\).
下载期刊附图 ||| Download journal figure
一个正项分解被排除，但真实多载波账本没有随它发散 ||| One positive-term decomposition is excluded, but the true multi-carrier ledger does not diverge with it
有限关口是：证明 action 与 joint exposure 的 hybrid payment，或构造 mixed-parity family 使真实 cubic row 在完整物理归一化后仍不消失。只有真实量可以决定候选，不再用发散的正上界代替它。 ||| The finite gate is to prove a hybrid payment from action and joint exposure, or construct a mixed-parity family whose true cubic row remains nonvanishing after complete physical normalization. Only the true quantity can decide the candidate; a divergent positive upper bound will no longer stand in for it.
这个发散来自上界，不是真实根账本的下界。保留 joint heat exposure，或直接利用 \(V\) 翻转奇偶格点，可得 \(G_{\rm all}^{\rm ex}\asymp M^2\)。完整物理比值在整个 \(0<g\le\gamma_0M^{3/2}\) 窗口内至多为 \(CM^{-4/9}(\log M)^{-2/3}\)，所以同一族不是 critical-log 候选的反例。 ||| This divergence comes from an upper bound, not a lower bound for the true root ledger. Retaining joint heat exposure, or directly using the fact that \(V\) flips lattice parity, gives \(G_{\rm all}^{\rm ex}\asymp M^2\). Throughout the window \(0<g\le\gamma_0M^{3/2}\), the complete physical ratio is at most \(CM^{-4/9}(\log M)^{-2/3}\), so the same family is not a counterexample to the critical-log candidate.
这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72I 的 99 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。这里的节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。 ||| This page follows the R0.00–R0.60 phase recap and organizes R0.61 through R0.72I into 99 research nodes. I record chronologically what each segment actually proves, which proposals are excluded by explicit counterexamples or scale analysis, and which conditions have not yet been derived from the Navier–Stokes equations. Node status describes the evidence type; archival completion is not misreported as resolution of the research objective.
R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 99 个节点沿着这个缺口推进；R0.70A–R0.72I 的 61 个版本已经公开；其中 37 个满足当前 formal-figure 完整封存合同，但其中仍包含条件定理、反例、有限诊断和开放缺口。 ||| The material from R0.00–R0.60 remains in the previous phase recap. The conclusion at R0.60 is that the complete Fourier–Leray structure and higher-order computations can continue, but the critical quantity for general three-dimensional solutions is still uncontrolled. The following 99 nodes advance along that gap; from R0.70A–R0.72I, 61 releases are public, of which 37 satisfy the current formal-figure complete-archive contract, while still containing conditional theorems, counterexamples, finite diagnostics, and open gaps.
R0.60 之后的路线分成二十五个阶段 ||| The route after R0.60 has twenty-five research phases
R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72I 的 99 个研究节点；最新一节分离了失败的正项吸收与真实完整根账本，并在全奇载波族上证明后者统一衰减。 ||| Research recap after R0.60: complete coverage from R0.61 through R0.72I across 99 research nodes; the latest section separates the failed positive-term absorption from the true complete-root ledger and proves uniform decay of the latter on the all-odd carrier family.
R0.61–R0.72I 的 99 节公开笔记 ||| Public notes from R0.61 through R0.72I: 99
R0.61–R0.72I 回顾 · 2026-08-27 ||| R0.61–R0.72I recap · 2026-08-27
R0.61–R0.72I 研究节点 ||| R0.61–R0.72I research nodes
R0.61–R0.72I｜R0.60 之后的研究回顾 ||| R0.61–R0.72I | Research recap after R0.60
R0.70A–R0.72I 的 61 节 HTML/PDF 与研究源稿列入公开路线。按当前 formal-figure 合同，37 节完整封存；24 节较早版本仍缺 formal 状态或正式附图包，列入可审计的旧档回补清单。公开页存在不等于档案合同完整。 ||| From R0.70A–R0.72I, the 61 HTML/PDF releases and research source reports are included in the public route. Under the current formal-figure contract, 37 are fully archived; 24 earlier releases still lack formal status or a formal figure package and remain on the auditable legacy backfill list. A public page does not by itself imply a complete archival contract.
R0.70A–R0.72I 已公开版本 ||| Published releases from R0.70A–R0.72I
R0.72H 的 mixed-row theorem 本身保留。R0.72I 排除的是把 complete-root corollary 的四个正项逐项塞进 \(D^{1/3}\Lambda_{1,*}\) 的做法；其中 \(B_AQ_*\) 丢失了载波共同存在的短时间。 ||| The mixed-row theorem from R0.72H itself remains valid. R0.72I excludes the method of placing the four positive terms of the complete-root corollary into \(D^{1/3}\Lambda_{1,*}\) one by one; the \(B_AQ_*\) term loses the short interval during which the carriers coexist.
R0.72I · 物理吸收失败与全奇载波修复 ||| R0.72I · Failure of physical absorption and all-odd carrier repair
R0.72I 的 physical-absorption audit：在 \(\delta=M\) 的全奇 Rudin–Shapiro 族上，R0.72H 的分离 \(B_AQ_*\) 正项归一化后按 \(M^{1/2}\log M\) 发散，所以 fixed termwise absorption 路线失效。joint exposure 与 odd-carrier parity 两条解析路线却给出真实 \(G_{\rm all}^{\rm ex}\asymp M^2\)，完整物理归一化比在整个 perturbative coupling window 内统一趋零。这是否定证明路线，不是否定候选不等式。 ||| Physical-absorption audit for R0.72I: on the all-odd Rudin–Shapiro family with \(\delta=M\), the separated positive \(B_AQ_*\) term from R0.72H diverges after normalization like \(M^{1/2}\log M\), so the fixed termwise-absorption route fails. Yet the two analytic routes, joint exposure and odd-carrier parity, give the true \(G_{\rm all}^{\rm ex}\asymp M^2\), and the complete physically normalized ratio tends uniformly to zero throughout the perturbative coupling window. This rejects a proof route, not the candidate inequality.
R0.72I 的结论限于 exact finite triangular 2.5D class 和声明的 all-odd perturbative window。它没有证明 arbitrary-carrier physical inequality，也没有证明一般三维 Navier–Stokes 的全局光滑性或有限时破裂；Clay 正式问题仍然开放。 ||| The conclusion of R0.72I is restricted to the exact finite triangular 2.5D class and the stated all-odd perturbative window. It proves neither the arbitrary-carrier physical inequality nor global smoothness or finite-time breakdown for general three-dimensional Navier–Stokes; the official Clay problem remains open.
R0.72I 附图 ||| R0.72I figure
R0.72I 证书 ||| R0.72I certificates
R0.72J 检查 mixed-parity 的真实 cubic interaction ||| R0.72J tests the true mixed-parity cubic interaction
按 carrier residue graph 检查 \(P_0V^2F\) 返回目标行的真实路径，寻找 action 与 joint exposure 的 hybrid payment；若失败，就要求 mixed-parity 反族使真实 cubic row 而非其分离正上界存活。 ||| Use the carrier residue graph to inspect the true paths by which \(P_0V^2F\) returns to the target row and seek a hybrid payment from action and joint exposure; if this fails, require a mixed-parity counterfamily in which the true cubic row, rather than its separated positive upper bound, survives.
保留 joint heat exposure，或直接利用 \(V\) 翻转奇偶格点，可得 \(G_{\rm all}^{\rm ex}\asymp M^2\)。完整物理比值在 \(0<g\le\gamma_0M^{3/2}\) 内满足 \(CM^{-4/9}(\log M)^{-2/3}\to0\)。因此这个族不是候选 physical inequality 的反例。 ||| Retaining joint heat exposure, or directly using the fact that \(V\) flips lattice parity, gives \(G_{\rm all}^{\rm ex}\asymp M^2\). For \(0<g\le\gamma_0M^{3/2}\), the complete physical ratio satisfies \(CM^{-4/9}(\log M)^{-2/3}\to0\). Hence this family is not a counterexample to the candidate physical inequality.
从多载波 mixed-row 行级封闭走到物理吸收 no-go 与 parity repair ||| From row-level closure of the multi-carrier mixed row to the physical-absorption no-go and parity repair
发散的是分离上界，不是真实完整根账本 ||| The separated upper bound diverges, not the true complete-root ledger
分离的 \(B_AQ_*\) 正项不能逐项物理吸收；同一全奇族的真实 complete ledger 由 joint exposure 与 parity 修复并统一衰减。 ||| The separated positive \(B_AQ_*\) term cannot be physically absorbed term by term; the true complete ledger of the same all-odd family is repaired by joint exposure and parity and decays uniformly.
环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \(M^{-2}\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → phase-uniform \(M^{-8/3}\) sharp algebraic prefactor → shifted Rudin–Shapiro heat pulse → positive-time simple root → full-charge normalized order-one saturation → fixed-carrier shell isolation → negative-Sobolev action decay → candidate D^{1/3}Λ₁ payment failure → critical-log repair → selected-family frontier → complete-root Rolle–BV closure → sharp critical-log saturation → carrier-free mixed-row payment → action-only no-go → termwise physical-absorption no-go → parity repair ||| Annulus exclusion → source–core ledger → covariance spectral stratification → all-frequency conditional bridge → response-slope chord gain → common-response order-one channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \(M^{-2}\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → phase-uniform \(M^{-8/3}\) sharp algebraic prefactor → shifted Rudin–Shapiro heat pulse → positive-time simple root → full-charge normalized order-one saturation → fixed-carrier shell isolation → negative-Sobolev action decay → candidate D^{1/3}Λ₁ payment failure → critical-log repair → selected-family frontier → complete-root Rolle–BV closure → sharp critical-log saturation → carrier-free mixed-row payment → action-only no-go → termwise physical-absorption no-go → parity repair
检查 mixed-parity carrier graph 的真实 cubic interaction，寻找 hybrid payment 或 actual normalized counterfamily。 ||| Test the true cubic interaction of the mixed-parity carrier graph and seek a hybrid payment or an actual normalized counterfamily.
结论限于 exact triangular 2.5D all-odd class。arbitrary mixed-parity cubic row 与一般三维正则性仍然开放。 ||| The conclusion is restricted to the exact triangular 2.5D all-odd class. The arbitrary mixed-parity cubic row and general three-dimensional regularity remain open.
静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71U–Z 依次处理 second-time jet、complete first row、fixed-small-coupling endpoint、selected roots 与 complete roots。R0.72A–C 建立 Bessel lower family、target-row participation 与 physical-phase sharp scales；R0.72D 再实现 positive-time root 与 full-charge order-one saturation。R0.72E 固定 \(q_0>R_*\)，用 Feynman–Kac、驻相和定量 Hörmander density 控制完整 \(H^{-1}\) action；exact one-carrier family 最终使 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。R0.72F 随后证明 selected roots 强制 \(1/3\) 下端点，而 Leray energy 只支付到 \(1/2\)；最小边界修正是 \(s^{-1/3}[1+\log(1/s)]\)。R0.72G 固定这一候选，用实相位 gauge、目标行恒等式与 Rolle–BV 归约证明完整根质量 \(G_{\rm all}\asymp\log\delta\)，并在原始幅度序列上得到 complete-root sharp saturation。R0.72H 转入有限共轭配对多载波 mixed row，证明载波数无关的 moment-resolved 上界；全奇数 Rudin–Shapiro 族排除 action-only payment，并使所需 \(M\)-幂次达到同阶。R0.72I 逐项换回物理量，证明分离的 \(B_AQ_*\) 项不能统一吸收；joint exposure 与 odd-carrier parity 又证明真实 complete ledger 统一衰减。 ||| After the static annular family is rigorously excluded, the main line turns to covariance-rank stratification and the all-frequency projection bridge. R0.71U–Z successively treats the second-time jet, the complete first row, the fixed-small-coupling endpoint, selected roots, and complete roots. R0.72A–C establishes the Bessel lower family, target-row participation, and sharp physical-phase scales; R0.72D then realizes a positive-time root and full-charge order-one saturation. R0.72E fixes \(q_0>R_*\) and controls the complete \(H^{-1}\) action using Feynman–Kac, stationary phase, and a quantitative Hörmander density; the exact one-carrier family ultimately makes the complete-root ledger relative to the candidate \(D^{1/3}\Lambda_1\) payment diverge like \(R^{4/3}\). R0.72F then proves that selected roots force the lower endpoint \(1/3\), while Leray energy pays only up to \(1/2\); the minimal boundary repair is \(s^{-1/3}[1+\log(1/s)]\). R0.72G fixes this candidate and uses a real phase gauge, target-row identities, and the Rolle–BV reduction to prove that the complete root mass satisfies \(G_{\rm all}\asymp\log\delta\), obtaining sharp complete-root saturation for the critical log on the original amplitude sequence. R0.72H moves to the mixed row in a finite conjugate-paired multi-carrier system and proves a carrier-count-independent moment-resolved upper bound; an all-odd Rudin–Shapiro family excludes the action-only payment and attains the required \(M\)-power. R0.72I converts each term back to physical quantities, proves that the separated \(B_AQ_*\) term cannot be absorbed uniformly, and then uses joint exposure and odd-carrier parity to prove uniform decay of the true complete ledger.
累计回顾 R0.61–R0.72I · 2026-08-27 ||| Cumulative recap R0.61–R0.72I · 2026-08-27
累计回顾现在分为二十五个问题阶段，完整覆盖 R0.61–R0.72I。R0.72E 排除 unweighted payment，R0.72F 选出 critical-log 修正，R0.72G 封闭 one-carrier complete roots，R0.72H 封闭 finite multi-carrier mixed row，R0.72I 再分离失败的正项吸收与真实 parity-resolved ledger。R0.70A–R0.72I 共 61 个版本已公开；37 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。 ||| The cumulative recap now has twenty-five problem phases and completely covers R0.61–R0.72I. R0.72E excludes the unweighted payment, R0.72F selects the critical-log repair, R0.72G closes the one-carrier complete roots, R0.72H closes the finite multi-carrier mixed row, and R0.72I separates the failed positive-term absorption from the true parity-resolved ledger. Across R0.70A–R0.72I, 61 releases are public; 37 satisfy the current formal-figure complete-archive contract, while 24 older figure archives remain on the backfill list.
取全奇 Rudin–Shapiro 载波和 \(\delta=M\)。R0.72H 的四个正项换回物理量后，前三项的归一化比都趋零；\(B_AQ_*\) 项却按 \(M^{1/2}\log M\) 发散。这严格排除了 fixed termwise absorption。 ||| Take all-odd Rudin–Shapiro carriers and \(\delta=M\). After converting the four positive terms from R0.72H back to physical quantities, the normalized ratios of the first three all tend to zero, but the \(B_AQ_*\) term diverges like \(M^{1/2}\log M\). This rigorously excludes fixed termwise absorption.
上次综述 v1.21 · 2026-08-27 ||| Previous review v1.21 · 2026-08-27
我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.72I 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。 ||| I also prepared a systematic review that places the classical theory, five literature strands, the candidate-elimination tree, progress from 2019—2026, and this site's R0.69P–R0.72I route on one diagram. The historical nodes R0.61–R0.69O remain in the cumulative recap.
我排除了一个具体证明路线，但没有排除 physical critical-log candidate。下一障碍是 mixed-parity 的真实 cubic interaction。 ||| I excluded one specific proof route, but did not exclude the physical critical-log candidate. The next obstruction is the true mixed-parity cubic interaction.
下一步 R0.72J： ||| Next R0.72J:
研究笔记 R0.72I · 2026-08-27 ||| Research note R0.72I · 2026-08-27
阅读 R0.72I 研究笔记 → ||| Read the R0.72I research note →
展开 69 篇公开笔记 ||| Expand 69 public notes
综述 v1.22 · 2026-08-27 ||| Review v1.22 · 2026-08-27
R0.60 recap 之后的累计回顾收录 99 个节点；全站现有 159 篇公开研究笔记 ||| The cumulative recap after R0.60 contains 99 nodes; the site now has 159 public research notes
R0.70A–R0.72I：61 节已公开，37 节完整封存 ||| R0.70A–R0.72I: 61 published, 37 fully archived
R0.72I 已完成： ||| R0.72I complete:
R0.72I 已证明分离的 B_AQ_* 正项不能逐项物理吸收，但同一全奇载波族的真实 complete ledger 在 critical-log normalization 下统一衰减；下一步只审 mixed-parity 的真实 cubic row。 ||| R0.72I proves that the separated positive B_AQ_* term cannot be physically absorbed term by term, while the true complete ledger of the same all-odd carrier family decays uniformly under critical-log normalization; the next step tests only the true mixed-parity cubic row.
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
  throw new Error("Duplicate Chinese keys in R0.72I translation rows");
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
  "notes/r0-72i.html",
  "recap-r0-61-r0-72i.html",
  "research-review.html",
];
for (const relative of expectedFiles) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.22')) {
    throw new Error(relative + ": expected i18n cache version v1.22");
  }
}

const source = await collectSiteStrings(publicDirectory);
const translations = JSON.parse(await readFile(translationPath, "utf8"));
const batchId = /^r072i\d+$/;
const retained = translations.filter((entry) => !batchId.test(entry.id));
const retainedByChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (retainedByChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.72I batch");
}

const missing = source.filter((entry) => !retainedByChinese.has(entry.zh));
const missingKeys = new Set(missing.map((entry) => entry.zh));
const uncovered = missing.filter((entry) => !additions.has(entry.zh));
const stale = [...additions.keys()].filter((zh) => !missingKeys.has(zh));
if (uncovered.length || stale.length || additions.size !== missing.length) {
  throw new Error(
    `R0.72I translation batch does not equal active missing set (${missing.length}):\n` +
      "UNCOVERED:\n" +
      uncovered.map((entry) => entry.zh).join("\n---\n") +
      "\nSTALE:\n" +
      stale.join("\n---\n"),
  );
}
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))];
if (!sameTokens(missingFiles, expectedFiles)) {
  throw new Error("Unexpected R0.72I source files: " + JSON.stringify(missingFiles));
}
await writeFile(
  snapshotPath,
  JSON.stringify(
    missing.map(({ zh, count, files }) => ({ zh, count, files })),
    null,
    2,
  ) + "\n",
);

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
    id: "r072i" + String(index + 1).padStart(3, "0"),
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

await writeFile(
  translationPath,
  JSON.stringify(finalTranslations, null, 2) + "\n",
);
console.log(
  JSON.stringify({
    added: translatedEntries.length,
    total: finalTranslations.length,
    liveStrings: source.length,
    missingBefore: missing.length,
    missingAfter: 0,
    files: missingFiles,
  }),
);
