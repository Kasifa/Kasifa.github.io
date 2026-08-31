# R0.73R bilingual dictionary and public-claim boundary

**Status:** canonical terminology for synchronized HTML/PDF rendering;
publication provenance is still pending

**Release title:** R0.73R | A shellwise phase certificate for the critical
heat trace

**Public title (zh):** R0.73R｜能谱看不见的相位：临界热流迹的壳层证书

**Next release:** R0.73S

All ordinary translation for this release is written and reviewed directly
on the local workstation.  DGX is not used for translation.

## 1. Mathematical terms

| English | Chinese | Required meaning |
| --- | --- | --- |
| critical heat-flow trace | 临界热流迹 | \(\|f\|_{\mathfrak X}=\|e^{t\Delta}f\|_{L^4((0,\infty);L^6)}\), the R0.73Q sufficient entrance norm.  “Critical” means scaling-critical, not decisive. |
| shellwise phase certificate | 逐壳相位证书 | A finite Fourier evaluation or certified upper bound for the dyadic quantities entering \(\mathfrak X\).  It is not a necessary regularity test. |
| shell energy | 壳层能量 | \(E_j=\|P_jf\|_2\) for the fixed smooth periodic LP decomposition. |
| normalized sextic concentration | 归一化六次集中度 | \(\Theta_j=\|P_jf\|_6^6/E_j^6\) when \(E_j>0\).  It retains nonquadratic spatial concentration. |
| exact vector triple convolution | 精确向量三重卷积 | The component-safe Fourier representation of \(|P_jf|^2P_jf\), whose squared \(\ell^2\) norm equals \(\|P_jf\|_6^6\).  It is an exact evaluation, not a cheaper a priori proxy. |
| additive multiplicity | 三重和加法重数 | \(R_j=\max_n\#\{k_1+k_2+k_3=n\}\).  It gives the phase-blind upper bound \(\|P_jf\|_6\le R_j^{1/6}E_j\). |
| support cardinality certificate | 支撑计数证书 | The phase-blind bound \(\|P_jf\|_6\le M_j^{1/3}E_j\), where \(M_j\) counts active vector Fourier sites. |
| matched Fourier pair | 匹配 Fourier 对 | The Dirichlet and Rudin--Shapiro fields with exactly the same support, coefficient magnitudes, \(L^2\), and all quadratic Fourier-weighted Sobolev norms. |
| phase-coherence separation | 相位相干分离 | The matched pair has critical heat traces whose ratio grows like \(m^{2/3}\), despite identical quadratic spectral data. |
| fixed-ratio annulus | 固定比例环带 | The common support satisfies \(N\le|k|\le(\sqrt{82}/8)N\).  It need not lie in exactly one block of every overlapping LP partition. |
| analytic scaling | 解析标度 | A power law proved from exact moments and multiplier estimates.  It is not a fitted numerical slope or simulation output. |
| prescribed-threshold comparison | 已给定阈值比较 | An additional common fixed amplitude may be chosen from strict analytic constants to place one sequence eventually inside and the other outside a specified positive heat-ball radius. |
| zero-nonlinearity boundary | 零非线性边界 | The matched fields have the form \(e_3g(x_1,x_2)\), so \((W\cdot\nabla)W=0\) and their Navier--Stokes evolution is the globally smooth heat flow. |
| classical collision | 经典文献碰撞 | The heat--Besov equivalence, sparse-frequency \(L^p\) improvement, random-sign gain, refined Sobolev estimates, spectral-cluster bounds, and oscillatory large-data mechanisms have direct predecessors. |
| local quantitative synthesis | 本地定量综合 | The admissible label for the three-level certificate and exact matched packaging.  It is not a novelty or priority claim. |

## 2. Required public tokens

```text
periodicHeatBesovEquivalence=VERIFIED_CLASSICAL
ell4ShellExponent=CLOSED_AFTER_AUDIT
exactVectorTripleConvolution=CLOSED_EXACT_EVALUATION
additiveMultiplicityCertificate=CLOSED
supportCardinalityCertificate=CLOSED_SHARP_FROM_SUPPORT_ONLY
matchedSupportMagnitudeQuadraticData=CLOSED_EXACT
matchedPhaseHeatTraceSeparation=CLOSED_AFTER_AUDIT
zeroNonlinearityBoundary=CLOSED
exactConvolutionIsCheapAPrioriProxy=FALSE
failureOfEntranceImpliesUnsafeDynamics=FALSE
uniformL2OnlyStrongRadius=OPEN
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
formulaCertificateValidation=PENDING
formulaCertificatePackage=PRESEAL_PENDING
sourceCommitAssigned=FALSE
finalSeal=FALSE
formalFigurePackage=PRESEAL_PENDING
publicReleaseContent=PENDING
translationPath=LOCAL_DIRECT_NO_DGX
NOT CLAY
```

## 3. Evidence-state vocabulary

| Token | Required interpretation |
| --- | --- |
| `VERIFIED_CLASSICAL` | A primary or authoritative source directly covers the mathematical mechanism.  The local proof fixes normalization but carries no novelty label. |
| `CLOSED_AFTER_AUDIT` | The declared internal implication has passed an independent reconstruction in its stated domain. |
| `CLOSED_EXACT_EVALUATION` | The finite identity is exact, but it evaluates the target norm rather than improving it a priori. |
| `CLOSED_SHARP_FROM_SUPPORT_ONLY` | The stated support-only exponent is valid and is saturated by the declared divergence-free Dirichlet patch. |
| `FALSE` | The forbidden implication is explicitly rejected, not left implicit. |
| `OPEN` | No theorem is asserted.  In particular, arbitrary \(L^2\)-small data are not covered. |
| `FORBIDDEN` | New, first, priority, breakthrough, or near-Clay wording is inadmissible. |
| provenance tokens | They certify byte identity and validation scope only after the recorded package exists; they do not enlarge the analytic result. |

## 4. Forbidden renderings

- Do not translate `critical` as “决定性的”.
- Do not call the exact triple convolution a cheap phase proxy; it is an exact
  Fourier evaluation of the same shell \(L^6\) norm.
- Do not say that the energy spectrum determines, nearly determines, or bounds
  the heat entrance without the additional concentration information.
- Do not say the matched support lies in exactly one arbitrary LP block.  Say
  “one fixed-ratio annulus” or “one dyadic scale”.
- Do not infer a numerical inside/outside decision from \(\asymp1\) without a
  prescribed threshold and strict constants.
- Do not describe a finite formula table or analytic power-law plot as a
  Navier--Stokes simulation.
- Do not interpret failure of the sufficient heat entrance as instability,
  blow-up, singularity, or unsafe dynamics.
- Do not hide that both matched families have zero nonlinearity and globally
  smooth heat-flow evolution.
- Do not claim that support counting, additive multiplicity, random phases,
  Rudin--Shapiro flatness, or heat--Besov equivalence are new.
- Do not mark any seal or public release complete before the corresponding
  provenance record exists.
- Do not state that R0.73R solves, nearly solves, or materially settles the
  Clay Millennium problem.

## 5. Public one-sentence boundary

**Chinese:** R0.73R 把 R0.73Q 的临界热流入口写成逐壳可核查的能量与
集中度预算，并用一对支撑、逐模幅值及全部二次 Sobolev 数据完全相同的
Dirichlet/Rudin--Shapiro 散度零场证明临界热流迹仍可相差
\(m^{2/3}\)；这是一项经典 Besov 机制上的确定性诊断综合，不是
\(L^2\)-only、奇性或 Clay 结论。

**English:** R0.73R rewrites the R0.73Q critical heat-flow entrance as an
auditable shellwise energy--concentration budget and uses a divergence-free
Dirichlet/Rudin--Shapiro pair with identical support, coefficient magnitudes,
and all quadratic Sobolev data to show a remaining \(m^{2/3}\) separation of
the critical heat trace; this is a deterministic diagnostic synthesis on a
classical Besov mechanism, not an \(L^2\)-only, singularity, or Clay result.

## 6. Literature and value boundary

The admissible literature statement is that Chemin--Gallagher already gives
the periodic thermic and dyadic negative Besov definitions; Rudin--Shapiro,
\(\Lambda(p)\), and Khintchine theory already explain sparse or randomized
\(L^p\) gain; refined Sobolev and spectral-projector theory already connect
concentration or curved frequency sets to improved \(L^p\) bounds; and
oscillatory large-data Navier--Stokes solutions already exist.

The permitted value statement is narrower.  R0.73R records a self-contained
three-level Fourier interface, an exact matched phase-separation construction,
and strict failure modes for energy-spectrum-only diagnostics.  This is a
useful bridge and counterexample tool, but it is not yet a high-level
regularity theorem.

## 7. Publication provenance

The provenance fields remain pending until the finite formula package and
formal figure are sealed to an immutable analytic-source commit.

```text
formulaCertificateValidation=PENDING
formulaCertificatePackage=PRESEAL_PENDING
sourceCommitAssigned=FALSE
finalSeal=FALSE
formalFigurePackage=PRESEAL_PENDING
publicReleaseContent=PENDING
translationPath=LOCAL_DIRECT_NO_DGX
```

## 8. Synchronized title

```text
R0.73R | A shellwise phase certificate for the critical heat trace
R0.73R｜能谱看不见的相位：临界热流迹的壳层证书
```
