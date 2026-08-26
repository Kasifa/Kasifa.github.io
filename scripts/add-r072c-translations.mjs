import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const projectRoot = resolve(import.meta.dirname, "..");
const translationsPath = resolve(projectRoot, "translations", "en.json");
const publicDirectory = resolve(projectRoot, "public");

const rows = [
  ["处理固定低维随机动力系统或交替正弦 shear，也不提供 deterministic phase-uniform growing-carrier theorem。已核对来源都不估计 decay time 之前累积的 launch-inclusive root ledger；terminal decay 只能改善 tail，不能删除 pre-ledger。这里不作优先权或一般 NSE 结论。"," treat fixed low-dimensional stochastic dynamical systems or alternating sinusoidal shears, and likewise do not provide a deterministic phase-uniform growing-carrier theorem. None of the checked sources estimates the launch-inclusive root ledger accumulated before the decay time; terminal decay can improve only the tail and cannot remove the pre-ledger. No claim of priority or general NSE conclusion is made here."],
  ["打开 93 节完整索引","Open the complete 93-note index"],
  ["共轭配对保留 skew coupling；joint participation inequality 给 phase-uniform exact-launch \\(M^{-8/3}\\) 与 fixed-positive tail \\(M^{-3}\\)。odd-generation Rudin–Shapiro signs 和固定正时刻同号 family 分别使两个 algebraic exponents 取到。","Conjugate pairing preserves skew coupling; the joint participation inequality gives phase-uniform exact-launch \\(M^{-8/3}\\) and fixed-positive tail \\(M^{-3}\\). Odd-generation Rudin–Shapiro signs and a same-sign family at fixed positive time attain the two algebraic exponents, respectively."],
  ["记录 Rudin–Shapiro recurrence、\\(\\pm1\\) coefficients 与 \\(\\sqrt M\\)-scale bound；本节只使用可由 parallelogram identity 直接复核的 dyadic odd generations。"," record the Rudin–Shapiro recurrence, \\(\\pm1\\) coefficients, and a \\(\\sqrt M\\)-scale bound; this note uses only dyadic odd generations that can be checked directly from the parallelogram identity."],
  ["检查 sharp algebraic prefactor 能否由真实 target roots、complete root-slope mass 与 full rotational charge 同时实现。","Test whether the sharp algebraic prefactor can be realized simultaneously by genuine target roots, complete root-slope mass, and the full rotational charge."],
  ["开放接口 · R0.72D","Open interface · R0.72D"],
  ["累计回顾与 93 节索引","Cumulative recap and 93-note index"],
  ["文献综述 v1.16 · 2026-08-27","Literature review v1.16 · 2026-08-27"],
  ["我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.72C 只列为研究笔记。我不把计算或笔记外推成正则性定理。","Published theorems are listed as established results, 2026 preprints are marked separately, and this site's R0.69P–R0.72C material is listed only as research notes. I do not extrapolate calculations or notes into regularity theorems."],
  ["中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–U 给出 conditional incidence、genuine internal-entry、second-time-jet 与 finite recurrence 边界。R0.71V–W 分离 fixed zero-level trace 并排除 data-uniform complete first-row ledger。R0.71X 在 fixed-dimensional small-coupling family 内达到 one-third endpoint；R0.71Y 处理 selected roots；R0.71Z 给出 all-root slope-mass bound 和 launch-inclusive floor cancellation；R0.72A 把 strong-coupling loss 局部化到实际观察层，R0.72B 保留 exact target-row participation，R0.72C 再以共轭配对覆盖任意 physical phases，并得到 phase-uniform exact-launch \\(M^{-8/3}\\) 与 fixed-positive tail \\(M^{-3}\\) 的 sharp algebraic scales。一般 Navier–Stokes 正则性仍开放。",". R0.69P–R0.71P reaches the positive-entry temporal-packing boundary; R0.71Q–U establishes the boundaries for conditional incidence, genuine internal entry, the second-time jet, and finite recurrence. R0.71V–W separates the fixed zero-level trace and rules out a data-uniform complete first-row ledger. R0.71X reaches the one-third endpoint in a fixed-dimensional small-coupling family; R0.71Y treats selected roots; R0.71Z gives an all-root slope-mass bound and launch-inclusive floor cancellation; R0.72A localizes the strong-coupling loss to the actual observation layer, R0.72B retains exact target-row participation, and R0.72C extends conjugate pairing to arbitrary physical phases and obtains the sharp algebraic scales of phase-uniform exact-launch \\(M^{-8/3}\\) and fixed-positive tail \\(M^{-3}\\). General Navier–Stokes regularity remains open."],
  ["中的 uniform-in-diffusivity 或 pathwise phase 针对一个固定 profile，不表示对 \\(M\\)-dependent carrier family 一致。"," treat uniform-in-diffusivity or pathwise phase for one fixed profile; this does not imply uniformity over an \\(M\\)-dependent carrier family."],
  ["physical-phase conjugate pairing 与 sharp carrier scales","Physical-phase conjugate pairing and sharp carrier scales"],
  ["R0.72C 的 phase theorem 与 Rudin–Shapiro sharpness","The R0.72C phase theorem and Rudin–Shapiro sharpness"],
  ["R0.72C 的主源边界","Primary-source boundary for R0.72C"],
  ["R0.72C 先修正 physical-phase operator：两侧 Fourier shifts 的系数必须互为共轭，直接把旧对称移位换成复系数会破坏 skew-adjointness。随后把 \\(\\chi_A\\) 与 \\(\\Omega_A\\) 联合估计，得到 \\(\\Phi_{A,M}\\le C M^{-3}H_M(A)^{1/3}\\)。exact launch 的 phase-uniform 尺度是 \\(M^{-8/3}\\)，固定正观察时刻的 restarted tail 尺度是 \\(M^{-3}\\)。scalar root-slope statement 对所有实 \\(\\delta\\) 成立，complete physical-time root ledger 只在 \\(\\delta\\ne0\\) 时陈述。","R0.72C first corrects the physical-phase operator: the coefficients of the two Fourier shifts must be complex conjugates, since directly replacing the old symmetric shifts with complex coefficients breaks skew-adjointness. A joint estimate of \\(\\chi_A\\) and \\(\\Omega_A\\) then gives \\(\\Phi_{A,M}\\le C M^{-3}H_M(A)^{1/3}\\). The phase-uniform scale at exact launch is \\(M^{-8/3}\\), while the restarted-tail scale at a fixed positive observation time is \\(M^{-3}\\). The scalar root-slope statement holds for every real \\(\\delta\\), whereas the complete physical-time root ledger is stated only for \\(\\delta\\ne0\\)."],
  ["，fixed-positive 为",", and the fixed-positive value is"],
  ["01 · 物理相位模型","01 · Physical-phase model"],
  ["03 · 联合相位不等式","03 · Joint phase inequality"],
  ["05 · 充分相界","05 · Sufficient phase boundaries"],
  ["06 · 两个尖锐族","06 · Two sharp families"],
  ["07 · burn-in 边界","07 · Burn-in boundary"],
  ["08 · 双路证书","08 · Dual-path certificates"],
  ["90 位 mpmath；重建 naive-complex witness、共轭配对、联合不等式、三个 heat regimes、相界与两个尖锐族。Rudin–Shapiro 尾指数为","90-digit mpmath; reconstructs the naive-complex witness, conjugate pairing, joint inequality, three heat regimes, phase boundaries, and two sharp families. The Rudin–Shapiro tail exponent is"],
  ["版本 v0.72C · 2026-08-27","Version v0.72C · 2026-08-27"],
  ["本节把“相位可能破坏结果”改写成一条尖锐、可计算的损失定理","This note turns “phases may break the result” into a sharp, computable loss theorem"],
  ["不导入 producer 或其结果；使用有限 complex matrices、角网格、独立 binary-parity Rudin–Shapiro 路径与 separate regressions。两条尾指数为","Does not import the producer or its outputs; uses finite complex matrices, an angular grid, an independent binary-parity Rudin–Shapiro path, and separate regressions. The two tail exponents are"],
  ["但损失可以精确量化","but the loss can be quantified exactly"],
  ["但它只用于解释 profile，真正提供 uniform power 的是上面的联合式。","It serves only to interpret the profile; the joint formula above supplies the uniform power."],
  ["第一，任意 physical phase 不是把旧系数换成复数那么简单；共轭配对是保持能量律的必要模型修正。第二，coherent \\(M^{-10/3}\\) 与 arbitrary-phase \\(M^{-8/3}\\) 的差距由 exact Rudin–Shapiro family 证明，不再是数值印象。第三，正 burn-in 的优势与 pre-ledger 的责任被严格分开。","First, arbitrary physical phases cannot be handled by merely replacing the old coefficients with complex numbers; conjugate pairing is the necessary model correction that preserves the energy law. Second, the gap between coherent \\(M^{-10/3}\\) and arbitrary-phase \\(M^{-8/3}\\) is proved by an exact Rudin–Shapiro family rather than inferred numerically. Third, the benefit of positive burn-in is separated rigorously from responsibility for the pre-ledger."],
  ["独立逐式审计","Independent line-by-line audit"],
  ["对每个实 \\(\\delta\\)，先得到不含除法的 slope theorem：","For every real \\(\\delta\\), first obtain a slope theorem that involves no division:"],
  ["对千禧年问题的价值仍然是边界性和排除性：它关闭了 declared triangular 2.5D class 内一种 phase-uniform coherent promotion，但没有控制一般三维 vortex stretching，也没有给出新的无条件继续性判据。","Its value for the Millennium Problem remains boundary-setting and exclusionary: it closes one phase-uniform coherent-promotion mechanism inside the declared triangular 2.5D class, but it neither controls general three-dimensional vortex stretching nor gives a new unconditional continuation criterion."],
  ["固定模长时 leading factor 不再依赖相位；exposure bracket 仍可能依赖相位。","For fixed moduli, the leading factor no longer depends on phase; the exposure bracket can still depend on phase."],
  ["耗散边界","Dissipation boundary"],
  ["解析证明、90 位 producer 与 binary64 checker 三条证据链相互分离","The analytic proof, 90-digit producer, and binary64 checker form three separate evidence chains"],
  ["旧的 symmetric-shift 写法若取单载波 \\(z=i\\)，就变成 self-adjoint 的 \\(K_z(T_1+T_{-1})\\)。在 \\((e_0+e_1)/\\sqrt2\\) 上，其能量导数可在大耦合下变成正数。因此该写法不能承载任意 Fourier 相位。","For the old symmetric-shift form, choosing a single carrier \\(z=i\\) produces the self-adjoint operator \\(K_z(T_1+T_{-1})\\). On \\((e_0+e_1)/\\sqrt2\\), its energy derivative can become positive at large coupling. This form therefore cannot represent arbitrary Fourier phases."],
  ["联合不等式","Joint inequality"],
  ["两个幂次都是 upper-ledger algebraic prefactor 的尖锐指数。它们不构成实际 root mass 的下界，也不表示 normalized nonlinear ledger 被某条解饱和。","Both powers are sharp exponents of the upper-ledger algebraic prefactor. They neither give a lower bound on actual root mass nor show that the normalized nonlinear ledger is saturated by a solution."],
  ["令 \\(A_{0,M}\\asymp M^{-\\sigma}\\)。则","Let \\(A_{0,M}\\asymp M^{-\\sigma}\\). Then"],
  ["目标行的模长不看相位，全部根估计因此保持稳定","The modulus of the target row does not see phase, so the all-root estimate remains stable"],
  ["取 \\(M=2^n\\)、\\(n\\) 为奇数，载波 \\(r_l=l\\)，系数使用 Rudin–Shapiro 符号。递推恒等式 \\(|P_n|^2+|Q_n|^2=2M\\) 与 \\(P_n(1)=\\sqrt{2M}\\) 给出 exact norm：","Take \\(M=2^n\\), with odd \\(n\\), carriers \\(r_l=l\\), and Rudin–Shapiro signs as coefficients. The recurrence identity \\(|P_n|^2+|Q_n|^2=2M\\) and \\(P_n(1)=\\sqrt{2M}\\) give the exact norm:"],
  ["热层","Heat layer"],
  ["任何合法的 terminal energy decay 都可以改善第二项；第一项非负，不能被减去。","Any valid terminal energy decay can improve the second term; the first term is nonnegative and cannot be subtracted."],
  ["任意物理相位把 coherent M^{-10/3} 修正为 sharp M^{-8/3}；固定正观察层的 tail 为 sharp M^{-3}。","Arbitrary physical phases change coherent M^{-10/3} to sharp M^{-8/3}; the tail at a fixed positive observation layer is sharp M^{-3}."],
  ["任意物理相位的统一指数是 \\(-8/3\\)，不是同相族的 \\(-10/3\\)","The uniform exponent for arbitrary physical phases is \\(-8/3\\), not the phase-aligned family's \\(-10/3\\)"],
  ["若 \\(\\eta=M^\\alpha\\)、\\(L=M^{-\\beta}\\)，且 \\(\\Phi=O(M^{-p})\\)，充分消失条件统一为","If \\(\\eta=M^\\alpha\\), \\(L=M^{-\\beta}\\), and \\(\\Phi=O(M^{-p})\\), the sufficient vanishing condition takes the uniform form"],
  ["若 \\(\\rho_A=0\\)，所有 \\(w_l\\) 都为零；该退化支路在任何除法前单独设 \\(q_\\rho=\\ell_\\times=\\chi_A=0\\)，根斜率与目标行质量均为零。","If \\(\\rho_A=0\\), every \\(w_l\\) is zero; before any division, this degenerate branch separately sets \\(q_\\rho=\\ell_\\times=\\chi_A=0\\), and both the root slope and target-row mass are zero."],
  ["若 \\(t_M=\\kappa A_{0,M}\\to\\infty\\)，首个 carrier 主导并进一步给 \\(\\Phi_{A,M}=O(M^{-3}e^{-2t_M/3})\\)。","If \\(t_M=\\kappa A_{0,M}\\to\\infty\\), the first carrier dominates and further gives \\(\\Phi_{A,M}=O(M^{-3}e^{-2t_M/3})\\)."],
  ["若该构造仍失败，则使用 evolution information 给出更强的 dynamical exclusion theorem。只有 terminal energy plot、FFT maximum 或 fitted exponent 都不足以通过该关口。","If that construction still fails, use evolution information to establish a stronger dynamical exclusion theorem. A terminal energy plot, FFT maximum, or fitted exponent alone is insufficient to pass this gate."],
  ["若载波是互异正整数且幅度可比，排序后 \\(r_{(j)}\\ge j\\)，于是 \\(K_s\\gtrsim M^3\\)、\\(K_v\\gtrsim a_M^2K_s\\)，而 \\(\\rho_A^2\\) 由 \\(H_M(A_0)\\) 控制。这给出统一 \\(M^{-3}H_M^{1/3}\\) 前因子。","If the carriers are distinct positive integers with comparable amplitudes, sorting gives \\(r_{(j)}\\ge j\\), hence \\(K_s\\gtrsim M^3\\) and \\(K_v\\gtrsim a_M^2K_s\\), while \\(\\rho_A^2\\) is controlled by \\(H_M(A_0)\\). This yields the uniform prefactor \\(M^{-3}H_M^{1/3}\\)."],
  ["三条具体边界是","The three specific boundaries are"],
  ["实际 root mass 下界、相图 converse、finite-time singularity、继续性判据、global regularity、原创性或优先权结论。","a lower bound on actual root mass, a converse to the phase diagram, finite-time singularity, a continuation criterion, global regularity, or claims of originality or priority."],
  ["双路程序都记录命令、环境、进度、资源与 SHA-256。它们不是 interval arithmetic，也不是 infinite-lattice proof；解析报告和独立逐式审计承担证明责任。","Both computational paths record commands, environment, progress, resources, and SHA-256. They are neither interval arithmetic nor an infinite-lattice proof; the analytic report and independent line-by-line audit carry the proof obligation."],
  ["所以 \\(V_w\\) 仍是 skew-adjoint，exact contraction 与耗散预算继续成立。","Thus \\(V_w\\) remains skew-adjoint, and the exact contraction and dissipation budget continue to hold."],
  ["所以 phase-uniform \\(O(M^{-10/3})\\) 不成立。固定 \\(A_0=A=A_*>0\\) 时，取同号 \\(r_l=l,w_l=a_M\\)，两个 heat sums 都趋于有限正极限，直接得到 \\(\\Phi_{A,M}\\asymp M^{-3}\\)。","Hence a phase-uniform \\(O(M^{-10/3})\\) bound is false. At fixed \\(A_0=A=A_*>0\\), choose same-sign \\(r_l=l,w_l=a_M\\); both heat sums converge to finite positive limits, directly giving \\(\\Phi_{A,M}\\asymp M^{-3}\\)."],
  ["它在角变量中对应 \\(-i\\) 乘以实剪切","In the angular variable it corresponds to a real shear multiplied by \\(-i\\)"],
  ["图 R0.72C-1。A：exact-launch coherent \\(M^{-10/3}\\) 与 odd-generation Rudin–Shapiro \\(M^{-8/3}\\) 精确前因子；后者证明 phase-uniform coherent 指数失败。B：coherent exact launch、arbitrary-phase exact launch 与 fixed-positive tail 的三条充分相界；曲线外没有 converse。附图使用解析公式，不把回归斜率当成定理。","Figure R0.72C-1. A: the exact prefactors for exact-launch coherent \\(M^{-10/3}\\) and odd-generation Rudin–Shapiro \\(M^{-8/3}\\); the latter disproves a phase-uniform coherent exponent. B: the three sufficient phase boundaries for coherent exact launch, arbitrary-phase exact launch, and the fixed-positive tail; there is no converse outside the curves. The figure uses analytic formulas and does not treat regression slopes as theorems."],
  ["下一步优先尝试 phase-cancelled dynamical lower family：明确给出 \\(F_M(0)\\)、\\(\\delta_M\\)、观察窗、exact roots、complete root-slope mass 与 full \\(\\Lambda_1\\) charge，并证明 normalized lower bound 不消失。","The next step prioritizes a phase-cancelled dynamical lower family: specify \\(F_M(0)\\), \\(\\delta_M\\), the observation window, exact roots, complete root-slope mass, and the full \\(\\Lambda_1\\) charge, then prove that the normalized lower bound does not vanish."],
  ["下一对象：actual root-ledger lower family","Next object: actual root-ledger lower family"],
  ["相界","Phase boundaries"],
  ["相图比较固定 effective coupling \\(\\eta\\)。若固定 raw coupling \\(\\delta\\)，则","The phase diagram compares fixed effective coupling \\(\\eta\\). If the raw coupling \\(\\delta\\) is fixed instead, then"],
  ["相位抵消会损失同相增益，","Phase cancellation loses the phase-aligned gain,"],
  ["相位抵消同时改变 participation 与 multiplier-to-moment，不能拆开估","Phase cancellation changes participation and multiplier-to-moment simultaneously, so they cannot be estimated separately"],
  ["相位模型","Phase model"],
  ["相位损失与三条充分边界使用同一组精确公式展示","Phase loss and the three sufficient boundaries are displayed using the same exact formulas"],
  ["研究笔记 R0.72C · PHYSICAL PHASES · HEAT PARTICIPATION · SHARP SCALE","Research note R0.72C · PHYSICAL PHASES · HEAT PARTICIPATION · SHARP SCALE"],
  ["研究笔记 R0.72C：修正任意物理相位下的共轭配对模型，证明 phase-uniform exact-launch M^{-8/3} 与 fixed-positive tail M^{-3} 的尖锐代数前因子；这不是一般三维正则性定理。","Research note R0.72C: corrects the conjugate-paired model for arbitrary physical phases and proves sharp algebraic prefactors of M^{-8/3} at phase-uniform exact launch and M^{-3} for the fixed-positive tail; this is not a general three-dimensional regularity theorem."],
  ["已核对的 time-dependent、pathwise、scalar-modulated、translating 与 random-shear 结果分别处理固定 profile、统一受控的有限临界几何、单个空间形状的时间调制、刚性平移正弦或固定随机动力系统。它们没有给随 \\(M\\) 改变的 heat-decaying phase family 的统一常数，也不估计从 launch 开始累计的 target-root ledger。","The checked time-dependent, pathwise, scalar-modulated, translating, and random-shear results respectively treat a fixed profile, uniformly controlled finite critical geometry, time modulation of one spatial shape, a rigidly translating sine wave, or a fixed stochastic dynamical system. They provide neither uniform constants for a heat-decaying phase family that varies with \\(M\\) nor an estimate of the target-root ledger accumulated from launch."],
  ["这里 \\(\\chi_A=\\rho_A^2/\\Omega_A^2\\)。抵消会压低 \\(\\Omega_A\\)，使 \\(\\chi_A\\) 变大；但同一个 \\(\\Omega_A\\) 又出现在另一个因子中。联合不等式保留了这组补偿，单独给 \\(\\chi_A\\) 找统一 \\(M^{-1}\\) 上界则会失败。","Here \\(\\chi_A=\\rho_A^2/\\Omega_A^2\\). Cancellation lowers \\(\\Omega_A\\), making \\(\\chi_A\\) larger; but the same \\(\\Omega_A\\) also appears in another factor. The joint inequality retains this compensation, whereas seeking a separate upper bound for \\(\\chi_A\\) uniformly of order \\(M^{-1}\\) fails."],
  ["这些都是 upper ledger 趋零的充分区域。等号线和外部点不是 converse。","These are sufficient regions in which the upper ledger vanishes. Neither the equality curves nor the exterior points provide a converse."],
  ["正 pre-observation layer 把有效 carrier 数压缩成 Gaussian heat sum","A positive pre-observation layer compresses the effective carrier count into a Gaussian heat sum"],
  ["正确的 conjugate-paired arbitrary-phase model；all-real-\\(\\delta\\) slope theorem；\\(\\delta\\ne0\\) complete target-root ledger；联合相位不等式；heat transition；两个尖锐 algebraic prefactor。","The correct conjugate-paired arbitrary-phase model; an all-real-\\(\\delta\\) slope theorem; the complete target-root ledger for \\(\\delta\\ne0\\); the joint phase inequality; the heat transition; two sharp algebraic prefactors."],
  ["正确模型必须共轭配对：","The correct model must use conjugate pairing:"],
  ["证明、文献边界、双路证书与正式附图包完整保留","The proof, literature boundary, dual-path certificates, and publication-ready figure package are retained in full"],
  ["直接把实系数改成复数会破坏能量律","Directly replacing real coefficients with complex ones breaks the energy law"],
  ["只有在 \\(\\delta\\ne0\\) 时，使用 \\(F_0'=\\delta P_0V_wF\\) 除以 \\(\\delta^2\\)，得到","Only for \\(\\delta\\ne0\\), dividing \\(F_0'=\\delta P_0V_wF\\) by \\(\\delta^2\\) gives"],
  ["状态 · R0.72C 完成","Status · R0.72C completed"],
  ["actual phase-cancelled root-ledger lower family；full normalized charge saturation；changing-profile uniform enhanced dissipation；非 triangular 三维反馈。","an actual phase-cancelled root-ledger lower family; saturation of the full normalized charge; changing-profile uniform enhanced dissipation; non-triangular three-dimensional feedback."],
  ["checked literature 不提供 carrier-count-uniform launch-ledger 定理","The checked literature provides no carrier-count-uniform launch-ledger theorem"],
  ["effective carrier 诊断仍有","The effective-carrier diagnostic still gives"],
  ["exact-launch 结果覆盖全部物理相位；固定正时间结果只控制 restart 后的 tail。已经在 \\([0,A_*]\\) 累积的非负 pre-ledger 不会被后来的衰减抵消。","The exact-launch result covers all physical phases; the fixed-positive-time result controls only the tail after restart. The nonnegative pre-ledger already accumulated on \\([0,A_*]\\) cannot be canceled by later decay."],
  ["heat-semigroup contraction 给 \\(\\Omega_A=\\|V_w(A_0)\\|\\)。differentiated row 与 mixed exposure 仍满足","Heat-semigroup contraction gives \\(\\Omega_A=\\|V_w(A_0)\\|\\). The differentiated row and mixed exposure still satisfy"],
  ["naive complex symmetric shifts；phase-uniform coherent \\(M^{-10/3}\\)；用 terminal decay 抹去 pre-ledger。","naive complex symmetric shifts; phase-uniform coherent \\(M^{-10/3}\\); using terminal decay to erase the pre-ledger."],
  ["phase-free、coherent 与 positive-tail 三条相界不能混写","The phase-free, coherent, and positive-tail phase boundaries must remain distinct"],
  ["R0.72B 的 \\(M^{-10/3}\\) 依赖 exact launch 的同相峰值。本节先修正复系数模型：两条反向 shift 必须使用 \\(w_l\\) 与 \\(\\overline{w_l}\\)，否则 skew-adjointness 直接失效。对正确的物理相位模型，target-row theorem 保持不变；把 participation 与 multiplier-to-moment 两项联合估计后，任意相位的 exact-launch 尺度变为 \\(M^{-8/3}\\)，固定正 restart tail 变为 \\(M^{-3}\\)。Rudin–Shapiro 与同号热层分别证明这两个代数幂次不能再统一改善。","The R0.72B scale \\(M^{-10/3}\\) relies on the phase-aligned peak at exact launch. This note first corrects the complex-coefficient model: the two opposite shifts must use \\(w_l\\) and \\(\\overline{w_l}\\), or skew-adjointness fails immediately. For the correct physical-phase model, the target-row theorem remains unchanged; after jointly estimating participation and multiplier-to-moment, the exact-launch scale for arbitrary phases becomes \\(M^{-8/3}\\), while the fixed-positive restarted-tail scale becomes \\(M^{-3}\\). The Rudin–Shapiro and same-sign heat-layer families respectively prove that these two algebraic powers cannot be improved uniformly."],
  ["R0.72C · 2026-08-27 · 个人数学研究日志","R0.72C · 2026-08-27 · Personal mathematical research log"],
  ["R0.72C｜物理相位、热参与率与尖锐 phase-free carrier 尺度","R0.72C | Physical phases, heat participation, and sharp phase-free carrier scales"],
  ["R0.72D 必须进入实际动力学，而不是继续优化静态代数前因子","R0.72D must enter the actual dynamics instead of further optimizing static algebraic prefactors"],
  ["Rudin–Shapiro 与同号热层分别达到两个 phase-free 幂次","Rudin–Shapiro and the same-sign heat layer attain the two phase-free powers, respectively"],
  ["“已公开并封存”表示相应推导、精确计算程序、独立检查和公开材料在声明范围内已经核对，不表示阶段目标已解决，也不表示通过外部同行评审。计算反例和光滑解族只排除它们明确覆盖的估计。", "The label “published and archived” means that the corresponding derivations, exact computational programs, independent checks, and public materials have been verified within their stated scope. It does not mean that the phase objective has been resolved or that the material has passed external peer review. Computational counterexamples and smooth solution families rule out only the estimates they explicitly cover."],
  ["01 · 二十个研究阶段", "01 · Twenty research phases"],
  ["02 · 93 节完整索引", "02 · Complete 93-note index"],
  ["保留 R0.72B 历史回顾", "Keep the R0.72B historical recap"],
  ["闭", "Closed"],
  ["查看 R0.72C 双路证书", "View the R0.72C dual-path certificates"],
  ["打开最新节点 R0.72C", "Open the latest node, R0.72C"],
  ["点态拉伸尖锐常数可由光滑无散场实现；方向扩散不是额外耗散，涡量差分优化仍回到经典六次代价，单个 Fourier 壳也可承载全部有符号拉伸。双增量物理环带恒等式随后成立。纯膨胀不能改善全空间比值；R0.69V 严格排除无限尺度分离，却只以 QMC 诊断尺度比四的有限分离。R0.69W 才用外向舍入区间和独立检查严格排除尺度比四的整个闭振幅族。", "The sharp pointwise stretching constant is attained by smooth divergence-free fields; directional diffusion supplies no additional dissipation, vorticity-increment optimization still returns to the classical sixth-power cost, and a single Fourier shell can carry all signed stretching. The two-increment physical-annulus identity then follows. Pure dilation cannot improve the whole-space ratio; R0.69V rigorously excludes infinite scale separation but diagnoses finite separation at scale ratio four only by QMC. Only R0.69W rigorously excludes the entire closed amplitude family at scale ratio four, using outward-rounded intervals and an independent check."],
  ["二十个阶段、93 个节点：从约化递推和动态路线，到 complete-root 账本、target-row participation，再到 arbitrary physical phases 与尖锐 phase-free carrier 尺度。", "Twenty phases and 93 nodes: from reduced recurrences and the dynamic route, through the complete-root ledger and target-row participation, to arbitrary physical phases and sharp phase-free carrier scales."],
  ["范围内闭合", "Closed within scope"],
  ["否", "No"],
  ["回顾截止节点：R0.72C", "Recap endpoint: R0.72C"],
  ["回顾截止时公开笔记：153", "Public notes at the recap endpoint: 153"],
  ["假设或缺口", "Assumption or gap"],
  ["截至 R0.72C，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 93 个节点或 55 个已公开并封存版本解释成对千禧年问题完成了某个比例。", "Through R0.72C, there is no new unconditional continuation criterion, no reduction of the set of all potential singular solutions, and no proof of finite-time breakdown. The 93 nodes or 55 published and archived releases cannot be interpreted as completing some percentage of the Millennium Problem."],
  ["旧实系数公式不能直接把系数改成复数：那会破坏 skew-adjointness。任意物理 Fourier 相位必须把相反位移共轭配对，", "The old real-coefficient formula cannot be complexified by simply replacing its coefficients: doing so destroys skew-adjointness. Arbitrary physical Fourier phases require conjugate pairing of opposite shifts,"],
  ["累计回顾 · R0.61–R0.72C · 2026-08-27", "Cumulative recap · R0.61–R0.72C · 2026-08-27"],
  ["留下的核心缺口不再是静态相位代数本身，而是实际 target-root mass 是否能饱和上界、完整 rotational charge 后是否还有非消失 normalized lower family，以及 changing phase profile 是否有 carrier-count-uniform enhanced dissipation。现有证明全部停留在声明的 finite-carrier triangular 2.5D class。", "The central gap is no longer static phase algebra itself. The open questions are whether the actual target-root mass can saturate the upper bound, whether a nonvanishing normalized lower family survives the full rotational charge, and whether changing phase profiles admit carrier-count-uniform enhanced dissipation. Every current proof remains within the stated finite-carrier triangular 2.5D class."],
  ["六阶零时间谱、仿射提升和完整热核主投影依次被封闭。十阶及以上目标尾在声明的剪切包内可求和。R0.68B-2 当时只完成首热块和数值主 jet，状态仍是“进行中”；R0.68B-2d/e 与 f/g/h 随后补齐导数、主根质量和完整缺陷修正，最终得到一个源锁定的严格负八阶系数。它仍是有限系数定理，不是全空间正则性结论。", "The sixth-order zero-time spectrum, affine lift, and leading full-heat-kernel projection close in sequence. The target tail from order ten onward is summable within the stated shear packet. R0.68B-2 completed only the first heat block and a numerical leading jet and was still marked “in progress”; R0.68B-2d/e and f/g/h later supplied the derivative, leading root mass, and full defect correction, ultimately yielding one strictly negative source-locked eighth-order coefficient. This remains a finite-coefficient theorem, not a whole-space regularity result."],
  ["路线排除", "Route exclusions"],
  ["任何构造都必须同时记录 pre-ledger 与 restarted tail，保留 \\(\\delta\\ne0\\) 的 target-row 量词，并把 algebraic prefactor sharpness、actual root-mass lower bound、normalized ledger saturation 和一般三维 NSE 主张分开。", "Every construction must record both the pre-ledger and restarted tail, retain the target-row quantifier for \\(\\delta\\ne0\\), and separate algebraic-prefactor sharpness, an actual root-mass lower bound, normalized-ledger saturation, and any claim about general three-dimensional NSE."],
  ["任意物理相位的代数逃逸被定量压缩，真正开放的问题转向动力学下界", "Algebraic escape under arbitrary physical phases is quantitatively compressed; the genuinely open question shifts to a dynamical lower bound"],
  ["上一版累计回顾 PDF", "Previous cumulative recap PDF"],
  ["收录节点：93", "Nodes included: 93"],
  ["双涡量增量的有符号物理环带恒等式、固定核心边界载荷的饱和与纯自相似膨胀下全空间比值不变。R0.69V 严格证明两尺度无限分离返回基线，但尺度比四有限分离当时仍是 QMC 诊断；R0.69W 的外向舍入区间证书才严格排除整个闭振幅静态族。", "The signed physical-annulus identity for two vorticity increments, saturation of the fixed-core boundary load, and invariance of the whole-space ratio under pure self-similar dilation are established. R0.69V rigorously proves that infinite two-scale separation returns to the baseline, while finite separation at scale ratio four remained only a QMC diagnostic at that point; the outward-rounded interval certificate in R0.69W is what rigorously excludes the entire closed-amplitude static family."],
  ["条件", "Conditional"],
  ["下面按原编号逐项列出本回顾覆盖的全部节点。状态标签只说明该节的主要证据类型：闭是声明范围内闭合，条件含有明确假设或仍有缺口，否是反例或 no-go，诊断是有限计算或中间节点；标签不表示 Clay 问题完成了多少。", "The complete set of nodes covered by this recap is listed below under the original numbering. A status label identifies only the main evidence type for that note: Closed means closed within the stated scope, Conditional marks an explicit assumption or remaining gap, No marks a counterexample or no-go result, and Diagnostic marks a finite computation or intermediate node. The labels do not measure progress toward the Clay problem."],
  ["下一有限任务需要二选一地形成可审计结果：构造一条 phase-cancelled family，明确 launch data、coupling、observation interval、全部 exact roots 与非消失 normalized lower ledger；或证明使用动力学信息的更强排除定理，把 R0.72C 的静态前因子上界继续压低。", "The next finite task must produce one of two auditable outcomes: construct a phase-cancelled family with explicit launch data, coupling, observation interval, all exact roots, and a nonvanishing normalized lower ledger; or prove a stronger exclusion theorem using dynamical information that further lowers the static-prefactor bound from R0.72C."],
  ["相位相消必须与 participation 联合估计。对互异正整数 carriers 和可比模长，", "Phase cancellation must be estimated jointly with participation. For distinct positive integer carriers with comparable moduli,"],
  ["有限或中间证据", "Finite or intermediate evidence"],
  ["这个算子在角变量中是 \\(-i\\) 乘实剪切，因此能量收缩、目标行范数、\\(q_\\rho\\le3\\) 与 mixed-exposure 常数全部保留。耦合满足 \\(\\delta\\in\\mathbb R\\)：标量零点斜率估计对每个实 \\(\\delta\\) 成立；只有 \\(\\delta\\ne0\\) 时才能除以 \\(\\delta^2\\)，得到 target-row complete-root mass theorem。", "In the angular variable, this operator is \\(-i\\) times a real shear, so energy contraction, the target-row norm, \\(q_\\rho\\le3\\), and the mixed-exposure constant are all retained. The coupling satisfies \\(\\delta\\in\\mathbb R\\): the scalar zero-slope estimate holds for every real \\(\\delta\\); only when \\(\\delta\\ne0\\) can division by \\(\\delta^2\\) yield the target-row complete-root mass theorem."],
  ["这里的“已公开并封存”只指声明范围内可复核", "Here, “published and archived” means auditable only within the stated scope"],
  ["这里的尖锐性只针对完整账本上界中的代数前因子，不是实际根质量下界、normalized ledger 饱和、奇性构造或一般三维 Navier–Stokes 继续性定理。", "Sharpness here concerns only the algebraic prefactor in the complete-ledger upper bound. It is not an actual root-mass lower bound, saturation of the normalized ledger, a singularity construction, or a continuation theorem for general three-dimensional Navier–Stokes."],
  ["这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72C 的 93 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。这里的节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。", "This page follows the R0.00–R0.60 phase recap and organizes the 93 research nodes from R0.61 through R0.72C. I record chronologically what each phase actually proved, which proposal was ruled out by a concrete counterexample or scale analysis, and which assumptions have not been derived from the Navier–Stokes equations. Node statuses describe evidence types; archiving a release is not presented as resolving the phase objective."],
  ["诊断", "Diagnostic"],
  ["exact launch 给 phase-uniform \\(O(M^{-8/3})\\)，Rudin–Shapiro 符号族使这个代数前因子达到同阶，因此不能把 R0.72B 的 coherent \\(M^{-10/3}\\) 统一推广到任意相位。固定正时间 \\(A_*>0\\) 的 tail 为 \\(O(M^{-3})\\)，同相族达到同阶；但正时间 burn-in 不能擦除此前已累计的 nonnegative pre-ledger。", "Exact launch gives the phase-uniform bound \\(O(M^{-8/3})\\), and the Rudin–Shapiro sign family attains the same order for this algebraic prefactor, so the coherent \\(M^{-10/3}\\) result from R0.72B cannot extend uniformly to arbitrary phases. At fixed positive time \\(A_*>0\\), the tail is \\(O(M^{-3})\\), attained to the same order by a phase-aligned family; a positive-time burn-in still cannot erase the nonnegative pre-ledger accumulated earlier."],
  ["R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 93 个节点沿着这个缺口推进；R0.70A–R0.72C 的 55 个版本已经公开并封存，但其中仍包含条件定理、反例、有限诊断和开放缺口。", "The R0.00–R0.60 material remains in the preceding phase recap. R0.60 concluded that the full Fourier–Leray structure and higher-order computations could continue, but the critical quantity for general three-dimensional solutions was still uncontrolled. The next 93 nodes advance along that gap; the 55 releases from R0.70A through R0.72C are published and archived, but they still include conditional theorems, counterexamples, finite diagnostics, and open gaps."],
  ["R0.60 之后的路线分成二十段", "The route after R0.60 is divided into twenty phases"],
  ["R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.72C 的 93 个研究节点；最新一节把 arbitrary physical phases 纳入共轭配对模型，并确定 phase-uniform M^{-8/3} 与正时间 tail M^{-3} 的尖锐代数前因子。", "Research recap after R0.60: 93 research nodes from R0.61 through R0.72C in chronological order; the latest note incorporates arbitrary physical phases through a conjugate-paired model and determines the sharp algebraic prefactors M^{-8/3} for phase-uniform launch and M^{-3} for the positive-time tail."],
  ["R0.61–R0.72C 的 93 节公开笔记", "93 public notes from R0.61–R0.72C"],
  ["R0.61–R0.72C 回顾 · 2026-08-27", "R0.61–R0.72C recap · 2026-08-27"],
  ["R0.61–R0.72C 研究节点", "R0.61–R0.72C research nodes"],
  ["R0.61–R0.72C｜R0.60 之后的研究回顾", "R0.61–R0.72C | Research recap after R0.60"],
  ["R0.68A 的十阶及以上目标尾求和，以及 R0.68B 系列的八阶有限关口。R0.68B-2 是明确标为“进行中”的中间页；d/e 与 f/g/h 才补齐严格导数、主根质量和完整缺陷修正，最终证明一个固定八阶系数严格为负。这些都是源与构造族锁定的系数结论。", "R0.68A sums the target tail from order ten onward, while the R0.68B series treats the finite eighth-order gate. R0.68B-2 is an intermediate page explicitly marked “in progress”; only d/e and f/g/h supply the rigorous derivative, leading root mass, and full defect correction, ultimately proving that one fixed eighth-order coefficient is strictly negative. These coefficient conclusions are locked to their sources and construction families."],
  ["R0.70A 的非显式比例邻域、共同短时连续性与移动标签恒等式；显式比例区间没有认证，诊断 pilot 不能升级为证书。R0.70B–I 随后给出匹配尺度反桥、真实小数据 signed cancellation、固定分辨率负部障碍、Yu remainder 横截性、相邻源伸缩缺陷、核心矩变化与尖锐 \\(s^{-1/2}\\) 时间 Hardy 核；frozen-low sector 闭合，moving-low 与 deviatoric diagonal 仍开放。", "R0.70A gives a non-explicit ratio neighborhood, common short-time continuity, and the moving-label identity; no explicit ratio interval is certified, and the diagnostic pilot cannot be promoted to a certificate. R0.70B–I then gives the matched-scale anti-bridge, genuine small-data signed cancellation, the fixed-resolution negative-part obstruction, Yu-remainder transversality, the adjacent-source dilation defect, core-moment variation, and the sharp temporal Hardy kernel \\(s^{-1/2}\\). The frozen-low sector closes, while the moving-low and deviatoric-diagonal sectors remain open."],
  ["R0.70A 只由比例四的严格余量推出非显式开邻域和共同短时连续性；诊断 pilot 的 \\(3.9<\\rho<4.1\\) 不是认证区间。移动环带标签本身也不会给出边界控制。匹配尺度、动态符号、固定尺度覆盖、单壳奇偶结构、仿射一阶展开、相邻源差分与核心矩变化随后被检查。冻结低频部分可由能量控制；移动低频与偏差对角项仍受临界时间 Hardy 核限制。", "R0.70A derives only a non-explicit open neighborhood and common short-time continuity from the strict margin at ratio four; the diagnostic pilot interval \\(3.9<\\rho<4.1\\) is not certified. A moving annulus label also supplies no boundary control by itself. Matched scales, dynamic signs, fixed-scale coverings, single-shell parity, affine first-order expansion, adjacent-source differences, and core-moment variation are checked afterward. Energy controls the frozen low-frequency part; the moving low frequencies and deviatoric diagonal remain limited by the critical temporal Hardy kernel."],
  ["R0.71U 给出 zero-count-independent all-shell second-time-jet theorem；finite prescribed recurrence 的量词是对每个 \\(N\\) 和给定有限时刻集合另选一条 exact 解，不是一条轨道无限回返。R0.71V 把第一行账本转成 Leray–Hopf right-rooted excursion-height packing，并分离 level integral 与 fixed zero-level atom。R0.71W 排除 data-uniform complete first-row bound，R0.71X 在 fixed-dimensional small-coupling family 内补齐 complete roots 并达到 \\(D^{1/3}\\) endpoint。R0.71Y 证明 bounded observation coupling 下 selected growing-root ratio 至多为 \\(C\\nu^{-2}\\delta_{\\rm obs}^{4/3}/N\\)。R0.71Z 不再计数根：复值 \\(W^{2,1}\\) 函数的 BV 零点斜率引理、实剪切三角系统的 exact contraction 与 dissipative target row 直接控制全部 exact roots 的 squared-slope mass；把付款区间扩到 launch 后，\\(\\mathcal R_Y\\) 又消去逐根 enstrophy floor，给出 \\(C\\nu^{-2}M^{-2}\\delta_{\\rm obs}^{4/3}(1+\\delta_{\\rm obs})\\) 的 complete ratio。bounded coupling 下该量按 \\(M^{-2}\\) 消失；结论只覆盖声明的 triangular class。", "R0.71U gives a zero-count-independent all-shell second-time-jet theorem; finite prescribed recurrence means that, for each \\(N\\) and each prescribed finite set of times, a separate exact solution is chosen, not that one trajectory returns infinitely often. R0.71V converts the first-row ledger into Leray–Hopf right-rooted excursion-height packing and separates the level integral from the fixed zero-level atom. R0.71W rules out a data-uniform complete first-row bound, and R0.71X closes complete roots in a fixed-dimensional small-coupling family and reaches the \\(D^{1/3}\\) endpoint. R0.71Y proves that, under bounded observation coupling, the selected growing-root ratio is at most \\(C\\nu^{-2}\\delta_{\\rm obs}^{4/3}/N\\). R0.71Z no longer counts roots: a BV zero-slope lemma for complex-valued \\(W^{2,1}\\) functions, exact contraction for the real-shear triangular system, and the dissipative target row directly control the squared-slope mass of all exact roots. Extending the payment interval back to launch lets \\(\\mathcal R_Y\\) remove the rootwise enstrophy floor and gives the complete ratio \\(C\\nu^{-2}M^{-2}\\delta_{\\rm obs}^{4/3}(1+\\delta_{\\rm obs})\\). Under bounded coupling, this quantity vanishes as \\(M^{-2}\\); the conclusion covers only the stated triangular class."],
  ["R0.72B 的 \\(M^{-10/3}\\) 是 exact-launch coherent family 的改进率。R0.72C 证明它不能 phase-uniform 保持：任意物理相位在正确的共轭配对模型中仍受 \\(M^{-8/3}\\) 上界，而 Rudin–Shapiro 符号族使这个代数前因子达到同阶。固定正时间的热参与率再把 tail 压到 \\(M^{-3}\\)，但 pre-ledger 仍不可删除。", "The \\(M^{-10/3}\\) rate in R0.72B is an improvement for the exact-launch coherent family. R0.72C proves that it cannot persist phase-uniformly: arbitrary physical phases in the correct conjugate-paired model still satisfy an \\(M^{-8/3}\\) upper bound, and the Rudin–Shapiro sign family attains the same order for this algebraic prefactor. At fixed positive time, heat participation further compresses the tail to \\(M^{-3}\\), but the pre-ledger still cannot be removed."],
  ["R0.72C · 任意物理相位、热参与率与尖锐 phase-free 尺度", "R0.72C · Arbitrary physical phases, heat participation, and sharp phase-free scales"],
  ["R0.72C 的 arbitrary-physical-phase extension：相反位移必须携带 \\(w_l\\) 与 \\(\\overline{w_l}\\)，不能把旧公式直接复系数化。标量 slope estimate 对每个实 \\(\\delta\\) 成立；target-row root-mass theorem 只在 \\(\\delta\\ne0\\) 时成立。联合 participation inequality 给出 exact-launch phase-uniform \\(M^{-8/3}\\) 与固定正时间 tail \\(M^{-3}\\)；Rudin–Shapiro 与同相族分别使这两个代数前因子达到同阶。它们不是 actual root-mass lower bounds，也不触及一般三维正则性。", "R0.72C extends the model to arbitrary physical phases: opposite shifts must carry \\(w_l\\) and \\(\\overline{w_l}\\), rather than directly complexifying the old formula. The scalar slope estimate holds for every real \\(\\delta\\); the target-row root-mass theorem holds only when \\(\\delta\\ne0\\). The joint participation inequality gives the exact-launch phase-uniform scale \\(M^{-8/3}\\) and the fixed-positive-time tail scale \\(M^{-3}\\); the Rudin–Shapiro and phase-aligned families respectively attain these two algebraic prefactors to the same order. They are not actual root-mass lower bounds and do not address general three-dimensional regularity."],
  ["R0.72C 附图", "R0.72C figure"],
  ["R0.72C 证书", "R0.72C certificates"],
  ["R0.72D 转向实际根质量与完整归一化下界", "R0.72D turns to actual root mass and a complete normalized lower bound"],
  ["查看独立检查程序", "View the independent checker"],
  ["从 complete-root 局部暴露走到 physical-phase sharp prefactor 边界", "From complete-root local exposure to the physical-phase sharp-prefactor boundary"],
  ["对任意 physical Fourier coefficients，正确的两侧移位必须写成 \\(w_lF_{r-r_l}+\\overline{w_l}F_{r+r_l}\\)。它对应实值 shear multiplier，因而保留 skew coupling 与能量收缩；把旧的对称移位直接换成复系数会破坏这一结构。精确 target row 仍满足 \\[ \\rho_A^2=2K_z^2\\sum_l|w_l|^2e^{-2\\kappa r_l^2A_0}. \\]", "For arbitrary physical Fourier coefficients, the two shifts must be written as \\(w_lF_{r-r_l}+\\overline{w_l}F_{r+r_l}\\). This form corresponds to a real-valued shear multiplier and therefore preserves skew coupling and energy contraction; directly replacing the old symmetric shifts by complex coefficients destroys that structure. The exact target row still satisfies \\[ \\rho_A^2=2K_z^2\\sum_l|w_l|^2e^{-2\\kappa r_l^2A_0}. \\]"],
  ["共轭配对保留 complete-root 定理，并给出 phase-uniform sharp carrier 尺度", "Conjugate pairing preserves the complete-root theorem and gives the sharp phase-uniform carrier scales"],
  ["环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \\(N^{-1}\\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \\(M^{-2}\\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → phase-uniform \\(M^{-8/3}\\) sharp algebraic prefactor → fixed-positive \\(M^{-3}\\) tail", "annular exclusion → source-kernel ledger → covariance-spectrum stratification → all-frequency conditional bridge → response-slope chord gain → common-response order-one channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment-projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \\(N^{-1}\\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \\(M^{-2}\\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → sharp phase-uniform \\(M^{-8/3}\\) algebraic prefactor → fixed-positive \\(M^{-3}\\) tail"],
  ["检查 Rudin–Shapiro phase cancellation 的 sharp algebraic prefactor 能否由真实 target roots、complete root-slope mass 与 full rotational charge 同时实现；任何 lower family 都必须保留 freezing error 和 pre/tail ledger。", "Test whether the sharp algebraic prefactor from Rudin–Shapiro phase cancellation can be realized simultaneously by actual target roots, complete root-slope mass, and the full rotational charge; every lower family must retain the freezing error and the pre/tail ledger."],
  ["检查 sharp algebraic prefactor 能否进入 actual normalized root ledger；构造必须同时保留真实 target roots、complete slope mass、full rotational charge 与 pre/tail ledger。", "Test whether the sharp algebraic prefactor enters the actual normalized root ledger; a construction must simultaneously retain actual target roots, complete slope mass, the full rotational charge, and the pre/tail ledger."],
  ["检查 sharp algebraic prefactor 能否进入真实 normalized root ledger，而不丢失 full charge 与 pre/tail 分离。", "Test whether the sharp algebraic prefactor enters the actual normalized root ledger without losing the full charge or the pre/tail separation."],
  ["静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71U–Z 依次处理 second-time jet、complete first row、fixed-small-coupling endpoint、selected roots 与 complete roots。R0.72A 把强耦合代价局部化到实际观察层，R0.72B 再以精确 target row 收紧 complete-root 前因子。R0.72C 把任意 physical Fourier phases 写成共轭配对的两侧移位，并联合估计 participation 与 multiplier norm：exact launch 的 phase-uniform algebraic prefactor 为 sharp \\(M^{-8/3}\\)，固定正观察时刻的 tail prefactor 为 sharp \\(M^{-3}\\)。", "After the static annular family is rigorously excluded, the main route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71U–Z treats, in sequence, the second-time jet, the complete first row, the fixed-small-coupling endpoint, selected roots, and complete roots. R0.72A localizes the strong-coupling cost to the actual observation layer, and R0.72B tightens the complete-root prefactor using the exact target row. R0.72C writes arbitrary physical Fourier phases as conjugate-paired opposite shifts and jointly estimates participation and the multiplier norm: at exact launch, the phase-uniform algebraic prefactor has the sharp scale \\(M^{-8/3}\\), while the tail prefactor at a fixed positive observation time has the sharp scale \\(M^{-3}\\)."],
  ["累计回顾 R0.61–R0.72C · 2026-08-27", "Cumulative recap R0.61–R0.72C · 2026-08-27"],
  ["目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.72C 在声明的 finite-carrier triangular 2.5D class 中证明 phase-uniform exact-launch \\(M^{-8/3}\\) sharp algebraic prefactor 与 fixed-positive \\(M^{-3}\\) tail；complete physical-time root ledger 只在 \\(\\delta\\ne0\\) 时陈述。这里没有一般 NSE 正则性结论。", "There is currently no new unconditional continuation criterion and no construction of a finite-time singularity. Within the stated finite-carrier triangular 2.5D class, R0.72C proves a sharp phase-uniform exact-launch algebraic prefactor of \\(M^{-8/3}\\) and a fixed-positive tail of \\(M^{-3}\\); the complete physical-time root ledger is stated only when \\(\\delta\\ne0\\). This is not a general NSE regularity result."],
  ["上次综述 v1.15 · 2026-08-27", "Previous review v1.15 · 2026-08-27"],
  ["我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.72C 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。", "A separate systematic review places classical theory, five main literature strands, the candidate-blowup exclusion tree, progress from 2019–2026, and this site's R0.69P–R0.72C route in one view. The historical R0.61–R0.69O nodes remain in the cumulative recap."],
  ["下一步 R0.72D：", "Next step R0.72D:"],
  ["研究笔记 R0.72C · 2026-08-27", "Research note R0.72C · 2026-08-27"],
  ["阅读 R0.72C 研究笔记 →", "Read research note R0.72C →"],
  ["展开 63 篇公开笔记", "Expand 63 public notes"],
  ["综述 v1.16 · 2026-08-27", "Review v1.16 · 2026-08-27"],
  ["odd-generation Rudin–Shapiro signs 精确实现 \\(\\chi_0=1/4\\) 与 \\(\\Phi_{0,M}\\asymp M^{-8/3}\\)，所以 coherent \\(M^{-10/3}\\) 不能对 phases 一致成立；固定正 \\(A_*\\) 的同号 family 则实现 \\(M^{-3}\\)。这里的 sharpness 只属于显示的 algebraic prefactor，不是 actual root mass、normalized ledger 或 NSE 奇性下界。", "Odd-generation Rudin–Shapiro signs exactly realize \\(\\chi_0=1/4\\) and \\(\\Phi_{0,M}\\asymp M^{-8/3}\\), so coherent \\(M^{-10/3}\\) cannot hold uniformly across phases; at fixed positive \\(A_*\\), a same-sign family realizes \\(M^{-3}\\). This sharpness belongs only to the displayed algebraic prefactor, not to actual root mass, the normalized ledger, or a lower bound for an NSE singularity."],
  ["participation 与 multiplier norm 需要联合估计： \\[ \\chi_A\\left(\\frac{\\Omega_A^2}{K_v}\\right)^{1/3} \\le\\left(\\frac{\\rho_A^2}{K_v}\\right)^{1/3}. \\] 对互异正整数 carriers 与可比模长，若 \\(H_M(A)=\\sum_{j=1}^Me^{-2\\kappa Aj^2}\\)，则 \\[ \\Phi_{A,M}\\le C M^{-3}H_M(A)^{1/3}. \\] exact launch 给 phase-uniform \\(O(M^{-8/3})\\)，固定正 \\(A_*\\) 的 restarted tail 给 \\(O(M^{-3})\\)。", "Participation and the multiplier norm must be estimated jointly: \\[ \\chi_A\\left(\\frac{\\Omega_A^2}{K_v}\\right)^{1/3} \\le\\left(\\frac{\\rho_A^2}{K_v}\\right)^{1/3}. \\] For distinct positive integer carriers with comparable moduli, let \\(H_M(A)=\\sum_{j=1}^Me^{-2\\kappa Aj^2}\\). Then \\[ \\Phi_{A,M}\\le C M^{-3}H_M(A)^{1/3}. \\] Exact launch gives the phase-uniform bound \\(O(M^{-8/3})\\), while the restarted tail at fixed positive \\(A_*\\) gives \\(O(M^{-3})\\)."],
  ["physical phases 必须以共轭配对进入两侧移位；phase-uniform exact-launch algebraic prefactor 的 sharp 尺度是 \\(M^{-8/3}\\)，固定正观察时刻的 tail 尺度是 \\(M^{-3}\\)。", "Physical phases must enter the two shifts as conjugate pairs; the sharp scale of the phase-uniform exact-launch algebraic prefactor is \\(M^{-8/3}\\), and the fixed-positive-observation-time tail scale is \\(M^{-3}\\)."],
  ["R0.60 之后的累计回顾按二十个阶段组织。R0.61–R0.69O 保留约化递推、剪切边界、横向扰动与压力局部预算；R0.69P–R0.71T 依次检查静态环带、协方差谱、projected-Lamb heat、faces、incidence 与真实内部 entry；R0.71U–R0.71Z 处理 second-time jet、complete first row 与全部根边界；R0.72A–C 依次给出 local exposure、target-row participation 与 physical-phase sharp prefactor。R0.70A–R0.72C 共 55 个已公开并封存版本。", "The cumulative recap after R0.60 is organized into twenty phases. R0.61–R0.69O retains reduced recurrences, shear boundaries, transverse perturbations, and local pressure budgets; R0.69P–R0.71T examines, in sequence, static annuli, covariance spectra, projected-Lamb heat, faces, incidence, and genuine internal entry; R0.71U–R0.71Z treats the second-time jet, the complete first row, and the all-root boundary; R0.72A–C gives, in sequence, local exposure, target-row participation, and the physical-phase sharp prefactor. R0.70A–R0.72C contains 55 published and archived releases."],
  ["R0.60 recap 之后的累计回顾收录 93 个节点；全站现有 153 篇公开研究笔记", "The cumulative recap after the R0.60 recap contains 93 nodes; the full site now has 153 public research notes"],
  ["R0.70A–R0.72C 已公开并封存版本", "R0.70A–R0.72C published and archived releases"],
  ["R0.72C 已完成：", "R0.72C completed:"],
  ["scalar root-slope estimate 对所有实 \\(\\delta\\) 成立，complete physical-time root ledger 只在 \\(\\delta\\ne0\\) 时陈述。正 burn-in 只能改善 restart 后的 tail，不能删除此前累积的 nonnegative pre-ledger。本节没有给出一般三维 Navier–Stokes 继续性或奇性结论。", "The scalar root-slope estimate holds for every real \\(\\delta\\), while the complete physical-time root ledger is stated only when \\(\\delta\\ne0\\). A positive burn-in can improve only the tail after restart; it cannot remove the nonnegative pre-ledger accumulated earlier. This note gives no continuation result or singularity result for general three-dimensional Navier–Stokes."],
];

const translations = JSON.parse(await readFile(translationsPath, "utf8"));

// R0.72B briefly translated an obsolete, malformed source string before the
// TeX delimiters were corrected. Keep that stale entry for provenance while
// assigning it a unique legacy ID.
const malformedR072b = translations.find(
  (entry) =>
    entry.zh ===
    "Bessel 诊断在 (R=512) 时给 (Theta_R=7.890686\\times10^{-5})、(Xi_R=9.429778\\times10^{-6})，analytic energy-loss upper bound 为",
);
if (
  malformedR072b?.id === "r072b140" &&
  !translations.some((entry) => entry.id === "r072b142")
) {
  malformedR072b.id = "r072b142";
}

const source = await collectSiteStrings(publicDirectory);
const sourceByChinese = new Map(source.map((entry) => [entry.zh, entry]));
const existing = new Set(translations.map((entry) => entry.zh));
const mapped = new Map(rows);
const duplicateKeys = rows
  .map(([zh]) => zh)
  .filter((zh, index, values) => values.indexOf(zh) !== index);
if (duplicateKeys.length) {
  throw new Error(`Duplicate mapping keys: ${duplicateKeys.join(" | ")}`);
}

const missing = source.filter((entry) => !existing.has(entry.zh));
const unmapped = missing.filter((entry) => !mapped.has(entry.zh));
if (unmapped.length) {
  throw new Error(
    `R0.72C translation source drift (${unmapped.length} unmapped live strings):\n${unmapped
      .map((entry) => entry.zh)
      .join("\n---\n")}`,
  );
}

for (const [zh, en] of rows) {
  if (!sourceByChinese.has(zh) || existing.has(zh)) continue;
  if (!en.trim() || containsChinese(en)) {
    throw new Error(`Invalid English translation for: ${zh}`);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error(`Collective English voice remains in: ${zh}`);
  }
  const zhTokens = extractProtectedTokens(zh);
  const enTokens = extractProtectedTokens(en);
  if (JSON.stringify(zhTokens) !== JSON.stringify(enTokens)) {
    throw new Error(
      `Protected-token mismatch for:\n${zh}\nZH ${JSON.stringify(zhTokens)}\nEN ${JSON.stringify(enTokens)}`,
    );
  }
}

let added = 0;
for (const [index, [zh, en]] of rows.entries()) {
  const live = sourceByChinese.get(zh);
  if (!live || existing.has(zh)) continue;
  translations.push({
    ...live,
    id: `r072c${String(index + 1).padStart(3, "0")}`,
    en,
  });
  existing.add(zh);
  added += 1;
}

for (const field of ["id", "zh"]) {
  const seen = new Set();
  const duplicates = translations
    .map((entry) => entry[field])
    .filter((value) => seen.size === seen.add(value).size);
  if (duplicates.length) {
    throw new Error(`Duplicate ${field} values: ${[...new Set(duplicates)].join(" | ")}`);
  }
}

await writeFile(translationsPath, `${JSON.stringify(translations, null, 2)}\n`);
console.log(
  JSON.stringify(
    {
      mapped: rows.length,
      liveMissing: missing.length,
      added,
      duplicateIds: 0,
      duplicateChineseKeys: 0,
    },
    null,
    2,
  ),
);
