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
  "r072f-missing.json",
);

const raw = String.raw;
const englishByChinese = new Map([
  [
    raw`本节的 Leray payment 是 Sobolev 对偶、插值和能量不等式的直接推导；critical-log selected-family law 来自 R0.72E exact family。核对的一手来源不陈述 complete-root candidate，也不支持把通过两项筛查升级为 continuation criterion。文献审计是截至 2026-08-27 的 bounded non-collision check，不是原创性、优先权或穷尽性声明。`,
    raw`The Leray payment in this section follows directly from Sobolev duality, interpolation, and the energy inequality; the critical-log selected-family law comes from the R0.72E exact family. The primary sources checked do not state a complete-root candidate, nor do they support upgrading success in two screens to a continuation criterion. The literature audit is a bounded non-collision check through 2026-08-27, not a claim of novelty, priority, or exhaustiveness.`,
  ],
  [raw`打开 96 节完整索引`, raw`Open the complete 96-note index`],
  [raw`的 critical (BMO^{-1}) solution space、`, raw`'s critical (BMO^{-1}) solution space,`],
  [
    raw`的 filtered palinstrophy defect 都提供邻近结构，但没有一项同时给出 arbitrary large-data/Leray payment、fixed-support amplitude coupling detection 与 distinguished temporal zero-level squared-slope ledger。`,
    raw`'s filtered palinstrophy defect all provide nearby structures, but none simultaneously supplies arbitrary large-data/Leray payment, fixed-support amplitude-coupling detection, and a distinguished temporal zero-level squared-slope ledger.`,
  ],
  [raw`的 quantitative regularity framework、`, raw`'s quantitative regularity framework,`],
  [raw`的 time-weighted nonlinear remainder、`, raw`'s time-weighted nonlinear remainder,`],
  [raw`的动态频率 occupation 与`, raw`'s dynamic frequency occupation, and`],
  [
    raw`固定 critical-log weight，检查全部 roots、restart covering 与 left-end cost；不再更换候选。`,
    raw`Fix the critical-log weight and test every root, restart covering, and left-end cost; the candidate will not be changed again.`,
  ],
  [raw`开放接口 · R0.72G`, raw`Open interface · R0.72G`],
  [raw`累计回顾与 96 节索引`, raw`Cumulative recap and 96-note index`],
  [raw`文献综述 v1.19 · 2026-08-27`, raw`Literature review v1.19 · 2026-08-27`],
  [
    raw`我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.72F 只列为研究笔记。我不把计算或笔记外推成正则性定理。`,
    raw`I list published theorems as known results, mark 2026 preprints separately, and list R0.69P–R0.72F on this site only as research notes. I do not extrapolate computations or notes into regularity theorems.`,
  ],
  [
    raw`中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–U 给出 conditional incidence、genuine internal-entry、second-time-jet 与 finite recurrence 边界。R0.71V–W 分离 fixed zero-level trace 并排除 data-uniform complete first-row ledger。R0.71X 在 fixed-dimensional small-coupling family 内达到 one-third endpoint；R0.71Y 处理 selected roots；R0.71Z 给出 all-root slope-mass bound 和 launch-inclusive floor cancellation；R0.72A 把 strong-coupling loss 局部化到实际观察层，R0.72B 保留 exact target-row participation，R0.72C 得到 phase-uniform exact-launch \(M^{-8/3}\) 与 fixed-positive tail \(M^{-3}\) 的 sharp algebraic scales。R0.72D 在 shifted Rudin–Shapiro family 上构造 positive-time exact root，保留 full rotational charge，并得到非消失但不发散的 normalized complete-root ledger。R0.72E 回到 fixed-carrier Bessel family，以定量 negative-Sobolev action 证明 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。R0.72F 再用 regularly varying initial-layer weights 分离 selected-root 的 \(1/3\) 阈值与 Leray payment 的 \(1/2\) 阈值，并选出 critical-log 最小边界。一般 Navier–Stokes 正则性仍开放。`,
    raw`. R0.69P–R0.71P reaches the positive-entry temporal-packing boundary; R0.71Q–U establishes the boundaries for conditional incidence, genuine internal entries, the second-time jet, and finite recurrence. R0.71V–W separates the fixed zero-level trace and excludes a data-uniform complete first-row ledger. R0.71X reaches the one-third endpoint in a fixed-dimensional small-coupling family; R0.71Y treats selected roots; R0.71Z gives an all-root slope-mass bound and launch-inclusive floor cancellation. R0.72A localizes the strong-coupling loss to the actual observation layer, R0.72B retains exact target-row participation, and R0.72C obtains the sharp phase-uniform exact-launch \(M^{-8/3}\) and fixed-positive-tail \(M^{-3}\) algebraic scales. R0.72D constructs a positive-time exact root in a shifted Rudin–Shapiro family, retains the full rotational charge, and obtains a nonvanishing but nondivergent normalized complete-root ledger. R0.72E returns to a fixed-carrier Bessel family and uses a quantitative negative-Sobolev action estimate to make the complete-root ledger relative to the candidate \(D^{1/3}\Lambda_1\) payment diverge as \(R^{4/3}\). R0.72F then uses regularly varying initial-layer weights to separate the selected-root threshold \(1/3\) from the Leray-payment threshold \(1/2\), selecting the minimal critical-log boundary. General Navier–Stokes regularity remains open.`,
  ],
  [raw`critical-log initial-layer repair 与可行窗口`, raw`Critical-log initial-layer repair and viable window`],
  [raw`R0.72F 的 weighted-action 与时间迹边界`, raw`R0.72F weighted-action and temporal-trace boundary`],
  [raw`R0.72F 的主源边界`, raw`R0.72F primary-source boundary`],
  [
    raw`selected Bessel roots 强制 \(\beta\ge1/3\)，纯幂端点还需 \(\gamma\ge1\)；Leray energy 只支付 \(\beta<1/2\)。最小边界权重是 \(s^{-1/3}[1+\log(1/s)]\)。这只通过两项筛查，不是 complete-root theorem。`,
    raw`The selected Bessel roots require \(\beta\ge1/3\), with \(\gamma\ge1\) also required at the pure-power endpoint; Leray energy pays only for \(\beta<1/2\). The minimal boundary weight is \(s^{-1/3}[1+\log(1/s)]\). This passes only two screens and is not a complete-root theorem.`,
  ],
  [
    raw`\[ \boxed{2a+c+\beta>1, \quad\text{或}\quad2a+c+\beta=1\ \text{且}\ \gamma\ge1.} \]`,
    raw`\[ \boxed{2a+c+\beta>1, \quad\text{or}\quad2a+c+\beta=1\ \text{and}\ \gamma\ge1.} \]`,
  ],
  [raw`01 · Leray 支付`, raw`01 · Leray payment`],
  [raw`02 · 精确族阈值`, raw`02 · Exact-family threshold`],
  [raw`03 · 统一边界`, raw`03 · Unified frontier`],
  [raw`04 · 双路证书`, raw`04 · Dual-path certificates`],
  [raw`05 · 正式附图`, raw`05 · Formal figure`],
  [
    raw`512-mode time-dependent Strang split-step Fourier；每一步对奇异权重使用精确零阶和一阶矩。临界归一化从 41.0235 变到 44.1958；fine/coarse 最大相对差 \(1.27\times10^{-3}\)。`,
    raw`A 512-mode time-dependent Strang split-step Fourier method uses exact zeroth and first moments for the singular weight at every step. The critical normalization changes from 41.0235 to 44.1958; the maximum fine/coarse relative difference is \(1.27\times10^{-3}\).`,
  ],
  [
    raw`把 active amplitude \(X_\delta=S_\delta^2\) 留作自由参数。对 \(0<\beta<1\)，选择 \(X_\delta=\delta^{1-\beta}(\log\delta)^{-\gamma}\) 让 action 保持有界。若数据坐标为 \(\mathfrak C\asymp\delta^2\)、coupling 坐标为 \(\Gamma\asymp\delta\)，则 raw selected ledger 强制`,
    raw`Leave the active amplitude \(X_\delta=S_\delta^2\) as a free parameter. For \(0<\beta<1\), choose \(X_\delta=\delta^{1-\beta}(\log\delta)^{-\gamma}\) so that the action stays bounded. If the data coordinate is \(\mathfrak C\asymp\delta^2\) and the coupling coordinate is \(\Gamma\asymp\delta\), then the raw selected ledger requires`,
  ],
  [raw`版本 v0.72F · 2026-08-27`, raw`Version v0.72F · 2026-08-27`],
  [
    raw`对 \(I=[a,a+T]\)，令 \(Y=\|\omega\|_2^2\)、\(L=\mathbb P(u\times\omega)\)，并定义`,
    raw`For \(I=[a,a+T]\), set \(Y=\|\omega\|_2^2\) and \(L=\mathbb P(u\times\omega)\), and define`,
  ],
  [
    raw`固定初始 Fourier 支撑的有限个振幅归一化频率矩都趋向常数，因此看不见这一 amplitude-driven 时间尺度。`,
    raw`Any finite collection of amplitude-normalized frequency moments with fixed initial Fourier support tends to constants and therefore cannot detect this amplitude-driven time scale.`,
  ],
  [
    raw`价值不在于增加一个任意强范数，而在于同时给出必要下端点、可支付上端点和最小边界权重。R0.72E 的失败现在被压缩成一个明确问题：critical-log action 是否足以支付完整 raw root ledger。`,
    raw`The value does not lie in adding an arbitrarily strong norm, but in obtaining a necessary lower endpoint, a payable upper endpoint, and the minimal boundary weight together. The R0.72E failure is now reduced to one precise question: whether the critical-log action can pay for the complete raw root ledger.`,
  ],
  [
    raw`仅凭 \(Y\in L_t^1\)，端点不能延长到 \(\beta\ge1/2\)。用于说明尖锐性的 \(Y(t)=t^{-p}\) 和 \(Y(t)=1/[t\log^2(e/t)]\) 只是标量预算轮廓，不是 Navier–Stokes 涡量轨道。`,
    raw`From \(Y\in L_t^1\) alone, the endpoint cannot be extended to \(\beta\ge1/2\). The profiles \(Y(t)=t^{-p}\) and \(Y(t)=1/[t\log^2(e/t)]\), used to show sharpness, are only scalar budget profiles and are not Navier–Stokes vorticity trajectories.`,
  ],
  [raw`精确族`, raw`Exact family`],
  [raw`两道阈值之间，`, raw`Between the two thresholds,`],
  [
    raw`两路所有权重、所有六个 \(\delta\) 点的最大逐点相对差为 \(4.76\times10^{-4}\)。独立路径的半径压力小于 \(1.28\times10^{-7}\)，容差压力小于 \(6.64\times10^{-7}\)，最大格点边界能量分数小于 \(8.47\times10^{-42}\)。这些是 binary64 有限审计，不是区间证明。`,
    raw`Across every weight and all six \(\delta\) values, the maximum pointwise relative difference between the two paths is \(4.76\times10^{-4}\). The independent path has radius stress below \(1.28\times10^{-7}\), tolerance stress below \(6.64\times10^{-7}\), and maximum lattice-edge energy fraction below \(8.47\times10^{-42}\). These are finite binary64 audits, not interval proofs.`,
  ],
  [
    raw`两种演化与两种奇点求积给出一致的有限审计`,
    raw`Two evolution methods and two singular quadratures give consistent finite audits`,
  ],
  [
    raw`临界对数权重是两项有限筛查共同允许的最小边界候选`,
    raw`The critical-log weight is the minimal boundary candidate admitted by both finite screens`,
  ],
  [
    raw`能量级信息给出严格的 \(1/2\) 上端点`,
    raw`Energy-level information gives the strict upper endpoint \(1/2\)`,
  ],
  [
    raw`前 \(R\) 个 selected roots 的质量为 \(\mathcal J_{{\rm sel},R}\asymp\delta_R\)，而 \(D_R^{1/3}\asymp\delta_R^{2/3}\)。因此`,
    raw`The mass of the first \(R\) selected roots is \(\mathcal J_{{\rm sel},R}\asymp\delta_R\), while \(D_R^{1/3}\asymp\delta_R^{2/3}\). Therefore`,
  ],
  [
    raw`三种修正位于同一个增广多项式边界`,
    raw`Three repairs lie on the same augmented polynomial frontier`,
  ],
  [
    raw`实不变格点上的 implicit BDF；沿自适应网格作 Gauss–Legendre 求积，并用 \(x=e^{-z}\) 处理 launch tail。临界归一化从 41.0430 变到 44.2103。`,
    raw`An implicit BDF method on the real invariant lattice uses Gauss–Legendre quadrature along an adaptive grid and treats the launch tail with \(x=e^{-z}\). The critical normalization changes from 41.0430 to 44.2103.`,
  ],
  [
    raw`所有 \(\beta<1/3\) 失败；\(\beta=1/3\) 时 \(\gamma<1\) 失败。\(w_*\) 使这一个 selected ratio 保持常数量级，但没有控制 selected neighborhoods 之外的其他根。`,
    raw`Every \(\beta<1/3\) fails; at \(\beta=1/3\), every \(\gamma<1\) fails. The weight \(w_*\) keeps this selected ratio at constant order but does not control roots outside the selected neighborhoods.`,
  ],
  [raw`统一边界`, raw`Unified frontier`],
  [
    raw`图 R0.72F-1。左：selected-root 与 Leray-payment 阈值；中：producer 与 independent 的临界归一化；右：增广 frontier 的三个修正顶点。图中有限值只佐证解析标度。`,
    raw`Figure R0.72F-1. Left: selected-root and Leray-payment thresholds. Center: the producer and independent critical normalizations. Right: three repair vertices on the augmented frontier. The finite values in the figure only support the analytic scaling.`,
  ],
  [
    raw`下一步固定 \(w_*\)，先在 exact triangular class 内证明或否定`,
    raw`The next step fixes \(w_*\) and first proves or disproves, within the exact triangular class,`,
  ],
  [raw`下一对象：all-root trace packing`, raw`Next object: all-root trace packing`],
  [
    raw`新继续性判据、有限时奇性、一般三维 global regularity、原创性或优先权结论。`,
    raw`a new continuation criterion, a finite-time singularity, general three-dimensional global regularity, or a claim of novelty or priority.`,
  ],
  [
    raw`沿用 R0.72E 的 exact triangular family，固定 \(q_0\)，取 \(\delta_R=R^4\)、\(P_R=q_0^2\delta_R\)、\(S_R^2=\delta_R/\log(2+\delta_R)\)。对每个固定 \(0<\beta<1\)、\(\gamma\ge0\)，解析上下界为`,
    raw`Use the R0.72E exact triangular family, fix \(q_0\), and take \(\delta_R=R^4\), \(P_R=q_0^2\delta_R\), and \(S_R^2=\delta_R/\log(2+\delta_R)\). For every fixed \(0<\beta<1\) and \(\gamma\ge0\), the analytic two-sided bounds are`,
  ],
  [
    raw`研究笔记 R0.72F · CRITICAL LOG · INITIAL LAYER · ENERGY PAYMENT`,
    raw`Research note R0.72F · CRITICAL LOG · INITIAL LAYER · ENERGY PAYMENT`,
  ],
  [
    raw`研究笔记 R0.72F：临界对数初始层权重同时通过 R0.72E selected-root 反例筛查与 Leray 能量支付；完整根估计仍开放。`,
    raw`Research note R0.72F: the critical-log initial-layer weight passes both the R0.72E selected-root counterexample screen and Leray-energy payment; the complete-root estimate remains open.`,
  ],
  [
    raw`有限关口必须包含所有根、restart covering 和 left-end cost。只重复 selected Bessel roots 不算推进。`,
    raw`The finite gate must include every root, restart covering, and left-end cost. Repeating only the selected Bessel roots does not count as progress.`,
  ],
  [
    raw`在历史数据指数 \(a=1/3\) 上，三个边界顶点分别是 critical-log action、\(c=1/3\) coupling payment，以及改变左端根账本后的 \(\alpha=4/9\) atom weight。后两者使用 \(\beta=0\) 的独立对数律，不能被冒充为上式的正 \(\beta\) 端点。`,
    raw`At the historical data exponent \(a=1/3\), the three boundary vertices are the critical-log action, the coupling payment \(c=1/3\), and the atom weight \(\alpha=4/9\), which changes the left-end root ledger. The latter two use the separate logarithmic law for \(\beta=0\) and cannot be presented as the positive-\(\beta\) endpoint of the formula above.`,
  ],
  [
    raw`在强能量不等式成立的每个 restart time \(a\)，Cauchy–Schwarz 随后给`,
    raw`At every restart time \(a\) where the strong energy inequality holds, Cauchy–Schwarz then gives`,
  ],
  [
    raw`这里的“可行”只表示同时没有被当前 selected-root family 排除，而且新增 action 可由 Leray 能量支付。它不表示完整根估计已经成立。`,
    raw`Here, “viable” means only that the present selected-root family does not exclude the candidate and that Leray energy can pay for the added action. It does not mean that the complete-root estimate has been proved.`,
  ],
  [
    raw`这仍没有缩小潜在奇性解的集合，也没有给出 continuation criterion。它只把下一次失败或成功变成一项边界清楚的 trace-packing 定理。`,
    raw`This still does not narrow the set of potential singular solutions or give a continuation criterion. It only turns the next failure or success into a trace-packing theorem with a clear boundary.`,
  ],
  [
    raw`这一节把“怎么修”压成一个可证伪候选`,
    raw`This section reduces “how to repair it” to one falsifiable candidate`,
  ],
  [
    raw`正式附图把两个阈值、有限渐近与三顶点边界分开`,
    raw`The formal figure separates the two thresholds, finite asymptotics, and three-vertex frontier`,
  ],
  [
    raw`证明、文献、双路证书、附图和累计回顾完整保留`,
    raw`The proof, literature, dual-path certificates, figure, and cumulative recap are preserved in full`,
  ],
  [raw`只留下一个临界对数入口`, raw`Only one critical-log entry remains`],
  [raw`状态 · R0.72F 完成`, raw`Status · R0.72F complete`],
  [
    raw`critical-log action 对 complete roots 的上界、restart/dyadic covering、\(\mathcal R_Y\) 的普适支付，以及向非三角形动力学的传递。`,
    raw`an upper bound for complete roots using the critical-log action, restart/dyadic covering, universal payment of \(\mathcal R_Y\), and transfer to nontriangular dynamics.`,
  ],
  [
    raw`Leray 支付、能量信息类的 \(1/2\) 尖锐性、exact family 的 regularly varying action 渐近、selected-family frontier 和 critical-log saturation。`,
    raw`Leray payment, sharpness of \(1/2\) in the energy-information class, the regularly varying action asymptotics of the exact family, the selected-family frontier, and critical-log saturation.`,
  ],
  [
    raw`R0.72E 排除了无权候选 \(D^{1/3}\Lambda_1\)。这一节不任意加一个修正项，而是把初始层权重写成 \(w_{\beta,\gamma}(s)=s^{-\beta}[1+\log(1/s)]^\gamma\)，分别计算 exact Bessel family 的必要阈值和 Leray 能量可以支付的充分阈值。selected roots 强制 \(\beta\ge1/3\)，纯幂端点还缺一个对数；能量只允许 \(\beta<1/2\)。因此最小边界候选是 \(w_*(s)=s^{-1/3}[1+\log(1/s)]\)。`,
    raw`R0.72E excludes the unweighted candidate \(D^{1/3}\Lambda_1\). Instead of adding an arbitrary repair term, this section writes the initial-layer weight as \(w_{\beta,\gamma}(s)=s^{-\beta}[1+\log(1/s)]^\gamma\) and separately computes the necessary threshold for the exact Bessel family and the sufficient threshold payable by Leray energy. The selected roots require \(\beta\ge1/3\), with one logarithm still missing at the pure-power endpoint; energy allows only \(\beta<1/2\). The minimal boundary candidate is therefore \(w_*(s)=s^{-1/3}[1+\log(1/s)]\).`,
  ],
  [
    raw`R0.72F · 2026-08-27 · 个人数学研究日志`,
    raw`R0.72F · 2026-08-27 · Personal mathematics research log`,
  ],
  [
    raw`R0.72F｜临界对数初始层修正与可行窗口`,
    raw`R0.72F | Critical-log initial-layer repair and viable window`,
  ],
  [
    raw`R0.72G 只检查完整根，不再移动候选`,
    raw`R0.72G tests only the complete roots; the candidate stays fixed`,
  ],
  [
    raw`selected Bessel roots 强制 \(1/3\) 与一个端点对数`,
    raw`Selected Bessel roots require \(1/3\) and one endpoint logarithm`,
  ],
  [
    raw`selected-root 阈值为 1/3，能量支付阈值为 1/2；最小边界权重是 s^{-1/3}(1+log(1/s))。`,
    raw`The selected-root threshold is 1/3 and the energy-payment threshold is 1/2; the minimal boundary weight is s^{-1/3}(1+log(1/s)).`,
  ],
  [
    raw`Sobolev 对偶、Hölder 和周期 Gagliardo–Nirenberg 不等式给`,
    raw`Sobolev duality, Hölder, and the periodic Gagliardo–Nirenberg inequality give`,
  ],
  [
    raw`“已公开”和“完整封存”从本版起分开计数`,
    raw`“Published” and “fully archived” are counted separately from this version onward`,
  ],
  [raw`01 · 二十三个研究阶段`, raw`01 · Twenty-three research phases`],
  [raw`02 · 96 节完整索引`, raw`02 · Complete 96-note index`],
  [raw`保留 R0.72E 历史回顾`, raw`Retain the historical R0.72E recap`],
  [raw`查看 R0.72F 双路证书`, raw`View the R0.72F dual-path certificates`],
  [raw`打开最新节点 R0.72F`, raw`Open the latest node R0.72F`],
  [
    raw`当前 formal-figure 合同下完整封存`,
    raw`Fully archived under the current formal-figure contract`,
  ],
  [
    raw`对 \(w_{\beta,\gamma}(s)=s^{-\beta}[1+\log(1/s)]^\gamma\)，Leray 能量在 \(\beta<1/2\) 时支付对应 projected-Lamb action；仅凭 \(Y\in L_t^1\)，这个 \(1/2\) 端点不能改善。R0.72E exact family 则给 \(Q_{\beta,\gamma}\asymp\delta^{\beta-1}(\log\delta)^\gamma\)，使 selected-root ratio 按 \(\delta^{1/3-\beta}(\log\delta)^{1-\gamma}\) 缩放。最小共同边界因此是 \(w_*(s)=s^{-1/3}[1+\log(1/s)]\)，且 \(\|w_*\|_2^2=75\)。`,
    raw`For \(w_{\beta,\gamma}(s)=s^{-\beta}[1+\log(1/s)]^\gamma\), Leray energy pays for the corresponding projected-Lamb action when \(\beta<1/2\); from \(Y\in L_t^1\) alone, this \(1/2\) endpoint cannot be improved. The R0.72E exact family gives \(Q_{\beta,\gamma}\asymp\delta^{\beta-1}(\log\delta)^\gamma\), so the selected-root ratio scales as \(\delta^{1/3-\beta}(\log\delta)^{1-\gamma}\). The minimal common boundary is therefore \(w_*(s)=s^{-1/3}[1+\log(1/s)]\), with \(\|w_*\|_2^2=75\).`,
  ],
  [
    raw`二十三个阶段、96 个节点：从约化递推和 complete-root 账本，到 full-charge saturation，再到候选 D^{1/3}Λ₁ payment 的严格失效。`,
    raw`Twenty-three phases and 96 nodes: from reduced recurrences and the complete-root ledger, through full-charge saturation, to rigorous failure of the candidate D^{1/3}Λ₁ payment.`,
  ],
  [raw`回顾截止节点：R0.72F`, raw`Recap endpoint: R0.72F`],
  [raw`回顾截止时公开笔记：156`, raw`Public notes at the recap endpoint: 156`],
  [
    raw`截至 R0.72F，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 96 个节点或 58 个公开版本解释成对千禧年问题完成了某个比例。`,
    raw`Through R0.72F, there is no new unconditional continuation criterion, no reduction of the full set of potential singular solutions, and no proof of finite-time breakdown. The 96 nodes or 58 published releases cannot be interpreted as a percentage completion of the Millennium Problem.`,
  ],
  [raw`旧版 formal-figure 档案待回补`, raw`Legacy formal-figure archive backlog`],
  [
    raw`累计回顾 · R0.61–R0.72F · 2026-08-27`,
    raw`Cumulative recap · R0.61–R0.72F · 2026-08-27`,
  ],
  [
    raw`若 complete ratio 仍发散，就关闭这一修正；若 exact class 内成立，再检查一般三维 Hilbert trace theorem 和 Leray 级付款。不会再用新的自由参数临时移动候选。`,
    raw`If the complete ratio still diverges, this repair will be closed. If it holds in the exact class, the next checks are a general three-dimensional Hilbert trace theorem and Leray-level payment. No new free parameter will be used to move the candidate provisionally.`,
  ],
  [raw`收录节点：96`, raw`Included nodes: 96`],
  [
    raw`下一有限任务在 exact triangular class 内先证明或否定 \(\mathcal J_{\rm all}\le CD^{1/3}\Lambda_{1,*}\)。证书必须包含 selected neighborhoods 之外的全部根、restart covering 和左端成本。`,
    raw`The next finite task first proves or disproves \(\mathcal J_{\rm all}\le CD^{1/3}\Lambda_{1,*}\) in the exact triangular class. The certificate must include every root outside the selected neighborhoods, restart covering, and the left-end cost.`,
  ],
  [
    raw`允许 active amplitude 自由变化后，正 \(\beta\) raw ledger 的必要边界为 \(2a+c+\beta>1\)，或等号且 \(\gamma\ge1\)。在历史 \(a=1/3\) 上，critical-log action、\(c=1/3\) coupling factor 与改变左端量的 \(\alpha=4/9\) root weight 构成三个增广顶点。当前只通过 selected roots 与 Leray payment 两项筛查；complete-root trace inequality 仍未证明。`,
    raw`Once the active amplitude is allowed to vary freely, the necessary frontier for the positive-\(\beta\) raw ledger is \(2a+c+\beta>1\), or equality with \(\gamma\ge1\). At the historical value \(a=1/3\), the critical-log action, the coupling factor \(c=1/3\), and the root weight \(\alpha=4/9\), which changes the left-end quantity, form three augmented vertices. Only the selected-root and Leray-payment screens have passed; the complete-root trace inequality remains unproved.`,
  ],
  [
    raw`这是一项 proof-route design theorem，不是 regularity theorem。它的价值是禁止继续移动目标，把下一关压成 complete-root trace packing。`,
    raw`This is a proof-route design theorem, not a regularity theorem. Its value is to prevent further movement of the target and reduce the next gate to complete-root trace packing.`,
  ],
  [
    raw`这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72F 的 96 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。这里的节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。`,
    raw`This page follows the R0.00–R0.60 phase recap and organizes the research nodes from R0.61 through R0.72F, 96 in total. I record chronologically what each segment actually proved, which proposals were ruled out by a concrete counterexample or scaling analysis, and which conditions have not been derived from the Navier–Stokes equations. Node status describes the evidence type and does not mistake an archived release for a solved phase objective.`,
  ],
  [
    raw`逐节笔记、证书、正式附图和历史回顾`,
    raw`Section-by-section notes, certificates, formal figures, and historical recaps`,
  ],
  [
    raw`最小修正已经被选定，但完整根桥仍未建立`,
    raw`The minimal repair has been selected, but the complete-root bridge has not been established`,
  ],
  [
    raw`R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 96 个节点沿着这个缺口推进；R0.70A–R0.72F 的 58 个版本已经公开；其中 34 个满足当前 formal-figure 完整封存合同，但其中仍包含条件定理、反例、有限诊断和开放缺口。`,
    raw`The R0.00–R0.60 material remains in the preceding phase recap. The R0.60 conclusion was that the complete Fourier–Leray structure and higher-order calculations could continue, but the critical quantity for general three-dimensional solutions was not controlled. The following 96 nodes advance along this gap; the releases from R0.70A through R0.72F number 58 and are published, and 34 satisfy the current formal-figure full-archive contract. They still include conditional theorems, counterexamples, finite diagnostics, and open gaps.`,
  ],
  [
    raw`R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.72F 的 96 个研究节点；最新一节用单载波 Bessel 根族与完整 H^{-1} action 严格排除候选 D^{1/3}Λ₁ 支付。`,
    raw`Research recap after R0.60: the nodes from R0.61 through R0.72F, 96 in total, are arranged chronologically; the latest segment uses a one-carrier Bessel root family and the complete H^{-1} action to rigorously exclude the candidate D^{1/3}Λ₁ payment.`,
  ],
  [
    raw`R0.61–R0.72F 的 96 节公开笔记`,
    raw`Public notes from R0.61 through R0.72F: 96`,
  ],
  [raw`R0.61–R0.72F 回顾 · 2026-08-27`, raw`R0.61–R0.72F recap · 2026-08-27`],
  [raw`R0.61–R0.72F 研究节点`, raw`R0.61–R0.72F research nodes`],
  [
    raw`R0.61–R0.72F｜R0.60 之后的研究回顾`,
    raw`R0.61–R0.72F | Research recap after R0.60`,
  ],
  [
    raw`R0.70A–R0.72F 的 58 节 HTML/PDF 与研究源稿均已公开。按当前 formal-figure 合同，34 节完整封存；24 节较早版本仍缺 formal 状态或正式附图包，列入可审计的旧档回补清单。公开页存在不等于档案合同完整。`,
    raw`The HTML/PDF notes and research source files from R0.70A through R0.72F, 58 in total, are published. Under the current formal-figure contract, 34 are fully archived; 24 earlier releases still lack formal status or a formal figure package and are listed in an auditable legacy-backfill inventory. A public page does not by itself mean that the archive contract is complete.`,
  ],
  [
    raw`R0.70A–R0.72F 已公开版本`,
    raw`Published releases R0.70A–R0.72F`,
  ],
  [
    raw`R0.72E 排除 unweighted candidate；R0.72F 又证明，任意 regularly varying initial-layer repair 都必须同时跨过 selected-root 的 \(1/3\) 下端点与 Leray payment 的 \(1/2\) 上端点。临界纯幂仍缺一个对数，所以 \(w_*=s^{-1/3}[1+\log(1/s)]\) 是下一步唯一固定候选。`,
    raw`R0.72E excludes the unweighted candidate. R0.72F then proves that every regularly varying initial-layer repair must cross both the selected-root lower endpoint \(1/3\) and the Leray-payment upper endpoint \(1/2\). The critical pure power still lacks one logarithm, so \(w_*=s^{-1/3}[1+\log(1/s)]\) is the only fixed candidate for the next step.`,
  ],
  [
    raw`R0.72F · 临界对数初始层修正与统一 selected-family frontier`,
    raw`R0.72F · Critical-log initial-layer repair and unified selected-family frontier`,
  ],
  [
    raw`R0.72F 的 critical-log repair screen：\(\mathscr A_{\beta,\gamma}\) 在 \(\beta<1/2\) 时由 Leray 能量支付；R0.72E exact family 则强制 \(\beta>1/3\)，或在端点取 \(\gamma\ge1\)。最小边界权重 \(w_*=s^{-1/3}[1+\log(1/s)]\) 恰好饱和 selected obstruction，free-amplitude audit 进一步给出增广必要 frontier。完整根上界、restart covering 与一般三维传递仍开放。`,
    raw`R0.72F critical-log repair screen: Leray energy pays for \(\mathscr A_{\beta,\gamma}\) when \(\beta<1/2\), while the R0.72E exact family requires \(\beta>1/3\), or \(\gamma\ge1\) at the endpoint. The minimal boundary weight \(w_*=s^{-1/3}[1+\log(1/s)]\) exactly saturates the selected obstruction, and the free-amplitude audit gives an augmented necessary frontier. An upper bound for complete roots, restart covering, and transfer to general three-dimensional dynamics remain open.`,
  ],
  [raw`R0.72F 附图`, raw`R0.72F figure`],
  [raw`R0.72F 证书`, raw`R0.72F certificates`],
  [
    raw`R0.72G 固定 \(w_*\)，只审完整根 trace packing`,
    raw`R0.72G fixes \(w_*\) and audits only complete-root trace packing`,
  ],
  [
    raw`对 \(w_{\beta,\gamma}=s^{-\beta}[1+\log(1/s)]^\gamma\)，Leray energy 在 \(\beta<1/2\) 时支付 action；R0.72E exact family 则强制 \(\beta>1/3\)，或在端点取 \(\gamma\ge1\)。`,
    raw`For \(w_{\beta,\gamma}=s^{-\beta}[1+\log(1/s)]^\gamma\), Leray energy pays for the action when \(\beta<1/2\), while the R0.72E exact family requires \(\beta>1/3\), or \(\gamma\ge1\) at the endpoint.`,
  ],
  [
    raw`固定 \(w_*(s)=s^{-1/3}[1+\log(1/s)]\)，把全部根、restart covering 与 left-end cost 放进同一个 estimate；不再移动候选。`,
    raw`Fix \(w_*(s)=s^{-1/3}[1+\log(1/s)]\) and place every root, restart covering, and left-end cost in one estimate; the candidate will not be moved again.`,
  ],
  [
    raw`固定 \(w_*\)，检查 complete-root trace packing、restart covering 与 left-end cost。`,
    raw`Fix \(w_*\) and test complete-root trace packing, restart covering, and the left-end cost.`,
  ],
  [
    raw`环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \(M^{-2}\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → phase-uniform \(M^{-8/3}\) sharp algebraic prefactor → shifted Rudin–Shapiro heat pulse → positive-time simple root → full-charge normalized order-one saturation → fixed-carrier shell isolation → negative-Sobolev action decay → candidate D^{1/3}Λ₁ payment failure → critical-log repair → selected-family frontier`,
    raw`annular exclusion → source–kernel ledger → covariance-spectrum stratification → all-frequency conditional bridge → response-slope chord gain → common-response order-one channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \(M^{-2}\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → sharp phase-uniform \(M^{-8/3}\) algebraic prefactor → shifted Rudin–Shapiro heat pulse → positive-time simple root → full-charge normalized order-one saturation → fixed-carrier shell isolation → negative-Sobolev action decay → candidate D^{1/3}Λ₁ payment failure → critical-log repair → selected-family frontier`,
  ],
  [
    raw`静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71U–Z 依次处理 second-time jet、complete first row、fixed-small-coupling endpoint、selected roots 与 complete roots。R0.72A–C 建立 Bessel lower family、target-row participation 与 physical-phase sharp scales；R0.72D 再实现 positive-time root 与 full-charge order-one saturation。R0.72E 固定 \(q_0>R_*\)，用 Feynman–Kac、驻相和定量 Hörmander density 控制完整 \(H^{-1}\) action；exact one-carrier family 最终使 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。R0.72F 随后证明 selected roots 强制 \(1/3\) 下端点，而 Leray energy 只支付到 \(1/2\)；最小边界修正是 \(s^{-1/3}[1+\log(1/s)]\)。`,
    raw`After the static annular family is rigorously excluded, the main route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71U–Z treats the second-time jet, complete first row, fixed-small-coupling endpoint, selected roots, and complete roots. R0.72A–C develops the Bessel lower family, target-row participation, and sharp physical-phase scales; R0.72D then realizes a positive-time root and full-charge order-one saturation. R0.72E fixes \(q_0>R_*\) and controls the complete \(H^{-1}\) action using Feynman–Kac, stationary phase, and a quantitative Hörmander density bound; the exact one-carrier family ultimately makes the complete-root ledger relative to the candidate \(D^{1/3}\Lambda_1\) payment diverge as \(R^{4/3}\). R0.72F then proves that selected roots require the lower endpoint \(1/3\), while Leray energy pays only up to \(1/2\); the minimal boundary repair is \(s^{-1/3}[1+\log(1/s)]\).`,
  ],
  [
    raw`累计回顾 R0.61–R0.72F · 2026-08-27`,
    raw`Cumulative recap R0.61–R0.72F · 2026-08-27`,
  ],
  [
    raw`R0.60 之后的路线分成二十三个阶段`,
    raw`The route after R0.60 is divided into twenty-three phases`,
  ],
  [
    raw`累计回顾按二十三个阶段覆盖 R0.61–R0.72F。R0.72E 排除 unweighted payment；R0.72F 给出 selected-root \(1/3\) 下端点、Leray-payment \(1/2\) 上端点与 critical-log 最小边界。R0.70A–R0.72F 共 58 个版本已公开；按当前 formal-figure 合同有 34 个完整封存，24 个旧版附图档案列入回补清单。`,
    raw`The cumulative recap covers R0.61–R0.72F in twenty-three phases. R0.72E excludes the unweighted payment; R0.72F gives the selected-root lower endpoint \(1/3\), the Leray-payment upper endpoint \(1/2\), and the minimal critical-log boundary. The releases from R0.70A through R0.72F number 58 and are published; under the current formal-figure contract, 34 are fully archived and 24 legacy figure archives are listed for backfill.`,
  ],
  [
    raw`临界对数初始层修正同时通过 selected-root 与 Leray-payment 筛查`,
    raw`The critical-log initial-layer repair passes both the selected-root and Leray-payment screens`,
  ],
  [
    raw`目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.72F 只把下一候选固定为 critical-log action；complete-root estimate 仍开放。`,
    raw`There is currently no new unconditional continuation criterion and no construction of a finite-time singularity. R0.72F only fixes the next candidate as the critical-log action; the complete-root estimate remains open.`,
  ],
  [raw`上次综述 v1.18 · 2026-08-27`, raw`Previous review v1.18 · 2026-08-27`],
  [
    raw`我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.72F 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。`,
    raw`I maintain a separate systematic review that places classical theory, five main literature lines, the candidate-blowup exclusion tree, developments from 2019–2026, and the R0.69P–R0.72F route on this site in one diagram. Historical nodes R0.61–R0.69O remain in the cumulative recap.`,
  ],
  [raw`下一步 R0.72G：`, raw`Next step R0.72G:`],
  [raw`研究笔记 R0.72F · 2026-08-27`, raw`Research note R0.72F · 2026-08-27`],
  [raw`阅读 R0.72F 研究笔记 →`, raw`Read the R0.72F research note →`],
  [raw`展开 66 篇公开笔记`, raw`Expand 66 public notes`],
  [
    raw`这只是 viable-candidate theorem。critical-log action 尚未支付 complete-root ledger，也没有给出 continuation criterion。`,
    raw`This is only a viable-candidate theorem. The critical-log action has not yet paid for the complete-root ledger and gives no continuation criterion.`,
  ],
  [raw`综述 v1.19 · 2026-08-27`, raw`Review v1.19 · 2026-08-27`],
  [
    raw`最小边界权重为 \(w_*=s^{-1/3}[1+\log(1/s)]\)，且 \(\|w_*\|_2^2=75\)。两路有限审计在 \(\delta=16,\ldots,512\) 上逐点一致到 \(4.76\times10^{-4}\) 以内。`,
    raw`The minimal boundary weight is \(w_*=s^{-1/3}[1+\log(1/s)]\), with \(\|w_*\|_2^2=75\). For \(\delta=16,\ldots,512\), the two finite audits agree pointwise to within \(4.76\times10^{-4}\).`,
  ],
  [
    raw`R0.60 recap 之后的累计回顾收录 96 个节点；全站现有 156 篇公开研究笔记`,
    raw`The cumulative recap after R0.60 contains 96 nodes; the site now has 156 public research notes`,
  ],
  [
    raw`R0.70A–R0.72F：58 节已公开，34 节完整封存`,
    raw`R0.70A–R0.72F: 58 published, 34 fully archived`,
  ],
  [
    raw`R0.72F 已把修正压缩到 critical-log initial-layer action；下一步固定这个候选，检查它能否支付 complete-root trace packing。`,
    raw`R0.72F reduces the repair to the critical-log initial-layer action; the next step fixes this candidate and tests whether it can pay for complete-root trace packing.`,
  ],
  [raw`R0.72F 已完成：`, raw`R0.72F complete:`],
  [
    raw`regularly varying initial-layer repair 的两道阈值已经封闭；critical-log weight 是最小边界候选。`,
    raw`The two thresholds for regularly varying initial-layer repairs are closed; the critical-log weight is the minimal boundary candidate.`,
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
if (!Array.isArray(snapshot) || snapshot.length !== 127) {
  throw new Error(
    "R0.72F snapshot cardinality drift: " +
      (Array.isArray(snapshot) ? snapshot.length : "not-an-array"),
  );
}
if (englishByChinese.size !== 127) {
  throw new Error(
    "R0.72F translation-map cardinality drift: " + englishByChinese.size,
  );
}

for (const [field, values] of [
  ["snapshot key", snapshot.map((entry) => entry.zh)],
  ["translation key", [...englishByChinese.keys()]],
]) {
  const duplicates = duplicateValues(values);
  if (duplicates.length) {
    throw new Error("Duplicate " + field + " values: " + duplicates.join(" | "));
  }
}

const snapshotByChinese = new Map(snapshot.map((entry) => [entry.zh, entry]));
const missingMappings = snapshot.filter(
  (entry) => !englishByChinese.has(entry.zh),
);
const extraMappings = [...englishByChinese.keys()].filter(
  (zh) => !snapshotByChinese.has(zh),
);
if (missingMappings.length || extraMappings.length) {
  throw new Error(
    "R0.72F snapshot/map key drift:\nMISSING " +
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
      "R0.72F live-source drift for snapshot key:\n" +
        entry.zh +
        "\nSNAPSHOT " +
        JSON.stringify({ count: entry.count, files: entry.files }) +
        "\nLIVE " +
        JSON.stringify(live ?? null),
    );
  }
}

const missing = source.filter((entry) => !existingByChinese.has(entry.zh));
const unmapped = missing.filter((entry) => !englishByChinese.has(entry.zh));
if (unmapped.length) {
  throw new Error(
    "R0.72F translation source drift (" +
      unmapped.length +
      " unmapped live strings):\n" +
      unmapped.map((entry) => entry.zh).join("\n---\n"),
  );
}

const rows = snapshot.map((entry, index) => [
  `r072f${String(index + 1).padStart(3, "0")}`,
  entry.zh,
  englishByChinese.get(entry.zh),
]);

for (const [id, zh, en] of rows) {
  if (!sourceByChinese.has(zh)) {
    throw new Error("R0.72F mapped source is no longer live: " + zh);
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
      "Existing R0.72F translation drift for " +
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
    "R0.72F full-site missing-after check failed (" +
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
