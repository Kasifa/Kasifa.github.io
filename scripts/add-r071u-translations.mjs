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

const translationRows = String.raw`
比较 atom mass 与 second-time-jet 两行，并测试 level-integrated 或 amplitude-thresholded excursion。 ||| Compare atom mass with the two second-time-jet rows and test level-integrated or amplitude-thresholded excursions.
处理 level-integrated crossings、variation 或 local time，不直接给 fixed zero-level normalized derivative mass。bounded audit 未定位到完整 R0.71U theorem；这不是原创性、优先权或不存在性结论。 ||| treat level-integrated crossings, variation, or local time and do not directly provide the normalized derivative mass at a fixed zero level. The bounded audit located no complete R0.71U theorem; this is not a claim of originality, priority, or nonexistence.
打开 85 节完整索引 ||| Open the complete 85-section index
给 Chebyshev-system interpolation 背景。 ||| provide the Chebyshev-system interpolation background.
给 upper critical Carleson control。 ||| provide upper critical Carleson control.
记录 exact 2D3C reduction； ||| record the exact 2D3C reduction;
开放接口 · R0.71V ||| Open interface · R0.71V
累计回顾与 85 节索引 ||| cumulative recap and 85-section index
文献综述 v1.06 · 2026-08-26 ||| Literature review v1.06 · 2026-08-26
我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.71U 只列为研究笔记。我不把计算或笔记外推成正则性定理。 ||| I list published theorems as known results, mark 2026 preprints separately, and classify this site's R0.69P–R0.71U material only as research notes. I do not extrapolate calculations or notes into regularity theorems.
研究带外力的 projection controllability；本节只选择初值、演化无外力，并允许解随 finite time set 改变，量词不同。 ||| study projection controllability with external forcing; this section selects only initial data, keeps the evolution unforced, and allows the solution to change with the finite time set, so the quantifiers differ.
支持 classical time-analyticity 与 strong-solution background。 ||| support classical time analyticity and the strong-solution background.
中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–T 给出 conditional Jensen/incidence、packet/Bessel 与 genuine internal-entry scale audits。R0.71U 再给出 classical second-time-jet packing，并用 exact unforced 2.5D NSE family 排除 unit energy–enstrophy ball 上的统一 raw count。保留下来的结果都不是全局正则性结论。 ||| . R0.69P–R0.71P reaches the positive-entry temporal-packing boundary; R0.71Q–T gives conditional Jensen/incidence, packet/Bessel, and genuine internal-entry scale audits. R0.71U then gives classical second-time-jet packing and uses an exact unforced 2.5D NSE family to rule out a uniform raw count on the unit energy-enstrophy ball. None of the retained results is a global-regularity conclusion.
classical second-time jet 可求和，raw count 无统一界 ||| The classical second-time jet is summable; raw count has no uniform bound
finite-dimensional IFT 的精确对象是 four-mode thin projection；与 seed 分离的 compact full support 需要把变量扩到全部 target modes。double scaling 给 atom λ⁻⁴、bare budget λ⁻⁶。 ||| The exact object of the finite-dimensional IFT is a four-mode thin projection; compact full support separated from the seed requires extending the variables to every target mode. Double scaling gives an atom of λ⁻⁴ and a bare budget of λ⁻⁶.
Hilbert sampling 给 zero-count-independent all-shell theorem；第一行 Leray-paid，第二行保留 recurrence tax。exact unforced 2.5D family 在每个 finite set 上选择新轨迹，排除 unit energy–enstrophy ball 上的统一 raw count；atoms 可缩小。 ||| Hilbert sampling gives a zero-count-independent all-shell theorem; the first row is Leray-paid, while the second retains the recurrence tax. The exact unforced 2.5D family selects a new trajectory for each finite set and rules out a uniform raw count on the unit energy-enstrophy ball; the atoms may shrink.
R0.71U 的一手文献边界 ||| Primary-source boundary for R0.71U
R0.71U 对带 \(\inf_KY>0\) 的 compact classical trajectory 证明 all-shell second-time-jet estimate；closed-interval endpoints 由 classical trace 纳入。第一行有 normalized Leray–Lamb payment，第二行保留 \(\omega_t\) 与 \(L_t\)，所以不是 Leray closure。exact torus scaling 只按 integer dilation 和协变运输的 frame/window 陈述。另一个 exact unforced 2.5D family 对每个 finite time set 选择新轨迹，排除 unit energy–enstrophy ball 上 raw count 的统一界；atom 可缩小，故 weighted packing 仍开放。R0.71V 只比较 weighted recurrence、second-time-jet tax 与 Leray-paid excursion。我继续用下面六条筛选。 ||| R0.71U proves an all-shell second-time-jet estimate for compact classical trajectories with \(\inf_KY>0\); classical traces include closed-interval endpoints. The first row has normalized Leray-Lamb payment, while the second retains \(\omega_t\) and \(L_t\), so this is not a Leray closure. Exact torus scaling is stated only for integer dilations and covariantly transported frames/windows. A second exact unforced 2.5D family selects a new trajectory for each finite time set and rules out a uniform raw count on the unit energy-enstrophy ball; atoms may shrink, so weighted packing remains open. R0.71V compares only weighted recurrence, the second-time-jet tax, and Leray-paid excursions. I continue to use the six filters below.
R0.71U 关闭了什么，R0.71V 只检查什么 ||| What R0.71U closes and what R0.71V alone tests
二次 Duhamel 展开同时给出 ||| The quadratic Duhamel expansion also gives
该有限矩阵可逆，隐函数定理给出真实修正 \(z(a)\)，使这个精确四模投影在 τ 为零。这里不能把四模消去误写成任意宽环带消去。若紧支撑目标与 seed shell 分离，我把变量空间扩为其全部有限 lattice support；此时 \(D_z\Phi=e^{\nu\tau\Delta}\) 在完整目标空间上仍为对角可逆矩阵，因而可以同时消去每个受支持模。 ||| This finite matrix is invertible, and the implicit function theorem gives a genuine correction \(z(a)\) that makes the exact four-mode projection vanish at τ. Four-mode cancellation cannot be restated as cancellation of an arbitrary broad annulus. If the compactly supported target is separated from the seed shell, I extend the variable space to its complete finite lattice support; then \(D_z\Phi=e^{\nu\tau\Delta}\) remains diagonal and invertible on the full target space, so every supported mode can be cancelled simultaneously.
真实 smooth positive-time exact-target internal entry；与 seed 分离的完整有限目标支撑扩展；至少一个 induced local positive cell；global positive entry 自动 simple；bounded-energy/enstrophy internal scaling no-go；finite outgoing-coarea identity；finite conditional trace-variation theorem。 ||| a genuine smooth positive-time exact-target internal entry; the complete finite-target-support extension separated from the seed; at least one induced positive local cell; automatic simplicity of a global positive entry; the bounded-energy/enstrophy internal scaling no-go; the finite outgoing-coarea identity; and the finite conditional trace-variation theorem.
只改初始目标空间，在预定正时间把完整声明投影压到零 ||| Modify only the initial target space to make the complete declared projection vanish at a prescribed positive time
R0.71S 的缩放结论只覆盖初始 observation face。本节对同一 Fourier seed 做有限壳预补偿：标准局部 NSE 流映射与有限维隐函数定理把精确的四模目标投影在预定正时间压到零，而 nonlinear Lamb forcing 仍非零。该零点是严格内部、simple、positive。随后取振幅 \(a_\lambda=\lambda^{-2}\) 再作 NSE 协变缩放，entry 原子按 λ⁻⁴、裸 normalized Leray-Lamb 时间预算按 λ⁻⁶，最优常数至少按 λ² 发散；初始能量与临界范数同时趋零。 ||| The scaling result in R0.71S covers only the initial observation face. This section precompensates finitely many shells for the same Fourier seed: the standard local NSE flow map and a finite-dimensional implicit function theorem make the exact four-mode target projection vanish at a prescribed positive time while nonlinear Lamb forcing remains nonzero. The zero is strictly internal, simple, and positive. After choosing the amplitude \(a_\lambda=\lambda^{-2}\) and applying NSE-covariant scaling, the entry atom scales as λ⁻⁴, the bare normalized Leray-Lamb time budget as λ⁻⁶, and the optimal constant diverges at least as λ²; the initial energy and critical norm both tend to zero.
01 · 零点采样 ||| 01 · Zero sampling
02 · all-shell 定理 ||| 02 · All-shell theorem
03 · NSE 账本 ||| 03 · NSE ledger
04 · 真实 recurrence ||| 04 · Genuine recurrence
06 · R0.71T 更正 ||| 06 · R0.71T correction
版本 v0.71U · 2026-08-26 ||| Version v0.71U · 2026-08-26
报告、文献、证书与期刊附图包全部保留 ||| The report, literature audit, certificates, and journal figure package are all retained
本节把 R0.71T 的二择一改写为更精确的边界。entry jet 的确可求和，但现有证明必须支付 \(C_{tt}\)；真实 NSE recurrence 又说明 analyticity、simplicity 或 bounded initial energy/enstrophy 不能提供统一 raw count。继续只研究零点数量不会关闭尺度零 packing。 ||| This section replaces the R0.71T dichotomy with a more precise boundary. The entry jet is summable, but the present proof must pay for \(C_{tt}\); genuine NSE recurrence also shows that analyticity, simplicity, or bounded initial energy/enstrophy cannot provide a uniform raw count. Studying only the number of zeros cannot close scale-zero packing.
本节得到两个互补结论。对满足 \(\inf_KY>0\) 的紧 classical 轨道区间，Hilbert 值零点采样把所有 global-shell positive entries 统一压到一阶与二阶时间 jet 的积分；常数不依赖零点数、最小间距或有限壳截断。第一行可由 normalized Leray–Lamb 账本支付，第二行保留 \(\omega_t\) 与 \(L_t\) 的 recurrence tax，因此不是 Leray-level closure。另一方面，一个真实、无外力、全局光滑的 2.5D NSE 不变类可在任意指定的有限时刻返回同一紧支撑环带；初始能量和 enstrophy 可统一限制在单位球内，但这些 entry atom 可以缩小。 ||| This section gives two complementary conclusions. On a compact classical trajectory interval satisfying \(\inf_KY>0\), Hilbert-valued zero sampling bounds all global-shell positive entries by integrals of the first and second time jets; the constant is independent of the number of zeros, minimum spacing, or finite shell truncation. The first row is paid by the normalized Leray-Lamb ledger, while the second retains the recurrence tax in \(\omega_t\) and \(L_t\), so this is not a Leray-level closure. Separately, a genuine unforced globally smooth invariant 2.5D NSE class can return to the same compactly supported annulus at any prescribed finite collection of times; initial energy and enstrophy remain uniformly bounded by one, but the entry atoms may shrink.
并保留至少 \(N\) 个指定的 positive entries。因此 unit energy–enstrophy ball 上不存在 raw global-shell entry count 的统一上界，也没有统一 minimum separation。另一方面，沿小参数 \(s\)，每个原子只满足 ||| while retaining at least \(N\) prescribed positive entries. Therefore no uniform bound for the raw global-shell entry count, and no uniform minimum separation, exists on the unit energy-enstrophy ball. On the other hand, along the small parameter \(s\), each atom only satisfies
采样 ||| Sampling
除以 \(Y\) 后，第一行由 normalized Leray–Lamb ledger 加上 \(\nu^2|K|\) 控制；前面的 \(|K|^{-1}\) 是支付每壳首个 trace 所需的尺度。第二行只在 classical solution 上有限，ordinary Leray energy inequality 不控制 \(\omega_t\) 或 \(L_t\)。对 exact torus scaling，只使用 integer \(\lambda\) 并协变运输 time window 与 multiplier frame；两行连同 entry mass 都具有零尺度指数。 ||| After division by \(Y\), the first row is controlled by the normalized Leray-Lamb ledger plus \(\nu^2|K|\); the factor \(|K|^{-1}\) supplies the scaling needed to pay for the first trace in each shell. The second row is finite only for a classical solution, and the ordinary Leray energy inequality does not control \(\omega_t\) or \(L_t\). Exact torus scaling uses only integer \(\lambda\) and covariantly transports the time window and multiplier frame; both rows and the entry mass have scale exponent zero.
处理 level-integrated crossings、variation 或 local time。这些文献不直接给 fixed zero-level normalized derivative mass 的求和定理。 ||| treat level-integrated crossings, variation, or local time. These sources do not directly give a summation theorem for normalized derivative mass at a fixed zero level.
第一行是 Leray-level，第二行是尚未关闭的 recurrence tax ||| The first row is Leray-level; the second is the still-open recurrence tax
对 compact classical interval \(K\)，记 \(\ell=|K|\)、\(\mathcal R_Y(K)=\sup_KY/\inf_KY\)。在统一 annular support 与 upper frame bound 下，任意有限壳集 \(\Lambda\) 满足 ||| For a compact classical interval \(K\), set \(\ell=|K|\) and \(\mathcal R_Y(K)=\sup_KY/\inf_KY\). Under uniform annular support and an upper frame bound, every finite shell set \(\Lambda\) satisfies
二阶时间 jet 可以求和， ||| The second-time jet is summable;
负面结果必须阻止 atom mass 塌缩；正面结果必须控制 distinguished zero level，不能只控制 almost every positive level。 ||| A negative result must prevent atom mass from collapsing; a positive result must control the distinguished zero level, not merely almost every positive level.
附图显示三次指定回返、cutoff 稳定性与 shrinking-atom 边界 ||| The figure shows three prescribed returns, cutoff stability, and the shrinking-atom boundary
给 critical upper Carleson control； ||| gives critical upper Carleson control;
给出 Chebyshev-system interpolation 背景。 ||| gives the Chebyshev-system interpolation background.
更正 ||| Correction
构成 Chebyshev system。有限维隐函数定理据此给出一个参数曲线，使同一 compact real-even annular multiplier 的完整声明投影在每个 \(t_m\) 精确归零，并且每个零点都是 first-order positive entry。 ||| form a Chebyshev system. The finite-dimensional implicit function theorem then gives a parameter curve that makes the complete declared projection of the same compact real-even annular multiplier vanish exactly at each \(t_m\), with every zero a first-order positive entry.
回返 ||| Recurrence
记录 2D3C reduction； ||| records the 2D3C reduction;
解析账本与独立重建分别检查关键边界 ||| The analytic ledger and independent reconstruction check the key boundaries separately
可利用的正面结构是 second-time-jet inequality。它给出一个与 NSE scaling 完全匹配的 benchmark，后续任何替代量都必须解释如何支付或避免 recurrence tax，同时保留 atom mass。 ||| The useful positive structure is the second-time-jet inequality. It gives a benchmark exactly matched to NSE scaling; any later replacement must explain how to pay or avoid the recurrence tax while retaining atom mass.
连续零点之间的平均导数为零，免去 zero-spacing 常数 ||| The derivative has zero mean between consecutive zeros, removing any zero-spacing constant
量词必须保持清楚：每个 finite set 和每个 \(N\) 可以选择一个新解。这里没有构造一条固定轨道去实现无限或任意可延长的 prescribed time set。 ||| The quantifiers must remain explicit: a new solution may be selected for each finite set and each \(N\). No single fixed trajectory is constructed to realize an infinite or arbitrarily extensible prescribed time set.
零点计数路线已经关闭，weighted recurrence 成为明确缺口 ||| The zero-count route is closed; weighted recurrence is now the precise gap
零点数无关的 Hilbert 采样、classical second-jet packing、Leray 边界、真实 2.5D NSE recurrence 与 shrinking-atom 边界。 ||| zero-count-independent Hilbert sampling, classical second-jet packing, the Leray boundary, genuine 2.5D NSE recurrence, and the shrinking-atom boundary.
令 \(X\in H^2(I;H)\)，\(I\) 的长度为 \(\ell\)，并取任意有限个有序零点 \(X(t_k)=0\)；classical trace 允许零点落在闭区间端点。则 ||| Let \(X\in H^2(I;H)\), let \(I\) have length \(\ell\), and take any finite ordered zeros \(X(t_k)=0\); the classical trace permits zeros at closed-interval endpoints. Then
每个 finite time set 可选一个新的 smooth solution；不声称一条固定解实现所有集合。 ||| a new smooth solution may be selected for each finite time set; no single fixed solution is claimed to realize every set.
每个给定 finite time set 都可选择一个新的真实无外力 NSE 解 ||| A new genuine unforced NSE solution can be selected for every prescribed finite time set
取精确不变类 ||| Take the exact invariant class
删除 second-time-jet tax；由 Leray energy 控制 \(\omega_t\) 或 \(L_t\)；weighted atom no-go；weak-solution jet trace；single-trajectory infinite recurrence；continuation、finite-time singularity 或 global regularity。 ||| removal of the second-time-jet tax; control of \(\omega_t\) or \(L_t\) by Leray energy; a weighted-atom no-go; a weak-solution jet trace; single-trajectory infinite recurrence; continuation, a finite-time singularity, or global regularity.
是对角可逆矩阵，可以同时消去每个 target-support mode。这个更正不改变 R0.71T 的 exact-thin theorem 或 scaling no-go。 ||| is a diagonal invertible matrix, so every target-support mode can be cancelled simultaneously. This correction does not change the exact-thin theorem or scaling no-go in R0.71T.
首个样本由 \(H^1\) point trace 支付。对后续样本，连续两个零点给出 \(\int_{t_{k-1}}^{t_k}X'=0\)；精确积分公式和 Cauchy–Schwarz 把它压到互不相交的 gap 上。这里的 \(\ell\) 是整个审计区间长度，不是最小零点间距、Voronoi 半径或假设的 forward window。证明没有使用错误的 vector-valued Rolle theorem。 ||| The first sample is paid by an \(H^1\) point trace. For later samples, consecutive zeros give \(\int_{t_{k-1}}^{t_k}X'=0\); an exact integral formula and Cauchy-Schwarz charge it to disjoint gaps. Here \(\ell\) is the length of the full audited interval, not the minimum zero spacing, a Voronoi radius, or an assumed forward window. The proof uses no false vector-valued Rolle theorem.
数值 shooting 只用于复核一个 \(N=3\) 的 finite lattice 例子。continuum theorem、uniform energy–enstrophy construction 与 classical second-jet bound 都来自解析证明。 ||| Numerical shooting only corroborates one finite-lattice example with \(N=3\). The continuum theorem, uniform energy-enstrophy construction, and classical second-jet bound all come from analytic proofs.
四模 thin projection 与完整有限支撑是两个精确表述 ||| The four-mode thin projection and complete finite support are two distinct exact statements
缩放 passive component 后，再沿足够小的隐函数曲线取非零点，可同时保证 ||| After scaling the passive component and taking a nonzero point sufficiently close to zero on the implicit curve, both bounds hold:
它是三维不可压 NSE 的全局光滑无外力子类，不是 forced surrogate。对任意 \(N\ge1\) 和 \(0<t_1<\cdots<t_N<T\)，选择 \(2N+1\) 个 shear 参数。响应函数 ||| This is a globally smooth unforced subclass of the three-dimensional incompressible NSE, not a forced surrogate. For any \(N\ge1\) and \(0<t_1<\cdots<t_N<T\), choose \(2N+1\) shear parameters. The response functions
同一时刻的所有 global-shell positive roots 还满足 \(\sum_jJ_j(t)\lesssim\|L(t)\|_{\dot H^{-1}}^2/Y(t)\)。真正困难是不同时间的 recurrence，而不是 same-time spatial batching。 ||| All global-shell positive roots at the same time also satisfy \(\sum_jJ_j(t)\lesssim\|L(t)\|_{\dot H^{-1}}^2/Y(t)\). The real difficulty is recurrence at distinct times, not same-time spatial batching.
图 R0.71U。固定 \(\nu=0.02\)、\(K=L=1\)、\(d=8\) 与三个指定时刻，有限 lattice shooting 把完整目标 annulus 的唯一共轭模对压到零；三个 target slopes 非零。主 cutoff 与独立加密给出一致结果。该图复核 finite example，不代替无限维 IFT、Hilbert sampling lemma 或 energy–enstrophy 量词。 ||| Figure R0.71U. With \(\nu=0.02\), \(K=L=1\), \(d=8\), and three prescribed times fixed, finite-lattice shooting makes the unique conjugate mode pair in the complete target annulus vanish; all three target slopes are nonzero. The primary cutoff and independent refinement agree. This figure corroborates a finite example and does not replace the infinite-dimensional IFT, Hilbert sampling lemma, or energy-enstrophy quantifiers.
文献支持工具与 2D3C 背景，不替代本节证明 ||| The literature supports the tools and 2D3C background but does not replace the proofs in this section
下一步量化 recurrence family 的 weighted atom sum 相对定理两行的大小，检查 \(C_{tt}\) tax 是否在该族上必要。并行测试 level-integrated 或 amplitude-thresholded excursions 能否用 genuine Leray-paid variation 代替 fixed zero-level charge。 ||| The next step quantifies the weighted atom sum of the recurrence family relative to the theorem's two rows and tests whether the \(C_{tt}\) tax is necessary on this family. In parallel, level-integrated or amplitude-thresholded excursions are tested as possible replacements of the fixed zero-level charge through genuine Leray-paid variation.
下一对象：weighted recurrence / excursion ||| Next object: weighted recurrence/excursion
研究笔记 R0.71U · SECOND-TIME JET · EXACT RECURRENCE ||| Research note R0.71U · SECOND-TIME JET · EXACT RECURRENCE
研究笔记 R0.71U：Hilbert 零点采样给出 classical trajectory 上的 all-shell 二阶时间 jet 求和；真实无外力 2.5D NSE 解可在任意给定有限时刻返回同一紧支撑环带。 ||| Research note R0.71U: Hilbert zero sampling sums the all-shell second-time jet on a classical trajectory; a genuine unforced 2.5D NSE solution can return to the same compactly supported annulus at any prescribed finite set of times.
研究带外力的 finite-dimensional projection controllability；本节只选择初值、演化无外力，并允许解随 finite time set 改变，量词不同。 ||| study finite-dimensional projection controllability with external forcing; this section selects only initial data, keeps the evolution unforced, and allows the solution to change with the finite time set, so the quantifiers differ.
原子 ||| Atom
在 \(\inf_KY>0\) 的 classical 区间上，常数与零点数和壳截断无关 ||| On a classical interval with \(\inf_KY>0\), the constant is independent of the zero count and shell truncation
这不是千禧年问题的解答。本节没有得到弱解零点 trace、继续性判据、有限时奇性或全局正则性。 ||| This is not a solution to the Millennium Problem. This section does not establish zero traces for weak solutions, a continuation criterion, a finite-time singularity, or global regularity.
正项可用 monotone convergence 延伸到 countable shells。该定理是 trajectory-wise classical estimate，明确要求 \(0<\inf_KY\le\sup_KY<\infty\)。它不是弱解定理，也不是标准的 \(|K|\)-Carleson estimate。 ||| The nonnegative terms extend to countable shells by monotone convergence. This theorem is a trajectory-wise classical estimate and explicitly requires \(0<\inf_KY\le\sup_KY<\infty\). It is neither a weak-solution theorem nor a standard \(|K|\)-Carleson estimate.
支持 classical trajectory 上的时间解析性与强解背景。 ||| support time analyticity along classical trajectories and the strong-solution background.
状态 · R0.71U 两条定理完成 ||| Status · two R0.71U theorems completed
admissible radius、插值斜率与 passive amplitude 都可能随 \(N\) 变小。这不是 weighted-atom counterexample，也没有排除未知的 Leray-paid packing law。 ||| The admissible radius, interpolation slopes, and passive amplitude may all decrease with \(N\). This is not a weighted-atom counterexample and does not rule out an unknown Leray-paid packing law.
bounded literature audit 没有定位到与本节完整量词相同的结果。这只是限定范围内的检索结论，不是原创性、优先权或不存在性声明。 ||| The bounded literature audit located no result with the complete quantifiers of this section. This is only a conclusion from a limited search, not a claim of originality, priority, or nonexistence.
exact audit 检查 zero-gap sampling、eigenshell jet identity、NSE scaling、2.5D 代数、response derivatives、modular support isolation 与 R0.71T full-support IFT boundary。independent audit 不读取 producer 结果，重建零点插值、cutoff refinement、非零 slopes 与 forced-path method test。 ||| The exact audit checks zero-gap sampling, the eigenshell jet identity, NSE scaling, the 2.5D algebra, response derivatives, modular support isolation, and the R0.71T full-support IFT boundary. The independent audit does not read the producer result and reconstructs zero interpolation, cutoff refinement, nonzero slopes, and the forced-path method test.
finite lattice figure 是可复现的 corroboration，不是 DNS，也不承担 continuum proof。 ||| The finite-lattice figure is reproducible corroboration, not DNS, and does not carry the continuum proof.
global atom 与 first-time jet 的 annular comparability；same-time all-shell batching；零点数无关的 Hilbert sampling；带 positive enstrophy floor 的 classical all-shell second-time-jet theorem；真实 unforced 2.5D finite recurrence；unit energy–enstrophy ball 上 raw count 无统一界。 ||| annular comparability between the global atom and first-time jet; same-time all-shell batching; zero-count-independent Hilbert sampling; the classical all-shell second-time-jet theorem with a positive enstrophy floor; genuine unforced 2.5D finite recurrence; and the absence of a uniform raw-count bound on the unit energy-enstrophy ball.
global-shell entry 的 weighted mass 可以在 compact classical interval 上统一求和，但要支付二阶时间 jet。相反，在单位 energy–enstrophy ball 内，raw entry count 与 minimum separation 都不能由初值的这两个数统一控制。后一个结论不反驳前一个：构造中的 atom 可随 entry 数增加而缩小。 ||| The weighted mass of global-shell entries can be summed uniformly on a compact classical interval, but the second-time jet must be paid. In contrast, within the unit energy-enstrophy ball, neither the raw entry count nor the minimum separation can be controlled uniformly by these two initial-data quantities. The latter conclusion does not contradict the former: the atoms in the construction may shrink as the number of entries increases.
R0.71T 的原始 IFT 变量精确覆盖 \(|k|^2=2\) 的 real-conjugate four-mode projection；它不能单凭四模 cancellation 推出一个含其他 active modes 的宽 annulus 为零。对与 seed shell 分离的 compact target support，可把 IFT 变量空间扩为该支撑上的完整有限维 real divergence-free space。此时 ||| The original IFT variables in R0.71T cover exactly the real-conjugate four-mode projection with \(|k|^2=2\); cancellation of those four modes alone cannot imply that a broad annulus containing other active modes vanishes. For compact target support separated from the seed shell, the IFT variable space can be enlarged to the complete finite-dimensional real divergence-free space on that support. Then
R0.71U · 2026-08-26 · 个人数学研究日志 ||| R0.71U · 2026-08-26 · Personal mathematical research log
R0.71U 2.5D NSE 有限 recurrence、目标零点、cutoff refinement 与 jet atom ||| R0.71U 2.5D NSE finite recurrence, target zeros, cutoff refinement, and jet atom
R0.71U｜二阶时间 jet 求和与真实有限 recurrence ||| R0.71U | Second-time-jet summation and genuine finite recurrence
R0.71V 比较 atom mass、二阶 jet 与 level-integrated excursion ||| R0.71V compares atom mass, the second-time jet, and level-integrated excursions
raw count 无统一界，但 weighted atom 可以塌缩 ||| Raw count has no uniform bound, but weighted atoms may collapse
raw recurrence 不能计数 ||| Raw recurrence cannot be counted uniformly
recurrence 量词： ||| Recurrence quantifier:
weighted jet 有 classical 求和定理，raw count 在真实 NSE 中无统一界 ||| The weighted jet has a classical summation theorem; raw count has no uniform bound for genuine NSE
02 · 85 节完整索引 ||| 02 · Complete 85-section index
并行测试 level-integrated 或 amplitude-thresholded excursion 是否能用 genuine Leray-paid variation 代替 fixed zero-level derivative charge。负面结论必须保持 atom mass；正面结论必须处理 distinguished zero level，而不只是 almost every positive level。R0.71V 仍不宣称继续性、奇性排除或全局正则性。 ||| In parallel, test whether level-integrated or amplitude-thresholded excursions can replace the fixed zero-level derivative charge with genuine Leray-paid variation. A negative conclusion must preserve atom mass; a positive conclusion must treat the distinguished zero level rather than only almost every positive level. R0.71V still makes no claim of continuation, singularity exclusion, or global regularity.
打开最新节点 R0.71U ||| Open the latest node R0.71U
负面边界同样具体：exact unforced globally smooth 2.5D NSE 解可以在每个指定 finite time set 返回同一 compact annulus，且初值保持在 unit energy–enstrophy ball 内。因此 analyticity、simplicity 与 raw counting 不能产生统一 packing law。但每个 finite set 可选择新解，atom 也可缩小；这不是 weighted-atom counterexample。 ||| The negative boundary is equally specific: an exact unforced globally smooth 2.5D NSE solution can return to the same compact annulus at every prescribed finite time set while its initial data remain in the unit energy-enstrophy ball. Thus analyticity, simplicity, and raw counting cannot produce a uniform packing law. Yet a new solution may be chosen for each finite set and the atoms may shrink; this is not a weighted-atom counterexample.
回顾截止节点：R0.71U ||| Recap endpoint: R0.71U
回顾截止时公开笔记：145 ||| Public notes at recap endpoint: 145
截至 R0.71U，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 85 个节点解释成对千禧年问题完成了某个比例。 ||| Through R0.71U, there is no new unconditional continuation criterion, no reduction of the class of all potentially singular solutions, and no proof of finite-time breakdown. The 85 nodes cannot be interpreted as completing any percentage of the Millennium Problem.
累计回顾 · R0.61–R0.71U · 2026-08-26 ||| Cumulative recap · R0.61–R0.71U · 2026-08-26
十二个阶段、85 个节点：从约化递推到 conditional incidence，再到 genuine internal entry、classical second-time-jet packing 与真实 2.5D finite recurrence。 ||| Twelve stages and 85 nodes: from reduced recurrences to conditional incidence, then genuine internal entry, classical second-time-jet packing, and genuine 2.5D finite recurrence.
收录节点：85 ||| Included nodes: 85
下一有限任务比较 recurrence family 的 atom sum 与 second-time-jet theorem 两行，检查 \(C_{tt}\) recurrence tax 是否在该族上必要，并寻找不会随 \(N\) 塌缩的 normalized mass。 ||| The next finite task compares the atom sum of the recurrence family with the two rows of the second-time-jet theorem, tests whether the \(C_{tt}\) recurrence tax is necessary on this family, and searches for a normalized mass that does not collapse with \(N\).
这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71U 的 85 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。 ||| This page follows the R0.00–R0.60 stage recap and organizes the research nodes from R0.61 through R0.71U: 85 nodes in total. It records chronologically what each segment actually proves, which proposals are ruled out by concrete counterexamples or scaling analysis, and which conditions have not yet been derived from the Navier–Stokes equations.
R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 85 个节点沿着这个缺口推进。 ||| The R0.00–R0.60 material remains in the preceding stage recap. The conclusion at R0.60 is that the full Fourier–Leray structure and higher-order calculations can be developed further, but the critical quantity for general three-dimensional solutions is still uncontrolled. The subsequent 85 nodes follow this gap.
R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71U 的 85 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、条件 incidence theorem、internal-entry no-go，再到 second-time jet 与真实有限 recurrence 的路线。 ||| Post-R0.60 research recap: a chronological account from R0.61 through R0.71U of 85 research nodes, tracing the route from reduced recurrences through projected-Lamb heat volume, positive-entry batching, the conditional incidence theorem, and the internal-entry no-go, then to the second-time jet and genuine finite recurrence.
R0.61–R0.71U 的 85 节公开笔记 ||| R0.61–R0.71U: 85 public notes
R0.61–R0.71U 回顾 · 2026-08-26 ||| R0.61–R0.71U recap · 2026-08-26
R0.61–R0.71U 研究节点 ||| R0.61–R0.71U research nodes
R0.61–R0.71U｜R0.60 之后的研究回顾 ||| R0.61–R0.71U | Research recap after R0.60
R0.70A–R0.71U 完成版本 ||| R0.70A–R0.71U completed releases
R0.71G–R0.71U · temporal packing、internal entry 与 finite recurrence ||| R0.71G–R0.71U · temporal packing, internal entry, and finite recurrence
R0.71O–P 恢复 soft quotient 的一侧 traces，并用同刻 spatial batching 吸收有限 frame multiplicity；R0.71Q–R 给出 finite conditional Jensen 与 incidence theorems。R0.71S 保留 entry direction 后证明 critical packet 单包即带 \(\kappa_j^2\) Bessel 税。R0.71T 用正向局部 NSE 流和 finite-dimensional IFT 构造 genuine positive-time internal entry，再以双尺度族排除 bare normalized Leray-Lamb time payment；outgoing coarea 只留下 scale-matched representation。R0.71U 对 global-shell entries 证明零点数与 separation 无关的 Hilbert sampling inequality，以及带 \(\inf_KY>0\) 假设的 classical all-shell second-time-jet theorem。第一行由 normalized Leray–Lamb ledger 支付，第二行保留 \(\omega_t\) 与 \(L_t\) 的 recurrence tax，因此不是 Leray-level closure。另一个 exact unforced 2.5D NSE family 可在任意指定 finite time set 返回同一 compact annulus；unit energy–enstrophy ball 上 raw entry count 无统一界，但 atom mass 可以随 \(N\) 缩小。 ||| R0.71O–P recover one-sided traces for the soft quotient and absorb finite frame multiplicity through same-time spatial batching; R0.71Q–R establish finite conditional Jensen and incidence theorems. After retaining entry direction, R0.71S proves that even a single critical packet incurs a \(\kappa_j^2\) Bessel tax. R0.71T uses the forward local NSE flow and a finite-dimensional IFT to construct a genuine positive-time internal entry, then rules out bare normalized Leray-Lamb time payment through a double-scale family; outgoing coarea leaves only a scale-matched representation. For global-shell entries, R0.71U proves a Hilbert sampling inequality independent of zero count and separation, together with a classical all-shell second-time-jet theorem under \(\inf_KY>0\). The first row is paid by the normalized Leray-Lamb ledger, while the second retains the recurrence tax in \(\omega_t\) and \(L_t\), so it is not a Leray-level closure. Another exact unforced 2.5D NSE family can return to the same compact annulus at any prescribed finite time set; raw entry count has no uniform bound on the unit energy-enstrophy ball, but atom mass may shrink with \(N\).
R0.71U 的 zero-count-independent Hilbert sampling、classical all-shell second-time-jet theorem、Leray-level first row 与 stronger recurrence row；exact unforced 2.5D prescribed finite recurrence；unit energy–enstrophy ball 上 raw count 无统一界；以及 shrinking-atom 与 R0.71T target-support 边界。 ||| R0.71U's zero-count-independent Hilbert sampling, classical all-shell second-time-jet theorem, Leray-level first row, and stronger recurrence row; exact unforced 2.5D prescribed finite recurrence; the absence of a uniform raw-count bound on the unit energy-enstrophy ball; and the shrinking-atom and R0.71T target-support boundaries.
R0.71U 的正面结果是 zero-count-independent second-time-jet estimate。它对满足 \(\inf_KY>0\) 的 compact classical trajectory 成立，常数不依赖零点数、minimum separation 或 finite shell truncation。第一行有 normalized Leray–Lamb payment；第二行要求 \(\omega_t\) 与 \(L_t\)，ordinary Leray inequality 尚未关闭。 ||| The positive result in R0.71U is the zero-count-independent second-time-jet estimate. It holds for a compact classical trajectory satisfying \(\inf_KY>0\), with a constant independent of the number of zeros, minimum separation, or finite shell truncation. The first row has a normalized Leray-Lamb payment; the second requires \(\omega_t\) and \(L_t\) and remains beyond the ordinary Leray inequality.
R0.71U 附图 ||| R0.71U figure
R0.71U 证书 ||| R0.71U certificates
R0.71V 量化 weighted recurrence，并测试 Leray-paid excursion ||| R0.71V quantifies weighted recurrence and tests Leray-paid excursions
raw count 已被真实 recurrence 排除，weighted mass 保留一条 classical 定理 ||| Genuine recurrence rules out raw count; weighted mass retains a classical theorem
本节没有删除 second-time-jet recurrence tax，没有得到 weak-solution jet trace、single-trajectory infinite recurrence、continuation、finite-time singularity 或 global regularity。 ||| This section does not remove the second-time-jet recurrence tax and does not establish a weak-solution jet trace, single-trajectory infinite recurrence, continuation, a finite-time singularity, or global regularity.
比较 recurrence family 的 weighted atom sum 与 second-time-jet 两行；检查 level-integrated 或 amplitude-thresholded excursion 能否避免 \(C_{tt}\) tax。 ||| Compare the weighted atom sum of the recurrence family with the two second-time-jet rows; test whether level-integrated or amplitude-thresholded excursions can avoid the \(C_{tt}\) tax.
从有符号环带障碍走到 second-time jet 与真实 finite recurrence ||| From the signed-annulus obstruction to the second-time jet and genuine finite recurrence
第一行由 normalized Leray–Lamb ledger 支付。第二行保留 \(\nu^2\|\omega_t\|_2^2+\|L_t\|_{\dot H^{-1}}^2\)，只在 classical level 有限，不由 ordinary Leray energy inequality 控制。exact torus covariance 只对 integer dilation 与协变运输的 frame/window 使用。 ||| The first row is paid by the normalized Leray-Lamb ledger. The second retains \(\nu^2\|\omega_t\|_2^2+\|L_t\|_{\dot H^{-1}}^2\), is finite only at the classical level, and is not controlled by the ordinary Leray energy inequality. Exact torus covariance is used only for integer dilations and covariantly transported frames/windows.
对 \(U=(0,\cos x_1,\cos x_2)\) 的 \(|k|^2=2\) exact four-mode real-conjugate projection，标准局部 NSE 流映射与有限维 IFT 给出初值预补偿 \[ z(a)=-a^2\tau F_*+O(a^3). \] 该精确 thin projection 在预定正时间 \(t=\tau\) 归零。若 compact target support 与 seed shell 分离，变量空间必须扩到全部 target-support modes，有限热半群矩阵才给 full-support cancellation。事件 forcing 仍为 \(a^2e^{-2\nu\tau}F_*+O(a^3)\ne0\)，所以该零点严格位于 observation window 内部、为 simple positive crossing，并满足 \[ \kappa^{-2}A_+(a)=\frac{a^2e^{-2\nu\tau}}4+O(a^3). \] ||| For the exact four-mode real-conjugate projection of \(U=(0,\cos x_1,\cos x_2)\) with \(|k|^2=2\), the standard local NSE flow map and a finite-dimensional IFT give the initial-data precompensation \[ z(a)=-a^2\tau F_*+O(a^3). \] This exact thin projection vanishes at the prescribed positive time \(t=\tau\). If the compact target support is separated from the seed shell, the variable space must be enlarged to all target-support modes before the finite heat-semigroup matrix yields full-support cancellation. The event forcing remains \(a^2e^{-2\nu\tau}F_*+O(a^3)\ne0\), so this zero lies strictly inside the observation window, is a simple positive crossing, and satisfies \[ \kappa^{-2}A_+(a)=\frac{a^2e^{-2\nu\tau}}4+O(a^3). \]
对满足 \(\inf_KY>0\) 的 compact classical trajectory，Hilbert-valued zero sampling 给出 all-shell estimate \[ \mu_J(K)\lesssim \mathcal R_Y(K)\left[ |K|^{-1}\!\int_K\!Y^{-1}\sum_j\kappa_j^{-6}\|C_{j,t}\|_2^2 +|K|\!\int_K\!Y^{-1}\sum_j\kappa_j^{-6}\|C_{j,tt}\|_2^2\right]. \] 常数不依赖 zero count、minimum separation 或 finite shell truncation。closed-interval endpoints 可用 classical trace 纳入。 ||| For a compact classical trajectory satisfying \(\inf_KY>0\), Hilbert-valued zero sampling gives the all-shell estimate \[ \mu_J(K)\lesssim \mathcal R_Y(K)\left[ |K|^{-1}\!\int_K\!Y^{-1}\sum_j\kappa_j^{-6}\|C_{j,t}\|_2^2 +|K|\!\int_K\!Y^{-1}\sum_j\kappa_j^{-6}\|C_{j,tt}\|_2^2\right]. \] The constant is independent of zero count, minimum separation, or finite shell truncation. Closed-interval endpoints are included through classical traces.
二阶时间 jet 可以求和，raw recurrence 不能计数 ||| The second-time jet is summable; raw recurrence cannot be counted uniformly
环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence ||| annular exclusion → source-core ledger → covariance spectral stratification → full-frequency conditional bridge → response-slope chord gain → common first-order response channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative-refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel sets → projective heat curvature → soft-denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment-projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence
静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–P 建立 projected-Lamb 热体积、局部化、denominator faces 与同刻 spatial batching。R0.71Q–T 给出 conditional Jensen/incidence、packet/Bessel scale audits 与 genuine internal-entry no-go。R0.71U 再证明 zero-count-independent classical second-time-jet packing；第一行 Leray-paid，第二行保留 recurrence tax。exact unforced 2.5D NSE family 同时排除 unit energy–enstrophy ball 上的统一 raw count，但 atom mass 可以塌缩。 ||| After the static annular family is rigorously excluded, the main route turns to covariance-rank stratification and the full-frequency projection bridge. R0.71A–P establish projected-Lamb heat volume, localization, denominator faces, and same-time spatial batching. R0.71Q–T give conditional Jensen/incidence results, packet/Bessel scale audits, and the genuine internal-entry no-go. R0.71U then proves zero-count-independent classical second-time-jet packing; the first row is Leray-paid, while the second retains the recurrence tax. An exact unforced 2.5D NSE family also rules out a uniform raw count on the unit energy-enstrophy ball, but atom mass may collapse.
累计回顾 R0.61–R0.71U · 2026-08-26 ||| Cumulative recap R0.61–R0.71U · 2026-08-26
量化 exact 2.5D recurrence family 的 weighted atom mass 与 classical second-time-jet recurrence tax；并检查 level-integrated excursion 能否由 Leray variation 支付。 ||| Quantify the weighted atom mass of the exact 2.5D recurrence family and the classical second-time-jet recurrence tax; then test whether level-integrated excursions can be paid by Leray variation.
量化 recurrence family 的 weighted atom mass 与 second-time-jet 两行，并测试 level-integrated / amplitude-thresholded excursion。 ||| Quantify the weighted atom mass of the recurrence family against the two second-time-jet rows, and test level-integrated / amplitude-thresholded excursions.
目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71U 给出带 positive enstrophy floor 的 trajectory-wise classical second-time-jet theorem；第一行 Leray-paid，第二行非 Leray。exact 2.5D family 排除 unit energy–enstrophy ball 上 raw count 的统一界，但 atom 可缩小，weighted packing 仍开放。 ||| There is currently no new unconditional continuation criterion and no construction of a finite-time singularity. R0.71U gives a trajectory-wise classical second-time-jet theorem with a positive enstrophy floor; the first row is Leray-paid and the second is not Leray-level. The exact 2.5D family rules out a uniform raw-count bound on the unit energy-enstrophy ball, but the atoms may shrink, so weighted packing remains open.
上次综述 v1.05 · 2026-08-26 ||| Previous review v1.05 · 2026-08-26
我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71U 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。 ||| I also prepared a systematic review that places classical theory, five main literature strands, the candidate-blowup exclusion tree, progress from 2019—2026, and this site's R0.69P–R0.71U route in one view. The historical R0.61–R0.69O nodes remain in the cumulative recap.
下一步 R0.71V： ||| Next step R0.71V:
研究笔记 R0.71U · 2026-08-26 ||| Research note R0.71U · 2026-08-26
阅读 R0.71U 研究笔记 → ||| Read research note R0.71U →
展开 55 篇公开笔记 ||| Expand 55 public notes
综述 v1.06 · 2026-08-26 ||| Review v1.06 · 2026-08-26
classical second-time-jet theorem 保留 recurrence tax；exact 2.5D finite recurrence 排除统一 raw count，但不排除 weighted packing。 ||| The classical second-time-jet theorem retains the recurrence tax; exact 2.5D finite recurrence rules out a uniform raw count but does not rule out weighted packing.
exact unforced globally smooth 2.5D NSE family 可在任意指定 finite time set 返回同一 compact annulus。每个 finite set 与每个 \(N\) 选择一条新轨迹；unit energy–enstrophy ball 上 raw global-shell entry count 没有统一上界。entry atom 可以随 \(N\) 缩小，所以这不是 weighted-atom counterexample。 ||| An exact unforced globally smooth 2.5D NSE family can return to the same compact annulus at any prescribed finite time set. A new trajectory is selected for each finite set and each \(N\); the raw global-shell entry count has no uniform bound on the unit energy-enstrophy ball. The entry atoms may shrink with \(N\), so this is not a weighted-atom counterexample.
R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen/incidence、packet/Bessel、internal-entry scaling、second-time jet 与 finite recurrence。R0.70A–R0.71U 共 47 个完成版本。 ||| The post-R0.60 route has twelve segments: reduced Picard analysis and the shear boundary; transverse perturbations; local pressure budgets; signed physical annuli; moving labels and source-core duality; defect tensors and finite observations; full-frame covariance; the constant-projection boundary; positive output and the material-heat tent; projected-Lamb heat volume; local heat packing and the critical-trace obstruction; and positive-entry temporal packing, conditional Jensen/incidence, packet/Bessel analysis, internal-entry scaling, the second-time jet, and finite recurrence. R0.70A–R0.71U contains 47 completed releases.
R0.60 recap 之后的累计回顾收录 85 个节点；全站现有 145 篇公开研究笔记 ||| The cumulative recap after the R0.60 recap contains 85 nodes; the full site now has 145 public research notes
R0.71U 已完成： ||| R0.71U completed:
`;

const rows = translationRows
  .trim()
  .split("\n")
  .filter(Boolean);
const additions = new Map(
  rows.map((row) => {
    const separator = " ||| ";
    const offset = row.indexOf(separator);
    if (offset < 1) throw new Error("invalid translation row: " + row);
    return [row.slice(0, offset), row.slice(offset + separator.length)];
  }),
);
if (additions.size !== rows.length) {
  throw new Error("duplicate Chinese keys in R0.71U translation rows");
}

function numericTokens(value) {
  return [...String(value).matchAll(/\d+(?:[.\-–—]\d+)*/g)].map(
    (match) => match[0],
  );
}

function same(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

for (const relative of [
  "research-review.html",
  "literature-review.html",
  "recap-r0-61-r0-71u.html",
  "notes/r0-71u.html",
]) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.06')) {
    throw new Error(relative + ": expected i18n cache version v1.06");
  }
}

const correctedPrevious = await readFile(
  resolve(publicDirectory, "notes/r0-71t.html"),
  "utf8",
);
if (!correctedPrevious.includes('/i18n-en.js?v=1.05')) {
  throw new Error("notes/r0-71t.html: expected historical i18n cache version v1.05");
}

const currentWithoutBatch = current.filter((entry) => !/^r071u\d+$/.test(entry.id));
const currentByChinese = new Map(
  currentWithoutBatch.map((entry) => [entry.zh, entry]),
);
if (currentByChinese.size !== currentWithoutBatch.length) {
  throw new Error("duplicate Chinese keys outside the R0.71U batch");
}

const sourceByChinese = new Map(source.map((entry) => [entry.zh, entry]));
if (sourceByChinese.size !== source.length) {
  throw new Error("duplicate Chinese keys in collected site strings");
}
const missing = source.filter((entry) => !currentByChinese.has(entry.zh));
const missingKeys = new Set(missing.map((entry) => entry.zh));
const uncovered = missing.filter((entry) => !additions.has(entry.zh));
const stale = [...additions.keys()].filter((zh) => !missingKeys.has(zh));
if (uncovered.length || stale.length || additions.size !== missing.length) {
  throw new Error(
    `translation batch does not equal active missing set (${missing.length}):\n` +
      "uncovered:\n" +
      uncovered.map((entry) => entry.zh).join("\n---\n") +
      "\nstale:\n" +
      stale.join("\n---\n"),
  );
}

const translated = missing.map((entry, index) => {
  const en = additions.get(entry.zh);
  if (!same(extractProtectedTokens(entry.zh), extractProtectedTokens(en))) {
    throw new Error("protected-token mismatch: " + entry.zh);
  }
  if (!same(numericTokens(entry.zh), numericTokens(en))) {
    throw new Error(
      "numeric-token mismatch: " +
        entry.zh +
        "\nZH " +
        JSON.stringify(numericTokens(entry.zh)) +
        "\nEN " +
        JSON.stringify(numericTokens(en)),
    );
  }
  if (!en.trim() || containsChinese(en)) {
    throw new Error("blank or Chinese-containing translation: " + entry.zh);
  }
  if (/\b(?:we|our|ours|us)\b/i.test(en)) {
    throw new Error("first-person plural voice: " + entry.zh);
  }
  return {
    ...entry,
    id: "r071u" + String(index + 1).padStart(3, "0"),
    en,
  };
});

const merged = [...currentWithoutBatch, ...translated];
if (new Set(merged.map((entry) => entry.zh)).size !== merged.length) {
  throw new Error("translation merge produced duplicate Chinese keys");
}
if (new Set(merged.map((entry) => entry.id)).size !== merged.length) {
  throw new Error("translation merge produced duplicate IDs");
}
await writeFile(translationPath, JSON.stringify(merged, null, 2) + "\n");
console.log(
  JSON.stringify(
    {
      source: source.length,
      existingWithoutBatch: currentWithoutBatch.length,
      activeMissingBefore: missing.length,
      added: translated.length,
      firstId: translated.at(0)?.id,
      lastId: translated.at(-1)?.id,
      total: merged.length,
      protectedTokenMismatches: 0,
      numericTokenMismatches: 0,
      englishWithChinese: 0,
      firstPersonPlural: 0,
    },
    null,
    2,
  ),
);
