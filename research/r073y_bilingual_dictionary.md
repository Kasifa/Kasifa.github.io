# R0.73Y bilingual dictionary and claim boundary

**Status:** exact analytic theorem, deterministic certificate, bounded primary-source audit, formal 25-file figure seal, and independent figure re-audit complete; reader publication is note-only and the cumulative recap remains frozen at R0.73X

**Release title:** R0.73Y | Exact shear class rules out production-only coercivity

**Public title (zh):** R0.73Y｜Exact shear 类否定 production-only coercivity

**Latest recap release:** r073x

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

“Heat” denotes the periodic heat semigroup (P_s=e^{s\Delta}), not
thermodynamic heat. “Positive scale” means (s>0); it does not silently add a
suitable-weak trace at (s=0). “Exact shear” means the full smooth periodic
Navier--Stokes solution in the stated orthogonal rank-one class, not a
linearized trajectory or a DNS sample.

## 1. Canonical section headings

| 中文标题 | English heading |
|---|---|
| 本节结论 | Main conclusion |
| 更强的 exact shear 类 | The full exact-shear class |
| 单一 Fourier 见证与可复现证书 | A single-Fourier witness and reproducible certificate |
| 正 covariance 由什么支付 | What pays for the positive covariance |
| 文献校准 | Literature calibration |
| 价值评估 | Assessment of value |
| R0.73Z 的冻结任务 | Frozen task for R0.73Z |

## 2. Mathematical terms

| 中文 | English | Required meaning |
|---|---|---|
| 正 heat 尺度 | positive heat scale | (s>0), with no automatic (s=0) endpoint |
| 正交 rank-one shear | orthogonal rank-one shear | (u^A=AaF(t,k\cdot x)), (a\cdot k=0) |
| 真实 NSE 解 | exact NSE solution | a smooth solution of the full unforced periodic equations with (p=0) |
| subfilter stress | subfilter stress | τ_s=P_s(u\otimes u)-P_su\otimes P_su |
| energy flux | energy flux | Π_s=-τ_s:\nabla P_su, a signed production channel |
| centered production | centered production | ᵊe_s, the centered cubic-increment production remainder |
| pressure--velocity covariance | pressure--velocity covariance | (Q_s=P_s(pu)-P_sp\,P_su) |
| gradient covariance | gradient covariance | (D_{ii,s}=P_s(|\nabla u|^2)-|\nabla P_su|^2\ge0) |
| production-only functional | production-only functional | a scalar construction from Π_s and ᵊe_s that vanishes on zero input |
| 振幅无关有限模量 | finite amplitude-independent modulus | ω with ω(0)<∞, independent of (A) |
| exact no-go theorem | exact no-go theorem | a quantified obstruction to the stated production-only implication |
| heat variance | heat variance | the strict variance in the braces of formula (2.8) |
| subfilter storage | subfilter storage | the energy account whose decay pays the positive covariance in the shear class |
| nonproduction debt | nonproduction debt | endpoint, time-cutoff, spatial-cutoff, or viscous-boundary accounts |
| finite cross-check | finite cross-check | a binary64 or Gaussian-integral check, never the source of a universal quantifier |
| bounded literature search | bounded literature search | a scoped primary-source collision audit, not novelty proof |
| quotient coercivity | quotient coercivity | a future estimate after explicitly removing the shear kernel |
| positive observable | positive observable | a covariance, endpoint/cutoff debt, or independent positive tent quantity |
| suitable-weak zero-scale endpoint | suitable-weak zero-scale endpoint | passage to (s=0) with defect measures and traces; open |
| epsilon regularity | epsilon regularity | a CKN-facing positive smallness implication; not proved here |
| formal figure | formal figure | deterministic source-data-bound PDF/PNG/SVG package with logs and validators |
| Clay conclusion | Clay conclusion | open and expressly not claimed |

## 3. Canonical notation

| Symbol | Frozen meaning |
|---|---|
| (k\in\mathbb Z^3\setminus\{0\}) | periodic shear wave vector |
| (a\in\mathbb R^3\setminus\{0\}) | velocity direction with (a\cdot k=0) |
| (F(t,\vartheta)) | one-dimensional heat evolution of a nonconstant zero-mean profile |
| (u^A=AaF(t,k\cdot x)) | arbitrary-amplitude exact periodic shear solution |
| (P_s=e^{s\Delta}) | periodic heat filter |
| τ_s | subfilter stress tensor |
| Π_s | signed stress--gradient production |
| ᵊe_s | centered cubic production remainder |
| (Q_s) | pressure--velocity heat covariance |
| (D_{ii,s}) | nonnegative gradient heat covariance, strictly positive here |
| \(\mathcal Z_A\) | the R0.73X positive-scale size evaluated on the amplitude-(A) shear |
| \(\mathfrak P\) | a zero-preserving production-only functional |
| \(\mathcal D_{3/2}^{\square}\) | proposed cubic positive observable for R0.73Z |

## 4. Mandatory bilingual boundary sentences

| 中文冻结句 | Mandatory English sentence |
|---|---|
| 该 exact shear 类是真实的光滑周期 Navier--Stokes 解，不是线性化轨道或数值样本。 | “The exact-shear class consists of genuine smooth periodic Navier--Stokes solutions, not linearized trajectories or numerical samples.” |
| 对每个正 heat 尺度，两个 production channel 与 pressure covariance 为零，而 gradient covariance 严格为正。 | “At every positive heat scale, both production channels and the pressure covariance vanish, while the gradient covariance is strictly positive.” |
| 否定的只是在零输入处取零的 production-only functional 所给出的振幅无关有限模量。 | “The theorem rules out only a finite amplitude-independent modulus built from a production-only functional that vanishes on zero input.” |
| 该结果不否定加入 covariance、endpoint 或 cutoff debt 的估计。 | “The result does not rule out estimates that retain covariance, endpoint terms, or cutoff debt.” |
| 正 covariance 由 subfilter storage 的下降支付，不由零 production 支付。 | “The positive covariance is paid by the decay of subfilter storage, not by the vanishing production.” |
| 严格正性来自解析 heat-variance 证明，不来自有限采样。 | “Strict positivity comes from the analytic heat-variance proof, not from finite sampling.” |
| Vreman 等已覆盖 simple-shear 零 SGS dissipation，因此 basic shear 机制不得申报为新发现或优先权。 | “Vreman and related literature already cover zero SGS dissipation in simple shear, so the basic shear mechanism is not claimed as a new discovery or priority result.” |
| 本节的可保留价值是将已知机制嵌入 R0.73X 量的精确全尺度 no-go 命题。 | “The retained contribution is an exact all-scale no-go statement obtained by inserting known mechanisms into the precise R0.73X quantities.” |
| 作为独立论文主定理，当前结果过于初等且与 LES/coarse-graining 文献高度邻近。 | “As a stand-alone paper theorem, the current result is too elementary and too close to the LES/coarse-graining literature.” |
| 下一步必须 quotient 掉 shear kernel，并加入能检测它的同次齐正观测。 | “The next step must quotient out the shear kernel and add a positive observable of matching homogeneity that detects it.” |
| 正式附图是解析见证的可视化，不是 DNS 或 turbulence-closure validation。 | “The formal figure visualizes an analytic witness; it is not DNS or turbulence-closure validation.” |
| 限定检索未找到逐字相同的打包命题，不等于 novelty 或 priority 证明。 | “A bounded search did not locate the verbatim packaged proposition; non-detection is not proof of novelty or priority.” |
| 本节只发布研究笔记；累积 Recap 保持在 R0.73X 里程碑。 | “This release publishes a research note only; the cumulative recap remains at the R0.73X milestone.” |
| 普通中英翻译在本机直接完成，不调用 DGX。 | “Ordinary Chinese--English translation is performed directly on the local workstation; DGX is not used.” |
| suitable-weak (s=0)、epsilon regularity、任意三维初值全局正则性与 Clay 结论全部开放。 | “The suitable-weak (s=0) endpoint, epsilon regularity, global regularity for arbitrary three-dimensional data, and the Clay conclusion all remain open.” |

## 5. Machine-readable release boundary

```text
exactShearNSE=PROVED_ANALYTICALLY
allPositiveHeatScalesZeroProduction=PROVED_ANALYTICALLY
gradientCovarianceStrictPositivity=PROVED_ANALYTICALLY
positiveSizeCubicHomogeneity=PROVED_ANALYTICALLY
productionOnlyCoercivity=REFUTED_FOR_ZERO_PRESERVING_FUNCTIONALS
singleFourierCertificate=FINITE_CROSS_CHECK_ONLY
strictPositivityFromSampling=FALSE
basicShearNoveltyOrPriority=NOT_CLAIMED
quotientCoercivity=OPEN
pressureActiveInvisibleFamily=OPEN
suitableWeakZeroScaleEndpoint=OPEN
epsilonRegularity=OPEN
formalEvidenceCertificate=SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED
formalFigurePackage=SEALED_COMMIT_BOUND_25_FILES
navierStokesSimulation=NOT_RUN
directNumericalSimulation=NOT_RUN
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=false
latestPublishedRelease=r073y
latestRecapRelease=r073x
recapPolicy=MILESTONE_ONLY
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
NOT CLAY
```

## 6. Forbidden public wording and replacement

| Forbidden wording | Required replacement |
|---|---|
| “production vanishes, therefore the solution is small” | “production vanishes while a positive covariance and nonproduction debts remain” |
| “the shear family disproves regularity” | “the smooth shear family disproves only the stated production-only modulus” |
| “strict positivity was proved numerically” | “strict positivity is analytic; finite calculations are cross-checks” |
| “the simple-shear mechanism is new” | “the mechanism directly collides with established LES/coarse-graining literature” |
| “the production-only route nearly solves Clay” | “the route is closed by an exact smooth kernel; global regularity remains open” |
| “R0.73Y updates the cumulative recap” | “R0.73Y publishes a note; R0.73X remains the latest milestone recap” |
