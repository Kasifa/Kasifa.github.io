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
打开 79 节完整索引 ||| Open the complete 79-section index
给出 variation-measure 稳定性和 BV chain-rule 基础； ||| provide the foundations for variation-measure stability and the BV chain rule;
给出周期强解经典区间内的时间解析性背景； ||| provide the time-analyticity background on the classical interval of a periodic strong solution;
及 ||| and
精确 factorization 把 soft source 分成 hard interior source 与 face layer。有限阶零点的 signed atom 可以消失，正负 Jordan masses 仍支付左右 traces；raw logarithms 只有联合后才有限。ordinary-budget 抽象族不等于 NSE 多-face 构造。 ||| The exact factorization splits the soft source into a hard interior source and a face layer. At a finite-order zero, the signed atom may vanish while the positive and negative Jordan masses still pay the left and right traces; the raw logarithms are finite only after they are combined. The abstract ordinary-budget family is not an NSE multiple-face construction.
开放接口 · R0.71P ||| Open interface · R0.71P
累计回顾与 79 节索引 ||| Cumulative recap and 79-section index
连接 BV、coarea 与 crossing counts。它们不从 Leray energy 生成本站 fixed-cell quotient 的零层 face sum。限定检索未找到同时识别一侧 Jordan atoms、又支付完整 NSE frame–cell sum 的直接定理；这是 bounded negative finding，不是原创性、优先权或不存在性结论。 ||| connect BV, coarea, and crossing counts. They do not derive the zero-level face sum for this site's fixed-cell quotient from Leray energy. The bounded search found no direct theorem that both identifies the one-sided Jordan atoms and pays the complete NSE frame–cell sum; this is a bounded negative finding, not a claim of originality, priority, or nonexistence.
完整 fixed-cell 标量只留下临界 signed second jet。 ||| The complete fixed-cell scalar retains only the critical signed second jet.
文献综述 v1.00 · 2026-08-26 ||| Literature review v1.00 · 2026-08-26
我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.71O 只列为研究笔记。我不把计算或笔记外推成正则性定理。 ||| I list published theorems as known results, mark 2026 preprints separately, and classify this site's R0.69P–R0.71O work only as research notes. I do not extrapolate calculations or notes into regularity theorems.
下一节固定 multiplier、cutoff 与 partition，检查 \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\)；total-Jordan sum 是更强的后续变体，暂不进入 refresh 或 moving cutoffs。 ||| The next section fixes the multiplier, cutoff, and partition and tests \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\); the total-Jordan sum is a stronger later variant, while refresh and moving cutoffs remain outside the scope.
中。R0.69P–R0.71O 从有符号物理环带经过 projected-Lamb 热体积、matched-cell heat gap、viscous fusion、increment bridge 与 signed second jet，走到 soft-denominator face boundary。R0.71O 证明 soft quotient 恢复 hard 一侧迹，signed atoms 可以相消而 Jordan face costs 保留。保留下来的结果都不是全局正则性结论。 ||| . From R0.69P through R0.71O, the route moves from signed physical annuli through projected-Lamb heat volume, the matched-cell heat gap, viscous fusion, the increment bridge, and the signed second jet to the soft-denominator face boundary. R0.71O proves that the soft quotient recovers the one-sided hard traces: signed atoms may cancel while the Jordan face costs remain. None of the retained results is a global-regularity conclusion.
R0.71O 的一手文献边界 ||| Primary-source boundary for R0.71O
R0.71O 关闭了什么，R0.71P 只检查什么 ||| What R0.71O closes, and what R0.71P alone will test
R0.71O 没有把 soft denominator 当作删除 \(d_Q=0\) faces 的规则。soft equation 精确恢复一侧 hard traces；signed atoms 可以抵消，但 Jordan variation 仍支付 entry 与 exit。抽象 smooth paths 只排除 ordinary budgets 的普适 face-count 控制，不是 NSE 多-face 反例。R0.71P 只检查 fixed-partition weighted positive-entry sum；total-Jordan sum 是更强的后续变体。我继续用下面六条筛选。 ||| R0.71O does not treat the soft denominator as a rule for deleting the faces at \(d_Q=0\). The soft equation recovers the one-sided hard traces exactly; signed atoms may cancel, but Jordan variation still pays the entry and exit. The abstract smooth paths rule out only universal face-count control by ordinary budgets; they are not NSE multiple-face counterexamples. R0.71P tests only the fixed-partition weighted positive-entry sum, while the total-Jordan sum is a stronger later variant. I continue to use the six filters below.
soft quotient 恢复一侧 traces 与 Jordan face atoms ||| The soft quotient recovers one-sided traces and Jordan face atoms
\(m\) 偶 ||| \(m\) even
\(m\) 奇 ||| \(m\) odd
01 · 两种 soft source ||| 01 · Two soft sources
02 · hard–soft 分解 ||| 02 · Hard–soft decomposition
03 · 有限阶零点 ||| 03 · Finite-order zeros
05 · raw 对数抵消 ||| 05 · Raw logarithmic cancellation
06 · ordinary-budget 分离 ||| 06 · Ordinary-budget separation
07 · NSE 初始 entry ||| 07 · NSE initial entry
08 · 经典区间解析性 ||| 08 · Analyticity on the classical interval
09 · 独立审计 ||| 09 · Independent audit
版本 v0.71O · 2026-08-26 ||| Version v0.71O · 2026-08-26
报告、证书、独立审计、累计回顾与附图源 ||| Report, certificates, independent audit, cumulative recap, and figure source
本节关闭 hard/soft face algebra，不关闭全局 face summability ||| This section closes the hard/soft face algebra, not global face summability
本节完成四个有限检查：先区分 R0.71N 与 R0.71I 的 soft source；再证明 exact hard–soft factorization；随后计算孤立有限阶零点的 signed/Jordan atoms；最后比较 face cost 与已有 ordinary budgets。 ||| This section completes four finite checks: it first distinguishes the soft sources in R0.71N and R0.71I, then proves the exact hard–soft factorization, next computes the signed and Jordan atoms at isolated finite-order zeros, and finally compares the face cost with the available ordinary budgets.
变差 ||| Variation
但 ||| but
但没有消除一侧 face cost ||| but does not remove the one-sided face cost
独立检查器不导入 exact producer。对 \(m=1,\ldots,8\)，finite-order derivative profile 的质量误差最大为 \(2.22\times10^{-16}\)。raw source/radial 数值积分分别显示对数增长，联合质量最大相对误差为 \(3.33\times10^{-16}\)。 ||| The independent checker does not import the exact producer. For \(m=1,\ldots,8\), the largest mass error of the finite-order derivative profile is \(2.22\times10^{-16}\). Separate numerical integrations of the raw source and radial terms show logarithmic growth, while the largest relative error of their joint mass is \(3.33\times10^{-16}\).
独立数值审计 ||| Independent numerical audit
对 \(N=1,2,4,\ldots,64\)，oscillatory variation 与 extra radial formula 的最大相对误差分别为 \(1.18\times10^{-16}\) 与 \(6.94\times10^{-17}\)。\(32^3\) NumPy FFT 重建四个目标模；全部记录的代数 residual 在该 binary64 运行中为 \(0.0\)。没有时间推进。 ||| For \(N=1,2,4,\ldots,64\), the largest relative errors in the oscillatory variation and extra radial formula are \(1.18\times10^{-16}\) and \(6.94\times10^{-17}\), respectively. A \(32^3\) NumPy FFT reconstructs the four target modes; in this binary64 run, every recorded algebraic residual is \(0.0\). No time stepping is used.
对数抵消 ||| Logarithmic cancellation
额外 damping 在标量等式左侧带正号。混用这两个定义会把同一项放错位置。 ||| The extra damping has a positive sign on the left side of the scalar equation. Mixing the two definitions places the same term on the wrong side.
给出 BV chain-rule 背景。固定 \(\varepsilon\) 的 smooth chain rule 不会自动给出 \(\varepsilon\downarrow0\) 的 uniform face bound。 ||| provide the BV chain-rule background. The smooth chain rule at fixed \(\varepsilon\) does not automatically give a uniform face bound as \(\varepsilon\downarrow0\).
给出 total-variation measure 的稳定性框架； ||| provide the stability framework for total-variation measures;
给出局部正则区间内的时间解析性。对固定线性 observable \(C_Q(t)\)，在紧子区间上要么恒为零，要么内部零点孤立且有限阶。 ||| give time analyticity on a local regularity interval. On a compact subinterval, a fixed linear observable \(C_Q(t)\) is either identically zero or has isolated finite-order interior zeros.
记 \(\lambda_j=\nu\kappa_j^2\) 与 \(\theta_{Q,\varepsilon}=\varepsilon/(d_Q+\varepsilon)\)。两种 source 是 ||| Set \(\lambda_j=\nu\kappa_j^2\) and \(\theta_{Q,\varepsilon}=\varepsilon/(d_Q+\varepsilon)\). The two sources are
价值是把 interior identity 与 boundary cost 分开 ||| The value is separating the interior identity from the boundary cost
截至 2026-08-26 的限定一手检索没有找到针对 \((B_Q^+)^2/[Y(d_Q+\varepsilon)]\) 同时识别一侧 atoms、又从 energy 与 denominator mass 支付完整 NSE frame–cell sum 的定理。这是 bounded negative finding，不是原创性、优先权或不存在性结论。 ||| The bounded primary-source search as of 2026-08-26 found no theorem for \((B_Q^+)^2/[Y(d_Q+\varepsilon)]\) that both identifies the one-sided atoms and pays the complete NSE frame–cell sum from energy and denominator mass. This is a bounded negative finding, not a claim of originality, priority, or nonexistence.
解析性 ||| Analyticity
解析性把单个经典 observable 的非平凡零点限制为孤立有限阶 ||| Analyticity restricts the nontrivial zeros of one classical observable to isolated finite order
精确 hard–soft factorization、有限阶零点原子、raw logarithmic cancellation、抽象预算分离和一个真实 NSE 初始 entry face。 ||| Exact hard–soft factorization, finite-order zero atoms, raw logarithmic cancellation, an abstract budget separation, and one genuine NSE initial entry face.
两个 raw 项分别发散，只有联合后留下有限 face mass ||| The two raw terms diverge separately; only their joint form leaves a finite face mass
零点阶数 ||| Zero order
另加一致有界余项。各自总变差对 \(\varepsilon\downarrow0\) 发散；联合后对数精确抵消，并恢复 \((\sigma_\varepsilon)_ta_Q\) 的有限原子。把 source 与 radial row 分开取绝对值会丢掉这个结构。 ||| plus uniformly bounded remainders. Their separate total variations diverge as \(\varepsilon\downarrow0\); after they are combined, the logarithms cancel exactly and recover the finite atom of \((\sigma_\varepsilon)_ta_Q\). Taking absolute values of the source and radial rows separately loses this structure.
能把已经受控的 BV 量转成 level/crossing 信息；它们不从 Leray energy 生成零层 crossing 预算。Temam 的解析性结论也不统一控制零点数。 ||| can convert an already controlled BV quantity into level and crossing information; they do not derive a zero-level crossing budget from Leray energy. Temam's analyticity result also gives no uniform control of the zero count.
偶阶且 \(\gamma>0\) 时，左右 hard 值相同，signed atom 为零；soft profile 仍必须降到零再升回去，所以绝对变差支付两次迹。 ||| When the order is even and \(\gamma>0\), the left and right hard values are equal and the signed atom is zero; the soft profile must still fall to zero and rise again, so its absolute variation pays the trace twice.
平滑抽象路径把 face count 与已有普通预算分开 ||| A smooth abstract path separates face count from the available ordinary budgets
取单位向量 \(e\)，在 \([0,2\pi]\) 上令 ||| Take a unit vector \(e\) and, on \([0,2\pi]\), set
若 \(\mathcal J_Q=z_{Q,t}+\lambda_jz_Q\)，则 ||| If \(\mathcal J_Q=z_{Q,t}+\lambda_jz_Q\), then
若 leading pairing 为零，则两侧迹都为零，本节的 leading face atom 也为零。 ||| If the leading pairing is zero, both one-sided traces vanish, as does the leading face atom in this section.
设 \(\tau=t-t_0\)。我要求 \(t_0\) 是孤立的经典有限阶零点，Taylor 余项可微，并假设 ||| Set \(\tau=t-t_0\). I require \(t_0\) to be an isolated classical finite-order zero with a differentiable Taylor remainder, and assume
同时，\(F_j\) 与 \(Y\) 在 \(t_0\) 附近具有有界一阶导数，且 ||| In addition, \(F_j\) and \(Y\) have bounded first derivatives near \(t_0\), and
图 R0.71O。有限阶 soft layer 恢复一侧 hard traces；signed atoms 可以抵消，Jordan masses 仍支付左右 faces。抽象 oscillatory path 显示 ordinary budgets 不控制 face count；最后一栏记录真实 NSE 初始 entry trace \(1/4\)。 ||| Figure R0.71O. The finite-order soft layer recovers the one-sided hard traces; signed atoms may cancel, while the Jordan masses still pay the left and right faces. The abstract oscillatory path shows that ordinary budgets do not control face count; the final panel records a genuine NSE initial entry trace of \(1/4\).
未证明：内部 NSE faces 可以任意多，或完整 weighted face sum 发散。 ||| Not proved: that there can be arbitrarily many internal NSE faces or that the complete weighted face sum diverges.
未证明：refresh、moving cells、弱解极限、继续性、全局正则性或有限时破裂。 ||| Not proved: refresh, moving cells, a weak-solution limit, continuation, global regularity, or finite-time breakdown.
文献审计 ||| Literature audit
我检查它能否在完整 frame–cell 求和后由已有 energy、denominator mass 或一个精确 NSE cancellation 支付。R0.71P 暂不引入 partition refresh、moving cutoffs 或更强的 total-Jordan sum。 ||| I test whether the complete frame–cell sum can be paid by the available energy, denominator mass, or an exact NSE cancellation. R0.71P does not yet introduce partition refresh, moving cutoffs, or the stronger total-Jordan sum.
我仍使用固定 multiplier、固定 cutoff 与固定 cell。对每个 \(\varepsilon>0\)，soft quotient 全局光滑；在 \(d_Q>0\) 上，它又精确等于 hard quotient 乘一个径向因子。孤立有限阶零点的极限因此可以逐项算清：signed atom 可能相消，正负 Jordan atoms 与绝对变差仍保留。现有 denominator mass 和 ordinary first-time budgets 没有给出这些 faces 的统一和。 ||| I continue to use a fixed multiplier, cutoff, and cell. For every \(\varepsilon>0\), the soft quotient is globally smooth; on \(d_Q>0\), it is exactly the hard quotient times a radial factor. The limit at an isolated finite-order zero can therefore be computed term by term: the signed atom may cancel, while the positive and negative Jordan atoms and the absolute variation remain. The available denominator mass and ordinary first-time budgets do not give a uniform sum of these faces.
下一对象：fixed-partition all-shell/all-cell positive-entry sum ||| Next object: the fixed-partition all-shell/all-cell positive-entry sum
下一节保持 multiplier、cutoff 与 partition 固定，先检查右侧正向进入 atoms 的主门槛 ||| The next section keeps the multiplier, cutoff, and partition fixed and first tests the main threshold formed by right-side positive-entry atoms
选实、偶、径向 multiplier，使其在半径 \(1\) 为零、在半径 \(\sqrt2\) 为一，并取 \(\chi_Q=1\)。初始 filtered vorticity 为零；quadratic Lamb field 在 \((\pm1,\pm1,0)\) 有四个目标模。 ||| Choose a real, even, radial multiplier that vanishes at radius \(1\) and equals one at radius \(\sqrt2\), and take \(\chi_Q=1\). The initial filtered vorticity is zero; the quadratic Lamb field has four target modes at \((\pm1,\pm1,0)\).
研究笔记 R0.71O · SOFT DENOMINATOR · ONE-SIDED TRACES · FACE MEASURES ||| Research note R0.71O · SOFT DENOMINATOR · ONE-SIDED TRACES · FACE MEASURES
研究笔记 R0.71O：soft denominator 在孤立有限阶零点恢复 hard quotient 的一侧迹，并产生显式 signed/Jordan face atoms；现有 ordinary budgets 不支付统一 face sum。 ||| Research note R0.71O: at an isolated finite-order zero, the soft denominator recovers the one-sided traces of the hard quotient and produces explicit signed and Jordan face atoms; the available ordinary budgets do not pay a uniform face sum.
一侧 hard traces 由零点阶数与一个标量 \(\gamma\) 完全决定 ||| The one-sided hard traces are determined completely by the zero order and one scalar \(\gamma\)
已构造：一个右 entry trace 为 \(1/4\) 的真实 smooth NSE initial jet。 ||| Constructed: a genuine smooth NSE initial jet with right entry trace \(1/4\).
已证明：\(z_\varepsilon=\sqrt\sigma z\)、\(a_\varepsilon=\sigma a\) 与 exact face-source identity。 ||| Established: \(z_\varepsilon=\sqrt\sigma z\), \(a_\varepsilon=\sigma a\), and the exact face-source identity.
已证明：抽象 smooth paths 的 ordinary budgets 不统一控制 face cost。 ||| Established: the ordinary budgets of abstract smooth paths do not uniformly control face cost.
已证明：孤立有限阶零点的一侧 hard traces、signed atom、Jordan atoms 及奇偶阶区别。 ||| Established: the one-sided hard traces, signed atom, Jordan atoms, and odd/even distinction at an isolated finite-order zero.
已证明：N-style 与 I-style soft source 的精确关系。 ||| Established: the exact relation between the N-style and I-style soft sources.
已证明：raw source 与 radial term 各自有对数发散质量，联合后恢复有限 face measure。 ||| Established: the raw source and radial term each have logarithmically divergent mass, while their joint form recovers a finite face measure.
因此 signed atom 可以消失，Jordan variation 却仍记录左右两侧的 face cost。 ||| The signed atom may therefore vanish, while Jordan variation still records the face cost on both sides.
因此下一步不应再寻找单个 fixed-cell 的另一种坐标重写。我需要直接检查固定 partition 上的全壳、全小区 weighted positive-entry sum 是否存在 NSE-specific cancellation 或新的可支付结构。完整 total-Jordan sum 是更强的后续变体。 ||| The next step should therefore not seek another coordinate rewrite of one fixed cell. I need to test directly whether the all-shell/all-cell weighted positive-entry sum on a fixed partition has an NSE-specific cancellation or a new payable structure. The complete total-Jordan sum is a stronger later variant.
有限阶零点 ||| Finite-order zeros
预算分离 ||| Budget separation
在 active half-face 上，两项的积分分别含 ||| On an active half-face, the two integrals contain, respectively,
在归一化环面取 ||| On the normalized torus, take
在任一 \(d_Q>0\) 分支上，令 ||| On any branch with \(d_Q>0\), set
则 \(d_Q=\|c\|_2^2\tau^{2m}+O(|\tau|^{2m+1})\)、\(B_Q=\langle F_j(t_0),c\rangle\tau^m+O(|\tau|^{m+1})\)，并且 ||| Then \(d_Q=\|c\|_2^2\tau^{2m}+O(|\tau|^{2m+1})\), \(B_Q=\langle F_j(t_0),c\rangle\tau^m+O(|\tau|^{m+1})\), and
这个结构把单个经典零点放入前面的 theorem，但不控制零点数量、阶数、间距或 transversality，也不提供跨解、跨壳、跨小区以及逼近潜在奇性端点时的统一计数。 ||| This structure places one classical zero under the preceding theorem, but it controls neither the number, order, spacing, nor transversality of the zeros. It also gives no uniform count across solutions, shells, cells, or intervals approaching a possible singular endpoint.
这是一个真正的一侧 NSE 初始 entry face。它不是内部 crossing，也没有构造任意多 NSE faces。 ||| This is a genuine one-sided NSE initial entry face. It is not an internal crossing and does not construct arbitrarily many NSE faces.
这些 ordinary budgets 有界，face cost 却按 \(N\) 增长。这个族是 smooth Hilbert path，不是耦合 NSE 的多-face 构造；它只排除从这些普通范数单独推出 face bound 的普适函数不等式。 ||| These ordinary budgets remain bounded, while the face cost grows like \(N\). This family is a smooth Hilbert path, not a multiple-face construction for the coupled NSE observables; it rules out only a universal functional inequality deriving a face bound from these ordinary norms alone.
真实光滑 NSE 初值可以从 \(d_Q=0\) 出发并有正 entry trace ||| Genuine smooth NSE data can start from \(d_Q=0\) with a positive entry trace
正式附图并列 hard/soft layer、Jordan atoms、预算分离与 NSE entry ||| The formal figure places the hard/soft layer, Jordan atoms, budget separation, and NSE entry side by side
主张—证据矩阵 ||| Claim–evidence matrix
状态 · R0.71O 精确 face theorem 与独立数值审计完成 ||| Status · R0.71O exact face theorem and independent numerical audit complete
BV、coarea 与时间解析性说明结构，不提供 NSE face sum ||| BV, coarea, and time analyticity describe the structure but do not provide an NSE face sum
hard/soft 极限关闭；weighted positive-entry sum 开放 ||| Hard/soft limit closed; weighted positive-entry sum open
I-style 右侧再加 \(2\lambda_j\theta_{Q,\varepsilon}a_{Q,\varepsilon}\)。有限阶零点上，这一附加非负测度的总质量趋于零。 ||| The I-style right side also contains \(2\lambda_j\theta_{Q,\varepsilon}a_{Q,\varepsilon}\). At a finite-order zero, the total mass of this additional nonnegative measure tends to zero.
R0.71N-style 与 R0.71I-style source 只差一个明确的 radial term ||| The R0.71N-style and R0.71I-style sources differ by one explicit radial term
R0.71O 没有新的 continuation criterion。它精确说明：soft denominator 不能作为“忽略 \(d_Q=0\)”的理由。有限阶 face 的 signed distribution、正负 Jordan atoms 和 absolute variation 都有明确公式；其中只有 signed 部分可能因左右重合而相消。 ||| R0.71O gives no new continuation criterion. It shows exactly why the soft denominator cannot justify ignoring \(d_Q=0\). The signed distribution, positive and negative Jordan atoms, and absolute variation of a finite-order face all have explicit formulas; only the signed part may cancel when the two sides coincide.
R0.71O soft denominator 的有限阶 profile、signed 与 Jordan face atoms、抽象预算分离和真实 NSE 初始 entry trace ||| The finite-order profile of the R0.71O soft denominator, signed and Jordan face atoms, abstract budget separation, and genuine NSE initial entry trace
R0.71O｜soft denominator 的一侧迹与 face measure ||| R0.71O | One-sided traces and face measure for the soft denominator
SciPy profiles、oscillatory paths 与 \(32^3\) FFT 分开核对 ||| SciPy profiles, oscillatory paths, and the \(32^3\) FFT are checked separately
signed jump 可以消失，正负 face atoms 不能因此删掉 ||| The signed jump may vanish, but the positive and negative face atoms cannot be deleted for that reason
soft 极限恢复 hard faces，而不是自动支付它们 ||| The soft limit recovers the hard faces rather than paying them automatically
soft denominator 消除坐标奇点， ||| The soft denominator removes the coordinate singularity,
soft regularization 解决的是 \(d_Q=0\) 处的坐标定义，不是 face-payment 问题。额外 soft radial damping 在有限阶零点没有原子；真正的 face measure 来自径向 cutoff factor 的导数。当前结果没有给出跨全部壳与小区的统一 NSE face sum。 ||| Soft regularization resolves the coordinate definition at \(d_Q=0\), not the face-payment problem. The extra soft radial damping has no atom at a finite-order zero; the actual face measure comes from the derivative of the radial cutoff factor. The current result gives no uniform NSE face sum across all shells and cells.
soft scalar 是 hard scalar 乘同一个径向因子 ||| The soft scalar is the hard scalar times the same radial factor
Temam 的周期强解理论 ||| Temam's periodic strong-solution theory
02 · 79 节完整索引 ||| 02 · Complete 79-section index
打开最新节点 R0.71O ||| Open the latest node R0.71O
回顾截止节点：R0.71O ||| Recap endpoint: R0.71O
回顾截止时公开笔记：139 ||| Public notes at the recap endpoint: 139
截至 R0.71O，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 79 个节点解释成对千禧年问题完成了某个比例。 ||| As of R0.71O, there is no new unconditional continuation criterion, no reduction of the class of all potential singular solutions, and no proof of finite-time breakdown. The 79 nodes cannot be interpreted as completing some percentage of the Millennium problem.
累计回顾 · R0.61–R0.71O · 2026-08-26 ||| Cumulative recap · R0.61–R0.71O · 2026-08-26
目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、有界重叠局部化与 denominator mass 支付。R0.71N 关闭了 fixed-cell interior 正平方候选；R0.71O 又关闭了“soft denominator 自动删除 faces”的想法。现在开放的是固定 partition 上的 all-shell/all-cell weighted positive-entry sum；total-Jordan sum 是更强的后续变体，refresh 与 moving-cutoff costs 则更靠后。 ||| The most substantial unconditional positive results remain the Leray-energy projected-Lamb heat volume, bounded-overlap localization, and denominator-mass payment. R0.71N closes the positive-square candidate in the fixed-cell interior; R0.71O also closes the idea that a soft denominator automatically deletes faces. The open object is now the all-shell/all-cell weighted positive-entry sum on a fixed partition. The total-Jordan sum is a stronger later variant, while refresh and moving-cutoff costs come later still.
十二个阶段、79 个节点：从约化递推到 projected-Lamb 局部热打包，再到 fixed-cell signed second jet 与 soft-denominator face boundary。 ||| Twelve phases and 79 nodes: from the reduced recurrence to projected-Lamb local heat packing, then to the fixed-cell signed second jet and soft-denominator face boundary.
收录节点：79 ||| Included nodes: 79
下一步固定 multiplier、cutoff 与 partition，检查右侧正向进入 atoms 的主门槛 \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\)。我先核对完整壳—小区求和是否存在 NSE-specific cancellation，或是否需要新的 crossing/transversality 输入。 ||| The next step fixes the multiplier, cutoff, and partition and tests the main threshold formed by right-side positive-entry atoms, \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\). I first check whether the complete shell–cell sum has an NSE-specific cancellation or requires a new crossing or transversality input.
这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71O 的 79 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。 ||| This page follows the R0.00–R0.60 phase recap and organizes R0.61 through R0.71O into 79 research nodes. I record chronologically what each phase actually proves, which proposals are ruled out by a concrete counterexample or scaling analysis, and which conditions have not been derived from the Navier–Stokes equations.
R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 79 个节点沿着这个缺口推进。 ||| The R0.00–R0.60 material remains in the previous phase recap. R0.60 concludes that the complete Fourier–Leray structure and higher-order calculations can continue, but the critical quantity for general three-dimensional solutions is still uncontrolled. The following 79 nodes proceed along this gap.
R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71O 的 79 个研究节点，记录从约化递推到 projected-Lamb 热体积、匹配小区 heat gap、signed second jet 与 soft-denominator face measure 的路线。 ||| Research recap after R0.60: a chronological account from R0.61 through R0.71O comprising 79 research nodes, tracing the route from the reduced recurrence to projected-Lamb heat volume, the matched-cell heat gap, the signed second jet, and the soft-denominator face measure.
R0.61–R0.71O 的 79 节公开笔记 ||| R0.61–R0.71O: 79 public notes
R0.61–R0.71O 回顾 · 2026-08-26 ||| R0.61–R0.71O recap · 2026-08-26
R0.61–R0.71O 研究节点 ||| R0.61–R0.71O research nodes
R0.61–R0.71O｜R0.60 之后的研究回顾 ||| R0.61–R0.71O | Research recap after R0.60
R0.70A–R0.71O 完成版本 ||| R0.70A–R0.71O completed releases
R0.71G–I 把时间缺口压到入口、单边联合生成与 faces。R0.71J–M 依次核对 matched-cell heat gap、viscous fusion 与 exact increment–projective bridge。R0.71N 证明表面的正平方被 local filtered-enstrophy acceleration 精确消去。R0.71O 再证明 soft quotient 精确恢复 hard 一侧迹；有限阶零点的 signed atom 可以相消，Jordan face cost 仍保留。raw source/radial logs 只有联合后才给出有限 face measure，ordinary budgets 不统一支付抽象 face count。 ||| R0.71G–I compress the time gap to entry, one-sided joint creation, and faces. R0.71J–M then check the matched-cell heat gap, viscous fusion, and the exact increment–projective bridge. R0.71N proves that the apparent positive square is canceled exactly by the local filtered-enstrophy acceleration. R0.71O further proves that the soft quotient recovers the one-sided hard traces exactly; the signed atom at a finite-order zero may cancel, while the Jordan face cost remains. The raw source/radial logarithms yield a finite face measure only after they are combined, and ordinary budgets do not uniformly pay the abstract face count.
R0.71G–R0.71O · 驻留、signed second jet 与 denominator faces ||| R0.71G–R0.71O · Residence, signed second jet, and denominator faces
R0.71O 把每个孤立有限阶零点的极限写成显式 atoms。signed jump 可能为零，但正负 Jordan masses 分别支付左右 traces。抽象 oscillatory paths 只排除 ordinary norms 单独控制 face count；一个真实 smooth NSE 初始 jet 给出 \(1/4\) 的右 entry trace，但没有构造大量内部 NSE faces。 ||| R0.71O writes the limit at every isolated finite-order zero as explicit atoms. The signed jump may be zero, but the positive and negative Jordan masses separately pay the left and right traces. The abstract oscillatory paths rule out only control of face count by ordinary norms alone; a genuine smooth NSE initial jet gives a right entry trace of \(1/4\), but does not construct many internal NSE faces.
R0.71P 检查 fixed-partition all-shell/all-cell weighted positive-entry sum ||| R0.71P tests the fixed-partition all-shell/all-cell weighted positive-entry sum
R0.71P 仍不引入 partition refresh 或 moving cutoffs。\(A_{j,Q,+}+A_{j,Q,-}\) 的 total-Jordan sum 是更强的后续变体，不是这一节的首要门槛；若正向进入和只能在额外 weighted-BV、zero-count 或 inverse-denominator 条件下闭合，我会把条件保留在 theorem 中。 ||| R0.71P still does not introduce partition refresh or moving cutoffs. The total-Jordan sum of \(A_{j,Q,+}+A_{j,Q,-}\) is a stronger later variant, not the primary threshold in that section. If the positive-entry sum closes only under an additional weighted-BV, zero-count, or inverse-denominator condition, I will retain that condition in the theorem.
raw source/radial 对数质量的精确抵消、ordinary-budget 抽象分离，以及右 entry trace \(1/4\) 的 smooth NSE initial jet。 ||| Exact cancellation of the logarithmic raw source/radial masses, an abstract ordinary-budget separation, and a smooth NSE initial jet with right entry trace \(1/4\).
soft–hard 精确因子分解、孤立有限阶零点的一侧 traces、signed/Jordan atoms 与奇偶阶 face 分类。 ||| Exact soft–hard factorization, one-sided traces at isolated finite-order zeros, signed and Jordan atoms, and the odd/even face classification.
本节关闭的是“soft denominator 自动删除 fixed-cell faces”这一想法。它没有证明完整 NSE weighted face sum 发散，也没有得到继续性、奇性或全局正则性结论。 ||| This section closes the idea that a soft denominator automatically deletes fixed-cell faces. It does not prove divergence of the complete NSE weighted face sum and gives no continuation, singularity, or global-regularity conclusion.
查看独立数值审计 ||| View the independent numerical audit
查看文献审计 ||| View the literature audit
查看主张—证据矩阵 ||| View the claim–evidence matrix
从有符号环带障碍走到 soft-denominator face boundary ||| From the signed-annulus obstruction to the soft-denominator face boundary
固定 partition 上，检查 \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\) 是否存在 NSE-specific cancellation 或新的必要输入。total-Jordan sum 是更强的后续变体。 ||| On a fixed partition, test whether \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\) has an NSE-specific cancellation or requires a new input. The total-Jordan sum is a stronger later variant.
固定 partition 上，检查全壳、全小区的正向进入和 \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\) 是否有新的 cancellation 或必须保留额外条件。 ||| On a fixed partition, test whether the all-shell/all-cell positive-entry sum \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\) has a new cancellation or must retain an additional condition.
环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary ||| Annulus exclusion → source–core ledger → covariance spectral stratification → all-frequency conditional bridge → response-slope chord gain → common-response order-one channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary
静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 建立 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–N 依次核对 residence、matched-cell heat gap、viscous fusion、increment bridge 与 signed second jet。R0.71O 证明 soft denominator 精确恢复 hard 一侧 traces：signed atoms 可以抵消，Jordan face costs 仍保留；ordinary budgets 不统一支付抽象 face count。 ||| After the static annular family is ruled out rigorously, the route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71A–F establish the Leray-energy projected-Lamb heat volume and its bounded-overlap localization. R0.71G–N then check residence, the matched-cell heat gap, viscous fusion, the increment bridge, and the signed second jet. R0.71O proves that the soft denominator recovers the one-sided hard traces exactly: signed atoms may cancel, while the Jordan face costs remain; ordinary budgets do not uniformly pay the abstract face count.
累计回顾 R0.61–R0.71O · 2026-08-26 ||| Cumulative recap R0.61–R0.71O · 2026-08-26
目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71O 证明 soft denominator 只平滑坐标，不删除一侧 face cost；signed atoms 可以抵消，Jordan masses 仍保留。固定 partition 上的 all-shell/all-cell weighted positive-entry sum 尚未闭合。 ||| There is no new unconditional continuation criterion and no construction of a finite-time singularity. R0.71O proves that the soft denominator only smooths the coordinates and does not delete the one-sided face cost; signed atoms may cancel, while the Jordan masses remain. The all-shell/all-cell weighted positive-entry sum on a fixed partition remains open.
若 \(C_Q(t_0+\tau)=c\tau^m+O(|\tau|^{m+1})\)、 \(C_{Q,t}(t_0+\tau)=mc\tau^{m-1}+O(|\tau|^m)\)，且 \(F_j,Y\) 的一阶导数局部有界，一侧 traces 由 \(\gamma=\langle F_j(t_0),c\rangle/(\sqrt{Y(t_0)}\|c\|_2)\) 决定。 奇阶零点的 signed atom 是 \(\gamma|\gamma|\delta_{t_0}\)，face variation 为 \(\gamma^2\)；偶阶 signed atom 为零，但 \(\gamma>0\) 时仍支付 \(2\gamma^2\) 的 Jordan variation。 ||| If \(C_Q(t_0+\tau)=c\tau^m+O(|\tau|^{m+1})\), \(C_{Q,t}(t_0+\tau)=mc\tau^{m-1}+O(|\tau|^m)\), and the first derivatives of \(F_j,Y\) are locally bounded, the one-sided traces are determined by \(\gamma=\langle F_j(t_0),c\rangle/(\sqrt{Y(t_0)}\|c\|_2)\). At an odd-order zero, the signed atom is \(\gamma|\gamma|\delta_{t_0}\) and the face variation is \(\gamma^2\); at an even-order zero, the signed atom is zero, but when \(\gamma>0\) it still pays Jordan variation \(2\gamma^2\).
上次综述 v0.99 · 2026-08-26 ||| Previous review v0.99 · 2026-08-26
我保持 multiplier、cutoff 与 partition 固定，先检查 \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\) 是否存在 NSE-specific cancellation；total-Jordan sum 是更强的后续变体，暂不引入 refresh atoms 或 moving cutoffs。 ||| I keep the multiplier, cutoff, and partition fixed and first test whether \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\) has an NSE-specific cancellation. The total-Jordan sum is a stronger later variant; refresh atoms and moving cutoffs remain outside the scope.
我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71O 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。 ||| I also maintain a systematic review page that places classical theory, five main literature branches, the candidate blow-up exclusion tree, progress from 2019—2026, and this site's R0.69P–R0.71O route on one map. Historical nodes R0.61–R0.69O remain in the cumulative recap.
下一步 R0.71P： ||| Next step R0.71P:
研究笔记 R0.71O · 2026-08-26 ||| Research note R0.71O · 2026-08-26
阅读 R0.71O 研究笔记 → ||| Read the R0.71O research note →
在每个 \(d_Q>0\) 分支上， \[ \sigma_{Q,\varepsilon}=\frac{d_Q}{d_Q+\varepsilon},\qquad z_{Q,\varepsilon}=\sqrt{\sigma_{Q,\varepsilon}}z_Q,\qquad a_{Q,\varepsilon}=\sigma_{Q,\varepsilon}a_Q. \] 因而 soft source 精确分成 hard interior source 与 \((\sigma_{Q,\varepsilon})_ta_Q\) face layer。 ||| On every branch with \(d_Q>0\), \[ \sigma_{Q,\varepsilon}=\frac{d_Q}{d_Q+\varepsilon},\qquad z_{Q,\varepsilon}=\sqrt{\sigma_{Q,\varepsilon}}z_Q,\qquad a_{Q,\varepsilon}=\sigma_{Q,\varepsilon}a_Q. \] The soft source therefore splits exactly into a hard interior source and the face layer \((\sigma_{Q,\varepsilon})_ta_Q\).
展开 49 篇公开笔记 ||| Expand 49 public notes
综述 v1.00 · 2026-08-26 ||| Review v1.00 · 2026-08-26
R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、固定匹配小区、signed second jet 与 soft-denominator faces。R0.70A–R0.71O 共 41 个完成版本。 ||| The route after R0.60 has twelve phases: reduced Picard and the shear boundary, transverse perturbations, the local pressure budget, signed physical annuli, moving labels and source–core duality, the defect tensor and finite observations, complete-frame covariance, the constant-projection boundary, positive output and the material-heat tent, projected-Lamb heat volume, local heat packing and the critical trace obstruction, and finally the residence boundary, fixed matched cells, the signed second jet, and soft-denominator faces. R0.70A–R0.71O contains 41 completed releases.
R0.60 recap 之后的累计回顾收录 79 个节点；全站现有 139 篇公开研究笔记 ||| The cumulative recap after the R0.60 recap contains 79 nodes; the site now has 139 public research notes
R0.71O 已完成： ||| R0.71O completed:
raw source 与 radial term 各自按 \(\log(1/\varepsilon)\) 增长，联合后对数精确抵消。一个 smooth Hilbert path 使 face cost 按零点数增长，而 ordinary derivative、source 与 denominator-mass budgets 保持有界；它不是 NSE 多-face 构造。真实 smooth NSE 初始 jet 则给出精确右 entry trace \(1/4\)。 ||| The raw source and radial term each grow like \(\log(1/\varepsilon)\), and their logarithms cancel exactly after they are combined. A smooth Hilbert path makes the face cost grow with the zero count while the ordinary derivative, source, and denominator-mass budgets remain bounded; it is not an NSE multiple-face construction. A genuine smooth NSE initial jet gives the exact right entry trace \(1/4\).
soft denominator 恢复一侧 hard traces，Jordan face cost 没有自动消失 ||| The soft denominator recovers one-sided hard traces; the Jordan face cost does not disappear automatically
soft–hard factorization 与有限阶 face atoms 已显式闭合；额外 soft radial damping 没有 finite-order atom。 ||| The soft–hard factorization and finite-order face atoms are closed explicitly; the extra soft radial damping has no finite-order atom.
`;

const rows = translationRows.trim().split("\n");
const additions = new Map(
  rows.map((row) => {
    const separator = " ||| ";
    const index = row.indexOf(separator);
    if (index < 1) throw new Error("invalid translation row: " + row);
    return [row.slice(0, index), row.slice(index + separator.length)];
  }),
);
if (additions.size !== rows.length) {
  throw new Error("duplicate Chinese keys in the R0.71O additions");
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
  "recap-r0-61-r0-71o.html",
  "notes/r0-71o.html",
];
for (const relative of activePages) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.00')) {
    throw new Error(relative + ": expected i18n cache version v1.00");
  }
}

const batchId = /^r071o\d+$/;
const currentWithoutBatch = current.filter((entry) => !batchId.test(entry.id));
const currentByChinese = new Map(
  currentWithoutBatch.map((entry) => [entry.zh, entry]),
);
if (currentByChinese.size !== currentWithoutBatch.length) {
  throw new Error(
    "duplicate Chinese keys already present outside the R0.71O batch",
  );
}

const sourceByChinese = new Map(source.map((entry) => [entry.zh, entry]));
if (sourceByChinese.size !== source.length) {
  throw new Error("duplicate Chinese keys in collected site strings");
}

const missing = source.filter((entry) => !currentByChinese.has(entry.zh));
const missingChinese = new Set(missing.map((entry) => entry.zh));
if (additions.size !== missing.length) {
  throw new Error(
    "expected additions to equal the " +
      missing.length +
      " active missing strings, found " +
      additions.size,
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
    id: "r071o" + String(index + 1).padStart(3, "0"),
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
