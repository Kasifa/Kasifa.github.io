# R0.73L bilingual terminology ledger

**Status:** canonical release terminology source
**Scope:** continuum proof, independent audits, finite diagnostic, formal figure,
HTML/PDF note, cumulative recap, and literature boundary
**Release title:** *Parameter-uniform nonselfadjoint adiabatic tracking*

This ledger fixes the English terminology and the claim-state vocabulary for
R0.73L. It does not enlarge the mathematical result.

## Core terminology

| 中文 | English | Exact usage boundary |
|---|---|---|
| 参数一致非自伴绝热跟踪 | parameter-uniform nonselfadjoint adiabatic tracking | Uniform in the shared small parameter that controls both viscosity and the slow time scale; it is proved only for the sealed two-dimensional linearized shear model. |
| 快时间 | fast time | The variable \(\theta\) in \(\partial_\theta u=B_\varepsilon(\varepsilon\theta)u\). |
| 慢时间 | slow time | The variable \(d=\varepsilon\theta\) in \(\varepsilon\partial_d u=B_\varepsilon(d)u\), restricted to \(0\le d\le1/450\). |
| 共同定义域演化 | common-domain evolution | Evolution generated on the common domain \(H^2_{\rm per}\); no viscosity-uniform graph norm is asserted. |
| Kato 修正 | Kato correction | \(\mathcal K_\varepsilon=[P_\varepsilon',P_\varepsilon]\), with the positive sign in the corrected generator. |
| 精确交织 | exact intertwining | \(P(d)U^{\rm a}(d,s)=U^{\rm a}(d,s)P(s)\); it moves both the selected line and complementary fiber exactly. |
| selected 谱线 | selected spectral line | The algebraically simple rank-one range \(P_\varepsilon(d)H\). “Selected line” is allowed in compact figure text. |
| 移动补空间 | moving complement | The nonorthogonal fiber \(Q_\varepsilon(d)H\), where \(Q_\varepsilon=I-P_\varepsilon\). |
| 固定快时间块 | fixed fast-time block | A block of viscosity-independent fast-time length \(T\), corresponding to slow length \(\varepsilon T\). |
| 单块相对收缩 | one-block relative contraction | Complementary evolution contracts relative to the selected action on each complete fast-time block. |
| 移动补空间相对稳定性 | moving-complement relative stability | The chained estimate \(\|U_Q^{\rm a}(d,s)\|\le M_Qe^{\Phi_\varepsilon(d,s)}e^{-\gamma_Q(d-s)/\varepsilon}\). |
| Kato selected 演化 | Kato selected evolution | The rank-one part of the corrected evolution; it is the comparison orbit, not the exact orbit. |
| 前向 Volterra 系统 | forward Volterra system | The coupled equations for \(p=P(d)u(d)\) and \(q=Q(d)u(d)\), estimated only forward in slow time. |
| 补空间泄漏 | complementary leakage | The \(Q\)-component generated from selected initial data; the theorem proves it is \(O(\varepsilon)\) relative to the selected action. |
| selected 坐标 | selected coordinate | The scalar rank-one coordinate transported by the Kato gauge. |
| 两侧有界前因子 | bounded two-sided prefactor | Constants \(0<c_L\le C_L<\infty\) independent of \(\varepsilon\) and \(D\); no prefactor limit is claimed. |
| 黏性作用量 | viscous action | \(\Phi_\varepsilon(d,s)=\varepsilon^{-1}\int_s^d\lambda_\varepsilon(r)\,dr\). |
| 无黏作用量 | inviscid action | \(\varepsilon^{-1}\int_s^d\lambda_0(r)\,dr\), obtained using the inherited \(O(\varepsilon)\) eigenvalue displacement. |
| 匹配增长作用量 | matching selected gain action | Two-sided comparison of the exact gain with the viscous action and, up to another fixed factor, the inviscid action. |
| 向量级相对跟踪 | vector-level relative tracking | The exact orbit differs from the Kato selected orbit by \(O(\varepsilon)e^{\Phi_\varepsilon}\); exact instantaneous invariance is not claimed. |
| 前向轨道定位 | forward-orbit localization | Action-resolved localization obtained by dividing estimates at two times on the same normalized forward orbit. |
| 反向抛物演化 | backward parabolic evolution | Explicitly not used and not claimed; the theorem does not solve the complementary parabolic equation backward from terminal data. |
| 显式绝热阈值 | explicit adiabatic threshold | A numerical value for \(\varepsilon_L\); this remains OPEN because inherited constants are qualitative. |
| 前因子极限 | prefactor limit | A limit of the action-normalized gain as \(\varepsilon\downarrow0\); boundedness alone does not establish it. |
| 两项 WKB 展开 | two-term WKB expansion | A higher-order asymptotic expansion requiring additional regularity and superadiabatic control; it remains OPEN. |
| 有限绝热诊断 | finite adiabatic diagnostic | Fifteen finite Fourier trajectories used for reproducibility and error detection, never as the continuum proof. |
| 独立有限重算 | independent finite reconstruction | Five midpoint matrix-exponential reconstructions that do not reuse the primary DOP853 time integrator. |
| 作用量归一化增益 | action-normalized gain | \(\|u(D)\|e^{-\Phi_\varepsilon(D,0)}\) in the finite diagnostic. |
| 终点泄漏比 | terminal leakage ratio | \(\|Q_Nu_N(D)\|/\|P_Nu_N(D)\|\) at the final slow-time node. |
| 后向作用量余差 | backward-action residual | A quotient computed from one forward orbit; it is not the output of a backward solve. |
| 正式附图包 | formal figure package | The sealed PDF/SVG/600-dpi PNG package with source data, provenance, monitoring logs, checksums, and visual QA. |

## Fixed theorem language

**Chinese**

对充分小的 \(0<\varepsilon\le\varepsilon_L\) 和全部
\(0\le D\le1/450\)，从 \(P_\varepsilon(0)H\) 的单位向量出发的真实
非自治轨道满足

\[
 c_Le^{\Phi_\varepsilon(D,0)}
 \le \|U_\varepsilon(D,0)h_\varepsilon(0)\|
 \le C_Le^{\Phi_\varepsilon(D,0)},
\]

其中 \(c_L,C_L\) 不随 \(\varepsilon,D\) 变化。精确轨道相对 Kato
selected 演化的误差为 \(O(\varepsilon)e^{\Phi_\varepsilon}\)，同一条前向
轨道还满足 action-resolved localization。把 \(\lambda_\varepsilon\) 换成
\(\lambda_0\) 只改变固定乘法常数。

**English**

For every sufficiently small \(0<\varepsilon\le\varepsilon_L\), every
\(0\le D\le1/450\), and unit initial data in \(P_\varepsilon(0)H\), the exact
nonautonomous orbit satisfies

\[
 c_Le^{\Phi_\varepsilon(D,0)}
 \le \|U_\varepsilon(D,0)h_\varepsilon(0)\|
 \le C_Le^{\Phi_\varepsilon(D,0)},
\]

with \(c_L,C_L\) independent of \(\varepsilon,D\). The exact orbit tracks the
Kato selected evolution with relative error \(O(\varepsilon)\), and the same
forward orbit obeys action-resolved localization. Replacing
\(\lambda_\varepsilon\) by \(\lambda_0\) changes only the fixed multiplicative
constant.

## Machine-readable claim ledger

The following assignments must remain byte-exact in Chinese and English.

```text
commonDomainEvolution=CLOSED
katoIntertwining=CLOSED
movingComplementRelativeStability=CLOSED
nonselfadjointAdiabaticTracking=CLOSED
matchingSelectedGainAction=CLOSED
actionResolvedBackwardLocalization=CLOSED

finiteDiagnosticPackage=CLOSED
primaryAdiabaticCases=15
independentFiniteReconstruction=PASS
formalFigurePackage=PASS
finiteDimensionDoesNotCertifyContinuum=TRUE

explicitAdiabaticThreshold=OPEN
prefactorLimit=OPEN
twoTermWKB=OPEN
nonlinearNavierStokes=OPEN
transverseThreeDimensionalClosure=OPEN
finiteTimeSingularity=OPEN
Clay=OPEN
```

## Required limitation language

**Chinese**

本节证明特定二维周期剪切流线性化模型中的参数一致非自伴绝热跟踪。
有限 Fourier 轨迹和正式附图只作诊断。结论没有给出显式
\(\varepsilon_L\)、前因子极限或两项 WKB 展开，也没有证明二维非线性
离轨、横向三维闭合、有限时间奇性或 Clay 问题。NOT CLAY。

**English**

R0.73L proves parameter-uniform nonselfadjoint adiabatic tracking only for the
specified two-dimensional periodic-shear linearization. The finite Fourier
trajectories and formal figure are diagnostic only. The result gives no
explicit \(\varepsilon_L\), prefactor limit, or two-term WKB expansion, and it
does not prove two-dimensional nonlinear departure, transverse
three-dimensional closure, finite-time singularity, or the Clay problem.
NOT CLAY.

## Translation invariants

- Preserve every formula, interval, release number, count, and machine-ledger
  assignment.
- Translate `selected action` as “selected action” or “selected spectral
  action”; do not replace it with an energy law.
- Translate `forward-orbit localization` literally enough to retain that the
  estimate uses one forward orbit and no backward parabolic solve.
- Keep theorem, finite diagnostic, formal figure, and open problem as four
  distinct evidence classes.
- Use individual-researcher voice. Do not claim generality, originality,
  priority, nonlinear instability, three-dimensional closure, or a solution
  of the Clay problem.

## Publication titles

```text
R0.73L｜Parameter-uniform nonselfadjoint adiabatic tracking
R0.61–R0.73L｜R0.60 之后的研究回顾
```
