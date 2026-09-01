# R0.73X bilingual dictionary and claim boundary

**Status:** research freeze and independent Gaussian/pressure audits complete;
the real figure is source-commit-bound, child-package sealed, and owner-visually
validated, while its two publication-facing source audits and public release
transaction remain pending

**Release title:** R0.73X | Localized heat ledgers with explicit exterior tails: Gaussian velocity control, algebraic pressure tails, and the open coercivity bridge

**Public title (zh):** R0.73X｜带显式外部尾项的局部热账本：Gaussian 速度控制、代数压力尾与未闭合 coercivity 桥

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

“Heat” denotes the filter semigroup \(P_s=e^{s\Delta}\), not thermodynamic
heat. “Positive scale” means \(s>0\); it never silently includes an arbitrary
suitable-weak trace at \(s=0\).

## 1. Canonical section headings

| 中文标题 | English heading |
|---|---|
| 直接结论 | Main result at a glance |
| 局部账本与问题入口 | The localized ledger and the entry question |
| Gaussian 速度尾控制 | Gaussian control of the velocity tail |
| 压力为什么留下代数尾 | Why pressure leaves an algebraic tail |
| 完整外部 functional | The complete exterior functional |
| positive-scale 绝对 size lemma | The positive-scale absolute size lemma |
| 两个精确负结果及其量词 | Two exact negative results and their quantifiers |
| 独立审计与可执行证据 | Independent audits and executable evidence |
| 文献归属与碰撞边界 | Literature ownership and collision boundary |
| 研究价值与未闭合 coercivity 桥 | Research value and the open coercivity bridge |
| 下一步：R0.73Y 与发布边界 | Next: R0.73Y and the release boundary |

## 2. Mathematical terms

| 中文 | English | Required meaning |
|---|---|---|
| 周期 heat 半群 | periodic heat semigroup | \(P_s=e^{s\Delta}\) on the normalized torus |
| 正 heat 尺度 | positive heat scale | \(s>0\); no automatic endpoint trace at \(s=0\) |
| 局部 heat-characteristic 账本 | localized heat-characteristic ledger | The fixed-cutoff resolved and subfilter balances along \(s'(t)=-\nu\) |
| centered production 余项 | centered-production remainder | \(\mathscr S_s\), the signed cubic remainder after the exact divergence split |
| 压力--速度 covariance | pressure--velocity covariance | \(Q_s=P_s(pu)-P_sp\,P_su\), used in a gauge-invariant form |
| 外部 functional | exterior functional | \(\mathcal A_{\rm ext}^{\square}=\mathcal G_{u,p}^{\square}+\mathcal H_u^{\square}\) |
| Gaussian 速度尾 | Gaussian velocity tail | Annular \(L^3\) velocity mass paid with super-exponential heat weights |
| Gaussian 压力源尾 | Gaussian pressure-source tail | Direct heat propagation of paid pressure/product source norms |
| harmonic pressure tail | harmonic pressure tail | Algebraic annular moment forced by the elliptic off-diagonal kernel |
| annular coefficient | annular coefficient | \(\gamma_m(\theta)=\theta^{-2}e^{-4^{m-1}/(32\theta)}\) for direct heat rows |
| harmonic moment | harmonic moment | \(\Lambda_R=R\sum_{m\ge1}(2^mR)^{-4}\int_{A_m}|\widetilde u|^2\) |
| positive-scale absolute size | positive-scale absolute size | A finite scale-compatible upper bound for absolute rows at \(s>0\), not smallness |
| measurable heat-scale selection | measurable heat-scale selection | Any measurable \(s(t)\in(0,\theta R^2]\) in the frozen theorem |
| core--core payment | core--core payment | Local singular-integral/harmonic pressure terms paid by local \(L^3\) interpolation |
| complete pressure distribution | complete pressure distribution | The periodized distribution retaining origin contact terms before localization |
| off-diagonal kernel | off-diagonal kernel | The ordinary order \(-4\) pressure derivative kernel after local-source subtraction |
| fixed harmonic probe | fixed harmonic probe | A positive periodic probe used for an exact finite absorption obstruction; not compactly supported |
| compact cutoff | compact cutoff | \(\eta_R\in W_0^{1,\infty}(B_R)\) with \(\|\nabla\eta_R\|_\infty\le C_\eta/R\) |
| translated packet | translated packet | A compact smooth divergence-free static velocity packet used only for functional counterexamples |
| associated pressure | associated pressure | The pressure determined by the NSE/Poisson relation for a given velocity; not replaced by \(p=0\) unless justified |
| signed-to-absolute coercivity | signed-to-absolute coercivity | The open implication from a signed payment to small positive absolute quantities |
| weighted tent/Carleson control | weighted tent/Carleson control | The open critical positive cylinder norm; not the proved unweighted size row |
| suitable-weak zero-scale endpoint | suitable-weak zero-scale endpoint | Passage to \(s=0\) while preserving defect measures and endpoint traces; open |
| epsilon regularity | epsilon regularity | A CKN/Lin/Vasseur/Kwon-facing positive smallness criterion; not proved here |
| bounded search | bounded search | Scoped primary-source search; non-detection is not novelty or priority evidence |
| formal figure | formal figure | Deterministic, source-data-bound PDF/PNG/SVG package with logs, manifest, validation, and audit |
| Clay conclusion | Clay conclusion | Open; expressly not claimed |

## 3. Canonical notation

| Symbol | Frozen meaning |
|---|---|
| \(z_0=(t_0,x_0)\) | cylinder center |
| \(R\) | physical cylinder radius |
| \(0<\theta\le1\) | maximum heat-scale fraction |
| \(I_R^{\square}\) | standard or viscosity-adapted time interval |
| \(s(t)\) | measurable selection in \((0,\theta R^2]\) |
| \(\eta_R\) | compact spatial cutoff with gradient bound \(C_\eta/R\) |
| \(\mathscr S_s\) | centered cubic production remainder |
| \(Q_s\) | gauge-invariant pressure--velocity heat covariance |
| \(A_m(R)\) | dyadic lifted annulus |
| \(\gamma_m(\theta)\) | Gaussian annular coefficient |
| \(\Lambda_R(t)\) | algebraic harmonic-pressure moment |
| \(\mathcal G_{u,p}^{\square}\) | Gaussian velocity/pressure source tail |
| \(\mathcal H_u^{\square}\) | algebraic harmonic-pressure tail |
| \(\mathcal A_{\rm ext}^{\square}\) | complete exterior functional |
| \(\mathcal E^{\square}\) | frozen local energy quantity |
| \(\mathcal C_{\mathscr S,0,\theta}^{\rm abs,\square}\) | unweighted full scale-integrated absolute centered-production row |

## 4. Mandatory bilingual boundary sentences

| 中文冻结句 | Mandatory English sentence |
|---|---|
| R0.73X 证明的是 positive-scale absolute size 与有限性，不是 smallness、absorption 或 coercivity。 | “R0.73X proves positive-scale absolute size and finiteness, not smallness, absorption, or coercivity.” |
| 直接 heat 传播产生 Gaussian 尾；harmonic pressure 由椭圆核产生代数尾，两者不能混写。 | “Direct heat propagation produces Gaussian tails; harmonic pressure produces an algebraic tail through the elliptic kernel, and the two mechanisms must not be conflated.” |
| 外部 functional 是显式声明的非局部输入，没有从一个局部 cylinder 自动控制为小量。 | “The exterior functional is an explicitly declared nonlocal input and is not automatically controlled as a small quantity by one local cylinder.” |
| \(|\mathscr S_s|\le C_0s^{-1/2}P_{2s}|u|^3\) 是 functional lemma，不使用 Navier--Stokes 时间轨道。 | “The bound \(|\mathscr S_s|\le C_0s^{-1/2}P_{2s}|u|^3\) is a functional lemma and does not use a Navier--Stokes time trajectory.” |
| 完整 pressure/exterior 估计对每个 measurable positive heat scale 成立，但没有给出 \(s=0\) endpoint。 | “The complete pressure/exterior estimate holds for every measurable positive heat scale, but it gives no endpoint at \(s=0\).” |
| pressure 的代数 annular moment 来自 off-diagonal order \(-4\) kernel，不能用 Gaussian 权重替代。 | “The algebraic annular pressure moment comes from the off-diagonal order \(-4\) kernel and cannot be replaced by a Gaussian weight.” |
| fixed harmonic probe 只排除指定 probe class 中的振幅无关二次吸收；compact-cutoff 命题仍开放。 | “The fixed harmonic probe excludes amplitude-independent quadratic absorption only in the stated probe class; the compact-cutoff statement remains open.” |
| translated packet 是带 \(p=\mu=0\) 的静态 functional 见证，通常不是 unforced NSE trajectory。 | “The translated packet is a static functional witness with \(p=\mu=0\) and is generally not an unforced Navier--Stokes trajectory.” |
| 该 packet 不反驳 associated-pressure inequality，也不反驳只对 NSE trajectories 陈述的估计。 | “The packet refutes neither an associated-pressure inequality nor an estimate stated only for Navier--Stokes trajectories.” |
| signed heat-characteristic payment 尚未推出 \(\mathcal E^{3/2}+\mathcal A_{\rm ext}\) 的 smallness。 | “A signed heat-characteristic payment has not been shown to imply smallness of \(\mathcal E^{3/2}+\mathcal A_{\rm ext}\).” |
| weighted tent/Carleson、suitable-weak \(s=0\)、epsilon regularity 与 Clay 结论全部开放。 | “Weighted tent/Carleson control, the suitable-weak \(s=0\) endpoint, epsilon regularity, and the Clay conclusion all remain open.” |
| 限定式检索未找到相同 bridge，不等于新颖性、优先权、不存在或第一性证明。 | “The bounded search did not locate the same bridge; non-detection is not proof of novelty, priority, non-existence, or first authorship.” |
| 普通中英翻译在本机直接完成，不调用 DGX。 | “Ordinary Chinese--English translation is performed directly on the local workstation; DGX is not used.” |
| 正式附图缺失时发布门必须失败，不得用占位资产伪造。 | “The release gate must fail while the formal figure is missing; no placeholder asset may be used.” |
| 任意三维初值的全局正则性与 Clay 千禧年问题仍然开放。 | “Global regularity for arbitrary three-dimensional data and the Clay Millennium problem remain open.” |

## 5. Machine-readable release boundary

```text
localizedHeatCharacteristicLedger=PROVED_WITH_STATED_SOLUTION_CLASS
centeredIncrementCutoffSplit=EXACT_AND_FINITE_CHECKED
gaussianVelocityTailLemma=INDEPENDENT_AUDIT_PASS
pressureExteriorTailSizeLemma=PASS_AT_POSITIVE_SCALE
positiveScaleAbsoluteSize=PROVED
fixedHarmonicProbeQuadraticAbsorption=REFUTED_EXACTLY
compactCutoffQuadraticAbsorption=OPEN
translatedPacketCounterexample=FUNCTIONAL_ONLY_NOT_NSE
associatedPressureCounterexample=NOT_CLAIMED
signedToAbsoluteCoercivity=OPEN
exteriorFunctionalLocallyControlled=OPEN
weightedTentCarlesonControl=OPEN
suitableWeakZeroScaleEndpoint=OPEN
epsilonRegularity=OPEN
formalEvidenceCertificate=SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED
formalFigurePackage=SEALED_COMMIT_BOUND
publicReleaseTransaction=READY_FOR_FINAL_CONTENT_AND_RELEASE_PINS
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=false
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```

## 6. Forbidden public wording and replacement

| Forbidden wording | Required replacement |
|---|---|
| “the tail is controlled locally” | “the explicit exterior functional remains on the right side” |
| “Gaussian pressure decay closes the estimate” | “direct heat rows are Gaussian, while harmonic pressure retains an algebraic tail” |
| “the size lemma is coercive” | “the lemma proves positive-scale absolute size only” |
| “the packet is an NSE counterexample” | “the packet refutes a velocity-only functional candidate under the stated static quantifiers” |
| “the harmonic probe settles compact cutoffs” | “the fixed probe obstruction leaves compact-cutoff absorption open” |
| “the tent norm is proved” | “the unweighted scale-integrated size row is proved; the weighted tent endpoint remains open” |
| “near a Clay solution” | “a rigorous nonlocal size ledger with an open signed-to-absolute bridge” |
