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
const snapshotPath = resolve(
  projectRoot,
  ".i18n-work",
  "r072e-missing.json",
);

const raw = String.raw;
const rows = [
  [
    "r072e001",
    raw`打开 95 节完整索引`,
    raw`Open the complete 95-note index`,
  ],
  [
    "r072e002",
    raw`的 Corollary (3.25) 与 inequality (3.27) 取得小时间多项式密度界。驻相、负矩和时间积分随后给 \(Q_{\delta,q_0}\lesssim(1+\log(2+\delta))/\delta\)。`,
    raw`Corollary (3.25) and inequality (3.27) yield a polynomial small-time density bound. Stationary phase, a negative moment, and time integration then give \(Q_{\delta,q_0}\lesssim(1+\log(2+\delta))/\delta\).`,
  ],
  [
    "r072e003",
    raw`固定 \(q_0>R_*\) 隔离 target shell。Feynman–Kac、固定相位驻相与定量 Hörmander density 给 \(Q_{\delta,q_0}\lesssim\log(2+\delta)/\delta\)；取 \(\delta_R=R^4\) 后，full-frequency charge 有界而 normalized complete-root ledger 至少按 \(R^{4/3}\) 发散。所有解仍全局光滑。`,
    raw`Fixing \(q_0>R_*\) isolates the target shell. Feynman–Kac, fixed-phase stationary phase, and a quantitative Hörmander density bound give \(Q_{\delta,q_0}\lesssim\log(2+\delta)/\delta\). With \(\delta_R=R^4\), the full-frequency charge stays bounded while the normalized complete-root ledger diverges at least as \(R^{4/3}\). Every solution remains globally smooth.`,
  ],
  [
    "r072e004",
    raw`候选修正必须先阻断 R0.72E exact family，再证明它能由 Leray 级或已知 continuation budget 支付。`,
    raw`A candidate repair must first block the R0.72E exact family and then be shown payable by Leray-level information or a known continuation budget.`,
  ],
  [
    "r072e005",
    raw`仅有 smooth density 不能推出所需负矩；这里使用 Part II 的定量 polynomial bound，并通过 lifted terminal-angle 权重取得二维边缘密度。Part III 的相关 density section 有零漂移限制，不是本节依据。DLMF 不提供非自治 action，Kusuoka–Stroock 也不提供 Bessel roots、NSE amplitude ledger 或 candidate-payment no-go。当前结果排除的是本站声明的 \(D^{1/3}\Lambda_1\) complete-root 中间估计，不作绝对原创性、优先权、奇性或一般正则性声明。`,
    raw`A smooth density alone does not imply the required negative moment. The argument uses the quantitative polynomial bound in Part II and obtains a two-dimensional marginal density by integrating the lifted terminal-angle weight. The relevant density section in Part III assumes zero drift and is not used here. DLMF does not provide the nonautonomous action estimate, while Kusuoka–Stroock provides neither Bessel roots, an NSE amplitude ledger, nor a candidate-payment no-go result. The present result excludes only the stated \(D^{1/3}\Lambda_1\) complete-root intermediate estimate; it makes no absolute claim of novelty, priority, singularity, or general regularity.`,
  ],
  [
    "r072e006",
    raw`开放接口 · R0.72F`,
    raw`Open interface · R0.72F`,
  ],
  [
    "r072e007",
    raw`累计回顾与 95 节索引`,
    raw`Cumulative recap and 95-note index`,
  ],
  [
    "r072e008",
    raw`提供 Jacobi–Anger 展开、Bessel zeros 与导数渐近；它只负责 frozen root ledger。新的 action 证明把角 Brownian motion 提升到 \(dZ=(-Z+e^{iB})dt\)，再用`,
    raw`provides the Jacobi–Anger expansion, Bessel zeros, and derivative asymptotics; it supports only the frozen root ledger. The new action proof lifts angular Brownian motion to \(dZ=(-Z+e^{iB})dt\), then uses`,
  ],
  [
    "r072e009",
    raw`文献综述 v1.18 · 2026-08-27`,
    raw`Literature review v1.18 · 2026-08-27`,
  ],
  [
    "r072e010",
    raw`我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.72E 只列为研究笔记。我不把计算或笔记外推成正则性定理。`,
    raw`Published theorems are listed as known results, 2026 preprints are marked separately, and R0.69P–R0.72E on this site are listed only as research notes. Computations and notes are not extrapolated into regularity theorems.`,
  ],
  [
    "r072e011",
    raw`中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–U 给出 conditional incidence、genuine internal-entry、second-time-jet 与 finite recurrence 边界。R0.71V–W 分离 fixed zero-level trace 并排除 data-uniform complete first-row ledger。R0.71X 在 fixed-dimensional small-coupling family 内达到 one-third endpoint；R0.71Y 处理 selected roots；R0.71Z 给出 all-root slope-mass bound 和 launch-inclusive floor cancellation；R0.72A 把 strong-coupling loss 局部化到实际观察层，R0.72B 保留 exact target-row participation，R0.72C 得到 phase-uniform exact-launch \(M^{-8/3}\) 与 fixed-positive tail \(M^{-3}\) 的 sharp algebraic scales。R0.72D 在 shifted Rudin–Shapiro family 上构造 positive-time exact root，保留 full rotational charge，并得到非消失但不发散的 normalized complete-root ledger。R0.72E 回到 fixed-carrier Bessel family，以定量 negative-Sobolev action 证明 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。一般 Navier–Stokes 正则性仍开放。`,
    raw`. R0.69P–R0.71P reaches the positive-entry temporal-packing boundary; R0.71Q–U establishes the boundaries for conditional incidence, genuine internal entries, the second-time jet, and finite recurrence. R0.71V–W separates the fixed zero-level trace and excludes a data-uniform complete first-row ledger. R0.71X reaches the one-third endpoint in a fixed-dimensional small-coupling family; R0.71Y treats selected roots; R0.71Z gives an all-root slope-mass bound and launch-inclusive floor cancellation. R0.72A localizes the strong-coupling loss to the actual observation layer, R0.72B retains exact target-row participation, and R0.72C obtains the sharp phase-uniform exact-launch \(M^{-8/3}\) and fixed-positive-tail \(M^{-3}\) algebraic scales. R0.72D constructs a positive-time exact root in a shifted Rudin–Shapiro family, retains the full rotational charge, and obtains a nonvanishing but nondivergent normalized complete-root ledger. R0.72E returns to a fixed-carrier Bessel family and uses a quantitative negative-Sobolev action estimate to make the complete-root ledger relative to the candidate \(D^{1/3}\Lambda_1\) payment diverge as \(R^{4/3}\). General Navier–Stokes regularity remains open.`,
  ],
  [
    "r072e012",
    raw`fixed-carrier Bessel family 排除候选 \(D^{1/3}\Lambda_1\) payment`,
    raw`A fixed-carrier Bessel family excludes the candidate \(D^{1/3}\Lambda_1\) payment`,
  ],
  [
    "r072e013",
    raw`R0.72E 的 kinetic density、Bessel 根与主张边界`,
    raw`R0.72E kinetic density, Bessel roots, and claim boundary`,
  ],
  [
    "r072e014",
    raw`R0.72E 的主源边界`,
    raw`R0.72E primary-source boundary`,
  ],
  [
    "r072e015",
    raw`R0.72E 固定整数 \(q_0>R_*\)，因此 \(A_q=q_0^{-2}-\partial_\theta^2\) 的零模权重只进入常数。`,
    raw`R0.72E fixes an integer \(q_0>R_*\), so the zero-mode weight in \(A_q=q_0^{-2}-\partial_\theta^2\) enters only through the constant.`,
  ],
  [
    "r072e016",
    raw`\(H^{-1}\) 权重、时间 Jacobian 和 shear-enstrophy denominator 各贡献 \(q_0^{-2}\)，故`,
    raw`The \(H^{-1}\) weight, time Jacobian, and shear-enstrophy denominator each contribute \(q_0^{-2}\), hence`,
  ],
  [
    "r072e017",
    raw`01 · 精确三角形解`,
    raw`01 · Exact triangular solution`,
  ],
  [
    "r072e018",
    raw`02 · Bessel 根族`,
    raw`02 · Bessel root family`,
  ],
  [
    "r072e019",
    raw`03 · 负 Sobolev action`,
    raw`03 · Negative-Sobolev action`,
  ],
  [
    "r072e020",
    raw`04 · 完整物理账本`,
    raw`04 · Complete physical ledger`,
  ],
  [
    "r072e021",
    raw`05 · 正进入与发散`,
    raw`05 · Positive entries and divergence`,
  ],
  [
    "r072e022",
    raw`版本 v0.72E · 2026-08-27`,
    raw`Version v0.72E · 2026-08-27`,
  ],
  [
    "r072e023",
    raw`不导入 producer，独立 action 窗口固定为 \(X=1\)：\(Q_{16}=1.326217539\)、\(Q_{128}=0.307998939\)。\(R=64\) root mass 为 \(3.565301087\)，相对 frozen 值偏差 \(-4.71\times10^{-6}\)。`,
    raw`The independent audit does not import the producer and fixes the action window at \(X=1\): \(Q_{16}=1.326217539\) and \(Q_{128}=0.307998939\). At \(R=64\), the root mass is \(3.565301087\), with relative deviation \(-4.71\times10^{-6}\) from the frozen value.`,
  ],
  [
    "r072e024",
    raw`从 R0.71X 到 R0.72D，\(D^{1/3}\Lambda_1\) 一直是 complete-root ledger 的候选支付。当前家族把 exact roots、真实数据、固定物理区间、enstrophy contrast 和 full-frequency charge 放进同一个光滑 NSE 解中，仍使比值发散。因此继续证明这一候选估计已经没有意义。`,
    raw`From R0.71X through R0.72D, \(D^{1/3}\Lambda_1\) remained the candidate payment for the complete-root ledger. The present family places exact roots, genuine data, a fixed physical interval, enstrophy contrast, and the full-frequency charge in one smooth NSE solution, yet the ratio still diverges. Pursuing a proof of this candidate estimate is therefore no longer meaningful.`,
  ],
  [
    "r072e025",
    raw`对千禧年问题的价值仍是间接的：我排除了一座可能的桥，没有得到 continuation criterion。反例就在全局光滑不变子类中，也说明 raw zero-crossing ledger 可能比正则性所需的量更强。`,
    raw`The value for the Millennium Problem remains indirect: one possible bridge is excluded, but no continuation criterion is obtained. The counterexample lies inside a globally smooth invariant subclass, also indicating that the raw zero-crossing ledger may be stronger than regularity requires.`,
  ],
  [
    "r072e026",
    raw`该家族没有爆破；它反而始终光滑。结论说明候选 \(D^{1/3}\Lambda_1\) complete-root 中间估计不能再作为一般证明的桥，但不排除加入新频率项、初始层费用或更强数据因子的替代估计。`,
    raw`This family does not blow up; it remains smooth for all time. The result shows that the candidate \(D^{1/3}\Lambda_1\) complete-root intermediate estimate cannot serve as a bridge in a general proof, but it does not exclude a replacement with a new frequency term, an initial-layer cost, or a stronger data factor.`,
  ],
  [
    "r072e027",
    raw`根族`,
    raw`Root family`,
  ],
  [
    "r072e028",
    raw`固定 \(q_0\) 不会改变根：精确标量共轭`,
    raw`Fixing \(q_0\) leaves the roots unchanged: exact scalar conjugacy`,
  ],
  [
    "r072e029",
    raw`固定 \(q_0\) 同时保留精确演化与目标壳隔离`,
    raw`A fixed \(q_0\) retains exact evolution and target-shell isolation`,
  ],
  [
    "r072e030",
    raw`固定相位驻相给 \(A_q^{-1}\) norm square \(\lesssim(1+\kappa)^{-1}\)。过程 \(dB=\sqrt2dW\)、\(dZ=(-Z+e^{iB})dt\) 的两个漂移括号在每一点都张成两个 \(Z\) 方向；它们与噪声场组成的绝对行列式恒为 \(4\)。Kusuoka–Stroock Part II 的定量密度界和 Brownian 反射原理给 \(\mathbb E|Z_t|^{-1}\le C_X/t\)，所以`,
    raw`Fixed-phase stationary phase bounds the squared \(A_q^{-1}\) norm by \(\lesssim(1+\kappa)^{-1}\). For \(dB=\sqrt2dW\) and \(dZ=(-Z+e^{iB})dt\), the two drift brackets uniformly span the two \(Z\) directions at every point; together with the noise field, they have absolute determinant \(4\). The quantitative density bound of Kusuoka–Stroock Part II and the Brownian reflection principle give \(\mathbb E|Z_t|^{-1}\le C_X/t\), hence`,
  ],
  [
    "r072e031",
    raw`候选 \(D^{1/3}\Lambda_1\) 支付在精确光滑子类中失败`,
    raw`The candidate \(D^{1/3}\Lambda_1\) payment fails in an exact smooth subclass`,
  ],
  [
    "r072e032",
    raw`候选 \(D^{1/3}\Lambda_1\) payment 被排除`,
    raw`The candidate \(D^{1/3}\Lambda_1\) payment is excluded`,
  ],
  [
    "r072e033",
    raw`交替 crossing sign 不会损失一半根`,
    raw`Alternating crossing signs do not discard half the roots`,
  ],
  [
    "r072e034",
    raw`结合 \(D_R^{1/3}\asymp\delta_R^{2/3}\) 与 bounded \(\Lambda_1\)，得到 \(\delta_R^{1/3}=R^{4/3}\) 发散。`,
    raw`Combining \(D_R^{1/3}\asymp\delta_R^{2/3}\) with bounded \(\Lambda_1\) gives divergence at \(\delta_R^{1/3}=R^{4/3}\).`,
  ],
  [
    "r072e035",
    raw`解析证明、producer 和独立 checker 分开承担责任`,
    raw`The analytic proof, producer, and independent checker have distinct roles`,
  ],
  [
    "r072e036",
    raw`仅有 smooth density 不够；这里需要小时间多项式上界。常数也不对 \(q_0\to\infty\) 一致，所以 \(q_0\) 必须固定。`,
    raw`A smooth density alone is insufficient; a polynomial small-time bound is required. The constant is also not uniform as \(q_0\to\infty\), so \(q_0\) must remain fixed.`,
  ],
  [
    "r072e037",
    raw`两个 action 数列属于不同的 \(X\) 窗口，不能逐项互比。有限计算只核对符号、归一化和代表性截断；无限格根证明、驻相、Malliavin 密度与 \(R\to\infty\) 结论由解析报告承担。`,
    raw`The two action sequences use different \(X\) windows and cannot be compared term by term. Finite computations check only signs, normalizations, and representative truncations; the analytic report carries the infinite-lattice root proof, stationary phase, the Malliavin density argument, and the \(R\to\infty\) conclusion.`,
  ],
  [
    "r072e038",
    raw`令 \(\delta_R=R^4\)、\(U_R(\tau)=F_R(\tau/\delta_R)\)。冻结系统的目标坐标是 \(P_0W(\tau)=J_1(2\tau)\)。增长窗口上的 \(C^1\) 比较误差为 \(O_{q_0}(R^{-1})\)，小于最弱 Bessel slope 的 \(R^{-1/2}\)。因此`,
    raw`Set \(\delta_R=R^4\) and \(U_R(\tau)=F_R(\tau/\delta_R)\). The target coordinate of the frozen system is \(P_0W(\tau)=J_1(2\tau)\). On the growing window, the \(C^1\) comparison error is \(O_{q_0}(R^{-1})\), smaller than the weakest Bessel slope \(R^{-1/2}\). Therefore`,
  ],
  [
    "r072e039",
    raw`令 \(A_q=q_0^{-2}-\partial_\theta^2\) 和 \(Q_{\delta,q_0}(X)=\int_0^X\|V(x)\phi(x)\|_{A_q^{-1}}^2dx\)。 对 \(B_t=\sqrt2W_t\)、\(Z_t=\int_0^te^{-(t-s)}e^{iB_s}ds\)，正确的反向时间公式是`,
    raw`Let \(A_q=q_0^{-2}-\partial_\theta^2\) and \(Q_{\delta,q_0}(X)=\int_0^X\|V(x)\phi(x)\|_{A_q^{-1}}^2dx\). For \(B_t=\sqrt2W_t\) and \(Z_t=\int_0^te^{-(t-s)}e^{iB_s}ds\), the correct reverse-time formula is`,
  ],
  [
    "r072e040",
    raw`每个 \(u_R\) 都是无外力、全局光滑的三维 Navier–Stokes 解，属于 \(u=(f(y,z,t),0,v(y,t))\) 的精确三角形 2.5D 子类。这个定理严格排除的是 complete-root 账本的候选中间估计，不是正则性本身。`,
    raw`Each \(u_R\) is an unforced, globally smooth three-dimensional Navier–Stokes solution in \(u=(f(y,z,t),0,v(y,t))\), the exact triangular 2.5D subclass. The theorem excludes a candidate intermediate estimate for the complete-root ledger, not regularity itself.`,
  ],
  [
    "r072e041",
    raw`能量收缩与一阶矩屏障给 \(D_R\asymp_{q_0}\delta_R^2\) 和 \(\mathcal R_Y([0,T])=O_{T,q_0}(1)\)，不需要额外背景。完整 projected Lamb field 满足`,
    raw`Energy contraction and the first-moment barrier give \(D_R\asymp_{q_0}\delta_R^2\) and \(\mathcal R_Y([0,T])=O_{T,q_0}(1)\), with no auxiliary background. The complete projected Lamb field satisfies`,
  ],
  [
    "r072e042",
    raw`前 \(R\) 个根在 \(O(R^{-3})\) 初始层内保持简单`,
    raw`The first \(R\) roots remain simple inside an \(O(R^{-3})\) initial layer`,
  ],
  [
    "r072e043",
    raw`取 \(F_R(0)=ie_{-1}\)、\(P_R=q_0^2\delta_R\)。所有 \(r\ne0\) active modes 和剪切模都在固定 target multiplier 之外；壳内只剩 \(\pm(0,0,1)\)。这修复了 \(q=1\) 时 radial annulus 无法隔离目标的问题。`,
    raw`Take \(F_R(0)=ie_{-1}\) and \(P_R=q_0^2\delta_R\). Every active mode with \(r\ne0\), together with the shear modes, lies outside the fixed target multiplier; only \(\pm(0,0,1)\) remains in the shell. This repairs the failure of a radial annulus to isolate the target when \(q=1\).`,
  ],
  [
    "r072e044",
    raw`声明子类内的 \(\mathcal J_{\rm all}\le CD^{1/3}\Lambda_1\)，其中 \(C\) 与光滑初值无关。`,
    raw`Within the stated subclass, \(\mathcal J_{\rm all}\le CD^{1/3}\Lambda_1\) with \(C\) independent of the smooth initial data.`,
  ],
  [
    "r072e045",
    raw`所有 \(q_0\) 因子和全部 Lamb 频率都进入账本`,
    raw`Every \(q_0\) factor and every Lamb frequency enters the ledger`,
  ],
  [
    "r072e046",
    raw`图 R0.72E-1。有限截断展示 selected slope mass 的对数增长、负 Sobolev action 的衰减和最终 \(R^{4/3}\) 标度。数值曲线只作有限审计；极限结论来自解析定理。`,
    raw`Figure R0.72E-1. Finite truncations show logarithmic growth of the selected slope mass, decay of the negative-Sobolev action, and the final \(R^{4/3}\) scaling. The numerical curves provide only a finite audit; the limiting conclusion follows from the analytic theorem.`,
  ],
  [
    "r072e047",
    raw`完整 target shell 的每个根都满足 \(C_{*,t}=-\Delta F_*\) 和 \(\langle F_*,C_{*,t}\rangle=\|\nabla F_*\|_2^2>0\)。 因此全部 \(R\) 个根都是 positive right entries。求和给`,
    raw`Every root in the complete target shell satisfies \(C_{*,t}=-\Delta F_*\) and \(\langle F_*,C_{*,t}\rangle=\|\nabla F_*\|_2^2>0\). Hence all \(R\) roots are positive right entries. Summation gives`,
  ],
  [
    "r072e048",
    raw`我会依次测试 frequency-sensitive initial-layer charge、time-weighted rotational action 和直接记录 coupling scale 的数据项。候选先要阻断当前 exact family，再检查是否仍由 Leray 级信息支付；若它已经等价于未知临界范数，就停止该路线。`,
    raw`The next tests will examine a frequency-sensitive initial-layer charge, a time-weighted rotational action, and a data term that records the coupling scale directly. A candidate must first block the present exact family and then remain payable by Leray-level information; the route stops if the candidate is already equivalent to an unknown critical norm.`,
  ],
  [
    "r072e049",
    raw`我取 \(\nu=d=K_z=r_1=1\)、\(K_y=0\)，并固定整数 \(q_0>R_*\)。剪切和正 \(K_z\) sector 写成`,
    raw`Set \(\nu=d=K_z=r_1=1\) and \(K_y=0\), and fix an integer \(q_0>R_*\). The shear and positive-\(K_z\) sector take the form`,
  ],
  [
    "r072e050",
    raw`我选择 \(\delta_R=R^4\)、\(P_R=q_0^2\delta_R\)、\(S_R^2=\delta_R/\log(2+\delta_R)\)。精确数据和涡量分解为`,
    raw`Choose \(\delta_R=R^4\), \(P_R=q_0^2\delta_R\), and \(S_R^2=\delta_R/\log(2+\delta_R)\). The exact data and enstrophy decompose as`,
  ],
  [
    "r072e051",
    raw`物理账本`,
    raw`Physical ledger`,
  ],
  [
    "r072e052",
    raw`下一对象：frequency-sensitive repair`,
    raw`Next object: frequency-sensitive repair`,
  ],
  [
    "r072e053",
    raw`研究笔记 R0.72E · ONE CARRIER · FULL H⁻¹ ACTION · PAYMENT FAILURE`,
    raw`Research note R0.72E · ONE CARRIER · FULL H⁻¹ ACTION · PAYMENT FAILURE`,
  ],
  [
    "r072e054",
    raw`研究笔记 R0.72E：精确单载波三角形 NSE 家族在完整负 Sobolev 旋转电荷有界时，使 complete-root ledger 相对 D^{1/3}Λ₁ 以 R^{4/3} 发散。`,
    raw`Research note R0.72E: an exact one-carrier triangular NSE family makes the complete-root ledger relative to D^{1/3}Λ₁ diverge as R^{4/3} while the complete negative-Sobolev rotational charge remains bounded.`,
  ],
  [
    "r072e055",
    raw`一个载波已经足够：`,
    raw`One carrier is enough:`,
  ],
  [
    "r072e056",
    raw`一条候选证明路线被真正关闭`,
    raw`A candidate proof route is genuinely closed`,
  ],
  [
    "r072e057",
    raw`有限时奇性、一般三维 global regularity、continuation criterion、原创性或优先权结论。`,
    raw`a finite-time singularity, general three-dimensional global regularity, a continuation criterion, or a claim of novelty or priority.`,
  ],
  [
    "r072e058",
    raw`这是 full-frequency charge，不是 selected-shell proxy。`,
    raw`This is the full-frequency charge, not a selected-shell proxy.`,
  ],
  [
    "r072e059",
    raw`这些都是固定物理区间 \([0,T]\) 内的正时间内点；我没有把 launch endpoint 算入这 \(R\) 个根。`,
    raw`All are positive-time interior points in the fixed physical interval \([0,T]\); the launch endpoint is not counted among these \(R\) roots.`,
  ],
  [
    "r072e060",
    raw`正进入`,
    raw`Positive entries`,
  ],
  [
    "r072e061",
    raw`正式附图分开显示根质量、作用量和最终发散`,
    raw`The formal figure separates root mass, action, and final divergence`,
  ],
  [
    "r072e062",
    raw`证明、文献边界、证书、正式附图和累计回顾完整保留`,
    raw`The proof, literature boundary, certificates, formal figure, and cumulative recap are preserved in full`,
  ],
  [
    "r072e063",
    raw`状态 · R0.72E 完成`,
    raw`Status · R0.72E complete`,
  ],
  [
    "r072e064",
    raw`作用量`,
    raw`Action`,
  ],
  [
    "r072e065",
    raw`Feynman–Kac 把完整 \(H^{-1}\) 作用量化成二维小球问题`,
    raw`Feynman–Kac reduces the complete \(H^{-1}\) action to a two-dimensional small-ball problem`,
  ],
  [
    "r072e066",
    raw`Feynman–Kac、驻相和定量 Hörmander 密度给出完整 H^{-1} action；精确 Bessel 根族使候选归一化支付发散。`,
    raw`Feynman–Kac, stationary phase, and a quantitative Hörmander density bound control the complete H^{-1} action; an exact Bessel root family makes the candidate normalized payment diverge.`,
  ],
  [
    "r072e067",
    raw`fixed-\(q_0\) Bessel 根、定量 \(A_q^{-1}\) action decay、完整数据与 enstrophy、full-frequency charge 有界、normalized ledger 发散。`,
    raw`fixed-\(q_0\) Bessel roots, quantitative \(A_q^{-1}\) action decay, complete data and enstrophy, bounded full-frequency charge, and a divergent normalized ledger.`,
  ],
  [
    "r072e068",
    raw`Fourier split-step；action 窗口固定为 \(X=6\)。有限值为 \(Q_{16}=1.329601902\)、\(Q_{512}=0.097737613\)。同时重算 fixed-\(q_0\) Bessel roots、selected slope mass、first-moment barrier 和指数账本。`,
    raw`Fourier split-step; the action window is fixed at \(X=6\). The finite values are \(Q_{16}=1.329601902\) and \(Q_{512}=0.097737613\). The audit also recomputes the fixed-\(q_0\) Bessel roots, selected slope mass, first-moment barrier, and exponent ledger.`,
  ],
  [
    "r072e069",
    raw`frequency-sensitive 修正、一般三维 critical-norm bridge、非三角形动力学中的对应结构。`,
    raw`a frequency-sensitive repair, a general three-dimensional critical-norm bridge, and the corresponding structure in nontriangular dynamics.`,
  ],
  [
    "r072e070",
    raw`R0.72D 只把归一化 complete-root ledger 推到常数量级。我回到 R0.72A 的单载波 Bessel 家族，固定一个能隔离目标壳的整数 \(q_0\)，再直接估计全部 Fourier 模的负 Sobolev 旋转电荷。Feynman–Kac、驻相和定量漂移括号密度给出 \(Q_{\delta,q_0}=O(\log\delta/\delta)\)。取 \(\delta_R=R^4\) 后，完整 charge 保持有界，而 \(R\) 个正时间根使候选归一化比值按 \(R^{4/3}\) 发散。`,
    raw`R0.72D brought the normalized complete-root ledger only to order one. The analysis returns to the one-carrier Bessel family of R0.72A, fixes an integer \(q_0\) that isolates the target shell, and directly estimates the negative-Sobolev rotational charge over all Fourier modes. Feynman–Kac, stationary phase, and a quantitative drift-bracket density bound give \(Q_{\delta,q_0}=O(\log\delta/\delta)\). With \(\delta_R=R^4\), the complete charge remains bounded while \(R\) positive-time roots make the candidate normalized ratio diverge as \(R^{4/3}\).`,
  ],
  [
    "r072e071",
    raw`R0.72E · 2026-08-27 · 个人数学研究日志`,
    raw`R0.72E · 2026-08-27 · Personal mathematics research log`,
  ],
  [
    "r072e072",
    raw`R0.72E｜单载波超临界根账本与候选 D^{1/3}Λ₁ payment 失效`,
    raw`R0.72E | One-carrier supercritical root ledger and failure of the candidate D^{1/3}Λ₁ payment`,
  ],
  [
    "r072e073",
    raw`01 · 二十二个研究阶段`,
    raw`01 · Twenty-two research phases`,
  ],
  [
    "r072e074",
    raw`02 · 95 节完整索引`,
    raw`02 · Complete 95-note index`,
  ],
  [
    "r072e075",
    raw`保留 R0.72D 历史回顾`,
    raw`Retain the historical R0.72D recap`,
  ],
  [
    "r072e076",
    raw`查看 R0.72E 双路证书`,
    raw`View the R0.72E dual-path certificates`,
  ],
  [
    "r072e077",
    raw`打开最新节点 R0.72E`,
    raw`Open the latest node R0.72E`,
  ],
  [
    "r072e078",
    raw`二十二个阶段、95 个节点：从约化递推和 complete-root 账本，到 full-charge saturation，再到候选 D^{1/3}Λ₁ payment 的严格失效。`,
    raw`Twenty-two phases and 95 nodes: from reduced recurrences and the complete-root ledger, through full-charge saturation, to rigorous failure of the candidate D^{1/3}Λ₁ payment.`,
  ],
  [
    "r072e079",
    raw`固定整数 \(q_0>R_*\) 后，单载波 Bessel family 同时获得 target-shell isolation 与 exact diagonal conjugacy。前 \(R\) 个正时间简单根落在 \(O(R^{-3})\) 初始层，selected target-row mass 为 \((8/\pi^2)\log R+O(1)\)。`,
    raw`After fixing an integer \(q_0>R_*\), the one-carrier Bessel family has both target-shell isolation and exact diagonal conjugacy. The first \(R\) simple positive-time roots lie in an \(O(R^{-3})\) initial layer, and the selected target-row mass is \((8/\pi^2)\log R+O(1)\).`,
  ],
  [
    "r072e080",
    raw`候选 \(D^{1/3}\Lambda_1\) payment 已被严格排除，但千禧年问题没有因此前进一个“百分比”`,
    raw`The candidate \(D^{1/3}\Lambda_1\) payment is rigorously excluded, but this does not complete any percentage of the Millennium Problem`,
  ],
  [
    "r072e081",
    raw`回顾截止节点：R0.72E`,
    raw`Recap endpoint: R0.72E`,
  ],
  [
    "r072e082",
    raw`回顾截止时公开笔记：155`,
    raw`Public notes at the recap endpoint: 155`,
  ],
  [
    "r072e083",
    raw`截至 R0.72E，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 95 个节点或 57 个已公开并封存版本解释成对千禧年问题完成了某个比例。`,
    raw`Through R0.72E, there is no new unconditional continuation criterion, no reduction of the full set of potential singular solutions, and no proof of finite-time breakdown. The 95 nodes or 57 published and archived releases cannot be interpreted as a percentage completion of the Millennium Problem.`,
  ],
  [
    "r072e084",
    raw`累计回顾 · R0.61–R0.72E · 2026-08-27`,
    raw`Cumulative recap · R0.61–R0.72E · 2026-08-27`,
  ],
  [
    "r072e085",
    raw`收录节点：95`,
    raw`Included nodes: 95`,
  ],
  [
    "r072e086",
    raw`通过反例测试还不够。候选随后必须能由 Leray 级或已知 continuation budget 支付；如果它已经强到等价于未知临界范数，就停止该路线。`,
    raw`Passing the counterexample test is not enough. The candidate must then be payable by Leray-level information or a known continuation budget; the route stops if it is already as strong as an unknown critical norm.`,
  ],
  [
    "r072e087",
    raw`下一有限任务先让每个修正量通过 R0.72E exact family：frequency-sensitive initial-layer charge、time-weighted rotational action，以及直接记录 coupling scale 的数据项，必须至少阻断 \(R^{4/3}\) 发散。`,
    raw`The next finite task first tests every repair against the R0.72E exact family: a frequency-sensitive initial-layer charge, a time-weighted rotational action, and a data term that records the coupling scale directly must at least block the \(R^{4/3}\) divergence.`,
  ],
  [
    "r072e088",
    raw`这关闭的是候选中间估计，不是正则性问题。它还提示 raw zero-crossing ledger 可能过强：它能在没有任何奇性风险的光滑不变子类里积累。`,
    raw`This closes a candidate intermediate estimate, not the regularity problem. It also suggests that the raw zero-crossing ledger may be too strong: it can accumulate in a smooth invariant subclass with no singularity risk.`,
  ],
  [
    "r072e089",
    raw`这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72E 的 95 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。这里的节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。`,
    raw`This page follows the R0.00–R0.60 phase recap and organizes the research nodes from R0.61 through R0.72E, 95 in total. It records chronologically what each segment actually proved, which proposals were ruled out by a concrete counterexample or scaling analysis, and which conditions have not been derived from the Navier–Stokes equations. Node status describes the evidence type and does not mistake an archived release for a solved phase objective.`,
  ],
  [
    "r072e090",
    raw`Feynman–Kac 把完整 \(A_q^{-1}\) action 化成 kinetic Brownian path 的振荡平均；驻相和 Kusuoka–Stroock 的定量漂移括号密度界给 \(Q_{\delta,q_0}\lesssim\log(2+\delta)/\delta\)。取 \(\delta_R=R^4\)、\(P_R=q_0^2\delta_R\)、\(S_R^2=\delta_R/\log(2+\delta_R)\)，则 \(D_R\asymp\delta_R^2\)、\(\Lambda_1=O(1)\)、\(\mathcal J_{\rm all}\gtrsim\delta_R\)，从而 normalized ratio 至少按 \(R^{4/3}\) 发散。这个结果排除一条候选中间估计，但所有解仍全局光滑。`,
    raw`Feynman–Kac converts the complete \(A_q^{-1}\) action into an oscillatory average along kinetic Brownian paths; stationary phase and the quantitative drift-bracket density bound of Kusuoka–Stroock give \(Q_{\delta,q_0}\lesssim\log(2+\delta)/\delta\). With \(\delta_R=R^4\), \(P_R=q_0^2\delta_R\), and \(S_R^2=\delta_R/\log(2+\delta_R)\), one has \(D_R\asymp\delta_R^2\), \(\Lambda_1=O(1)\), and \(\mathcal J_{\rm all}\gtrsim\delta_R\), so the normalized ratio diverges at least as \(R^{4/3}\). This excludes a candidate intermediate estimate, while every solution remains globally smooth.`,
  ],
  [
    "r072e091",
    raw`R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 95 个节点沿着这个缺口推进；R0.70A–R0.72E 的 57 个版本已经公开并封存，但其中仍包含条件定理、反例、有限诊断和开放缺口。`,
    raw`The R0.00–R0.60 material remains in the preceding phase recap. The R0.60 conclusion was that the complete Fourier–Leray structure and higher-order calculations could continue, but the critical quantity for general three-dimensional solutions was not controlled. The following 95 nodes advance along this gap; the releases from R0.70A through R0.72E number 57 and are published and archived, while still containing conditional theorems, counterexamples, finite diagnostics, and open gaps.`,
  ],
  [
    "r072e092",
    raw`R0.60 之后的路线分成二十二个阶段`,
    raw`The route after R0.60 is divided into twenty-two phases`,
  ],
  [
    "r072e093",
    raw`R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.72E 的 95 个研究节点；最新一节用单载波 Bessel 根族与完整 H^{-1} action 严格排除候选 D^{1/3}Λ₁ 支付。`,
    raw`Research recap after R0.60: the nodes from R0.61 through R0.72E, 95 in total, are arranged chronologically; the latest note uses a one-carrier Bessel root family and the complete H^{-1} action to rigorously exclude the candidate D^{1/3}Λ₁ payment.`,
  ],
  [
    "r072e094",
    raw`R0.61–R0.72E 的 95 节公开笔记`,
    raw`Public notes from R0.61 through R0.72E: 95`,
  ],
  [
    "r072e095",
    raw`R0.61–R0.72E 回顾 · 2026-08-27`,
    raw`R0.61–R0.72E recap · 2026-08-27`,
  ],
  [
    "r072e096",
    raw`R0.61–R0.72E 研究节点`,
    raw`R0.61–R0.72E research nodes`,
  ],
  [
    "r072e097",
    raw`R0.61–R0.72E｜R0.60 之后的研究回顾`,
    raw`R0.61–R0.72E | Research recap after R0.60`,
  ],
  [
    "r072e098",
    raw`R0.72D 留下的 supercritical alternative 已经实现。一个单载波、始终全局光滑的 exact triangular family，在 full-frequency \(H^{-1}\) rotational charge、真实数据成本和固定区间 enstrophy 全部计入后，仍使 complete-root ledger 相对 \(D^{1/3}\Lambda_1\) 发散。`,
    raw`The supercritical alternative left by R0.72D is realized. After the full-frequency \(H^{-1}\) rotational charge, genuine data cost, and fixed-interval enstrophy are all included, a one-carrier exact triangular family that remains globally smooth still makes the complete-root ledger diverge relative to \(D^{1/3}\Lambda_1\).`,
  ],
  [
    "r072e099",
    raw`R0.72E · 单载波 supercritical ledger 与候选 \(D^{1/3}\Lambda_1\) payment 失效`,
    raw`R0.72E · One-carrier supercritical ledger and failure of the candidate \(D^{1/3}\Lambda_1\) payment`,
  ],
  [
    "r072e100",
    raw`R0.72E 的 one-carrier supercritical no-go：固定整数 \(q_0>R_*\) 后，R0.72A 的 Bessel 根通过精确 diagonal conjugacy 保持。Feynman–Kac、\(A_q^{-1}\) 驻相与定量 parabolic Hörmander density 给 full-frequency action \(Q_{\delta,q_0}\lesssim\log(2+\delta)/\delta\)。在 \(\delta_R=R^4\)、\(S_R^2=\delta_R/\log(2+\delta_R)\) 下，完整数据、固定区间 enstrophy contrast 与 rotational charge 都被支付，而 \(\mathcal J_{\rm all}/(D^{1/3}\Lambda_1)\gtrsim R^{4/3}\)。这严格排除候选 \(D^{1/3}\Lambda_1\) complete-root 中间估计，但不产生爆破或一般正则性结论。`,
    raw`R0.72E one-carrier supercritical no-go: after fixing an integer \(q_0>R_*\), exact diagonal conjugacy preserves the Bessel roots from R0.72A. Feynman–Kac, \(A_q^{-1}\) stationary phase, and a quantitative parabolic Hörmander density bound give the full-frequency action \(Q_{\delta,q_0}\lesssim\log(2+\delta)/\delta\). With \(\delta_R=R^4\) and \(S_R^2=\delta_R/\log(2+\delta_R)\), the complete data, fixed-interval enstrophy contrast, and rotational charge are all paid, while \(\mathcal J_{\rm all}/(D^{1/3}\Lambda_1)\gtrsim R^{4/3}\). This rigorously excludes the candidate \(D^{1/3}\Lambda_1\) complete-root intermediate estimate, but yields neither blowup nor a general regularity result.`,
  ],
  [
    "r072e101",
    raw`R0.72E 附图`,
    raw`R0.72E figure`,
  ],
  [
    "r072e102",
    raw`R0.72E 证书`,
    raw`R0.72E certificates`,
  ],
  [
    "r072e103",
    raw`R0.72F 寻找最小 frequency-sensitive repair`,
    raw`R0.72F searches for the minimal frequency-sensitive repair`,
  ],
  [
    "r072e104",
    raw`从 complete-root 局部暴露走到候选 payment 的严格失效`,
    raw`From complete-root local exposure to rigorous failure of the candidate payment`,
  ],
  [
    "r072e105",
    raw`单载波 Bessel 根族严格排除候选 \(D^{1/3}\Lambda_1\) complete-root payment`,
    raw`A one-carrier Bessel root family rigorously excludes the candidate \(D^{1/3}\Lambda_1\) complete-root payment`,
  ],
  [
    "r072e106",
    raw`固定整数 \(q_0>R_*\)，取 \(\nu=d=K_z=r_1=1\)、\(K_y=0\)。 载波隔离、精确 diagonal conjugacy 与 Bessel \(C^1\) 比较给前 \(R\) 个正时间简单根； selected target-row mass 为 \((8/\pi^2)\log R+O(1)\)。`,
    raw`Fix an integer \(q_0>R_*\) and set \(\nu=d=K_z=r_1=1\) and \(K_y=0\). Carrier isolation, exact diagonal conjugacy, and a Bessel \(C^1\) comparison give the first \(R\) simple positive-time roots; the selected target-row mass is \((8/\pi^2)\log R+O(1)\).`,
  ],
  [
    "r072e107",
    raw`环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \(M^{-2}\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → phase-uniform \(M^{-8/3}\) sharp algebraic prefactor → shifted Rudin–Shapiro heat pulse → positive-time simple root → full-charge normalized order-one saturation → fixed-carrier shell isolation → negative-Sobolev action decay → candidate D^{1/3}Λ₁ payment failure`,
    raw`annular exclusion → source–kernel ledger → covariance-spectrum stratification → all-frequency conditional bridge → response-slope chord gain → common-response order-one channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \(M^{-2}\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → sharp phase-uniform \(M^{-8/3}\) algebraic prefactor → shifted Rudin–Shapiro heat pulse → positive-time simple root → full-charge normalized order-one saturation → fixed-carrier shell isolation → negative-Sobolev action decay → candidate D^{1/3}Λ₁ payment failure`,
  ],
  [
    "r072e108",
    raw`静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71U–Z 依次处理 second-time jet、complete first row、fixed-small-coupling endpoint、selected roots 与 complete roots。R0.72A–C 建立 Bessel lower family、target-row participation 与 physical-phase sharp scales；R0.72D 再实现 positive-time root 与 full-charge order-one saturation。R0.72E 固定 \(q_0>R_*\)，用 Feynman–Kac、驻相和定量 Hörmander density 控制完整 \(H^{-1}\) action；exact one-carrier family 最终使 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。`,
    raw`After the static annular family is rigorously excluded, the main route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71U–Z treats the second-time jet, complete first row, fixed-small-coupling endpoint, selected roots, and complete roots. R0.72A–C develops the Bessel lower family, target-row participation, and sharp physical-phase scales; R0.72D then realizes a positive-time root and full-charge order-one saturation. R0.72E fixes \(q_0>R_*\) and controls the complete \(H^{-1}\) action using Feynman–Kac, stationary phase, and a quantitative Hörmander density bound; the exact one-carrier family ultimately makes the complete-root ledger relative to the candidate \(D^{1/3}\Lambda_1\) payment diverge as \(R^{4/3}\).`,
  ],
  [
    "r072e109",
    raw`累计回顾 R0.61–R0.72E · 2026-08-27`,
    raw`Cumulative recap R0.61–R0.72E · 2026-08-27`,
  ],
  [
    "r072e110",
    raw`目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.72E 的每个解都全局光滑；它证明的是 complete-root ledger 的候选中间估计失败，并提示 raw zero-crossing ledger 可能比正则性需要更强。`,
    raw`There is currently no new unconditional continuation criterion and no construction of a finite-time singularity. Every R0.72E solution is globally smooth; the result proves failure of a candidate intermediate estimate for the complete-root ledger and suggests that the raw zero-crossing ledger may be stronger than regularity requires.`,
  ],
  [
    "r072e111",
    raw`上次综述 v1.17 · 2026-08-27`,
    raw`Previous review v1.17 · 2026-08-27`,
  ],
  [
    "r072e112",
    raw`我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.72E 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。`,
    raw`A separate systematic review places classical theory, five main literature lines, the candidate-blowup exclusion tree, developments from 2019–2026, and the R0.69P–R0.72E route on this site in one diagram. Historical nodes R0.61–R0.69O remain in the cumulative recap.`,
  ],
  [
    "r072e113",
    raw`下一步 R0.72F：`,
    raw`Next step R0.72F:`,
  ],
  [
    "r072e114",
    raw`寻找最小 frequency-sensitive repair，并要求它同时阻断当前 exact family、又能由已知 NSE 预算支付。`,
    raw`Find the minimal frequency-sensitive repair that both blocks the present exact family and is payable by known NSE budgets.`,
  ],
  [
    "r072e115",
    raw`研究笔记 R0.72E · 2026-08-27`,
    raw`Research note R0.72E · 2026-08-27`,
  ],
  [
    "r072e116",
    raw`一个 fixed-carrier exact family 在完整 \(H^{-1}\) rotational charge 有界时，使 normalized complete-root ledger 按 \(R^{4/3}\) 发散；这排除候选 \(D^{1/3}\Lambda_1\) payment。`,
    raw`With the complete \(H^{-1}\) rotational charge bounded, a fixed-carrier exact family makes the normalized complete-root ledger diverge as \(R^{4/3}\); this excludes the candidate \(D^{1/3}\Lambda_1\) payment.`,
  ],
  [
    "r072e117",
    raw`依次测试 initial-layer frequency charge、time-weighted rotational action 和显式 coupling-scale data term。候选必须先阻断 R0.72E exact family，再证明它不等价于尚未知的临界范数。`,
    raw`Test an initial-layer frequency charge, a time-weighted rotational action, and an explicit coupling-scale data term in sequence. A candidate must first block the R0.72E exact family and then be shown inequivalent to an unknown critical norm.`,
  ],
  [
    "r072e118",
    raw`阅读 R0.72E 研究笔记 →`,
    raw`Read the R0.72E research note →`,
  ],
  [
    "r072e119",
    raw`展开 65 篇公开笔记`,
    raw`Expand 65 public notes`,
  ],
  [
    "r072e120",
    raw`这是 exact triangular 2.5D 光滑子类中的 candidate-payment no-go theorem。它没有构造奇性，没有给出 continuation criterion，也不解决一般三维 Navier–Stokes 正则性。`,
    raw`This is a candidate-payment no-go theorem in an exact smooth triangular 2.5D subclass. It constructs no singularity, gives no continuation criterion, and does not solve general three-dimensional Navier–Stokes regularity.`,
  ],
  [
    "r072e121",
    raw`综述 v1.18 · 2026-08-27`,
    raw`Review v1.18 · 2026-08-27`,
  ],
  [
    "r072e122",
    raw`最终 \[ \frac{\mathcal J_{{\rm all},R}} {D_R^{1/3}\Lambda_1([0,T];u_R)} \ge cR^{4/3}\longrightarrow\infty. \] Producer 与 independent checker 均为 16/16 PASS；两路 action 窗口分别是 \(X=6\) 与 \(X=1\)，不能混合比较。`,
    raw`Finally, \[ \frac{\mathcal J_{{\rm all},R}} {D_R^{1/3}\Lambda_1([0,T];u_R)} \ge cR^{4/3}\longrightarrow\infty. \] The producer and independent checker both record 16/16 PASS; their action windows are \(X=6\) and \(X=1\), respectively, and must not be compared as a common window.`,
  ],
  [
    "r072e123",
    raw`Feynman–Kac、固定相位驻相和定量 Hörmander density 给 \[ Q_{\delta,q_0}(X)\le C_{X,q_0}\frac{1+\log(2+\delta)}{\delta}. \] 取 \(\delta_R=R^4\)、\(P_R=q_0^2\delta_R\)、 \(S_R^2=\delta_R/\log(2+\delta_R)\)，完整数据与 enstrophy contrast 得到支付， full-frequency rotational charge 保持有界，而 \(\mathcal J_{\rm all}\gtrsim\delta_R\)。`,
    raw`Feynman–Kac, fixed-phase stationary phase, and a quantitative Hörmander density bound give \[ Q_{\delta,q_0}(X)\le C_{X,q_0}\frac{1+\log(2+\delta)}{\delta}. \] With \(\delta_R=R^4\), \(P_R=q_0^2\delta_R\), and \(S_R^2=\delta_R/\log(2+\delta_R)\), the complete data and enstrophy contrast are paid, the full-frequency rotational charge stays bounded, and \(\mathcal J_{\rm all}\gtrsim\delta_R\).`,
  ],
  [
    "r072e124",
    raw`R0.60 之后的累计回顾按二十二个阶段组织。R0.61–R0.69O 保留约化递推、剪切边界、横向扰动与压力局部预算；R0.69P–R0.71T 依次检查静态环带、协方差谱、projected-Lamb heat、faces、incidence 与真实内部 entry；R0.71U–R0.71Z 处理 second-time jet、complete first row 与全部根边界；R0.72A–D 依次给出 Bessel lower family、target-row participation、physical-phase sharp prefactor 与 full-charge order-one saturation；R0.72E 再用 fixed-carrier exact family 严格排除候选 \(D^{1/3}\Lambda_1\) payment。R0.70A–R0.72E 共 57 个已公开并封存版本。`,
    raw`The cumulative recap after R0.60 is organized into twenty-two phases. R0.61–R0.69O retains reduced recurrences, shear boundaries, transverse perturbations, and local pressure budgets; R0.69P–R0.71T successively examines static annuli, covariance spectra, projected-Lamb heat, faces, incidence, and genuine interior entries. R0.71U–R0.71Z treats the second-time jet, complete first row, and all-root boundaries. R0.72A–D successively establishes the Bessel lower family, target-row participation, the sharp physical-phase prefactor, and full-charge order-one saturation; R0.72E then uses a fixed-carrier exact family to rigorously exclude the candidate \(D^{1/3}\Lambda_1\) payment. Published and archived releases from R0.70A through R0.72E number 57.`,
  ],
  [
    "r072e125",
    raw`R0.60 recap 之后的累计回顾收录 95 个节点；全站现有 155 篇公开研究笔记`,
    raw`The cumulative recap after R0.60 contains 95 nodes; the site now has 155 public research notes`,
  ],
  [
    "r072e126",
    raw`R0.70A–R0.72E 已公开并封存版本`,
    raw`Published and archived releases R0.70A–R0.72E`,
  ],
  [
    "r072e127",
    raw`R0.72E 已完成：`,
    raw`R0.72E complete:`,
  ],
  [
    "r072e128",
    raw`R0.72E 已在 exact smooth class 中排除候选 \(D^{1/3}\Lambda_1\) complete-root payment；下一步寻找最小的 frequency-sensitive repair，并检查它是否仍由 Leray 级信息支付。`,
    raw`R0.72E excludes the candidate \(D^{1/3}\Lambda_1\) complete-root payment in an exact smooth class; the next step seeks the minimal frequency-sensitive repair and tests whether Leray-level information can still pay for it.`,
  ],
];

function duplicateValues(values) {
  const seen = new Set();
  const duplicates = new Set();
  for (const value of values) {
    if (seen.has(value)) duplicates.add(value);
    seen.add(value);
  }
  return [...duplicates];
}

function numericTokens(value) {
  return [...value.matchAll(/\p{N}+(?:[.,]\p{N}+)*/gu)].map(
    (match) => match[0],
  );
}

function protectedBundle(value) {
  return {
    texAndUrls: extractProtectedTokens(value),
    numbers: numericTokens(value),
  };
}

const declaredSourceCorrections = new Map([
  [
    raw`的 Corollary (3.25) 与 (3.27) 取得小时间多项式密度界。驻相、负矩和时间积分随后给 \(Q_{\delta,q_0}\lesssim(1+\log(2+\delta))/\delta\)。`,
    raw`的 Corollary (3.25) 与 inequality (3.27) 取得小时间多项式密度界。驻相、负矩和时间积分随后给 \(Q_{\delta,q_0}\lesssim(1+\log(2+\delta))/\delta\)。`,
  ],
  [
    raw`固定相位驻相给 \(A_q^{-1}\) norm square \(\lesssim(1+\kappa)^{-1}\)。过程 \(dB=\sqrt2dW\)、\(dZ=(-Z+e^{iB})dt\) 的两个漂移括号在每一点一致张成两个 \(Z\) 方向；它们与噪声场组成的绝对行列式恒为 \(4\)。Kusuoka–Stroock Part II 的定量密度界和 Brownian 反射原理给 \(\mathbb E|Z_t|^{-1}\le C_X/t\)，所以`,
    raw`固定相位驻相给 \(A_q^{-1}\) norm square \(\lesssim(1+\kappa)^{-1}\)。过程 \(dB=\sqrt2dW\)、\(dZ=(-Z+e^{iB})dt\) 的两个漂移括号在每一点都张成两个 \(Z\) 方向；它们与噪声场组成的绝对行列式恒为 \(4\)。Kusuoka–Stroock Part II 的定量密度界和 Brownian 反射原理给 \(\mathbb E|Z_t|^{-1}\le C_X/t\)，所以`,
  ],
]);
const snapshotRaw = JSON.parse(await readFile(snapshotPath, "utf8"));
const snapshot = Array.isArray(snapshotRaw)
  ? snapshotRaw.map((entry) => ({
      ...entry,
      zh: declaredSourceCorrections.get(entry.zh) ?? entry.zh,
    }))
  : snapshotRaw;
if (!Array.isArray(snapshot) || snapshot.length !== 128 || rows.length !== 128) {
  throw new Error(
    "R0.72E snapshot/row cardinality drift: snapshot=" +
      (Array.isArray(snapshot) ? snapshot.length : "not-an-array") +
      ", rows=" +
      rows.length,
  );
}

for (const [field, values] of [
  ["row id", rows.map(([id]) => id)],
  ["row key", rows.map(([, zh]) => zh)],
  ["snapshot id", snapshot.map((entry) => entry.id)],
  ["snapshot key", snapshot.map((entry) => entry.zh)],
]) {
  const duplicates = duplicateValues(values);
  if (duplicates.length) {
    throw new Error("Duplicate " + field + " values: " + duplicates.join(" | "));
  }
}

for (const [index, [, zh]] of rows.entries()) {
  if (snapshot[index]?.zh !== zh) {
    throw new Error(
      "R0.72E snapshot source drift at row " +
        String(index + 1) +
        ":\nSNAPSHOT " +
        JSON.stringify(snapshot[index]?.zh) +
        "\nROW " +
        JSON.stringify(zh),
    );
  }
}

const translations = JSON.parse(await readFile(translationsPath, "utf8"));
const source = await collectSiteStrings(publicDirectory);
const sourceByChinese = new Map(source.map((entry) => [entry.zh, entry]));
const existingByChinese = new Map(
  translations.map((entry) => [entry.zh, entry]),
);
const mapped = new Map(rows.map(([id, zh, en]) => [zh, { id, en }]));

for (const entry of snapshot) {
  const live = sourceByChinese.get(entry.zh);
  if (
    !live ||
    live.count !== entry.count ||
    JSON.stringify(live.files) !== JSON.stringify(entry.files)
  ) {
    throw new Error(
      "R0.72E live-source drift for snapshot key:\n" +
        entry.zh +
        "\nSNAPSHOT " +
        JSON.stringify({ count: entry.count, files: entry.files }) +
        "\nLIVE " +
        JSON.stringify(live ?? null),
    );
  }
}

const missing = source.filter((entry) => !existingByChinese.has(entry.zh));
const unmapped = missing.filter((entry) => !mapped.has(entry.zh));
if (unmapped.length) {
  throw new Error(
    "R0.72E translation source drift (" +
      unmapped.length +
      " unmapped live strings):\n" +
      unmapped.map((entry) => entry.zh).join("\n---\n"),
  );
}

for (const [id, zh, en] of rows) {
  if (!sourceByChinese.has(zh)) {
    throw new Error("R0.72E mapped source is no longer live: " + zh);
  }
  if (!en.trim() || containsChinese(en)) {
    throw new Error("Invalid English translation for: " + zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("Collective English voice remains in: " + zh);
  }
  const zhTokens = protectedBundle(zh);
  const enTokens = protectedBundle(en);
  if (JSON.stringify(zhTokens) !== JSON.stringify(enTokens)) {
    throw new Error(
      "Protected-token mismatch for:\n" +
        zh +
        "\nZH " +
        JSON.stringify(zhTokens) +
        "\nEN " +
        JSON.stringify(enTokens),
    );
  }
  const existing = existingByChinese.get(zh);
  if (existing && (existing.id !== id || existing.en !== en)) {
    throw new Error(
      "Existing R0.72E translation drift for " +
        id +
        ":\n" +
        JSON.stringify(existing),
    );
  }
}

for (const field of ["id", "zh"]) {
  const duplicates = duplicateValues(translations.map((entry) => entry[field]));
  if (duplicates.length) {
    throw new Error(
      "Duplicate existing " + field + " values: " + duplicates.join(" | "),
    );
  }
}

let added = 0;
for (const [id, zh, en] of rows) {
  if (existingByChinese.has(zh)) continue;
  const live = sourceByChinese.get(zh);
  translations.push({ ...live, id, en });
  existingByChinese.set(zh, translations.at(-1));
  added += 1;
}

const sourceAfter = await collectSiteStrings(publicDirectory);
const missingAfter = sourceAfter.filter(
  (entry) => !existingByChinese.has(entry.zh),
);
if (missingAfter.length) {
  throw new Error(
    "R0.72E full-site missing-after check failed (" +
      missingAfter.length +
      " strings):\n" +
      missingAfter.map((entry) => entry.zh).join("\n---\n"),
  );
}

for (const field of ["id", "zh"]) {
  const duplicates = duplicateValues(translations.map((entry) => entry[field]));
  if (duplicates.length) {
    throw new Error(
      "Duplicate final " + field + " values: " + duplicates.join(" | "),
    );
  }
}

await writeFile(translationsPath, JSON.stringify(translations, null, 2) + "\n");
console.log(
  JSON.stringify({
    added,
    total: translations.length,
    liveStrings: source.length,
    missingBefore: missing.length,
    missingAfter: missingAfter.length,
    mappedRows: rows.length,
  }),
);
