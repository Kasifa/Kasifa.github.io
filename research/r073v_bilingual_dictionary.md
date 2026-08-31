# R0.73V bilingual dictionary and public-claim boundary

**Status:** canonical terminology, analytic audit, two-path exact-certificate
seal, formal-figure source seal, immutable source pins, and local-direct
translation route are frozen; HTML/PDF rendering and public deployment remain
separate gates

**Release title:** R0.73V | A pressure-aware signed third-order heat lift: exact scale generation and the 3→4 physical-time boundary

**Public title (zh):** R0.73V｜压力感知的有符号三阶热提升：精确尺度生成律与 3→4 物理时间边界

**Previous release:** R0.73U

**Analytic source commit:** `25636c886f1ee2449418b5548b42f9f0fa269b47`

**Certificate source commit:** `7c445c522a241bdc8b867b6fce0f0fed9b82e97d`

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

Ordinary Chinese--English translation for this release is performed directly
on the local workstation. DGX and external translation services are not used.
In English, “heat” refers to the heat semigroup or its filter-scale parameter,
not to thermodynamic heat. The phrase “third-order” refers to polynomial order
in the velocity unless a moment or cumulant is named explicitly.

## 1. Canonical section headings

| 中文标题 | English heading |
|---|---|
| 直接结论 | Main result at a glance |
| 方程槽压缩提升与精确尺度生成律 | The equation-slot-compressed lift and its exact scale-generation law |
| 透明的三阶 cumulant 与完整压力账本 | The transparent third cumulant and the complete pressure ledger |
| 条件性临界行与精确 trace 投影 | Conditional critical rows and the exact trace projection |
| 物理时间中的 \(3\to4\) 边界 | The \(3\to4\) boundary in physical time |
| 底 heat 尺度的阶数分离 | Order separation at the bottom heat scale |
| 两路径精确证书说明了什么 | What the two-path exact certificate establishes |
| 四站点的 \(O(s^2)\) 对 \(O(s)\) 分离 | Four-site \(O(s^2)\)-versus-\(O(s)\) separation |
| 压缩提升的精确系数 | Exact coefficients of the compressed lift |
| 六站点的同输出压力见证 | The six-site same-output pressure witness |
| 一个非零四次 next-level remainder | A nonzero quartic next-level remainder |
| 文献归属与限定式检索 | Literature attribution and the bounded search |
| 结果价值与下一步 | Research value and the next step |

## 2. Mathematical terms

| 中文 | English | Required meaning |
|---|---|---|
| 周期 heat 半群 | periodic heat semigroup | \(P_s=e^{s\Delta}\) on the normalized torus. “Heat” is not thermodynamic heat. |
| 投影非线性 | projected nonlinearity | \(N=\mathbb P\nabla\cdot(u\otimes u)=(u\cdot\nabla)u+\nabla p\). It already contains pressure through the Leray projector. |
| 对称张量积 | symmetric tensor product | \(a\odot b=a\otimes b+b\otimes a\). |
| 压力感知 | pressure-aware | The chosen object contains the Leray/Riesz pressure contribution. It does not mean pressure is bounded from the energy class. |
| 完整奇次三阶张量切向量 | complete odd cubic tensor tangent | \(\mathcal C_s=P_s(u\odot N)\), the complete odd cubic contribution in the quadratic tensor equation. |
| 方程槽压缩提升 | equation-slot-compressed lift | \(\chi_s=\mathcal C_s-v_s\odot N_s\), a single symmetric tensor chosen for the odd slot in the \(\Theta_s\) equation. Do not shorten this to “minimal lift.” |
| 压力感知 cross-covariance | pressure-aware cross-covariance | The centered covariance \(\tau_s(u,N)+\tau_s(N,u)=\chi_s\). |
| 精确尺度生成律 | exact scale-generation law | The PDE for \(\chi_s\) in the filter variable \(s\), together with its zero datum and Duhamel formula. |
| 向下三角尺度恒等式 | downward-triangular scale identity | The value at scale \(s\) is generated from the lower-scale path \(0\le r\le s\); it is not a same-positive-scale constitutive law. |
| tensor heat-plane 方程 | tensor heat-plane equation | The exact \((t,s)\) identity for \(\Theta_s\), containing \(G_s\), the resolved odd product, and \(\chi_s\). |
| 底尺度导数 | bottom-scale derivative | Evaluation of \(\partial_r\tau_r\) at \(r=0\). It is exact on a smooth full-scale path but not a stable one-scale inversion. |
| 原始三阶局部矩 | raw local third moment | \(M_{ijk,s}=P_s(u_i u_j u_k)\). |
| 第三 generalized heat cumulant | third generalized heat cumulant | The centered tensor \(\kappa_{ijk,s}\) obtained by subtracting every first-times-second product and adding the resolved cubic correction. |
| 三阶 cumulant 尺度方程 | third-cumulant scale equation | The exact \(s\)-PDE coupling \(\partial v_s\) to \(\partial\tau_s\); it is not a physical-time closure. |
| 压力--速度 covariance | pressure--velocity covariance | \(Q_{i,s}=\tau_s(p,u_i)\). It is cubic in velocity through pressure. |
| 压力--应变 covariance | pressure--strain covariance | \(R_{ij,s}=\tau_s(p,S_{ij})\). It contains a derivative and has no derivative-free critical row in this release. |
| 梯度 covariance | gradient covariance | \(D_{ij,s}=\sum_k\tau_s(\partial_k u_i,\partial_k u_j)\). Its trace is nonnegative. |
| 完整 Germano stress 账本 | complete Germano stress ledger | The exact stress equation containing \(\kappa,Q,R,D\), transport, viscosity, and resolved production. |
| 透明三阶 bundle | transparent third-order bundle | The Germano objects \((\kappa,Q,R)\) used to display separate velocity and pressure rows. It is not uniquely minimal. |
| 压缩表示 | compressed representation | The Leray-projected symmetric tensor \(\chi_s\), used to occupy one tensor-tangent slot. It is equivalent to the transparent representation only with the declared lower state retained. |
| 假截断 | false truncation | An equation that retains \(\kappa_s\) but omits the exact \(Q_s\) or \(R_s\) rows. This formula-level failure is not a whole-field information no-go. |
| complete centered pressure source | complete centered pressure source | \(\mathfrak P_{ij,s}=-\partial_iQ_{j,s}-\partial_jQ_{i,s}+2R_{ij,s}\). |
| 条件性临界通量行 | conditional critical flux row | A uniform \(L_t^{4/3}L_x^2\) bound that already assumes \(u\in L_t^4L_x^6\). |
| 精确 trace 投影 | exact trace projection | Half the trace of the complete stress equation. It kills \(R_{ii}\) by incompressibility, not by an estimate. |
| 亚滤波能量 | subfilter energy | \(k_s=\tfrac12\operatorname{tr}\tau_s\). |
| 完整标量三阶通量 | complete scalar third-order flux | \(J_{k,s}=\tfrac12\kappa_{iik,s}+Q_{k,s}\). Pressure--velocity covariance remains inside this flux. |
| 带符号 production | signed production | \(-\tau_{ik,s}\partial_kv_{s,i}=-\tau_s:\nabla v_s\). It has no fixed sign and is the next scalar obstruction. |
| \(3\to4\) 物理时间边界 | \(3\to4\) physical-time boundary | The displayed natural third-level observables have physical-time equations containing quartic velocity terms. It is not a fourth-order non-closure theorem. |
| 四次 next-level remainder | quartic next-level remainder | A fourth-degree contribution in a selected third-level time derivative. Nonzero does not imply that fourth-order data cannot close. |
| 底尺度阶数分离 | bottom-scale order separation | \(\kappa_s=O(s^2)\) while the centered pressure source is generally \(O(s)\), with explicit leading tensors. |
| 非退化精确见证 | nondegenerate exact witness | A declared finite Fourier field for which the relevant leading coefficients are both certified nonzero. |
| 系数级 \(s^{-1}\) 代价 | coefficient-level \(s^{-1}\) cost | The cost required to absorb the selected \(O(s)\) pressure coefficient into the selected \(O(s^2)\) cumulant-flux coefficient. It is not a whole-field norm lower bound. |
| 同输出系数非恢复 | same-output coefficient non-recovery | At one output mode, the declared contracted velocity row vanishes while a pressure row does not. It is not a two-state collision. |
| 全场信息碰撞 | whole-field information collision | Two distinct inputs with the same complete declared state but different target output. R0.73V does not provide such a collision for the full \(\kappa_s\) field. |
| 两路径精确证书 | two-path exact certificate | Two independent exact-rational implementations that agree byte-for-byte on their complete common core. |
| 精确稀疏 Fourier 诊断 | exact sparse-Fourier diagnostic | Finite algebra for selected smooth trigonometric fields. It is not PDE time integration or a Navier--Stokes simulation. |
| 限定式检索 | bounded search | A scoped primary-source search. Non-detection does not establish novelty, priority, non-existence, or first authorship. |
| 任意初值三维全局正则性 | arbitrary-data three-dimensional global regularity | Open. No R0.73V estimate derives the critical strong norm from energy data. |
| Clay 千禧年问题结论 | Clay Millennium conclusion | Open and expressly not claimed. |

## 3. Canonical notation

| Symbol | Frozen meaning |
|---|---|
| \(P_s=e^{s\Delta}\) | periodic heat semigroup |
| \(v_s=P_su\) | signed heat-filtered velocity |
| \(\Theta_s=P_s(u\otimes u)\) | heat-filtered local quadratic tensor |
| \(\tau_s=\Theta_s-v_s\otimes v_s\) | heat covariance / exact subfilter stress |
| \(\mathcal B(a,b)=\mathbb P\nabla\cdot(a\otimes b)\) | Leray-projected bilinear nonlinearity |
| \(N=\mathcal B(u,u)\), \(N_s=P_sN\) | unfiltered and heat-filtered projected nonlinearities |
| \(a\odot b=a\otimes b+b\otimes a\) | symmetric tensor product |
| \(\mathcal C_s=P_s(u\odot N)\) | complete odd cubic tensor-tangent contribution |
| \(\chi_s=\mathcal C_s-v_s\odot N_s\) | equation-slot-compressed pressure-aware lift |
| \(G_s=P_s\sum_\ell\partial_\ell u\otimes\partial_\ell u\) | even gradient moment in the tensor heat-plane equation |
| \(M_{ijk,s}=P_s(u_i u_j u_k)\) | raw local third moment |
| \(\kappa_{ijk,s}\) | third generalized heat cumulant defined in report equation (3.2) |
| \(Q_{i,s}=\tau_s(p,u_i)\) | pressure--velocity covariance |
| \(R_{ij,s}=\tau_s(p,S_{ij})\) | pressure--strain covariance |
| \(D_{ij,s}=\sum_k\tau_s(\partial_k u_i,\partial_k u_j)\) | gradient covariance |
| \(\rho_s=P_s(u\odot\nabla p)-v_s\odot\nabla p_s\) | centered pressure-gradient covariance |
| \(\mathfrak P_{ij,s}=-\partial_iQ_{j,s}-\partial_jQ_{i,s}+2R_{ij,s}\) | complete centered pressure source |
| \(E(I)=L^4(I;L^6(\mathbb T^3))\) | critical strong velocity space used only conditionally |
| \(k_s=\tfrac12\operatorname{tr}\tau_s\) | subfilter energy |
| \(J_{k,s}=\tfrac12\kappa_{iik,s}+Q_{k,s}\) | complete scalar third-order flux |
| \(q=e^{-s}\) | exact certificate heat variable |
| \(h_*=(1,2,0)\) | selected four-site output mode |
| \(K=\begin{psmallmatrix}-2&1&0\\1&0&0\\0&0&0\end{psmallmatrix}\) | compressed-lift coefficient matrix, with \(|K|_F=\sqrt6\) |
| \(u_L(x)=u(Lx)\), \(s=\theta L^{-2}\) | integer covering dilation and parabolic heat slice |

Tensor norms are Frobenius norms unless explicitly stated otherwise. The
English HTML/PDF must preserve the time-space order in
\(L_t^4L_x^6\) and \(L_t^{4/3}L_x^2\). The symbol \(\chi_s\) is reserved
for the compressed lift; do not reuse it for the full Germano source.

## 4. Frozen equation descriptions

| Equation | Required English description |
|---|---|
| \((\partial_s-\Delta)\chi_s=2\sum_\ell\partial_\ell v_s\odot\partial_\ell N_s\), \(\chi_0=0\) | the exact filter-scale generation law for the equation-slot-compressed pressure-aware lift; not a physical-time closure |
| \(\chi_s=2\int_0^sP_{s-r}[\sum_\ell\partial_\ell v_r\odot\partial_\ell N_r]dr\) | a downward-triangular lower-scale representation, not a same-positive-scale constitutive law |
| \((\partial_t-\nu\partial_s)\Theta_s=-2\nu G_s-v_s\odot N_s-\chi_s\) | the exact tensor heat-plane equation; \(\chi_s\) fills the odd cubic slot while \(G_s\) remains |
| report equation (3.3) | the exact third generalized heat-cumulant equation in the filter variable |
| report equation (3.8) | Germano's complete second-stress equation specialized to the heat filter and the current sign convention |
| \(\sup_s\|\kappa_s\|_{L_t^{4/3}L_x^2}\le C_\kappa\|u\|_{L_t^4L_x^6}^3\) | a conditional critical row that already assumes the classical strong norm |
| \(\sup_s\|Q_s\|_{L_t^{4/3}L_x^2}\le2C_R\|u\|_{L_t^4L_x^6}^3\) | the conditional pressure--velocity row; no analogous derivative-free row is claimed for \(R,\rho,\chi\) |
| report equation (4.5) | the exact subfilter-energy trace equation; pressure--strain cancels, but signed production remains |
| report equations (5.1) and (5.4) | exact physical-time entry from the natural third level to quartic velocity terms; not a non-closure theorem |
| \(\kappa_s=O(s^2)\), \(\mathfrak P_s=O(s)\) | bottom-scale order separation, with any ratio claim restricted to a certified nondegenerate coefficient |
| report equations (7.2)--(7.5) | exact four-site coefficient formulas proving an \(s^{-1}\) absorption cost only for the selected rows |
| \(\partial_t\widehat\kappa_{112,s}(0,2,0)|_{\rm nonlinear}=2iq^2(1-q^2)^2\) | a selected nonzero quartic next-level remainder, not fourth-order non-closure |

## 5. Mandatory bilingual boundary sentences

The English sentences below are release-locked. They may be line-wrapped but
must not be strengthened.

| 中文冻结句 | Mandatory English sentence |
|---|---|
| R0.73V 的“压力感知”表示投影非线性 \(N\) 已包含压力贡献，不表示压力已由能量类控制。 | “In R0.73V, ‘pressure-aware’ means that the projected nonlinearity \(N\) already contains the pressure contribution; it does not mean that pressure is controlled from the energy class.” |
| \(\chi_s\) 是为二次张量方程选择的方程槽压缩提升，不承担信息论最小、分量最小、唯一或稳定可逆声明。 | “The field \(\chi_s\) is an equation-slot-compressed lift chosen for the quadratic tensor equation; no information-theoretic minimality, componentwise minimality, uniqueness, or stable invertibility is claimed.” |
| \(\chi_s\) 的精确方程沿 filter parameter \(s\) 演化，并使用全部较小尺度路径；它不是物理时间闭合或单正尺度本构律。 | “The exact equation for \(\chi_s\) evolves in the filter parameter \(s\) and uses the full lower-scale path; it is neither a physical-time closure nor a single-positive-scale constitutive law.” |
| \(\chi_s\) 精确填入二次张量 heat-plane 方程的奇次三阶槽，但偶次梯度矩 \(G_s\) 仍然存在。 | “The field \(\chi_s\) exactly fills the odd cubic slot in the quadratic tensor heat-plane equation, while the even gradient moment \(G_s\) remains.” |
| 完整 Germano stress 方程同时含有 \(\kappa_s,Q_s,R_s,D_s\) 和 resolved production；只保留 \(\kappa_s\) 是假截断。 | “The complete Germano stress equation contains \(\kappa_s,Q_s,R_s,D_s\) and resolved production; retaining only \(\kappa_s\) is a false truncation.” |
| 假截断漏掉非零压力项，不等于这些项从所有其他全场状态都不可恢复。 | “A false truncation omits nonzero pressure terms, but this does not show that those terms are unrecoverable from every other full-field state.” |
| \(\kappa_s\) 与 \(Q_s\) 的一致临界通量估计已经假设 \(u\in L_t^4L_x^6\)，所以它们对任意能量初值的全局正则性是循环的。 | “The uniform critical flux estimates for \(\kappa_s\) and \(Q_s\) already assume \(u\in L_t^4L_x^6\), so they are circular for global regularity from arbitrary energy data.” |
| 本节没有给出 \(R_s,\rho_s\) 或 \(\chi_s\) 的无导数临界行。 | “This release does not provide a derivative-free critical row for \(R_s,\rho_s\), or \(\chi_s\).” |
| 一半 trace 严格消掉 pressure--strain，但完整标量方程仍含没有固定符号的 production \(-\tau_s:\nabla v_s\)。 | “Taking half the trace removes pressure--strain exactly, but the complete scalar equation still contains the sign-indefinite production \(-\tau_s:\nabla v_s\).” |
| 物理时间 \(3\to4\) 结论只针对文中展示的原始三阶矩与压缩提升，不是四阶不闭合或有限层级 no-go。 | “The physical-time \(3\to4\) conclusion applies only to the displayed raw third moment and compressed lift; it is not fourth-order non-closure or a finite-hierarchy no-go theorem.” |
| 一般 centered \(\kappa_s\) 的完整四阶索引账本没有在本节声明；有限证书只核对一个选定系数。 | “A complete fourth-order index ledger for the general centered \(\kappa_s\) is not claimed in this release; the finite certificate checks only one selected coefficient.” |
| 四站点证书证明选定 cumulant-flux 系数为 \(O(s^2)\)，选定完整压力系数为 \(O(s)\)，因此该系数级吸收至少损失 \(s^{-1}\)。 | “The four-site certificate proves that the selected cumulant-flux coefficient is \(O(s^2)\) while the selected complete pressure coefficient is \(O(s)\), so this coefficient-level absorption loses at least \(s^{-1}\).” |
| 这个 \(s^{-1}\) 结论不是全场范数下界，也不是所有闭合方案的普适代价。 | “This \(s^{-1}\) conclusion is neither a whole-field norm lower bound nor a universal cost for all closure schemes.” |
| 六站点结果是同输出系数见证，不是两个完整 \(\kappa_s\) 场相同而压力源不同的 collision。 | “The six-site result is a same-output coefficient witness, not a collision between two identical full \(\kappa_s\) fields with different pressure sources.” |
| 非零四次 remainder 证明选定三阶时间方程进入下一阶，不证明四阶数据本身不能闭合。 | “The nonzero quartic remainder proves that the selected third-level time equation enters the next order; it does not prove that fourth-order data themselves cannot close.” |
| 有限证书是光滑三角多项式上的精确 Fourier 代数，不是 Navier--Stokes 轨道、奇性或仿真。 | “The finite certificate is exact Fourier algebra on smooth trigonometric polynomials; it is not a Navier--Stokes trajectory, singularity, or simulation.” |
| 限定式检索没有找到相同打包，但未检出不是新颖性、优先权、不存在或第一性证明。 | “The bounded search did not locate an identical package, but non-detection is not proof of novelty, priority, non-existence, or first authorship.” |
| 普通中英翻译在本机直接完成，不调用 DGX。 | “Ordinary Chinese--English translation is performed directly on the local workstation; DGX is not used.” |
| 任意三维初值的全局正则性与 Clay 千禧年问题仍然开放。 | “Global regularity for arbitrary three-dimensional data and the Clay Millennium problem remain open.” |

## 6. Machine-readable release boundary

```text
problemFreeze=COMPLETE
parentAnalyticDerivation=COMPLETE
independentAnalyticAudit=PASS
primaryLiteratureAudit=BOUNDED_COMPLETE
pressureAwareSignedHeatLift=INTERNAL_EXACT_AUDITED
signedCrossCovarianceScalePDE=INTERNAL_EXACT_AUDITED
tensorHeatPlaneOddSlot=INTERNAL_EXACT_AUDITED
germanoStressEquation=VERIFIED_CLASSICAL_INDEX_AUDITED
kappaOnlyCompleteStressInterface=FALSE_AS_TRUNCATED_EQUATION
conditionalKappaCriticalRow=INTERNAL_CONDITIONAL_AUDITED
conditionalPressureVelocityCriticalRow=INTERNAL_CONDITIONAL_AUDITED
pressureStrainCriticalRow=OPEN
scalarTraceEquation=INTERNAL_EXACT_AUDITED
conditionalScalarFluxRow=INTERNAL_CONDITIONAL_AUDITED
signedProductionEnergyControl=OPEN
rawAndCompressedThreeToFour=INTERNAL_EXACT_AUDITED
generalCenteredKappaFourthOrderLedger=NOT_CLAIMED
bottomScaleOrderSeparation=INTERNAL_EXACT_AUDITED
fourSiteCoefficientOrderSeparation=INTERNAL_EXACT_FINITE_SEALED
sixSiteSameOutputPressureWitness=INTERNAL_EXACT_FINITE_SEALED
selectedQuarticNextLevelRemainder=INTERNAL_EXACT_FINITE_SEALED
formalFiniteCertificate=PASS
formalFiniteCertificateChecks=66
analyticSourceCommit=25636c886f1ee2449418b5548b42f9f0fa269b47
certificateSourceCommit=7c445c522a241bdc8b867b6fce0f0fed9b82e97d
finitePackageCommit=b34d91ea96c257b943f11d134e8024138e5f3cb0
finalSeal=TRUE
formalFigurePackage=PASS
formalFigureChecks=147
formalFigureRows=158
figureSourceCommit=f94915332ff405ae723711e8041acc2af07e896b
figurePackageCommit=ae679d5afa5f3cfacfe79c4d7b8a462baca2c195
publicReleaseTransaction=PENDING
signedLiftInformationTheoreticMinimality=NOT_ESTABLISHED
signedLiftComponentwiseMinimality=NOT_ESTABLISHED
signedLiftUniqueness=NOT_ESTABLISHED
fullThirdCumulantStateNonAutonomy=NOT_ESTABLISHED
wholeFieldKappaCollision=NOT_ESTABLISHED
fourthOrderNonClosure=NOT_ESTABLISHED
finiteMomentHierarchyNoGo=NOT_ESTABLISHED
navierStokesSimulation=NOT_RUN
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=FALSE
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```

## 7. Forbidden public wording and required replacement

| Forbidden or misleading wording | Required replacement |
|---|---|
| “the minimal signed lift” | “the equation-slot-compressed pressure-aware lift chosen for the quadratic tensor equation” |
| “\(\chi_s\) is the unique third-order state” | “\(\chi_s\) is one exact compressed representation; the Germano bundle is a transparent exact representation” |
| “the scale PDE closes the dynamics” | “the exact scale PDE is downward triangular in the filter variable and is not a physical-time closure” |
| “the full tensor hierarchy is now closed” | “the odd cubic slot is represented exactly, while \(G_s\), derivative pressure rows, and the next physical-time level remain” |
| “\(\kappa_s\) closes the stress equation” | “a \(\kappa_s\)-only equation omits the exact \(Q_s\) and \(R_s\) pressure rows” |
| “pressure cannot be recovered from \(\kappa_s\)” | “the selected local-cumulant row does not supply the complete same-output pressure forcing” |
| “a whole-field collision” | “a same-output coefficient witness,” unless an actual equality-state collision is later certified |
| “an unconditional critical cubic estimate” | “a critical \(\kappa,Q\) row conditional on \(u\in L_t^4L_x^6\)” |
| “the trace equation removes pressure” | “the trace cancels pressure--strain, while pressure--velocity remains in the flux \(J_s\)” |
| “the trace equation is a new regularity criterion” | “the trace equation is an exact scalar interface with signed production still open” |
| “the third-order state is non-autonomous” | “the displayed raw and compressed third-level observables have explicit quartic terms in their time equations” |
| “fourth-order non-closure” | “a nonzero quartic next-level remainder for the selected third-level observable” |
| “no finite hierarchy can close” | “no universal finite-hierarchy conclusion is established” |
| “universal \(s^{-1}\) lower bound” | “an \(s^{-1}\) coefficient-level absorption cost for the certified four-site rows” |
| “a six-mode turbulence simulation” | “an exact six-site Fourier coefficient diagnostic on a smooth planar field” |
| “no prior work exists” | “no identical package was located in the bounded search” |
| “R0.73V solves or nearly solves Navier--Stokes” | “R0.73V identifies an exact signed third-order interface and a precise remaining scalar obstruction; arbitrary-data global regularity remains open” |
| “translation was run on DGX” | “ordinary translation was performed directly on the local workstation” |

## 8. Mandatory English boundary paragraph

Use this paragraph without strengthening its verbs:

> R0.73V gives an exact scale-generation law for an equation-slot-compressed,
> pressure-aware signed third-order lift and verifies the complete Germano
> stress ledger for the heat filter. The critical \(\kappa_s\), \(Q_s\), and
> traced-flux rows remain conditional on the classical \(L_t^4L_x^6\) strong
> norm. Exact finite Fourier coefficients separate an \(O(s^2)\) velocity
> cumulant flux from an \(O(s)\) pressure source and exhibit one nonzero
> quartic next-level remainder, but they do not establish a whole-field
> collision, fourth-order non-closure, or a finite-hierarchy no-go theorem.
> The trace equation still contains the sign-indefinite production
> \(-\tau_s:\nabla v_s\). Arbitrary-data three-dimensional global regularity
> and the Clay Millennium problem remain open.

## 9. Literature-attribution phrases

| Topic | Required attribution boundary |
|---|---|
| Complete filtered stress hierarchy | Attribute the generalized-central-moment stress and trace equations to Germano (1992); describe R0.73V as a heat-filter specialization, sign/index audit, and local conditional norm bookkeeping. |
| Two-point and structure-function hierarchy | Attribute the classical two-point hierarchy to von K\'arm\'an--Howarth (1938) and arbitrary-order exact structure-function equations to Hill (2001); state that these are not the deterministic local heat cumulants. |
| Exact signed subgrid transfer | Cite Eyink (1996, 2006) for exact flux/locality and multiscale-gradient context under stated assumptions. |
| Local cubic defect | Cite Duchon--Robert (2000) as classical context for signed cubic transfer, not as the source of the R0.73V heat-cumulant PDE or finite witness. |
| Contemporary two-point closure | Describe Zambrano--Duraisamy (2026) as a model-based closure under homogeneous-isotropic and additional modeling assumptions, not a deterministic general-3D closure theorem. |
| Ensemble and moment chains | Describe LMN and Fursikov as higher-order ensemble/moment hierarchies, not finite deterministic local heat closures. |
| Third heat-cumulant scale PDE | Call it an internal exact audited derivation. The bounded search did not locate the same formula, but no novelty or priority claim follows. |
| Negative search result | Use “not located in the bounded search,” never “absent from the literature.” |

## 10. Public one-sentence boundary

**Chinese:** R0.73V 为一个压力感知、方程槽压缩的有符号三阶提升给出精确
heat 尺度生成律，并在完整 Germano 账本中找到可消去 pressure--strain 的
trace 投影；但临界通量估计仍以 \(L_t^4L_x^6\) 为前提，带符号 production
\(-\tau_s:\nabla v_s\) 仍未控制，而有限证书只证明选定系数的
\(O(s^2)\) 对 \(O(s)\) 分离和一个非零四次 remainder，所以任意三维
初值全局正则性与 Clay 问题仍然开放。

**English:** R0.73V gives an exact heat-scale generation law for a
pressure-aware, equation-slot-compressed signed third-order lift and identifies
a trace projection of the complete Germano ledger in which pressure--strain
cancels; however, the critical flux estimates still assume
\(L_t^4L_x^6\), the signed production \(-\tau_s:\nabla v_s\) remains
uncontrolled, and the finite certificate proves only selected-coefficient
\(O(s^2)\)-versus-\(O(s)\) separation and one nonzero quartic remainder, so
arbitrary-data three-dimensional global regularity and the Clay problem remain
open.
