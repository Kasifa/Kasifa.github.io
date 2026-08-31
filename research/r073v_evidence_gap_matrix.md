# R0.73V evidence and gap matrix

**Status:** analytic, two-path exact-certificate, and immutable formal-figure
source gates complete; the public-release gate remains open

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

| Claim slot | Best current evidence | Confidence | Collision, contradiction, or unresolved gap | Required treatment |
|---|---|---:|---|---|
| Meaning of “minimal signed third-order lift” | Polynomial degree in the exact second-order generalized-stress equation | high as a definition | The signed velocity is already odd, and backward heat inversion is injective on smooth data; parity does not prove global or componentwise minimality | Use “canonical lowest odd-order bundle for the chosen stress equation”; forbid unqualified minimality or uniqueness |
| Equation-slot-compressed lift \(\chi_s\) | \(\chi_s=P_s(u\odot N)-v_s\odot P_sN\), with \(N=\mathbb P\nabla\cdot(u\otimes u)\) | high, parent derivation | It is a derivative-carrying cubic tensor and is not automatically in the same \(L_t^{4/3}L_x^2\) flux row as an undifferentiated moment | Use as the primary tensor-tangent lift; keep its norm question separate |
| Compressed lift scale PDE | Two-field heat covariance identity gives \((\partial_s-\Delta)\chi_s=2\sum_\ell\partial_\ell v_s\odot\partial_\ell N_s\) | exact, independently audited | The identity uses the lower-scale path and does not supply a physical-time closure | Label `INTERNAL_EXACT_AUDITED`; do not call it a time closure |
| Recovery of the odd tensor tangent | \((\partial_t-\nu\partial_s)\Theta_s=-2\nu G_s-v_s\odot N_s-\chi_s\) | high, parent derivation | The even gradient moment \(G_s\) remains, and \(\chi_s\) itself needs an evolution | State exact slot recovery together with both remaining gaps |
| Third heat-cumulant scale PDE | Direct product calculation gives (3.2) in the problem freeze | exact, independently audited | No matching primary-source formula was located in the bounded search | Label `INTERNAL_EXACT_AUDITED`; give the complete derivation and make no novelty claim |
| Pressure-cumulant scale PDEs | General two-field heat covariance identity applied to \((p,u_i)\) and \((p,S_{ij})\) | exact, independently audited | \(p\) depends on time and on \(u\), but at each fixed physical time the scale calculation is valid | State that these are \(s\)-equations, not autonomous time laws |
| Exact second-order stress equation | Germano 1992, equations (22)--(25), specialized to \(P_s\) | classical and independently index-audited | No remaining sign/index discrepancy; the pressure rows still carry the analytic loss | Label `VERIFIED_CLASSICAL_INDEX_AUDITED` |
| Velocity cumulant \(\kappa\) alone closes the tensor stress equation | Contradicted at formula level by the exact \(Q\) and \(R\) rows | high at formula level | A missing term in one representation does not prove information-theoretic non-reconstructibility from all other fields | State `KAPPA_ONLY_TRUNCATED_EQUATION=FALSE`; keep stronger equality-state no-go `OPEN` |
| Pressure-aware signed bundle | \((\kappa,Q,R)\) contains every odd cubic object displayed in the Germano second-stress equation | high | Componentwise minimality and uniqueness are not established; an equivalent Leray/Riesz projected lift may compress the bundle | Call it canonical and pressure-aware, not uniquely minimal |
| Critical row for \(\kappa\) | Heat contraction plus \(u^3\in L_t^{4/3}L_x^2\), and lower cumulant products | conditional and independently audited | The row assumes the classical strong norm | Publish only with the hypothesis \(u\in L_t^4L_x^6\) in the same sentence |
| Critical row for \(Q\) | Riesz gives \(p\in L_t^2L_x^3\); multiply by \(u\in L_t^4L_x^6\) | conditional and independently audited | Still conditional on the strong norm; pressure gauge is removed by covariance | Keep `INTERNAL_CONDITIONAL_AUDITED`; no arbitrary-energy conclusion |
| Critical row for \(R\) | None from \(L_t^4L_x^6\) alone | open | \(S(u)\) contains a derivative; treating \(R\) like \(\kappa,Q\) would hide the main loss | Mark `OPEN`; test heat-scale Duhamel and cancellation-sensitive estimates separately |
| Trace projection | \(R_{ii}=0\), and \(J_k=\tfrac12\kappa_{iik}+Q_k\) lies in conditional \(L_t^{4/3}L_x^2\) | high, parent derivation | The scalar equation retains signed production \(-\tau:\nabla v\), and the flux estimate still assumes \(L_t^4L_x^6\) | Publish as an exact scalar interface, not a continuation criterion |
| Heat direction versus physical time | Exact \(s\)-PDEs are downward triangular; raw third and compressed-lift physical-time equations contain quartic terms | high | A full general centered-\(\kappa\) fourth-order index ledger is not written; only a selected coefficient is assigned to the finite gate | Separate the two evolution variables and restrict self-contained claims to the displayed equations |
| Bottom-scale order separation | Heat covariance expansion gives \(\kappa_s=O(s^2)\) and the centered pressure source \(\mathfrak P_s=O(s)\), with explicit leading tensors | high, parent derivation | A ratio lower bound needs a witness on which the relevant leading coefficients do not vanish | Publish the general expansion and bind any \(s^{-1}\) ratio to the exact four-site coefficient |
| Fourth-order nonclosure | Classical KHM/Germano/LMN hierarchy plus direct raw-moment product law | next-level entry exact; nonclosure open | The sealed selected coefficient proves a nonzero quartic remainder, not that fourth-order data cannot close | Publish only `nonzeroQuarticNextLevelRemainder`; keep `fourthOrderNonClosure=NOT_ESTABLISHED` |
| R0.73U witness decomposition | The R0.73V certificate independently rebuilds the full \(\kappa,Q,\Xi\) maps and the compressed lift | exact, sealed | Reuse is restricted to recomputed rows and the final source-bound seal | Cite the new R0.73V manifest and finite audit |
| Formal figure | Four panels are rebuilt from the sealed two-path common core; 158 source-data rows and 147 validation checks are bound to immutable source and package commits | exact, source sealed | The curve is a closed-form renderer sample, not fitted or simulated data; the finite claims remain coefficientwise | Publish the figure with its caption, manifest, source data, QA rasters, and `NOT CLAY` boundary |
| Equality-state collision for \(\kappa\)-only non-sufficiency | No witness yet | open | Raw cubic data plus lower moments can be information-rich; all-scale data may permit unstable inversion | Do not claim a no-go unless the exact collision is found |
| Coefficientwise local-cubic failure | The sealed six-site zero mode has vanishing contracted \(\kappa\)-flux and \(Q\)-divergence but nonzero \(\Xi\) | exact, two-path sealed | It does not compare two whole states and does not exclude whole-field or inverse-heat reconstruction | Call only `sameOutputCoefficientNonRecovery` |
| Primary-source collision | Germano 1992 is direct; Hill 2001, Eyink 1996/2006, Duchon--Robert 2000, LMN and Fursikov moment chains are adjacent | high | The deterministic local heat state differs from two-point or ensemble hierarchies | Keep object distinctions explicit and prohibit novelty/priority claims |
| Arbitrary-data global regularity | No row controls \(R\), the zero-scale limit, or the critical strong norm from energy | open | The cubic lift moves the closure boundary; it does not close it | `arbitraryThreeDimensionalGlobalRegularity=OPEN`, `clayConclusion=OPEN`, `NOT CLAY` |

## Current contradiction checks

1. **Downward heat hierarchy versus upward time hierarchy:** compatible.  The
   former differentiates the filter parameter for fixed physical fields; the
   latter differentiates a nonlinear Navier--Stokes trajectory.
2. **Uniform critical \(\kappa,Q\) rows versus no regularity theorem:** compatible.
   Both rows assume \(u\in L_t^4L_x^6\), and \(R\) still carries a derivative.
3. **Nonzero omitted pressure term versus no information-theoretic no-go:**
   compatible.  A truncated equation is false, but another declared field
   might still reconstruct the omitted term.
4. **Heat injectivity versus closure difficulty:** compatible.  Exact backward
   inversion on smooth data is unbounded and is not a stable same-scale
   constitutive law.

## Next bounded actions

1. Publish the analytic proof, independent audit, exact certificate, figure,
   bilingual note, and cumulative recap as one atomic GitHub transaction.
2. Keep the failed stronger equality-state collision explicit; do not upgrade
   the coefficientwise witness into a whole-field no-go.
3. In the next section, test whether the trace equation can pay the signed
   production \(-\tau:\nabla v\) through heat carré-du-champ or time-integrated
   cancellation without assuming \(L_t^4L_x^6\).

Ordinary translation is performed directly on the local workstation.  DGX is
not used for translation or for the present exact finite algebra.
