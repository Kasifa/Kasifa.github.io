# R0.73X claim--source ledger

**Status:** research freeze complete; Gaussian and pressure-tail independent
audits pass at the stated positive-scale boundary; the real 25-file figure is
source-commit-bound, package-commit sealed, and visually validated, while the
two publication-facing source audits and the public transaction remain pending

**Claim class:** `EXACT IDENTITIES + POSITIVE-SCALE ABSOLUTE SIZE + SCOPED NEGATIVE RESULTS + OPEN COERCIVITY`

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

## Claim ledger

| ID | Claim | Evidence class | Exact source or proof | Release use and boundary |
|---|---|---|---|---|
| X1 | The localized resolved-energy and subfilter ledgers, including the fixed-cutoff centered-increment split, are exact on the smooth lifespan. | `INTERNAL_EXACT_AUDITED` | [Localized ledger](r073x_localized_heat_characteristic.md); [claim-state update](r073x_claim_state_update.md), Section 1 | For suitable weak solutions, the characteristic pullback is distributional only after fixing a positive heat-scale floor. |
| X2 | The exterior functional is explicitly split as \(\mathcal A_{\rm ext}^{\square}=\mathcal G_{u,p}^{\square}+\mathcal H_u^{\square}\). | `INTERNAL_DEFINITION_AUDITED` | [Exterior-tail freeze](r073x_exterior_tail_freeze.md), Sections 2 and 6; [pressure audit](r073x_pressure_tail_independent_audit.md), Section 9 | This is a declared nonlocal input, not a locally controlled small quantity. |
| X3 | Direct heat propagation carries Gaussian annular weights \(\gamma_m(\theta)=\theta^{-2}e^{-4^{m-1}/(32\theta)}\). | `INTERNAL_EXACT_AUDITED` | Kernel calculation in the [exterior-tail freeze](r073x_exterior_tail_freeze.md); [Gaussian proof](r073x_gaussian_velocity_tail_proof.md) | Gaussian decay belongs to the heat operator; it does not create source integrability or smallness. |
| X4 | The harmonic-pressure tail is algebraic: \(\Lambda_R(t)=R\sum_{m\ge1}(2^mR)^{-4}\int_{A_m(R)}|\widetilde u|^2\). | `INTERNAL_EXACT_AUDITED` | Local pressure split and off-diagonal order \(-4\) kernel in the [exterior-tail freeze](r073x_exterior_tail_freeze.md), Section 4; [pressure audit](r073x_pressure_tail_independent_audit.md) | It must not be replaced by a Gaussian tail. |
| X5 | The centered production obeys \(|\mathscr S_s|\le C_0s^{-1/2}P_{2s}(|u|^3)\), with \(C_0=2^{5/2}e^{-1/2}+2^{7/2}/\sqrt\pi<10\). | `INTERNAL_FUNCTIONAL_LEMMA_CERTIFIED` | [Gaussian proof](r073x_gaussian_velocity_tail_proof.md), (1.2)--(1.3); [independent audit](r073x_gaussian_tail_independent_audit.md), Section 5 | Pointwise functional lemma at \(s>0\); no pressure, PDE trajectory, or regularity theorem is used. |
| X6 | The unweighted absolute centered-production tent row closes with a critical Gaussian \(L^3\) velocity tail. | `INTERNAL_POSITIVE_SCALE_SIZE_AUDITED` | [Gaussian proof](r073x_gaussian_velocity_tail_proof.md), (1.7); certificate payload `fcac9744...e3b7` | Finiteness and scale-compatible size only; the tail is not shown small from one cylinder. |
| X7 | The complete exterior centered-production plus pressure-covariance cutoff row is bounded by \(C[\mathcal E^{\square}(z_0,4R)^{3/2}+\mathcal A_{\rm ext}^{\square}]\) for every measurable \(0<s(t)\le\theta R^2\). | `INTERNAL_POSITIVE_SCALE_SIZE_AUDITED` | [Exterior-tail freeze](r073x_exterior_tail_freeze.md), (6.3); [pressure audit](r073x_pressure_tail_independent_audit.md), Sections 9.3--9.5 | The constant is independent of \(R,z_0\), the solution, and the selected measurable scale, but the right side is not proved small. |
| X8 | The full scale-integrated absolute \(\mathscr S_s\) row satisfies the analogous \(\mathcal E^{3/2}+\mathcal A_{\rm ext}\) bound. | `INTERNAL_POSITIVE_SCALE_SIZE_AUDITED` | [Exterior-tail freeze](r073x_exterior_tail_freeze.md), (6.5); [claim-state update](r073x_claim_state_update.md), (U3.4) | Unweighted positive-scale integral only; the extra \(s^{-1/2}\) weighted endpoint remains open. |
| X9 | The periodic pressure-gradient representation has multiplier \(-ik_\ell k_i k_j/|k|^2\), with origin contact terms retained in the complete distribution and absent only after off-diagonal localization. | `INTERNAL_DISTRIBUTIONAL_IDENTITY_AUDITED` | [Exterior-tail freeze](r073x_exterior_tail_freeze.md), Lemma 4.1; [pressure audit](r073x_pressure_tail_independent_audit.md), Section 9.2 | This justifies the algebraic harmonic tail; it is not a pressure-free closure. |
| X10 | \(Q_s=P_s((p-c_R)u)-P_s(p-c_R)P_su\) is gauge-invariant and lies in \(L^1\) under \(p-c_R\in L^{3/2}\), \(u\in L^3\). | `INTERNAL_INTEGRABILITY_AUDITED` | [Exterior-tail freeze](r073x_exterior_tail_freeze.md), Section 5; [pressure audit](r073x_pressure_tail_independent_audit.md), Section 9.3 | The source norm is explicitly paid; heat decay alone does not control it. |
| X11 | A fixed positive harmonic probe refutes an amplitude-independent comparison of cubic production or centered remainder with \(\nu D+R^{-2}k\). | `INTERNAL_EXACT_FINITE` | [Finite diagnostic design](r073x_finite_diagnostic_design.md); [finite harness report](r073x_finite_fourier_harness_report.md) | The probe is periodic and positive but not compactly supported; compact-cutoff absorption remains open. |
| X12 | A translated compact packet refutes an exterior-free velocity-only functional bound and a weighted-\(L^2\)-mass-to-\(3/2\) replacement. | `FUNCTIONAL_COUNTEREXAMPLE_SCOPED` | [Counterexample audit](r073x_exterior_tail_counterexample_audit.md) | It is a static divergence-free triple with \(p=\mu=0\), generally not an unforced NSE trajectory; no associated-pressure or NSE-only inequality is refuted. |
| X13 | The Gaussian certificate independently derives annular constants, concentration exponents, quadrature slopes, interpolation powers, and lifted-tail summability. | `INTERNAL_SECOND_PRODUCER_PASS` | [Certificate report](r073x_gaussian_tail_certificate_report.md); [independent audit](r073x_gaussian_tail_independent_audit.md), Section 5 | It certifies the functional tail lemma, not pressure closure or PDE regularity. |
| X14 | Primary literature owns local coarse-grained energy balances, local pressure/harmonic decompositions, heat off-diagonal bounds, and positive CKN/Koch--Tataru interfaces. | `VERIFIED_CLASSICAL_CONTEXT` | [Primary literature audit](r073x_primary_literature_audit.md); [pressure source ledger](r073x_pressure_tail_primary_source_ledger.md) | R0.73X is a localized heat-coordinate synthesis and size lemma; novelty or priority claims are forbidden. |
| X15 | The bounded search did not locate the implication from signed heat-characteristic payment to local absolute/tent smallness and then to a CKN epsilon scale. | `BOUNDED_NEGATIVE_FINDING` | [Primary literature audit](r073x_primary_literature_audit.md), (2.1) | Non-detection is not proof of novelty, priority, non-existence, or first authorship. |
| X16 | Small signed payment does not presently imply small \(\mathcal E^{3/2}+\mathcal A_{\rm ext}\). | `OPEN` | [Claim-state update](r073x_claim_state_update.md), (U6.1) | This is the exact coercivity bridge left for R0.73Y. |
| X17 | Weighted tent/Carleson control, compact-cutoff absorption, suitable-weak \(s=0\) passage, epsilon regularity, arbitrary-data global regularity, and the Clay conclusion remain open. | `OPEN` | [Claim-state update](r073x_claim_state_update.md), Section 7 | `NOT CLAY`. |
| X18 | The formal figure is a deterministic rendering of frozen definitions and certificate rows, with source data, PDF/PNG/SVG, monitoring logs, manifest, validation, and source audit. | `FORMAL_FIGURE_SEALED_COMMIT_BOUND` | Real 25-file package `figures/r073x/fig-r073x-exterior-tail-ledger/`; portable source/raw commit `161fd9d5...ecfb`; child package commit `d11025bb...aa5` | All 21 source/raw paths are byte-bound to the first commit; the four metadata files complete the child seal; owner visual QA and 50/50 validation pass. Publication remains fail-closed until both publication-facing source audits and later release pins pass; no placeholder asset is allowed. |

## Current release-binding ledger

```text
problemFreeze=COMPLETE
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
navierStokesSimulation=NOT_RUN
directNumericalSimulation=NOT_RUN
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```

## Evidence rules

1. `INTERNAL_POSITIVE_SCALE_SIZE_AUDITED` means the exact positive-scale
   quantifiers, scale factors, pressure gauge, and exterior functional passed
   independent readback. It does not mean smallness, absorption, or coercivity.
2. Gaussian heat tails and algebraic harmonic-pressure tails are different
   mechanisms and must remain separate in every public display.
3. The static packet has exactly the functional quantifiers stated in X12.
   It must never be described as an NSE counterexample, a singular trajectory,
   or a blow-up witness.
4. A signed characteristic payment is not an absolute tent norm. The open
   bridge may not be hidden inside a constant or a change of terminology.
5. Ordinary Chinese--English translation is performed directly on the local
   workstation; DGX is not used for translation.
