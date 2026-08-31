# R0.73V claim--source ledger

**Status:** analytic parent derivation, bounded primary-source search,
independent analytic audit, the two-path exact certificate, and the immutable
formal-figure source seal are complete; the publication transaction remains
open

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

## Claim ledger

| ID | Claim | Evidence class | Exact source or proof | Release use and boundary |
|---|---|---|---|---|
| V1 | “Minimal” is used only in the relative sense of the lowest odd polynomial order in the chosen complete second-stress equation. | `SCOPE_DEFINITION` | [Problem freeze](r073v_problem_freeze.md), Section 1 | Does not assert information-theoretic, componentwise, stable, or unique minimality. |
| V2 | With \(N=\mathbb P\nabla\cdot(u\otimes u)\), one has \(N_s=P_sN=\mathbb P\nabla\cdot\Theta_s\). | `INTERNAL_EXACT` | Commutation of \(P_s\), derivatives, and the periodic Leray projector; [analytic proof](r073v_signed_third_order_heat_lift.md), Section 1 | Exact lower-state reconstruction of the filtered nonlinearity; no inverse heat flow is used. |
| V3 | The pressure-aware centered lift \(\chi_s=P_s(u\odot N)-v_s\odot N_s\) obeys \((\partial_s-\Delta)\chi_s=2\sum_\ell\partial_\ell v_s\odot\partial_\ell N_s\), \(\chi_0=0\), and the corresponding \(s\)-Duhamel formula. | `INTERNAL_EXACT_AUDITED` | Two-field heat covariance identity; [analytic proof](r073v_signed_third_order_heat_lift.md), (3.1)--(3.2); [independent audit](r073v_independent_analytic_audit.md), Section 1 | Equation in filter scale, not physical time; uses the smaller-scale path, not only one positive scale. |
| V4 | The exact tensor heat-plane equation is \((\partial_t-\nu\partial_s)\Theta_s=-2\nu G_s-v_s\odot N_s-\chi_s\). | `INTERNAL_EXACT_AUDITED` | Product equation for \(u\otimes u\); [analytic proof](r073v_signed_third_order_heat_lift.md), (3.3)--(3.5); [independent audit](r073v_independent_analytic_audit.md), Section 2 | \(\chi_s\) fills the odd cubic slot, while the even gradient moment \(G_s\) remains. This is not a closed system. |
| V5 | The full heat-scale path recovers \(G_s\) from the bottom derivative \(G_s=\tfrac12P_s[\partial_r\tau_r|_{r=0}]\). | `INTERNAL_EXACT_AUDITED` | R0.73U covariance PDE evaluated at \(r=0\); [analytic proof](r073v_signed_third_order_heat_lift.md), (3.6); [independent audit](r073v_independent_analytic_audit.md), Section 2 | A bottom-scale derivative is not a stable single-positive-scale constitutive law. |
| V6 | The third velocity heat cumulant \(\kappa_{ijk,s}\) satisfies the exact downward-triangular scale PDE in (4.4). | `INTERNAL_EXACT_AUDITED` | Semigroup product lemma and cancellation of the undifferentiated resolved terms; [analytic proof](r073v_signed_third_order_heat_lift.md), Section 4; [independent audit](r073v_independent_analytic_audit.md), Section 3 | No matching primary-source formula was located in the bounded search; no novelty claim follows. |
| V7 | The local velocity third moment reconstructs the cubic transport divergence, but the complete tensor tangent also contains the pressure--velocity term. | `VERIFIED_CLASSICAL_RECONSTRUCTION` | Direct product rule; [analytic proof](r073v_signed_third_order_heat_lift.md), (4.5)--(4.9); Germano 1992 [DOI](https://doi.org/10.1017/S0022112092001733) | A \(\kappa\)-only truncated tensor equation is false. This is not yet a whole-field information no-go. |
| V8 | The pressure-gradient covariance \(\rho_s=P_s(u\odot\nabla p)-v_s\odot\nabla p_s\) has the exact heat covariance PDE (4.8). | `INTERNAL_EXACT_AUDITED` | Two-field heat covariance identity; [analytic proof](r073v_signed_third_order_heat_lift.md), Section 4; [independent audit](r073v_independent_analytic_audit.md), Section 3 | Carries a derivative; no undifferentiated critical norm is asserted. |
| V9 | Germano's complete second-stress equation contains \(\kappa_s\), pressure--velocity covariance \(Q_s\), pressure--strain covariance \(R_s\), gradient covariance, and resolved production. | `VERIFIED_CLASSICAL_INDEX_AUDITED` | Germano 1992, equations (22)--(25), [primary PDF](https://gibbs.science/teaching/les/handouts/germano_1992.pdf); current derivation [Section 5](r073v_signed_third_order_heat_lift.md); [independent index audit](r073v_independent_analytic_audit.md), Section 4 | The local third velocity cumulant alone is not the complete exact stress interface. |
| V10 | \(Q_s\) and \(R_s\) satisfy the two exact heat covariance PDEs (5.3)--(5.4). | `INTERNAL_EXACT_AUDITED` | Apply the covariance lemma to \((p,u_i)\) and \((p,S_{ij})\); [analytic proof](r073v_signed_third_order_heat_lift.md); [independent audit](r073v_independent_analytic_audit.md), Section 3 | These are scale identities for the current physical fields, not autonomous time laws. |
| V11 | If \(u\in L_t^4L_x^6\), then \(\sup_s\|\kappa_s\|_{L_t^{4/3}L_x^2}\le C_\kappa\|u\|_E^3\). | `INTERNAL_CONDITIONAL_AUDITED` | Heat contraction, H\"older, and the R0.73U stress row; [analytic proof](r073v_signed_third_order_heat_lift.md), (6.2); [independent audit](r073v_independent_analytic_audit.md), Section 5 | The hypothesis is the classical critical strong norm; arbitrary-energy regularity does not follow. |
| V12 | Under the same hypothesis, \(\sup_s\|Q_s\|_{L_t^{4/3}L_x^2}\le2C_R\|u\|_E^3\). | `INTERNAL_CONDITIONAL_AUDITED` | Periodic Riesz, heat contraction, and H\"older; [analytic proof](r073v_signed_third_order_heat_lift.md), (6.3)--(6.4); [independent audit](r073v_independent_analytic_audit.md), Section 5 | No analogous derivative-free row is claimed for \(R_s,\rho_s,\chi_s\). |
| V12A | Taking half the trace of the stress equation kills \(R_{ii}\) and gives the exact subgrid-energy equation (6.6), whose third-order flux \(J_k=\tfrac12\kappa_{iik}+Q_k\) lies in conditional \(L_t^{4/3}L_x^2\). | `INTERNAL_CONDITIONAL_AUDITED` | Incompressibility, V9, V11, and V12; [analytic proof](r073v_signed_third_order_heat_lift.md), (6.5)--(6.7); [independent audit](r073v_independent_analytic_audit.md), Section 5 | The production \(-\tau:\nabla v\) is signed and uncontrolled from energy; this is not a regularity criterion. |
| V13 | The raw third heat moment has the exact physical-time equation (7.1), whose nonlinear row is fourth order in velocity. | `INTERNAL_EXACT_AUDITED` | Direct three-factor product law; [analytic proof](r073v_signed_third_order_heat_lift.md), Section 7; [independent audit](r073v_independent_analytic_audit.md), Section 6 | Proves a \(3\to4\) entry for this hierarchy; does not prove fourth-order non-closure. |
| V14 | The compressed raw tangent \(\mathcal C_s=P_s(u\odot N)\) has equation (7.4), with explicit quartic row \(N\odot N+u\odot[\mathcal B(N,u)+\mathcal B(u,N)]\). | `INTERNAL_EXACT_AUDITED` | Bilinear differentiation of \(N=\mathcal B(u,u)\); [analytic proof](r073v_signed_third_order_heat_lift.md), (7.2)--(7.4); [independent audit](r073v_independent_analytic_audit.md), Section 6 | The centered equation reorganizes but does not erase the next level. No universal hierarchy no-go is licensed. |
| V14A | As \(s\downarrow0\), \(\kappa_s=O(s^2)\), while the centered pressure source in the stress equation has the explicit generally nonzero \(O(s)\) term (8.6); the compressed \(\chi_s\) also starts at \(O(s)\). | `INTERNAL_EXACT_AUDITED` | Repeated differentiation of the exact scale PDEs; [analytic proof](r073v_signed_third_order_heat_lift.md), Section 8; [independent audit](r073v_independent_analytic_audit.md), Section 7 | A uniform ratio lower bound requires a nondegenerate witness; the general expansion alone does not assert nonvanishing for every field. |
| V15 | On the R0.73U four-site witness, the velocity-cumulant flux and pressure rows have different exact small-\(s\) orders, \(O(s^2)\) and \(O(s)\), respectively. | `INTERNAL_EXACT_FINITE_SEALED` | Two independent exact implementations and immutable manifest under `research/certificates/r073v/`; [finite audit](r073v_finite_diagnostic_audit.md) | Excludes an \(s\)-uniform absorption of the pressure source by that cumulant-flux coefficient. It is not a whole-field collision. |
| V16 | On the R0.73T six-site witness at output mode zero, the contracted velocity-cumulant flux vanishes while the centered pressure--strain coefficient is nonzero for \(s>0\). | `INTERNAL_EXACT_FINITE_SEALED` | R0.73V two-path certificate, with the R0.73T field reused only as input data; [finite audit](r073v_finite_diagnostic_audit.md) | Permitted conclusion: same-output coefficientwise non-recovery. Forbidden conclusion: two full \(\kappa_s\) fields coincide. |
| V17 | A selected nonlinear physical-time derivative of \(\widehat\kappa_{112,s}(0,2,0)\) on the four-site witness equals \(2iq^2(1-q^2)^2\), hence is nonzero for \(0<s<\infty\). | `INTERNAL_EXACT_FINITE_SEALED` | Formal-polynomial path plus independent finite-\(\varepsilon\) extraction in the sealed certificate; [finite audit](r073v_finite_diagnostic_audit.md) | Certifies a nonzero quartic next-level remainder for the chosen lift, not fourth-order non-closure. |
| V18 | Exact KHM, generalized filtered-moment, LMN, and rigorous moment theories advance to the next order. | `VERIFIED_CLASSICAL` | von K\'arm\'an--Howarth 1938 [DOI](https://doi.org/10.1098/rspa.1938.0013); Hill 2001 [DOI](https://doi.org/10.1017/S0022112001003949); Germano 1992; Fursikov 1993 [DOI](https://doi.org/10.1070/IM1993v041n03ABEH002274) | These objects and hypotheses differ from the deterministic local heat state; they provide context, not the finite witness proof. |
| V19 | The bounded search did not locate the present third heat-cumulant PDE or a universal minimality/no-go theorem for finite local heat-moment states. | `BOUNDED_NEGATIVE_FINDING` | [Primary-literature audit](r073v_primary_literature_audit.md) | Cannot support non-existence, novelty, priority, or first-authorship wording. |
| V20 | Arbitrary-data three-dimensional global regularity and the Clay problem remain open. | `OPEN` | The derivative pressure row, zero-scale energy control, and critical strong-norm budget remain uncontrolled | `NOT CLAY`. |
| V21 | The formal four-panel figure is reconstructed from the sealed two-path certificate and passes 147 checks over 158 source-data rows. | `FORMAL_FIGURE_SOURCE_SEALED` | `figures/r073v/fig-r073v-signed-third-order-interface/`, source commit `680fde5a24834b8e1c877f651eb20b119c671f49`, package commit `b413586aa7a7389f8943acb2469eb28cdbbf31f3` | The plotted curve is a deterministic rendering of a closed formula, not a fit or Navier--Stokes simulation; all finite conclusions remain coefficientwise or selected-coefficient. |

## Current release-binding ledger

```text
problemFreeze=COMPLETE
parentAnalyticDerivation=COMPLETE
independentAnalyticAudit=PASS
primaryLiteratureAudit=BOUNDED_COMPLETE
pressureAwareSignedHeatLift=INTERNAL_EXACT_AUDITED
signedCrossCovarianceScalePDE=INTERNAL_EXACT_AUDITED
quadraticTensorOddSlotRecovered=INTERNAL_EXACT_AUDITED
germanoStressEquation=VERIFIED_CLASSICAL_INDEX_AUDITED
conditionalKappaCriticalRow=INTERNAL_CONDITIONAL_AUDITED
conditionalPressureVelocityCriticalRow=INTERNAL_CONDITIONAL_AUDITED
pressureStrainCriticalRow=OPEN
formalFiniteCertificate=SEALED
formalFigurePackage=PASS
formalFigureChecks=147
formalFigureRows=158
figureSourceCommit=680fde5a24834b8e1c877f651eb20b119c671f49
figurePackageCommit=b413586aa7a7389f8943acb2469eb28cdbbf31f3
publicReleaseTransaction=PENDING
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=FALSE
signedLiftInformationTheoreticMinimality=NOT_ESTABLISHED
signedLiftComponentwiseMinimality=NOT_ESTABLISHED
signedLiftUniqueness=NOT_ESTABLISHED
fullThirdCumulantStateNonAutonomy=NOT_ESTABLISHED
fourthOrderNonClosure=NOT_ESTABLISHED
finiteMomentHierarchyNoGo=NOT_ESTABLISHED
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```

## Evidence rules

1. `INTERNAL_EXACT_AUDITED` means a self-contained parent derivation and a
   separate sign/index readback both pass.  It does not convert the identity
   into a regularity theorem.
2. The compressed \(\chi_s\) and the transparent Germano bundle are two
   representations chosen for different equations.  Neither is called
   uniquely minimal.
3. An exact coefficient omitted by a truncated law proves that truncation
   false.  It does not prove whole-field information non-reconstructibility.
4. A nonzero quartic term in the third-level time equation proves a hierarchy
   entry, not non-closure of the fourth level or every finite hierarchy.
5. Full raw cubic data at \(s=0\) can re-encode signed velocity through
   \(u_a=F_{aii}/\operatorname{tr}(u\otimes u)\) where \(u\ne0\).  Such a
   state is not automatically a reduced closure.
6. The critical \(\kappa,Q\) rows assume \(L_t^4L_x^6\).  The derivative
   pressure and compressed rows remain outside the proved estimate.
7. Ordinary translation is local and direct.  DGX is not used for
   translation or for the current exact finite algebra.
