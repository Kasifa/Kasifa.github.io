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
处理 occupation、crossings 与 truncated variation。 ||| treat occupation, crossings, and truncated variation.
打开 86 节完整索引 ||| Open the complete 86-section index
给 level indicatrix 与 total variation； ||| give the level indicatrix and total variation;
给 weighted area formula； ||| give the weighted area formula;
开放接口 · R0.71W ||| Open interface · R0.71W
累计回顾与 86 节索引 ||| cumulative recap and 86-section index
平衡 decoupled background，并比较 atom 与完整 \(\nu^2\) baseline、projected rotational charge。 ||| Balance the decoupled background and compare the atom with the complete \(\nu^2\) baseline and projected rotational charge.
文献综述 v1.07 · 2026-08-26 ||| Literature review v1.07 · 2026-08-26
我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.71V 只列为研究笔记。我不把计算或笔记外推成正则性定理。 ||| I list published theorems as known results, mark 2026 preprints separately, and classify this site's R0.69P–R0.71V material only as research notes. I do not extrapolate calculations or notes into regularity theorems.
支持 weak energy spaces 与二维 strong-solution background。checked sources 给 level-integrated 或 almost-every-level 结论，不给 fixed zero-level quadratic trace。bounded audit 未定位到完整 R0.71V theorem；这不是原创性、优先权或不存在性结论。 ||| support weak energy spaces and the two-dimensional strong-solution background. The checked sources give level-integrated or almost-every-level conclusions, not a fixed zero-level quadratic trace. The bounded audit located no complete R0.71V theorem; this is not a claim of originality, priority, or nonexistence.
中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–U 给出 conditional incidence、genuine internal-entry、second-time-jet 与 finite recurrence 边界。R0.71V 再证明 Leray-paid excursion-height packing，并用 weighted area hierarchy、sine test 和 genuine 2.5D sequence 分离 level integral 与 fixed zero-level trace。保留下来的结果都不是全局正则性结论。 ||| . R0.69P–R0.71P reaches the positive-entry temporal-packing boundary; R0.71Q–U gives the conditional-incidence, genuine-internal-entry, second-time-jet, and finite-recurrence boundaries. R0.71V then proves Leray-paid excursion-height packing and uses the weighted-area hierarchy, sine test, and a genuine 2.5D sequence to separate the level integral from the fixed zero-level trace. None of the retained results is a global-regularity conclusion.
compact-shell AC representatives 与 weighted Cauchy–Schwarz 给 scale-zero excursion packing。area formula、sine test 与 fixed-target genuine 2.5D sequence 排除 first-row-only fixed-zero sampling；完整 \(\nu^2\) baseline 尚未排除。 ||| Compact-shell AC representatives and weighted Cauchy–Schwarz give scale-zero excursion packing. The area formula, sine test, and fixed-target genuine 2.5D sequence rule out first-row-only fixed-zero sampling; the complete \(\nu^2\) baseline remains unexcluded.
excursion height Leray-paid，fixed zero-level trace 仍开放 ||| Excursion height is Leray-paid; the fixed zero-level trace remains open
Hilbert sampling 给 zero-count-independent all-shell theorem；第一行 Leray-paid，第二行保留 recurrence tax。exact unforced 2.5D family 排除 unit energy–enstrophy ball 上的统一 raw count；atoms 可缩小。 ||| Hilbert sampling gives a zero-count-independent all-shell theorem; the first row is Leray-paid, while the second retains the recurrence tax. The exact unforced 2.5D family rules out a uniform raw count on the unit energy-enstrophy ball; the atoms may shrink.
R0.71V 的一手文献边界 ||| Primary-source boundary for R0.71V
R0.71V 关闭了什么，R0.71W 只检查什么 ||| What R0.71V closes and what R0.71W alone tests
R0.71V 在 Leray–Hopf 层级证明 compact-shell excursion-height packing，并写出 classical root atom 与 excursion 的精确无量纲转换因子 \(D_E\)。weighted area formula 只把 linear-slope level density 压到 first-time row；quadratic slope 需要 cubic time occupation，普通 \(L^1\) level control 不决定 distinguished zero-level trace。sine path 给抽象 method test，固定 target/window 的 genuine unforced 2.5D NSE 序列进一步排除只保留同一 first-time row 的指定零点采样。该序列不证明 second-time coefficient sharp，也不排除完整 global \(\nu^2\) baseline 或另一 dynamical charge。R0.71W 只检查完整 Leray ledger。我继续用下面六条筛选。 ||| R0.71V proves compact-shell excursion-height packing at the Leray–Hopf level and gives the exact dimensionless conversion factor \(D_E\) between a classical root atom and its excursion. The weighted area formula charges only the linear-slope level density to the first-time row; a quadratic slope requires cubic time occupation, and ordinary \(L^1\) level control does not determine the distinguished zero-level trace. The sine path is an abstract method test, while a fixed-target/window genuine unforced 2.5D NSE sequence further rules out prescribed-zero sampling that retains only the same first-time row. The sequence proves neither sharpness of the second-time coefficient nor failure of the complete global \(\nu^2\) baseline or another dynamical charge. R0.71W tests only the complete Leray ledger. I continue to use the six filters below.
01 · excursion 定理 ||| 01 · Excursion theorem
02 · 原子转换 ||| 02 · Atom conversion
05 · 真实 NSE 序列 ||| 05 · Genuine NSE sequence
06 · mollifier 极限 ||| 06 · Mollifier limits
08 · 审计 ||| 08 · Audit
把 variation 写成 level indicatrix 积分； ||| write variation as an integral of the level indicatrix;
版本 v0.71V · 2026-08-26 ||| Version v0.71V · 2026-08-26
背景边界： ||| Background boundary:
本节把 R0.71U 的两个时间 jet 拆开检查。compact Fourier shells 在 Leray–Hopf 层级有绝对连续代表，归一化 excursion height 满足尺度零求和定理。另一方面，一个固定目标、固定宏观时间窗的真实无外力 2.5D NSE 序列使第二个指定零点的 atom 与 first-time-jet row 之比按 \(q^2\) 增长；second-time row 仍能支付该事件。结果说明 level-integrated height 与 fixed zero-level slope 不能直接互换。 ||| This section examines the two time jets from R0.71U separately. Compact Fourier shells have absolutely continuous representatives at the Leray–Hopf level, and normalized excursion height obeys a scale-zero summation theorem. Separately, a genuine unforced 2.5D NSE sequence with a fixed target and fixed macroscopic time window makes the ratio between the second prescribed zero atom and the first-time-jet row grow as \(q^2\); the second-time row still pays for the event. Thus level-integrated height and fixed zero-level slope cannot be interchanged directly.
尺度零 amplitude-excursion packing 在 Leray–Hopf 层级成立。若另有统一 excursion-to-atom noncollapse，则可删除 R0.71U 的 second-time tax；真实 2.5D NSE boundary layer 证明该 noncollapse 不能仅由光滑、无外力和有界初始 energy/enstrophy 推出。 ||| Scale-zero amplitude-excursion packing holds at the Leray–Hopf level. A uniform excursion-to-atom noncollapse condition would remove the R0.71U second-time tax; the genuine 2.5D NSE boundary layer shows that such noncollapse does not follow solely from smooth unforced dynamics and bounded initial energy/enstrophy.
处理 occupation、upward/downward crossings 与 truncated variation。 ||| treat occupation, upward/downward crossings, and truncated variation.
但若在每个 level 保留目标二次斜率 \(\mathcal Q(z)\)，则 ||| But retaining the target quadratic slope \(\mathcal Q(z)\) at each level gives
第一行支付 excursion height，不支付任意固定零层斜率 ||| The first row pays excursion height, not an arbitrary fixed zero-level slope
对 outgoing occupation mollifier，\(\delta/|s|\to\infty\) 时 band 会越过整个坍缩 excursion，积分最终为零；\(\delta\asymp|s|\) 时得到依赖比例的 \(s^2\) profile；\(\delta/|s|\to0\) 才恢复 simple-root atom。两个极限不交换。这说明 exact coarea representation 仍需要 uniform endpoint control。 ||| For the outgoing occupation mollifier, when \(\delta/|s|\to\infty\), the band overtakes the entire collapsing excursion and the integral eventually vanishes; when \(\delta\asymp|s|\), it gives a ratio-dependent \(s^2\) profile; only when \(\delta/|s|\to0\) does it recover the simple-root atom. The two limits do not commute. Thus the exact coarea representation still needs uniform endpoint control.
在 Leray 层级，\(\mathcal M\) 与 \(\mathcal Q\) 只是 a.e.-\(z\) 等价类；只在 classical、finite-shell 且只有有限 isolated simple roots 时，\(\mathcal Q(0+)\) 才按点给出 jet mass。普通 \(L^1(dz)\) 控制不决定 distinguished zero-level boundary trace。 ||| At Leray regularity, \(\mathcal M\) and \(\mathcal Q\) are only almost-everywhere-in-\(z\) equivalence classes. Only in the classical finite-shell case with finitely many isolated simple roots does \(\mathcal Q(0+)\) give the jet mass pointwise. Ordinary \(L^1(dz)\) control does not determine the distinguished zero-level boundary trace.
附图比较 atom、两行 jet 与 excursion noncollapse ||| The figure compares the atom, both jet rows, and excursion noncollapse
固定零层原子仍需额外边界信息 ||| A fixed zero-level atom still needs additional boundary information
固定目标与固定时间窗下，第二个零点击穿 first-row-only sampling ||| With fixed target and fixed time window, the second zero defeats first-row-only sampling
记录 2D3C reduction。Leray 与 Temam 给弱能量框架，不给 \(C_{tt}\)、\(\omega_t\) 或 \(L_t\) 控制。 ||| records the 2D3C reduction. Leray and Temam provide the weak-energy framework, not control of \(C_{tt}\), \(\omega_t\), or \(L_t\).
解析证书与独立重建分别检查指数、极限与边界 ||| The analytic certificate and independent reconstruction separately check exponents, limits, and boundaries
精确不变类 ||| Exact invariant class
零层 ||| Zero level
令 \(r_j=\|C_j\|_2\)，\(K=[a,b]\) 长度为 \(\ell\)。对 \(\{r_j>0\}\) 每个向右从零点出发的连通分支 \(E\)，定义 ||| Let \(r_j=\|C_j\|_2\), and let \(K=[a,b]\) have length \(\ell\). In \(\{r_j>0\}\), for each connected component \(E\) that starts at a zero and runs to the right, define
取固定 target \(K_y=K_z=1\)。允许把 auxiliary shear frequencies 送到 \(q\to\infty\)，同时保持 target multiplier、macroscopic window、初始 energy/enstrophy 与 enstrophy ratio 统一有界。加入不进入 target annulus 的 decoupled background 后，指定第二个根相对所选 singleton target-shell rows 满足 ||| Fix the target \(K_y=K_z=1\). The auxiliary shear frequencies may tend to \(q\to\infty\) while the target multiplier, macroscopic window, initial energy/enstrophy, and enstrophy ratio remain uniformly bounded. After adding a decoupled background outside the target annulus, the second prescribed root satisfies the following relative to the selected singleton target-shell rows
缺口从“是否有 excursion”收缩为“零点斜率能否持续” ||| The gap narrows from whether an excursion exists to whether the zero slope persists
缺失量可以写成一个精确无量纲因子 ||| The missing quantity is an exact dimensionless factor
若所有目标事件满足统一 \(D_E\ge d_0>0\)，则原子和由上一节的 Leray 右端支付，不再需要 \(C_{tt}\)。这个条件要求零点斜率持续形成非坍缩 excursion；它不是 R0.71V 的无条件输入。 ||| If every target event satisfies a uniform \(D_E\ge d_0>0\), the atom sum is paid by the preceding Leray right side and no longer needs \(C_{tt}\). This condition requires the zero slope to persist into a noncollapsing excursion; it is not an unconditional input of R0.71V.
时间圆上的 \(C_N=N^{-1}\sin(Nt)e\)、\(Y=\kappa=1\) 有 \(2N\) 个 simple roots。每个 component 满足 ||| On the time circle, \(C_N=N^{-1}\sin(Nt)e\) with \(Y=\kappa=1\) has \(2N\) simple roots. Each component satisfies
数值部分只计算有限响应和一维求积，不 time-step NSE，也不承担 IFT remainder 或 continuum proof。 ||| The numerical part computes only finite responses and one-dimensional quadratures. It does not time-step NSE and does not carry the IFT remainder or continuum proof.
所以对任意 permissible finite shell selection，删除 second-time row 后仅保留同一 selected first row 的零点采样不能统一成立；singleton target-shell selection 已经失败。这不是对 complete fixed-frame ledger 的 no-go。该族让 selected second row 过度支付，不能据此声称 \(7\ell/3\) 最优；也没有排除保留完整 global \(\nu^2\) baseline 或另一 dynamical charge 的估计。 ||| Therefore, for any permissible finite shell selection, zero sampling cannot hold uniformly after deleting the second-time row and retaining only the same selected first row; the singleton target-shell selection already fails. This is not a no-go theorem for the complete fixed-frame ledger. The family makes the selected second row overpay, so it does not establish optimality of \(7\ell/3\); it also does not exclude an estimate retaining the complete global \(\nu^2\) baseline or another dynamical charge.
图 R0.71V。固定 target \(K_y=K_z=1\) 与 window 的 closed-response 计算复核 second prescribed root atom \(q^{-4}\)、selected singleton target-shell first row \(q^{-6}\)、second row \(q^{-2}\)、internal \(D_E\) 的 \(q^{-2}\) 和 terminal \(D_E\) 的 \(q^{-4}\) 标度。第一个 prescribed root 已另行支付。附图是可复现 corroboration，不代替 exact NSE diagonal argument。 ||| Figure R0.71V. With fixed target \(K_y=K_z=1\) and fixed window, the closed-response calculation checks the second prescribed root atom at \(q^{-4}\), the selected singleton target-shell first row at \(q^{-6}\), the second row at \(q^{-2}\), internal \(D_E\) at \(q^{-2}\), and terminal \(D_E\) at \(q^{-4}\). The first prescribed root is paid separately. The figure is reproducible corroboration, not a substitute for the exact NSE diagonal argument.
文献给出 area、variation 与 2D3C 背景，不给固定零层二次迹 ||| The literature provides area, variation, and 2D3C background, not a fixed zero-level quadratic trace
下一步移除或平衡 decoupled background，量化 fixed-target high-frequency events 相对 complete Leray ledger 的大小。若得到负面结论，必须让 atom 相对完整账本保持非坍缩；若得到正面结论，需要新的 dynamical inequality，而不是从 \(L^1\) level occupation 直接读取 fixed boundary trace。 ||| The next step removes or balances the decoupled background and quantifies fixed-target high-frequency events relative to the complete Leray ledger. A negative conclusion must keep the atom noncollapsing relative to the complete ledger; a positive conclusion needs a new dynamical inequality, not a direct reading of the fixed boundary trace from \(L^1\) level occupation.
下一对象：complete Leray ledger ||| Next object: complete Leray ledger
先压振幅与先取零层极限给出不同结果 ||| Shrinking amplitude first and taking the zero-level limit first give different results
限定检索没有定位到把 level-integrated control 提升为 fixed zero-level quadratic trace、同时不增加 reverse average 或 persistence 假设的定理。这不是原创性、优先权或不存在性声明。 ||| The bounded search located no theorem that promotes level-integrated control to a fixed zero-level quadratic trace without adding a reverse-average or persistence hypothesis. This is not a claim of originality, priority, or nonexistence.
研究笔记 R0.71V · EXCURSION PACKING · ZERO-LEVEL BOUNDARY ||| Research note R0.71V · EXCURSION PACKING · ZERO-LEVEL BOUNDARY
研究笔记 R0.71V：Leray–Hopf 层级的尺度零 excursion-height packing，以及固定目标、固定时间窗的真实无外力 2.5D NSE first-row-only sampling obstruction。 ||| Research note R0.71V: scale-zero excursion-height packing at the Leray–Hopf level and a genuine unforced 2.5D NSE obstruction to first-row-only sampling with a fixed target and fixed time window.
一维 weighted area formula 给出 ||| The one-dimensional weighted area formula gives
因此 \(\#\{(j,E):H_E\ge\delta\}\le\delta^{-2}B_1(K)/\ell\)。finite shell/component 结论由 Tonelli 与 monotone convergence 扩展到 countable family。若某个 component 在左端 \(a\) 已经为正，它不属于 right-rooted family，必须另付 initial trace。 ||| Hence \(\#\{(j,E):H_E\ge\delta\}\le\delta^{-2}B_1(K)/\ell\). The finite shell/component result extends to a countable family by Tonelli and monotone convergence. A component already positive at the left endpoint \(a\) is not in the right-rooted family and requires a separate initial trace.
于是 \(\sum_EH_E^2=1/\pi^2\)，而 zero-slope proxy sum 为 \(2N\)。同时 \(\int\mathcal Q_N=4/3\)、\(\int\mathcal M_N=\pi/2\)，二者零层迹仍是 \(2N\)。这是 shell-path method test，不是真实 NSE 轨迹。 ||| Thus \(\sum_EH_E^2=1/\pi^2\), while the zero-slope proxy sum is \(2N\). Also, \(\int\mathcal Q_N=4/3\) and \(\int\mathcal M_N=\pi/2\), yet both zero-level traces remain \(2N\). This is a shell-path method test, not a genuine NSE trajectory.
在 classical simple root \(t_E\) 上，令 \(s_E=\|C_{j,t}(t_E)\|_2\)，并定义 ||| At a classical simple root \(t_E\), set \(s_E=\|C_{j,t}(t_E)\|_2\) and define
这不是千禧年问题的解答。本节没有给出 weak zero-jet、继续性判据、有限时奇性或全局正则性。 ||| This is not a solution to the Millennium problem. This section provides no weak zero-jet, continuation criterion, finite-time singularity, or global regularity.
真实 NSE ||| Genuine NSE
真实 NSE 序列使用不进入目标 annulus 的 decoupled background 来保持正 enstrophy floor；完整 global \(\nu^2\) baseline 尚未被排除。 ||| The genuine NSE sequence uses a decoupled background outside the target annulus to maintain a positive enstrophy floor; the complete global \(\nu^2\) baseline remains unexcluded.
振幅 excursion 可以由 Leray 支付， ||| Amplitude excursions can be paid by Leray,
振幅 excursion 可由第一时间 jet 支付；二次零斜率原子仍是固定零层边界迹。 ||| Amplitude excursions can be paid by the first-time jet; a quadratic zero-slope atom remains a fixed zero-level boundary trace.
正面结果把一类尺度零、可在 Leray–Hopf 层级定义的 excursion mass 完整支付。负面结果说明同一支付不能自动读取 fixed zero-level slope；真实 NSE boundary layer 能把斜率压进越来越窄、越来越低的 excursion。 ||| The positive result fully pays a class of scale-zero excursion masses defined at the Leray–Hopf level. The negative result shows that the same payment cannot automatically read a fixed zero-level slope; the genuine NSE boundary layer compresses the slope into progressively narrower and lower excursions.
转换 ||| Conversion
状态 · R0.71V 两条边界完成 ||| Status · both R0.71V boundaries completed
closed-response figure 是 corroboration，不是 DNS，也不承担解析证明。 ||| The closed-response figure is corroboration, not DNS, and does not carry the analytic proof.
compact shell 的归一化 excursion height 可以统一求和 ||| Normalized excursion heights of compact shells are uniformly summable
非空正 excursion 有 \(h_E>0\)；连续性与 annular Bernstein 蕴含 \(Y_E>0\)，所以归一化有定义。compact torus annulus 只含有限 lattice modes；Leray–Hopf 弱方程使每个 shell coefficient 属于 \(W^{1,1}(K)\)。加权 Cauchy–Schwarz 与 R0.71U 第一行给出 ||| A nonempty positive excursion has \(h_E>0\); continuity and annular Bernstein imply \(Y_E>0\), so the normalization is defined. A compact torus annulus contains only finitely many lattice modes; the Leray–Hopf weak equation puts every shell coefficient in \(W^{1,1}(K)\). Weighted Cauchy–Schwarz and the R0.71U first row give
exact audit 检查 area algebra、sine constants、尺度指数、2.5D response asymptotics、IFT tangent、first/second-row powers 与 mollifier regimes；excursion inequality 本身由解析证明承担。research independent audit 不读取 producer certificate；figure package 的 ||| The exact audit checks the area algebra, sine constants, scale exponents, 2.5D response asymptotics, IFT tangent, first/second-row powers, and mollifier regimes; the excursion inequality itself is carried by the analytic proof. The research independent audit does not read the producer certificate; the figure package's
以独立重建完成 21 项 response、quadrature、prefactor 与 output checks。 ||| performs 21 response, quadrature, prefactor, and output checks through an independent reconstruction.
Leray 支付一次斜率，二次零斜率带来三次时间 occupation ||| Leray pays one slope; a quadratic zero-slope charge produces cubic time occupation
Leray–Hopf compact-shell AC trace；scale-zero excursion-height packing；精确 \(D_E\) 因子；weighted area hierarchy；sine obstruction；固定 target/window 的真实无外力 2.5D repeated-root first-row obstruction。 ||| Leray–Hopf compact-shell AC traces; scale-zero excursion-height packing; the exact \(D_E\) factor; the weighted-area hierarchy; the sine obstruction; and a genuine unforced 2.5D repeated-root first-row obstruction with fixed target/window.
level integral 保持有界时，零层迹仍可按根数增长 ||| The zero-level trace can grow with the number of roots while the level integral stays bounded
R0.71U 的 second-time row 因而不是单纯证明技术遗留：当前序列确实需要比 first row 更强的时间信息。不过本节没有证明现有 second-time coefficient sharp，也没有排除另一种完整 Leray 账本。 ||| The R0.71U second-time row is therefore not merely a proof artifact: the present sequence genuinely requires stronger time information than the first row. This section does not prove the current second-time coefficient sharp and does not rule out another complete Leray ledger.
R0.71U second-time coefficient sharp；所有替代 Leray zero-atom estimate 都不可能；weak zero-jet；localized-cell theorem；single-trajectory infinite recurrence；继续性、有限时奇性或 global regularity。 ||| sharpness of the R0.71U second-time coefficient; impossibility of every alternative Leray zero-atom estimate; a weak zero-jet; a localized-cell theorem; single-trajectory infinite recurrence; continuation, a finite-time singularity, or global regularity.
R0.71V · 2026-08-26 · 个人数学研究日志 ||| R0.71V · 2026-08-26 · Personal mathematics research log
R0.71V 零层边界、first-time row、second-time row 与 excursion noncollapse ||| R0.71V zero-level boundary, first-time row, second-time row, and excursion noncollapse
R0.71V｜Leray-paid excursion 与零层边界 ||| R0.71V | Leray-paid excursion and the zero-level boundary
R0.71W 检查完整 \(\nu^2\) baseline 与 projected rotational term ||| R0.71W tests the complete \(\nu^2\) baseline and projected rotational term
02 · 86 节完整索引 ||| 02 · Complete 86-section index
打开最新节点 R0.71V ||| Open the latest node R0.71V
负面边界是 fixed zero-level trace。weighted coarea 对二次 slope 产生三次时间 occupation；sine path 显示 level integral 与零层迹可以分离。真实无外力 2.5D NSE 序列又在固定 target/window 下使第二个 atom 相对 first row 按 \(q^2\) 增长。它没有证明 second-time coefficient sharp，也没有排除完整 global \(\nu^2\) baseline 或另一 dynamical charge。 ||| The negative boundary is the fixed zero-level trace. Weighted coarea turns a quadratic slope into cubic time occupation; the sine path separates the level integral from the zero-level trace. A genuine unforced 2.5D NSE sequence with fixed target/window further makes the ratio of the second atom to the first row grow as \(q^2\). It proves neither sharpness of the second-time coefficient nor failure of the complete global \(\nu^2\) baseline or another dynamical charge.
负面结论必须让 atom 相对完整账本保持非坍缩；正面结论需要新的 dynamical inequality，不能从 \(L^1\) level occupation 直接读取 distinguished zero-level boundary trace。R0.71W 仍不宣称继续性、奇性排除或全局正则性。 ||| A negative conclusion must keep the atom noncollapsing relative to the complete ledger; a positive conclusion needs a new dynamical inequality and cannot read the distinguished zero-level boundary trace directly from \(L^1\) level occupation. R0.71W still claims no continuation, singularity exclusion, or global regularity.
回顾截止节点：R0.71V ||| Recap endpoint: R0.71V
回顾截止时公开笔记：146 ||| Public notes at recap endpoint: 146
截至 R0.71V，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 86 个节点解释成对千禧年问题完成了某个比例。 ||| As of R0.71V, there is no new unconditional continuation criterion, no reduction of the set of all potential singular solutions, and no proof of finite-time breakdown. The 86 nodes cannot be interpreted as a percentage completion of the Millennium problem.
累计回顾 · R0.61–R0.71V · 2026-08-26 ||| Cumulative recap · R0.61–R0.71V · 2026-08-26
十二个阶段、86 个节点：从约化递推到 conditional incidence，再到 genuine internal entry、classical second-time-jet packing、Leray-paid excursion 与真实 NSE fixed-zero obstruction。 ||| Twelve phases and 86 nodes: from reduced recurrence to conditional incidence, then genuine internal entry, classical second-time-jet packing, Leray-paid excursions, and a genuine NSE fixed-zero obstruction.
收录节点：86 ||| Included nodes: 86
下一有限任务移除或平衡 decoupled background，量化 fixed-target high-frequency events 相对完整 \(\nu^2\) baseline 与 projected rotational term 的大小。 ||| The next finite task removes or balances the decoupled background and quantifies fixed-target high-frequency events relative to the complete \(\nu^2\) baseline and projected rotational term.
这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71V 的 86 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。 ||| This page follows the R0.00–R0.60 phase recap and organizes the research nodes from R0.61 through R0.71V, 86 in total. I record chronologically what each phase actually proved, which proposals were excluded by concrete counterexamples or scale analysis, and which conditions still have not been derived from the Navier–Stokes equations.
正面结果是 Leray–Hopf compact-shell excursion theorem：归一化高度 \(H_E^2=\kappa_j^{-6}h_E^2/(\ell Y_E)\) 可统一求和，并给出 amplitude-thresholded excursion count。若另有统一 \(D_E\ge d_0>0\)，它会把 R0.71U 的 root atoms 压回 first-time row；该 noncollapse 不是无条件输入。 ||| The positive result is the Leray–Hopf compact-shell excursion theorem: normalized heights \(H_E^2=\kappa_j^{-6}h_E^2/(\ell Y_E)\) are uniformly summable and give an amplitude-thresholded excursion count. An additional uniform \(D_E\ge d_0>0\) would charge the R0.71U root atoms back to the first-time row; that noncollapse is not an unconditional input.
excursion height 已由 Leray 支付，fixed zero-level slope 仍是边界迹 ||| Excursion height is paid by Leray; the fixed zero-level slope remains a boundary trace
R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 86 个节点沿着这个缺口推进。 ||| The R0.00–R0.60 material remains in the preceding phase recap. The R0.60 conclusion was that the full Fourier–Leray structure and higher-order computations could continue, but still did not control a critical quantity for general three-dimensional solutions. The following 86 nodes advance along that gap.
R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71V 的 86 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、条件 incidence theorem、second-time jet，再到 Leray-paid excursion 与固定零层边界的路线。 ||| Post-R0.60 research recap: a chronological organization of the research nodes from R0.61 through R0.71V, 86 in total, recording the route from reduced recurrence to projected-Lamb heat volume, positive-entry batching, the conditional incidence theorem, the second-time jet, Leray-paid excursions, and the fixed zero-level boundary.
R0.61–R0.71V 的 86 节公开笔记 ||| Public notes from R0.61–R0.71V: 86 sections
R0.61–R0.71V 回顾 · 2026-08-26 ||| R0.61–R0.71V recap · 2026-08-26
R0.61–R0.71V 研究节点 ||| R0.61–R0.71V research nodes
R0.61–R0.71V｜R0.60 之后的研究回顾 ||| R0.61–R0.71V | Post-R0.60 research recap
R0.70A–R0.71V 完成版本 ||| R0.70A–R0.71V completed releases
R0.71G–R0.71V · temporal packing、finite recurrence 与 fixed-zero boundary ||| R0.71G–R0.71V · temporal packing, finite recurrence, and the fixed-zero boundary
R0.71O–P 恢复 soft quotient 的一侧 traces，并用同刻 spatial batching 吸收有限 frame multiplicity；R0.71Q–R 给出 finite conditional Jensen 与 incidence theorems。R0.71S–T 证明 critical packet 的 Bessel 税，并构造 genuine positive-time internal entry 以排除 bare normalized Leray–Lamb time payment。R0.71U 给出 zero-count-independent classical second-time-jet theorem；第一行 Leray-paid，第二行保留 recurrence tax，同时 exact unforced 2.5D family 排除 unit energy–enstrophy ball 上的统一 raw count。R0.71V 再证明 compact-shell excursion-height packing 可在 Leray–Hopf 层级由第一行支付，并写出 excursion-to-atom 因子 \(D_E\)。weighted area formula 与 sine test 表明 level integral 不能自动控制 distinguished zero-level quadratic trace；固定 target/window 的真实无外力 2.5D NSE 序列进一步使 second root atom 相对 first row 按 \(q^2\) 增长，而 second row 仍可支付。 ||| R0.71O–P restores one-sided traces of the soft quotient and uses same-time spatial batching to absorb finite frame multiplicity; R0.71Q–R gives finite conditional Jensen and incidence theorems. R0.71S–T proves the Bessel tax of a critical packet and constructs a genuine positive-time internal entry to rule out a bare normalized Leray–Lamb time payment. R0.71U gives a zero-count-independent classical second-time-jet theorem; the first row is Leray-paid, while the second retains the recurrence tax, and an exact unforced 2.5D family rules out a uniform raw count on the unit energy-enstrophy ball. R0.71V then proves that the first row pays compact-shell excursion-height packing at the Leray–Hopf level and gives the excursion-to-atom factor \(D_E\). The weighted area formula and sine test show that a level integral does not automatically control the distinguished zero-level quadratic trace; a fixed-target/window genuine unforced 2.5D NSE sequence further makes the second-root atom relative to the first row grow as \(q^2\), while the second row still pays.
R0.71V 的 Leray–Hopf compact-shell AC representatives、scale-zero excursion-height packing、精确 excursion-to-atom 因子、weighted area hierarchy 与 sine method test；以及固定 target/window 的 genuine unforced 2.5D first-row-only sampling obstruction。完整 global \(\nu^2\) baseline 与替代 dynamical charge 尚未排除。 ||| R0.71V provides Leray–Hopf compact-shell AC representatives, scale-zero excursion-height packing, the exact excursion-to-atom factor, the weighted-area hierarchy, and the sine method test; it also gives a fixed-target/window genuine unforced 2.5D obstruction to first-row-only sampling. The complete global \(\nu^2\) baseline and alternative dynamical charges remain unexcluded.
R0.71V 附图 ||| R0.71V figure
R0.71V 证书 ||| R0.71V certificates
R0.71W 检查完整 Leray ledger ||| R0.71W tests the complete Leray ledger
本节没有得到 weak zero-jet、继续性、finite-time singularity 或 global regularity；closed-response figure 只作可复现 corroboration。 ||| This section obtains no weak zero-jet, continuation, finite-time singularity, or global regularity; the closed-response figure is reproducible corroboration only.
从有符号环带障碍走到 Leray-paid excursion 与固定零层边界 ||| From the signed-annulus obstruction to Leray-paid excursions and the fixed zero-level boundary
固定 target \(K_y=K_z=1\) 与固定 macroscopic window 的 exact unforced 2.5D NSE 序列，对 second prescribed root 与 selected singleton target-shell rows 满足 \[ J_{2,q}/((2/\ell)B_{1,q}^{(*)})\asymp q^2,\qquad J_{2,q}/((7\ell/3)B_{2,q}^{(*)})\asymp q^{-2}. \] selected second-time row 能支付该事件，同一 selected first-time row 单独不能；singleton selection 已经失败。这不是 complete fixed-frame ledger 的 no-go。该族不证明 \(7\ell/3\) sharp，也不排除完整 global \(\nu^2\) baseline 或另一 dynamical charge。 ||| With fixed target \(K_y=K_z=1\) and fixed macroscopic window, the exact unforced 2.5D NSE sequence satisfies, for the second prescribed root and selected singleton target-shell rows, \[ J_{2,q}/((2/\ell)B_{1,q}^{(*)})\asymp q^2,\qquad J_{2,q}/((7\ell/3)B_{2,q}^{(*)})\asymp q^{-2}. \] The selected second-time row pays for the event, while the same selected first-time row alone does not; the singleton selection already fails. This is not a no-go theorem for the complete fixed-frame ledger. The family does not prove \(7\ell/3\) sharp and does not exclude the complete global \(\nu^2\) baseline or another dynamical charge.
环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero first-row obstruction ||| annulus exclusion → source-core ledger → covariance spectral stratification → all-frequency conditional bridge → response-slope chord gain → shared-response first-order channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero first-row obstruction
检查 fixed-target high-frequency events 相对完整 \(\nu^2\) baseline 与 projected rotational term 是否仍非坍缩；fixed zero-level trace 不能直接从 level-integrated occupation 读取。 ||| Test whether fixed-target high-frequency events remain noncollapsing relative to the complete \(\nu^2\) baseline and projected rotational term; the fixed zero-level trace cannot be read directly from level-integrated occupation.
检查完整 \(\nu^2\) baseline 与 projected rotational term，判断 fixed-target high-frequency events 相对完整 Leray ledger 是否仍非坍缩。 ||| Test the complete \(\nu^2\) baseline and projected rotational term to determine whether fixed-target high-frequency events remain noncollapsing relative to the complete Leray ledger.
静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–T 建立 projected-Lamb 热体积、局部化、temporal packing 与 genuine internal-entry no-go。R0.71U 给出 classical second-time-jet theorem 与 exact finite recurrence。R0.71V 证明 compact-shell excursion-height packing 可由 Leray–Hopf 第一行支付；weighted area formula、sine test 与 fixed-target 2.5D NSE 序列同时表明 distinguished zero-level slope 仍需 noncollapse 或另一 dynamical charge。 ||| After the static annular families are rigorously excluded, the main route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71A–T establishes projected-Lamb heat volume, localization, temporal packing, and a genuine internal-entry no-go. R0.71U gives the classical second-time-jet theorem and exact finite recurrence. R0.71V proves that the Leray–Hopf first row pays compact-shell excursion-height packing; the weighted area formula, sine test, and fixed-target 2.5D NSE sequence together show that the distinguished zero-level slope still needs noncollapse or another dynamical charge.
累计回顾 R0.61–R0.71V · 2026-08-26 ||| Cumulative recap R0.61–R0.71V · 2026-08-26
目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71V 在 Leray–Hopf 层级支付 scale-zero excursion height；fixed target/window 的 genuine 2.5D sequence 排除只保留 first-time row 的指定零点采样。second-time row 仍可支付，完整 global \(\nu^2\) baseline 与替代账本尚未排除。 ||| There is still no new unconditional continuation criterion and no construction of a finite-time singularity. R0.71V pays scale-zero excursion height at the Leray–Hopf level; the fixed-target/window genuine 2.5D sequence rules out prescribed-zero sampling that retains only the first-time row. The second-time row still pays, while the complete global \(\nu^2\) baseline and alternative ledgers remain unexcluded.
上次综述 v1.06 · 2026-08-26 ||| Previous review v1.06 · 2026-08-26
我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71V 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。 ||| I also prepared a systematic review that places classical theory, five main literature strands, the candidate-blowup exclusion tree, progress from 2019—2026, and this site's R0.69P–R0.71V route in one view. The historical R0.61–R0.69O nodes remain in the cumulative recap.
下一步 R0.71W： ||| Next step R0.71W:
研究笔记 R0.71V · 2026-08-26 ||| Research note R0.71V · 2026-08-26
移除或平衡 decoupled background，比较 fixed-target high-frequency atom 与完整 \(\nu^2\) baseline、projected rotational term。 ||| Remove or balance the decoupled background and compare the fixed-target high-frequency atom with the complete \(\nu^2\) baseline and projected rotational term.
阅读 R0.71V 研究笔记 → ||| Read research note R0.71V →
展开 56 篇公开笔记 ||| Expand 56 public notes
综述 v1.07 · 2026-08-26 ||| Review v1.07 · 2026-08-26
classical root atom 与 excursion 的精确转换因子是 \[ D_E=\frac{h_E^2Y(t_E)}{\ell Y_Es_E^2}. \] 统一 \(D_E\ge d_0>0\) 会关闭 first-row payment；weighted area formula 与 sine test 说明，这种 fixed-zero noncollapse 不能从 level-integrated \(L^1\) 控制自动推出。 ||| The exact conversion factor between a classical root atom and its excursion is \[ D_E=\frac{h_E^2Y(t_E)}{\ell Y_Es_E^2}. \] A uniform \(D_E\ge d_0>0\) would close the first-row payment; the weighted area formula and sine test show that this fixed-zero noncollapse does not follow automatically from level-integrated \(L^1\) control.
compact Fourier shells 在 Leray–Hopf 层级有绝对连续代表。对每个正 excursion \(E\)， \[ H_E^2=\frac{\kappa_j^{-6}h_E^2}{\ell Y_E}, \qquad \sum_{j,E}H_E^2\le\frac{B_1(K)}{\ell}. \] 因此 amplitude-thresholded excursion count 有尺度零上界，并可由 finite family 经 Tonelli 与 monotone convergence 扩展。 ||| Compact Fourier shells have absolutely continuous representatives at the Leray–Hopf level. For every positive excursion \(E\), \[ H_E^2=\frac{\kappa_j^{-6}h_E^2}{\ell Y_E}, \qquad \sum_{j,E}H_E^2\le\frac{B_1(K)}{\ell}. \] Therefore the amplitude-thresholded excursion count has a scale-zero bound and extends from finite families by Tonelli and monotone convergence.
excursion height 可由 Leray 支付，固定零层斜率仍需额外信息 ||| Excursion height can be paid by Leray; the fixed zero-level slope still needs additional information
Leray–Hopf excursion-height packing 成立；fixed zero-level atom 不能只由同一 first-time row 统一支付。 ||| Leray–Hopf excursion-height packing holds; a fixed zero-level atom cannot be uniformly paid by the same first-time row alone.
R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen/incidence、packet/Bessel、internal-entry scaling、second-time jet、finite recurrence、Leray-paid excursion 与 fixed-zero boundary。R0.70A–R0.71V 共 48 个完成版本。 ||| The post-R0.60 route has twelve segments: reduced Picard analysis and the shear boundary; transverse perturbations; local pressure budgets; signed physical annuli; moving labels and source-core duality; defect tensors and finite observations; full-frame covariance; the constant-projection boundary; positive output and the material-heat tent; projected-Lamb heat volume; local heat packing and the critical-trace obstruction; and positive-entry temporal packing, conditional Jensen/incidence, packet/Bessel analysis, internal-entry scaling, the second-time jet, finite recurrence, Leray-paid excursions, and the fixed-zero boundary. R0.70A–R0.71V contains 48 completed releases.
R0.60 recap 之后的累计回顾收录 86 个节点；全站现有 146 篇公开研究笔记 ||| The cumulative recap after the R0.60 recap contains 86 nodes; the full site now has 146 public research notes
R0.71V 已完成： ||| R0.71V completed:
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
  throw new Error("duplicate Chinese keys in R0.71V translation rows");
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
  "recap-r0-61-r0-71v.html",
  "notes/r0-71v.html",
]) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.07')) {
    throw new Error(relative + ": expected i18n cache version v1.07");
  }
}

const previous = await readFile(
  resolve(publicDirectory, "notes/r0-71u.html"),
  "utf8",
);
if (!previous.includes('/i18n-en.js?v=1.06')) {
  throw new Error("notes/r0-71u.html: expected historical i18n cache version v1.06");
}

const currentWithoutBatch = current.filter((entry) => !/^r071v\d+$/.test(entry.id));
const currentByChinese = new Map(
  currentWithoutBatch.map((entry) => [entry.zh, entry]),
);
if (currentByChinese.size !== currentWithoutBatch.length) {
  throw new Error("duplicate Chinese keys outside the R0.71V batch");
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
    "translation batch does not equal active missing set (" +
      missing.length +
      "):\n" +
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
    id: "r071v" + String(index + 1).padStart(3, "0"),
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
