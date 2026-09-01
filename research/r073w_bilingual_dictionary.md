# R0.73W bilingual dictionary and claim boundary

**Status:** analytic wording, bounded primary-literature audit, commit-bound
finite certificate, and immutable formal-figure source/package seal complete;
the public release transaction is ready

**Release title:** R0.73W | Signed subfilter production: heat-plane
characteristics, the energy-class boundary, and exact counterexamples

**Public title (zh):** R0.73W｜带符号亚滤波 production：heat-plane
特征线、能量类边界与精确反例

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

The word “heat” below refers to the filter semigroup \(P_s=e^{s\Delta}\), not
to thermodynamic heat.  The sign convention is always
\(\Pi_s=-\tau_s:\nabla v_s\).

## 1. Canonical section headings

| 中文标题 | English heading |
|---|---|
| 直接结论 | Main result at a glance |
| 带符号 production 与 deviatoric 障碍 | Signed production and the deviatoric obstruction |
| \((t,s)\) heat-plane 特征线恒等式 | The \((t,s)\) heat-plane characteristic identity |
| 能量类的绝对估计 | The absolute energy-class estimate |
| 两路径精确 Fourier 反例 | The two-path exact Fourier counterexample |
| 固定符号为什么失败 | Why a universal sign fails |
| 同时刻二次吸收为什么失败 | Why same-time quadratic absorption fails |
| 文献归属与限定式检索 | Literature attribution and the bounded search |
| 结果价值与下一步 | Research value and the next step |

## 2. Mathematical terms

| 中文 | English | Required meaning |
|---|---|---|
| 周期 heat 半群 | periodic heat semigroup | \(P_s=e^{s\Delta}\) on the normalized torus |
| heat-filtered velocity | heat-filtered velocity | \(v_s=P_su\); preserve the sign of \(u\) |
| 精确亚滤波应力 | exact subfilter stress | \(\tau_s=P_s(u\otimes u)-v_s\otimes v_s\) |
| heat covariance | heat covariance | The same tensor \(\tau_s\), viewed as a positive covariance |
| resolved strain | resolved strain | \(S_s=(\nabla v_s+\nabla v_s^T)/2\), with zero trace |
| 带符号亚滤波 production | signed subfilter production | \(\Pi_s=-\tau_s:S_s\); positive values remove resolved energy under the frozen convention |
| deviatoric stress | deviatoric stress | \(\tau_s^\circ=\tau_s-(\operatorname{tr}\tau_s/3)I\) |
| deviatoric alignment | deviatoric alignment | The sign-indefinite contraction \(-\tau_s^\circ:S_s\) |
| 强制扩散方程 | forced diffusion equation | The exact \(s\)-equation for \(\tau_s\), established for Gaussian filtering |
| 精确尺度积分 | exact scale integral | The Duhamel representation over all \(0\le r\le s\) |
| resolved energy density | resolved energy density | \(e_s=|v_s|^2/2\) |
| heat-plane 特征线 | heat-plane characteristic | A curve with \(s'(t)=-\nu\), tangent to \(\partial_t-\nu\partial_s\) |
| 特征线能量支付 | characteristic energy payment | The signed spatially averaged \(\Pi_s\) integral equals an endpoint energy difference |
| Leray--Hopf 能量类 | Leray--Hopf energy class | \(L_t^\infty L_x^2\cap L_t^2H_x^1\) |
| 固定尺度绝对估计 | fixed-scale absolute estimate | The \(L^1_{t,x}\) bound with factor \(s^{-1/4}\) |
| heat 尺度可积 | integrable over heat scale | \(\int_0^S\|\Pi_s\|_1ds\lesssim S^{3/4}\); not uniform at \(s=0\) |
| centered increment | centered increment | \(a_s(x,y)=u(x-y)-v_s(x)\), centered at the filtered value rather than at \(u(x)\) |
| 收缩三阶中心通量 | contracted third central flux | \(K_{j,s}=\kappa_{iij,s}/2\) |
| 带符号中心增量余项 | signed centered-increment remainder | \(\mathscr S_s=(4s)^{-1}\int y\cdot a_s|a_s|^2g_sdy\) |
| carré-du-champ 耗散行 | carré-du-champ dissipation row | \(D_{ii,s}=2\int_0^sP_{s-r}|\nabla^2v_r|^2dr\ge0\) |
| 临界 heat 尺度权重 | critical heat-scale weight | \(w(s)=s^{-1/2}\), whose multiplier is \(\sqrt{\pi/2}L^{-1/2}\) |
| 临界尺度平均 | critical scale average | Signed integration of the spatial mean over \(s\) before taking an absolute value |
| Riesz 三线性型 | Riesz trilinear form | \(-\sqrt{\pi/2}\int u_i u_jR_ju_i\), bounded by \(C\|u\|_3^3\) |
| 梯度 covariance | gradient covariance | \(D_{ij,s}=P_s(\partial_k u_i\partial_k u_j)-\partial_kv_{s,i}\partial_kv_{s,j}\) |
| 同时刻二次吸收 | same-time quadratic absorption | A comparison of the cubic mean production with the positive quadratic \(\nu\langle D_{ii,s}\rangle\) at one time |
| 振幅缩放障碍 | amplitude-scaling obstruction | Production scales as \(A^3\), while the declared viscous covariance scales as \(A^2\) |
| 秩三 Fourier 支撑见证 | rank-three Fourier-support witness | The public finite field has support spanning three independent frequency directions; this is not a genericity claim |
| 2D3C 诊断见证 | 2D3C diagnostic witness | A lower-dimensional cross-check retained inside the certificate, not the public primary field |
| 两路径精确证书 | two-path exact certificate | Two non-importing finite-algebra implementations with identical declared outputs |
| 限定式检索 | bounded search | A scoped primary-source search; non-detection is not a novelty or priority proof |
| 局部尺度临界控制 | localized scale-critical control | The open next interface; no such estimate is proved in R0.73W |
| 任意初值三维全局正则性 | arbitrary-data three-dimensional global regularity | Open |
| Clay 千禧年问题结论 | Clay Millennium conclusion | Open and expressly not claimed |

## 3. Canonical notation

| Symbol | Frozen meaning |
|---|---|
| \(P_s=e^{s\Delta}\) | periodic heat semigroup |
| \(v_s=P_su\) | heat-filtered velocity |
| \(\tau_s=P_s(u\otimes u)-v_s\otimes v_s\) | exact subfilter stress / heat covariance |
| \(S_s\) | resolved symmetric strain |
| \(\Pi_s=-\tau_s:S_s\) | signed subgrid production |
| \(e_s=|v_s|^2/2\) | resolved energy density |
| \(E_s=\langle e_s\rangle\) | spatially averaged resolved energy |
| \(k_s=\operatorname{tr}\tau_s/2\) | subfilter energy |
| \(D_{ij,s}\) | gradient covariance |
| \(K_{j,s}=\kappa_{iij,s}/2\) | contracted third central flux |
| \(\mathscr S_s\) | signed centered-increment remainder after the divergence split |
| \(L=-\Delta\) | positive periodic Laplacian on mean-zero fields |
| \(I_\Pi(u)\) | critical \(s^{-1/2}\)-weighted spatial-mean production |
| \(q=e^{-s}\) | exact certificate heat variable |
| \(R\) | frozen rank-three-support trigonometric polynomial |
| \(u_A=AR\) | amplitude-scaled finite witness |

## 4. Mandatory bilingual boundary sentences

| 中文冻结句 | Mandatory English sentence |
|---|---|
| Gaussian 亚滤波应力的强制扩散方程与精确尺度积分已有文献结果，本节不主张新颖性。 | “The forced-diffusion equation and exact scale integral for the Gaussian subfilter stress are established in the literature; this release does not claim novelty for them.” |
| \(\tau_s\) 半正定，但 incompressible strain 无迹，因此 production 的符号由 deviatoric alignment 决定。 | “The tensor \(\tau_s\) is positive semidefinite, but incompressible strain is trace-free, so the sign of production is determined by deviatoric alignment.” |
| heat-plane 特征线恒等式精确控制带符号的空间平均，不控制 \(|\Pi_s|\) 或逐点符号。 | “The heat-plane characteristic identity exactly controls the signed spatial mean; it does not control \(|\Pi_s|\) or a pointwise sign.” |
| 能量类绝对估计在 \(s\downarrow0\) 时损失 \(s^{-1/4}\)，但该损失对 heat 尺度积分是可积的。 | “The absolute energy-class estimate loses \(s^{-1/4}\) as \(s\downarrow0\), but this loss is integrable over heat scale.” |
| 收缩三阶中心通量是一个精确 divergence；消去它以后，trace 方程只剩压力通量、非负梯度 covariance 与带符号中心增量余项。 | “The contracted third central flux is an exact divergence; after it is cancelled, the trace equation retains only the pressure flux, the nonnegative gradient covariance, and the signed centered-increment remainder.” |
| 临界 \(s^{-1/2}\) 尺度平均恢复的是经典 \(H^{1/2}\) 小数据三线性结构，不是任意能量的 coercive 吸收。 | “The critical \(s^{-1/2}\) scale average recovers the classical \(H^{1/2}\) small-data trilinear structure, not coercive absorption for arbitrary energy.” |
| 临界尺度估计先对空间和 heat 尺度做带符号积分，再取绝对值；它不是局部或逐尺度绝对通量估计。 | “The critical-scale estimate first performs signed integration in space and heat scale and only then takes an absolute value; it is not a local or fixed-scale absolute-flux estimate.” |
| 本节没有证明 \(1/4\) 是最优指数。 | “This release does not prove that \(1/4\) is the optimal exponent.” |
| 精确 Fourier 见证给出两种平均 production 符号，所以不存在对所有光滑散度自由数据成立的单边符号律。 | “The exact Fourier witness produces both signs of the mean production, so no one-sided sign law holds for all smooth divergence-free data.” |
| 振幅缩放排除了文中指定的同时刻、振幅无关二次吸收；它不排除非线性、时间积分或局部化估计。 | “Amplitude scaling excludes the stated same-time amplitude-independent quadratic absorption; it does not exclude nonlinear, time-integrated, or localized estimates.” |
| 公开主见证具有秩三 Fourier 支撑，但它仍只是普适符号命题的反例，不是 generic turbulence、奇性或 blow-up 候选。 | “The public primary witness has rank-three Fourier support, but it remains only a counterexample to a universal sign statement, not generic turbulence, a singularity, or a blow-up candidate.” |
| 有限证书是精确 Fourier 代数，不是 Navier--Stokes 时间仿真。 | “The finite certificate is exact Fourier algebra, not a Navier--Stokes time simulation.” |
| 限定式检索未找到相同打包，不等于新颖性、优先权、不存在或第一性证明。 | “The bounded search did not locate an identical package; non-detection is not proof of novelty, priority, non-existence, or first authorship.” |
| 普通中英翻译在本机直接完成，不调用 DGX。 | “Ordinary Chinese--English translation is performed directly on the local workstation; DGX is not used.” |
| 任意三维初值的全局正则性与 Clay 千禧年问题仍然开放。 | “Global regularity for arbitrary three-dimensional data and the Clay Millennium problem remain open.” |

## 5. Machine-readable release boundary

```text
problemFreeze=COMPLETE
parentAnalyticDerivation=COMPLETE
independentAnalyticAudit=PASS_WITH_WEAK_SOLUTION_BOUNDARY
primaryLiteratureAudit=BOUNDED_COMPLETE
gaussianStressDuhamel=VERIFIED_CLASSICAL_REDERIVED
deviatoricProductionIdentity=VERIFIED_CLASSICAL_REDERIVED
heatPlaneCharacteristicIdentity=INTERNAL_EXACT_AUDITED
characteristicMeanPayment=INTERNAL_EXACT_AUDITED
energyClassFixedScaleEstimate=INTERNAL_UNCONDITIONAL_AUDITED
energyClassScaleIntegral=INTERNAL_UNCONDITIONAL_AUDITED
centeredIncrementSplit=INTERNAL_EXACT_AUDITED
traceFluxCancellation=INTERNAL_EXACT_AUDITED
gradientCovarianceCarreDuChamp=INTERNAL_EXACT_AUDITED
weightedMeanMultiplierIdentity=INTERNAL_EXACT_AUDITED
criticalHalfScaleAverage=INTERNAL_CRITICAL_AUDITED
universalProductionSign=FALSE
amplitudeIndependentQuadraticAbsorption=FALSE
formalFiniteCertificate=SEALED_COMMIT_BOUND
formalFigurePackage=SEALED_COMMIT_BOUND
formalFigureChecks=49
formalFigureRows=1416
figureSourceCommit=ac6293ac4d0c46c696d2ec8e29d3fb1350e341f1
figurePackageCommit=60b0e869bbaa3a0ace185bf450e067d79fcd79b3
publicReleaseTransaction=READY
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=false
localizedScaleCriticalControl=OPEN
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```

## 6. Forbidden public wording and replacement

| Forbidden wording | Required replacement |
|---|---|
| “positive stress makes the cascade positive” | “positive stress leaves an indefinite deviatoric contraction with trace-free strain” |
| “viscosity absorbs production” | “the signed spatial mean is paid along a descending heat characteristic” |
| “energy controls the flux uniformly” | “energy gives an \(s^{-1/4}\) fixed-scale bound and an \(S^{3/4}\) scale integral” |
| “the Fourier mode proves blow-up” | “the finite field disproves a universal sign or quadratic-absorption statement” |
| “new exact Gaussian stress formula” | “the established Johnson formula in the current heat-semigroup normalization” |
| “near a Clay solution” | “a rigorous structural identity and a still-insufficient energy-class estimate” |
