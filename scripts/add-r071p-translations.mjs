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
const source = await collectSiteStrings(publicDirectory);
const current = JSON.parse(await readFile(translationPath, "utf8"));

const translationRows = [
  String.raw`
把已有 variation 写成 coarea/upcrossing 形式，不从 Leray energy 创造 positive-entry budget。 ||| express the existing variation in coarea/upcrossing form without creating a positive-entry budget from Leray energy.
半开窗口上的 segmented/soft entry 与 hard BV 正跳跃精确分离，初始 trace 单独扣除；bounded support overlap 与 \(\dot H^{-1}\) Lamb square sum 删除同刻 cell multiplicity。完整和变成 time-slice budget 对 distinct entry-time counting measure 的积分；componentwise relaxed 正 atoms 内部没有 signed shell–cell cancellation，但它们不一般等于 signed aggregate 的正 Jordan 部。 ||| Segmented/soft entry on a half-open window is separated exactly from a hard BV positive jump, with the initial trace deducted separately; bounded support overlap and the \(\dot H^{-1}\) Lamb square sum remove simultaneous cell multiplicity. The full sum becomes the integral of a time-slice budget against the distinct entry-time counting measure; the componentwise relaxed positive atoms admit no signed shell–cell cancellation internally, but they do not in general equal the positive Jordan part of the signed aggregate.
打开 80 节完整索引 ||| Open the complete 80-section index
的 spatial Gevrey decay 不计 temporal crossings。两轮限定检索未找到从这些工具支付完整 entry-time counting measure 的定理；这是 bounded negative finding，不是原创性、优先权或不存在性结论。 ||| 's spatial Gevrey decay does not count temporal crossings. Two bounded searches found no theorem that pays the full entry-time counting measure from these tools; this is a bounded negative finding, not a claim of originality, priority, or nonexistence.
的唯一延拓针对完整速度场在空间开集消失； ||| 's unique-continuation result concerns vanishing of the full velocity field on a spatial open set;
精确 factorization 把 soft source 分成 hard interior source 与 face layer；signed atoms 可以相消而 Jordan face costs 保留。 ||| The exact factorization splits the soft source into a hard interior source and a face layer; signed atoms may cancel while Jordan face costs remain.
开放接口 · R0.71Q ||| Open interface · R0.71Q
累计回顾与 80 节索引 ||| Cumulative recap and 80-section index
同刻 positive entries 由空间平方和支付，时间 packing 仍开放 ||| Simultaneous positive entries are paid by a spatial square sum; temporal packing remains open
文献综述 v1.01 · 2026-08-26 ||| Literature review v1.01 · 2026-08-26
我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.71P 只列为研究笔记。我不把计算或笔记外推成正则性定理。 ||| I list published theorems as known results, mark 2026 preprints separately, and classify this site's R0.69P–R0.71P work only as research notes. I do not extrapolate calculations or notes into regularity theorems.
下一节显式检查 analytic radius、complex growth、projection anchor 与窗口 covering；定性时间解析性不被写成 uniform zero count。 ||| The next section explicitly tests the analytic radius, complex growth, projection anchor, and window covering; qualitative time analyticity is not treated as a uniform zero count.
只在 classical interval 给逐 observable 的时间解析性； ||| provides time analyticity for each observable only on the classical interval;
中。R0.69P–R0.71P 从有符号物理环带经过 projected-Lamb 热体积、matched-cell heat gap、viscous fusion、signed second jet 与 soft-denominator faces，走到 positive-entry temporal-packing boundary。R0.71P 删除同刻空间 cell multiplicity，留下 distinct entry-time packing。保留下来的结果都不是全局正则性结论。 ||| . From R0.69P through R0.71P, the route moves from signed physical annuli through projected-Lamb heat volume, the matched-cell heat gap, viscous fusion, the signed second jet, and soft-denominator faces to the positive-entry temporal-packing boundary. R0.71P removes simultaneous spatial cell multiplicity, leaving distinct entry-time packing. None of the retained results is a global-regularity conclusion.
R0.71P 的一手文献边界 ||| Primary-source boundary for R0.71P
R0.71P 关闭了什么，R0.71Q 只检查什么 ||| What R0.71P closes, and what R0.71Q alone tests
R0.71P 证明 \(A_+\) 与 ordinary hard positive jump 不同，并用 cutoff support overlap 与 \(\dot H^{-1}\) square sum 支付所有同刻 entries。逐 shell–cell 先取 soft 正部再求和后，relaxed 正测度内部没有符号抵消；它不一般等于 signed aggregate 的正 Jordan 部。留下的是 distinct entry-time counting measure。R0.71Q 只检查 quantitative complex-time/parabolic-window zero packing，不引入 moving cutoff、refresh 或 total-Jordan sum。我继续用下面六条筛选。 ||| R0.71P proves that \(A_+\) differs from an ordinary hard positive jump and pays all simultaneous entries using cutoff support overlap and the \(\dot H^{-1}\) square sum. After taking the soft positive part shell–cell by shell–cell and then summing, the relaxed positive measure admits no internal sign cancellation; it does not in general equal the positive Jordan part of the signed aggregate. What remains is the distinct entry-time counting measure. R0.71Q tests only quantitative complex-time/parabolic-window zero packing, without introducing moving cutoffs, refresh, or a total-Jordan sum. I continue to apply the six filters below.`,
  String.raw`
01 · 正进入目标 ||| 01 · Positive-entry target
03 · 正原子测度 ||| 03 · Positive atomic measure
04 · 同刻空间批次 ||| 04 · Same-time spatial batch
05 · 时间计数测度 ||| 05 · Time-counting measure
06 · 有限解析截断 ||| 06 · Finite analytic truncation
09 · Jensen 条件窗口 ||| 09 · Conditional Jensen window
16 · 复现 ||| 16 · Reproduction
把同刻所有 faces 看成一个 batch。令 ||| Treat all faces at the same time as one batch. Let
版本 v0.71P · 2026-08-26 ||| Version v0.71P · 2026-08-26
报告、双实现证书与图件包 ||| Report, dual-implementation certificates, and figure package
本节关闭同刻空间 multiplicity，不关闭 temporal packing ||| This section closes same-time spatial multiplicity, not temporal packing
本节目标严格保持为 ||| The target of this section remains strictly
本节先把 \(A_+\) 与 ordinary hard BV 分开，再把全部同刻 faces 做一次局部平方和，最后才累加不同时间。这个顺序得到一个精确而有限的判断。 ||| This section first separates \(A_+\) from ordinary hard BV, then performs one local square sum over all same-time faces, and only then accumulates across distinct times. This order yields an exact finite conclusion.
本节也关闭一个过宽的措辞：正进入 atoms 已经非负，不能再期待它们在 all-shell/all-cell sum 中直接做 signed cancellation。真正开放的是 distinct entry times 的 packing。这个定位比继续重排 fixed-cell source 更具体，但仍离继续性判据很远。 ||| This section also closes an overbroad formulation: positive-entry atoms are already nonnegative, so direct signed cancellation cannot be expected in the all-shell/all-cell sum. What remains open is the packing of distinct entry times. This localization is more specific than another rearrangement of the fixed-cell source, but remains far from a continuation criterion.
本页只报告 exact finite theorem、conditional Jensen gate、abstract separation 与 one-sided NSE initial sharpness。不作新颖性、优先权或发表级别声明。 ||| This page reports only the exact finite theorem, conditional Jensen gate, abstract separation, and one-sided NSE initial sharpness. It makes no claim of novelty, priority, or publication level.
标量 Jensen count 按重数计，只会更大。这条条件式明确暴露四项输入：complex-time radius、整盘 complex norm、非退化 projection anchor 与窗口覆盖。当前 Leray budget 没有给出它们的一致版本。 ||| The scalar Jensen count includes multiplicity and can only be larger. This conditional formula explicitly exposes four inputs: complex-time radius, whole-disk complex norm, a nondegenerate projection anchor, and window covering. The current Leray budget provides no uniform version of them.
不同进入时刻仍需要独立计数预算 ||| Distinct entry times still require an independent counting budget
的 spatial Gevrey decay 也不计 temporal zeros。 ||| 's spatial Gevrey decay does not count temporal zeros either.
的唯一延拓针对完整速度场在空间开集消失，不适用于一个 filtered observable 落入算子核； ||| 's unique continuation concerns the full velocity field vanishing on a spatial open set and does not apply when a filtered observable falls into an operator kernel;
定量窗口 ||| Quantitative window
定义目标以后，跨壳跨小区没有符号可以抵消 ||| Once the target is defined, no signs remain to cancel across shells or cells
独立 checker ||| Independent checker
独立 checker 用固定 seed __I18N_BACKTICK__71071__I18N_BACKTICK__ 做了 64 组有限 overlap 测试。最大 cellwise ratio 为 \(0.6780322244\)，最大 entry-sum/overlap-budget ratio 为 \(0.1434662197\)，所有不等式通过。 ||| The independent checker used fixed seed __I18N_BACKTICK__71071__I18N_BACKTICK__ for 64 finite-overlap tests. The maximum cellwise ratio was \(0.6780322244\), the maximum entry-sum/overlap-budget ratio was \(0.1434662197\), and every inequality passed.
对 \(N=1,2,\ldots,64\) 的七个 dyadic 样本，sampled signs 与 Brent roots 在半开窗口上给出零 entry-count error；soft rising-layer quadrature 的最大相对误差为 \(1.18\times10^{-16}\)。独立 \(32^3\) FFT 得到 \(A_+=1/4\) 与 sharpness ratio \(1\)，包括 filtered-vorticity 与 viscous-jet 检查在内的 residual 全为 \(0.0\)。没有 PDE 时间推进。 ||| For the seven dyadic samples \(N=1,2,\ldots,64\), sampled signs and Brent roots gave zero entry-count error on the half-open window; the maximum relative error of the soft rising-layer quadrature was \(1.18\times10^{-16}\). An independent \(32^3\) FFT obtained \(A_+=1/4\) and sharpness ratio \(1\), with every residual—including the filtered-vorticity and viscous-jet checks—equal to \(0.0\). No PDE time evolution was performed.
对可数族，约定非 entry 时 \(A_{j,Q,+}(t)=0\)，并对固定的全体 counting measure 使用 Tonelli 与 monotone convergence。该 measure 可以不局部有限；无限多个同刻 entries 的总权重仍由上面的 time-slice bound 控制。 ||| For a countable family, set \(A_{j,Q,+}(t)=0\) away from entries and apply Tonelli and monotone convergence to the fixed global counting measure. This measure need not be locally finite; the total weight of infinitely many same-time entries is still controlled by the time-slice bound above.
对每个 shell–cell，soft face 的正、负部分可以分别趋于 \(A_+\delta_{t_0}\)、\(A_-\delta_{t_0}\)，而 signed difference 在偶阶 touch 可以趋于零。因此 \(\eta^+_\Lambda\) 是 componentwise relaxed positive-entry measure，不是 signed weak limit 或 signed aggregate 的正 Jordan 部。 ||| For each shell–cell, the positive and negative parts of the soft face can converge separately to \(A_+\delta_{t_0}\) and \(A_-\delta_{t_0}\), while the signed difference can converge to zero at an even-order touch. Thus \(\eta^+_\Lambda\) is a componentwise relaxed positive-entry measure, not a signed weak limit or the positive Jordan part of a signed aggregate.
附图、数据与源代码包 ||| Figure, data, and source-code package
个人研究记录 · R0.71P · 2026-08-26 · ||| Personal research record · R0.71P · 2026-08-26 ·
给经典区间内的时间解析性； ||| gives time analyticity on classical intervals;
固定时间 \(t\)，记 \(\mathcal E_\Lambda(t)\) 为所有此时右进入的 \((j,Q)\)。Taylor leading direction 仍支撑在 \(\operatorname{supp}\chi_Q\)，所以 Cauchy–Schwarz 给出 sharp cell bound ||| At a fixed time \(t\), let \(\mathcal E_\Lambda(t)\) denote all \((j,Q)\) entering from the right at that time. The Taylor leading direction remains supported in \(\operatorname{supp}\chi_Q\), so Cauchy–Schwarz gives the sharp cell bound
固定有限个 \((j,Q)\) 时，\(\mathsf S_{\Lambda,+}(K)<\infty\)。解析性没有给出随截断、解、壳、小区或 \(K\uparrow T^*\) 一致的零点数、阶数、间距与 transversality。 ||| For a fixed finite set of \((j,Q)\), \(\mathsf S_{\Lambda,+}(K)<\infty\). Analyticity does not provide zero counts, orders, spacings, or transversality uniformly over truncations, solutions, shells, cells, or \(K\uparrow T^*\).
固定有限截断在经典紧区间内确实有限 ||| A fixed finite truncation is indeed finite on a compact classical interval
光滑抽象路径把 counting measure 与 \(dt\) 分开 ||| A smooth abstract path separates the counting measure from \(dt\)
价值是把“空间太多”与“时间太多”严格拆开 ||| The value lies in rigorously separating “too many in space” from “too many in time”
截至 2026-08-26 的两轮限定一手检索，没有找到从 Leray energy、时间解析性、唯一延拓或空间频率衰减直接支付本节完整正进入和的定理。这是 bounded negative finding，不是原创性、优先权或不存在性结论。 ||| Two bounded primary-source searches through 2026-08-26 found no theorem that directly pays for the full positive-entry sum in this section using Leray energy, time analyticity, unique continuation, or spatial frequency decay. This is a bounded negative finding, not a claim of originality, priority, or nonexistence.
精确 producer ||| Exact producer
空间 cell multiplicity 可以删掉，时间 event multiplicity 还不能删 ||| Spatial cell multiplicity can be removed; temporal event multiplicity cannot yet be removed
跨时计数 ||| Across-time counting
令径向 multiplier 在半径 \(1\) 为零、在 \(\sqrt2\) 为一，并取 \(\chi=1\)。此时初始 filtered vorticity 与 filtered viscous jet 都为零。精确 Fourier convolution 给出 ||| Let the radial multiplier vanish at radius \(1\), equal one at \(\sqrt2\), and take \(\chi=1\). The initial filtered vorticity and filtered viscous jet then both vanish. Exact Fourier convolution gives
能表示已经受控的 variation；作用于 ordinary hard path 时只看到 \((A_+-A_-)^+\)，恢复 \(A_+\) 必须使用 soft 或 zero-padded representative。 ||| can represent variation that is already controlled; when applied to an ordinary hard path, it sees only \((A_+-A_-)^+\), and recovering \(A_+\) requires a soft or zero-padded representative.
偶阶 touch 且 \(A_-=A_+>0\) 时，ordinary hard BV 原子为零，soft/segmented ledger 仍保留完整 \(A_+\)。 ||| At an even-order touch with \(A_-=A_+>0\), the ordinary hard BV atom is zero, while the soft/segmented ledger retains the full \(A_+\).
其中 \(\mathcal T_\Lambda(K)\) 只记录 \(A_{j,Q,+}(t)>0\) 的不同 entry times。定义 ||| Here \(\mathcal T_\Lambda(K)\) records only the distinct entry times for which \(A_{j,Q,+}(t)>0\). Define
取 \(\varepsilon_N=N^{-4}\)，soft 正进入质量为 \(N/(1+N^{-2})\)，所以 soft/hard 比值趋于一。这个 smooth Hilbert path 证明 counting measure 不能由这些 ordinary budgets 普适替换为 \(dt\)；它不是 NSE 多-face 构造。 ||| Taking \(\varepsilon_N=N^{-4}\), the soft positive-entry mass is \(N/(1+N^{-2})\), so the soft/hard ratio tends to one. This smooth Hilbert path proves that the counting measure cannot universally be replaced by \(dt\) under these ordinary budgets; it is not an NSE multi-face construction.
权重与原子全部非负。同一时间的 atoms 相加；扩大有限截断时总质量单调增加。可数 frame 给出 extended positive Borel measure，极限允许为无穷，也没有预先声称局部有限。 ||| All weights and atoms are nonnegative. Atoms at the same time are added; the total mass increases monotonically as the finite truncation expands. A countable frame gives an extended positive Borel measure whose limit may be infinite, with no prior claim of local finiteness.
若 \(K=[a,b)\) 且 \(\overline K=[a,b]\Subset I_{\rm strong}\)，周期强解对时间解析。固定 bounded observable \(C_{j,Q}(t)\) 要么恒为零，要么每个零点孤立且有限阶；\(\overline K\) 上零点有限。恒零 observable 没有 positive-denominator component，也没有 entry。 ||| If \(K=[a,b)\) and \(\overline K=[a,b]\Subset I_{\rm strong}\), the periodic strong solution is analytic in time. A fixed bounded observable \(C_{j,Q}(t)\) is either identically zero or has isolated zeros of finite order; it has finitely many zeros on \(\overline K\). An identically zero observable has no positive-denominator component and no entry.
若 cutoff support overlap 为 \(M_\chi\)，且固定 annular frame 满足标准 \(\dot H^{-1}\) square-function 上界，则 ||| If the cutoff-support overlap is \(M_\chi\) and the fixed annular frame satisfies the standard \(\dot H^{-1}\) square-function upper bound, then
若 Hilbert 空间复化后的 \(C\) 在复圆盘 \(D(t_*,R)\) 解析，且 ||| If the complexification of \(C\) in the Hilbert space is analytic in the complex disk \(D(t_*,R)\), and
若这些输入只能由已知 continuation norm、inverse denominator、target BV 或额外 transversality 支付，我会把 zero-count route 保留为条件结论并停止这一分支。 ||| If these inputs can be paid for only by a known continuation norm, inverse denominator, target BV, or additional transversality, the zero-count route will be retained as a conditional conclusion and this branch will stop.
剩余对象是 distinct entry times，而不是 Lebesgue time ||| The remaining object is distinct entry times, not Lebesgue time
随机 overlap、root detection、quadrature 与 FFT 分开复核 ||| Random overlap, root detection, quadrature, and FFT were checked separately
同刻批次 ||| Same-time batch
同刻全部 entries 先由 support overlap 合并 ||| All same-time entries are first combined through support overlap
同时 ||| Meanwhile
同一时刻的全部正进入可以做空间平方和， ||| All positive entries at a single time admit a spatial square sum,
图 R0.71P。A：偶阶 touch 的 hard positive jump 为零，但 segmented/soft entry 保留 \(A_+\)。B：同刻 cell entries 经 support overlap 合并为空间平方和。C：半开窗口上的 sequential abstract path，其 entry mass 按 \(N\) 增长，而 ordinary budgets 不随 \(N\) 增长。D：真实 smooth NSE initial jet 达到 \(A_+=\|F\|_2^2/Y=1/4\)。 ||| Figure R0.71P. A: At an even-order touch, the hard positive jump is zero, but the segmented/soft entry retains \(A_+\). B: Same-time cell entries are combined by support overlap into a spatial square sum. C: On a half-open window, the entry mass of the sequential abstract path grows like \(N\), while the ordinary budgets do not grow with \(N\). D: A genuine smooth NSE initial jet attains \(A_+=\|F\|_2^2/Y=1/4\).
未证明：继续性、有限时奇性、三维全局正则性或千禧年问题结论。 ||| Not proved: continuation, finite-time singularity, three-dimensional global regularity, or any conclusion on the Millennium Problem.
未证明：uniform NSE zero count、内部多 face、无限 frame、Leray 极限或接近潜在奇性端点的 bound。 ||| Not proved: a uniform NSE zero count, interior multiple faces, an infinite frame, the Leray limit, or a bound near a potential singular endpoint.
我继续固定 multiplier、cutoff 与 partition。R0.71O 给出的 \(A_{j,Q,+}\) 是 soft/分段路径的正进入原子，不是普通 hard BV 的正跳跃。把同刻所有壳与小区先合并后，cutoff 有界重叠和 Littlewood–Paley \(\dot H^{-1}\) 平方和确实删除了空间 cell count；但完整目标变成同一预算对 entry-time counting measure 的积分。现有 Leray 时间积分不能替代这张计数测度。 ||| The multiplier, cutoff, and partition remain fixed. The \(A_{j,Q,+}\) supplied by R0.71O is a positive-entry atom of the soft/segmented path, not the positive jump of ordinary hard BV. After all same-time shells and cells are combined, bounded cutoff overlap and the Littlewood–Paley \(\dot H^{-1}\) square sum do remove the spatial cell count; but the full target becomes the integral of the same budget against the entry-time counting measure. Existing Leray time integrals cannot replace this counting measure.
我只讨论非平凡零均值经典解，因此 \(Y(t)=\|\omega(t)\|_2^2>0\)；平凡解的 entry mass 约定为零。total-Jordan \(A_++A_-\)、moving cutoff 与 refresh atoms 都没有混入这一节。全文固定半开窗口 \(K=[a,b)\)：左端零点可以计入，右观测端点不计入。 ||| Only nontrivial zero-mean classical solutions are considered, so \(Y(t)=\|\omega(t)\|_2^2>0\); the entry mass of the trivial solution is defined as zero. Total-Jordan \(A_++A_-\), moving cutoffs, and refresh atoms are not included in this section. The half-open window \(K=[a,b)\) is fixed throughout: a zero at the left endpoint may be counted, while the right observation endpoint is excluded.
下一对象：quantitative complex-time zero packing ||| Next object: quantitative complex-time zero packing
下一节把 Jensen 条件式放进 parabolic windows，逐项记录 analytic radius \(R\)、complex growth \(M\)、projection anchor \(\|C(t_*)\|\) 与窗口覆盖数。 ||| The next section places the conditional Jensen formula in parabolic windows and records, term by term, the analytic radius \(R\), complex growth \(M\), projection anchor \(\|C(t_*)\|\), and window-covering number.
选取在 \(C(t_*)\) 上取范数的单位复线性泛函，再用 Jensen 公式可得 distinct vector-zero count ||| Choose a unit complex-linear functional that norms \(C(t_*)\); Jensen's formula then gives the distinct vector-zero count
研究笔记 R0.71P · POSITIVE ENTRIES · SPATIAL BATCHING · TEMPORAL PACKING ||| Research note R0.71P · POSITIVE ENTRIES · SPATIAL BATCHING · TEMPORAL PACKING
研究笔记 R0.71P：同刻正进入原子可由 bounded-overlap 与 H^{-1} Lamb 平方和支付；完整累积仍需要控制不同 entry times 的计数测度。 ||| Research note R0.71P: Same-time positive-entry atoms can be paid for by bounded overlap and the H^{-1} Lamb square sum; the full accumulation still requires control of the counting measure of distinct entry times.
已构造：达到单格 projection 常数的真实 smooth NSE initial jet。 ||| Constructed: a genuine smooth NSE initial jet attaining the single-cell projection constant.
已证明：半开窗口上的抽象 sequential path 排除用 ordinary \(dt\) budgets 普适支付 entry count。 ||| Proved: an abstract sequential path on a half-open window rules out universally paying for the entry count with ordinary \(dt\) budgets.
已证明：该正测度内部没有 signed shell–cell cancellation。 ||| Proved: this positive measure has no internal signed shell–cell cancellation.
已证明：固定有限截断在经典紧区间内有限。 ||| Proved: a fixed finite truncation is finite on a compact classical interval.
已证明：同刻 frame–cell entries 的 bounded-overlap 与 \(\dot H^{-1}\) Lamb 上界。 ||| Proved: the bounded-overlap and \(\dot H^{-1}\) Lamb upper bound for same-time frame–cell entries.
已证明：完整目标是 time-slice budget 对 distinct entry-time counting measure 的积分。 ||| Proved: the full target is the integral of the time-slice budget against the distinct entry-time counting measure.
已证明：逐分量 soft 正部的 relaxed entry atoms 组成正测度；它不等于 signed aggregate 的正 Jordan 部。 ||| Proved: the relaxed entry atoms of the componentwise soft positive parts form a positive measure; it is not the positive Jordan part of the signed aggregate.
已证明：segmented/soft 正进入与 ordinary hard positive BV 的精确差。 ||| Proved: the exact difference between segmented/soft positive entry and ordinary hard positive BV.
因此 R0.71O 留下的“是否有 summed cancellation”在这一节被收紧：对已经定义好的 \(\eta^+\)，字面上的 signed cancellation 不存在。仍可能存在的是新的 NSE estimate、packing law，或者先在一个 signed precursor 中抵消，再证明它支配这张正测度。 ||| Thus the question of “summed cancellation” left by R0.71O is sharpened here: for the already-defined \(\eta^+\), literal signed cancellation does not exist. What may still exist is a new NSE estimate, a packing law, or cancellation in a signed precursor followed by a proof that it dominates this positive measure.
有限正结果 ||| Finite positive result
再由 Sobolev duality、Hölder 与插值， ||| Then, by Sobolev duality, Hölder, and interpolation,
在 \(K=[a,b)\) 内，把 \(\{d_{j,Q}>0\}\) 的每个连通分支在两端分别补零。若 \(d_{j,Q}(a)>0\)，这会人为产生左端上升 \(0\to a_{j,Q}(a+)\)；我把它声明为 initial trace \(I^+_{j,Q}(K)\)，而不是 entry。于是 ||| Within \(K=[a,b)\), zero-pad both ends of every connected component of \(\{d_{j,Q}>0\}\). If \(d_{j,Q}(a)>0\), this artificially creates the left-end rise \(0\to a_{j,Q}(a+)\); it is declared to be the initial trace \(I^+_{j,Q}(K)\), not an entry. Hence
在半开窗口 \(K=[0,2\pi)\) 取单位向量 \(e\)，令 ||| On the half-open window \(K=[0,2\pi)\), take a unit vector \(e\) and let
在有限阶零点 \(t_0\)，若 ||| At a finite-order zero \(t_0\), if
则 R0.71O 给出 ||| then R0.71O gives
这里数的是 amplitude 从零向上穿过正层 \(s\)，不是非负 \(d_Q\) 对零层的符号 crossing。 ||| This counts the amplitude crossing upward from zero through the positive level \(s\), not a sign crossing of the nonnegative \(d_Q\) through the zero level.
这一步删除了“同一时刻有多少 cells”这个因子。它没有累加不同时间。 ||| This step removes the factor “how many cells occur at the same time.” It does not accumulate across distinct times.
真实 smooth NSE initial jet 达到单格 projection 常数 ||| A genuine smooth NSE initial jet attains the single-cell projection constant
正 atoms 位于 \(t=2k\pi/N\)，\(k=0,\ldots,N-1\)。左端 \(t=0\) 计入，右端 \(2\pi\) 不计入，因此共有 \(N\) 个正进入，每个 \(A_+=1\)： ||| The positive atoms lie at \(t=2k\pi/N\), \(k=0,\ldots,N-1\). The left endpoint \(t=0\) is included and the right endpoint \(2\pi\) is excluded, so there are \(N\) positive entries, each with \(A_+=1\):
正测度 ||| Positive measure
正进入和是逐 shell–cell 先取 soft 正部、再求和得到的 relaxed 正测度；它一般不等于 signed aggregate 的正 Jordan 部。同刻全部 faces 由 \(\dot H^{-1}\) Lamb budget 支付；完整和则由该 budget 对 distinct entry-time counting measure 的积分控制。当前缺的是 temporal packing，不是另一个 fixed-cell 代数恒等式。 ||| The positive-entry sum is the relaxed positive measure obtained by taking the soft positive part shell–cell by shell–cell and then summing; in general, it is not the positive Jordan part of the signed aggregate. All same-time faces are paid for by the \(\dot H^{-1}\) Lamb budget; the full sum is controlled by integrating that budget against the distinct entry-time counting measure. What is currently missing is temporal packing, not another fixed-cell algebraic identity.
正式附图分开显示 BV 缺失、空间 batching、跨时增长与 NSE sharpness ||| The formal figure separately shows the BV discrepancy, spatial batching, across-time growth, and NSE sharpness
证书与 SHA-256 ||| Certificates and SHA-256
主张用语 ||| Claim language
状态 · R0.71P 同刻 batching theorem 与独立审计完成 ||| Status · R0.71P same-time batching theorem and independent audit completed
Cauchy residual 为零。因此单 face 上不能普适插入小于一的改进常数。这仍是一侧初始 jet，不是内部 crossing 或重复 NSE face theorem。 ||| The Cauchy residual is zero. Therefore no improved constant smaller than one can be inserted universally for a single face. This remains a one-sided initial jet, not an interior crossing or a repeated NSE face theorem.
crossing formulas 表示已有变差，解析性只给逐 observable 的有限性 ||| Crossing formulas represent existing variation; analyticity gives only observable-by-observable finiteness
Jensen 可以计数，但必须显式支付 radius、growth 与 anchor ||| Jensen can count, but radius, growth, and anchor must be paid for explicitly
Leray energy 可以控制若干 \(\mathcal H(t)\,dt\) 型普通时间积分；它不控制同一函数在零测 entry set 上被重复抽样。把 \(d\mathfrak n_\Lambda\) 直接换成 \(dt\) 是本节明确排除的一步。 ||| Leray energy can control certain ordinary time integrals of the form \(\mathcal H(t)\,dt\); it does not control repeated sampling of the same function on a measure-zero entry set. Directly replacing \(d\mathfrak n_\Lambda\) with \(dt\) is a step explicitly ruled out in this section.
ordinary hard representative 在内部零点直接从 \(A_-\) 跳到 \(A_+\)，它的正原子只是 ||| At an interior zero, the ordinary hard representative jumps directly from \(A_-\) to \(A_+\), so its positive atom is only
R0.71P 给出一个新的有限正结果：同一时刻不必逐 cell 付费，cutoff support overlap 与 LP square sum 已经把它们统一压成 \(\dot H^{-1}\) Lamb budget。真实 NSE 初始 jet 说明 cellwise projection 的常数一是 sharp 的；它不说明完整 \(M_\chi C_T\) frame 常数 sharp。 ||| R0.71P gives a new finite positive result: cells at the same time need not be paid for individually, because cutoff-support overlap and the LP square sum compress them into a single \(\dot H^{-1}\) Lamb budget. The genuine NSE initial jet shows that the cellwise projection constant one is sharp; it does not show that the full \(M_\chi C_T\) frame constant is sharp.
R0.71P 只检查右侧正进入原子 ||| R0.71P checks only right-sided positive-entry atoms
R0.71P segmented positive entry 与 hard BV 的差、同刻 bounded-overlap batching、跨时 entry count 增长和真实 NSE initial entry sharpness ||| R0.71P: the difference between segmented positive entry and hard BV, same-time bounded-overlap batching, across-time entry-count growth, and genuine NSE initial-entry sharpness
R0.71P｜同刻空间批次可支付，跨时进入计数仍开放 ||| R0.71P | Same-time spatial batches are payable; across-time entry counting remains open
segmented positive variation、逐分量 relaxed 正进入测度、同刻 frame-cell batching、时间计数测度、解析性边界和 sharp NSE initial entry。 ||| Segmented positive variation, componentwise relaxed positive-entry measure, same-time frame-cell batching, time-counting measure, the analyticity boundary, and a sharp NSE initial entry.
soft/分段进入质量不是 ordinary hard \(V^+\) ||| Soft/segmented entry mass is not ordinary hard \(V^+\)
Tonelli 还给出精确幅值层析： ||| Tonelli also gives the exact amplitude-layer decomposition:
R0.71Q 检查 quantitative complex-time/parabolic-window zero packing ||| R0.71Q examines quantitative complex-time/parabolic-window zero packing`,
  String.raw`
02 · 80 节完整索引 ||| 02 · Complete 80-section index
半开窗口上的 componentwise segmented/relaxed positive-entry decomposition：扣除 branch-interior variation 与 initial trace 后恢复 entries；ordinary hard BV 正跳跃与 soft entry 相差 \(\min(A_+,A_-)\)。 ||| Componentwise segmented/relaxed positive-entry decomposition on a half-open window: entries are recovered after subtracting branch-interior variation and the initial trace; an ordinary hard BV positive jump differs from a soft entry by \(\min(A_+,A_-)\).
打开最新节点 R0.71P ||| Open the latest node, R0.71P
回顾截止节点：R0.71P ||| Recap endpoint: R0.71P
回顾截止时公开笔记：140 ||| Public notes at the recap endpoint: 140
截至 R0.71P，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 80 个节点解释成对千禧年问题完成了某个比例。 ||| As of R0.71P, there is no new unconditional continuation criterion, no reduction of the set of all potential singular solutions, and no proof of finite-time breakdown. The 80 nodes cannot be interpreted as completing any percentage of the Millennium Problem.
累计回顾 · R0.61–R0.71P · 2026-08-26 ||| Cumulative recap · R0.61–R0.71P · 2026-08-26
目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、有界重叠局部化与 denominator mass 支付。R0.71N 关闭 fixed-cell interior 正平方候选，R0.71O 关闭“soft denominator 自动删除 faces”的想法；R0.71P 又删除同刻 spatial multiplicity，并确认 componentwise relaxed 正 atoms 内部不能直接做 signed shell–cell cancellation。现在开放的是 distinct entry-time counting measure 的 uniform NSE packing。 ||| The most substantial unconditional positive result remains the Leray-energy-level projected-Lamb heat volume, bounded-overlap localization, and payment by denominator mass. R0.71N closes the fixed-cell interior positive-square candidate, R0.71O closes the idea that the soft denominator automatically removes faces, and R0.71P further removes simultaneous spatial multiplicity and confirms that componentwise relaxed positive atoms do not permit direct signed shell–cell cancellation internally. What remains open is uniform NSE packing of the distinct entry-time counting measure.
十二个阶段、80 个节点：从约化递推到 projected-Lamb 局部热打包，再到 soft-denominator faces、同刻 spatial batching 与 temporal-packing boundary。 ||| Twelve phases and 80 nodes: from the reduced recurrence to projected-Lamb local heat packing, then to soft-denominator faces, simultaneous spatial batching, and the temporal-packing boundary.
收录节点：80 ||| Included nodes: 80
同刻 positive entries 的 bounded-overlap spatial batching、distinct entry-time counting-measure reduction、有限解析截断与 sharp NSE initial entry。 ||| Bounded-overlap spatial batching of simultaneous positive entries, reduction to the distinct entry-time counting measure, finite analytic truncations, and a sharp NSE initial entry.
下一步把 quantitative complex-time Jensen bound 放进 parabolic windows，逐项记录 analytic radius \(R\)、complex growth \(M\)、projection anchor \(\|C(t_*)\|\) 与窗口 covering。目标是检查这些量能否给 distinct entry times 一个可由 NSE 预算支付的 packing estimate，而不是把定性解析性直接写成 uniform zero count。 ||| The next step places a quantitative complex-time Jensen bound in parabolic windows and records, term by term, the analytic radius \(R\), complex growth \(M\), projection anchor \(\|C(t_*)\|\), and window covering. The aim is to test whether these quantities yield a packing estimate for distinct entry times that an NSE budget can pay, rather than turning qualitative analyticity directly into a uniform zero count.
这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71P 的 80 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。 ||| This page follows the R0.00–R0.60 phase recap and organizes R0.61 through R0.71P into 80 research nodes. I record chronologically what each phase actually proves, which proposals are ruled out by a concrete counterexample or scaling analysis, and which conditions have not been derived from the Navier–Stokes equations.
R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 80 个节点沿着这个缺口推进。 ||| The R0.00–R0.60 material remains in the previous phase recap. R0.60 concludes that the complete Fourier–Leray structure and higher-order calculations can continue, but the critical quantity for general three-dimensional solutions is still uncontrolled. The following 80 nodes proceed along this gap.
R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71P 的 80 个研究节点，记录从约化递推到 projected-Lamb 热体积、soft-denominator faces、同刻 spatial batching 与 temporal-packing boundary 的路线。 ||| Research recap after R0.60: a chronological account from R0.61 through R0.71P comprising 80 research nodes, tracing the route from the reduced recurrence to projected-Lamb heat volume, soft-denominator faces, simultaneous spatial batching, and the temporal-packing boundary.
R0.61–R0.71P 的 80 节公开笔记 ||| R0.61–R0.71P: 80 public notes
R0.61–R0.71P 回顾 · 2026-08-26 ||| R0.61–R0.71P recap · 2026-08-26
R0.61–R0.71P 研究节点 ||| R0.61–R0.71P research nodes
R0.61–R0.71P｜R0.60 之后的研究回顾 ||| R0.61–R0.71P | Research recap after R0.60
R0.70A–R0.71P 完成版本 ||| R0.70A–R0.71P completed releases
R0.71G–N 依次核对 residence、matched-cell heat gap、viscous fusion、increment bridge 与 signed second jet。R0.71O 证明 soft quotient 恢复 hard 一侧迹，Jordan face cost 没有自动消失。R0.71P 再把正进入和识别为 componentwise relaxed positive-entry measure：它由逐 shell–cell 的 soft 正部先取极限、再求和得到，一般不等于 signed aggregate 的正 Jordan 部；该正测度内部没有直接的 signed shell–cell cancellation。同刻 entries 可由 bounded support overlap 与 \(\dot H^{-1}\) Littlewood–Paley square sum 做 spatial batching。完整累积仍是 time-slice budget 对 distinct entry-time counting measure 的积分，temporal packing 尚未闭合。 ||| R0.71G–N sequentially check residence, the matched-cell heat gap, viscous fusion, the increment bridge, and the signed second jet. R0.71O proves that the soft quotient recovers the one-sided hard trace, while the Jordan face cost does not disappear automatically. R0.71P then identifies the positive-entry sum as a componentwise relaxed positive-entry measure: it is obtained by first taking the limit of the soft positive part shell–cell by shell–cell and then summing, and in general is not the positive Jordan part of the signed aggregate; there is no direct signed shell–cell cancellation within this positive measure. Simultaneous entries admit spatial batching through bounded support overlap and the \(\dot H^{-1}\) Littlewood–Paley square sum. The full accumulation remains the integral of a time-slice budget against the distinct entry-time counting measure, so temporal packing is not yet closed.
R0.71G–R0.71P · 驻留、denominator faces 与 temporal packing ||| R0.71G–R0.71P · Residence, denominator faces, and temporal packing
R0.71P 把每个 entry time 的全部 faces 先合成一个 spatial batch，并由 cutoff support overlap 与 \(\dot H^{-1}\) Lamb square sum 支付。对半开窗口 \(K=[a,b)\) 且 \([a,b]\Subset I_{\rm strong}\)，固定有限 frame–cell 截断只有有限 entry mass；定性时间解析性却不给跨截断、跨解或逼近潜在奇性端点时的统一计数。sequential abstract path 只证明 ordinary budgets 不支付 distinct-time packing，不是 NSE 多-face 反例。 ||| R0.71P first combines all faces at each entry time into one spatial batch and pays it through cutoff support overlap and the \(\dot H^{-1}\) Lamb square sum. For the half-open window \(K=[a,b)\) with \([a,b]\Subset I_{\rm strong}\), a fixed finite frame–cell truncation has finite entry mass; qualitative time analyticity, however, gives no uniform count across truncations, across solutions, or while approaching a potential singular endpoint. The sequential abstract path proves only that ordinary budgets do not pay distinct-time packing; it is not an NSE multiple-face counterexample.
R0.71Q 仍不引入 moving cutoff、refresh 或更强的 total-Jordan sum。若 analytic radius、growth 或 anchor 只能由已知 continuation norm、inverse denominator、target BV 或额外 transversality 支付，我会把 zero-count route 保留为条件结论并停止这一分支。 ||| R0.71Q still does not introduce moving cutoffs, refresh, or a stronger total-Jordan sum. If the analytic radius, growth, or anchor can be paid only by a known continuation norm, inverse denominator, target BV, or additional transversality, I will retain the zero-count route only as a conditional conclusion and stop this branch.`,
  String.raw`
\(A_{j,Q,+}\) 是逐 shell–cell 的 soft/zero-padded 正进入原子，不是 ordinary hard BV 的正跳跃，也不一般等于 signed aggregate 的正 Jordan 部： \[ A_+-(A_+-A_-)^+=\min(A_+,A_-). \] 偶阶 touch 可以让 hard positive jump 为零，同时保留完整 \(A_+\)。 ||| \(A_{j,Q,+}\) is the soft/zero-padded positive-entry atom for each shell–cell, not the positive jump of ordinary hard BV and not, in general, the positive Jordan part of the signed aggregate: \[ A_+-(A_+-A_-)^+=\min(A_+,A_-). \] An even-order touch can make the hard positive jump zero while retaining the full \(A_+\).
把 complex-time Jensen zero count 放进 parabolic windows，逐项核对 analytic radius、growth、projection anchor 与窗口 covering 是否能从 NSE 预算支付。 ||| Place the complex-time Jensen zero count in parabolic windows and test, term by term, whether the analytic radius, growth, projection anchor, and window covering can be paid from NSE budgets.
把 quantitative complex-time Jensen bound 放进 parabolic windows，显式检查 analytic radius、complex growth、projection anchor 与窗口覆盖是否能从 NSE 预算支付。 ||| Place a quantitative complex-time Jensen bound in parabolic windows and explicitly test whether the analytic radius, complex growth, projection anchor, and window covering can be paid from NSE budgets.
本节关闭同刻空间 multiplicity，没有给出 uniform NSE temporal packing、内部多 face、无限 frame、Leray 极限、继续性或全局正则性结论。 ||| This section closes simultaneous spatial multiplicity; it gives no uniform NSE temporal packing, internal multiple-face construction, infinite-frame limit, Leray limit, continuation result, or global-regularity conclusion.
从有符号环带障碍走到 positive-entry temporal-packing boundary ||| From the signed-annulus obstruction to the positive-entry temporal-packing boundary
对同一时刻的全部 entries，leading direction 支撑在 cutoff cell 中。bounded overlap 与 annular \(\dot H^{-1}\) square sum 给出 \[ \mathsf e_\Lambda(t) \le M_\chi C_T\frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)} \lesssim M_\chi C_T\|u(t)\|_2Y(t)^{1/2}. \] 因而空间 cell multiplicity 被删除。 ||| For all entries at the same time, the leading direction is supported in the cutoff cell. Bounded overlap and the annular \(\dot H^{-1}\) square sum give \[ \mathsf e_\Lambda(t) \le M_\chi C_T\frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)} \lesssim M_\chi C_T\|u(t)\|_2Y(t)^{1/2}. \] Spatial cell multiplicity is therefore removed.
环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary ||| Annulus exclusion → source–core ledger → covariance spectral stratification → all-frequency conditional bridge → response-slope chord gain → common-response order-one channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary
静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 建立 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–O 依次核对 residence、matched-cell heat gap、viscous fusion、increment bridge、signed second jet 与 soft denominator faces。R0.71P 再证明同刻正进入可由空间平方和支付，而完整累积仍需要 distinct entry-time packing。 ||| After the static annular family is ruled out rigorously, the route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71A–F establish the Leray-energy projected-Lamb heat volume and its bounded-overlap localization. R0.71G–O then check residence, the matched-cell heat gap, viscous fusion, the increment bridge, the signed second jet, and soft denominator faces. R0.71P further proves that simultaneous positive entries can be paid by a spatial square sum, while the full accumulation still requires distinct entry-time packing.
累计回顾 R0.61–R0.71P · 2026-08-26 ||| Cumulative recap R0.61–R0.71P · 2026-08-26
目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71P 删除了同刻空间 cell multiplicity，并证明正进入 atoms 本身不能直接做 signed shell–cell cancellation；未闭合的是 distinct entry-time counting measure 的 uniform NSE packing。 ||| There is no new unconditional continuation criterion and no construction of a finite-time singularity. R0.71P removes simultaneous spatial cell multiplicity and proves that positive-entry atoms themselves do not permit direct signed shell–cell cancellation; uniform NSE packing of the distinct entry-time counting measure remains open.
上次综述 v1.00 · 2026-08-26 ||| Previous review v1.00 · 2026-08-26
同刻正进入可以做空间平方和，跨时累积仍需要 entry-time packing ||| Simultaneous positive entries admit a spatial square sum; accumulation across time still requires entry-time packing
同刻正进入由 bounded-overlap 与 \(\dot H^{-1}\) Lamb square sum 支付；完整时间累积被精确归约到 distinct entry-time counting measure。 ||| Simultaneous positive entries are paid by bounded overlap and the \(\dot H^{-1}\) Lamb square sum; full temporal accumulation is reduced exactly to the distinct entry-time counting measure.
完整目标精确变成 \[ \mathsf S_{\Lambda,+}(K) \le\int_K M_\chi C_T \frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)} \,d\mathfrak n_\Lambda(t). \] 其中 \(\mathfrak n_\Lambda\) 只计不同 entry times。逐分量 relaxed 正原子已经非负，不能在该目标内部再做 shell–cell signed cancellation。半开窗口上的抽象 sequential path 使计数质量按 \(N\) 增长；真实 smooth NSE initial jet 则达到 cellwise 常数 \(A_+=\|F\|_2^2/Y=1/4\)。 ||| The full target becomes exactly \[ \mathsf S_{\Lambda,+}(K) \le\int_K M_\chi C_T \frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)} \,d\mathfrak n_\Lambda(t). \] Here \(\mathfrak n_\Lambda\) counts only distinct entry times. The componentwise relaxed positive atoms are already nonnegative, so no further signed shell–cell cancellation is available inside this target. An abstract sequential path on a half-open window makes the counting mass grow like \(N\); a genuine smooth NSE initial jet attains the cellwise constant \(A_+=\|F\|_2^2/Y=1/4\).
我把 Jensen zero-count 条件放进 parabolic windows，显式记录 analytic radius \(R\)、complex growth \(M\)、projection anchor \(\|C(t_*)\|\) 与窗口 covering；不把定性解析性写成 uniform count。 ||| I place the Jensen zero-count condition in parabolic windows and explicitly record the analytic radius \(R\), complex growth \(M\), projection anchor \(\|C(t_*)\|\), and window covering; I do not turn qualitative analyticity into a uniform count.
我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71P 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。 ||| I also maintain a systematic review page that places classical theory, five main literature branches, the candidate blow-up exclusion tree, progress from 2019—2026, and this site's R0.69P–R0.71P route on one map. Historical nodes R0.61–R0.69O remain in the cumulative recap.
下一步 R0.71Q： ||| Next step R0.71Q:
研究笔记 R0.71P · 2026-08-26 ||| Research note R0.71P · 2026-08-26
阅读 R0.71P 研究笔记 → ||| Read the R0.71P research note →
展开 50 篇公开笔记 ||| Expand 50 public notes
综述 v1.01 · 2026-08-26 ||| Review v1.01 · 2026-08-26
R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、固定匹配小区、soft-denominator faces 与 positive-entry temporal packing。R0.70A–R0.71P 共 42 个完成版本。 ||| The route after R0.60 has twelve phases: reduced Picard and the shear boundary, transverse perturbations, the local pressure budget, signed physical annuli, moving labels and source–core duality, the defect tensor and finite observations, complete-frame covariance, the constant-projection boundary, positive output and the material-heat tent, projected-Lamb heat volume, local heat packing and the critical trace obstruction, and finally the residence boundary, fixed matched cells, soft-denominator faces, and positive-entry temporal packing. R0.70A–R0.71P contains 42 completed releases.
R0.60 recap 之后的累计回顾收录 80 个节点；全站现有 140 篇公开研究笔记 ||| The cumulative recap after the R0.60 recap contains 80 nodes; the site now has 140 public research notes
R0.71P 已完成： ||| R0.71P completed:`,
  String.raw`
\(A_{j,Q,+}\) 是逐 shell–cell 的 soft/zero-padded 正进入原子，不是 ordinary hard BV 的正跳跃，也不一般等于 signed aggregate 的正 Jordan 部： \[ A_+-(A_+-A_-)^+=\min(A_+,A_-). \] 偶阶 touch 可以让 hard positive jump 为零，同时保留完整 \(A_+\)。 ||| \(A_{j,Q,+}\) is the soft/zero-padded positive-entry atom for each shell–cell, not the positive jump of ordinary hard BV and not, in general, the positive Jordan part of the signed aggregate: \[ A_+-(A_+-A_-)^+=\min(A_+,A_-). \] An even-order touch can make the hard positive jump zero while retaining the full \(A_+\).
把 complex-time Jensen zero count 放进 parabolic windows，逐项核对 analytic radius、growth、projection anchor 与窗口 covering 是否能从 NSE 预算支付。 ||| Place the complex-time Jensen zero count in parabolic windows and test, term by term, whether the analytic radius, growth, projection anchor, and window covering can be paid from NSE budgets.
把 quantitative complex-time Jensen bound 放进 parabolic windows，显式检查 analytic radius、complex growth、projection anchor 与窗口覆盖是否能从 NSE 预算支付。 ||| Place a quantitative complex-time Jensen bound in parabolic windows and explicitly test whether the analytic radius, complex growth, projection anchor, and window covering can be paid from NSE budgets.
本节关闭同刻空间 multiplicity，没有给出 uniform NSE temporal packing、内部多 face、无限 frame、Leray 极限、继续性或全局正则性结论。 ||| This section closes simultaneous spatial multiplicity; it gives no uniform NSE temporal packing, internal multiple-face construction, infinite-frame limit, Leray limit, continuation result, or global-regularity conclusion.
从有符号环带障碍走到 positive-entry temporal-packing boundary ||| From the signed-annulus obstruction to the positive-entry temporal-packing boundary
对同一时刻的全部 entries，leading direction 支撑在 cutoff cell 中。bounded overlap 与 annular \(\dot H^{-1}\) square sum 给出 \[ \mathsf e_\Lambda(t) \le M_\chi C_T\frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)} \lesssim M_\chi C_T\|u(t)\|_2Y(t)^{1/2}. \] 因而空间 cell multiplicity 被删除。 ||| For all entries at the same time, the leading direction is supported in the cutoff cell. Bounded overlap and the annular \(\dot H^{-1}\) square sum give \[ \mathsf e_\Lambda(t) \le M_\chi C_T\frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)} \lesssim M_\chi C_T\|u(t)\|_2Y(t)^{1/2}. \] Spatial cell multiplicity is therefore removed.
环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary ||| Annulus exclusion → source–core ledger → covariance spectral stratification → all-frequency conditional bridge → response-slope chord gain → common-response order-one channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary
静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 建立 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–O 依次核对 residence、matched-cell heat gap、viscous fusion、increment bridge、signed second jet 与 soft denominator faces。R0.71P 再证明同刻正进入可由空间平方和支付，而完整累积仍需要 distinct entry-time packing。 ||| After the static annular family is ruled out rigorously, the route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71A–F establish the Leray-energy projected-Lamb heat volume and its bounded-overlap localization. R0.71G–O then check residence, the matched-cell heat gap, viscous fusion, the increment bridge, the signed second jet, and soft denominator faces. R0.71P further proves that simultaneous positive entries can be paid by a spatial square sum, while the full accumulation still requires distinct entry-time packing.
累计回顾 R0.61–R0.71P · 2026-08-26 ||| Cumulative recap R0.61–R0.71P · 2026-08-26
目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71P 删除了同刻空间 cell multiplicity，并证明正进入 atoms 本身不能直接做 signed shell–cell cancellation；未闭合的是 distinct entry-time counting measure 的 uniform NSE packing。 ||| There is no new unconditional continuation criterion and no construction of a finite-time singularity. R0.71P removes simultaneous spatial cell multiplicity and proves that positive-entry atoms themselves do not permit direct signed shell–cell cancellation; uniform NSE packing of the distinct entry-time counting measure remains open.
上次综述 v1.00 · 2026-08-26 ||| Previous review v1.00 · 2026-08-26
同刻正进入可以做空间平方和，跨时累积仍需要 entry-time packing ||| Simultaneous positive entries admit a spatial square sum; accumulation across time still requires entry-time packing
同刻正进入由 bounded-overlap 与 \(\dot H^{-1}\) Lamb square sum 支付；完整时间累积被精确归约到 distinct entry-time counting measure。 ||| Simultaneous positive entries are paid by bounded overlap and the \(\dot H^{-1}\) Lamb square sum; full temporal accumulation is reduced exactly to the distinct entry-time counting measure.
完整目标精确变成 \[ \mathsf S_{\Lambda,+}(K) \le\int_K M_\chi C_T \frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)} \,d\mathfrak n_\Lambda(t). \] 其中 \(\mathfrak n_\Lambda\) 只计不同 entry times。逐分量 relaxed 正原子已经非负，不能在该目标内部再做 shell–cell signed cancellation。半开窗口上的抽象 sequential path 使计数质量按 \(N\) 增长；真实 smooth NSE initial jet 则达到 cellwise 常数 \(A_+=\|F\|_2^2/Y=1/4\)。 ||| The full target becomes exactly \[ \mathsf S_{\Lambda,+}(K) \le\int_K M_\chi C_T \frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)} \,d\mathfrak n_\Lambda(t). \] Here \(\mathfrak n_\Lambda\) counts only distinct entry times. The componentwise relaxed positive atoms are already nonnegative, so no further signed shell–cell cancellation is available inside this target. An abstract sequential path on a half-open window makes the counting mass grow like \(N\); a genuine smooth NSE initial jet attains the cellwise constant \(A_+=\|F\|_2^2/Y=1/4\).
我把 Jensen zero-count 条件放进 parabolic windows，显式记录 analytic radius \(R\)、complex growth \(M\)、projection anchor \(\|C(t_*)\|\) 与窗口 covering；不把定性解析性写成 uniform count。 ||| I place the Jensen zero-count condition in parabolic windows and explicitly record the analytic radius \(R\), complex growth \(M\), projection anchor \(\|C(t_*)\|\), and window covering; I do not turn qualitative analyticity into a uniform count.
我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71P 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。 ||| I also maintain a systematic review page that places classical theory, five main literature branches, the candidate blow-up exclusion tree, progress from 2019—2026, and this site's R0.69P–R0.71P route on one map. Historical nodes R0.61–R0.69O remain in the cumulative recap.
下一步 R0.71Q： ||| Next step R0.71Q:
研究笔记 R0.71P · 2026-08-26 ||| Research note R0.71P · 2026-08-26
阅读 R0.71P 研究笔记 → ||| Read the R0.71P research note →
展开 50 篇公开笔记 ||| Expand 50 public notes
综述 v1.01 · 2026-08-26 ||| Review v1.01 · 2026-08-26
R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、固定匹配小区、soft-denominator faces 与 positive-entry temporal packing。R0.70A–R0.71P 共 42 个完成版本。 ||| The route after R0.60 has twelve phases: reduced Picard and the shear boundary, transverse perturbations, the local pressure budget, signed physical annuli, moving labels and source–core duality, the defect tensor and finite observations, complete-frame covariance, the constant-projection boundary, positive output and the material-heat tent, projected-Lamb heat volume, local heat packing and the critical trace obstruction, and finally the residence boundary, fixed matched cells, soft-denominator faces, and positive-entry temporal packing. R0.70A–R0.71P contains 42 completed releases.
R0.60 recap 之后的累计回顾收录 80 个节点；全站现有 140 篇公开研究笔记 ||| The cumulative recap after the R0.60 recap contains 80 nodes; the site now has 140 public research notes
R0.71P 已完成： ||| R0.71P completed:`,
]
  .join("\n")
  .replaceAll("__I18N_BACKTICK__", "`");

const rawRows = translationRows
  .trim()
  .split("\n")
  .filter((row) => row.length > 0);
const rows = [
  ...new Map(
    rawRows.map((row) => [row.slice(0, row.indexOf(" ||| ")), row]),
  ).values(),
];
const additions = new Map(
  rows.map((row) => {
    const separator = " ||| ";
    const index = row.indexOf(separator);
    if (index < 1) throw new Error("invalid translation row: " + row);
    return [row.slice(0, index), row.slice(index + separator.length)];
  }),
);
if (additions.size !== rows.length) {
  throw new Error("duplicate Chinese keys after R0.71P row normalization");
}

function extractNumericTokens(value) {
  return [...String(value).matchAll(/\d+(?:[.\-–—]\d+)*/g)].map(
    (match) => match[0],
  );
}

function sameTokens(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

const activePages = [
  "research-review.html",
  "literature-review.html",
  "recap-r0-61-r0-71p.html",
  "notes/r0-71p.html",
];
for (const relative of activePages) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.01')) {
    throw new Error(relative + ": expected i18n cache version v1.01");
  }
}

const batchId = /^r071p\d+$/;
const currentWithoutBatch = current.filter((entry) => !batchId.test(entry.id));
const currentByChinese = new Map(
  currentWithoutBatch.map((entry) => [entry.zh, entry]),
);
if (currentByChinese.size !== currentWithoutBatch.length) {
  throw new Error(
    "duplicate Chinese keys already present outside the R0.71P batch",
  );
}

const sourceByChinese = new Map(source.map((entry) => [entry.zh, entry]));
if (sourceByChinese.size !== source.length) {
  throw new Error("duplicate Chinese keys in collected site strings");
}

const missing = source.filter((entry) => !currentByChinese.has(entry.zh));
const missingChinese = new Set(missing.map((entry) => entry.zh));
if (additions.size !== missing.length) {
  const uncovered = missing
    .filter((entry) => !additions.has(entry.zh))
    .map((entry) => entry.zh);
  throw new Error(
    "expected additions to equal the " +
      missing.length +
      " active missing strings, found " +
      additions.size +
      "\nuncovered:\n" +
      uncovered.join("\n---\n"),
  );
}
for (const entry of missing) {
  if (!additions.has(entry.zh)) {
    throw new Error("missing translation: " + entry.zh);
  }
}
for (const zh of additions.keys()) {
  if (!missingChinese.has(zh)) {
    throw new Error("translation is not an active missing string: " + zh);
  }
}

const translatedEntries = missing.map((entry, index) => {
  const en = additions.get(entry.zh);
  const zhProtected = extractProtectedTokens(entry.zh);
  const enProtected = extractProtectedTokens(en);
  if (!sameTokens(zhProtected, enProtected)) {
    throw new Error(
      "protected-token mismatch for " +
        entry.zh +
        "\nZH " +
        JSON.stringify(zhProtected) +
        "\nEN " +
        JSON.stringify(enProtected),
    );
  }

  const zhNumeric = extractNumericTokens(entry.zh);
  const enNumeric = extractNumericTokens(en);
  if (!sameTokens(zhNumeric, enNumeric)) {
    throw new Error(
      "numeric-token mismatch for " +
        entry.zh +
        "\nZH " +
        JSON.stringify(zhNumeric) +
        "\nEN " +
        JSON.stringify(enNumeric),
    );
  }
  if (!en.trim() || containsChinese(en)) {
    throw new Error(
      "blank or Chinese-containing English translation for " + entry.zh,
    );
  }
  if (/\b(?:we|our|ours|us)\b/i.test(en)) {
    throw new Error("first-person plural voice in translation for " + entry.zh);
  }

  return {
    ...entry,
    id: "r071p" + String(index + 1).padStart(3, "0"),
    en,
  };
});

const merged = [...currentWithoutBatch, ...translatedEntries];
const mergedChinese = new Set(merged.map((entry) => entry.zh));
const mergedIds = new Set(merged.map((entry) => entry.id));
if (mergedChinese.size !== merged.length) {
  throw new Error("translation merge produced duplicate Chinese keys");
}
if (mergedIds.size !== merged.length) {
  throw new Error("translation merge produced duplicate IDs");
}

const invalid = merged.filter(
  (entry) =>
    !entry.en?.trim() ||
    containsChinese(entry.en) ||
    !sameTokens(
      extractProtectedTokens(entry.zh),
      extractProtectedTokens(entry.en),
    ),
);
if (invalid.length) {
  throw new Error(
    "invalid translations after merge: " +
      invalid.map((entry) => entry.id).join(", "),
  );
}

await writeFile(translationPath, JSON.stringify(merged, null, 2) + "\n");
console.log(
  JSON.stringify(
    {
      source: source.length,
      existingWithoutBatch: currentWithoutBatch.length,
      activeMissingBefore: missing.length,
      added: translatedEntries.length,
      firstId: translatedEntries.at(0)?.id,
      lastId: translatedEntries.at(-1)?.id,
      total: merged.length,
      duplicateChinese: merged.length - mergedChinese.size,
      duplicateIds: merged.length - mergedIds.size,
      invalid: invalid.length,
      englishWithChinese: translatedEntries.filter((entry) =>
        containsChinese(entry.en),
      ).length,
      firstPersonPlural: translatedEntries.filter((entry) =>
        /\b(?:we|our|ours|us)\b/i.test(entry.en),
      ).length,
      protectedTokenMismatches: translatedEntries.filter(
        (entry) =>
          !sameTokens(
            extractProtectedTokens(entry.zh),
            extractProtectedTokens(entry.en),
          ),
      ).length,
      numericTokenMismatches: translatedEntries.filter(
        (entry) =>
          !sameTokens(
            extractNumericTokens(entry.zh),
            extractNumericTokens(entry.en),
          ),
      ).length,
    },
    null,
    2,
  ),
);
