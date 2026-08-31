# R0.73P gap matrix

**Status:** analytic synthesis and independent readback complete;
formula-diagnostic and publication audits pending

| ID | Interface | Status | Exact content | Excluded inference |
| --- | --- | --- | --- | --- |
| P1 | All-time weak \(L^2\) relative stability | **CLOSED AFTER AUDIT** | Every Leray--Hopf comparison solution obeys relative energy and exponential \(L^2\) decay against the fixed global strong orbit | Does not make the comparison solution strong during its early weak interval |
| P2 | Global \(H^{1/2}\) orbit tube | **CLOSED AS CLASSICAL COROLLARY** | Burczak--Zaj\k{a}czkowski plus finite \(\int_0^\infty|u|_1^4\) gives one radius valid for every starting time | Not a new critical robustness theorem |
| P3 | Critical exponential synchronization | **CLOSED AFTER AUDIT** | Retaining Poincare damping in the published critical difference inequality gives exponential decay | Requires a smaller critical radius; no numerical constant claimed without full normalization |
| P4 | Critical data in \(H^3\) remain globally \(H^3\) | **CLOSED AS CLASSICAL COROLLARY** | \(L^\infty H^{1/2}\cap L^2H^{3/2}\subset L^4L^6\) is a Serrin class | Does not apply to an initial datum known only in \(L^2\) |
| P5 | Band-limited \(L^2\) gate | **CLOSED AS COROLLARY** | \(\operatorname{supp}\widehat w_0\subset\{|k|\le N\}\) and \(\|w_0\|_2<R_{1/2}N^{-1/2}\) imply global strong continuation | The \(N^{-1/2}\) exponent is not claimed dynamically necessary |
| P6 | Mixed \(L^2+H^s\) gate | **CLOSED AS COROLLARY** | \(\|w_0\|_2<R_{1/2}^{2s/(2s-1)}M^{-1/(2s-1)}\) when \(|w_0|_s\le M\) | Depends on the higher-norm envelope and is not \(L^2\)-only |
| P7 | Low/high critical-tail certificate | **CLOSED AS COROLLARY** | \(N\|w_0\|_2^2+|Q_{>N}w_0|_{1/2}^2<R_{1/2}^2\) is sufficient | A high-frequency lower cutoff or tail \(L^2\) norm alone is insufficient |
| P8 | Uniform eventual regularity on an energy ball | **CLOSED AFTER AUDIT** | Every Leray selection with \(\|v_0\|_2\le M\) is strong after a common upper time \(T_{\rm reg}(M)\) | Individual entry times may depend on the selected weak solution |
| P9 | One-sided delayed \(L^2\to H^3\) synchronization | **CLOSED AFTER AUDIT** | Relative to a fixed global strong reference, every Leray selection in the energy ball satisfies a delayed \(H^3\) Lipschitz estimate | Does not create a Lipschitz semigroup between arbitrary weak selections |
| P10 | Sharpness of \(N^{-1/2}\) | **CLOSED FOR NORM TRANSFER ONLY** | A single Fourier mode attains \(|w|_{1/2}=N^{1/2}\|w\|_2\) | The same mode is a smooth shear and cannot prove PDE failure above the gate |
| P11 | Uniform \(L^2\)-only strong threshold from the initial time | **OPEN / COLLISION-SENSITIVE** | No verified proof or counterexample | At the zero background it is a supercritical small-energy regularity problem |
| P12 | Backward inference from eventual regularity | **NOT AVAILABLE** | Later Gevrey regularity alone gives no information that eliminates an earlier singular interval | “Eventually smooth” cannot be rewritten as “always smooth” |
| P13 | Arbitrary three-dimensional global regularity | **OPEN** | No change | NOT CLAY |

## Release ledger

```text
allTimeWeakL2RelativeStability=CLOSED_AFTER_AUDIT
globalCriticalH12OrbitStability=CLOSED_AS_CLASSICAL_COROLLARY
criticalH12Synchronization=CLOSED_AFTER_AUDIT
globalH3PropagationFromCriticalSolution=CLOSED_AS_CLASSICAL_COROLLARY
bandLimitedL2ThresholdNMinusHalf=CLOSED_AS_COROLLARY
mixedL2HsThreshold=CLOSED_AS_COROLLARY
lowHighCriticalTailCertificate=CLOSED_AS_COROLLARY
uniformEventualRegularityOnL2Ball=CLOSED_AFTER_AUDIT
oneSidedDelayedL2ToH3Synchronization=CLOSED_AFTER_AUDIT
arbitraryLerayPairLipschitzSemigroup=NOT_PROVED
normTransferNMinusHalfSharp=CLOSED
PDEDynamicalNMinusHalfSharp=NOT_CLAIMED
uniformL2OnlyStrongThreshold=OPEN_COLLISION_SENSITIVE
earlyWeakIntervalRegularity=OPEN
backwardRegularityInference=NOT_AVAILABLE
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
```
