# R0.73N bilingual terminology ledger

**Status:** canonical terminology and claim-boundary source for the public note

**Scope:** continuum theorem, synchronized-trajectory definitions, independent
and adversarial audits, symmetry and compactness obstruction, bounded
literature audit, validated pre-seal finite diagnostic, formal figure
placeholder, and public-release language

**Release title:** *R0.73N | Fixed-member finite-strain stability and the family-transfer obstruction*

**Public title (zh):** *R0.73N｜固定成员有限应变稳定性与族转移障碍*

**Next release:** PENDING

This ledger fixes the bilingual vocabulary for R0.73N. It does not enlarge
the mathematical theorem and must not be used to merge distinct input and
output topologies.

## 1. Stability and topology terminology

| 中文 | English | Exact usage boundary |
|---|---|---|
| 固定成员 | fixed member | One trajectory \(\overline U_\Lambda\) with one finite \(\Lambda>0\); \(\Lambda\) is not allowed to vary with the perturbation size. |
| 固定轨迹 | fixed trajectory | The exact nonstationary unforced solution through \(\overline U_\Lambda(0)\); it is not an equilibrium or an orbit modulo phase. |
| 从 \(t_0=0\) 出发的前向同步稳定性 | forward synchronized stability from \(t_0=0\) | Reference and perturbed solutions start at the same fixed physical time and are compared at equal later times. No orbital shift and no uniformity over all starting times are asserted. |
| FPS \((X,Z)\) 范数量词 | FPS \((X,Z)\) norm quantifiers | In FPS Definition 2.1, \(X\) is the global solution-regularity class and \(Z\) controls both initial smallness and observed distance. FPS state this for an equilibrium. |
| 全三维同步 \((H^3,H^3)\) 稳定性 | full-three-dimensional synchronized \((H^3,H^3)\) stability | The proved fixed-trajectory theorem: initial smallness and observed distance are both in \(H^3\), and the nearby strong solution is global. |
| 全三维 \(H^3\)-输入/\(L^2\)-输出推论 | full-three-dimensional \(H^3\)-in/\(L^2\)-out corollary | Initial smallness is in \(H^3\), while the synchronized output is observed in \(L^2\). This is a custom mixed-topology corollary, not FPS \((H^3,L^2)\). |
| 平面同步 \((H^3_{\rm pl},L^2_{\rm pl})\) 稳定性 | planar synchronized \((H^3_{\rm pl},L^2_{\rm pl})\) stability | The datum is \(H^3_{\rm pl}\)-regular but is required to be small only in \(L^2_{\rm pl}\); global two-dimensional regularity is used. Both spaces are restricted to the invariant planar subsystem. |
| 全三维 FPS \((H^3,L^2)\) 稳定性 | full-three-dimensional FPS \((H^3,L^2)\) stability | **OPEN.** It would require global \(H^3\) control for arbitrary \(H^3\)-regular perturbations small only in \(L^2\), possibly large in \(H^3\). |
| 共存强解 | coexisting strong solution | A comparison solution that exists strongly on the same interval as the reference solution. |
| 共同强解寿命 | common strong lifespan | The relative \(L^2\) estimate is valid there for arbitrary three-dimensional comparisons. It becomes all-time only in the planar subsystem or inside the proved \(H^3\) tube. |
| 固定距离逃逸 | fixed-distance escape | A perturbation sequence tends to zero in the stated input norm while its output stays above one fixed positive distance for the same background, equation, domain, and norms. |

The following four lines are never to be collapsed:

```text
fixedMemberThreeDimensionalH3SynchronizedStability=CLOSED
fullThreeDimensionalH3InputL2Output=CLOSED_AS_COROLLARY
fixedMemberPlanarL2SynchronizedStability=CLOSED
fullThreeDimensionalFPSH3L2Stability=OPEN
```

## 2. Finite-strain and flow-map terminology

| 中文 | English | Exact usage boundary |
|---|---|---|
| 相对应变能量估计 | relative-strain energy estimate | The exact nonlinear \(L^2\) comparison estimate for \(w=V-\overline U_\Lambda\), valid on the common strong lifespan. |
| 有限累积应变包络 | finite accumulated-strain envelope | \(j(T)=(1-e^{-4T})/4+(1-e^{-16T})/16\), with \(j(\infty)=5/16\). |
| 正的全三维 \(H^3\) 稳定管 | positive full-three-dimensional \(H^3\) stability tube | A sufficient, \(\Lambda\)-dependent neighborhood in which the comparison solution is global and remains synchronized in \(H^3\). It is not asserted optimal. |
| 背景 \(H^4\) 总量 | integrated background \(H^4\) size | \(A_{4,\Lambda}=\int_0^\infty\|\overline U_\Lambda(t)\|_{H^4}\,dt\), bounded by \(489\Lambda/(32\sqrt2)\). |
| 强解定义域 | strong-solution domain | \(\mathcal D_T\) is the set of mean-zero divergence-free \(H^3\) data whose unique strong solution exists on \([0,T]\). |
| \(H^3\)-局部的 \(L^2\)-对-\(L^2\) 弦模量 | \(H^3\)-localized \(L^2\)-to-\(L^2\) chordal modulus | The quotient uses \(L^2\) in numerator and denominator, while the neighborhood shrinks in \(H^3\). The superscript \(2\to2\) does not mean an \(L^2\)-open phase space. |
| \(H^3\)-输入/\(L^2\)-输出局部模量 | local \(H^3\)-input/\(L^2\)-output modulus | The same \(H^3\)-localized definition with \(\|h\|_{H^3}\) in the denominator. |
| 指向放大 | pointed amplification | Amplification measured at \(\overline U_\Lambda(0)\). Its local modulus is finite for every fixed member but grows nonuniformly across the family. |
| 族不等度连续性 | family non-equicontinuity | The pointed maps are not equicontinuous at zero as \(\Lambda\to\infty\). This is not discontinuity at any fixed basepoint. |
| 标记数据集上的非一致连续性 | failure of uniform continuity on the marked data set | One time-\(T_*\) Navier--Stokes flow map sends selected pairs with vanishing \(H^3\) separation to outputs with fixed positive \(L^2\) separation. |
| 同一流映射、不同基点 | same flow map, different basepoints | Viscosity, torus, forcing, and observation time are fixed. \(\Lambda\) labels basepoints of the same partially defined strong-solution map, not different equations or solution maps. |

## 3. Family-transfer obstruction terminology

| 中文 | English | Exact usage boundary |
|---|---|---|
| 族层面偏离 | family-level departure | R0.73M keeps the endpoint distance at order \(\rho\) only while changing the background through \(\Lambda\). |
| 量词交换障碍 | quantifier-exchange obstruction | \(\Lambda\to\infty\) changes the base; fixing one admissible \(\Lambda\) and sending \(\rho\downarrow0\) sends the actual endpoint distance to zero. |
| 族转移障碍 | family-transfer obstruction | The registered R0.73M family cannot be relabeled as instability of one fixed member while retaining one equation, torus, topology, and observation time. |
| 纯振幅偶然性 | amplitude-only accident | Multiplication by \(\Lambda\) preserves the shear background because its self-advection vanishes, but it is not a symmetry of the perturbed nonlinear equation. |
| 时间平移障碍 | time-translation obstruction | The two heat harmonics decay at rates \(4\) and \(16\), so no nonzero shift identifies distinct amplitudes. |
| 抛物缩放障碍 | parabolic-scaling obstruction | Fixed-viscosity scaling changes frequencies, torus representation, observation time, and \(H^3\) size unless the scale is one. |
| 原时刻非紧性 | original-time noncompactness | \(\|\overline U_\Lambda(0)\|_2^2=5\Lambda^2/8\), so the family is unbounded in every fixed Sobolev space. |
| 时间平移紧致性退化 | time-shift compactness degeneration | Every bounded shifted limit loses the second harmonic and therefore loses the certified two-harmonic R0.73M mechanism. |
| 光滑无限块捷径 | smooth infinite-block shortcut | **CLOSED for this route.** Any fixed smooth heat shear still has finite integrated \(H^4\) size and a positive \(H^3\) tube; a different infinite-block mechanism would require a new theorem. |

The obstruction is route-specific. It does not classify every possible fixed
non-autonomous background or every transformation not registered in the
R0.73N audit.

## 4. Exact formulas licensed for publication

The background and finite-strain functions are

\[
 \overline U_\Lambda(t,y)
 =\left(0,0,-\Lambda e^{-4t}\sin2y
 +{\Lambda\over2}e^{-16t}\sin4y\right),
\]

\[
 j(T)={1-e^{-4T}\over4}+{1-e^{-16T}\over16},
 \qquad j(\infty)={5\over16},
\]

and

\[
 A_{4,\Lambda}\le {489\over32\sqrt2}\Lambda.
\]

For every fixed \(\Lambda>0\), the continuum proof gives

\[
 \|w(T)\|_2\le e^{\Lambda j(T)}\|w(0)\|_2
\]

on the common strong lifespan and a sufficient tube

\[
 R_\Lambda={1\over4C_3}e^{-C_3A_{4,\Lambda}}>0,
 \qquad
 \sup_{t\ge0}\|w(t)\|_{H^3}
 \le e^{C_3A_{4,\Lambda}}\|w(0)\|_{H^3}.
\]

At \(T_*=1/1800\), for every sufficiently large \(\Lambda\),

\[
 c_*e^{\Lambda\mathcal A_*}
 \le\mathfrak L_{\Lambda,\mathrm{loc}}^{2\to2}(T_*)
 \le e^{\Lambda j_*},
\]

\[
 {c_*\over C_H}\Lambda^{-2}e^{\Lambda\mathcal A_*}
 \le\mathfrak L_{\Lambda,\mathrm{loc}}^{3\to2}(T_*)
 \le e^{\Lambda j_*},
\]

with the exact compatibility chain

\[
 j_*>{359\over324000}>{173\over450000}>\mathcal A_*.
\]

These brackets are not sharp-exponent or prefactor-limit theorems.

## 5. Evidence-state vocabulary

| Token | Meaning |
|---|---|
| `CLOSED` | A continuum obligation is closed by the analytic proof. |
| `CLOSED_AS_COROLLARY` | A consequence follows from a stronger proved estimate but must retain its own topology label. |
| `PASS` | An independent audit, finite validator, or other frozen gate passed its stated checks. |
| `VALIDATED_PRESEAL` | Internal validators passed, but the package has not yet been bound to the final source commit or granted release-evidence status. |
| `FALSE_AS_INFERENCE` | The proposed implication is invalid; this does not negate unrelated statements. |
| `OPEN` | No theorem is claimed in this release. |
| `PENDING` | The artifact or publication gate has not been completed and must not be described as released. |

The canonical claim-state ledger is

```text
fixedTimeRelativeL2LipschitzBound=CLOSED
finiteAllTimeStrainEnvelope=CLOSED
fixedMemberPlanarL2SynchronizedStability=CLOSED
fixedMemberThreeDimensionalH3SynchronizedStability=CLOSED
fullThreeDimensionalH3InputL2Output=CLOSED_AS_COROLLARY
familyFlowMapNonuniformMarkedBasepointSensitivity=CLOSED
familyDepartureImpliesFixedMemberInstability=FALSE_AS_INFERENCE
singleR073mMemberH3SmallL2FixedDistanceEscape=FALSE
fullThreeDimensionalFPSH3L2Stability=OPEN
optimalFixedMemberStabilityRadius=OPEN
sharpFamilyLipschitzExponent=OPEN
arbitraryFixedBackgroundInstability=OPEN
transverseCriticalNormGrowth=OPEN
finiteTimeSingularity=OPEN
Clay=OPEN
```

## 6. Finite diagnostic and figure language

The current R0.73N finite diagnostic is `VALIDATED_PRESEAL`, not sealed release
evidence. Its primary and independent validators passed, but
`sourceCommitAssigned=false` and `finalSeal=false`; therefore the package
remains `PENDING` for release. The following may be recorded only as pre-seal
observations:

- the package contains 605 source-data rows: 241 strain samples, 243
  cumulative-\(j\) samples, and 121 marked-basepoint samples;
- the exact rational chain and the high-precision value of \(j_*\) pass both
  the primary and independent validators;
- the independent reconstruction uses six sentinel times;
- the package is diagnostic only and does not prove the continuum energy
  estimate, the \(H^3\) tube, a sharp modulus, or any open statement.

The 605 rows and validation outputs do not become publication evidence until
the parent release binds the final source commit and completes the final seal.

The formal figure package is `PENDING`. No figure identifier, caption, file
count, visual QA result, or publication status is frozen in R0.73N at this
stage. Do not infer a formal figure from the diagnostic CSV alone.

```text
finiteDiagnosticValidation=VALIDATED_PRESEAL
finiteDiagnosticPackage=PENDING
sourceCommitAssigned=FALSE
finalSeal=FALSE
formalFigurePackage=PENDING
publicRelease=PENDING
```

## 7. Literature and public-voice boundary

The admissible literature statement is: “No single source in the recorded
bounded search supplies the R0.73N fixed-member theorem and family-transfer
obstruction as a black box.” This is non-exhaustive and carries no novelty,
priority, or first-result claim.

The strongest admissible English summary is:

> Every fixed member of the explicit unforced two-harmonic family has a
> positive full-three-dimensional synchronized \((H^3,H^3)\) stability tube,
> while R0.73M records nonuniform pointed amplification only across the
> unbounded family. The varying-background construction therefore cannot be
> transferred to fixed-member instability by the audited quantifier,
> symmetry, or compactness routes.

The strongest admissible Chinese summary is:

> 对显式无外力双谐波背景族中的每个固定成员，连续统估计给出一个正的
> 全三维同步 \((H^3,H^3)\) 稳定管；R0.73M 的非一致放大发生在随
> \(\Lambda\) 变化的无界背景族上。因此，在已审计的量词交换、精确对称性
> 与紧致性路线内，不能把该族层面结论转移为单个固定成员的不稳定性。

Every public summary must separately retain the custom
\(H^3\)-in/\(L^2\)-out corollary, the planar
\((H^3_{\rm pl},L^2_{\rm pl})\) theorem, and
full-three-dimensional FPS \((H^3,L^2)=\mathrm{OPEN}\).

Forbidden public wording includes:

- “R0.73M proves instability of one fixed background”;
- “full-three-dimensional FPS \((H^3,L^2)\) is closed”;
- “\((H^3,H^3)\), hence FPS \((H^3,L^2)\)”;
- “there is one Navier--Stokes flow map for each \(\Lambda\)”;
- “large finite transient gain is Lyapunov instability”;
- “the radius or either exponential modulus bound is sharp”;
- “the bounded literature search proves novelty or priority”;
- any claim about arbitrary-background regularity, singularity, or resolution
  of the Clay problem.

Every public rendering must retain the literal boundary label `NOT CLAY`.

## 8. Synchronized title

```text
R0.73N | Fixed-member finite-strain stability and the family-transfer obstruction
R0.73N｜固定成员有限应变稳定性与族转移障碍
```
