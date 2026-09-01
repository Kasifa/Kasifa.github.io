# R0.73W claim--source ledger

**Status:** parent derivation and independent analytic audit complete;
two-path finite sealing and formal-figure sealing remain pending

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

## Claim ledger

| ID | Claim | Evidence class | Exact source or proof | Release use and boundary |
|---|---|---|---|---|
| W1 | The frozen production convention is \(\Pi_s=-\tau_s:\nabla v_s\); positive \(\Pi_s\) is a sink in the resolved-energy equation. | `SCOPE_DEFINITION` | [Problem freeze](r073w_problem_freeze.md), Section 1; [parent proof](r073w_signed_production_heat_characteristic.md), Section 1 | Every imported LES formula must first be converted to this stress and flux convention. |
| W2 | The heat stress satisfies the forced diffusion equation and exact Duhamel formula (2.1)--(2.2). | `VERIFIED_CLASSICAL_REDERIVED` | Direct heat-product calculation; Johnson 2020, equations (9)--(10), after \(s=\ell^2/2\); [parent proof](r073w_signed_production_heat_characteristic.md), Section 2 | Established Gaussian-filter identity; no novelty or priority wording is permitted. |
| W3 | \(\tau_s(x)\) is positive semidefinite. | `INTERNAL_EXACT` | Jensen/variance identity (2.3) in the [parent proof](r073w_signed_production_heat_characteristic.md) | Positivity of stress is not positivity of production. |
| W4 | Only the deviatoric heat covariance contributes: \(\Pi_s=-\tau_s^\circ:S_s\). | `VERIFIED_CLASSICAL_REDERIVED` | Incompressibility and symmetry; [parent proof](r073w_signed_production_heat_characteristic.md), (2.4); Johnson 2020--2021 for the multiscale deviatoric mechanism | The obstruction is signed alignment with trace-free strain. |
| W5 | The local filtered resolved-energy equation is (3.2). | `VERIFIED_CLASSICAL_REDERIVED` | Filtered Navier--Stokes equation and product rule; standard coarse-grained energy balance; [parent proof](r073w_signed_production_heat_characteristic.md), Section 3 | Local equation retains spatial transport and signed transfer. |
| W6 | Combining physical viscosity with the heat-scale energy identity gives \((\partial_t-\nu\partial_s)e_s+\nabla\cdot F_s=-\Pi_s\). | `INTERNAL_EXACT_AUDITED` | Subtract \(\nu(\partial_se_s=\Delta e_s-|\nabla v_s|^2)\) from W5; [parent proof](r073w_signed_production_heat_characteristic.md), (3.3)--(3.4); [independent audit](r073w_independent_analytic_audit.md), Section 2 | Exact heat-plane rewrite; a bounded negative search is not a novelty proof. |
| W7 | Along \(s'(t)=-\nu\), the spatially averaged signed production equals the resolved-energy drop (3.6). | `INTERNAL_EXACT_AUDITED` | Spatial integration of W6 and the chain rule; [parent proof](r073w_signed_production_heat_characteristic.md), (3.5)--(3.6); [independent audit](r073w_independent_analytic_audit.md), Section 2 | Controls the signed integral only; for Leray--Hopf endpoints at \(s=0\), energy equality must not be assumed. |
| W8 | The energy class gives \(\|\Pi_s\|_{L^1_{t,x}}\lesssim s^{-1/4}\|u\|_{L_t^\infty L_x^2}\|\nabla u\|_{L^2_{t,x}}^2\) for \(0<s\le1\). | `INTERNAL_UNCONDITIONAL_AUDITED` | Exact stress Duhamel, \(\|\tau_s\|_1\le2s\|\nabla u\|_2^2\), heat \(L^2\to L^\infty\) with one derivative, and Hölder; [parent proof](r073w_signed_production_heat_characteristic.md), Section 4; [independent audit](r073w_independent_analytic_audit.md), Section 3 | Uses only the Leray--Hopf energy class. It is not uniform at zero scale, and optimality is not claimed. |
| W9 | Integrating W8 in heat scale gives an \(S^{3/4}\) bound. | `INTERNAL_UNCONDITIONAL_AUDITED` | Integrate \(s^{-1/4}\) on \((0,S)\); [parent proof](r073w_signed_production_heat_characteristic.md), (4.4); [independent audit](r073w_independent_analytic_audit.md), Section 3 | Establishes scale integrability, not a scale-critical continuation criterion. |
| W10 | The declared rank-three-support trigonometric polynomial has \(\langle\Pi_s(u_A)\rangle=\frac14A^3e^{-2s}(1-e^{-2s})\), and changing \(A\) to \(-A\) changes the sign. | `INTERNAL_EXACT_FINITE_PENDING_SEAL` | Two independent exact finite producers under `research/certificates/r073w/`; [problem freeze](r073w_problem_freeze.md), Section 4 | Once sealed, disproves a universal pointwise or mean one-sided sign. It is not a PDE trajectory or blow-up candidate. |
| W11 | The same witness has \(\langle D_{ii,s}\rangle=\frac12A^2(1-q^2)(13+12q^2+10q^4+4q^6)\). | `INTERNAL_EXACT_FINITE_PENDING_SEAL` | Two-path exact certificate; [parent proof](r073w_signed_production_heat_characteristic.md), (5.3)--(5.5) | Positive quadratic comparison row for the narrowly stated absorption test. |
| W12 | No amplitude-independent constant can make \(|\langle\Pi_s\rangle|\le C\nu\langle D_{ii,s}\rangle\) hold for all smooth data at fixed \(s>0\). | `INTERNAL_EXACT_FINITE_PENDING_SEAL` | W10 is cubic in \(A\), W11 is quadratic; exact ratio (5.6) | Refutes only this declared same-time quadratic absorption. It does not exclude nonlinear, time-integrated, or localized estimates. |
| W13 | Local subgrid transfer can take both signs in turbulent data. | `VERIFIED_EMPIRICAL_CONTEXT` | Alexakis--Chibbaro 2020, *Physical Review Fluids* **5**, 094604; later primary filtering studies | Context only; the exact finite witness, not DNS evidence, proves the universal-sign counterexample used here. |
| W14 | The bounded primary-source search did not locate the exact combined heat-characteristic display W6, the exact energy-class statement W8, or the critical weighted display W21 in the inspected sources. | `BOUNDED_NEGATIVE_FINDING` | [Primary-literature audit](r073w_primary_literature_audit.md) | Non-detection cannot establish novelty, priority, non-existence, or first authorship. |
| W15 | Arbitrary-data three-dimensional global regularity and the Clay problem remain open. | `OPEN` | W7 uses signed cancellation; W8 loses \(s^{-1/4}\); no localized scale-critical closure has been proved | `NOT CLAY`. |
| W16 | The formal figure is a deterministic rendering of exact identities and certificate formulas. | `FORMAL_FIGURE_PENDING` | Future package under `figures/r073w/` | It will not be described as DNS, fitting, or a Navier--Stokes time simulation. |
| W17 | With \(K_{j,s}=\kappa_{iij,s}/2\), one has \(\Pi_s=\partial_jK_{j,s}+\mathscr S_s\), where \(\mathscr S_s=(4s)^{-1}\int y\cdot a_s|a_s|^2g_s\,dy\). | `INTERNAL_EXACT_AUDITED` | Direct differentiation of the centered third moment and integration by parts; [parent proof](r073w_signed_production_heat_characteristic.md), (6.1)--(6.4); [independent audit](r073w_independent_analytic_audit.md), Section 4 | Exact finite-scale increment split; related coarse-grained increment formulas are classical. |
| W18 | Substitution of W17 into the R0.73V trace equation cancels \(K_s\) and leaves \(\partial_tk_s+\nabla\cdot(v_sk_s+Q_s-\nu\nabla k_s)=-\nu D_{ii,s}+\mathscr S_s\). | `INTERNAL_EXACT_AUDITED` | [Parent proof](r073w_signed_production_heat_characteristic.md), (6.5)--(6.6); [independent audit](r073w_independent_analytic_audit.md), Section 5 | Separates transport, a nonnegative quadratic covariance, and one signed remainder; no absorption follows. |
| W19 | \(D_{ii,s}=2\int_0^sP_{s-r}|\nabla^2v_r|_F^2dr\ge0\). | `INTERNAL_EXACT_AUDITED` | Apply the two-field heat covariance identity to every \(\partial_k u_i\); [parent proof](r073w_signed_production_heat_characteristic.md), (6.7); [independent audit](r073w_independent_analytic_audit.md), Section 5 | Carré-du-champ representation for the trace only; \(\partial_s\tau_s\) itself need not be pointwise positive semidefinite. |
| W20 | The spatial mean obeys \(\langle\Pi_s\rangle=\langle e^{-2sL}u,(u\cdot\nabla)u\rangle\), hence any convergent scale weight gives the multiplier identity (7.3). | `INTERNAL_EXACT_AUDITED` | Periodic integration by parts and self-adjointness of \(P_s\); [parent proof](r073w_signed_production_heat_characteristic.md), Section 7; [independent audit](r073w_independent_analytic_audit.md), Section 6 | Periodic or boundary-decaying spatial statement; not a pointwise formula. |
| W21 | At weight \(s^{-1/2}\), the mean production becomes \(\sqrt{\pi/2}\langle L^{-1/2}u,(u\cdot\nabla)u\rangle\), a zero-order Riesz trilinear form bounded by \(C\|u\|_3^3\). | `INTERNAL_CRITICAL_AUDITED` | Gamma integral, spectral calculus, Riesz boundedness, and \(H^{1/2}\hookrightarrow L^3\); [parent proof](r073w_signed_production_heat_characteristic.md), (7.4)--(7.8); [independent audit](r073w_independent_analytic_audit.md), Section 6 | Recovers classical critical small-data structure; it is not arbitrary-energy coercivity. |
| W22 | Energy solutions satisfy the time-integrated critical-scale bound (7.9). | `INTERNAL_ENERGY_CLASS_AUDITED` | Interpolate \(L^3\) between \(L^2\) and \(L^6\), then use Hölder in time and the energy inequality; [independent audit](r073w_independent_analytic_audit.md), Section 7 | The absolute value is taken after signed spatial and scale integration, not before. |

## Current release-binding ledger

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
formalFiniteCertificate=COMPUTED_HASH_BOUND_PENDING_COMMIT_SEAL
formalFigurePackage=PENDING
publicReleaseTransaction=PENDING
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=false
fixedScaleUniformEnergyClassControl=OPEN
localizedScaleCriticalControl=OPEN
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```

## Evidence rules

1. `VERIFIED_CLASSICAL_REDERIVED` means the current notation has a complete
   derivation and a primary source owns the underlying established identity.
2. `INTERNAL_EXACT_PENDING_AUDIT` is not promoted until an independent
   sign/index readback agrees with the parent proof.
3. `INTERNAL_EXACT_FINITE_PENDING_SEAL` requires two independent producers,
   byte-identical common cores, immutable source and result pins, and a final
   reader audit.
4. A characteristic identity for a signed spatial mean is not an estimate for
   \(|\Pi_s|\) and is not a local regularity criterion.
5. A finite smooth field can disprove a universal theorem.  It cannot by
   itself establish generic turbulent behavior, singularity, or minimality.
6. Ordinary Chinese--English translation is performed directly on the local
   workstation.  DGX is not used for translation or this exact finite algebra.
