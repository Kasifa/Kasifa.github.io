# R0.73P bilingual dictionary and public-claim boundary

**Status:** canonical terminology for HTML/PDF rendering

**Release title:** R0.73P | Critical stability, the N^{-1/2} frequency gate, and the early-time regularity gap

**Public title (zh):** R0.73P｜临界稳定、N^{-1/2} 频率门槛与早期正则缺口

**Next release:** R0.73Q

## 1. Mathematical terms

| English | Chinese | Required meaning |
| --- | --- | --- |
| critical \(H^{1/2}\) stability tube | 临界 \(H^{1/2}\) 稳定管 | A sufficient open neighborhood in the critical Sobolev topology |
| all-time weak relative-energy stability | 全时弱相对能量稳定 | \(L^2\) comparison for every Leray--Hopf selection; no early strong-regularity claim |
| band-limited perturbation | 带限扰动 | Fourier support contained in \(0<|k|\le N\) |
| \(N^{-1/2}\) critical frequency gate | \(N^{-1/2}\) 临界频率门槛 | Sufficient \(L^2\) threshold obtained by entering the critical tube |
| \(N^{-3}\) immediate \(H^3\) gate | \(N^{-3}\) 即时 \(H^3\) 门槛 | Sufficient \(L^2\) threshold obtained by direct entry into the R0.73O tube |
| higher-norm envelope | 高阶范数包络 | A stated bound \(|w_0|_s\le M\); not implicit smoothness |
| critical tail certificate | 临界尾部证书 | An upper bound on \(|Q_{>N}w_0|_{1/2}\) combined with low-frequency energy |
| norm-transfer sharpness | 范数换算锐性 | Equality-level saturation of the Fourier embedding; not PDE necessity |
| one-sided delayed synchronization | 单侧延迟同步 | Every Leray selection compared with one fixed global strong reference after a common delay |
| early weak interval | 早期弱阶段 | The interval before guaranteed eventual regularity; singularity/uniqueness remain unknown there |
| collision-sensitive | 文献碰撞敏感 | A claim whose exact prior theorem quantifiers have not been completely excluded |
| classical corollary | 经典推论 | A result obtained by combining verified published theory with the current hypotheses |

## 2. Required public tokens

```text
allTimeWeakL2RelativeStability=CLOSED_AFTER_AUDIT
globalCriticalH12OrbitStability=CLOSED_AS_CLASSICAL_COROLLARY
criticalH12Synchronization=CLOSED_AFTER_AUDIT
criticalToGlobalH3Propagation=CLOSED_AS_CLASSICAL_COROLLARY
bandLimitedL2ThresholdNMinusHalf=CLOSED_AS_COROLLARY
mixedL2HsThreshold=CLOSED_AS_COROLLARY
lowHighCriticalTailCertificate=CLOSED_AS_COROLLARY
uniformEventualRegularityOnL2Ball=CLOSED_AFTER_AUDIT
uniformEventualSmallH3Entry=CLOSED_AFTER_AUDIT
oneSidedDelayedL2ToH3Synchronization=CLOSED_AFTER_AUDIT
normTransferNMinusHalfSharp=CLOSED
PDEDynamicalNMinusHalfSharp=NOT_CLAIMED
arbitraryLerayPairLipschitzSemigroup=NOT_PROVED
uniformL2OnlyStrongThreshold=OPEN_COLLISION_SENSITIVE
earlyWeakIntervalRegularity=OPEN
backwardRegularityInference=NOT_AVAILABLE
arbitraryThreeDimensionalGlobalRegularity=OPEN
finiteAnalyticFigureProvesPDEThresholdNecessity=FALSE
formulaDiagnosticValidation=PASS
formulaDiagnosticPackage=CLOSED
sourceCommitAssigned=TRUE
finalSeal=TRUE
formalFigurePackage=PASS
publicReleaseContent=READY
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```

## 3. Forbidden renderings

- Do not translate `critical` as “决定性的”; here it means scaling-critical.
- Do not translate `eventual regularity` as “global regularity”; use “最终正则” or “晚时正则”.
- Do not call the \(N^{-1/2}\) exponent a PDE-optimal threshold.
- Do not call a single Fourier mode an instability or singularity witness.
- Do not write that every Leray--Hopf solution is unique after comparing two arbitrary weak branches.
- Do not infer initial-time smoothness from delayed Gevrey regularity.
- Do not state that Mucha 2001 has a frequency-independent threshold until its full quantifiers are read.
- Do not claim a new Fujita--Kato, Serrin, or eventual-regularity theorem.
- Do not state that R0.73P solves or nearly solves the Clay problem.

## 4. Public one-sentence boundary

**Chinese:** R0.73P 把带限扰动的充分 \(L^2\) 门槛高频幂次从 \(N^{-3}\) 改进到临界的 \(N^{-1/2}\)，并证明所有弱分支晚时同步；但无频率条件的初时刻强正则仍然开放。

**English:** R0.73P improves the high-frequency exponent in the sufficient band-limited \(L^2\) gate from \(N^{-3}\) to the critical \(N^{-1/2}\) scale and proves delayed synchronization of every weak branch, while initial-time strong regularity without frequency control remains open.

## 5. Publication provenance

The formula-diagnostic certificate and formal figure are sealed to immutable
source commit `c087845e65034d2ba92b8a8330d90e36e77704d3`.  These labels certify
package identity and the declared validation scope; they do not enlarge the
analytic theorems.

```text
formulaDiagnosticValidation=PASS
formulaDiagnosticPackage=CLOSED
sourceCommitAssigned=TRUE
finalSeal=TRUE
formalFigurePackage=PASS
publicReleaseContent=READY
```

## 6. Synchronized title

```text
R0.73P | Critical stability, the N^{-1/2} frequency gate, and the early-time regularity gap
R0.73P｜临界稳定、N^{-1/2} 频率门槛与早期正则缺口
```
