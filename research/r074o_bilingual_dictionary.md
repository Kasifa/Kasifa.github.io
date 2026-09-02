# R0.74O bilingual terminology lock

This dictionary is for local direct translation in the publication task.
No DGX translation is required.

| English source term | Locked Chinese publication term | Boundary note |
|---|---|---|
| amplitude freedom | 自由振幅 / 振幅自由度 | Only the passive first component is rescaled; this is not general Navier--Stokes amplitude scaling. |
| passive-component amplitude | 被动分量振幅 | The scalar multiplier \(\mathfrak a\) in \((\mathfrak a F,B\theta,0)\). |
| normalized amplitude | 归一化振幅 | \(\mathfrak a_0=B\Gamma^{-1/2}\), used in R0.74G--N. |
| amplitude multiplier | 振幅乘子 | Use \(\varkappa\), never \(\kappa\); the latter is the inherited geometric constant 16. |
| amplified exact family | 放大后的精确解族 | Still smooth, periodic, mean-zero, unforced, and exact. |
| scalar payment | 标量支付量 | The complete frozen \(P_R^\alpha\), not a selected denominator row. |
| scalar-payment-only estimate | 纯标量支付估计 | Its right side is a function of \(P_R^\alpha\) alone. |
| square-root-log endpoint | 平方根对数端点 | \(P^{2/3}\sqrt{1+\log_+P}\). |
| universal scalar endpoint | 普适标量端点 | Refuted for the frozen \(P_R^\alpha\); augmented estimates are not refuted. |
| large-payment regime | 大支付区 | The counterexample has \(P_*\to\infty\). |
| small-payment bound | 小支付上界 | Inherited and unchanged. |
| exact 2D3C splitting | 精确 2D3C 分裂 | Two-dimensional dependence with three velocity components. |
| passive packet | 被动包 | The field \(F\) solving a linear advection--diffusion equation over the shear. |
| background shear | 背景剪切 | The \(B\theta\) component that fixes the payment lower scale. |
| complete payment ledger | 完整支付账本 | Includes energy, gauge-fixed pressure, velocity-cubic, harmonic, and acceleration rows. |
| buffered local energy | 缓冲局部能量 | The packet is exponentially suppressed after the amplified substitution. |
| exact energy reserve | 精确能量余量 | \(e_E-2m/3=1171/943200>0\). |
| gauge-fixed pressure row | 固定规范压力行 | Retained even though the physical pressure is zero. |
| velocity-cubic row | 速度三次行 | Its packet-to-background ratio equals 1 for the selected exponential multiplier. |
| algebraic harmonic row | 调和代数行 | Its packet-to-background ratio is \(L^{-3/2}\). |
| fifth-shell shear lower bound | 第五支付壳剪切下界 | Independent of the passive amplitude. |
| pointwise orthogonality | 逐点正交 | Prevents the passive component from cancelling the shear lower bound. |
| positive cumulative collar flux | 正累积领圈通量 | \(\mathfrak C_R^\alpha\), formed from the positive part and time supremum. |
| exact quadratic flux scaling | 通量的精确二次缩放 | \(\mathfrak C_* =\varkappa^2\mathfrak C_0\). |
| endpoint energy-and-dissipation quantity | 端点动能—耗散量 | \(X_R^\alpha\); do not imply a separate matching dissipation lower bound. |
| terminal-lobe lower bound | 终端叶片下界 | Valid for every passive amplitude. |
| non-circular closure | 非循环闭合 | Direct \(X\) lower plus direct collar upper precede the signed-flux \(X\) upper. |
| power increment | 幂指数增量 | \(\delta_*=86/11907\). |
| realized scalar frontier | 已实现的标量前沿 | \(q_*=8024/11907\); no optimality above this scale is claimed. |
| scalar sub-frontier no-go | 标量次前沿不可能性 | Every \(o(p^{q_*}(1+\log_+p)^{7/6})\) majorant fails. |
| fixed logarithmic correction | 固定对数修正 | Every prescribed \(P^{2/3}(1+\log_+P)^\gamma\) fails after choosing a family for that \(\gamma\). |
| polynomial amplitude corollary | 多项式振幅推论 | The exact family may depend on the fixed \(\gamma\). |
| additive repair observable | 加法修复可观测量 | Must detect at least \(c\varkappa^2B^2LR^2\) along this family. |
| flux-augmented payment | 通量增广支付 | \(\widehat P=P+\mathfrak C^{3/2}\); detects the obstruction but does not make flux independently small. |
| temporal concentration | 时间集中 | A candidate structural feature missed by scalar payment; no sufficiency theorem is claimed. |
| exact rational certificate | 精确有理数证书 | Checks arithmetic and finite ledgers only. |
| independent analytic reconstruction | 独立解析重建 | Must recompute every amplitude ledger and quantifier. |
| bounded primary-source audit | 有界一手文献审计 | A finite non-hit is not novelty or priority evidence. |
| admissibility precedent | 可容许结构先例 | 2D3C passive-component literature supports structure, not project-specific scaling laws. |
| schematic analytic figure | 解析示意图 | Not to scale; not DNS, simulation, or sampled dynamics. |
| PROVED | 已证明 | Use only after the analytic argument and independent audit pass. |
| INHERITED | 沿用 | Established and audited in an earlier frozen release. |
| FINITE | 有限验证 | Exact computation, not an analytic proof. |
| LITERATURE BOUNDARY | 文献边界 | Records search scope and theorem mismatch only. |
| OPEN | 未解决 | Not established by R0.74O. |
| NOT CLAY | 非 Clay 结论 / NOT CLAY | Keep the literal English flag visible. |

Publication prose must say that the universal square-root-log estimate is
refuted only when the right side is a function of the frozen scalar payment
\(P_R^\alpha\) alone.  It must not say that all endpoint estimates, all
epsilon-regularity criteria, or all augmented structural estimates fail.
It must say that every constructed solution is smooth and global for the
required time range, that no singularity is produced, and that novelty and
priority remain open.  The one-sequence exponential result and the
family-may-depend-on-\(\gamma\) polynomial corollary must not be conflated.
