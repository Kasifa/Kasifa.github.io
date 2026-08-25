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
打开 78 节完整索引 ||| Open the complete 78-section index
给出 filtered vortex force 与 filtered enstrophy； ||| gives the filtered vortex force and filtered enstrophy;
给出单位涡量方向的切投影方程； ||| gives the tangent-projection equation for the unit vorticity direction;
给出严谨 local-enstrophy cutoff ledger； ||| give rigorous local-enstrophy cutoff ledgers;
环带 Lamb 交换子具有精确二次速度增量表示；fixed-cell projective pairing 保留四行临界消费者。热包只排除这些绝对预算的普适能量嵌入，不是 NSE 解反例。 ||| The annular Lamb commutator has an exact quadratic velocity-increment representation, and the fixed-cell projective pairing retains four critical consumers. The heat packets rule out only a universal energy embedding for these absolute budgets; they are not counterexamples among NSE solutions.
开放接口 · R0.71O ||| Open interface · R0.71O
累计回顾与 78 节索引 ||| Cumulative recap and 78-section index
是已查到最邻近的 filtered-vorticity/local-cutoff 账本。它们都没有本站固定单元的 cutoff–curl denominator 与 \(B_Q/\sqrt{Yd_Q}\) 完整时间演化。限定检索未找到同时保留 \(B_{Q,t},d_{Q,t},Y_t\) 的直接来源；这是 bounded negative finding，不是原创性、优先权或不存在性结论。 ||| is the nearest filtered-vorticity/local-cutoff ledger found in the search. None of these sources has this site's fixed-cell cutoff–curl denominator and complete evolution of \(B_Q/\sqrt{Yd_Q}\). The bounded search found no direct source retaining \(B_{Q,t},d_{Q,t},Y_t\) simultaneously; this is a bounded negative finding, not a claim of originality, priority, or nonexistence.
完整 \(B_{Q,t},d_{Q,t},Y_t\) 标量先写成 square–residual form；代入 \(B_Q=e_{Q,t}+\nu D_Q^\chi\) 后，acceleration 中的同一 pairing 产生 \(-\mathcal P_Q^\square\)，恰好消去表面的正平方。两个 \(z_Q>0\) 的 smooth NSE initial jets 给出 \(\mathcal J_Q\) 双号，但不是时间区间符号定理。 ||| The complete \(B_{Q,t},d_{Q,t},Y_t\) scalar first takes a square–residual form. After substituting \(B_Q=e_{Q,t}+\nu D_Q^\chi\), the same pairing in the acceleration produces \(-\mathcal P_Q^\square\), exactly canceling the apparent positive square. Two smooth NSE initial jets with \(z_Q>0\) give opposite signs of \(\mathcal J_Q\), but not a sign theorem on a time interval.
文献综述 v0.99 · 2026-08-26 ||| Literature review v0.99 · 2026-08-26
我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.71N 只列为研究笔记。我不把计算或笔记外推成正则性定理。 ||| I list published theorems as known results, mark 2026 preprints separately, and classify this site's R0.69P–R0.71N work only as research notes. I do not extrapolate calculations or notes into regularity theorems.
下一节仍留在 fixed cells，比较 hard components 与 \(\sqrt{d_Q+\varepsilon}\)，检查 \(\varepsilon\downarrow0\) 的 source measures 和 denominator-zero 一侧 faces；暂不进入 refresh 或 moving cutoffs。 ||| The next section remains on fixed cells, compares the hard components with \(\sqrt{d_Q+\varepsilon}\), and checks the source measures and one-sided denominator-zero faces as \(\varepsilon\downarrow0\); refresh and moving cutoffs remain outside the scope.
正平方被 local-enstrophy acceleration 精确消去 ||| The positive square is canceled exactly by the local-enstrophy acceleration
中。R0.69P–R0.71N 从有符号物理环带经过 projected-Lamb 热体积、matched-cell heat gap、viscous fusion 与 exact increment–projective bridge，走到完整 fixed-cell 标量的 signed second-jet boundary。R0.71N 证明 projective completion 中表面的正平方被 local filtered-enstrophy acceleration 精确消去；留下的临界二阶余项没有固定符号。保留下来的结果都不是全局正则性结论。 ||| . From R0.69P through R0.71N, the route moves from signed physical annuli through projected-Lamb heat volume, the matched-cell heat gap, viscous fusion, and the exact increment–projective bridge to the signed second-jet boundary of the complete fixed-cell scalar. R0.71N establishes that the apparent positive square in the projective completion is canceled exactly by the local filtered-enstrophy acceleration; the remaining critical second-order residual has no fixed sign. None of the retained results is a global-regularity conclusion.
R0.71N 的一手文献边界 ||| Primary-source boundary for R0.71N
查看主源文献台账 ||| View the primary-source literature ledger
R0.71N 关闭了什么，R0.71O 只检查什么 ||| What R0.71N closes, and what R0.71O alone will test
R0.71N 没有把完成平方后的非负项当作自动耗散。完整时间导数与局部 filtered enstrophy 代回后，同一平方在 acceleration 中以负号出现并精确消去；最终只剩临界 signed second jet。这关闭的是一个 fixed-cell 代数候选，不是一般 signed NSE no-go。R0.71O 只检查 hard/soft denominator 极限与一侧 face measure，并继续用下面六条筛选。 ||| R0.71N does not treat the nonnegative term from completing the square as automatic dissipation. After substituting the complete time derivative and local filtered enstrophy, the same square reappears with a negative sign in the acceleration and cancels exactly; only the critical signed second jet remains. This closes one fixed-cell algebraic candidate, not a general signed NSE no-go result. R0.71O tests only the hard/soft denominator limit and one-sided face measure, using the six filters below.
soft denominator 与 \(d_Q=0\) 一侧 faces ||| Soft denominator and one-sided faces at \(d_Q=0\)
\(\langle N_j,E_Q\rangle/\sqrt Y\) 中有 \(+\lambda_jz_Q\)；上式最后一项贡献 \(-\lambda_jz_Q\)。两个名义率完全消去，既没有遗漏，也没有把阻尼重复计费。 ||| The term \(\langle N_j,E_Q\rangle/\sqrt Y\) contains \(+\lambda_jz_Q\), while the final term above contributes \(-\lambda_jz_Q\). The two nominal rates cancel exactly, with neither omission nor double charging of damping.
\(+\lambda_j z_Q\) 与 projective radial row 中的负项精确相消 ||| \(+\lambda_j z_Q\) cancels exactly with the negative term in the projective radial row
\(B_Q\) 是局部 enstrophy 导数加一个 signed diffusion form ||| \(B_Q\) is the local enstrophy derivative plus a signed diffusion form
\(P_Q=I-E_Q\otimes E_Q\)、\(E_Q=C_Q/\sqrt{d_Q}\) 是实 \(L^2\) 中的全局余维一投影，不是逐点矩阵。\(z_Q\) 的分母不是 \(\|F_j\|_2\sqrt{d_Q}\)，所以它不是相关系数，也没有 \(|z_Q|\le1\) 的普遍界。 ||| \(P_Q=I-E_Q\otimes E_Q\) and \(E_Q=C_Q/\sqrt{d_Q}\) define a global corank-one projection in real \(L^2\), not a pointwise matrix. The denominator of \(z_Q\) is not \(\|F_j\|_2\sqrt{d_Q}\), so it is not a correlation coefficient and has no universal bound \(|z_Q|\le1\).
\[ \kappa_j^{-2}z_Q^+\mathcal J_Q^+\,dt \quad\text{的总尺度指数为 }0. \] ||| \[ \kappa_j^{-2}z_Q^+\mathcal J_Q^+\,dt \quad\text{has total scaling exponent }0. \]
02 · 完整导数 ||| 02 · Complete derivative
03 · 名义率消去 ||| 03 · Nominal-rate cancellation
04 · 平方—余项 ||| 04 · Square–residual form
05 · 局部 enstrophy ||| 05 · Local enstrophy
06 · 二阶余项 ||| 06 · Second-order residual
07 · 两个状态量 ||| 07 · Two state variables
08 · 临界尺度 ||| 08 · Critical scaling
09 · 双号诊断 ||| 09 · Opposite-sign diagnostic
15 · 复现 ||| 15 · Reproduction
把 \(I_Q=\mathcal P_Q^\square-(\nu^2/4)\int\chi_Q|H_j|^2\) 代入，\(\mathcal P_Q^\square\) 精确抵消，得到 ||| Substituting \(I_Q=\mathcal P_Q^\square-(\nu^2/4)\int\chi_Q|H_j|^2\), the term \(\mathcal P_Q^\square\) cancels exactly, giving
版本 v0.71N · 2026-08-26 ||| Version v0.71N · 2026-08-26
本节关闭一个 fixed-cell 代数候选，不关闭所有 signed 路线 ||| This section closes one fixed-cell algebraic candidate, not every signed route
本节完成三件事：先从 quotient rule 展开完整 \(\mathcal J_Q\)；再把 R0.71M 的 radial pairing 代回，核对 \(\nu\kappa_j^2\) 的符号；最后使用局部 filtered-enstrophy 表示 \(B_Q\)。 ||| This section completes three tasks: first expanding the complete \(\mathcal J_Q\) by the quotient rule, then substituting the radial pairing from R0.71M and checking the sign of \(\nu\kappa_j^2\), and finally using the local filtered-enstrophy representation of \(B_Q\).
表面的正平方与加速度行中的负配对是同一个量。二者在完整标量中精确消去。已检查的插入因此留下有符号二阶余项，而不是第二个 coercive scalar fusion。这里没有证明别的 NSE signed estimate 也会失败。 ||| The apparent positive square and the negative pairing in the acceleration row are the same quantity. They cancel exactly in the complete scalar. The checked substitution therefore leaves a signed second-order residual rather than a second coercive scalar fusion. This does not prove that another signed NSE estimate must fail.
第二个正二次融合关闭；denominator faces 开放 ||| Second positive quadratic fusion closed; denominator faces remain open
第一项是 vortex stretching。把 \(Y_t\) 写成纯黏性耗散会把二维恒等式误用于三维。 ||| The first term is vortex stretching. Writing \(Y_t\) as purely viscous dissipation would incorrectly apply a two-dimensional identity in three dimensions.
独立检查器不导入 symbolic producer。它用显式五模无散初值、固定正三角 cutoff、\(\kappa=4\)、\(\nu=0.2\)，从 NSE 在 \(t=0\) 直接计算 \(u_t,\omega_t,L_t\)，没有时间推进。 ||| The independent checker does not import the symbolic producer. It uses explicit five-mode divergence-free initial data, a fixed positive trigonometric cutoff, \(\kappa=4\), and \(\nu=0.2\), and at \(t=0\) directly computes \(u_t,\omega_t,L_t\) from NSE, with no time stepping.
二阶余项 ||| Second-order residual
二阶重写没有找回低阶能量支付。这个局部 co-scaling 也不是固定 torus、固定 multiplier 与固定 cell 的连续对称性。 ||| The second-order rewrite recovers no lower-order energy payment. This local co-scaling is also not a continuous symmetry of a fixed torus, fixed multiplier, and fixed cell.
负 source ||| Negative source
给出点态单位涡量方向的切投影方程。 ||| gives the tangent-projection equation for the pointwise unit vorticity direction.
记 \(\lambda_j=\nu\kappa_j^2\)。直接微分给出 ||| Set \(\lambda_j=\nu\kappa_j^2\). Direct differentiation gives
价值是阻止把一个坐标平方误当成新的耗散 ||| The value is preventing a coordinate square from being mistaken for new dissipation
检查的第二融合没有产生独立正项 ||| The checked second fusion produces no independent positive term
见证 ||| Witness
截至 2026-08-26 的限定一手检索没有找到同时保留该 \(B_{Q,t},d_{Q,t},Y_t\) 的直接来源。这是 bounded negative finding，不是原创性、优先权或不存在性结论。 ||| The bounded primary-source search as of 2026-08-26 found no direct source retaining \(B_{Q,t},d_{Q,t},Y_t\) simultaneously. This is a bounded negative finding, not a claim of originality, priority, or nonexistence.
局部 enstrophy ||| Local enstrophy
局部 enstrophy 又把它精确消掉 ||| local enstrophy then cancels it exactly
局部 filtered enstrophy 与 projective denominator 不能混同 ||| Local filtered enstrophy and the projective denominator are distinct
两个 \(z_Q>0\) 的光滑 NSE 初始 jet 给出 \(\mathcal J_Q\) 双向符号 ||| Two smooth NSE initial jets with \(z_Q>0\) give opposite signs of \(\mathcal J_Q\)
令 \(H_j=(\Delta+\kappa_j^2)W_j\)、\(M_Q=C_{Q,t}+\lambda_jC_Q\)。R0.71M 的 radial identity 是 ||| Let \(H_j=(\Delta+\kappa_j^2)W_j\) and \(M_Q=C_{Q,t}+\lambda_jC_Q\). The radial identity from R0.71M is
另一方面，\(B_{Q,t}+\lambda_jB_Q=\langle G_{j,t},\chi_QW_j\rangle+I_Q\)。因此 ||| On the other hand, \(B_{Q,t}+\lambda_jB_Q=\langle G_{j,t},\chi_QW_j\rangle+I_Q\). Therefore
名义黏性率精确消去，正平方被局部 enstrophy 加速度账本重新吸收；两个正 z 的光滑 NSE 初始 jet 给出 J 的双向符号诊断。 ||| The nominal viscous rate cancels exactly, and the positive square is reabsorbed by the local-enstrophy acceleration ledger; two smooth NSE initial jets with positive z give opposite-sign diagnostics for J.
平方—余项 ||| Square–residual
前者是 cross pairing，后者是 square；只有全局 cell \(\chi_Q=1\) 时才一致。一般 cutoff 下没有普遍比例或符号关系。 ||| The former is a cross pairing and the latter a square; they coincide only for the global cell \(\chi_Q=1\). A general cutoff gives no universal proportionality or sign relation.
三个时间导数先在同一个式子里出现 ||| The three time derivatives first appear in one formula
三维全局 enstrophy 的正确导数是 ||| The correct derivative of three-dimensional global enstrophy is
是已查到最邻近的 filtered-vorticity/local-cutoff 账本，但没有本文的 cutoff–curl denominator 或 \(B_Q/\sqrt{Yd_Q}\) 演化。 ||| is the nearest filtered-vorticity/local-cutoff ledger found, but it has neither the cutoff–curl denominator used here nor the evolution of \(B_Q/\sqrt{Yd_Q}\).
四个邻近部件都有先例，完整 fixed-cell 对象尚未在限定检索中直接碰撞 ||| All four neighboring components have precedents; the bounded search found no direct match for the complete fixed-cell object
投影消去 ||| Projective cancellation
图 R0.71N。A 展示两次精确重写：名义率消去后出现 square–residual，局部 enstrophy 再把同一平方消去。B、C 是两个 \(z_Q>0\) 的 smooth NSE initial-jet 诊断，不是 interval sign theorem。D 记录剩余行的临界尺度与 R0.71O 的 denominator-face 门。 ||| Figure R0.71N. A shows two exact rewrites: nominal-rate cancellation produces the square–residual form, and local enstrophy then cancels the same square. B and C are two smooth NSE initial-jet diagnostics with \(z_Q>0\), not interval sign theorems. D records the critical scaling of the remaining rows and the R0.71O denominator-face gate.
完整标量出现一个正平方， ||| The complete scalar produces a positive square,
完整导数 ||| Complete derivative
完整源先出现一个非负平方 ||| The complete source first produces a nonnegative square
未证明：faces、refresh、moving cells、无限 frame–cell 极限、继续性、全局正则性或有限时破裂。 ||| Not proved: faces, refresh, moving cells, the infinite frame–cell limit, continuation, global regularity, or finite-time breakdown.
未证明：second-jet residual 无法由另一种 NSE signed mechanism 控制。 ||| Not proved: that the second-jet residual cannot be controlled by another signed NSE mechanism.
我继续停在固定小区，同时保留 \(B_{Q,t}\)、\(d_{Q,t}\) 与 \(Y_t\)。名义黏性率在 radial 与 projective 两边精确消去；完整源先化为“非负平方 + 有符号余项”。但把局部 filtered-enstrophy 恒等式代回后，\(G_{j,t}\) 含同一个配对的负号，正平方随之完全消失。最后留下的是临界尺度的二阶时间/归一化余项，不是新的 coercive payment。 ||| I remain on fixed cells and retain \(B_{Q,t}\), \(d_{Q,t}\), and \(Y_t\) simultaneously. The nominal viscous rate cancels exactly between the radial and projective sides, and the complete source first becomes a nonnegative square plus a signed residual. After substituting the local filtered-enstrophy identity, however, \(G_{j,t}\) contains the same pairing with a negative sign, so the positive square disappears completely. What remains is a critical second-order time/normalization residual, not a new coercive payment.
下一对象：soft denominator 与一侧 faces ||| Next object: soft denominator and one-sided faces
下一节仍用固定 cell，比较 hard components 与 ||| The next section remains on a fixed cell and compares the hard components with
研究笔记 R0.71N · FULL SCALAR · EXACT CANCELLATION · SIGNED SECOND JET ||| Research note R0.71N · FULL SCALAR · EXACT CANCELLATION · SIGNED SECOND JET
研究笔记 R0.71N：完整 fixed-cell 标量有精确平方—余项形式；局部 filtered-enstrophy 代回后，表面的正平方精确消去，留下同尺度的有符号二阶余项。 ||| Research note R0.71N: the complete fixed-cell scalar has an exact square–residual form; after the local filtered-enstrophy substitution, the apparent positive square cancels exactly, leaving a signed second-order residual at the same scale.
已诊断：两个 \(z_Q>0\) 的 smooth NSE initial jets 给出 \(\mathcal J_Q\) 双号。 ||| Diagnosed: two smooth NSE initial jets with \(z_Q>0\) give opposite signs of \(\mathcal J_Q\).
已证明：名义 \(\nu\kappa_j^2\) 在 radial/projective 坐标中精确消去。 ||| Established: the nominal \(\nu\kappa_j^2\) cancels exactly in the radial/projective coordinates.
已证明：剩余 second-jet rows 处在同一个临界尺度。 ||| Established: the remaining second-jet rows lie at the same critical scale.
已证明：完整 \(B_{Q,t},d_{Q,t},Y_t\) derivative identity 与正确三维 \(Y_t\)。 ||| Established: the complete \(B_{Q,t},d_{Q,t},Y_t\) derivative identity and the correct three-dimensional \(Y_t\).
已证明：square–residual form 与 local-enstrophy 代回后的正平方精确消去。 ||| Established: the square–residual form and exact cancellation of the positive square after the local-enstrophy substitution.
因此下一步不能继续重排同一个 interior identity。真正尚未结算的是 \(d_Q\downarrow0\) 的一侧 faces、soft-limit source measure，以及随后才出现的 refresh/moving-cell atoms。 ||| The next step therefore cannot keep rearranging the same interior identity. What remains unpaid is the one-sided faces as \(d_Q\downarrow0\), the soft-limit source measure, and only afterward the refresh/moving-cell atoms.
硬归一化只在 \(Y>0\)、\(d_Q>0\) 上使用 ||| Hard normalization is used only when \(Y>0\) and \(d_Q>0\)
有限问题是：\(\varepsilon\downarrow0\) 时的 source measures 与 denominator-zero 一侧 faces，能否由已有 energy 与 denominator-mass budgets 统一支付。R0.71O 暂不进入 refresh atoms 或 moving cutoffs。 ||| The finite question is whether the source measures and one-sided denominator-zero faces as \(\varepsilon\downarrow0\) can be paid uniformly by the existing energy and denominator-mass budgets. R0.71O does not yet enter refresh atoms or moving cutoffs.
余项的每一行仍处在同一个临界阶 ||| Every residual row remains at the same critical order
在 filter 与 cutoff 同步缩放的形式局部 Euclidean NSE scaling 下，\(\sqrt{Yd_Q}\) 的指数为 2；acceleration、annular-mismatch square 和 normalization numerator 的指数都为 5；因此 \(\mathcal J_Q\) 的指数是 3。 ||| Under formal local Euclidean NSE scaling with the filter and cutoff co-scaled, \(\sqrt{Yd_Q}\) has exponent 2; the acceleration, annular-mismatch square, and normalization numerator all have exponent 5; therefore \(\mathcal J_Q\) has exponent 3.
这里的 \(-I_Q\) 正是关键。它包含前一节刚完成平方的同一个 pairing。 ||| The term \(-I_Q\) is the key: it contains the same pairing whose square was just completed in the preceding section.
这是一个精确、有符号、二阶时间/混合归一化 residual。它与原来的 quotient derivative 等价；不能把中途出现的平方单独解释成新的 dissipation。 ||| This is an exact, signed, second-order time/mixed-normalization residual. It is equivalent to the original quotient derivative; the intermediate square cannot be interpreted separately as new dissipation.
这一步本身不提供正性，因为 \(\mathfrak R_Q\) 包含 filtered Lamb acceleration、annular mismatch 和两个归一化导数。 ||| This step alone gives no positivity because \(\mathfrak R_Q\) contains the filtered Lamb acceleration, annular mismatch, and two normalization derivatives.
正 source ||| Positive source
正平方在完整标量中完全消失 ||| The positive square disappears completely in the full scalar
正式附图记录精确消去、双号见证与下一道 face 门 ||| The formal figure records exact cancellation, opposite-sign witnesses, and the next face gate
状态 · R0.71N 精确恒等式与独立 Fourier 审计完成 ||| Status · R0.71N exact identity and independent Fourier audit completed
状态量区别 ||| Distinct state variables
最后一个 \(H_j\) 项的符号是负号。宽环带也不使 \(H_j\) 自动成为小量。 ||| The final \(H_j\) term has a negative sign. A broad annulus does not automatically make \(H_j\) small.
order 48、64、80 的结果一致，全部恒等式残差低于声明阈值。第二个见证中，signed residual 压过正平方。当前计算使用高裕量 binary64 与无混叠求积，尚不是 outward-rounded interval sign theorem；解析 theorem 不依赖这张符号表。 ||| Results agree at orders 48, 64, and 80, and all identity residuals lie below the declared thresholds. In the second witness, the signed residual exceeds the positive square in magnitude. The current calculation uses high-margin binary64 arithmetic and alias-free quadrature, but is not yet an outward-rounded interval sign theorem; the analytic theorem does not depend on this sign table.
R0.71N 对千禧年问题没有直接解答，也没有新的 continuation criterion。它的实际作用是关闭一条容易产生假正性的代数路线：如果只看 projective pairing 完成平方，会看到一个非负项；如果同时保留 \(B_{Q,t}\) 并使用局部 enstrophy，这个项恰好被 acceleration 里的同一 pairing 吃掉。 ||| R0.71N does not directly answer the Millennium problem and gives no new continuation criterion. Its practical role is to close an algebraic route prone to false positivity: completing the square in the projective pairing alone produces a nonnegative term, but retaining \(B_{Q,t}\) and using local enstrophy shows that the same pairing in the acceleration cancels it exactly.
R0.71N 完整标量的平方—余项分解、局部 enstrophy 精确消去、双号 Fourier 诊断和临界尺度 ||| R0.71N square–residual decomposition of the complete scalar, exact local-enstrophy cancellation, opposite-sign Fourier diagnostics, and critical scaling
R0.71N｜完整标量的平方—余项分解与二阶边界 ||| R0.71N | Square–residual decomposition and second-order boundary of the complete scalar
02 · 78 节完整索引 ||| 02 · Complete 78-section index
打开最新节点 R0.71N ||| Open the latest node R0.71N
回顾截止节点：R0.71N ||| Recap endpoint: R0.71N
回顾截止时公开笔记：138 ||| Public notes at recap endpoint: 138
截至 R0.71N，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 78 个节点解释成对千禧年问题完成了某个比例。 ||| Through R0.71N, there is no new unconditional continuation criterion, no reduction of the set of all potential singular solutions, and no proof of finite-time breakdown. The 78 nodes cannot be interpreted as a percentage completion of the Millennium problem.
累计回顾 · R0.61–R0.71N · 2026-08-26 ||| Cumulative recap · R0.61–R0.71N · 2026-08-26
两个 \(z_Q>0\) 的显式 smooth NSE initial jets 给出 \(\mathcal J_Q\) 双号；这是有限初始-jet 诊断，不是时间区间符号定理。 ||| Two explicit smooth NSE initial jets with \(z_Q>0\) give opposite signs of \(\mathcal J_Q\); this is a finite initial-jet diagnostic, not a sign theorem on a time interval.
目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、它的有界重叠局部化，以及 fixed-cell denominator mass 的能量支付。R0.71G–N 把 interior direct route 继续收缩：residence、heat-only、raw collar 与 increment split 依次被核对；完整 \(\mathcal J_Q\) 的正平方又被 local-enstrophy acceleration 精确消去。现在开放的是临界 signed second jet、soft denominator、零分母 faces 和 refresh，而不是另一个 interior quadratic rearrangement。 ||| The most substantive unconditional positive results remain the Leray-energy projected-Lamb heat volume, its bounded-overlap localization, and energy payment of the fixed-cell denominator mass. R0.71G–N further narrows the interior direct route by checking residence, heat-only payment, the raw collar, and the increment split in turn; the positive square in the complete \(\mathcal J_Q\) is then canceled exactly by the local-enstrophy acceleration. What remains open is the critical signed second jet, soft denominator, zero-denominator faces, and refresh, not another interior quadratic rearrangement.
十二个阶段、78 个节点：从约化递推到 projected-Lamb 局部热打包，再到固定匹配小区 heat gap、黏性融合、exact increment–projective bridge 与 signed second-jet boundary。 ||| Twelve phases and 78 nodes: from reduced recurrence to localized projected-Lamb heat packing, then to the fixed matched-cell heat gap, viscous fusion, the exact increment–projective bridge, and the signed second-jet boundary.
收录节点：78 ||| Nodes included: 78
完整 fixed-cell 标量的 square–residual form、\(\nu\kappa_j^2\) radial/projective 精确消去，以及 local filtered-enstrophy 代回后的正平方精确抵消。 ||| The square–residual form of the complete fixed-cell scalar, exact radial/projective cancellation of \(\nu\kappa_j^2\), and exact cancellation of the positive square after substituting local filtered enstrophy.
下一步仍留在固定 cell，比较 hard denominator 与 \(R_{Q,\varepsilon}=\sqrt{d_Q+\varepsilon}\)。R0.71O 检查 \(\varepsilon\downarrow0\) 时的 source measures 和 \(d_Q=0\) 一侧 faces，能否由已有 energy 与 denominator-mass budgets 统一支付。 ||| The next step remains on a fixed cell and compares the hard denominator with \(R_{Q,\varepsilon}=\sqrt{d_Q+\varepsilon}\). R0.71O checks whether, as \(\varepsilon\downarrow0\), the source measures and one-sided faces at \(d_Q=0\) can be paid uniformly by the existing energy and denominator-mass budgets.
这个有限门只处理 hard/soft 极限与一侧时间面，不进入 refresh atoms 或 moving cutoffs。若 source measure 需要未控制的逆分母或新的临界输入，应把它明确记为条件，而不是从 interior identity 中重复制造支付。 ||| This finite gate treats only the hard/soft limit and one-sided time faces, without entering refresh atoms or moving cutoffs. If the source measure requires an uncontrolled inverse denominator or a new critical input, it must be recorded explicitly as a condition rather than manufactured repeatedly from the interior identity.
这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71N 的 78 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。 ||| This page follows the R0.00–R0.60 phase recap and organizes the route from R0.61 through R0.71N into 78 research nodes. I record chronologically what each segment actually proves, which proposal is ruled out by a specific counterexample or scaling analysis, and which conditions have not been derived from the Navier–Stokes equations.
R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 78 个节点沿着这个缺口推进。 ||| The R0.00–R0.60 material remains in the preceding phase recap. The conclusion at R0.60 is that the complete Fourier–Leray structure and higher-order calculations can continue, but the critical quantity for general three-dimensional solutions remains uncontrolled. The following 78 nodes proceed along that gap.
R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71N 的 78 个研究节点，记录从约化递推到 projected-Lamb 热体积、匹配小区 heat gap、黏性融合、增量—投影接口与 signed second jet 的路线。 ||| Research recap after R0.60: a chronological account from R0.61 through R0.71N comprising 78 research nodes, tracing the route from reduced recurrence to projected-Lamb heat volume, the matched-cell heat gap, viscous fusion, the increment–projective interface, and the signed second jet.
R0.61–R0.71N 的 78 节公开笔记 ||| R0.61–R0.71N: 78 public notes
R0.61–R0.71N 回顾 · 2026-08-26 ||| R0.61–R0.71N recap · 2026-08-26
R0.61–R0.71N 研究节点 ||| R0.61–R0.71N research nodes
R0.61–R0.71N｜R0.60 之后的研究回顾 ||| R0.61–R0.71N | Research recap after R0.60
R0.71G–I 把时间缺口压到入口、单边联合生成与 faces。R0.71J–K 在完整 broad parent frame 和固定 aligned matched cells 上证明 \(K^{-2}\) 正生成与 \(O((\nu K^4)^{-1})\) heat payment 的两阶缺口。R0.71L 把 raw viscous collar 精确融合回 localized Laplacian row；R0.71M 再给出 exact increment–projective bridge。R0.71N 从完整 \(B_{Q,t},d_{Q,t},Y_t\) 标量出发，证明 projective completion 中表面的正平方被 local filtered-enstrophy acceleration 精确消去。剩余 signed second jet 仍在临界尺度，且没有固定符号。 ||| R0.71G–I compress the time gap to entry, joint one-sided creation, and faces. R0.71J–K establish a two-power gap between positive creation of order \(K^{-2}\) and heat payment of order \(O((\nu K^4)^{-1})\) on the complete broad parent frame and fixed aligned matched cells. R0.71L fuses the raw viscous collar exactly back into the localized Laplacian row, and R0.71M then gives the exact increment–projective bridge. Starting from the complete \(B_{Q,t},d_{Q,t},Y_t\) scalar, R0.71N proves that the apparent positive square in the projective completion is canceled exactly by the local filtered-enstrophy acceleration. The remaining signed second jet stays at critical scale and has no fixed sign.
R0.71G–R0.71N · 驻留、匹配小区、黏性融合与 signed second jet ||| R0.71G–R0.71N · Residence, matched cells, viscous fusion, and the signed second jet
R0.71N 对完整标量中的第二个正二次候选作了精确复核。完成平方会暂时出现非负 \(\mathcal P_Q^\square\)，但 \(B_Q=e_{Q,t}+\nu D_Q^\chi\) 代回后，acceleration 中的同一 pairing 产生 \(-\mathcal P_Q^\square\) 并完全抵消。两个初始 jet 说明剩余量可以双向取号；它们没有排除时间积分后的其他 NSE signed mechanism。 ||| R0.71N exactly rechecks the second positive quadratic candidate in the complete scalar. Completing the square temporarily produces the nonnegative \(\mathcal P_Q^\square\), but after substituting \(B_Q=e_{Q,t}+\nu D_Q^\chi\), the same pairing in the acceleration produces \(-\mathcal P_Q^\square\) and cancels it completely. Two initial jets show that the remainder can take either sign; they do not rule out another signed NSE mechanism after time integration.
R0.71O 检查 soft denominator 与一侧 face measure ||| R0.71O checks the soft denominator and one-sided face measure
本节关闭的是“完成 projective square 后把它当作新耗散”这一条 fixed-cell 代数路线。它没有证明 signed second jet 不能由其他 NSE 机制控制，也没有得到继续性、奇性或全局正则性结论。 ||| This section closes the fixed-cell algebraic route that treats the completed projective square as new dissipation. It does not prove that the signed second jet cannot be controlled by another NSE mechanism, and it gives no continuation, singularity, or global-regularity conclusion.
表面的正平方被 local-enstrophy acceleration 精确消去；完整 fixed-cell 标量只留下同尺度的 signed second jet。 ||| The apparent positive square is canceled exactly by the local-enstrophy acceleration; the complete fixed-cell scalar retains only a signed second jet at the same scale.
表面的正平方在完整标量中精确消去，留下临界 signed second jet ||| The apparent positive square cancels exactly in the complete scalar, leaving a critical signed second jet
从有符号环带障碍走到 signed second-jet boundary ||| From the signed-annulus obstruction to the signed second-jet boundary
固定 cell 上比较 hard denominator 与 \(\sqrt{d_Q+\varepsilon}\)，核对 \(d_Q=0\) 的一侧 faces 和 soft-limit source measure；暂不进入 refresh 或 moving cells。 ||| On a fixed cell, compare the hard denominator with \(\sqrt{d_Q+\varepsilon}\), checking the one-sided faces at \(d_Q=0\) and the soft-limit source measure; refresh and moving cells remain outside the scope.
固定 cell 上比较 hard denominator 与 \(\sqrt{d_Q+\varepsilon}\)，检查 \(\varepsilon\downarrow0\) 的 source measure 和 \(d_Q=0\) 一侧 faces 能否由已有预算支付。 ||| On a fixed cell, compare the hard denominator with \(\sqrt{d_Q+\varepsilon}\) and check whether the source measure as \(\varepsilon\downarrow0\) and one-sided faces at \(d_Q=0\) can be paid by existing budgets.
固定小区上，完整标量先有精确的平方—余项表示 \[ \mathcal J_Q =\frac{\mathcal P_Q^\square+\mathfrak R_Q}{\sqrt{Yd_Q}}, \qquad \mathcal P_Q^\square =\int\chi_Q\left|G_j+\frac\nu2H_j\right|^2. \] 名义率 \(\nu\kappa_j^2\) 与 radial/projective 坐标中的项精确消去。 ||| On a fixed cell, the complete scalar first has the exact square–residual representation \[ \mathcal J_Q =\frac{\mathcal P_Q^\square+\mathfrak R_Q}{\sqrt{Yd_Q}}, \qquad \mathcal P_Q^\square =\int\chi_Q\left|G_j+\frac\nu2H_j\right|^2. \] The nominal rate \(\nu\kappa_j^2\) cancels exactly against the term in radial/projective coordinates.
环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary ||| Annulus exclusion → source–core ledger → covariance spectral stratification → all-frequency conditional bridge → response-slope chord gain → common-response order-one channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary
静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 建立 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–L 把时间缺口收缩到 fixed matched-cell heat gap 和 exact viscous fusion；R0.71M 再给出 exact increment–projective bridge。R0.71N 从完整标量同时保留三个时间导数，证明 projective completion 中表面的正平方被 local-enstrophy acceleration 精确消去。留下的是同尺度的 signed second jet，而不是新的耗散。 ||| After the static annular family is ruled out rigorously, the route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71A–F establish the Leray-energy projected-Lamb heat volume and its bounded-overlap localization. R0.71G–L compress the time gap to the fixed matched-cell heat gap and exact viscous fusion; R0.71M then gives the exact increment–projective bridge. R0.71N retains all three time derivatives in the complete scalar and proves that the apparent positive square in the projective completion is canceled exactly by the local-enstrophy acceleration. What remains is a signed second jet at the same scale, not new dissipation.
累计回顾 R0.61–R0.71N · 2026-08-26 ||| Cumulative recap R0.61–R0.71N · 2026-08-26
两个显式五模光滑 NSE 初始 jet 都满足 \(z_Q>0\)，但分别给出 \(\mathcal J_Q=1.3523543\) 与 \(-7.3713441\)。48、64、80 三档 Fourier 网格一致；这是有限初始-jet 诊断，不是时间区间符号定理。 ||| Two explicit smooth five-mode NSE initial jets both satisfy \(z_Q>0\), but give \(\mathcal J_Q=1.3523543\) and \(-7.3713441\), respectively. The Fourier grids at 48, 64, and 80 agree; this is a finite initial-jet diagnostic, not a sign theorem on a time interval.
令 \(e_Q=\frac12\int\chi_Q|W_j|^2\) 与 \(D_Q^\chi=-\langle\chi_QW_j,\Delta W_j\rangle\)。局部 filtered-enstrophy 恒等式 \(B_Q=e_{Q,t}+\nu D_Q^\chi\) 代回后，\(\mathfrak R_Q\) 中出现 \(-\mathcal P_Q^\square\)，恰好消去前面的正平方。剩余项仍是尺度临界的有符号二阶时间与混合归一化账本。 ||| Let \(e_Q=\frac12\int\chi_Q|W_j|^2\) and \(D_Q^\chi=-\langle\chi_QW_j,\Delta W_j\rangle\). After substituting the local filtered-enstrophy identity \(B_Q=e_{Q,t}+\nu D_Q^\chi\), \(\mathfrak R_Q\) contains the term \(-\mathcal P_Q^\square\), which cancels the preceding positive square exactly. The remaining terms still form a scale-critical signed ledger of second time derivatives and mixed normalization.
目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71N 关闭了把 projective completion 中的正平方解释成新耗散的路线：local filtered enstrophy 代回后，同一平方被 acceleration 精确消去。剩余 signed second jet 仍是临界量；soft denominator、零分母 faces 和无条件 weighted BV 仍未闭合。 ||| There is no new unconditional continuation criterion and no construction of a finite-time singularity. R0.71N closes the route that interprets the positive square in the projective completion as new dissipation: after substituting local filtered enstrophy, the same square is canceled exactly by the acceleration. The remaining signed second jet is still critical; the soft denominator, zero-denominator faces, and unconditional weighted BV remain unclosed.
上次综述 v0.98 · 2026-08-26 ||| Previous review v0.98 · 2026-08-26
我继续使用 fixed cells，比较 hard components 与 \(R_{Q,\varepsilon}=\sqrt{d_Q+\varepsilon}\)。R0.71O 检查 \(\varepsilon\downarrow0\) 时的 source measures 和 denominator-zero 一侧 faces，能否由已有 energy 与 denominator-mass budgets 统一支付；暂不进入 refresh atoms 或 moving cutoffs。 ||| I continue to use fixed cells and compare the hard components with \(R_{Q,\varepsilon}=\sqrt{d_Q+\varepsilon}\). R0.71O checks whether the source measures and one-sided denominator-zero faces as \(\varepsilon\downarrow0\) can be paid uniformly by the existing energy and denominator-mass budgets; refresh atoms and moving cutoffs remain outside the scope.
我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71N 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。 ||| I also maintain a systematic review page that places classical theory, five main literature branches, the candidate blow-up exclusion tree, progress from 2019—2026, and this site's R0.69P–R0.71N route on one map. Historical nodes R0.61–R0.69O remain in the cumulative recap.
下一步 R0.71O： ||| Next step R0.71O:
研究笔记 R0.71N · 2026-08-26 ||| Research note R0.71N · 2026-08-26
阅读 R0.71N 研究笔记 → ||| Read the R0.71N research note →
展开 48 篇公开笔记 ||| Expand 48 public notes
综述 v0.99 · 2026-08-26 ||| Review v0.99 · 2026-08-26
R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、固定匹配小区、黏性融合、增量—投影接口与 signed second jet。 ||| The route after R0.60 has twelve phases: reduced Picard and the shear boundary, transverse perturbations, the local pressure budget, signed physical annuli, moving labels and source–core duality, the defect tensor and finite observations, complete-frame covariance, the constant-projection boundary, positive output and the material-heat tent, projected-Lamb heat volume, local heat packing and the critical trace obstruction, and finally the residence boundary, fixed matched cells, viscous fusion, the increment–projective interface, and the signed second jet.
R0.60 recap 之后的累计回顾收录 78 个节点；全站现有 138 篇公开研究笔记 ||| The cumulative recap after the R0.60 recap contains 78 nodes; the site now has 138 public research notes
R0.71N 已完成： ||| R0.71N completed:
Soft denominator 与 \(d_Q=0\) 一侧 faces ||| Soft denominator and one-sided faces at \(d_Q=0\)
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
  throw new Error("duplicate Chinese keys in the R0.71N additions");
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
  "recap-r0-61-r0-71n.html",
  "notes/r0-71n.html",
];
for (const relative of activePages) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=0.99')) {
    throw new Error(relative + ": expected i18n cache version v0.99");
  }
}

const batchId = /^r071n\d+$/;
const currentWithoutBatch = current.filter((entry) => !batchId.test(entry.id));
const currentByChinese = new Map(
  currentWithoutBatch.map((entry) => [entry.zh, entry]),
);
if (currentByChinese.size !== currentWithoutBatch.length) {
  throw new Error(
    "duplicate Chinese keys already present outside the R0.71N batch",
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
    id: "r071n" + String(index + 1).padStart(3, "0"),
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
