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
  "scripts/i18n-snapshots/r072j-missing.json",
);

const translationRows = String.raw`
本节的 graph classification 是精确离散定理；物理 no-go 只覆盖声明的 common-band aligned perturbative families。限定检索没有发现把这些三项直接组合成 arbitrary-carrier complete-root theorem 的来源；这是 bounded non-collision check，不是原创性、优先权或一般 NSE 结论。 ||| The graph classification in this section is an exact discrete theorem; the physical no-go covers only the stated common-band aligned perturbative families. The bounded search found no source that directly combines these three ingredients into an arbitrary-carrier complete-root theorem; this is a bounded non-collision check, not a claim of novelty, priority, or a conclusion about general NSE.
打开 100 节完整索引 ||| Open the complete 100-note index
的 Cayley graph homomorphism criterion 支持 gcd 约化后的二分分类；它不区分目标 row 的长度三返回与更长奇闭路。真实 cubic 返回由 \(R_1(0)\cap R_2(0)\) 决定，等价于三载波有符号关系。 ||| 's Cayley graph homomorphism criterion supports the bipartite classification after gcd reduction; it does not distinguish a length-three return to the target row from a longer odd closed walk. The true cubic return is determined by \(R_1(0)\cap R_2(0)\), equivalently by a signed three-carrier relation.
给出 sum-free sets 的标准语言，但不估计带相位、热权和物理 lift 的 signed convolution。 ||| gives the standard language of sum-free sets, but does not estimate the signed convolution with phases, heat weights, and the physical lift.
检查跨热时间尺度的 triangles、完整强耦合账本，或不依赖实 Rolle 符号交替的 complex target complete-root mechanism。 ||| Test triangles across heat time scales, a complete strong-coupling ledger, or a complex-target complete-root mechanism that does not rely on real Rolle sign alternation.
开放接口 · R0.72K ||| Open interface · R0.72K
累计回顾与 100 节索引 ||| Cumulative recap and 100-note index
目标 carrier Cayley 图二分当且仅当所有约化载波为奇数；non-bipartite 不等于 triangle return。相干稠密块虽有 raw \(\mathcal C_{\times,R}\asymp R^2\)，true cubic contribution 的归一化比仍衰减。 ||| The target carrier Cayley graph is bipartite if and only if every reduced carrier is odd; non-bipartite does not mean triangle return. Although a coherent dense block has raw \(\mathcal C_{\times,R}\asymp R^2\), the normalized ratio of the true cubic contribution still decays.
提供相邻的 bilinear、trilinear 和 semigroup Carleson 框架；它们不直接给出 endogenous \(h=P_0VF\)、\(b=P_0V^2F\) 的 joint exposure 或 complex-root ledger。 ||| provide nearby bilinear, trilinear, and semigroup Carleson frameworks; they do not directly give joint exposure or a complex-root ledger for the endogenous \(h=P_0VF\) and \(b=P_0V^2F\).
文献综述 v1.23 · 2026-08-27 ||| Literature review v1.23 · 2026-08-27
我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.72J 只列为研究笔记。我不把计算或笔记外推成正则性定理。 ||| I list published theorems as known results, mark 2026 preprints separately, and list R0.69P–R0.72J on this site only as research notes. I do not extrapolate computations or notes into regularity theorems.
中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–U 给出 conditional incidence、genuine internal-entry、second-time-jet 与 finite recurrence 边界。R0.71V–W 分离 fixed zero-level trace 并排除 data-uniform complete first-row ledger。R0.71X 在 fixed-dimensional small-coupling family 内达到 one-third endpoint；R0.71Y 处理 selected roots；R0.71Z 给出 all-root slope-mass bound 和 launch-inclusive floor cancellation；R0.72A 把 strong-coupling loss 局部化到实际观察层，R0.72B 保留 exact target-row participation，R0.72C 得到 phase-uniform exact-launch \(M^{-8/3}\) 与 fixed-positive tail \(M^{-3}\) 的 sharp algebraic scales。R0.72D 在 shifted Rudin–Shapiro family 上构造 positive-time exact root，保留 full rotational charge，并得到非消失但不发散的 normalized complete-root ledger。R0.72E 回到 fixed-carrier Bessel family，以定量 negative-Sobolev action 证明 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。R0.72F 再用 regularly varying initial-layer weights 分离 selected-root 的 \(1/3\) 阈值与 Leray payment 的 \(1/2\) 阈值，并选出 critical-log 最小边界。R0.72G 在 exact real one-carrier lattice 上用 phase gauge、目标行恒等式与 Rolle–BV 归约证明完整根质量恰为对数量级，并得到 critical-log complete-root sharp saturation。R0.72H 在有限共轭配对多载波系统中证明 mixed row 的载波数无关 moment-resolved payment；全奇数 Rudin–Shapiro 族排除 action-only 版本，并使该 moment 所编码的载波幂次达到同阶。R0.72I 证明分离的 \(B_AQ_*\) 正项不能逐项物理吸收，同时用 joint exposure 和 odd-carrier parity 证明真实 complete ledger 统一衰减。R0.72J 完成 gcd-reduced Cayley graph 的二分分类，区分 odd cycle 与 triangle return，并证明 common-band coherent mixed-parity cubic 在物理归一化后仍衰减。一般 Navier–Stokes 正则性仍开放。 ||| . R0.69P–R0.71P reaches the positive-entry temporal-packing boundary, and R0.71Q–U gives the boundaries for conditional incidence, genuine internal entry, the second-time jet, and finite recurrence. R0.71V–W separates the fixed zero-level trace and excludes a data-uniform complete first-row ledger. R0.71X reaches the one-third endpoint in a fixed-dimensional small-coupling family; R0.71Y treats selected roots; R0.71Z gives an all-root slope-mass bound and launch-inclusive floor cancellation. R0.72A localizes the strong-coupling loss to the actual observation layer, R0.72B retains exact target-row participation, and R0.72C obtains the sharp algebraic scales \(M^{-8/3}\) for phase-uniform exact launch and \(M^{-3}\) for the fixed-positive tail. R0.72D constructs a positive-time exact root in a shifted Rudin–Shapiro family, retains the full rotational charge, and obtains a nonvanishing but nondivergent normalized complete-root ledger. R0.72E returns to a fixed-carrier Bessel family and uses a quantitative negative-Sobolev action estimate to make the complete-root ledger relative to the candidate \(D^{1/3}\Lambda_1\) payment diverge like \(R^{4/3}\). R0.72F then uses regularly varying initial-layer weights to separate the selected-root threshold \(1/3\) from the Leray-payment threshold \(1/2\), selecting the minimal critical-log boundary. On the exact real one-carrier lattice, R0.72G uses a phase gauge, target-row identities, and the Rolle–BV reduction to prove that the complete root mass has exactly logarithmic order and obtains sharp critical-log complete-root saturation. In a finite conjugate-paired multi-carrier system, R0.72H proves a carrier-count-independent moment-resolved payment for the mixed row; an all-odd Rudin–Shapiro family excludes the action-only version and attains the carrier power encoded by that moment. R0.72I proves that the separated positive \(B_AQ_*\) term cannot be absorbed physically term by term, while joint exposure and odd-carrier parity prove that the true complete ledger decays uniformly. R0.72J completes the bipartite classification of the gcd-reduced Cayley graph, distinguishes an odd cycle from a triangle return, and proves that a common-band coherent mixed-parity cubic still decays after physical normalization. General Navier–Stokes regularity remains open.
gcd-reduced graph classification 与 common-band cubic no-go ||| gcd-reduced graph classification and common-band cubic no-go
R0.72J 的 Cayley graph、additive triangle 与 root 边界 ||| Cayley graph, additive-triangle, and root boundary of R0.72J
R0.72J 的主张边界 ||| Claim boundary for R0.72J
\(R=64\) 时 \(T_R=12480\)、\(|b(0)|=8824.692629208112\)，且 \(\mathcal C_{\times,R}=69.2166385023\)。末三档 raw 与 normalized 斜率分别为 1.9501881021 和 -0.7370277418。 ||| At \(R=64\), \(T_R=12480\), \(|b(0)|=8824.692629208112\), and \(\mathcal C_{\times,R}=69.2166385023\). The raw and normalized slopes over the final three scales are 1.9501881021 and -0.7370277418, respectively.
\[ \boxed{\operatorname{Cay}(\mathbb Z;\{\pm a_j\})\text{ 二分} \quad\Longleftrightarrow\quad a_j\equiv1\pmod2\ \text{对所有 }j.} \] ||| \[ \boxed{\operatorname{Cay}(\mathbb Z;\{\pm a_j\})\text{ is bipartite} \quad\Longleftrightarrow\quad a_j\equiv1\pmod2\ \text{for every }j.} \]
00 · 四句判断 ||| 00 · Four conclusions
01 · gcd 约化图 ||| 01 · gcd-reduced graph
02 · 三角返回 ||| 02 · Triangle return
03 · 共同频带 no-go ||| 03 · Common-band no-go
04 · 相干稠密族 ||| 04 · Coherent dense family
05 · 复目标根边界 ||| 05 · Complex-target root boundary
06 · 独立审计 ||| 06 · Independent audit
11 · 复现入口 ||| 11 · Reproduction
把带相位的 signed carrier coefficient 记为 \(c_s(x)\)，\(s\in\pm S\)。目标行的两个真实量为 ||| Denote the phased signed carrier coefficient by \(c_s(x)\), with \(s\in\pm S\). The two true quantities in the target row are
版本 v0.72J · 2026-08-27 ||| Version v0.72J · 2026-08-27
报告、双路证书、附图与累计回顾 ||| Report, two-route certificates, figure, and cumulative recap
本节没有证明 arbitrary-carrier physical inequality，没有 complete complex-root theorem，没有构造有限时奇性，也没有证明一般三维 Navier–Stokes 全局光滑性。Clay 千禧年问题仍未解决。 ||| This section proves no arbitrary-carrier physical inequality, no complete complex-root theorem, no finite-time singularity construction, and no global smoothness result for general three-dimensional Navier–Stokes. The Clay Millennium Problem remains unsolved.
不再使用 R0.72I 已排除的 \(B_AQ_*\) 分离。共同热时间 \(R^{-2}\)、aligned row 大小和 perturbative coupling window 联合给出 ||| Do not reuse the \(B_AQ_*\) separation excluded by R0.72I. The common heat time \(R^{-2}\), the aligned-row size, and the perturbative coupling window jointly give
但相同数据的 physical lift、能量成本和 critical-log action 也同步增长。诊断缩放给 ||| The physical lift, energy cost, and critical-log action of the same data also grow in tandem. The diagnostic scaling gives
当前结果没有闭合 mixed-parity complete-root ledger ||| The present result does not close the mixed-parity complete-root ledger
独立 edge-list/RK45 路线在 \(R=64\) 得到 \(\mathcal C_{\times,R}=69.2166385022\)、normalized true cubic \(1.0386272844\times10^{-6}\)。 ||| The independent edge-list/RK45 route gives, at \(R=64\), \(\mathcal C_{\times,R}=69.2166385022\) and normalized true cubic \(1.0386272844\times10^{-6}\).
对 carrier set \(S=\{r_1,\ldots,r_M\}\subset\mathbb N\)，令 \(g=\gcd S\)，并在目标连通分支 \(g\mathbb Z\) 上连边 \(n\leftrightarrow n\pm r_j\)。除以 \(g\) 后得到由 \(a_j=r_j/g\) 生成的连通 Cayley 图。 ||| For a carrier set \(S=\{r_1,\ldots,r_M\}\subset\mathbb N\), set \(g=\gcd S\). On the target connected component \(g\mathbb Z\), join \(n\leftrightarrow n\pm r_j\). Dividing by \(g\) gives the connected Cayley graph generated by \(a_j=r_j/g\).
对载波位于一个可比频带、系数和 launch 满足报告所列统一界的 mixed-parity family，真实 cubic payment 直接保留为 ||| For a mixed-parity family whose carriers lie in one comparable band and whose coefficients and launch satisfy the uniform bounds stated in the report, retain the true cubic payment directly as
非二分图出现以后， ||| Once a non-bipartite graph appears,
根账本 ||| Root ledger
更关键的负结果是：即使选择三角数达到二次规模的 coherent block，true cubic contribution 的归一化比也没有存活。下一步必须改变尺度结构或耦合区间，而不是继续堆积同频带三角关系。 ||| The more important negative result is that even a coherent block with quadratically many triangles does not yield a surviving normalized ratio for the true cubic contribution. The next step must change the scale structure or the coupling regime instead of continuing to accumulate same-band triangle relations.
共同频带 ||| Common band
关闭的是一条看似直接的 mixed-parity 反族路线 ||| A seemingly direct mixed-parity counterfamily route is closed
还要再问 cubic 是否真的存活 ||| The cubic must still be tested for genuine survival
累计回顾 PDF ||| Cumulative recap PDF
令 \(g=\gcd(r_1,\ldots,r_M)\)。目标连通分支的 Cayley 图二分，当且仅当每个约化载波 \(r_j/g\) 都是奇数。 ||| Let \(g=\gcd(r_1,\ldots,r_M)\). The Cayley graph on the target connected component is bipartite if and only if every reduced carrier \(r_j/g\) is odd.
奇闭路可能很长；cubic 只看长度三 ||| An odd closed walk may be long; the cubic sees only length three
取最直接的 mixed-parity 稠密集合 \(S_R=\{R,R+1,\ldots,3R-1\}\)。若 \(T_R\) 计数 \((s,t,u)\in(\pm S_R)^3\) 中满足 \(s+t+u=0\) 的有序有符号三元组，则 ||| Take the most direct mixed-parity dense set \(S_R=\{R,R+1,\ldots,3R-1\}\). If \(T_R\) counts the ordered signed triples \((s,t,u)\in(\pm S_R)^3\) satisfying \(s+t+u=0\), then
若全部 \(a_j\) 为奇数，整数 parity 就是一组二着色，每条 carrier edge 都换色。反之，连通 Cayley 图的二着色从零点唯一延伸，并给出到 \(\mathbb Z_2\) 的群同态；每个生成元必须映到 1，因此不允许偶生成元。 ||| If every \(a_j\) is odd, integer parity is a two-coloring and every carrier edge changes color. Conversely, a two-coloring of the connected Cayley graph extends uniquely from zero and gives a group homomorphism to \(\mathbb Z_2\); every generator must map to 1, so no even generator is allowed.
三角返回 ||| Triangle return
三角关系使 cubic 非零，却没有克服物理归一化 ||| Triangle relations make the cubic nonzero but do not overcome physical normalization
双路机器证书 ||| Two-route machine certificates
所以 \(\{2,6\}\) 虽然原载波全偶，除以 \(g=2\) 后是 \(\{1,3\}\)，仍属于 R0.72I 的二分修复。混合 parity 也必须先约化再判断。 ||| Thus, although the original carriers in \(\{2,6\}\) are all even, division by \(g=2\) gives \(\{1,3\}\), which still belongs to the bipartite repair of R0.72I. Mixed parity must likewise be judged only after reduction.
所以本节严格控制的是 aligned true-cubic interaction 与其物理尺度，不把它升级成 complete temporal self-zero theorem。要得到根账本，还需要复目标的二维零点机制、额外相位锁定，或不依赖 Rolle 的全新归约。 ||| Thus this section rigorously controls the aligned true-cubic interaction and its physical scale; it does not promote that result to a complete temporal self-zero theorem. A root ledger still requires a two-dimensional zero mechanism for the complex target, additional phase locking, or a new reduction independent of Rolle's theorem.
图分类 ||| Graph classification
图分类与 triangle-return 判据是精确离散结论。common-band no-go 和 coherent-family scaling 只覆盖报告中声明的 exact triangular 2.5D aligned perturbative families。 ||| The graph classification and triangle-return criterion are exact discrete conclusions. The common-band no-go and coherent-family scaling cover only the exact triangular 2.5D aligned perturbative families stated in the report.
图论、cubic 返回、物理尺度和根账本不能混成一句 ||| Graph theory, cubic return, physical scale, and the root ledger cannot be collapsed into one statement
图论障碍、三角返回与物理归一化必须分开；当前 common-band 构造没有产生存活的 normalized cubic ledger。 ||| The graph obstruction, triangle return, and physical normalization must remain separate; the present common-band construction produces no surviving normalized cubic ledger.
五个共同规模上的最大相对差为：\(Q_*\) 的 \(1.53322\times10^{-6}\)、\(\mathcal C_{\times,R}\) 的 \(2.94064\times10^{-12}\)、normalized true cubic 的 \(7.28034\times10^{-9}\)。有限审计只核对离散代数、实现与有限尺度趋势；渐近 no-go 由报告中的解析估计承担。 ||| Across the five common scales, the maximum relative differences are: for \(Q_*\), \(1.53322\times10^{-6}\); for \(\mathcal C_{\times,R}\), \(2.94064\times10^{-12}\); and for the normalized true cubic, \(7.28034\times10^{-9}\). The finite audit checks only the discrete algebra, implementation, and finite-scale trend; the analytic estimates in the report establish the asymptotic no-go.
下一关只保留三个可能改变结论的接口：让 carrier triangles 跨多个热时间尺度；离开当前 perturbative coupling window 并重新支付完整能量与 action；或先建立 complex target 的 complete-root ledger。 ||| The next gate retains only three interfaces that could change the conclusion: let carrier triangles span several heat time scales; leave the present perturbative coupling window and repay the full energy and action; or first establish a complete-root ledger for the complex target.
下载 PNG ||| Download PNG
相干族 ||| Coherent family
研究笔记 R0.72J · CAYLEY GRAPH · TRIANGLE RETURN · TRUE CUBIC ||| Research note R0.72J · CAYLEY GRAPH · TRIANGLE RETURN · TRUE CUBIC
研究笔记 R0.72J：gcd 约化后的载波 Cayley 图二分性具有精确分类；真正的 cubic 返回要求三角关系。common-band 与 coherent mixed-parity 族的真实 cubic 虽非零，物理归一化后仍衰减。 ||| Research note R0.72J: bipartiteness of the carrier Cayley graph after gcd reduction has an exact classification; a true cubic return requires a triangle relation. Although the true cubic is nonzero in the common-band and coherent mixed-parity families, it still decays after physical normalization.
验收标准仍是直接控制真实 \(|\delta|\int|hP_0V^2F|\) 或真实根斜率账本，并在完整物理归一化后给出闭合上界或存活反族。 ||| The acceptance criterion remains direct control of the true \(|\delta|\int|hP_0V^2F|\) or the true root-slope ledger, followed by either a closed upper bound or a surviving counterfamily after complete physical normalization.
一般 Navier–Stokes 问题仍然开放 ||| The general Navier–Stokes problem remains open
因此“很多三角关系”是 raw interaction 的充分来源，却不是物理归一化反例的充分来源。 ||| Thus, “many triangle relations” provide ample raw interaction but do not suffice for a physically normalized counterexample.
在声明的 common-band perturbative scaling 下，true cubic contribution 的归一化比至多为 \(CR^{-4/9}(1+\log R)^{-2/3}\)，所以一致趋零。 ||| Under the stated common-band perturbative scaling, the normalized ratio of the true cubic contribution is at most \(CR^{-4/9}(1+\log R)^{-2/3}\), and therefore tends uniformly to zero.
这是一条 common-band aligned perturbative no-go，不是 arbitrary-carrier 上界。它说明只在同一频带增加三角数，仍不能得到存活的 normalized cubic counterfamily。 ||| This is a common-band aligned perturbative no-go, not an arbitrary-carrier upper bound. It shows that increasing the triangle count within a single band still cannot produce a surviving normalized cubic counterfamily.
这是载波 Cayley 图中的三角关系。它严格强于 non-bipartite。例如约化集合 \(\{1,4\}\) 的图非二分，但最短奇闭路长度为五，没有三载波关系，所以 aligned launch 不产生 leading cubic return。 ||| This is a triangle relation in the carrier Cayley graph. It is strictly stronger than non-bipartiteness. For example, the graph for the reduced set \(\{1,4\}\) is non-bipartite, but its shortest odd closed walk has length five and it has no three-carrier relation, so an aligned launch produces no leading cubic return.
这一步把 R0.72I 的 parity observation 提升成精确的 gcd-reduced graph theorem，并识别出真正进入 cubic row 的长度三 additive relation。它阻止两种误判：原载波有偶数就一定失去修复；图非二分就一定有 leading cubic。 ||| This step upgrades the parity observation of R0.72I to an exact gcd-reduced graph theorem and identifies the length-three additive relation that actually enters the cubic row. It prevents two mistaken inferences: an even original carrier necessarily destroys the repair; a non-bipartite graph necessarily has a leading cubic.
真正的不变量是约化载波，不是原整数的表面奇偶 ||| The true invariant is the reduced carrier, not the superficial parity of the original integer
正关系 \(a+b=c\) 的有序对共有 \(R(R+1)/2\) 个，再乘负项位置和整体符号的六种选择。相位对齐后，真实 raw cubic 满足 \(\mathcal C_{\times,R}\asymp R^2\)，不是被 parity 消掉的零量。 ||| For the positive relation \(a+b=c\), there are \(R(R+1)/2\) ordered pairs, followed by six choices for the position of the negative term and the overall sign. After phase alignment, the true raw cubic satisfies \(\mathcal C_{\times,R}\asymp R^2\); it is not a zero quantity removed by parity.
正式附图包 ||| Formal figure package
正式附图分开显示图分类、三角计数与归一化衰减 ||| The formal figure separately shows the graph classification, triangle count, and normalized decay
状态 · R0.72J 负结果完成 ||| Status · R0.72J negative result complete
组合计数、图分类和有限动力学由两条实现交叉核对 ||| Combinatorial counts, graph classification, and finite dynamics are cross-checked by two implementations
aligned launch 支持在第一球 \(R_1(0)=\pm S\)。因此 \(b\) 在零时刻读到 launch，当且仅当 ||| The aligned launch is supported on the first sphere \(R_1(0)=\pm S\). Thus \(b\) reads the launch at time zero if and only if
mixed-parity aligned target 一般是复值。前几节依赖实标量 Rolle 归约的 complete-root ledger 没有自动延伸到这里。 ||| A mixed-parity aligned target is generally complex-valued. The complete-root ledger in the preceding sections, which relies on a real-scalar Rolle reduction, does not extend here automatically.
non-bipartite 只保证某条奇闭路；aligned launch 的二步返回要求 \(R_1(0)\cap R_2(0)\ne\varnothing\)，等价于存在有符号三载波关系。 ||| Non-bipartiteness guarantees only an odd closed walk; the two-step return of an aligned launch requires \(R_1(0)\cap R_2(0)\ne\varnothing\), equivalently a signed three-carrier relation.
R0.72G–I 的 Rolle–BV 归约使用兼容 gauge 把目标坐标和目标 row 变成实标量。mixed-parity coherent family 的 phase alignment 一般使目标轨道落在 \(\mathbb C\)，而复曲线的零点没有实函数符号交替。 ||| The Rolle–BV reductions in R0.72G–I use a compatible gauge to make the target coordinate and target row real scalars. Phase alignment in a mixed-parity coherent family generally places the target trajectory in \(\mathbb C\), while zeros of a complex curve have no real-function sign alternation.
R0.72I 的奇偶修复不是“原整数全奇”这一种写法，而是 gcd 约化后的 Cayley 图二分性。离开二分情形只说明存在某条奇闭路；真实 \(P_0V^2F\) 在 aligned launch 上立即返回，还需要三步有符号关系。共同频带内即使安排大量三角关系，raw cubic 可以增长，true cubic contribution 的归一化比仍然衰减。这个方向需要进入多尺度或强耦合，不能把 non-bipartite 直接写成反例。 ||| The parity repair in R0.72I is not merely the statement that the original integers are all odd; it is bipartiteness of the Cayley graph after gcd reduction. Leaving the bipartite case shows only that an odd closed walk exists; an immediate return of the true \(P_0V^2F\) under an aligned launch additionally requires a three-step signed relation. Even when many triangle relations are arranged within a common band, the raw cubic can grow while the normalized ratio of the true cubic contribution still decays. This direction must enter multiple scales or strong coupling; non-bipartiteness cannot be presented directly as a counterexample.
R0.72J｜非二分不等于 cubic 反例 ||| R0.72J | Non-bipartite does not mean a cubic counterexample
R0.72K：多尺度、强耦合，或复目标根机制 ||| R0.72K: multiple scales, strong coupling, or a complex-target root mechanism
raw cubic 达到二次规模，true cubic contribution 的归一化比仍衰减 ||| The raw cubic reaches quadratic order, while the normalized ratio of the true cubic contribution still decays
01 · 二十六个研究阶段 ||| 01 · Twenty-six research phases
02 · 100 节完整索引 ||| 02 · Complete 100-note index
保留 R0.72I 历史回顾 ||| Retain the R0.72I historical recap
本节把 parity repair 的适用范围精确扩大到 gcd 约化后全奇的 carrier sets，并证明 non-bipartite 与 leading cubic 之间还隔着 triangle relation。这个区分是可复用的结构结果。 ||| This section precisely extends the parity repair to carrier sets that are all odd after gcd reduction and proves that a triangle relation still separates non-bipartiteness from a leading cubic. This distinction is a reusable structural result.
查看 R0.72J 双路证书 ||| View the R0.72J two-route certificates
打开最新节点 R0.72J ||| Open the latest node, R0.72J
二十六个阶段、100 个节点：从约化递推和时间迹账本，到 unweighted payment 失效，再到 gcd-reduced graph classification 与 common-band cubic no-go。 ||| Twenty-six phases and 100 nodes: from reduced recurrences and the temporal-trace ledger, through failure of the unweighted payment, to gcd-reduced graph classification and the common-band cubic no-go.
共同频带 perturbative family 的 true cubic contribution 归一化比仍至多为 \(CR^{-4/9}(1+\log R)^{-2/3}\)。相干集合 \(S_R=\{R,\ldots,3R-1\}\) 有 \(T_R=3R(R+1)\) 个有序有符号三角，raw \(\mathcal C_{\times,R}\asymp R^2\)，其归一化比却按 \(R^{-2/3}\) 衰减。复目标的 complete-root Rolle 账本没有在本节闭合。 ||| The normalized ratio of the true cubic contribution in a common-band perturbative family is still at most \(CR^{-4/9}(1+\log R)^{-2/3}\). The coherent set \(S_R=\{R,\ldots,3R-1\}\) has \(T_R=3R(R+1)\) ordered signed triangles and raw \(\mathcal C_{\times,R}\asymp R^2\), yet its normalized ratio decays like \(R^{-2/3}\). This section does not close the complete-root Rolle ledger for a complex target.
回顾截止节点：R0.72J ||| Recap cutoff node: R0.72J
回顾截止时公开笔记：160 ||| Public notes at the recap cutoff: 160
截至 R0.72J，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 100 个节点或 62 个公开版本解释成对千禧年问题完成了某个比例。 ||| Through R0.72J, there is no new unconditional continuation criterion, no reduction of the set of all potentially singular solutions, and no proof of finite-time breakdown. The 100 nodes or 62 public releases cannot be interpreted as completing any percentage of the Millennium Problem.
累计回顾 · R0.61–R0.72J · 2026-08-27 ||| Cumulative recap · R0.61–R0.72J · 2026-08-27
令 \(g=\gcd(r_1,\ldots,r_M)\)。目标连通分支的 carrier Cayley 图二分，当且仅当所有约化载波 \(r_j/g\) 都是奇数。non-bipartite 只保证某条奇闭路；aligned launch 的 leading cubic 还要求第一球与第二球相交，即存在 \(s+t+u=0\) 的有符号三载波关系。 ||| Let \(g=\gcd(r_1,\ldots,r_M)\). The carrier Cayley graph on the target connected component is bipartite if and only if every reduced carrier \(r_j/g\) is odd. Non-bipartiteness guarantees only an odd closed walk; the leading cubic of an aligned launch additionally requires the first and second spheres to intersect, equivalently a signed three-carrier relation \(s+t+u=0\).
若目标保持复值，则 complete-root 结论必须先建立二维零点或相位锁定机制；不能直接复用实标量 Rolle 账本。 ||| If the target remains complex-valued, a complete-root conclusion first requires a two-dimensional zero or phase-locking mechanism; the real-scalar Rolle ledger cannot be reused directly.
收录节点：100 ||| Included nodes: 100
图论分类已闭合，同频带 mixed-parity 反族路线被排除 ||| The graph-theoretic classification is closed, and the same-band mixed-parity counterfamily route is excluded
下一步不再扩大同频带三角数。优先检查跨热时间尺度的 carrier triangles，或在完整能量与 critical-log action 重新结算后离开 perturbative coupling window。 ||| The next step will not enlarge the number of same-band triangles. Priority goes to carrier triangles spanning heat time scales, or to leaving the perturbative coupling window after recomputing the full energy and critical-log action.
这个发散来自上界，不是真实根账本的下界。保留 joint heat exposure，或直接利用 \(V\) 翻转奇偶格点，可得 \(G_{\rm all}^{\rm ex}\asymp M^2\)。R0.72I complete-ledger 的物理归一化比值在整个 \(0<g\le\gamma_0M^{3/2}\) 窗口内至多为 \(CM^{-4/9}(\log M)^{-2/3}\)，所以同一族不是 critical-log 候选的反例。 ||| This divergence comes from an upper bound, not a lower bound for the true root ledger. Retaining joint heat exposure, or directly using the fact that \(V\) flips lattice parity, gives \(G_{\rm all}^{\rm ex}\asymp M^2\). The physically normalized R0.72I complete-ledger ratio is, throughout the entire \(0<g\le\gamma_0M^{3/2}\) window, at most \(CM^{-4/9}(\log M)^{-2/3}\), so the same family is not a counterexample to the critical-log candidate.
这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72J 的 100 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。这里的节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。 ||| This page follows the R0.00–R0.60 phase recap and organizes the research nodes from R0.61 through R0.72J, 100 in total. I record chronologically what each segment actually proves, which proposal a concrete counterexample or scaling analysis excludes, and which conditions have not been derived from the Navier–Stokes equations. Node status here describes the evidence type; it does not misstate a release archive as a solved phase objective.
common-band 与 coherent dense block 都没有给出存活的 normalized cubic counterfamily。障碍已经转到多尺度、强耦合或 complex target complete-root mechanism。 ||| Neither the common-band family nor the coherent dense block gives a surviving normalized cubic counterfamily. The obstruction has shifted to multiple scales, strong coupling, or a complex-target complete-root mechanism.
R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 100 个节点沿着这个缺口推进；R0.70A–R0.72J 的 62 个版本已经公开；其中 38 个满足当前 formal-figure 完整封存合同，但其中仍包含条件定理、反例、有限诊断和开放缺口。 ||| The material from R0.00–R0.60 remains in the preceding phase recap. The conclusion at R0.60 was that the complete Fourier–Leray structure and higher-order computation could continue, but the critical quantity for general three-dimensional solutions was still uncontrolled. The next 100 nodes advance along this gap; the releases from R0.70A–R0.72J, 62 in all, are public; 38 satisfy the current formal-figure complete-archive contract, but those releases still include conditional theorems, counterexamples, finite diagnostics, and open gaps.
R0.60 之后的路线分成二十六个阶段 ||| The route after R0.60 is divided into twenty-six phases
R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72J 的 100 个研究节点；最新一节完成 gcd 约化 Cayley 图分类，并排除 common-band mixed-parity cubic 反族路线。 ||| Research recap after R0.60: complete coverage from R0.61 through R0.72J, comprising 100 research nodes; the latest section completes the gcd-reduced Cayley graph classification and excludes the common-band mixed-parity cubic counterfamily route.
R0.61–R0.72J 的 100 节公开笔记 ||| Public notes from R0.61–R0.72J: 100
R0.61–R0.72J 回顾 · 2026-08-27 ||| R0.61–R0.72J recap · 2026-08-27
R0.61–R0.72J 研究节点 ||| R0.61–R0.72J research nodes
R0.61–R0.72J｜R0.60 之后的研究回顾 ||| R0.61–R0.72J | Research recap after R0.60
R0.70A–R0.72J 的 62 节 HTML/PDF 与研究源稿列入公开路线。按当前 formal-figure 合同，38 节完整封存；24 节较早版本仍列入可审计的旧档回补清单。 ||| The HTML/PDF releases and research sources from R0.70A–R0.72J, 62 in all, are included in the public route. Under the current formal-figure contract, 38 are fully archived; 24 earlier figure archives remain on the auditable backfill list.
R0.70A–R0.72J 已公开版本 ||| Published R0.70A–R0.72J releases
R0.72J · 约化 Cayley 图与真实 cubic no-go ||| R0.72J · Reduced Cayley graph and true-cubic no-go
R0.72J 的 gcd-reduced carrier theorem：目标 Cayley 图二分当且仅当所有约化载波为奇数；non-bipartite 不自动产生 cubic，leading return 需要三载波有符号关系。common-band aligned perturbative families 的 true cubic contribution 归一化比统一趋零；稠密相干块虽有 \(\mathcal C_{\times,R}\asymp R^2\)，仍不是 normalized counterfamily。complete complex-root ledger 保持开放。 ||| The gcd-reduced carrier theorem of R0.72J states that the target Cayley graph is bipartite if and only if every reduced carrier is odd; non-bipartiteness does not automatically produce a cubic, and a leading return requires a signed three-carrier relation. The normalized ratio of the true cubic contribution tends uniformly to zero in common-band aligned perturbative families; despite \(\mathcal C_{\times,R}\asymp R^2\), the dense coherent block is still not a normalized counterfamily. The complete complex-root ledger remains open.
R0.72J 的渐近 no-go 限于 exact triangular 2.5D common-band aligned perturbative families。它没有证明 arbitrary-carrier physical inequality，也没有证明一般三维 Navier–Stokes 的全局光滑性或有限时破裂；Clay 正式问题仍然开放。 ||| The asymptotic no-go of R0.72J is restricted to exact triangular 2.5D common-band aligned perturbative families. It proves neither an arbitrary-carrier physical inequality nor global smoothness or finite-time breakdown for general three-dimensional Navier–Stokes; the official Clay problem remains open.
R0.72J 附图 ||| R0.72J figure
R0.72J 证书 ||| R0.72J certificates
R0.72K 进入多尺度或强耦合，并单列 complex-root gate ||| R0.72K enters multiple scales or strong coupling, with a separate complex-root gate
保留 joint heat exposure，或直接利用 \(V\) 翻转奇偶格点，可得 \(G_{\rm all}^{\rm ex}\asymp M^2\)。R0.72I complete-ledger 的物理归一化比值在 \(0<g\le\gamma_0M^{3/2}\) 内满足 \(CM^{-4/9}(\log M)^{-2/3}\to0\)。因此这个族不是候选 physical inequality 的反例。 ||| Retaining joint heat exposure, or directly using the fact that \(V\) flips lattice parity, gives \(G_{\rm all}^{\rm ex}\asymp M^2\). The physically normalized R0.72I complete-ledger ratio, for \(0<g\le\gamma_0M^{3/2}\), satisfies \(CM^{-4/9}(\log M)^{-2/3}\to0\). Hence this family is not a counterexample to the candidate physical inequality.
从 parity repair 走到 gcd-reduced graph classification 与 cubic no-go ||| From parity repair to gcd-reduced graph classification and the cubic no-go
非二分图、三角返回和物理反族是三道不同的门 ||| A non-bipartite graph, triangle return, and a physical counterfamily are three distinct gates
环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \(M^{-2}\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → phase-uniform \(M^{-8/3}\) sharp algebraic prefactor → shifted Rudin–Shapiro heat pulse → positive-time simple root → full-charge normalized order-one saturation → fixed-carrier shell isolation → negative-Sobolev action decay → candidate D^{1/3}Λ₁ payment failure → critical-log repair → selected-family frontier → complete-root Rolle–BV closure → sharp critical-log saturation → carrier-free mixed-row payment → action-only no-go → termwise physical-absorption no-go → parity repair → gcd-reduced Cayley classification → triangle-return criterion → common-band cubic no-go ||| Annulus exclusion → source–core ledger → covariance spectral stratification → all-frequency conditional bridge → response-slope chord gain → common-response order-one channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \(M^{-2}\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → phase-uniform \(M^{-8/3}\) sharp algebraic prefactor → shifted Rudin–Shapiro heat pulse → positive-time simple root → full-charge normalized order-one saturation → fixed-carrier shell isolation → negative-Sobolev action decay → candidate D^{1/3}Λ₁ payment failure → critical-log repair → selected-family frontier → complete-root Rolle–BV closure → sharp critical-log saturation → carrier-free mixed-row payment → action-only no-go → termwise physical-absorption no-go → parity repair → gcd-reduced Cayley classification → triangle-return criterion → common-band cubic no-go
检查 multi-scale triangles、strong-coupling physical ledger，或 complex target complete-root mechanism。 ||| Test multi-scale triangles, a strong-coupling physical ledger, or a complex-target complete-root mechanism.
检查跨多个热时间尺度的 carrier triangles，或在完整能量与 critical-log action 下进入强耦合；若目标保持复值，先建立不依赖实 Rolle 符号交替的 complete-root mechanism。 ||| Test carrier triangles across several heat time scales, or enter strong coupling under the full energy and critical-log action; if the target remains complex-valued, first establish a complete-root mechanism independent of real Rolle sign alternation.
静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71U–Z 依次处理 second-time jet、complete first row、fixed-small-coupling endpoint、selected roots 与 complete roots。R0.72A–C 建立 Bessel lower family、target-row participation 与 physical-phase sharp scales；R0.72D 再实现 positive-time root 与 full-charge order-one saturation。R0.72E 固定 \(q_0>R_*\)，用 Feynman–Kac、驻相和定量 Hörmander density 控制完整 \(H^{-1}\) action；exact one-carrier family 最终使 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。R0.72F 随后证明 selected roots 强制 \(1/3\) 下端点，而 Leray energy 只支付到 \(1/2\)；最小边界修正是 \(s^{-1/3}[1+\log(1/s)]\)。R0.72G 固定这一候选，用实相位 gauge、目标行恒等式与 Rolle–BV 归约证明完整根质量 \(G_{\rm all}\asymp\log\delta\)，并在原始幅度序列上得到 complete-root sharp saturation。R0.72H 转入有限共轭配对多载波 mixed row，证明载波数无关的 moment-resolved 上界；全奇数 Rudin–Shapiro 族排除 action-only payment，并使所需 \(M\)-幂次达到同阶。R0.72I 逐项换回物理量，证明分离的 \(B_AQ_*\) 项不能统一吸收；joint exposure 与 odd-carrier parity 又证明真实 complete ledger 统一衰减。R0.72J 把 parity 修复提升为 gcd-reduced Cayley 图二分定理，区分 odd cycle 与 triangle return，并排除 common-band coherent cubic 反族。 ||| After the static annular family is rigorously excluded, the main line turns to covariance-rank stratification and the all-frequency projection bridge. R0.71U–Z successively treats the second-time jet, the complete first row, the fixed-small-coupling endpoint, selected roots, and complete roots. R0.72A–C establishes the Bessel lower family, target-row participation, and sharp physical-phase scales; R0.72D then realizes a positive-time root and full-charge order-one saturation. R0.72E fixes \(q_0>R_*\) and controls the complete \(H^{-1}\) action using Feynman–Kac, stationary phase, and a quantitative Hörmander density; the exact one-carrier family ultimately makes the complete-root ledger relative to the candidate \(D^{1/3}\Lambda_1\) payment diverge like \(R^{4/3}\). R0.72F then proves that selected roots force the lower endpoint \(1/3\), while Leray energy pays only up to \(1/2\); the minimal boundary repair is \(s^{-1/3}[1+\log(1/s)]\). R0.72G fixes this candidate and uses a real phase gauge, target-row identities, and the Rolle–BV reduction to prove that the complete root mass satisfies \(G_{\rm all}\asymp\log\delta\), obtaining sharp complete-root saturation for the critical log on the original amplitude sequence. R0.72H moves to the mixed row in a finite conjugate-paired multi-carrier system and proves a carrier-count-independent moment-resolved upper bound; an all-odd Rudin–Shapiro family excludes the action-only payment and attains the required \(M\)-power. R0.72I converts each term back to physical quantities, proves that the separated \(B_AQ_*\) term cannot be absorbed uniformly, and then uses joint exposure and odd-carrier parity to prove uniform decay of the true complete ledger. R0.72J upgrades the parity repair to a gcd-reduced Cayley-graph bipartiteness theorem, distinguishes an odd cycle from a triangle return, and excludes the common-band coherent cubic counterfamily.
累计回顾 R0.61–R0.72J · 2026-08-27 ||| Cumulative recap R0.61–R0.72J · 2026-08-27
累计回顾现在分为二十六个问题阶段，完整覆盖 R0.61–R0.72J。R0.72E 排除 unweighted payment，R0.72F 选出 critical-log 修正，R0.72G 封闭 one-carrier complete roots，R0.72H 封闭 finite multi-carrier mixed row，R0.72I 分离失败的正项吸收与真实 parity ledger，R0.72J 再完成 gcd-reduced graph classification 与 common-band cubic no-go。R0.70A–R0.72J 共 62 个版本已公开；38 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。 ||| The cumulative recap now has twenty-six problem phases and completely covers R0.61–R0.72J. R0.72E excludes the unweighted payment, R0.72F selects the critical-log repair, R0.72G closes the one-carrier complete roots, R0.72H closes the finite multi-carrier mixed row, R0.72I separates the failed positive-term absorption from the true parity ledger, and R0.72J completes the gcd-reduced graph classification and common-band cubic no-go. Across R0.70A–R0.72J, 62 releases are public; 38 satisfy the current formal-figure complete-archive contract, while 24 older figure archives remain on the backfill list.
令 \(g=\gcd(r_1,\ldots,r_M)\)。carrier Cayley 图二分当且仅当所有 \(r_j/g\) 为奇数。离开二分情形只保证奇闭路；aligned launch 的 leading \(P_0V^2F\) 还需要 \(s+t+u=0\) 的三载波关系。 ||| Let \(g=\gcd(r_1,\ldots,r_M)\). The carrier Cayley graph is bipartite if and only if every \(r_j/g\) is odd. Leaving the bipartite case guarantees only an odd closed walk; the leading \(P_0V^2F\) of an aligned launch additionally requires a three-carrier relation \(s+t+u=0\).
上次综述 v1.22 · 2026-08-27 ||| Previous review v1.22 · 2026-08-27
同频带增加 carrier triangles 不能产生存活的 normalized cubic counterfamily；下一障碍是多尺度、强耦合或 complex-root ledger。 ||| Adding carrier triangles within one band cannot produce a surviving normalized cubic counterfamily; the next obstruction is multiple scales, strong coupling, or the complex-root ledger.
我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.72J 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。 ||| I also prepared a systematic review that places the classical theory, five literature strands, the candidate-elimination tree, progress from 2019—2026, and this site's R0.69P–R0.72J route on one diagram. The historical nodes R0.61–R0.69O remain in the cumulative recap.
下一步 R0.72K： ||| Next R0.72K:
相干集合 \(S_R=\{R,\ldots,3R-1\}\) 有 \(3R(R+1)\) 个有序有符号三角，raw \(\mathcal C_{\times,R}\asymp R^2\)；true cubic contribution 的归一化比仍按 \(R^{-2/3}\) 衰减。更一般的 common-band perturbative 上界为 \(CR^{-4/9}(1+\log R)^{-2/3}\)。 ||| The coherent set \(S_R=\{R,\ldots,3R-1\}\) has \(3R(R+1)\) ordered signed triangles and raw \(\mathcal C_{\times,R}\asymp R^2\); the normalized ratio of the true cubic contribution still decays like \(R^{-2/3}\). The more general common-band perturbative upper bound is \(CR^{-4/9}(1+\log R)^{-2/3}\).
研究笔记 R0.72J · 2026-08-27 ||| Research note R0.72J · 2026-08-27
阅读 R0.72J 研究笔记 → ||| Read the R0.72J research note →
展开 70 篇公开笔记 ||| Expand 70 public notes
综述 v1.23 · 2026-08-27 ||| Review v1.23 · 2026-08-27
gcd 约化 Cayley 图的二分性已精确分类；non-bipartite 不自动产生 cubic，common-band coherent family 的 true cubic contribution 归一化比仍衰减。 ||| Bipartiteness of the gcd-reduced Cayley graph is classified exactly; non-bipartiteness does not automatically produce a cubic, and the normalized ratio of the true cubic contribution in the common-band coherent family still decays.
mixed-parity 目标一般是复值，实 Rolle complete-root 账本没有在本节闭合。一般三维正则性仍然开放。 ||| A mixed-parity target is generally complex-valued, and this section does not close the real-Rolle complete-root ledger. General three-dimensional regularity remains open.
R0.60 recap 之后的累计回顾收录 100 个节点；全站现有 160 篇公开研究笔记 ||| The cumulative recap after R0.60 contains 100 nodes; the site now has 160 public research notes
R0.70A–R0.72J：62 节已公开，38 节完整封存 ||| R0.70A–R0.72J: 62 published, 38 fully archived
R0.72J 已完成 gcd 约化 Cayley 图分类，并证明 non-bipartite 不等于 leading cubic；common-band coherent mixed-parity 族虽有 raw cubic 增长，true cubic contribution 的归一化比仍衰减。 ||| R0.72J completes the gcd-reduced Cayley graph classification and proves that non-bipartite does not mean a leading cubic; although the raw cubic grows in the common-band coherent mixed-parity family, the normalized ratio of the true cubic contribution still decays.
R0.72J 已完成： ||| R0.72J complete:
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
  throw new Error("Duplicate Chinese keys in R0.72J translation rows");
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
  "notes/r0-72j.html",
  "recap-r0-61-r0-72j.html",
  "research-review.html",
];
for (const relative of expectedFiles) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.23')) {
    throw new Error(relative + ": expected i18n cache version v1.23");
  }
}

const source = await collectSiteStrings(publicDirectory);
const translations = JSON.parse(await readFile(translationPath, "utf8"));
const batchId = /^r072j\d+$/;
const retained = translations.filter((entry) => !batchId.test(entry.id));
const retainedByChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (retainedByChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.72J batch");
}

const missing = source.filter((entry) => !retainedByChinese.has(entry.zh));
const missingKeys = new Set(missing.map((entry) => entry.zh));
const uncovered = missing.filter((entry) => !additions.has(entry.zh));
const stale = [...additions.keys()].filter((zh) => !missingKeys.has(zh));
if (uncovered.length || stale.length || additions.size !== missing.length) {
  throw new Error(
    `R0.72J translation batch does not equal active missing set (${missing.length}):\n` +
      "UNCOVERED:\n" +
      uncovered.map((entry) => entry.zh).join("\n---\n") +
      "\nSTALE:\n" +
      stale.join("\n---\n"),
  );
}
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))];
if (!sameTokens(missingFiles, expectedFiles)) {
  throw new Error("Unexpected R0.72J source files: " + JSON.stringify(missingFiles));
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
    id: "r072j" + String(index + 1).padStart(3, "0"),
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
