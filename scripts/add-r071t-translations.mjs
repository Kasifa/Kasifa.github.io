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
02 · 84 节完整索引 ||| 02 · Complete 84-section index
打开最新节点 R0.71T ||| Open the latest node R0.71T
回顾截止节点：R0.71T ||| Recap endpoint: R0.71T
回顾截止时公开笔记：144 ||| Public notes at recap endpoint: 144
截至 R0.71T，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 84 个节点解释成对千禧年问题完成了某个比例。 ||| At R0.71T, there is no new unconditional continuation criterion, no narrowing of the class of all potential singular solutions, and no proof of finite-time breakdown. The 84 nodes cannot be interpreted as completing any percentage of the Millennium Problem.
累计回顾 · R0.61–R0.71T · 2026-08-26 ||| Cumulative recap · R0.61–R0.71T · 2026-08-26
目标是证明一个 summed/Carleson estimate，或构造 recurrence family 排除该估计。并行保留 fixed-packet amplitude-thresholded excursion：它已有真实 Leray-paid variation bound，但改变了 raw zero-entry target。R0.71U 仍不宣称继续性、奇性排除或全局正则性。 ||| The objective is to prove a summed/Carleson estimate or construct a recurrence family that rules it out. In parallel, the fixed-packet amplitude-thresholded excursion is retained: it has a genuine Leray-paid variation bound, but it changes the raw zero-entry target. R0.71U still makes no claim of continuation, singularity exclusion, or global regularity.
内部事件已经存在，真正缺口转为 scale-zero charge 的总量控制 ||| Internal events now exist; the real gap shifts to aggregate control of the scale-zero charge
十二个阶段、84 个节点：从约化递推到 conditional incidence，再到 genuine positive-time internal entry、internal scaling no-go 与 outgoing occupation boundary。 ||| Twelve stages and 84 nodes: from reduced recurrences to conditional incidence, then to a genuine positive-time internal entry, the internal scaling no-go, and the outgoing-occupation boundary.
收录节点：84 ||| Included nodes: 84
下一有限任务研究 simple global entries 的 \(q_\beta^{\rm jet}=\kappa_j^{-6}\|C_t(t_\beta)\|_2^2/Y(t_\beta)\)。它在单半径 full-shell root 上与 entry atom 精确同阶，也与 outgoing occupation representation 相容。 ||| The next finite task studies \(q_\beta^{\rm jet}=\kappa_j^{-6}\|C_t(t_\beta)\|_2^2/Y(t_\beta)\) for simple global entries. At a single-radius full-shell root, it is exactly of the same order as the entry atom and is also compatible with the outgoing-occupation representation.
这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71T 的 84 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。 ||| This page follows the R0.00–R0.60 stage recap and organizes the research nodes from R0.61 through R0.71T, 84 in total. I record chronologically what each stage actually proves, which proposals are ruled out by specific counterexamples or scaling analyses, and which conditions have not been derived from the Navier–Stokes equations.
正面结构是 global-shell positive entries 自动 simple，full-shell root 至少诱导一个 positive local cell，outgoing coarea 精确保留 odd crossing 与 even touch。尚缺的是该 scale-zero occupation/jet charge 的 summed NSE estimate；finite trace-variation theorem 所需 strong Lamb、\(F_t\)、\(Y_t\) 与 multiplicity 仍未由 Leray inequality 关闭。 ||| The positive structure is that global-shell positive entries are automatically simple, a full-shell root induces at least one positive local cell, and outgoing coarea exactly retains both odd crossings and even touches. What remains missing is a summed NSE estimate for this scale-zero occupation/jet charge; the strong Lamb term, \(F_t\), \(Y_t\), and multiplicity required by the finite trace-variation theorem are still not closed by the Leray inequality.
finite conditional directional-packet payment、critical Bessel diagonal 与 repeated-packet lower bounds、necessary directional Carleson condition、backward-heat kernel 和 bounded bilinear constant-mode dichotomy；R0.71S 的 genuine NSE scaling no-go 只覆盖 initial observation-boundary entry。 ||| finite conditional directional-packet payment; the critical Bessel diagonal and repeated-packet lower bounds; the necessary directional Carleson condition; the backward-heat kernel; and the bounded bilinear constant-mode dichotomy; the genuine NSE scaling no-go in R0.71S covers only an initial observation-boundary entry.
R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 84 个节点沿着这个缺口推进。 ||| The R0.00–R0.60 material remains in the previous stage recap. R0.60 concludes that the full Fourier–Leray structure and higher-order calculations can continue, but still do not control a critical quantity for general three-dimensional solutions. The subsequent 84 nodes advance along this gap.
R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71T 的 84 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、条件 incidence theorem，以及 packet/Bessel 与 NSE initial-face scaling 边界的路线。 ||| Research recap after R0.60: a chronological account from R0.61 through R0.71T, covering 84 research nodes and recording the route from reduced recurrences to the projected-Lamb heat volume, positive-entry batching, the conditional incidence theorem, and the packet/Bessel and NSE initial-face scaling boundaries.
R0.61–R0.71T 的 84 节公开笔记 ||| Public notes from R0.61–R0.71T: 84 sections
R0.61–R0.71T 回顾 · 2026-08-26 ||| R0.61–R0.71T recap · 2026-08-26
R0.61–R0.71T 研究节点 ||| R0.61–R0.71T research nodes
R0.61–R0.71T｜R0.60 之后的研究回顾 ||| R0.61–R0.71T | Research recap after R0.60
R0.70A–R0.71T 完成版本 ||| Completed releases R0.70A–R0.71T
R0.71G–R0.71T · temporal packing、internal entry 与 scale-matched occupation ||| R0.71G–R0.71T · temporal packing, internal entry, and scale-matched occupation
R0.71O–P 恢复 soft quotient 的一侧 traces，并用同刻 spatial batching 吸收有限 frame multiplicity；R0.71Q–R 给出 finite conditional Jensen 与 incidence theorems。R0.71S 保留 entry direction 后证明 critical packet 单包即带 \(\kappa_j^2\) Bessel 税，并用 genuine NSE initial face 排除 observation-boundary 版本的 bare payment。R0.71T 进一步用正向局部 NSE 流映射和有限维 IFT 构造预定正时间的 full-shell zero：event forcing 非零，所以它是 genuine smooth internal simple positive entry。选择 \(a_\lambda=\lambda^{-2}\) 再作协变 scaling 后，entry atom 为 \(\lambda^{-4}\)、bare normalized Leray-Lamb time budget 为 \(\lambda^{-6}\)，比值按 \(\lambda^2\) 发散；初始 energy 与 critical norm 趋零，enstrophy 有界。outgoing coarea 对所有 finite-order entries 给出 even-touch-safe 的 exact scale-zero representation，但其零层集中尚无 Leray payment。finite trace-variation theorem 则保留 strong Lamb、\(F_t\)、\(Y_t\) 与 repeated-direction Bessel ledgers。 ||| R0.71O–P recovers one-sided traces of the soft quotient and uses same-time spatial batching to absorb finite frame multiplicity; R0.71Q–R gives finite conditional Jensen and incidence theorems. After retaining the entry direction, R0.71S proves that even a single critical packet carries the \(\kappa_j^2\) Bessel tax and uses a genuine NSE initial face to rule out the observation-boundary version of bare payment. R0.71T then uses the forward local NSE flow map and a finite-dimensional IFT to construct a full-shell zero at a prescribed positive time: the event forcing is nonzero, so this is a genuine smooth internal simple positive entry. After choosing \(a_\lambda=\lambda^{-2}\) and applying covariant scaling, the entry atom is \(\lambda^{-4}\), the bare normalized Leray-Lamb time budget is \(\lambda^{-6}\), and their ratio diverges as \(\lambda^2\); the initial energy and critical norm tend to zero while enstrophy remains bounded. Outgoing coarea gives an exact scale-zero representation safe for even touches for every finite-order entry, but its concentration on the zero level still has no Leray payment. The finite trace-variation theorem retains the strong Lamb term, \(F_t\), \(Y_t\), and the repeated-direction Bessel ledgers.
R0.71T 的 finite-dimensional IFT positive-time internal-entry construction、global positive entry simplicity、induced local positive cell、bounded-energy/enstrophy internal scaling no-go、finite outgoing-coarea identity，以及带完整 \(F_t\)、\(Y_t\) 账本的 conditional trace-variation theorem。 ||| R0.71T's finite-dimensional IFT construction of a positive-time internal entry; simplicity of global positive entries; the induced positive local cell; the bounded-energy/enstrophy internal scaling no-go; the finite outgoing-coarea identity; and the conditional trace-variation theorem with complete \(F_t\) and \(Y_t\) ledgers.
R0.71T 的实质进展是关闭 R0.71S 留下的 initial-boundary caveat：smooth positive-time internal entry 可以由 exact forward NSE flow 构造，且 bare normalized \(\dot H^{-1}\)-Lamb time integral 对它仍少两阶。这个 no-go 沿 energy 与 critical norm 趋零、enstrophy 有界的解族成立，因此不是高能数据假象。 ||| The substantive advance in R0.71T is to close the initial-boundary caveat left by R0.71S: a smooth positive-time internal entry can be constructed by the exact forward NSE flow, and the bare normalized \(\dot H^{-1}\)-Lamb time integral still falls short by two orders. This no-go holds along a family of solutions whose energy and critical norm tend to zero while enstrophy remains bounded, so it is not an artifact of high-energy data.
R0.71T 附图 ||| R0.71T figure
R0.71T 证书 ||| R0.71T certificates
R0.71U 检查 global-shell jet 与 outgoing occupation packing ||| R0.71U tests the global-shell jet and outgoing-occupation packing
本节没有得到 outgoing occupation packing、continuation、singularity 或 global regularity。no-go 只排除 covariant frame/window、常数沿该解族一致、RHS 恰为 bare normalized Leray-Lamb time integral 的声明类。 ||| This section does not obtain outgoing-occupation packing, continuation, singularity, or global regularity. The no-go rules out only the class of claims with a covariant frame/window, a constant uniform along this solution family, and a right-hand side equal exactly to the bare normalized Leray-Lamb time integral.
查看附图、数据、进度与源代码包 ||| View the figure, data, progress, and source package
从有符号环带障碍走到 genuine internal-entry scale boundary ||| From the signed-annulus obstruction to the genuine internal-entry scale boundary
对 \(U=(0,\cos x_1,\cos x_2)\) 的 \(|k|^2=2\) 目标壳，标准局部 NSE 流映射与有限维 IFT 给出初值预补偿 \[ z(a)=-a^2\tau F_*+O(a^3), \] 使整个目标壳在预定正时间 \(t=\tau\) 精确归零。事件 forcing 仍为 \(a^2e^{-2\nu\tau}F_*+O(a^3)\ne0\)，所以该零点严格位于 observation window 内部、为 simple positive crossing，并满足 \[ \kappa^{-2}A_+(a)=\frac{a^2e^{-2\nu\tau}}4+O(a^3). \] ||| For \(U=(0,\cos x_1,\cos x_2)\), the target shell \(|k|^2=2\) is handled by the standard local NSE flow map and a finite-dimensional IFT, which give the initial-data precompensation \[ z(a)=-a^2\tau F_*+O(a^3), \], making the entire target shell vanish exactly at the prescribed positive time \(t=\tau\). The event forcing remains \(a^2e^{-2\nu\tau}F_*+O(a^3)\ne0\), so the zero lies strictly inside the observation window, is a simple positive crossing, and satisfies \[ \kappa^{-2}A_+(a)=\frac{a^2e^{-2\nu\tau}}4+O(a^3). \]
环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary ||| annular exclusion → source–kernel ledger → covariance spectral stratification → all-frequency conditional bridge → response-slope chord gain → common-response order-one channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → localized heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel sets → projective heat curvature → soft-denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing-occupation boundary
检查 \(\kappa_j^{-6}\|C_t(t_\beta)\|_2^2/Y(t_\beta)\) 是否有 summed / Carleson estimate，或由 recurrence family 排除；并行保留 amplitude-thresholded excursion。 ||| Test whether \(\kappa_j^{-6}\|C_t(t_\beta)\|_2^2/Y(t_\beta)\) admits a summed/Carleson estimate or is ruled out by a recurrence family; retain the amplitude-thresholded excursion in parallel.
检查 global-shell simple-entry jet 与 outgoing occupation 能否得到 summed / Carleson payment；bare normalized \(\dot H^{-1}\)-Lamb time integral 已被 genuine internal family 排除。 ||| Test whether the global-shell simple-entry jet and outgoing occupation admit summed/Carleson payment; the bare normalized \(\dot H^{-1}\)-Lamb time integral has been ruled out by a genuine internal family.
检查 global-shell simple-entry jet 与 outgoing occupation 是否有 summed / Carleson payment；并行保留 amplitude-thresholded excursion 分支。 ||| Test whether the global-shell simple-entry jet and outgoing occupation admit summed/Carleson payment; retain the amplitude-thresholded-excursion branch in parallel.
静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–P 建立 projected-Lamb 热体积、局部化、denominator faces 与同刻 spatial batching。R0.71Q–S 给出 conditional Jensen/incidence 与 packet/Bessel scale audits。R0.71T 用正向局部 NSE 流映射和 finite-dimensional IFT 构造 genuine smooth positive-time internal entry；双尺度族把 atom 与 bare normalized Leray-Lamb time budget 分别压到 λ⁻⁴ 与 λ⁻⁶，从而关闭 initial-boundary caveat。outgoing coarea 保留为 scale-matched representation，但 summed payment 仍开放。 ||| After the static annular family is rigorously excluded, the main line turns to covariance-rank stratification and the all-frequency projection bridge. R0.71A–P establishes the projected-Lamb heat volume, localization, denominator faces, and same-time spatial batching. R0.71Q–S gives conditional Jensen/incidence and packet/Bessel scale audits. R0.71T uses the forward local NSE flow map and a finite-dimensional IFT to construct a genuine smooth positive-time internal entry; the two-scale family drives the atom and the bare normalized Leray-Lamb time budget to λ⁻⁴ and λ⁻⁶, respectively, thereby closing the initial-boundary caveat. Outgoing coarea remains as a scale-matched representation, but summed payment is still open.
累计回顾 R0.61–R0.71T · 2026-08-26 ||| Cumulative recap R0.61–R0.71T · 2026-08-26
目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71T 已构造 genuine smooth positive-time internal entry，并用 energy/critical norm 趋零、enstrophy 有界的双尺度族排除 bare normalized Leray-Lamb time integral 的 scale-uniform internal payment。outgoing coarea 是 exact scale-matched representation，但零层 concentration、jet summability 与 recurrence packing 仍开放。 ||| There is currently no new unconditional continuation criterion and no construction of a finite-time singularity. R0.71T constructs a genuine smooth positive-time internal entry and uses a two-scale family with energy and critical norm tending to zero and bounded enstrophy to rule out scale-uniform internal payment by the bare normalized Leray-Lamb time integral. Outgoing coarea is an exact scale-matched representation, but zero-level concentration, jet summability, and recurrence packing remain open.
取 base amplitude \(a_\lambda=\lambda^{-2}\) 再作 compatible NSE dilation。internal atom 为 \(\lambda^{-4}\)，bare normalized \(\dot H^{-1}\)-Lamb time budget 为 \(\lambda^{-6}\)，两者之比按 \[ \frac{2\nu}{\sinh(2\nu\tau)}\lambda^2 \] 发散；与此同时 initial energy 与 \(\dot H^{1/2}\) norm 趋零，enstrophy 保持有界。因此 bare time integral 的 scale-uniform internal-entry payment 被 genuine smooth NSE family 排除。 ||| Take the base amplitude \(a_\lambda=\lambda^{-2}\) and then apply the compatible NSE dilation. The internal atom is \(\lambda^{-4}\), the bare normalized \(\dot H^{-1}\)-Lamb time budget is \(\lambda^{-6}\), and their ratio diverges as \[ \frac{2\nu}{\sinh(2\nu\tau)}\lambda^2 \]; meanwhile, the initial energy and \(\dot H^{1/2}\) norm tend to zero and enstrophy remains bounded. Thus scale-uniform internal-entry payment by the bare time integral is ruled out by a genuine smooth NSE family.
上次综述 v1.04 · 2026-08-26 ||| Previous review v1.04 · 2026-08-26
我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71T 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。 ||| I also prepared a systematic review that places classical theory, five main literature strands, the candidate-blowup exclusion tree, progress from 2019—2026, and this site's R0.69P–R0.71T route in a single map. The historical R0.61–R0.69O nodes remain in the cumulative recap.
下一步 R0.71U： ||| Next step R0.71U:
研究笔记 R0.71T · 2026-08-26 ||| Research note R0.71T · 2026-08-26
阅读 R0.71T 研究笔记 → ||| Read the R0.71T research note →
展开 54 篇公开笔记 ||| Expand 54 public notes
真实正时间内部 entry 排除裸 Leray 时间支付 ||| A genuine positive-time internal entry rules out bare Leray time payment
综述 v1.05 · 2026-08-26 ||| Review v1.05 · 2026-08-26
finite outgoing-coarea identity 对 odd crossings 与 even touches 都精确保留 \(A_+\)，但其 zero-level mollifier concentration 尚无 Leray payment。finite trace-variation theorem 也成立，却保留 strong Lamb、\(F_t\)、\(Y_t\) 与 repeated-direction Bessel ledgers。 ||| The finite outgoing-coarea identity exactly retains \(A_+\) for both odd crossings and even touches, but its zero-level mollifier concentration still has no Leray payment. The finite trace-variation theorem also holds, but retains the strong Lamb term, \(F_t\), \(Y_t\), and the repeated-direction Bessel ledgers.
finite-dimensional IFT 构造 genuine smooth positive-time internal entry；double scaling 排除 bare normalized Leray-Lamb time payment；outgoing coarea 保留为未闭合的 scale-matched charge。 ||| A finite-dimensional IFT constructs a genuine smooth positive-time internal entry; double scaling rules out bare normalized Leray-Lamb time payment; outgoing coarea remains as an unclosed scale-matched charge.
R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen/incidence、packet/Bessel 与 internal-entry scale audit。R0.70A–R0.71T 共 46 个完成版本。 ||| The route after R0.60 has twelve segments: reduced Picard dynamics and the shear boundary; transverse perturbations; localized pressure budgets; signed physical annuli; moving labels and source–core duality; deviation tensors and finite observations; full-frame covariance; the constant-projection boundary; positive output and the material-heat tent; the projected-Lamb heat volume; localized heat packing and the critical-trace obstruction; and positive-entry temporal packing, conditional Jensen/incidence, packet/Bessel analysis, and the internal-entry scale audit. R0.70A–R0.71T contains 46 completed releases.
R0.60 recap 之后的累计回顾收录 84 个节点；全站现有 144 篇公开研究笔记 ||| The cumulative recap after the R0.60 recap includes 84 nodes; the site now contains 144 public research notes
R0.71T 已完成： ||| R0.71T completed:
打开 84 节完整索引 ||| Open the complete 84-section index
分别控制 local energy/singular sets、averaged flux 与 upper Carleson norms，不给每次 smooth zero lower charge。 ||| respectively control local energy/singular sets, averaged flux, and upper Carleson norms, but do not give a lower charge for each smooth zero.
检查 scale-zero jet 或 outgoing occupation 是否有 summed / Carleson estimate；并行保留 amplitude-thresholded excursion。 ||| Test whether the scale-zero jet or outgoing occupation admits a summed/Carleson estimate; retain the amplitude-thresholded excursion in parallel.
开放接口 · R0.71U ||| Open interface · R0.71U
累计回顾与 84 节索引 ||| Cumulative recap and 84-section index
文献综述 v1.05 · 2026-08-26 ||| Literature review v1.05 · 2026-08-26
我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.71T 只列为研究笔记。我不把计算或笔记外推成正则性定理。 ||| I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.71T material only as research notes. I do not extrapolate calculations or notes into regularity theorems.
支持 level-averaged occupation 或 positive-height crossings，不给 fixed zero-level raw count。两轮 bounded audit 未找到完整 R0.71T payment theorem；这不是原创性、优先权或不存在性结论。 ||| support level-averaged occupation or positive-height crossings, but do not give a raw count at a fixed zero level. Two bounded audit rounds found no complete R0.71T payment theorem; this is not a claim of originality, priority, or nonexistence.
支持 smooth local flow-map input。 ||| supports the smooth local flow-map input.
中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–S 给出 finite conditional Jensen/incidence 与 packet/Bessel scale audits。R0.71T 再构造 genuine smooth positive-time internal entry，并排除 bare normalized Leray-Lamb time integral 的 scale-uniform internal payment。保留下来的结果都不是全局正则性结论。 ||| . R0.69P–R0.71P reaches the positive-entry temporal-packing boundary, and R0.71Q–S gives finite conditional Jensen/incidence and packet/Bessel scale audits. R0.71T then constructs a genuine smooth positive-time internal entry and rules out scale-uniform internal payment by the bare normalized Leray-Lamb time integral. None of the retained results is a global regularity theorem.
finite directional-packet theorem 成立，但单包对角、same-direction Gram clustering、frozen-denominator backward heat 与限定 normalized bilinear kernels 都保留两阶或事件密度代价。genuine NSE initial-face scaling 只排除 observation-boundary 版本。 ||| The finite directional-packet theorem holds, but the single-packet diagonal, same-direction Gram clustering, frozen-denominator backward heat, and the specified normalized bilinear kernels all retain a two-order or event-density cost. Genuine NSE initial-face scaling rules out only the observation-boundary version.
finite-dimensional IFT 构造 smooth positive-time full-shell root；double scaling 给 atom λ⁻⁴、bare budget λ⁻⁶。outgoing coarea 精确保留 entry，但 summed payment 未闭合。 ||| A finite-dimensional IFT constructs a smooth positive-time full-shell root; double scaling gives an atom of λ⁻⁴ and a bare budget of λ⁻⁶. Outgoing coarea retains the entry exactly, but summed payment is not closed.
genuine internal entry 保留同一两阶错配 ||| A genuine internal entry retains the same two-order mismatch
R0.71T 的一手文献边界 ||| Primary-literature boundary for R0.71T
R0.71T 关闭了什么，R0.71U 只检查什么 ||| What R0.71T closes, and what R0.71U alone tests
R0.71T 用标准 local strong flow 与 finite-dimensional IFT 构造 genuine positive-time full-shell zero；event forcing 非零，所以 root 是 simple positive internal entry。取 a_lambda=lambda^-2 再作 covariant NSE dilation 后，entry atom 为 lambda^-4、bare normalized Leray-Lamb time budget 为 lambda^-6，比值按 lambda^2 发散；initial energy 与 critical norm 趋零，enstrophy 有界。因此 bare payment 的 internal-entry 版本也停止。outgoing coarea 是 exact scale-zero representation，但 zero-level concentration 尚无 a priori bound。R0.71U 只检查 global-shell jet / outgoing occupation packing 与 amplitude-thresholded excursion。我继续用下面六条筛选。 ||| R0.71T uses the standard local strong flow and a finite-dimensional IFT to construct a genuine positive-time full-shell zero; the event forcing is nonzero, so the root is a simple positive internal entry. After taking a_lambda=lambda^-2 and applying covariant NSE dilation, the entry atom is lambda^-4, the bare normalized Leray-Lamb time budget is lambda^-6, and their ratio diverges as lambda^2; the initial energy and critical norm tend to zero while enstrophy remains bounded. The internal-entry version of bare payment therefore also stops. Outgoing coarea is an exact scale-zero representation, but zero-level concentration has no a priori bound. R0.71U tests only global-shell jet/outgoing-occupation packing and the amplitude-thresholded excursion. I continue to apply the following six filters.
01 · IFT 内部化 ||| 01 · IFT internalization
02 · 双尺度 no-go ||| 02 · Two-scale no-go
06 · 双重审计 ||| 06 · Dual audit
07 · 正式附图 ||| 07 · Publication figure
版本 v0.71T · 2026-08-26 ||| Version v0.71T · 2026-08-26
报告、文献、证书、进度日志与独立 checker 全部保留 ||| The report, literature audit, certificates, progress log, and independent checker are all retained
尺度匹配的表示存在，但 Leray payment 尚未建立 ||| A scale-matched representation exists, but Leray payment has not been established
初始边界 caveat 已关闭，裸时间积分不再是候选终局 ||| The initial-boundary caveat is closed; the bare time integral is no longer a candidate endpoint
存在一族真实光滑周期 NSE 解，使 R0.71P 的目标壳在正时间 \(t=\tau\) 精确归零并以正方向横穿。这个事件严格位于 \([0,2\tau)\) 内部。对其振幅—频率双尺度族，scale-zero entry target 与 bare normalized \(\dot H^{-1}\)-Lamb time integral 的比值按 λ² 发散；即使把数据限制在能量趋零、临界范数趋零和 enstrophy 有界的解族，该统一支付仍不成立。 ||| There is a family of genuine smooth periodic NSE solutions for which the R0.71P target shell vanishes exactly at the positive time \(t=\tau\) and crosses in the positive direction. This event lies strictly inside \([0,2\tau)\). For its amplitude–frequency two-scale family, the ratio of the scale-zero entry target to the bare normalized \(\dot H^{-1}\)-Lamb time integral diverges as λ²; uniform payment still fails even when the data are restricted to a solution family with energy tending to zero, critical norm tending to zero, and bounded enstrophy.
对固定 entry direction 与对称窗口 \(h=\theta\kappa^{-2}\)，三角核恒等式给出 ||| For a fixed entry direction and a symmetric window \(h=\theta\kappa^{-2}\), the triangular-kernel identity gives
对有限个孤立有限阶 internal zeros，令 \(r=\|C\|_2\)、\(\xi=C/r\)、\(q=\langle F,\xi\rangle_+^2/Y\)。任取单位质量的一侧 mollifier \(\rho_\delta\)，有 outgoing coarea identity ||| For finitely many isolated finite-order internal zeros, set \(r=\|C\|_2\), \(\xi=C/r\), and \(q=\langle F,\xi\rangle_+^2/Y\). For any one-sided unit-mass mollifier \(\rho_\delta\), the outgoing-coarea identity is
符号证书与独立 FFT / quadrature 重建分别通过 ||| The symbolic certificate and independent FFT/quadrature reconstruction both pass
附图、数据、manifest、progress 与源代码包 ||| Figure, data, manifest, progress, and source package
附图把预补偿、内部横穿、原子与双尺度 no-go 分开显示 ||| The figure shows precompensation, the internal crossing, the atom, and the two-scale no-go separately
该有限矩阵可逆，隐函数定理给出真实修正 \(z(a)\)，使目标壳在 τ 精确为零。二次 Duhamel 展开同时给出 ||| This finite matrix is invertible, and the implicit function theorem gives a genuine correction \(z(a)\) that makes the target shell vanish exactly at τ. The quadratic Duhamel expansion also gives
计算边界： ||| Computational boundary:
价值是把一个边界疑问变成严格内部 no-go ||| The value is to turn a boundary question into a rigorous internal no-go
精确落在 \(|k|^2=2\) 的四个目标模。令 \(P_*\) 为该实共轭闭合壳的投影，\(S_t\) 为局部经典 NSE 流。对 \(z\) 属于目标壳，定义 \(\Phi(a,z)=P_*S_\tau(aU+z)\)。在零解处 ||| falls exactly on the four target modes with \(|k|^2=2\). Let \(P_*\) be the projection onto this real conjugation-closed shell and \(S_t\) the local classical NSE flow. For \(z\) in the target shell, define \(\Phi(a,z)=P_*S_\tau(aU+z)\). At the zero solution,
精确求导必须保留 \(f_t=\langle F_t,e\rangle/\sqrt Y-(Y_t/2Y)f\)。在 finite active-direction Bessel 条件下可求和，但右端包含 strong \(\|F_j\|_2^2/Y\)、\(\kappa_j^{-2}\|F_j\|_2\|F_{j,t}\|_2/Y\) 与 normalized \(Y_t\) variation。三项尺度都正确，却都不是 ordinary Leray budget；重复方向还会使 Bessel 常数增长。 ||| Exact differentiation must retain \(f_t=\langle F_t,e\rangle/\sqrt Y-(Y_t/2Y)f\). Summation is possible under a finite active-direction Bessel condition, but the right-hand side contains the strong term \(\|F_j\|_2^2/Y\), the term \(\kappa_j^{-2}\|F_j\|_2\|F_{j,t}\|_2/Y\), and normalized \(Y_t\) variation. All three have the correct scaling, but none is an ordinary Leray budget; repeated directions also make the Bessel constant grow.
控制 critical upper Carleson norms；这些结论都不为每次 smooth coefficient zero 提供 lower charge。 ||| control critical upper Carleson norms; none of these results provides a lower charge for each smooth coefficient zero.
控制 ensemble/time-averaged flux， ||| control ensemble/time-averaged flux;
控制 local energy 与 singular set， ||| control local energy and the singular set;
内部构造 ||| Internal construction
排除裸 Leray 时间支付 ||| Bare Leray time payment ruled out
取 \(U=(0,\cos x_1,\cos x_2)\)。它只含半径一的速度模，但二次 projected Lamb 场 ||| Take \(U=(0,\cos x_1,\cos x_2)\). It contains only radius-one velocity modes, but the quadratic projected Lamb field
任意非负 covering partition 至少有一格满足 \(\langle F,c_Q\rangle=\int\chi_Q|\operatorname{curl}F|^2>0\)。该正号依赖 full-shell root；一般 localized zero 仍有 cutoff commutator，不能据此排除 even touch。 ||| Every nonnegative covering partition has at least one cell satisfying \(\langle F,c_Q\rangle=\int\chi_Q|\operatorname{curl}F|^2>0\). This positive sign depends on a full-shell root; a general localized zero still has a cutoff commutator, so even touches cannot be ruled out from this identity.
事件时 \(W_*(\tau)=0\)，滤波涡量方程给 \(C_t(\tau)=-\Delta F_*(u^a(\tau))\)，于是 \(\langle F_*,C_t\rangle=\|\nabla F_*\|_2^2>0\)。零点为一阶、\(A_-=0\)，且 ||| At the event time, \(W_*(\tau)=0\), and the filtered vorticity equation gives \(C_t(\tau)=-\Delta F_*(u^a(\tau))\); hence \(\langle F_*,C_t\rangle=\|\nabla F_*\|_2^2>0\). The zero is first order, \(A_-=0\), and
它对 odd crossing 与 even touch 都成立，且 NSE 给 \(r_t=\langle\xi,G\rangle-\nu\|\nabla C\|_2^2/r\)。但 \(\rho_\delta(r)\) 在零层附近按 δ⁻¹ 集中，普通 \(L_t^pG\) 上界不能统一支付该极限。因此这里是精确 representation，不是 a priori occupation theorem。 ||| It holds for both odd crossings and even touches, and NSE gives \(r_t=\langle\xi,G\rangle-\nu\|\nabla C\|_2^2/r\). But \(\rho_\delta(r)\) concentrates near the zero level at rate δ⁻¹, and ordinary \(L_t^pG\) upper bounds cannot pay this limit uniformly. This is therefore an exact representation, not an a priori occupation theorem.
它与 entry atom 同尺度，并在单半径 full-shell root 上精确等价。有限任务是证明一个 summed/Carleson estimate，或构造 recurrence family 排除它。并行保留 amplitude-thresholded excursion 这一保守 Leray-paid 分支。 ||| It has the same scaling as the entry atom and is exactly equivalent to it at a single-radius full-shell root. The finite task is to prove a summed/Carleson estimate or construct a recurrence family that rules it out. The conservative Leray-paid amplitude-thresholded-excursion branch is retained in parallel.
同时 \(\|u_\lambda(0)\|_2^2=O(\lambda^{-2})\)、\(\|u_\lambda(0)\|_{\dot H^{1/2}}^2=O(\lambda^{-1})\)、\(\|\omega_\lambda(0)\|_2^2=1+o(1)\)。该 no-go 不是初始能量增长造成的。 ||| Meanwhile, \(\|u_\lambda(0)\|_2^2=O(\lambda^{-2})\), \(\|u_\lambda(0)\|_{\dot H^{1/2}}^2=O(\lambda^{-1})\), and \(\|\omega_\lambda(0)\|_2^2=1+o(1)\). This no-go is not caused by growth of the initial energy.
图 R0.71T。A：预补偿范数相对二次 Duhamel 主项收敛。B：目标壳主系数在预定正时间过零，横向残差保持在求根容差内。C：finite Galerkin entry atom 与 slope-charge identity 一致，并向小时间种子值 1/4 靠近。D：双尺度主阶 atom 为 λ⁻⁴、bare budget 为 λ⁻⁶、比值为 λ²。A–C 是 finite Fourier–Galerkin corroboration；D 是解析主阶重建；均不是 DNS。 ||| Figure R0.71T. A: the precompensation norm converges relative to the quadratic Duhamel leading term. B: the leading target-shell coefficient crosses zero at the prescribed positive time, while the transverse residual remains within the root-finding tolerance. C: the finite Galerkin entry atom agrees with the slope-charge identity and approaches the small-time seed value 1/4. D: at leading order in the two-scale family, the atom is λ⁻⁴, the bare budget is λ⁻⁶, and the ratio is λ². A–C provide finite Fourier–Galerkin corroboration; D is an analytic leading-order reconstruction; none is DNS.
无 sampling coherence 的有限条件定理保留三个 strong ledgers ||| The finite conditional theorem without sampling coherence retains three strong ledgers
下一步首先研究 simple global entries 的 instantaneous jet ||| The next step first studies the instantaneous jet of simple global entries
下一对象：internal jet / occupation packing ||| Next object: internal jet/occupation packing
先取 \(a_\lambda=\lambda^{-2}\)，再作 \(u_\lambda(x,t)=\lambda u^{a_\lambda}(\lambda x,\lambda^2t)\)。内部事件移动到 \(\tau/\lambda^2\)，仍严格位于协变窗口内部。精确主阶为 ||| First take \(a_\lambda=\lambda^{-2}\), then set \(u_\lambda(x,t)=\lambda u^{a_\lambda}(\lambda x,\lambda^2t)\). The internal event moves to \(\tau/\lambda^2\) and remains strictly inside the covariant window. The exact leading terms are
现有定理支付能量、平均 flux 或幅度 excursion，不支付裸零级 entry ||| Existing theorems pay for energy, averaged flux, or amplitude excursions, not a raw zero-level entry
研究笔记 R0.71T · INTERNAL ENTRY · SCALE AUDIT ||| Research note R0.71T · INTERNAL ENTRY · SCALE AUDIT
研究笔记 R0.71T：用有限维隐函数定理构造真实光滑 NSE 正时间内部 entry；双尺度族排除由裸 normalized Leray-Lamb 时间积分统一支付该原子；outgoing coarea 给出尺度匹配的精确表示。 ||| Research note R0.71T: a finite-dimensional implicit function theorem constructs a genuine smooth positive-time internal entry for NSE; a two-scale family rules out uniform payment of its atom by the bare normalized Leray-Lamb time integral; outgoing coarea gives an exact scale-matched representation.
占据量 ||| Occupation
这不是 backward NSE，也不要求完整流映射在无限维空间局部满射；只使用光滑初值的标准正向局部流和一个有限维投影。 ||| This is not backward NSE and does not require the full flow map to be locally onto in an infinite-dimensional space; it uses only the standard forward local flow for smooth initial data and a finite-dimensional projection.
这不是千禧年问题的解答。它严格排除一个此前仍开放的支付机制，并把可行候选缩到 instantaneous jet、outgoing occupation 或改变目标后的 amplitude excursion。 ||| This is not a solution to the Millennium Problem. It rigorously rules out a previously open payment mechanism and narrows the viable candidates to an instantaneous jet, outgoing occupation, or an amplitude excursion after changing the target.
真实 smooth positive-time full-shell internal entry；至少一个 induced local positive cell；global positive entry 自动 simple；bounded-energy/enstrophy internal scaling no-go；finite outgoing-coarea identity；finite conditional trace-variation theorem。 ||| a genuine smooth positive-time full-shell internal entry; at least one induced positive local cell; automatic simplicity of a global positive entry; the bounded-energy/enstrophy internal scaling no-go; the finite outgoing-coarea identity; and the finite conditional trace-variation theorem.
真实正时间内部 entry， ||| a genuine positive-time internal entry;
正面价值同样明确。global-shell positive entries 自动 simple；outgoing coarea 给出 even-touch-safe 的尺度零 representation；fixed-packet amplitude excursions 给出真实 Leray-paid 替代对象。 ||| The positive value is equally clear. Global-shell positive entries are automatically simple; outgoing coarea gives a scale-zero representation safe for even touches; fixed-packet amplitude excursions give a genuine Leray-paid alternative object.
正时间 IFT 构造、内部缩放 no-go、outgoing occupation 表示、完整 trace-variation 账本与有限 Galerkin 复核。 ||| the positive-time IFT construction, internal scaling no-go, outgoing-occupation representation, complete trace-variation ledger, and finite Galerkin corroboration.
支持 level-averaged occupation 或 positive-height crossings。固定 smooth packet 的 amplitude-weighted excursions 确实由 Leray energy 支付；raw zero-entry count 不受 BV 或 W¹,² 控制。两轮 bounded audit 未定位到完整 raw-entry theorem；这不是原创性、优先权或不存在性声明。 ||| support level-averaged occupation or positive-height crossings. Amplitude-weighted excursions of a fixed smooth packet are genuinely paid by Leray energy; the raw zero-entry count is not controlled by BV or W¹,². Two bounded audit rounds located no complete raw-entry theorem; this is not a claim of originality, priority, or nonexistence.
支持本节使用的局部强流映射。 ||| supports the local strong flow map used in this section.
只改初始目标壳，在预定正时间把整个壳精确压到零 ||| Modify only the initial target shell to make the entire shell vanish exactly at a prescribed positive time
只排除所有 smooth 解上、covariant frame/window 下、常数沿该解族一致、RHS 恰为 bare normalized \(\dot H^{-1}\)-Lamb time integral 的定理。 ||| It rules out only a theorem over all smooth solutions with a covariant frame/window, a constant uniform along this solution family, and a right-hand side equal exactly to the bare normalized \(\dot H^{-1}\)-Lamb time integral.
状态 · R0.71T 构造与 no-go 完成 ||| Status · R0.71T construction and no-go completed
atom 是 λ⁻⁴，bare budget 是 λ⁻⁶ ||| The atom is λ⁻⁴; the bare budget is λ⁻⁶
base family 在 \([0,2\tau)\) 上满足 ||| On \([0,2\tau)\), the base family satisfies
exact producer 用 sparse rational Fourier 与 SymPy 检查八组对象；independent checker 用 32³ FFT、adaptive quadrature、finite differences 与 λ=1…128 的直接 sweep 重建六组对象。coarea 最大单位质量残差为 \(6.661\times10^{-16}\)，trace residual 为 \(1.110\times10^{-16}\)，ratio/λ² 最大相对残差为 \(3.559\times10^{-16}\)。 ||| The exact producer checks eight groups of objects using sparse rational Fourier algebra and SymPy; the independent checker reconstructs six groups using a 32³ FFT, adaptive quadrature, finite differences, and a direct sweep over λ=1…128. The maximum coarea unit-mass residual is \(6.661\times10^{-16}\), the trace residual is \(1.110\times10^{-16}\), and the maximum relative residual in ratio/λ² is \(3.559\times10^{-16}\).
Galerkin 图是截断 ODE 复核；continuum existence 与 no-go 来自解析证明和精确 NSE scaling。 ||| The Galerkin figure is a truncated-ODE corroboration; continuum existence and the no-go come from the analytic proof and exact NSE scaling.
IFT 是 continuum analytic theorem，不由脚本替代。有限 Galerkin 只复核 root shooting、横穿方向与渐近量级。 ||| The IFT is a continuum analytic theorem and is not replaced by a script. Finite Galerkin computation corroborates only root shooting, the crossing direction, and the asymptotic orders.
no-go 边界： ||| No-go boundary:
outgoing occupation 的 Leray payment、jet sum、recurrence packing、任意 localized root 的 simplicity、continuation criterion、finite-time singularity 或 global regularity。 ||| Leray payment for outgoing occupation; the jet sum; recurrence packing; simplicity of an arbitrary localized root; a continuation criterion; a finite-time singularity; or global regularity.
R0.71S 的缩放结论只覆盖初始 observation face。本节对同一 Fourier seed 做有限壳预补偿：标准局部 NSE 流映射与有限维隐函数定理把整个目标壳在预定正时间精确压到零，而 nonlinear Lamb forcing 仍非零。该零点是严格内部、simple、positive。随后取振幅 \(a_\lambda=\lambda^{-2}\) 再作 NSE 协变缩放，entry 原子按 λ⁻⁴、裸 normalized Leray-Lamb 时间预算按 λ⁻⁶，最优常数至少按 λ² 发散；初始能量与临界范数同时趋零。 ||| The scaling result in R0.71S covers only an initial observation face. This section applies finite-shell precompensation to the same Fourier seed: the standard local NSE flow map and a finite-dimensional implicit function theorem make the entire target shell vanish exactly at a prescribed positive time while the nonlinear Lamb forcing remains nonzero. The zero is strictly internal, simple, and positive. Then the amplitude \(a_\lambda=\lambda^{-2}\) is chosen before applying NSE covariant scaling: the entry atom scales as λ⁻⁴, the bare normalized Leray-Lamb time budget as λ⁻⁶, and the best constant diverges at least as λ²; the initial energy and critical norm both tend to zero.
R0.71S 仍可能被质疑为“只在起始面失败”。R0.71T 用正向 NSE 流和有限维 IFT 消除了这个疑问：同一尺度错配在 genuine internal entry 上出现，而且数据的能量尺度更好。这个结论足以停止 bare \(H^{-1}\)-Lamb time integral 的继续包装，避免在不同 temporal kernels 上重复支付同一两阶税。 ||| R0.71S could still be questioned as failing only at the initial face. R0.71T removes that doubt using the forward NSE flow and a finite-dimensional IFT: the same scale mismatch occurs at a genuine internal entry, and the data have better energy scaling. This conclusion is sufficient to stop further reformulations of the bare \(H^{-1}\)-Lamb time integral and avoid paying the same two-order tax again through different temporal kernels.
R0.71T · 2026-08-26 · 个人数学研究日志 ||| R0.71T · 2026-08-26 · Personal mathematics research log
R0.71T 有限 Galerkin 内部 entry、预补偿、entry atom 与双尺度缩放 ||| R0.71T finite Galerkin internal entry, precompensation, entry atom, and two-scale scaling
R0.71T｜真实内部 entry 排除裸 Leray 时间支付 ||| R0.71T | A genuine internal entry rules out bare Leray time payment
R0.71U 检查 global-shell jet 与 outgoing occupation 能否求和 ||| R0.71U tests whether the global-shell jet and outgoing occupation can be summed
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
  throw new Error("duplicate Chinese keys in R0.71T translation rows");
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
  "recap-r0-61-r0-71t.html",
  "notes/r0-71t.html",
]) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.05')) {
    throw new Error(relative + ": expected i18n cache version v1.05");
  }
}

const currentWithoutBatch = current.filter((entry) => !/^r071t\d+$/.test(entry.id));
const currentByChinese = new Map(
  currentWithoutBatch.map((entry) => [entry.zh, entry]),
);
if (currentByChinese.size !== currentWithoutBatch.length) {
  throw new Error("duplicate Chinese keys outside the R0.71T batch");
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
    id: "r071t" + String(index + 1).padStart(3, "0"),
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
