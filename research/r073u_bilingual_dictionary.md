# R0.73U bilingual dictionary and public-claim boundary

**Status:** canonical terminology, exact-certificate final seal, formal-figure
QA, immutable source pins, and the local-direct translation route are frozen;
HTML/PDF rendering and public deployment remain separate gates

**Release title:** R0.73U | Full tensors in the heat hierarchy: pressure is
recoverable, but the even quadratic state is not dynamically closed

**Public title (zh):** R0.73U｜完整张量进入热层级：压力可以恢复，但偶二次状态的动力学并不闭合

**Next release:** R0.73V

**Analytic source commit:** `84e808dae473f6381cbf9df55a71f5fe81a1cfce`

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

Ordinary Chinese--English translation for this release is performed directly
on the local workstation.  DGX and external translation services are not
used.  In Chinese copy, “heat” denotes the heat semigroup or its filter-scale
parameter; it must not be rendered as thermodynamic heat.

## 1. Canonical section headings

| 中文标题 | English heading |
|---|---|
| 直接结论 | Main result at a glance |
| 先区分两种完全不同的“张量相关” | First distinguish two different tensor correlations |
| heat covariance 的精确正结构 | The exact positive structure of heat covariance |
| 同尺度压力、filtered NSE 与有符号能量通量 | Same-scale pressure, filtered NSE, and signed energy flux |
| 两条临界 stress 估计 | Two critical stress estimates |
| 加权中心压力方差收紧 R0.73T | A centered weighted pressure variance sharpens R0.73T |
| 物理时间方程为何仍不闭合 | Why the physical-time equation remains unclosed |
| 四站点精确见证与 parabolic loss | The exact four-site witness and the parabolic loss |
| 文献归属、结果价值与下一步 | Literature attribution, research value, and the next step |

## 2. Mathematical terms

| 中文 | English | Required meaning |
|---|---|---|
| 局部乘积张量 | local product tensor | \(T^{\rm loc}_{ij}(h)=\widehat{u_i u_j}(h)\), containing cross-wave-number convolution data. Do not call it the two-point correlation tensor. |
| 完整局部二次张量 | full local quadratic tensor | The complete component array \(u_i u_j\), not only its trace \(|u|^2\). |
| 两点 K\'arm\'an--Howarth--Monin 张量 | two-point K\'arm\'an--Howarth--Monin tensor | \(R_{ij}(r)=\int u_i(x)u_j(x+r)d\mu(x)\), whose Fourier transform contains same-wave-number covariance. |
| 同波数协方差 | same-wave-number covariance | \(\widehat u_j(k)\overline{\widehat u_i(k)}\); distinct from the convolution defining \(\widehat{u_i u_j}(h)\). |
| 跨波数卷积 | cross-wave-number convolution | \(\sum_k\widehat u_i(k)\widehat u_j(h-k)\). |
| 张量极化 | tensor polarization | Component information in \(u_i u_j\) that is lost by the scalar trace. |
| 同尺度压力重建 | same-scale pressure reconstruction | \(p_s=R_iR_j\Theta_{s,ij}\) with the release's fixed Riesz sign convention. It is instantaneous sufficiency, not dynamic closure. |
| heat 滤波速度 | heat-filtered velocity | \(v_s=P_su\), a signed field. |
| heat 滤波局部乘积张量 | heat-filtered local product tensor | \(\Theta_s=P_s(u\otimes u)\), an even quadratic field. |
| heat 协方差／亚滤波应力 | heat covariance / subfilter stress | \(\tau_s=\Theta_s-v_s\otimes v_s\). It is PSD but not an eddy-viscosity model. |
| heat 协方差尺度方程 | heat-covariance scale equation | The exact PDE in the filter parameter \(s\), not a physical-time stress closure. |
| heat 半群两层恒等式 | two-level heat-semigroup identity | \(\tau_{s+r}(u)=P_r\tau_s(u)+\tau_r(P_su)\). It organizes scales without closing one-scale dynamics. |
| 对称正半定 | symmetric positive semidefinite | \(a^TAa\ge0\) for every real vector \(a\). It does not imply a signed energy flux. |
| 亚滤波能量通量 | subfilter energy flux | \(\Pi_s=-\tau_s:\nabla v_s\), a signed cubic quantity. |
| 精确滤波方程 | exact filtered equation | The Navier--Stokes equation after applying \(P_s\), with the exact unresolved stress retained. |
| 临界乘积空间 | critical product space | \(L_t^2L_x^3\), paired with \(E=L_t^4L_x^6\). “Critical” is local/Euclidean parabolic terminology, not literal fixed-torus dilation invariance. |
| 条件性临界张量行 | conditional critical tensor row | The uniform tensor bound that already assumes \(u\in L_t^4L_x^6\). |
| 固定正 heat 尺度 | fixed positive heat scale | A fixed \(s>0\); the energy-only estimate is finite there but is not uniform as \(s\downarrow0\). |
| 能量唯一估计 | energy-only estimate | A bound using the energy inequality rather than an assumed critical strong norm. |
| 短尺度 \(s^{-1/2}\) 损失 | short-scale \(s^{-1/2}\) loss | The explicit loss in the energy-only \(L_t^2L_x^3\) stress norm as \(s\downarrow0\). |
| 中心化压力均值 | centered weighted pressure mean | \(\bar p_w=(\int wp)/(\int w)\), with the zero solution handled separately. |
| 加权压力方差 | weighted pressure variance | \(\mathcal P_*=\int w(p-\bar p_w)^2d\mu\). |
| 中心化压力方差不等式 | centered pressure-variance inequality | The internal corollary obtained from the classical quartic balance, weighted Cauchy, and Young. |
| 公式层直接经典碰撞 | direct classical formula-level collision | Tran--Yu--Dritschel 2021 treats the closely related weighted pressure mechanism. The R0.73U centered form carries no novelty claim. |
| 张量 heat-plane 方程 | tensor heat-plane equation | The exact \((t,s)\) identity for \(\Theta_{s,ij}\), containing even gradient products and odd cubic/pressure--velocity terms. |
| 带符号三阶切向量 | signed third-order tangent | The odd physical-time tensor tangent that the even quadratic state cannot determine. |
| 偶二次 heat 状态 | even quadratic heat state | \(\mathcal H(u)=\{\Theta_s,\tau_s,p_s:s\ge0\}\); it deliberately excludes the signed velocity \(v_s\). |
| 单值自治演化律 | single-valued autonomous evolution law | A law that assigns the signed tensor tangent from the declared state alone. |
| 二次状态非自治 | quadratic-state non-autonomy | Failure of such a signed-tangent equality for the even quadratic state, not failure of every estimate or augmentation. |
| 四站点见证 | four-site witness | The real divergence-free trigonometric polynomial supported on two conjugate Fourier pairs. “Four-site” counts all positive and negative Fourier sites. |
| 精确稀疏 Fourier 卷积 | exact sparse-Fourier convolution | Finite algebra used to evaluate the witness; not a Navier--Stokes simulation. |
| 非线性张量切向量 | nonlinear tensor tangent | The matrix \(K\) at the selected Fourier coefficient, with the viscous coefficient separately verified to vanish. |
| 符号对 | sign pair | \(u\) and \(-u\), which share all even quadratic data and reverse odd tangent data. |
| 整数覆盖伸缩 | integer covering dilation | \(u_L(x)=u(Lx)\) on the normalized periodic torus. It is used for an exact coefficient calculation, not literal Euclidean norm invariance. |
| 抛物 heat 切片 | parabolic heat slice | \(s=\theta L^{-2}\) with fixed \(\theta>0\). |
| 一阶导数代价 | one-derivative cost | The factor proportional to \(L\), equivalently \(s^{-1/2}\), for the selected signed tensor coefficient at a parabolic slice. |
| 系数级分离 | coefficient-level separation | The Frobenius difference of one selected Fourier tensor tangent, not a universal norm lower bound. |
| 带符号增广 | signed augmentation | Adding \(v_s\), cubic moments, or another odd state; the R0.73U no-go does not exclude it. |
| 限定式碰撞检索 | bounded collision search | A scoped primary-source search. Non-detection does not establish novelty, priority, or non-existence. |
| 可审计的本地综合 | local auditable synthesis | The strongest permitted value label for the release. |
| 任意初值三维全局正则性 | arbitrary-data three-dimensional global regularity | Open. R0.73U does not establish it. |
| Clay 千禧年问题结论 | Clay Millennium conclusion | Open and expressly not claimed. |

## 3. Canonical notation

| Symbol | Frozen meaning |
|---|---|
| \(P_s=e^{s\Delta}\) | periodic heat semigroup |
| \(v_s=P_su\) | signed heat-filtered velocity |
| \(\Theta_s=P_s(u\otimes u)\) | heat-filtered local product tensor |
| \(\tau_s=\Theta_s-v_s\otimes v_s\) | heat covariance / exact subfilter stress |
| \(p_s=P_sp=R_iR_j\Theta_{s,ij}\) | mean-zero pressure at heat scale \(s\) |
| \(E(I)=L^4(I;L^6(\mathbb T^3))\) | critical strong velocity space used conditionally |
| \(\mathcal S_\nu F\) | causal periodic Stokes map from the R0.73Q interface |
| \(w=|u|^2\), \(Q=\int w^2\) | energy density and quartic energy |
| \(X^2=\int|\nabla w|^2\), \(Y=\int w|\nabla u|^2\) | quartic-balance dissipation quantities |
| \(\bar p_w=(\int wp)/(\int w)\) | weighted pressure mean, defined when \(u\not\equiv0\) |
| \(\mathcal P_*=\int w(p-\bar p_w)^2\) | centered weighted pressure variance |
| \(\beta_*=\mathcal P_*/Q\) | centered pressure-variance rate when \(Q>0\) |
| \(h_*=(1,2,0)\) | selected witness coefficient |
| \(K=\begin{psmallmatrix}-2&1&0\\1&0&0\\0&0&0\end{psmallmatrix}\) | selected nonlinear tensor tangent; \(|K|_F=\sqrt6\) |
| \(u_L(x)=u(Lx)\), \(h_L=(L,2L,0)\) | integer-dilated witness and selected coefficient |
| \(s=\theta L^{-2}\) | parabolic heat slice |

Tensor norms are Frobenius norms unless explicitly stated otherwise.  The
English HTML/PDF must preserve the time-space order in
\(L_t^4L_x^6\) and \(L_t^2L_x^3\).

## 4. Frozen equation descriptions

| Equation | Required English description |
|---|---|
| \((\partial_s-\Delta)\tau_s=2\sum_\ell\partial_\ell v_s\otimes\partial_\ell v_s\), \(\tau_0=0\) | the exact heat-covariance equation in the filter parameter, not a physical-time closure |
| \(p_s=R_iR_j\Theta_{s,ij}\) | same-scale instantaneous pressure reconstruction from the full local product tensor |
| \(\partial_tv_s+\mathbb P\nabla\cdot(v_s\otimes v_s+\tau_s)=\nu\Delta v_s\) | the exact filtered Navier--Stokes equation with unresolved stress retained |
| \(\sup_s\|\tau_s\|_{L_t^2L_x^3}\le\|u\|_{L_t^4L_x^6}^2\) | the conditional critical tensor row; its right-hand side already assumes the classical strong norm |
| \(\|\tau_s\|_{L_t^2L_x^3}\lesssim E_0(\nu s)^{-1/2}\) | the energy-only positive-scale bound with a non-uniform short-scale loss |
| \(Q'+4\nu Y+(2-\vartheta)\nu X^2\le4\mathcal P_*/(\vartheta\nu)\) | the centered pressure-variance corollary of the classical quartic balance |
| tensor equation (analytic proof (6.2); reader report (7.2)) | the exact tensor heat-plane law; its odd cubic and pressure--velocity terms remain unclosed by even quadratic data |
| \(\partial_t\widehat\Theta_s(h_*;u)-\partial_t\widehat\Theta_s(h_*;-u)=2e^{-5s}K\) | the exact four-site initial-time signed-tangent separation at the selected coefficient; not a trajectory symmetry |
| \(2\sqrt6Le^{-5\theta}=2\sqrt{6\theta}e^{-5\theta}s^{-1/2}\) | the coefficient-level one-derivative cost for the dilated witness at a fixed parabolic heat slice |

## 5. Mandatory bilingual boundary sentences

The English sentences below are release-locked.  They may be line-wrapped but
must not be strengthened.

| 中文冻结句 | Mandatory English sentence |
|---|---|
| R0.73U 的局部乘积张量 \(\widehat{u_i u_j}(h)\) 与经典两点 KHM 张量不是同一个对象：前者保留跨波数卷积，后者保留同波数协方差。 | “The R0.73U local product tensor \(\widehat{u_i u_j}(h)\) is not the classical two-point KHM tensor: the former retains cross-wave-number convolutions, while the latter retains same-wave-number covariance.” |
| 完整局部二次张量能够在同一 heat 尺度重建瞬时压力，但这不等于二次张量的物理时间动力学已经闭合。 | “The full local quadratic tensor reconstructs instantaneous pressure at the same heat scale, but this does not close its physical-time dynamics.” |
| heat 协方差在每一点对称正半定，并满足精确的尺度方程；这个方程沿滤波参数 \(s\) 演化，不是物理时间应力闭合。 | “The heat covariance is pointwise symmetric positive semidefinite and satisfies an exact scale equation; that equation evolves in the filter parameter \(s\), not as a physical-time stress closure.” |
| \(\tau_s\) 正半定并不使 \(-\tau_s:\nabla v_s\) 具有固定符号。 | “Positive semidefiniteness of \(\tau_s\) does not give the flux \(-\tau_s:\nabla v_s\) a fixed sign.” |
| 一致的 \(L_t^2L_x^3\) 张量估计已经假设 \(u\in L_t^4L_x^6\)，所以它对任意初值全局正则性是循环的。 | “The uniform \(L_t^2L_x^3\) tensor estimate already assumes \(u\in L_t^4L_x^6\), so it is circular for arbitrary-data global regularity.” |
| 只用能量时，固定 \(s>0\) 的应力估计是有限的，但在 \(s\downarrow0\) 时损失 \(s^{-1/2}\)，不能作为一致的零尺度控制。 | “Using energy alone, the stress estimate is finite at each fixed \(s>0\), but it loses \(s^{-1/2}\) as \(s\downarrow0\) and therefore is not uniform control at zero scale.” |
| 中心化压力方差可以改进局部右端，但它与 Tran--Yu--Dritschel 2021 的加权压力机制存在直接公式层经典碰撞，不能承载新颖性或优先权声明。 | “The centered pressure variance can sharpen the local right-hand side, but it has a direct classical formula-level collision with the weighted-pressure mechanism of Tran--Yu--Dritschel (2021) and cannot support a novelty or priority claim.” |
| 精确张量 heat-plane 方程仍含有带符号的三次速度项和压力--速度项。 | “The exact tensor heat-plane equation still contains signed cubic-velocity and pressure--velocity terms.” |
| 四站点符号对证明的只是偶二次 heat 状态不能单值确定带符号张量切向量。 | “The four-site sign pair proves only that the even quadratic heat state cannot determine the signed tensor tangent through a single-valued law.” |
| 这里比较的是 \(u\) 和 \(-u\) 作为同一时刻初值时的 Navier--Stokes 切向量，不是轨道对称性。 | “The comparison concerns Navier--Stokes tangents at the same initial time for \(u\) and \(-u\); it is not a trajectory symmetry.” |
| 一旦把带符号速度 \(v_s\) 或其他奇／三阶状态加入变量，这个二次状态 no-go 就不再适用。 | “Once the signed velocity \(v_s\) or another odd or third-order state is added, this quadratic-state no-go no longer applies.” |
| 该见证不排除一侧估计、绝对值估计、时间积分或其他抵消机制。 | “The witness does not exclude one-sided estimates, absolute-value estimates, time integration, or other cancellation mechanisms.” |
| 抛物切片上的 \(s^{-1/2}\) 分离只认证这个见证的选定 Fourier 系数需要一阶导数代价，不是对所有闭合方案的普适下界。 | “The \(s^{-1/2}\) separation at a parabolic slice certifies a one-derivative cost only for the selected Fourier coefficient of this witness; it is not a universal lower bound for all closure schemes.” |
| 四站点场是光滑、平面、散度为零的三角多项式；它不是奇性、近奇性、爆破解、涡伸展示例或 Navier--Stokes 仿真。 | “The four-site field is a smooth planar divergence-free trigonometric polynomial; it is not a singularity, near-singularity, blow-up solution, vortex-stretching example, or Navier--Stokes simulation.” |
| 有限证书只是精确稀疏卷积诊断；它不认证连续 PDE 证明。 | “The finite certificate is an exact sparse-convolution diagnostic; it does not certify the continuum PDE proof.” |
| 限定式碰撞检索没有找到相同打包，但未检出不是新颖性、优先权、不存在或第一性证明。 | “The bounded collision search did not locate an identical package, but non-detection is not proof of novelty, priority, non-existence, or first authorship.” |
| 普通中英翻译在本机直接完成，不调用 DGX。 | “Ordinary Chinese--English translation is performed directly on the local workstation; DGX is not used.” |
| 任意三维初值的全局正则性与 Clay 千禧年问题仍然开放。 | “Global regularity for arbitrary three-dimensional data and the Clay Millennium problem remain open.” |

## 6. Machine-readable release boundary

```text
localProductTensorDistinctFromKHM=TRUE
instantaneousPressureFromLocalProductTensor=VERIFIED_CLASSICAL
quadraticTensorOnlyDynamicClosure=NOT_ESTABLISHED
exactHigherMomentHierarchy=VERIFIED_CLASSICAL
heatCovariancePSD=INTERNAL_EXACT
heatCovarianceScalePDE=INTERNAL_EXACT
filterParameterEquationIsPhysicalTimeClosure=FALSE
filteredEquation=VERIFIED_CLASSICAL_RECONSTRUCTION
subfilterFluxSignDefinite=FALSE
criticalTensorStressRow=INTERNAL_COROLLARY
criticalTensorStressRowAssumesL4tL6x=TRUE
energyOnlyFixedScaleStress=INTERNAL_COROLLARY
energyOnlyUniformAsSToZero=FALSE
energyOnlyShortScaleLoss=s^(-1/2)
centeredPressureVariance=INTERNAL_COROLLARY
centeredPressureVarianceDirectClassicalCollision=TRUE
centeredPressureVarianceNoveltyClaim=FORBIDDEN
fourSiteParityWitness=INTERNAL_EXACT
formalFiniteCertificate=PASS
formalFiniteCertificateChecks=75
formalFigurePackage=PASS
formalFigureChecks=325
sourceCommitAssigned=TRUE
sourceCommit=84e808dae473f6381cbf9df55a71f5fe81a1cfce
certificateSourceCommit=6c79f23152116f5d420be6ff03653500ab02ef0e
finitePackageCommit=044bfb3f7e5af98e2615f60747c9e5109ef12d7c
figurePackageCommit=6c20af03a21488fea3f060738084fa9048437984
finalSeal=TRUE
quadraticStateNoGoExcludesSignedAugmentation=FALSE
universalClosureLowerBound=NOT_PROVED
navierStokesSimulation=NOT_RUN
finiteWitnessIsSimulation=FALSE
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=FALSE
publicReleaseTransaction=PENDING
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```

## 7. Forbidden public wording and required replacement

| Forbidden or misleading wording | Required replacement |
|---|---|
| “the KHM tensor used in R0.73U” | “the heat-filtered local product tensor, explicitly distinguished from the classical two-point KHM tensor” |
| “pressure is still missing from the full tensor” | “the full local tensor reconstructs instantaneous pressure, while signed third-order dynamics remain missing” |
| “a closed heat-stress evolution” | “an exact covariance equation in the filter parameter \(s\)” |
| “PSD stress dissipates energy” | “the PSD covariance has a signed contraction with the trace-free strain” |
| “an energy-class critical closure” | “a critical tensor row conditional on \(L_t^4L_x^6\), plus a fixed-positive-scale energy estimate with \(s^{-1/2}\) loss” |
| “a new pressure regularity criterion” | “an internal centered corollary with a direct classical weighted-pressure collision” |
| “the quadratic tensor can never be evolved” | “the even quadratic state alone cannot determine the signed tensor tangent through a single-valued autonomous equality” |
| “the witness rules out every estimate” | “the witness leaves one-sided, absolute, integrated, and signed-augmentation routes open” |
| “a four-mode blow-up simulation” | “an exact four-site sparse-Fourier diagnostic for a smooth planar initial field” |
| “a universal \(s^{-1/2}\) lower bound” | “an \(s^{-1/2}\) coefficient-level cost for the selected dilated witness at a parabolic slice” |
| “no prior work exists” | “no identical package was located in the bounded search” |
| “R0.73U solves or nearly solves Navier--Stokes” | “R0.73U isolates a useful tensor hierarchy and a precise signed-information boundary; arbitrary-data global regularity remains open” |
| “translation was run on DGX” | “ordinary translation was performed directly on the local workstation” |

## 8. Mandatory English boundary paragraph

Use this paragraph without strengthening its verbs:

> R0.73U reconstructs instantaneous pressure from the heat-filtered local
> product tensor and derives an exact positive covariance hierarchy in the
> filter parameter.  The uniform critical tensor row is conditional on the
> classical \(L_t^4L_x^6\) strong norm, while the energy-only row loses
> \(s^{-1/2}\) at short scale.  An exact four-site sign pair shows that the
> even quadratic heat state alone cannot determine the signed tensor tangent;
> it does not rule out signed augmentation, one-sided estimates, time
> integration, or cancellation.  This release is a local auditable synthesis,
> not a Navier--Stokes simulation, novelty claim, or Clay conclusion.

## 9. Literature-attribution phrases

| Topic | Required attribution boundary |
|---|---|
| Two-point hierarchy | Attribute the classical KHM hierarchy to von K\'arm\'an--Howarth (1938) and the arbitrary-order structure-function equations to Hill (2001); state that these are not the local product tensor. |
| Contemporary physical-space closure | Describe Zambrano--Duraisamy (2026) as a model-based closure for homogeneous isotropic turbulence, not a deterministic general-3D closure theorem. |
| Exact filtering | Attribute the filtering framework and inter-filter identities to Germano (1992); do not turn exact stress definition into a constitutive closure. |
| Signed subgrid transfer | Cite Eyink (1996) for exact stress/flux and locality results under stated hypotheses. |
| Cubic commutator/defect | Cite Constantin--E--Titi (1994) and Duchon--Robert (2000) as classical context for signed cubic transfer, not as the source of the four-site witness. |
| Centered pressure variance | Cite Tran--Yu--Dritschel (2021), DOI `10.1017/jfm.2020.1033`, as the direct classical weighted-pressure collision; call the centered inequality an internal corollary. |
| Negative search result | Use “not located in the bounded search,” never “absent from the literature.” |

## 10. Public one-sentence boundary

**Chinese:** R0.73U 用完整局部二次张量在同一 heat 尺度重建压力，并给出
正半定协方差的精确尺度方程；但一致临界估计仍以经典强范数为前提，能量唯一
估计在零尺度损失 \(s^{-1/2}\)，而四站点符号对只证明偶二次状态不能单值确定
带符号张量切向量，因此任意三维初值全局正则性与 Clay 问题仍然开放。

**English:** R0.73U reconstructs pressure at the same heat scale from the
full local quadratic tensor and gives an exact scale equation for its positive
semidefinite covariance; however, the uniform critical estimate still assumes
a classical strong norm, the energy-only estimate loses \(s^{-1/2}\) at zero
scale, and the four-site sign pair proves only that the even quadratic state
cannot determine the signed tensor tangent through a single-valued law, so
arbitrary-data three-dimensional global regularity and the Clay problem remain
open.
