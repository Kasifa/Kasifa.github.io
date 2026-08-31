# R0.73O bilingual terminology ledger

**Status:** canonical terminology and claim-boundary source for the public note

**Release title:** *R0.73O | Global-orbit stability and a forced Kolmogorov contrast*

**Public title (zh):** *R0.73O｜先验全局轨道稳定性与强迫 Kolmogorov 对照*

**Next release:** R0.73P

This ledger fixes the bilingual vocabulary for R0.73O. It does not enlarge
either theorem, identify a finite matrix with an infinite-dimensional
operator, or transfer a forced conclusion to the unforced Clay equation.

## 1. Unforced orbit and topology

| 中文 | English | Exact usage boundary |
| --- | --- | --- |
| 先验全局轨道 | a priori global orbit | A mean-zero periodic strong solution already known to belong to \(C([0,\infty);H^3)\cap L^2_{\rm loc}H^4\). The theorem does not prove this hypothesis for arbitrary data. |
| 累积 \(H^4\) 作用量 | accumulated \(H^4\) action | \(\mathcal A_4[u]=\int_0^\infty\|u(t)\|_{H^4}\,dt\), proved finite for each a priori global orbit in the stated class. |
| 对全部起始时刻有效的稳定半径 | one stability radius valid for every starting time | One radius depending on the fixed reference orbit works for every \(t_0\ge0\); it is not uniform over all global orbits. |
| 前向同步稳定性 | forward synchronized stability | Reference and comparison solutions are evaluated at the same physical time; no phase or time shift is allowed. |
| 指数同步 | exponential synchronization | The \(H^3\) difference decays exponentially after the chosen starting time. |
| 全三维 \((H^3,H^3)\) 稳定 | full-three-dimensional \((H^3,H^3)\) stability | Initial smallness and observed distance are both measured in \(H^3\). |
| \(H^3\)-输入/\(L^2\)-输出推论 | \(H^3\)-input/\(L^2\)-output corollary | The datum is still required to be small in \(H^3\). This is not an \(L^2\)-only input theorem. |
| 全三维 \(L^2\)-only 输入接口 | full-three-dimensional \(L^2\)-only input interface | **OPEN.** The datum may be smooth and small in \(L^2\) while arbitrarily large in \(H^3\). |
| 全局初值集的 \(H^3\) 开性 | \(H^3\)-openness of the global-data set | A corollary around each already-global datum. It does not prove that every datum lies in that set. |

The topology labels must remain separate:

```text
unforcedGlobalOrbitH3Stability=CLOSED_CONDITIONALLY_AFTER_AUDIT
unforcedH3InputL2Output=CLOSED_AS_COROLLARY
uniformL2OnlyInputThreshold=OPEN_COLLISION_SENSITIVE
arbitraryThreeDimensionalGlobalRegularity=OPEN
```

## 2. Forced Kolmogorov contrast

| 中文 | English | Exact usage boundary |
| --- | --- | --- |
| 强迫 Kolmogorov 平衡态 | forced Kolmogorov equilibrium | \(U_*=(30.12\sin10y,0,0)\) solves the equation with \(f_*=(3012\sin10y,0,0)\). This is a different equation from the unforced Clay problem. |
| 非衰减平衡态 | nondecaying equilibrium | The equilibrium is constant in time and has infinite accumulated strain; this alone is not turbulence or singularity evidence. |
| 平面不变子空间 | invariant planar subspace | \(z\)-independent velocities with zero third component. The nonlinear flow and the selected witnesses stay in this subspace. |
| 正实平面特征值 | positive real planar eigenvalue | At least one eigenvalue of the infinite-dimensional two-dimensional linearized operator is real and strictly positive. No essentially three-dimensional mode is claimed. |
| 组合主来源证书 | composite primary-source certificate | The sign uses Nagatou, Matsuda--Miyatake, Ilyin, and standard compact-resolvent/Riesz-projection continuation. No single checked source carries every parameter and direction claim. |
| 固定 \(L^2\) 逃逸 | fixed \(L^2\) escape | Initial perturbations tend to zero in \(H^3\), while at selected times the distance from the equilibrium is bounded below by one positive \(L^2\) radius. |
| 全局光滑见证 | globally smooth witness | FPS is applied first in two dimensions; classical two-dimensional regularity and constant extension in \(z\) keep every selected witness global and smooth. |
| 全相空间中的平面见证不稳定性 | full-phase-space instability witnessed by planar directions | A planar sequence belongs to the full three-dimensional phase space and suffices for instability there. It does not describe arbitrary nonplanar perturbations. |

The forced labels are:

```text
forcedKolmogorovH3InputL2Escape=CLOSED_BY_COMPOSITE_PRIMARY_SOURCE_CHAIN_AFTER_AUDIT
forcedWitnessSolutionsGlobalSmooth=PLANAR_ONLY
essentiallyThreeDimensionalUnstableMode=OPEN_NOT_NEEDED
forcedConclusionTransfersToClay=FALSE
```

## 3. Spectral-continuation terminology

| 中文 | English | Exact usage boundary |
| --- | --- | --- |
| 临界区间 | rigorous critical interval | \(R_c\in[3.011528364444,3.011528364446]\) is an imported computer-assisted theorem input. |
| 超临界目标参数 | supercritical target parameter | \(R=3.012\), strictly above the rigorous upper endpoint by \(4.71635554\times10^{-4}\). |
| 高参数正谱锚点 | large-parameter positive-spectrum anchor | Ilyin Theorem 5.1, specialized to \(L=2\pi\), gives a positive eigenvalue at a finite sufficiently large Reynolds parameter. |
| 右半平面 Riesz 投影秩 | rank of the right-half-plane Riesz projection | The algebraic multiplicity count used in continuation. It is not the number of distinct eigenvalues. |
| 统一高频谱界 | uniform high-frequency spectral bound | On each compact positive Reynolds interval, all spectrum with nonnegative real part lies in one bounded disk. This makes the Riesz count finite and locally constant away from imaginary-axis crossings. |
| 全 Fourier 扇区 | full Fourier space | The cosine sector, its sine translate, negative longitudinal modes, and the \(m=0\) sector are treated separately; the constant stream-function gauge is removed. |
| 非零虚轴穿越排除 | exclusion of nonzero imaginary-axis crossings | Nagatou proves that an eigenvalue with nonnegative real part is real. |
| 零特征值唯一性 | uniqueness of the neutral value | Matsuda--Miyatake Proposition 1 supplies the only neutral Reynolds value in the \(m=1\) sector and none for \(m\ge2\) at \(\alpha=0.7\). |

## 4. Finite diagnostic language

| 中文 | English | Exact usage boundary |
| --- | --- | --- |
| 有限 Fourier 谱诊断 | finite Fourier spectral diagnostic | A truncated matrix calculation used for sign, scaling, convergence, and implementation checks. |
| 独立广义铅笔重算 | independent generalized-pencil recomputation | A separately assembled \(Ac=\sigma Bc\) path that does not import the producer. |
| 有限临界穿越 | finite critical crossing | The zero of the truncated spectral abscissa. Its agreement with the rigorous interval is diagnostic, not a new proof of that interval. |
| 无量纲增长率 | dimensionless growth rate | \(\sigma\) in the normalized eigenproblem. |
| 物理增长率 | physical growth rate | \(\lambda=AN\sigma=301.2\sigma\) for the registered equilibrium. |
| 平衡后的广义残差 | equilibrated generalized residual | A numerical backward-error measure after spectrum-preserving left row scaling of both \(A\) and \(B\). |

The finite package may record

\[
 \sigma_{\max}^{(120)}=3.7327236415731776\times10^{-5},
 \qquad
 \lambda^{(120)}=0.011242963608418411,
\]

and the independent differences, but every presentation must retain:

```text
finiteFourierDiagnostic=PASS
finiteComputationProvesInfiniteDimensionalSpectrum=FALSE
finiteComputationProvesNonlinearInstability=FALSE
finiteComputationReplacesNagatouCertificate=FALSE
```

## 5. Evidence-state vocabulary

| Token | Meaning |
| --- | --- |
| `CLOSED_CONDITIONALLY_AFTER_AUDIT` | The theorem is proved under an explicit a priori global-orbit hypothesis. |
| `CLOSED_BY_COMPOSITE_PRIMARY_SOURCE_CHAIN_AFTER_AUDIT` | The conclusion follows from a stated combination of external theorems and an audited internal spectral-continuation argument. |
| `PASS` | A validator or independent audit passed its declared scope. |
| `DIAGNOSTIC_ONLY` | The computation may detect mistakes and illustrate scale but carries no continuum proof weight. |
| `OPEN_COLLISION_SENSITIVE` | No theorem is claimed; the bounded literature search found a close collision and must not be read as exhaustive. |
| `FALSE` | The inference is invalid within the frozen equation/topology contract. |

## 6. Literature and public-voice boundary

The admissible literature statement is that the unforced orbit theorem is a
self-contained closure of a classical stability route. Pizzocchero 2021 is a
direct periodic smooth-global-solution collision, and related stability and
eventual-decay results predate R0.73O. No novelty or priority claim is made.

The exact Mucha 2001 theorem quantifiers were not available in the checked
full text. Mucha 2008 shows high-norm dependence in its own accessible
stability theorem. This does not prove that the entire literature lacks a
uniform \(L^2\)-only threshold.

The strongest admissible Chinese summary is:

> 对每条已经先验全局存在的无强迫周期 \(H^3\) 轨道，能量阶梯给出有限的
> 累积 \(H^4\) 作用量和一个对全部起始时刻有效的正 \(H^3\) 同步稳定半径。
> 一个不同的强迫方程则有显式 Kolmogorov 平衡态，其平面光滑扰动可从任意
> 小的 \(H^3\) 输入逃离固定 \(L^2\) 球。前者有先验全局假设，后者含非零
> 外力；两者都不解决任意三维初值的全局正则性。

The strongest admissible English summary is:

> Every a priori global unforced periodic \(H^3\) orbit has finite accumulated
> \(H^4\) action and one positive \(H^3\) synchronization radius valid at all
> starting times. A separate forced Kolmogorov equilibrium has globally smooth
> planar perturbations that are arbitrarily small in \(H^3\) and escape a fixed
> \(L^2\) ball. The first statement assumes global existence and the second uses
> nonzero forcing; neither resolves global regularity for arbitrary 3D data.

Every public rendering must retain the literal label `NOT CLAY`.

## 7. Publication provenance

The finite diagnostic certificate and formal figure are sealed to immutable
source commit `f139c5e707ffdfe855ca114faac669d12e431e59`. These labels certify package
identity and the declared validation scope; they do not enlarge the analytic
theorems.

```text
finiteDiagnosticValidation=PASS
finiteDiagnosticPackage=CLOSED
sourceCommitAssigned=TRUE
finalSeal=TRUE
formalFigurePackage=PASS
publicReleaseContent=READY
```

## 8. Synchronized title

```text
R0.73O | Global-orbit stability and a forced Kolmogorov contrast
R0.73O｜先验全局轨道稳定性与强迫 Kolmogorov 对照
```
