# R0.73T bilingual dictionary and public-claim boundary

**Status:** canonical titles, terminology, sentence pairs, claim-state tokens,
the local-direct translation route, and the immutable source/artifact bindings
are frozen; public HTML/PDF rendering and deployment have not yet been completed

**Release title:** R0.73T | Dynamic autocorrelation and the pressure-tensor barrier

**Public title (zh):** R0.73T｜自相关进入动力学：一个临界一侧估计与压力张量障碍

**Canonical deck (zh):** 静态自相关证书已经进入动力学，但临界的
\(A\) 预算、压力张量和带符号通量仍未闭合。

**Canonical deck (en):** The static autocorrelation certificate has entered
the dynamics, but the critical \(A\) budget, the pressure tensor, and the signed
flux remain unclosed.

**Next release:** R0.73U

**Source commit:** `05c55d21f060a17a0a4db04c12e89e7271b03d30`

**Scientific artifact commit:** `29d01625731d1c611f927c2852dbddf05967c6cb`

**Figure metadata reseal commit:** `b17c45013cc9a3f6f09efa146bcbc2ef8ab043f9`

The later commit is a metadata-only reseal. It records the log-derived wall
time and bracketed same-host OS/CPU/memory fields; the exact data, validation,
PDF, SVG, and PNG remain byte-identical to the scientific-artifact commit.

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

The translation path above is a release constraint. It does not assert that
translation, HTML generation, deployment, or public readback has already been
completed. Ordinary Chinese--English translation must be performed directly on
the local workstation; DGX and external translation services are not used.

## Canonical section headings

| 中文标题 | English heading |
|---|---|
| 直接结论 | Main result at a glance |
| 精确自相关演化 | Exact autocorrelation evolution |
| 一侧动态估计 | The one-sided dynamic estimate |
| 为什么这还不是新的正则性门槛 | Why this is not a new regularity threshold |
| 两个精确非自治见证 | Two exact non-autonomy witnesses |
| 逐壳输运与 heat 版本 | Shellwise transport and the heat formulation |
| 文献归属、精确证书与声明边界 | Literature attribution, exact certificates, and claim boundaries |
| 研究价值与下一步 | Research value and the next step |

Do not translate “heat” as thermodynamic heat in this release. It denotes the
heat semigroup or heat-flow parameter used in the analytic construction.

## Mathematical terms

| 中文 | English |
|---|---|
| 动态自相关 | dynamic autocorrelation |
| 能量密度自相关 | energy-density autocorrelation |
| 二次自相关证书 | quadratic-autocorrelation certificate |
| 标量自相关 | scalar autocorrelation |
| 完整标量自相关 | complete scalar autocorrelation |
| 无权标量自相关 | unweighted scalar autocorrelation |
| 自相关动力学 | autocorrelation dynamics |
| 自相关系数 | autocorrelation coefficient |
| 自相关支撑 | autocorrelation support |
| 自治变量 | autonomous state variable |
| 非自治 | non-autonomy |
| 非自治见证 | non-autonomy witness |
| 一侧动态估计 | one-sided dynamic estimate |
| 临界一侧估计 | critical one-sided estimate |
| 动态 \(AQ\) 上界 | dynamic \(AQ\) upper inequality |
| 四次能量平衡 | quartic-energy balance |
| 经典 \(L^4\) 平衡 | classical \(L^4\) balance |
| 能量密度方程 | local energy-density equation |
| 压力张量障碍 | pressure-tensor barrier |
| 压力极化 | pressure polarization |
| 张量极化 | tensor polarization |
| 压力配对中的带符号速度相位 | signed velocity phase in the pressure pairing |
| 带符号速度相位不可辨识性 | signed-velocity-phase non-identifiability |
| 梯度相关 | gradient correlation |
| 带频率权重的梯度相关 | frequency-weighted gradient correlation |
| 三次压力通量 | cubic pressure flux |
| 带符号向量通量 \(u(\lvert u\rvert^2+2p)\) | signed vector flux \(u(\lvert u\rvert^2+2p)\) |
| 绝对载频 | absolute carrier frequency |
| 载频信息 | carrier-frequency information |
| 载频非自治 | carrier-scale non-autonomy |
| 临界预算 | critical budget |
| 临界积分 | critical integral |
| 经典 LPS 门槛 | classical LPS threshold |
| 空间 \(L^\infty\) 临界等式端 | spatial-\(L^\infty\) critical-equality end |
| 上 Dini 导数 | upper Dini derivative |
| 导数加权 Wiener 范数 | derivative-weighted Wiener norm |
| 分辨率一致的局部估计 | resolution-uniform local estimate |
| 两侧／绝对值 no-go | two-sided/absolute-value no-go |
| 固定摘要 | fixed summary statistics |
| 光滑三角多项式 | smooth trigonometric polynomial |
| 固定宽比环带 | fixed-ratio annulus |
| 精确有限证书 | exact finite certificate |
| 有理数稀疏卷积 | exact rational sparse convolution |
| 逐壳输运 | shellwise transport |
| 精确逐壳平衡 | exact shell balance |
| 壳层强制性 | shell coercivity |
| 周期频率局部化 nonlinear Bernstein 不等式 | periodic frequency-localized nonlinear Bernstein inequality |
| 标量定理逐分量向量适配 | componentwise vector adaptation of the scalar theorem |
| 固定投影支撑 | fixed projection support |
| 固定投影支撑差集 | fixed projection-support difference set |
| 瞬时活动支撑 | instantaneous active support |
| 壳外强迫 | off-shell forcing |
| 壳通量 | shell flux |
| Duhamel 形式 | Duhamel form |
| 经典强范数分支 | classical strong-norm branch |
| 能量唯一分支 | energy-only branch |
| 循环估计 | circular estimate |
| 超临界高频代价 | supercritical high-frequency cost |
| heat 半群 | heat semigroup |
| heat 权重 | heat weighting |
| heat 权重后的带符号向量通量缺口 | signed-vector-flux gap after heat weighting |
| heat-plane 恒等式 | heat-plane identity |
| 双线性 heat commutator | bilinear heat commutator |
| 带符号 heat commutator | signed heat commutator |
| 张量 heat hierarchy | tensor heat hierarchy |
| 抛物尺度感知 | parabolic-scale-aware |
| 经典直接碰撞 | direct classical collision |
| 公式层直接碰撞 | direct formula-level collision |
| 限定式碰撞检索 | bounded collision search |
| 可审计的本地综合 | local auditable synthesis |
| 任意初值全局正则性 | arbitrary-data global regularity |
| Clay 结论 | Clay conclusion |

## Canonical notation and exponent conventions

These expressions must be carried into the English HTML without changing
normalization, factors, signs, or the meaning of the norms.

| Symbol | Frozen meaning |
|---|---|
| \(w=\lvert u\rvert^2\) | scalar energy density |
| \(C_h=\widehat w(h)=\widehat{\lvert u\rvert^2}(h)\) | Fourier coefficient of the energy density; equivalently the shifted Fourier autocorrelation of \(u\) |
| \(Q=\sum_h\lvert C_h\rvert^2=\lVert u\rVert_4^4\) | quartic energy |
| \(A=\sum_h\lvert C_h\rvert\) | Wiener norm of the energy density, not the Wiener norm of the velocity |
| \(X^2=\lVert\nabla w\rVert_2^2\) | squared gradient norm of the energy density |
| \(Y=\int w\lvert\nabla u\rvert^2\) | weighted velocity-gradient dissipation |
| \(T_{ij}(h)=\widehat{u_i u_j}(h)\) | tensor correlation proposed for the next gate |
| \(v_j=P_ju\) | fixed Littlewood--Paley shell projection |
| \(\mathcal F_j=P_j\mathbb P\nabla\!\cdot(u\otimes u)\) | full projected nonlinear forcing of the shell |
| \(\overline D_j=\lvert\Sigma_j-\Sigma_j\rvert\) | fixed projection-support difference count, not an instantaneous active-support count |

The public copy must avoid an ambiguous \((p,q)\) convention. Write
“time exponent \(2\), space exponent \(\infty\)” or
\((p_x,q_t)=(\infty,2)\). The resulting condition is
\(u\in L_t^2L_x^\infty\). Never translate it as
\(u\in L_t^\infty L_x^2\), and never confuse it with the difficult
\(u\in L_t^\infty L_x^3\) endpoint.

## Frozen equation descriptions

| Equation or implication | Required English description |
|---|---|
| \(\dot C_h=-\nu\lvert h\rvert^2C_h-2\nu\widehat{\lvert\nabla u\rvert^2}(h)-ih\cdot\widehat{u(\lvert u\rvert^2+2p)}(h)\) | the exact, non-autonomous Fourier law for the energy-density autocorrelation |
| \(Q'+4\nu Y+2\nu X^2=4\int p\,u\cdot\nabla w\) | the classical quartic-energy balance reconstructed through autocorrelation |
| \(Q'+4\nu Y+\nu X^2\le4C_R^2\nu^{-1}AQ\) | the one-sided dynamic \(AQ\) inequality; an internal corollary of classical estimates and R0.73S |
| \(\int_0^TA(t)\,dt<\infty\Rightarrow u\in L_t^2L_x^\infty\) | the missing \(A\) budget has at least classical LPS strength; this implication is not a new criterion |
| \(\mathcal D_j\ge c_B2^{2j}Q_j\) | periodic scalar frequency-localized Bernstein applied componentwise to obtain the vector shell bound |
| \(D^+(Q_j^{1/2})+2\nu c_B2^{2j}Q_j^{1/2}\le2A_j^{1/2}F_j\) | conditional shellwise Duhamel transport with the full projected forcing left unclosed |
| \(F_j\lesssim2^j\lVert u\rVert_4^2\) or \(F_j\lesssim2^{5j/2}\lVert u\rVert_2^2\) | the first forcing branch is circular for the target; the energy-only branch is supercritical at high frequency |
| \((\partial_t-\nu\partial_s)\lVert v_s\rVert_4^4=-4\int\lvert v_s\rvert^2v_s\cdot e^{s\Delta}\mathbb P\nabla\!\cdot(u\otimes u)\) | the exact heat-plane identity; its signed bilinear commutator remains open |

The first coefficient law is classified as
`VERIFIED_CLASSICAL_RECONSTRUCTION`: it is the spatial Fourier transform of
the classical local-energy identity. Its literal \(C_h\) packaging is not a
basis for a novelty claim.

## Exact witness facts and allowed interpretation

The following numbers and signs are frozen. They must not be rounded,
rescaled silently, or translated into claims about singular behavior.

| Witness | Frozen exact fact | Allowed interpretation |
|---|---|---|
| Rotating shear \(v_N=(0,\cos Nx_1,\sin Nx_1)\) | At \(t=0\), \(\lvert v_N\rvert^2\equiv1\), \(C_h=\mathbf1_{h=0}\), \(A=Q=1\), while \(\dot C_0=-2\nu N^2\) and \(Q'=-4\nu N^2\) under heat evolution. | Complete unweighted scalar autocorrelation loses the carrier scale, already in a linear exact solution. |
| Six-mode signed pressure-pairing witness | \(\mathcal E=42\), \(Q=2918\), \(A=164\), \(D_C=15\), \(X^2=4296\), \(Y=1986\), and \(\mathcal N_4=-384\) | An exact finite evaluation of a nonzero pressure pairing, not by itself a witness that the quadratic tensor \(u\otimes u\) or reconstructed pressure \(p\) differs. It is not a simulation or singular solution. |
| Dilated sign pair \(u_L,-u_L\) | The complete scalar \(C\), the tensor \(u\otimes u\), and the reconstructed pressure \(p\) are identical; the pressure work is \(\mp384L\), while the common viscous term scales as \(-16536\nu L^2\). | The shared pressure is paired with a sign-reversed velocity, so the certificate isolates the signed velocity phase entering the pressure pairing. It does not exhibit different pressures or different quadratic tensors, and it does not contradict the one-sided upper bound. |
| Fixed-summary shear | At the initial evaluation time, \((\mathcal E,Q,A,D_C)=(1/2,3/8,1,3)\) and \(\lvert Q'\rvert=(3/2)\nu L^2\). | No finite two-sided/absolute-value bound follows from those fixed summaries; the one-sided estimate remains valid. |
| Heat-weighted sign pair | The signed separation is \(-768Le^{-8\tau L^2}\). | Heat weighting restores scale sensitivity, but the scalar heat-weighted state still does not close the signed vector flux. The sign pair has the same pressure and tensor, and the statement is not a closed heat hierarchy. |

## Mandatory bilingual boundary sentences

The English sentences in this section are release-locked and should be used
verbatim, or checked sentence by sentence if line wrapping changes.

| 中文冻结句 | Mandatory English sentence |
|---|---|
| 这条 \(AQ\) 不等式把 R0.73S 的静态证书接入了动力学，但没有控制临界积分 \(\int A\,dt\)。 | “The dynamic \(AQ\) inequality brings the static R0.73S certificate into the dynamics, but it does not control the critical integral \(\int A\,dt\).” |
| 因为 \(\lVert u\rVert_\infty^2\le A\)，所以 \(A\in L_t^1\) 直接蕴含 \(u\in L_t^2L_x^\infty\)。 | “Because \(\lVert u\rVert_\infty^2\le A\), the condition \(A\in L_t^1\) directly implies \(u\in L_t^2L_x^\infty\).” |
| 这是经典 LPS 缩放线的空间 \(L^\infty\) 临界等式端，不是困难的 \(L_t^\infty L_x^3\) 端点。 | “This is the spatial-\(L^\infty\) critical-equality end of the classical LPS line, not the difficult \(L_t^\infty L_x^3\) endpoint.” |
| 完整标量自相关不是自治状态：一般 \(C_h\) 方程仍含有不能由 \(C\) 确定的带符号向量通量 \(\widehat{u(\lvert u\rvert^2+2p)}\)，而重建 \(p\) 需要张量 \(\widehat{u_i u_j}\)，不只是其迹 \(C\)。 | “The complete scalar autocorrelation is not an autonomous state: the general \(C_h\) law still contains the signed vector flux \(\widehat{u(\lvert u\rvert^2+2p)}\), which is not determined by \(C\), while reconstructing \(p\) requires the tensor \(\widehat{u_i u_j}\), not only its trace \(C\).” |
| \(u_L\) 与 \(-u_L\) 有相同的 \(u\otimes u\) 和相同的 \(p\)；这个符号对隔离的是进入压力配对的带符号速度相位，不能作为 \(p\) 或二次张量 \(u\otimes u\) 不同的见证。 | “The pair \(u_L,-u_L\) has the same \(u\otimes u\) and the same \(p\); it isolates the signed velocity phase entering the pressure pairing and is not a witness that \(p\) or the quadratic tensor \(u\otimes u\) differs.” |
| 精确 \(C_h\) 方程是经典局部能量恒等式的 Fourier 重建，不是新的动力学定理。 | “The exact \(C_h\) equation is a Fourier reconstruction of the classical local-energy identity, not a new dynamical theorem.” |
| Tran--Yu--Dritschel 2021 是经典 \(L^4\) 平衡与压力相关机制的直接公式层碰撞。 | “Tran--Yu--Dritschel (2021) is a direct formula-level collision for the classical \(L^4\) balance and its pressure-correlation mechanism.” |
| Li--Sire 2023 的 Theorem 4.2 是标量定理；这里的向量壳层强制性来自逐分量适配。 | “Li--Sire's Theorem 4.2 is scalar; the vector shell coercivity used here follows by a componentwise adaptation.” |
| 两个见证都是光滑三角多项式；它们不是奇性、近奇性、爆破解或 Navier--Stokes 全局正则性反例。 | “Both witnesses are smooth trigonometric polynomials; they are not singular, near-singular, blow-up solutions, or counterexamples to Navier--Stokes global regularity.” |
| 一侧 \(AQ\) 上界与两侧／绝对值 no-go 相容，二者必须同时陈述。 | “The one-sided \(AQ\) upper bound and the two-sided/absolute-value no-go are compatible and must be stated together.” |
| 分辨率一致的比较 ODE 只给局部控制；该 ODE 本身允许有限时爆破，因而不能推出全局正则性。 | “The resolution-uniform comparison ODE provides local control only; the ODE itself permits finite-time blow-up and therefore cannot imply global regularity.” |
| 逐壳估计仍留下完整投影非线性强迫；一个分支循环，另一个分支在高频超临界。 | “The shellwise estimate still leaves the full projected nonlinear forcing unclosed: one branch is circular, while the other is supercritical at high frequency.” |
| heat 权重恢复了尺度敏感性，但标量 heat 状态仍不能闭合 \(u(\lvert u\rvert^2+2p)\) 的带符号向量通量。 | “Heat weighting restores scale sensitivity, but the scalar heat state still does not close the signed vector flux \(u(\lvert u\rvert^2+2p)\).” |
| 固定投影支撑差集可以穿过壳层零点；瞬时活动支撑数不能替代它。 | “The fixed projection-support difference set remains valid through shell zero crossings; an instantaneous active-support count cannot replace it.” |
| 有限证书只是精确稀疏卷积诊断；它不是 Navier--Stokes 仿真，也不认证连续 PDE 证明。 | “The finite certificate is an exact sparse-convolution diagnostic; it is not a Navier--Stokes simulation and does not certify the continuum PDE proof.” |
| 限定式碰撞检索没有找到相同打包，但未检出不是新颖性、优先权或不存在证明。 | “The bounded collision search did not locate an identical package, but non-detection is not proof of novelty, priority, or non-existence.” |
| 本站只把这一节称为可审计的本地综合。 | “This release is described only as a local auditable synthesis.” |
| 任意三维初值的全局正则性与 Clay 千禧年问题仍然开放。 | “Global regularity for arbitrary three-dimensional data and the Clay Millennium problem remain open.” |

## Mandatory English boundary paragraph

Use this paragraph without strengthening its verbs:

> The dynamic \(AQ\) inequality is a local synthesis of classical pressure,
> \(L^4\)-energy, and autocorrelation estimates. It is not asserted as a new
> regularity criterion or a priority theorem. The exact scalar autocorrelation
> law remains non-autonomous, and the unresolved step is a scale-aware tensor
> closure with a controllable signed flux. Global regularity for arbitrary
> three-dimensional data and the Clay Millennium problem remain open.

## Literature-attribution phrases

| Topic | Required attribution boundary |
|---|---|
| Exact \(L^4\) and pressure mechanism | Attribute the direct formula-level collision to Tran--Yu--Dritschel (2021), DOI `10.1017/jfm.2020.1033`. |
| Periodic nonlinear Bernstein | Attribute the scalar frequency-localized theorem to Li--Sire (2023), DOI `10.1090/tran/8708`; state separately that the vector conclusion is componentwise. |
| Classical space--time regularity | Say “the classical LPS line” and state the time and space exponents explicitly; do not attribute every modern endpoint formulation verbatim to Serrin 1962. |
| Velocity Wiener/Gevrey near-neighbour | Ambrose--Lopes Filho--Nussenzveig Lopes (2024), DOI `10.1090/proc/16615`, controls velocity Fourier/Wiener quantities, not the energy-density state \(C_h\). |
| Negative collision search | Use “not located in the bounded search,” never “does not exist in the literature.” |

## Forbidden public wording and required replacement

| Forbidden or misleading wording | Required replacement |
|---|---|
| “a new Navier--Stokes regularity criterion” | “an internal one-sided corollary whose missing \(A\) budget already has classical LPS strength” |
| “a closed equation for \(C_h\)” | “an exact non-autonomous equation involving gradient correlation and cubic pressure flux” |
| “Li--Sire's vector theorem” | “the scalar Li--Sire theorem followed by a componentwise vector adaptation” |
| “the Serrin endpoint” without exponents | “the time-2, space-\(\infty\) critical-equality end of the classical LPS line” |
| “the shell autocorrelation proves full regularity” | “a single shell estimate is conditional and does not control the full velocity” |
| “the finite certificate is a Navier--Stokes simulation” | “the finite certificate is an exact sparse-convolution diagnostic” |
| “the witnesses show blow-up” | “the witnesses show carrier-scale non-autonomy and signed-velocity-phase non-identifiability in the pressure pairing” |
| “the sign pair has different pressure polarization” | “the sign pair has the same \(u\otimes u\) and the same \(p\); only the signed velocity phase entering the pressure pairing is reversed” |
| “heat weighting does not restore scalar pressure polarization” | “the scalar heat-weighted state still does not close the signed vector flux” |
| “no prior work exists” | “no identical package was located in the bounded search” |
| “R0.73T advances the Clay problem by a measurable percentage” | “R0.73T isolates the precise tensor and signed-flux obstruction; the Clay problem remains open” |
| “R0.73U will close the problem” | “R0.73U tests a specific tensor heat-hierarchy gate” |

## R0.73U next-gate wording

**Frozen question (zh):** 能否构造一个保留压力极化、具有抛物尺度感知的
张量 heat hierarchy，并在不超出 R0.73Q/R0.73R 临界指数的前提下，
得到可被耗散吸收的带符号 heat commutator 或壳通量估计？

**Frozen question (en):** Can one construct a tensor heat hierarchy that
retains pressure polarization, is parabolic-scale-aware, and yields a
signed heat-commutator or shell-flux estimate absorbable by dissipation without
exceeding the critical exponents of R0.73Q/R0.73R?

**Short gate label (zh):** 张量极化 heat hierarchy 与临界带符号通量

**Short gate label (en):** tensor-polarized heat hierarchy and critical signed flux

R0.73U is a frozen research question, not a theorem, scheduled result, or
promise of closure.

## Human translation QA checklist for the HTML release

1. The English and Chinese titles exactly match the frozen strings above.
2. Every occurrence of \(A\) says or clearly implies that it is the Wiener norm
   of the energy density, not of the velocity.
3. The coefficient law is labeled a classical Fourier reconstruction; the
   one-sided \(AQ\) inequality is labeled an internal corollary.
4. The time exponent is \(2\), the space exponent is \(\infty\), and the copy
   never swaps \(L_t^2L_x^\infty\) with another mixed norm.
5. “One-sided upper bound” is never shortened to “bound” where a reader could
   infer a two-sided or absolute-value estimate.
6. The carrier-scale witness and the signed-velocity-phase witness are called
   smooth exact witnesses, never simulations, singular solutions, or blow-up
   examples.  The sign pair is stated to have the same \(u\otimes u\) and the
   same reconstructed pressure \(p\).
7. The Li--Sire attribution remains scalar, and the componentwise vector step
   is visible in the prose or a nearby note.
8. The shell forcing remains \(P_j\mathbb P\nabla\cdot(u\otimes u)\); it is not
   mistranslated as shell self-advection.
9. The fixed support-difference count \(\overline D_j\) is not replaced by an
   instantaneous active-support count at shell zero crossings.
10. The heat-plane object is a semigroup/commutator construction, not a
    thermodynamic heat equation.
11. Classical, internal, exact finite, conditional, and open statements retain
    their separate evidence labels.
12. The bounded-search sentence includes the non-novelty caveat in both
    languages.
13. The final paragraph states that arbitrary-data three-dimensional global
    regularity and the Clay conclusion remain open.
14. R0.73U appears only as the next research gate, using the frozen question.
15. Translation and deployment status are not inferred from the existence of
    this dictionary.

## Machine-readable release boundary

```text
releaseId=R0.73T
nextRelease=R0.73U
bilingualDictionary=FROZEN
sourceCommitAssigned=TRUE
sourceCommit=05c55d21f060a17a0a4db04c12e89e7271b03d30
generatedArtifactCommitAssigned=TRUE
generatedArtifactCommitAlias=scientificArtifactCommit
scientificArtifactCommit=29d01625731d1c611f927c2852dbddf05967c6cb
figureMetadataResealCommit=b17c45013cc9a3f6f09efa146bcbc2ef8ab043f9
figureMetadataResealScope=ENVIRONMENT_MANIFEST_SUMS_ONLY
figureMetadataBackfill=SAME_HOST_BRACKETED_NOT_ORIGINAL_RUN_EMISSION
originalFormalFigureManifestSha256=29d34366e2715819e08f1c6f1dc77bff5fcb089a2e2c2e6ce33616825fccae1d
currentFormalFigureManifestSha256=bfa5c468ecb43a287239fd5e368c66d0eefad6ffe09dff241e828e806279a10e
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
translationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=FALSE
externalTranslationServiceUsed=FALSE
publicHtmlRendered=FALSE
publicDeploymentCompleted=FALSE
publicReleaseContent=SOURCE_AND_ARTIFACT_BINDINGS_FROZEN
exactAutocorrelationEvolution=VERIFIED_CLASSICAL_RECONSTRUCTION
quarticBalance=VERIFIED_CLASSICAL_RECONSTRUCTION
dynamicAQUpperInequality=INTERNAL_COROLLARY
criticalAIntegral=INTERNAL_EXACT_SCALING
criticalAIntegralControl=OPEN
AIntegralImpliesLt2LxInfinity=VERIFIED_CLASSICAL
carrierScaleNonAutonomy=CLOSED_EXACT
signPairTensorAndPressureIdentical=CLOSED_EXACT
signedVelocityPhaseInPressurePairingNonIdentifiability=CLOSED_EXACT
generalCoefficientLawContainsSignedVectorFlux=VERIFIED_CLASSICAL_RECONSTRUCTION
scalarStateSignedVectorFluxClosure=OPEN
pressureReconstructionRequiresTensor=VERIFIED_CLASSICAL
absoluteTwoSidedQPrimeNoGo=CLOSED_EXACT
scalarFrequencyLocalizedBernstein=VERIFIED_CLASSICAL
vectorShellCoercivity=VERIFIED_CLASSICAL_WITH_ADAPTATION
shellDuhamelTransport=INTERNAL_CONDITIONAL
fixedProjectionSupportDifferenceCount=REQUIRED
instantaneousActiveSupportAtZeroCrossing=FORBIDDEN
heatPlaneIdentity=INTERNAL_EXACT
heatWeightedScalarSignedVectorFluxClosure=OPEN
signedShellFluxClosure=OPEN
tensorHeatClosure=OPEN
nextGateR073U=OPEN
finiteFormulaCertificateOnly=TRUE
finiteFormulaDiagnosticValidation=PASS
finiteFormulaDiagnosticChecks=55
formalFigurePackage=PASS
formalFigureChecks=106
formalFigureRows=28
finalSeal=TRUE
navierStokesSimulation=NOT_RUN
finiteFormulaDiagnosticIsNavierStokesSimulation=FALSE
finiteFormulaDiagnosticCertifiesContinuumPdeProof=FALSE
finiteWitnessImpliesSingularity=FALSE
boundedSearchProvesAbsence=FALSE
noveltyOrPriorityClaim=FORBIDDEN
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
NOT CLAY
```
