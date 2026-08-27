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
  "r072g-missing.json",
);

const raw = String.raw;
const translationsByChinese = new Map([
  [
    raw`本节真正使用的是 exact one-carrier lattice 的实相位 gauge、两个目标行恒等式与 Rolle–BV 归约；它们把根采样转成连续 negative-Sobolev action，不依赖解析零点计数。限定一手来源检索没有找到直接给出这条 complete temporal root-slope estimate 的定理；该判断是截至 2026-08-27 的 bounded non-collision check，不是原创性、优先权或穷尽性声明。`,
    raw`This section actually uses the real-phase gauge of the exact one-carrier lattice, two target-row identities, and the Rolle–BV reduction. They turn root sampling into a continuous negative-Sobolev action without relying on analytic zero counting. The bounded search of primary sources found no theorem directly giving this complete temporal root-slope estimate. That assessment is a bounded non-collision check through 2026-08-27, not a claim of novelty, priority, or exhaustiveness.`,
  ],
  [
    raw`处理 \(\mathcal E_Q=\int|hQF|\)，要求载波数无关的 critical-log payment，或构造显式 growing-carrier 反族。`,
    raw`Treat \(\mathcal E_Q=\int|hQF|\), requiring either a critical-log payment independent of carrier count or an explicit growing-carrier counterfamily.`,
  ],
  [
    raw`处理结构受控的固定采样或整函数零点，也不直接适用于随解移动的 temporal self-zero nodes。`,
    raw`treats structurally controlled fixed sampling or zeros of entire functions and likewise does not apply directly to temporal self-zero nodes that move with the solution.`,
  ],
  [raw`打开 97 节完整索引`, raw`Open the complete 97-note index`],
  [
    raw`的 Jacobi–Anger 展开、Bessel zeros 与导数渐近支持 selected logarithmic lower mass；`,
    raw`'s Jacobi–Anger expansion, Bessel zeros, and derivative asymptotics support the selected logarithmic lower mass;`,
  ],
  [
    raw`的定量 density input 支持继承自 R0.72E 的 negative-Sobolev action 上界。`,
    raw`'s quantitative density input supports the negative-Sobolev action upper bound inherited from R0.72E.`,
  ],
  [
    raw`的时间解析性或唯一延拓结果不能推出 launch-uniform root count、root separation 或 slope mass。`,
    raw`'s time-analyticity or unique-continuation results do not imply a launch-uniform root count, root separation, or slope mass.`,
  ],
  [
    raw`给出复杂量热流固定点时间迹在无界半线上出现 \(\tau_k\to\infty\) 零点序列的例子，但不否定紧正时间区间上的有限根数，也不估计根斜率平方和。`,
    raw`gives an example in which the fixed-point temporal trace of a complex-valued heat flow has a zero sequence \(\tau_k\to\infty\) on an unbounded half-line, but it neither rules out finitely many roots on a compact positive-time interval nor estimates the sum of squared root slopes.`,
  ],
  [raw`开放接口 · R0.72H`, raw`Open interface · R0.72H`],
  [
    raw`控制一维实抛物方程的空间零数；`,
    raw`controls the spatial zero number for one-dimensional real parabolic equations;`,
  ],
  [raw`累计回顾与 97 节索引`, raw`Cumulative recap and 97-note index`],
  [
    raw`实相位 gauge、目标行恒等式与 Rolle–BV 归约给 \(G_{\rm all}\lesssim\log\delta\)，selected Bessel roots 给匹配下界；原始幅度序列上 critical-log payment 对 complete roots 同阶。结论限于精确实单载波 ray。`,
    raw`The real-phase gauge, target-row identities, and Rolle–BV reduction give \(G_{\rm all}\lesssim\log\delta\), while the selected Bessel roots give a matching lower bound. On the original amplitude sequence, the critical-log payment has the same order for the complete roots. The conclusion is limited to the exact real one-carrier ray.`,
  ],
  [
    raw`文献综述 v1.20 · 2026-08-27`,
    raw`Literature review v1.20 · 2026-08-27`,
  ],
  [
    raw`我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.72G 只列为研究笔记。我不把计算或笔记外推成正则性定理。`,
    raw`I list published theorems as known results, mark 2026 preprints separately, and list R0.69P–R0.72G on this site only as research notes. I do not extrapolate computations or notes into regularity theorems.`,
  ],
  [
    raw`中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–U 给出 conditional incidence、genuine internal-entry、second-time-jet 与 finite recurrence 边界。R0.71V–W 分离 fixed zero-level trace 并排除 data-uniform complete first-row ledger。R0.71X 在 fixed-dimensional small-coupling family 内达到 one-third endpoint；R0.71Y 处理 selected roots；R0.71Z 给出 all-root slope-mass bound 和 launch-inclusive floor cancellation；R0.72A 把 strong-coupling loss 局部化到实际观察层，R0.72B 保留 exact target-row participation，R0.72C 得到 phase-uniform exact-launch \(M^{-8/3}\) 与 fixed-positive tail \(M^{-3}\) 的 sharp algebraic scales。R0.72D 在 shifted Rudin–Shapiro family 上构造 positive-time exact root，保留 full rotational charge，并得到非消失但不发散的 normalized complete-root ledger。R0.72E 回到 fixed-carrier Bessel family，以定量 negative-Sobolev action 证明 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。R0.72F 再用 regularly varying initial-layer weights 分离 selected-root 的 \(1/3\) 阈值与 Leray payment 的 \(1/2\) 阈值，并选出 critical-log 最小边界。R0.72G 在 exact real one-carrier lattice 上用 phase gauge、目标行恒等式与 Rolle–BV 归约证明完整根质量恰为对数量级，并得到 critical-log complete-root sharp saturation。一般 Navier–Stokes 正则性仍开放。`,
    raw`. R0.69P–R0.71P reaches the positive-entry temporal-packing boundary; R0.71Q–U establishes the boundaries for conditional incidence, genuine internal entries, the second-time jet, and finite recurrence. R0.71V–W separates the fixed zero-level trace and excludes a data-uniform complete first-row ledger. R0.71X reaches the one-third endpoint in a fixed-dimensional small-coupling family; R0.71Y treats selected roots; R0.71Z gives an all-root slope-mass bound and launch-inclusive floor cancellation. R0.72A localizes the strong-coupling loss to the actual observation layer, R0.72B retains exact target-row participation, and R0.72C obtains the sharp phase-uniform exact-launch \(M^{-8/3}\) and fixed-positive-tail \(M^{-3}\) algebraic scales. R0.72D constructs a positive-time exact root in a shifted Rudin–Shapiro family, retains the full rotational charge, and obtains a nonvanishing but nondivergent normalized complete-root ledger. R0.72E returns to a fixed-carrier Bessel family and uses a quantitative negative-Sobolev action estimate to make the complete-root ledger relative to the candidate \(D^{1/3}\Lambda_1\) payment diverge as \(R^{4/3}\). R0.72F then uses regularly varying initial-layer weights to separate the selected-root threshold \(1/3\) from the Leray-payment threshold \(1/2\), selecting the minimal critical-log boundary. On the exact real one-carrier lattice, R0.72G uses a phase gauge, target-row identities, and the Rolle–BV reduction to prove that the complete root mass has exactly logarithmic order and obtains sharp critical-log complete-root saturation. General Navier–Stokes regularity remains open.`,
  ],
  [
    raw`exact one-carrier complete-root packing 与尖锐饱和`,
    raw`Exact one-carrier complete-root packing and sharp saturation`,
  ],
  [
    raw`R0.72G 的 temporal self-zero sampling 边界`,
    raw`R0.72G temporal self-zero sampling boundary`,
  ],
  [raw`R0.72G 的主源边界`, raw`R0.72G primary-source boundary`],
  [
    raw`\(\delta=0\) 被明确排除：此时 \(f\equiv0\) 而 \(h\not\equiv0\)，按同一定义完整根质量发散。这正是定理保留 \(\delta\ge1\) 的原因。`,
    raw`The case \(\delta=0\) is explicitly excluded: then \(f\equiv0\) while \(h\not\equiv0\), so the complete root mass under the same definition diverges. This is why the theorem retains \(\delta\ge1\).`,
  ],
  [raw`01 · 精确格点`, raw`01 · Exact lattice`],
  [raw`03 · 尖锐对数`, raw`03 · Sharp logarithm`],
  [raw`04 · 物理账本`, raw`04 · Physical ledger`],
  [raw`05 · 双路证书`, raw`05 · Dual-path certificates`],
  [raw`06 · 正式附图`, raw`06 · Formal figure`],
  [raw`把预选根撤掉之后，`, raw`After removing the preselected roots,`],
  [raw`版本 v0.72G · 2026-08-27`, raw`Version v0.72G · 2026-08-27`],
  [
    raw`报告、证明审计、双路证书与正式附图全部保留`,
    raw`The report, proof audit, dual-path certificates, and formal figure are all preserved`,
  ],
  [
    raw`多重根满足 \(h=0\)，无需另加重数。代入目标行恒等式，再用上面的 \(q\)-界与 Cauchy–Schwarz，就得到主上界。最后对所有有限根子集取上确界，因此证明没有暗中使用根集有限、根间距正下界或解析零点计数。`,
    raw`A multiple root satisfies \(h=0\), so no multiplicity charge is needed. Substituting the target-row identity and then using the preceding \(q\)-bounds and Cauchy–Schwarz gives the main upper bound. Finally, taking the supremum over every finite root subset ensures that the proof does not implicitly use finiteness of the root set, a positive lower bound on root spacing, or analytic zero counting.`,
  ],
  [raw`返回 R0.72F`, raw`Return to R0.72F`],
  [
    raw`复 Fourier Strang split，热半步与时间势积分均精确；独立覆盖 \(R=8,12,16,24,32\)。共同根数逐点完全一致，最大 complete-mass 差为 \(9.18\times10^{-7}\)。`,
    raw`A complex Fourier Strang splitting uses exact heat half-steps and an exact integrated time potential; the independent coverage is \(R=8,12,16,24,32\). The common root counts agree pointwise exactly, and the maximum complete-mass difference is \(9.18\times10^{-7}\).`,
  ],
  [raw`格点`, raw`Lattice`],
  [
    raw`根数与根间距不进入常数；完整根质量恰为对数量级。结论只覆盖声明的精确实单载波族。`,
    raw`Neither the root count nor root spacing enters the constant; the complete root mass has exactly logarithmic order. The conclusion covers only the stated exact real one-carrier family.`,
  ],
  [
    raw`固定整数 \(q_0\) 大于目标 multiplier 的支撑半径，令 \(\mu=q_0^{-2}\)，并只考虑 \(\delta\ge1\)。对精确单载波格点`,
    raw`Fix an integer \(q_0\) larger than the support radius of the target multiplier, set \(\mu=q_0^{-2}\), and consider only \(\delta\ge1\). For the exact one-carrier lattice`,
  ],
  [
    raw`回到全局光滑的实三角形解 \(u=(f_{\rm phys}(y,z,t),0,v(y,t))\)。保持 shear amplitude \(P=q_0^2\delta\)，并令 active squared amplitude \(A_\delta=S_\delta^2\le C_A\delta\)。根账本使用 \([0,T)\)，连续积分使用 \([0,T]\)，从而不让终端根在两边产生不同约定。对所有充分大的 \(\delta\)，`,
    raw`Return to the globally smooth real triangular solution \(u=(f_{\rm phys}(y,z,t),0,v(y,t))\). Keep the shear amplitude \(P=q_0^2\delta\) and take the active squared amplitude \(A_\delta=S_\delta^2\le C_A\delta\). The root ledger uses \([0,T)\), while the continuous integral uses \([0,T]\), so a terminal root cannot be treated differently on the two sides. For all sufficiently large \(\delta\),`,
  ],
  [
    raw`价值是把下一障碍从“也许还有更多根”推进到“多载波混合行能否维数无关地支付”。这是一项精确模型类内部的 trace-packing 定理，不是千禧年问题的部分解答；节点数也不能换算成问题完成比例。`,
    raw`The value is that the next obstruction moves from “there may be more roots” to “can the multi-carrier mixed row be paid dimension-independently?” This is a trace-packing theorem within an exact model class, not a partial solution of the Millennium Problem; the number of nodes cannot be converted into a percentage of completion.`,
  ],
  [
    raw`截至 2026-08-27 的限定一手来源检索中，我没有找到直接给出本节 complete temporal root-slope estimate 的定理。这是 bounded non-collision check，不是原创性、优先权或穷尽性声明。`,
    raw`In the bounded search of primary sources through 2026-08-27, I found no theorem directly giving the complete temporal root-slope estimate in this section. This is a bounded non-collision check, not a claim of novelty, priority, or exhaustiveness.`,
  ],
  [
    raw`令 \(\psi=e^{\mu x}f\)，则 \(\psi'=\delta e^{\mu x}h\)。对任意有限的正根子集 \(0<x_1<\cdots<x_N<X\)，Rolle 定理在每两个相邻目标根之间给出一个 \(h\) 的零点。于是 \(h^2\) 的总变差支付所有采样值：`,
    raw`Set \(\psi=e^{\mu x}f\), so \(\psi'=\delta e^{\mu x}h\). For any finite subset of positive roots \(0<x_1<\cdots<x_N<X\), Rolle's theorem gives a zero of \(h\) between each pair of adjacent target roots. The total variation of \(h^2\) therefore pays for every sampled value:`,
  ],
  [
    raw`目标相位实化；两个精确目标行恒等式；不依赖根数的 Rolle–BV packing；完整质量 \(\asymp\log\delta\)；声明物理幅度族上的 critical-log complete-root payment 与尖锐饱和。`,
    raw`Realification of the target phase; two exact target-row identities; Rolle–BV packing independent of root count; complete mass \(\asymp\log\delta\); and critical-log complete-root payment with sharp saturation on the stated physical-amplitude family.`,
  ],
  [
    raw`其中 \(\Lambda_{1,*}=\mathcal R_Y[1+\mathscr A_*]\)，\(\mathscr A_*\) 使用 R0.72F 的 \(w_*(s)=s^{-1/3}[1+\log(1/s)]\)。对原始幅度 \(A_R=\delta_R/\log(2+\delta_R)\)，`,
    raw`Here \(\Lambda_{1,*}=\mathcal R_Y[1+\mathscr A_*]\), and \(\mathscr A_*\) uses the R0.72F weight \(w_*(s)=s^{-1/3}[1+\log(1/s)]\). For the original amplitude \(A_R=\delta_R/\log(2+\delta_R)\),`,
  ],
  [
    raw`若 \(q=\lVert VF\rVert_{A_\mu^{-1}}^2\)，则 Cauchy–Schwarz 直接给`,
    raw`If \(q=\lVert VF\rVert_{A_\mu^{-1}}^2\), Cauchy–Schwarz gives directly`,
  ],
  [
    raw`时间解析性、空间零数与固定采样都不是这条估计`,
    raw`Time analyticity, spatial zero number, and fixed sampling are not this estimate`,
  ],
  [
    raw`实不变格点、fixed-step RK4、cubic Hermite + Brent 求根；\(R=8,12,16,24,32,48,64\)。根数从 443 增至 31,242，complete mass 从 3.629980008 增至 7.091268660。`,
    raw`A real invariant lattice with fixed-step RK4 and cubic Hermite + Brent root finding; \(R=8,12,16,24,32,48,64\). The root count grows from 443 to 31,242, while the complete mass grows from 3.629980008 to 7.091268660.`,
  ],
  [
    raw`实格点 RK4 与复 Fourier Strang 得到同一根账本`,
    raw`Real-lattice RK4 and complex Fourier Strang recover the same root ledger`,
  ],
  [
    raw`双路数值证书与失败尝试`,
    raw`Dual-path numerical certificates and failed attempts`,
  ],
  [
    raw`所有构造解仍是全局光滑的三角形 2.5D 解。本页既没有构造有限时奇性，也没有证明一般三维解全局光滑；Clay 千禧年问题仍未解决。`,
    raw`Every constructed solution remains a globally smooth triangular 2.5D solution. This page neither constructs a finite-time singularity nor proves global smoothness for general three-dimensional solutions; the Clay Millennium Problem remains unsolved.`,
  ],
  [
    raw`图 R0.72G-1。左：两路 complete mass、selected mass 与对数 guide；中：有限窗内 resolved root count；右：\(R=64\) 的 dyadic root-mass packets。有限点只用于实现审计，解析结论来自 Rolle–BV 证明。`,
    raw`Figure R0.72G-1. Left: complete mass from both paths, selected mass, and the logarithmic guide. Center: the resolved root count on the finite window. Right: dyadic root-mass packets for \(R=64\). The finite points are used only to audit the implementation; the analytic conclusion comes from the Rolle–BV proof.`,
  ],
  [
    raw`完整根斜率质量由同一个负 Sobolev action 支付`,
    raw`The complete root-slope mass is paid by the same negative-Sobolev action`,
  ],
  [raw`完整账本仍只有一个对数`, raw`the complete ledger still has only one logarithm`],
  [
    raw`系数和初值都为实数，因此 \(f=a_0\) 与 \(h=e^{-x}(a_{-1}-a_1)\) 为实函数。目标行给出两个精确恒等式：`,
    raw`The coefficients and initial data are real, so \(f=a_0\) and \(h=e^{-x}(a_{-1}-a_1)\) are real functions. The target row gives two exact identities:`,
  ],
  [
    raw`下一步保留实相位、固定目标和有限载波，不先跨到一般三维系统。目标是处理 finite real multi-carrier 的 mixed row term：`,
    raw`The next step retains a real phase, fixed target, and finitely many carriers, without first moving to a general three-dimensional system. The target is the mixed row term for finitely many real carriers:`,
  ],
  [
    raw`相邻目标根之间必有一个 \(h\) 的零点`,
    raw`Between adjacent target roots there must be a zero of \(h\)`,
  ],
  [
    raw`相位 gauge 把目标坐标变成实函数`,
    raw`A phase gauge makes the target coordinate real`,
  ],
  [
    raw`写 \(f=F_0\)、\(h=P_0VF\)、\(q=\lVert VF\rVert_{A_\mu^{-1}}^2\)。在半开窗 \([0,X)\) 上，把根和定义成任意有限根子集之和的单调上确界：`,
    raw`Write \(f=F_0\), \(h=P_0VF\), and \(q=\lVert VF\rVert_{A_\mu^{-1}}^2\). On the half-open window \([0,X)\), define the root sum as the monotone supremum of the sums over arbitrary finite root subsets:`,
  ],
  [
    raw`沿 R0.72E 的 \(\delta_R=R^4\)，标准 Bessel 零点与导数渐近给`,
    raw`Along the R0.72E sequence \(\delta_R=R^4\), the standard asymptotics for Bessel zeros and derivatives give`,
  ],
  [
    raw`研究笔记 R0.72G · COMPLETE ROOTS · ROLLE–BV · CRITICAL LOG`,
    raw`Research note R0.72G · COMPLETE ROOTS · ROLLE–BV · CRITICAL LOG`,
  ],
  [
    raw`研究笔记 R0.72G：在精确实单载波三角形 Navier–Stokes 族上，用 Rolle–BV 论证把完整根斜率质量压到负 Sobolev action，并证明 critical-log payment 的完整根尖锐饱和。`,
    raw`Research note R0.72G: on the exact real one-carrier triangular Navier–Stokes family, a Rolle–BV argument bounds the complete root-slope mass by the negative-Sobolev action and proves sharp complete-root saturation of the critical-log payment.`,
  ],
  [raw`一般三维正则性：OPEN`, raw`General three-dimensional regularity: OPEN`],
  [
    raw`因此额外根可以改变有界常数，却不能在这条精确族中制造隐藏的超对数斜率质量。`,
    raw`Additional roots can therefore change a bounded constant, but they cannot create hidden super-logarithmic slope mass in this exact family.`,
  ],
  [
    raw`有限关口只有两个可接受结果：证明它可由 critical-log action 以载波数无关常数支付，或构造一个随载波数增长的显式反族。两者都必须保留 complete roots、launch atom 与 full-frequency charge。`,
    raw`The finite gate has only two acceptable outcomes: prove payment by the critical-log action with a carrier-count-independent constant, or construct an explicit counterfamily that grows with carrier count. Either outcome must retain the complete roots, launch atom, and full-frequency charge.`,
  ],
  [
    raw`有限或无限多载波的维数无关常数；一般 triangular launch data；任意复目标；restart/dyadic 覆盖到一般弱解；三维 Navier–Stokes continuation 或 singularity theorem。`,
    raw`A dimension-independent constant for finitely or infinitely many carriers; general triangular launch data; arbitrary complex targets; restart/dyadic covering for general weak solutions; or a three-dimensional Navier–Stokes continuation or singularity theorem.`,
  ],
  [
    raw`阅读 R0.60 之后的完整累计回顾`,
    raw`Read the complete cumulative recap after R0.60`,
  ],
  [
    raw`这把 R0.72F 的 selected-root saturation 提升为同一测试序列上的 complete-root saturation。它仍不是一般三维解的 continuation criterion。`,
    raw`This upgrades the R0.72F selected-root saturation to complete-root saturation on the same test sequence. It is still not a continuation criterion for general three-dimensional solutions.`,
  ],
  [
    raw`这一节关闭了候选在原始反例族上的最后一个漏洞`,
    raw`This section closes the candidate's last gap on the original counterexample family`,
  ],
  [
    raw`正式附图、数据、代码、环境与校验和`,
    raw`Formal figure, data, code, environment, and checksums`,
  ],
  [
    raw`正式附图分开显示完整质量、独立一致性与 dyadic packets`,
    raw`The formal figure separates complete mass, independent agreement, and dyadic packets`,
  ],
  [
    raw`证明域被固定在精确实单载波 ray`,
    raw`The proof domain is fixed to the exact real one-carrier ray`,
  ],
  [
    raw`置 \(F_r=i^{-r}a_r\)，则 \(a_{-1}(0)=1\)，其余初值为零，且`,
    raw`Set \(F_r=i^{-r}a_r\). Then \(a_{-1}(0)=1\), every other initial value is zero, and`,
  ],
  [raw`状态 · R0.72G 完成`, raw`Status · R0.72G complete`],
  [
    raw`critical-log payment 在完整根集上成立并饱和`,
    raw`The critical-log payment holds and saturates on the complete root set`,
  ],
  [
    raw`DLMF 的 Jacobi–Anger 展开、Bessel zeros 与导数渐近支持 selected logarithmic lower mass；Kusuoka–Stroock 的定量密度估计是继承自 R0.72E 的 action 上界输入。Poláčik–Šverák 说明复杂量热流的固定点时间迹可以在无界半线上出现趋向无穷的零点序列，但不否定正距离紧区间上的有限根数。`,
    raw`The DLMF Jacobi–Anger expansion, Bessel zeros, and derivative asymptotics support the selected logarithmic lower mass; the Kusuoka–Stroock quantitative density estimate is an input to the action upper bound inherited from R0.72E. Poláčik–Šverák show that the fixed-point temporal trace of a complex-valued heat flow can have a zero sequence tending to infinity on an unbounded half-line, but this does not rule out finitely many roots on a compact interval bounded away from zero.`,
  ],
  [
    raw`Dong–Zhang、Giga 等的时间解析性只给正时间根的隔离，不给 launch-uniform 根数、根分离或平方斜率和。Angenent、Matano 控制一维实抛物方程的空间零数；de Branges、Paley–Wiener 与 Cartwright 理论则处理满足结构条件的固定采样或整函数零点。它们都不能替代这里随解移动的 temporal self-zero sampling。`,
    raw`Time analyticity results of Dong–Zhang, Giga, and others give only isolation of positive-time roots, not a launch-uniform root count, root separation, or sum of squared slopes. Angenent and Matano control the spatial zero number for one-dimensional real parabolic equations, while de Branges, Paley–Wiener, and Cartwright theory treat fixed sampling or zeros of entire functions under structural assumptions. None can replace the temporal self-zero sampling that moves with the solution here.`,
  ],
  [
    raw`launch root 单独贡献 \(h(0)^2=1\)。这一步也解释了为何结论不能直接搬到任意复相位目标坐标。`,
    raw`The launch root contributes \(h(0)^2=1\) separately. This step also explains why the conclusion cannot be transferred directly to an arbitrary complex-phase target coordinate.`,
  ],
  [
    raw`producer 的有限 \(\log\delta\) 斜率是 \(0.40754165\)，对照渐近 \(4/\pi^2=0.40528473\)。最大步长压力 \(7.40\times10^{-7}\)，最大半径压力 \(4.39\times10^{-8}\)，horizon tail 为 \(1.67\times10^{-8}\)。这些结果只审计实现和有限渐近，不替代解析证明，也不是区间证书。两次失败的初始压力测试连同修正原因都保留在证书目录中。`,
    raw`The producer's finite \(\log\delta\) slope is \(0.40754165\), compared with the asymptotic value \(4/\pi^2=0.40528473\). The maximum step-size stress is \(7.40\times10^{-7}\), the maximum radius stress is \(4.39\times10^{-8}\), and the horizon tail is \(1.67\times10^{-8}\). These results audit only the implementation and finite asymptotics; they neither replace the analytic proof nor constitute interval certificates. Both failed initial stress tests and the reasons for their corrections are retained in the certificate directory.`,
  ],
  [
    raw`R0.72E 已给 \(\int_0^Xq\lesssim(1+\log(2+\delta))/\delta\)，所以 \(G_{\rm all}\lesssim1+\log(2+\delta)\)。常数不依赖根数或根间距。`,
    raw`R0.72E gives \(\int_0^Xq\lesssim(1+\log(2+\delta))/\delta\), hence \(G_{\rm all}\lesssim1+\log(2+\delta)\). The constant is independent of root count and root spacing.`,
  ],
  [
    raw`R0.72E 只需要 selected roots 就足以排除无权 payment；R0.72F 用同一 selected family 选出 critical-log repair。R0.72G 进一步证明，遗漏的根不会让这条 exact family 重新击穿修正。于是这条测试序列现在同时给出 complete-root 上界和匹配下界。`,
    raw`R0.72E needs only selected roots to exclude the unweighted payment; R0.72F uses the same selected family to choose the critical-log repair. R0.72G further proves that the omitted roots do not let this exact family break the repair again. This test sequence now provides both a complete-root upper bound and a matching lower bound.`,
  ],
  [
    raw`R0.72F 留下的疑问是：selected Bessel neighborhoods 之外的根，会不会藏着更大的斜率质量。我在精确实单载波格点上不再计数根，也不假设根分离；实相位 gauge、目标行恒等式与 Rolle–BV 归约直接把全部根压到完整 \(H^{-1}\) action。结果是 \(G_{\rm all}\asymp\log\delta\)，critical-log payment 在这条精确族上成立而且尖锐。`,
    raw`The question left by R0.72F is whether roots outside the selected Bessel neighborhoods hide a larger slope mass. On the exact real one-carrier lattice, I neither count roots nor assume their separation; the real-phase gauge, target-row identities, and Rolle–BV reduction directly bound every root by the complete \(H^{-1}\) action. The result is \(G_{\rm all}\asymp\log\delta\): the critical-log payment holds and is sharp on this exact family.`,
  ],
  [
    raw`R0.72G · 2026-08-27 · 个人数学研究日志`,
    raw`R0.72G · 2026-08-27 · Personal mathematics research log`,
  ],
  [
    raw`R0.72G｜精确单载波上的完整根打包`,
    raw`R0.72G | Complete-root packing on the exact one-carrier ray`,
  ],
  [
    raw`R0.72H 转向有限实多载波的混合行`,
    raw`R0.72H turns to the mixed row for finitely many real carriers`,
  ],
  [
    raw`selected roots 是 complete roots 的子集，与刚证明的上界合并后，`,
    raw`The selected roots are a subset of the complete roots. Combining them with the upper bound just proved gives`,
  ],
  [
    raw`selected roots 已经把对数上界取到`,
    raw`The selected roots already attain the logarithmic upper bound`,
  ],
  [raw`02 · 97 节完整索引`, raw`02 · Complete 97-note index`],
  [raw`保留 R0.72F 历史回顾`, raw`Retain the historical R0.72F recap`],
  [raw`查看 R0.72G 双路证书`, raw`View the R0.72G dual-path certificates`],
  [raw`打开最新节点 R0.72G`, raw`Open the latest node R0.72G`],
  [
    raw`单载波上的完整根缺口已经封闭，主障碍转到混合行`,
    raw`The one-carrier complete-root gap is closed; the main obstruction moves to the mixed row`,
  ],
  [
    raw`二十三个阶段、97 个节点：从约化递推和时间迹账本，到 unweighted payment 失效，再到 critical-log complete-root 尖锐封闭。`,
    raw`Twenty-three phases and 97 nodes: from reduced recurrences and the temporal-trace ledger, through failure of the unweighted payment, to sharp critical-log complete-root closure.`,
  ],
  [
    raw`公开、完整封存与问题解决继续分开计数`,
    raw`Publication, complete archiving, and solving the problem remain separate counts`,
  ],
  [raw`回顾截止节点：R0.72G`, raw`Recap endpoint: R0.72G`],
  [raw`回顾截止时公开笔记：157`, raw`Public notes at the recap endpoint: 157`],
  [
    raw`截至 R0.72G，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 97 个节点或 59 个公开版本解释成对千禧年问题完成了某个比例。`,
    raw`Through R0.72G, there is no new unconditional continuation criterion, no reduction of the full set of potential singular solutions, and no proof of finite-time breakdown. The 97 nodes or 59 published releases cannot be interpreted as a percentage completion of the Millennium Problem.`,
  ],
  [
    raw`累计回顾 · R0.61–R0.72G · 2026-08-27`,
    raw`Cumulative recap · R0.61–R0.72G · 2026-08-27`,
  ],
  [raw`收录节点：97`, raw`Included nodes: 97`],
  [
    raw`下一有限任务保留 real phase、fixed target 与 full-frequency charge，处理 \(\mathcal E_Q=\int|hQF|\)，其中 \(Q=P_0[V'+V(D+\lambda_0)]\)。目标是证明载波数无关的 critical-log payment，或构造一个显式 growing-carrier 反族。`,
    raw`The next finite task retains the real phase, fixed target, and full-frequency charge and treats \(\mathcal E_Q=\int|hQF|\), where \(Q=P_0[V'+V(D+\lambda_0)]\). The goal is either to prove a critical-log payment independent of carrier count or to construct an explicit growing-carrier counterfamily.`,
  ],
  [
    raw`这是一项精确模型类内部的 sharp trace-packing theorem，不是 regularity theorem。它把下一关从未知根数压缩为有限多载波中一个明确的 mixed-row payment。`,
    raw`This is a sharp trace-packing theorem within an exact model class, not a regularity theorem. It reduces the next gate from an unknown root count to one explicit mixed-row payment for finitely many carriers.`,
  ],
  [
    raw`这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72G 的 97 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。这里的节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。`,
    raw`This page follows the R0.00–R0.60 phase recap and organizes the research nodes from R0.61 through R0.72G, 97 in total. I record chronologically what each segment actually proves, which proposal a specific counterexample or scaling analysis excludes, and which conditions have not yet been derived from the Navier–Stokes equations. The node states describe the type of evidence; they do not misstate release archiving as completion of a phase objective.`,
  ],
  [
    raw`这一步不会先假定一般三维 Hilbert trace theorem，也不会换掉 critical-log candidate。只有多载波关口完成后，才有理由讨论 restart covering 与一般三维传递。`,
    raw`This step will neither assume a general three-dimensional Hilbert trace theorem in advance nor replace the critical-log candidate. Only after the multi-carrier gate is completed is there reason to discuss restart covering and transfer to general three-dimensional dynamics.`,
  ],
  [
    raw`R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 97 个节点沿着这个缺口推进；R0.70A–R0.72G 的 59 个版本已经公开；其中 35 个满足当前 formal-figure 完整封存合同，但其中仍包含条件定理、反例、有限诊断和开放缺口。`,
    raw`The R0.00–R0.60 material remains in the previous phase recap. R0.60 concludes that the full Fourier–Leray structure and higher-order computations can continue, but no critical quantity for general three-dimensional solutions is yet controlled. The subsequent 97 nodes advance along this gap; the releases from R0.70A through R0.72G, 59 in total, are published, of which 35 satisfy the current formal-figure complete-archive contract. They still include conditional theorems, counterexamples, finite diagnostics, and open gaps.`,
  ],
  [
    raw`R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72G 的 97 个研究节点；最新一节在精确实单载波族上封闭完整根打包并证明 critical-log 尖锐饱和。`,
    raw`Research recap after R0.60: complete coverage from R0.61 through R0.72G, comprising 97 research nodes; the latest section closes complete-root packing on the exact real one-carrier family and proves sharp critical-log saturation.`,
  ],
  [
    raw`R0.61–R0.72G 的 97 节公开笔记`,
    raw`Public notes from R0.61 through R0.72G: 97`,
  ],
  [raw`R0.61–R0.72G 回顾 · 2026-08-27`, raw`R0.61–R0.72G recap · 2026-08-27`],
  [raw`R0.61–R0.72G 研究节点`, raw`R0.61–R0.72G research nodes`],
  [
    raw`R0.61–R0.72G｜R0.60 之后的研究回顾`,
    raw`R0.61–R0.72G | Research recap after R0.60`,
  ],
  [
    raw`R0.70A–R0.72G 的 59 节 HTML/PDF 与研究源稿列入公开路线。按当前 formal-figure 合同，35 节完整封存；24 节较早版本仍缺 formal 状态或正式附图包，列入可审计的旧档回补清单。公开页存在不等于档案合同完整。`,
    raw`The releases from R0.70A through R0.72G comprise 59 HTML/PDF releases and research source files on the published route. Under the current formal-figure contract, 35 are fully archived; 24 earlier releases still lack formal status or a formal figure package and remain on an auditable legacy-backfill list. A public page does not by itself mean that the archive contract is complete.`,
  ],
  [raw`R0.70A–R0.72G 已公开版本`, raw`Published releases R0.70A–R0.72G`],
  [
    raw`R0.72E 排除 unweighted candidate；R0.72F 选出 critical-log 最小修正；R0.72G 又证明，在制造原反例的 exact one-carrier ray 上，遗漏的根不会击穿这一修正。这里的完整根质量恰是对数量级，原始幅度序列使两边同阶。`,
    raw`R0.72E excludes the unweighted candidate; R0.72F selects the minimal critical-log repair; and R0.72G proves that, on the exact one-carrier ray that generated the original counterexample, the omitted roots do not break this repair. The complete root mass has exactly logarithmic order there, and the original amplitude sequence makes both sides comparable in order.`,
  ],
  [
    raw`R0.72F 对 \(w_{\beta,\gamma}(s)=s^{-\beta}[1+\log(1/s)]^\gamma\) 分别计算 Leray payment 与 selected Bessel obstruction：能量支付要求 \(\beta<1/2\)，exact family 强制 \(\beta>1/3\)，或在端点取 \(\gamma\ge1\)。最小共同边界是 \(w_*(s)=s^{-1/3}[1+\log(1/s)]\)。`,
    raw`R0.72F separately computes the Leray payment and selected Bessel obstruction for \(w_{\beta,\gamma}(s)=s^{-\beta}[1+\log(1/s)]^\gamma\): energy payment requires \(\beta<1/2\), while the exact family requires \(\beta>1/3\), or \(\gamma\ge1\) at the endpoint. The minimal common boundary is \(w_*(s)=s^{-1/3}[1+\log(1/s)]\).`,
  ],
  [
    raw`R0.72F–R0.72G · 临界对数候选与完整根封闭`,
    raw`R0.72F–R0.72G · Critical-log candidate and complete-root closure`,
  ],
  [
    raw`R0.72G 的 exact one-carrier complete-root theorem：实相位 gauge、两个目标行恒等式与 Rolle–BV 归约给出根数无关的 \(G_{\rm all}\lesssim\log\delta\)；selected Bessel roots 给匹配下界。原始幅度序列上 \(\mathcal J_{\rm all}\asymp D^{1/3}\Lambda_{1,*}\asymp\delta\)，所以 critical-log payment 对完整根集尖锐。结论只覆盖固定 \(q_0\)、实单载波、\(\delta\ge1\) 与 \(A_\delta=O(\delta)\)；多载波和一般三维传递仍开放。`,
    raw`R0.72G exact one-carrier complete-root theorem: the real-phase gauge, two target-row identities, and the Rolle–BV reduction give \(G_{\rm all}\lesssim\log\delta\) independently of root count, while the selected Bessel roots give a matching lower bound. On the original amplitude sequence, \(\mathcal J_{\rm all}\asymp D^{1/3}\Lambda_{1,*}\asymp\delta\), so the critical-log payment is sharp on the complete root set. The conclusion covers only fixed \(q_0\), one real carrier, \(\delta\ge1\), and \(A_\delta=O(\delta)\); multi-carrier and general three-dimensional transfer remain open.`,
  ],
  [
    raw`R0.72G 的定理限于精确实单载波三角形 2.5D 光滑解族。本回顾没有证明三维 Navier–Stokes 的全局光滑性或有限时破裂；Clay 正式问题仍然开放。`,
    raw`The R0.72G theorem is limited to the exact real one-carrier triangular 2.5D smooth-solution family. This recap does not prove global smoothness or finite-time breakdown for the three-dimensional Navier–Stokes equations; the formal Clay problem remains open.`,
  ],
  [raw`R0.72G 附图`, raw`R0.72G figure`],
  [
    raw`R0.72G 固定这个候选，不再预选根。在精确实单载波格点上，phase gauge、目标行恒等式与 Rolle–BV 归约给出不依赖根数和根间距的 \(G_{\rm all}\lesssim\log\delta\)；selected Bessel roots 给匹配下界。原始幅度序列上，完整物理 root ledger 与 \(D^{1/3}\Lambda_{1,*}\) 同阶。下一障碍转到有限实多载波的 mixed row；一般三维传递仍开放。`,
    raw`R0.72G fixes this candidate and no longer preselects roots. On the exact real one-carrier lattice, the phase gauge, target-row identities, and Rolle–BV reduction give \(G_{\rm all}\lesssim\log\delta\) independently of root count and spacing, while the selected Bessel roots give a matching lower bound. On the original amplitude sequence, the complete physical root ledger has the same order as \(D^{1/3}\Lambda_{1,*}\). The next obstruction moves to the mixed row for finitely many real carriers; general three-dimensional transfer remains open.`,
  ],
  [raw`R0.72G 证书`, raw`R0.72G certificates`],
  [
    raw`R0.72H 检查有限实多载波 mixed row`,
    raw`R0.72H tests the mixed row for finitely many real carriers`,
  ],
  [
    raw`保留 real phase、fixed target 与 full-frequency charge，证明 \(\mathcal E_Q=\int|hQF|\) 可由 critical-log action 以载波数无关常数支付，或给出显式 growing-carrier 反族。`,
    raw`Retain the real phase, fixed target, and full-frequency charge, and either prove that \(\mathcal E_Q=\int|hQF|\) is paid by the critical-log action with a carrier-count-independent constant or give an explicit growing-carrier counterfamily.`,
  ],
  [
    raw`处理有限实多载波的新 mixed row \(\mathcal E_Q=\int|hQF|\)，要求 dimension-free payment 或显式 growing-carrier 反族。`,
    raw`Treat the new mixed row \(\mathcal E_Q=\int|hQF|\) for finitely many real carriers, requiring either a dimension-free payment or an explicit growing-carrier counterfamily.`,
  ],
  [
    raw`从候选 payment 失效走到 critical-log complete-root 尖锐封闭`,
    raw`From failure of the candidate payment to sharp critical-log complete-root closure`,
  ],
  [
    raw`定理只覆盖固定 \(q_0\)、\(\delta\ge1\)、实单载波与 \(A_\delta=O(\delta)\) 的 exact triangular 2.5D 光滑解族；不是一般三维 continuation theorem，也没有解决千禧年问题。`,
    raw`The theorem covers only fixed \(q_0\), \(\delta\ge1\), one real carrier, and \(A_\delta=O(\delta)\) within an exact triangular 2.5D smooth-solution family. It is not a general three-dimensional continuation theorem and does not solve the Millennium Problem.`,
  ],
  [
    raw`环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \(M^{-2}\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → phase-uniform \(M^{-8/3}\) sharp algebraic prefactor → shifted Rudin–Shapiro heat pulse → positive-time simple root → full-charge normalized order-one saturation → fixed-carrier shell isolation → negative-Sobolev action decay → candidate D^{1/3}Λ₁ payment failure → critical-log repair → selected-family frontier → complete-root Rolle–BV closure → sharp critical-log saturation`,
    raw`annular exclusion → source–kernel ledger → covariance-spectrum stratification → all-frequency conditional bridge → response-slope chord gain → common-response order-one channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \(M^{-2}\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → sharp phase-uniform \(M^{-8/3}\) algebraic prefactor → shifted Rudin–Shapiro heat pulse → positive-time simple root → full-charge normalized order-one saturation → fixed-carrier shell isolation → negative-Sobolev action decay → candidate D^{1/3}Λ₁ payment failure → critical-log repair → selected-family frontier → complete-root Rolle–BV closure → sharp critical-log saturation`,
  ],
  [
    raw`精确实单载波上的完整根斜率质量恰为对数量级`,
    raw`The complete root-slope mass on the exact real one-carrier ray has exactly logarithmic order`,
  ],
  [
    raw`静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71U–Z 依次处理 second-time jet、complete first row、fixed-small-coupling endpoint、selected roots 与 complete roots。R0.72A–C 建立 Bessel lower family、target-row participation 与 physical-phase sharp scales；R0.72D 再实现 positive-time root 与 full-charge order-one saturation。R0.72E 固定 \(q_0>R_*\)，用 Feynman–Kac、驻相和定量 Hörmander density 控制完整 \(H^{-1}\) action；exact one-carrier family 最终使 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。R0.72F 随后证明 selected roots 强制 \(1/3\) 下端点，而 Leray energy 只支付到 \(1/2\)；最小边界修正是 \(s^{-1/3}[1+\log(1/s)]\)。R0.72G 固定这一候选，用实相位 gauge、目标行恒等式与 Rolle–BV 归约证明完整根质量 \(G_{\rm all}\asymp\log\delta\)，并在原始幅度序列上得到 complete-root sharp saturation。`,
    raw`After the static annular family is rigorously excluded, the main route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71U–Z treats the second-time jet, complete first row, fixed-small-coupling endpoint, selected roots, and complete roots. R0.72A–C develops the Bessel lower family, target-row participation, and sharp physical-phase scales; R0.72D then realizes a positive-time root and full-charge order-one saturation. R0.72E fixes \(q_0>R_*\) and controls the complete \(H^{-1}\) action using Feynman–Kac, stationary phase, and a quantitative Hörmander density bound; the exact one-carrier family ultimately makes the complete-root ledger relative to the candidate \(D^{1/3}\Lambda_1\) payment diverge as \(R^{4/3}\). R0.72F then proves that selected roots require the lower endpoint \(1/3\), while Leray energy pays only up to \(1/2\); the minimal boundary repair is \(s^{-1/3}[1+\log(1/s)]\). R0.72G fixes this candidate and uses the real-phase gauge, target-row identities, and the Rolle–BV reduction to prove \(G_{\rm all}\asymp\log\delta\), obtaining sharp complete-root saturation on the original amplitude sequence.`,
  ],
  [
    raw`累计回顾 R0.61–R0.72G · 2026-08-27`,
    raw`Cumulative recap R0.61–R0.72G · 2026-08-27`,
  ],
  [
    raw`累计回顾保持二十三个问题阶段，完整覆盖 R0.61–R0.72G。R0.72E 排除 unweighted payment，R0.72F 选出 critical-log 最小修正，R0.72G 在 exact real one-carrier ray 上封闭 complete roots 并证明尖锐饱和。R0.70A–R0.72G 共 59 个版本已公开；按当前 formal-figure 合同有 35 个完整封存，24 个旧版附图档案列入回补清单。`,
    raw`The cumulative recap retains twenty-three problem phases and covers R0.61–R0.72G in full. R0.72E excludes the unweighted payment, R0.72F selects the minimal critical-log repair, and R0.72G closes the complete roots and proves sharp saturation on the exact real one-carrier ray. The releases from R0.70A through R0.72G number 59 and are published; under the current formal-figure contract, 35 are fully archived and 24 legacy figure archives are listed for backfill.`,
  ],
  [
    raw`目前没有新的无条件继续性判据，也没有构造有限时奇性。下一障碍是有限实多载波 mixed row 的维数无关支付，不是重复单载波根扫描。`,
    raw`There is currently no new unconditional continuation criterion and no construction of a finite-time singularity. The next obstruction is dimension-independent payment of the mixed row for finitely many real carriers, not another one-carrier root scan.`,
  ],
  [raw`上次综述 v1.19 · 2026-08-27`, raw`Previous review v1.19 · 2026-08-27`],
  [
    raw`我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.72G 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。`,
    raw`I maintain a separate systematic review that places classical theory, five main literature lines, the candidate-blowup exclusion tree, developments from 2019–2026, and the R0.69P–R0.72G route on this site in one diagram. Historical nodes R0.61–R0.69O remain in the cumulative recap.`,
  ],
  [raw`下一步 R0.72H：`, raw`Next step R0.72H:`],
  [
    raw`写 \(f=F_0\)、\(h=P_0VF\)、\(q=\lVert VF\rVert_{A_\mu^{-1}}^2\)。实相位 gauge 给 \(f,h\in\mathbb R\)，目标行恒等式与 Rolle–BV 归约给`,
    raw`Write \(f=F_0\), \(h=P_0VF\), and \(q=\lVert VF\rVert_{A_\mu^{-1}}^2\). The real-phase gauge gives \(f,h\in\mathbb R\), and the target-row identities together with the Rolle–BV reduction give`,
  ],
  [raw`研究笔记 R0.72G · 2026-08-27`, raw`Research note R0.72G · 2026-08-27`],
  [raw`阅读 R0.72G 研究笔记 →`, raw`Read the R0.72G research note →`],
  [raw`展开 67 篇公开笔记`, raw`Expand 67 public notes`],
  [raw`综述 v1.20 · 2026-08-27`, raw`Review v1.20 · 2026-08-27`],
  [
    raw`exact real one-carrier ray 上的全部根由 Rolle–BV 与完整 action 支付；critical-log payment 对 complete roots 尖锐。`,
    raw`Every root on the exact real one-carrier ray is paid by Rolle–BV and the complete action; the critical-log payment is sharp for the complete roots.`,
  ],
  [
    raw`R0.60 recap 之后的累计回顾收录 97 个节点；全站现有 157 篇公开研究笔记`,
    raw`The cumulative recap after R0.60 contains 97 nodes; the site now has 157 public research notes`,
  ],
  [
    raw`R0.70A–R0.72G：59 节已公开，35 节完整封存`,
    raw`R0.70A–R0.72G: 59 published, 35 fully archived`,
  ],
  [raw`R0.72G 已完成：`, raw`R0.72G complete:`],
  [
    raw`R0.72G 已在精确实单载波族上封闭 complete-root trace packing，并证明 critical-log payment 尖锐；下一步只审有限实多载波的新 mixed row。`,
    raw`R0.72G closes complete-root trace packing on the exact real one-carrier family and proves the critical-log payment sharp; the next step audits only the new mixed row for finitely many real carriers.`,
  ],
  [
    raw`selected Bessel roots 给匹配下界，所以 \(G_{\rm all}(\delta_R;X)\asymp\log\delta_R\)。原始幅度序列上，\(\mathcal J_{\rm all}\asymp D^{1/3}\Lambda_{1,*}\asymp\delta_R\)：critical-log repair 对完整根集成立并尖锐。`,
    raw`The selected Bessel roots give a matching lower bound, so \(G_{\rm all}(\delta_R;X)\asymp\log\delta_R\). On the original amplitude sequence, \(\mathcal J_{\rm all}\asymp D^{1/3}\Lambda_{1,*}\asymp\delta_R\): the critical-log repair holds and is sharp on the complete root set.`,
  ],
]);

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

const snapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
if (!Array.isArray(snapshot) || snapshot.length !== 138) {
  throw new Error(
    "R0.72G snapshot cardinality drift: " +
      (Array.isArray(snapshot) ? snapshot.length : "not-an-array"),
  );
}
if (translationsByChinese.size !== 138) {
  throw new Error(
    "R0.72G translation-map cardinality drift: " +
      translationsByChinese.size,
  );
}

for (const [field, values] of [
  ["snapshot key", snapshot.map((entry) => entry.zh)],
  ["translation key", [...translationsByChinese.keys()]],
]) {
  const duplicates = duplicateValues(values);
  if (duplicates.length) {
    throw new Error("Duplicate " + field + " values: " + duplicates.join(" | "));
  }
}

const snapshotByChinese = new Map(snapshot.map((entry) => [entry.zh, entry]));
const missingMappings = snapshot.filter(
  (entry) => !translationsByChinese.has(entry.zh),
);
const extraMappings = [...translationsByChinese.keys()].filter(
  (zh) => !snapshotByChinese.has(zh),
);
if (missingMappings.length || extraMappings.length) {
  throw new Error(
    "R0.72G snapshot/map key drift:\nMISSING " +
      missingMappings.map((entry) => entry.zh).join(" | ") +
      "\nEXTRA " +
      extraMappings.join(" | "),
  );
}

const translations = JSON.parse(await readFile(translationsPath, "utf8"));
const source = await collectSiteStrings(publicDirectory);
const sourceByChinese = new Map(source.map((entry) => [entry.zh, entry]));
const existingByChinese = new Map(
  translations.map((entry) => [entry.zh, entry]),
);

for (const entry of snapshot) {
  const live = sourceByChinese.get(entry.zh);
  if (
    !live ||
    live.count !== entry.count ||
    JSON.stringify(live.files) !== JSON.stringify(entry.files)
  ) {
    throw new Error(
      "R0.72G live-source drift for snapshot key:\n" +
        entry.zh +
        "\nSNAPSHOT " +
        JSON.stringify({ count: entry.count, files: entry.files }) +
        "\nLIVE " +
        JSON.stringify(live ?? null),
    );
  }
}

const missing = source.filter((entry) => !existingByChinese.has(entry.zh));
const unmapped = missing.filter(
  (entry) => !translationsByChinese.has(entry.zh),
);
if (unmapped.length) {
  throw new Error(
    "R0.72G translation source drift (" +
      unmapped.length +
      " unmapped live strings):\n" +
      unmapped.map((entry) => entry.zh).join("\n---\n"),
  );
}

const rows = snapshot.map((entry, index) => [
  `r072g${String(index + 1).padStart(3, "0")}`,
  entry.zh,
  translationsByChinese.get(entry.zh),
]);

for (const [id, zh, en] of rows) {
  if (!sourceByChinese.has(zh)) {
    throw new Error("R0.72G mapped source is no longer live: " + zh);
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
      "Existing R0.72G translation drift for " +
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
    "R0.72G full-site missing-after check failed (" +
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
