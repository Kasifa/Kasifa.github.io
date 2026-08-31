# R0.73U evidence and gap matrix

**Status:** analytic derivation, independent readback, exact certificate, and
formal figure complete; bilingual publication and live deployment remain open
release gates

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

| Claim slot | Best current evidence | Confidence | Collision, contradiction, or unresolved gap | Release treatment / next query |
|---|---|---:|---|---|
| Local product tensor versus two-point KHM tensor | Direct Fourier formulas: \(\widehat{u_i u_j}(h)\) is a cross-wave-number convolution, while \(\widehat R_{ij}(k)\) is a same-wave-number covariance; checked against von K\'arm\'an--Howarth 1938 and Hill 2001 | high | The shared words “tensor,” “correlation,” and “hierarchy” create a serious risk of silent conflation | Put both formulas side by side in every long-form account; never cite a KHM result as if it were a theorem about \(P_s(u\otimes u)\) |
| Classical KHM closure boundary | Exact two-point hierarchy in von K\'arm\'an--Howarth 1938 and Hill 2001; Zambrano--Duraisamy 2026 explicitly model the unclosed third-order term for homogeneous isotropic turbulence | high | Statistical homogeneity/isotropy and closure assumptions do not yield a deterministic general 3D Navier--Stokes closure | Label `VERIFIED_CLASSICAL`; use only as the nearest hierarchy comparison |
| Same-scale pressure reconstruction | Pressure Poisson/Riesz formula, parent derivation, and independent pressure-sign audit agree | high | Instantaneous pressure is determined, but its product with signed velocity in the time law remains third order | State “pressure recovered, dynamics not closed”; never infer time autonomy from pressure sufficiency |
| PSD of \(\Theta_s\) and \(\tau_s\) | Nonnegative heat kernel and Jensen; independent covariance reconstruction | high | PSD covariance does not imply sign-definite subgrid flux because incompressible strain is indefinite | Label `INTERNAL_EXACT`; display \(\Pi_s=-\tau_s:\nabla v_s\) beside the positivity statement |
| Exact covariance scale PDE | Two independent semigroup/product derivations of \((\partial_s-\Delta)\tau_s=2\sum_\ell\partial_\ell v_s\otimes\partial_\ell v_s\) | high | It is an evolution in filter scale, not physical time, and it still depends on the signed resolved velocity gradients across scales | Label `INTERNAL_EXACT`; forbid “closed stress evolution” without the qualifier “in filter parameter” |
| Two-level heat-filter identity | Exact semigroup algebra; direct conceptual collision with Germano 1992 | high | Inter-filter composition is not a constitutive law from a single resolved scale | Publish as an exact filtering identity with classical collision, not a closure theorem |
| Exact filtered Navier--Stokes and resolved energy law | Direct filtering and integration by parts; consistent with Germano/Eyink filtering literature | high | \(\nabla\cdot\tau_s\) and the signed flux remain unresolved | Label `VERIFIED_CLASSICAL_RECONSTRUCTION`; no LES-model or sign claim |
| Uniform critical tensor row conditional on \(u\in L_t^4L_x^6\) | PSD trace bound, heat contraction, H\"older, periodic Riesz, and R0.73Q Stokes--HLS map | high | The right side already assumes the classical critical strong norm; the argument is circular for arbitrary energy data | Label `INTERNAL_COROLLARY`/`INTERNAL_CONDITIONAL`; keep the hypothesis in the same sentence as the estimate |
| Energy-only tensor row at fixed positive \(s\) | Energy inequality + Sobolev + heat \(L^1\to L^3\) smoothing + time interpolation | high | \(H_3(s)\asymp s^{-1}\) at short scale, so the norm costs \(s^{-1/2}\) and cannot be passed uniformly to \(s=0\). Infinite-time notation must not assume a global smooth branch | Publish the explicit \((\nu s)^{-1/2}\) loss; next analytic query is whether a time-integrated or cancellation-sensitive state can pay it |
| Centered pressure variance \(\mathcal P_*\) | Gauge invariance and two independent weighted Cauchy/Young derivations | high | Strong formula-level collision with Tran--Yu--Dritschel 2021, who study \(\int p^2|u|^{q-2}\) and velocity--pressure correlations | Label `INTERNAL_COROLLARY` and state the direct classical collision in the same row; novelty and priority claims forbidden |
| Comparison \(\beta_*\le C_R^2A\) | Periodic Riesz, H\"older, and R0.73T definitions; strictness visible for pressure-free shears | high | “Never worse” does not give an a priori bound on \(\int\beta_*dt\); the new notation can obscure that the continuation strength remains classical | Place the missing \(L_t^1\) budget next to the comparison |
| Tensor heat-plane law | Parent product calculation and independent index/sign derivation agree | high | Cubic velocity and pressure--velocity terms remain; replacing pressure by its Riesz formula keeps the expression third order and nonlocal | Label `VERIFIED_CLASSICAL_RECONSTRUCTION`; use it as the exact interface to the parity witness |
| Abstract even-state parity obstruction | \(\Theta_s,\tau_s,p_s\) are even under \(u\mapsto-u\), while the odd nonlinear tangent reverses sign | high | Parity alone would be vacuous if every candidate tangent vanished; the four-site witness is required | Bind the abstract no-go to the exact nonzero witness |
| Four-site witness | Two independent exact sparse-convolution paths and the sealed 75/75 rational certificate agree on \(\widehat T(h_*)=0\), zero viscous coefficient, and \(K=\begin{psmallmatrix}-2&1&0\\1&0&0\\0&0&0\end{psmallmatrix}\) | exact, sealed | The witness is planar and smooth and has no vortex stretching; the finite seal does not certify the continuum PDE proof | Label `INTERNAL_EXACT` with `formalFiniteCertificate=PASS`; do not call it a simulation, singularity, near-singularity, or blow-up example |
| Scope of the tensor no-go | Sign pair gives identical \(\{\Theta_s,\tau_s,p_s\}_{s\ge0}\) and opposite signed tensor tangents | high | It excludes only a single-valued autonomous equality from the even quadratic state. It does not exclude upper bounds; the quadratic tensor can still encode magnitudes of some symmetrized quantities when suitable pairings are supplied | State the allowed and excluded conclusions together; next query may add signed velocity, cubic moments, or flux variables |
| Parabolic coefficient separation | Exact dilation gives \(2\sqrt6Le^{-5\theta}=2\sqrt{6\theta}e^{-5\theta}s^{-1/2}\) at \(s=\theta L^{-2}\) | exact analytic crosscheck | This is a one-coefficient, one-witness cost. It does not prove that every time-integrated estimate or augmented hierarchy loses a derivative | Label `INTERNAL_EXACT_SCALING`; keep “for this coefficient at a fixed parabolic slice” in the conclusion |
| Signed SGS/commutator context | Eyink 1996, Constantin--E--Titi 1994, and Duchon--Robert 2000 show that coarse-grained transfer/defect is cubic and signed under their stated hypotheses | high | Those papers address energy transfer/conservation and do not contain the specific R0.73U finite tensor-tangent witness | Use as classical context, not provenance for the local finite calculation |
| Identical prior package | Bounded search across KHM, filtering, Onsager commutators, and current physical-space closures did not locate the same package | bounded only | Search non-detection cannot prove novelty, priority, non-existence, or completeness | Use `NOT_ESTABLISHED`; permitted wording: “not located in the bounded search” |
| Formal exact certificate | Standard-library exact Gaussian-rational reconstruction; two independent full-map paths; 75/75 checklist; sealed manifest and SHA-256 inventory | high, sealed | The package certifies finite algebra and provenance only, not the continuum derivation, novelty, or regularity | Keep analytic source `84e808d…`, certificate source `6c79f23…`, and package commit `044bfb3…` visible |
| Formal figure | Certificate-backed source data; vector PDF/SVG, 600 dpi PNG, print-size and grayscale QA; 325/325 checks | high, sealed | The plotted parabolic curve is an exact coefficient-level initial-time diagnostic, not a trajectory, simulation, fit, or universal lower bound | Publish the package bound to analytic source `84e808d…` and figure commit `6c20af0…`; retain “exact finite diagnostic, not simulation” in the caption |
| Bilingual/public synchronization | This dictionary and ledger freeze terminology and boundaries | pending | HTML/PDF generation, cross-language equation parity, homepage counters, route inventory, and live Pages readback are not yet verified | Translate locally, compare equation/token parity, then run the normal publication gates |
| Arbitrary-data global regularity | No current row controls the critical norm or removes the \(s^{-1/2}\) energy loss | open | The Clay problem is untouched by the restricted information obstruction | Publish `arbitraryThreeDimensionalGlobalRegularity=OPEN`, `clayConclusion=OPEN`, and `NOT CLAY` |

## Contradiction checks that must remain visible

1. **Pressure recovered versus dynamics unclosed:** these are compatible.
   The quadratic local tensor determines instantaneous pressure, while its
   physical-time law still contains signed third-order information.
2. **PSD stress versus signed transfer:** these are compatible.  A positive
   covariance paired with an indefinite trace-free strain has no fixed sign.
3. **Critical exponent row versus no Clay theorem:** these are compatible.
   The uniform row assumes \(u\in L_t^4L_x^6\); the energy-only row loses
   \(s^{-1/2}\).
4. **Centered improvement versus classical collision:** these are compatible.
   Centering can reduce the weighted pressure variance, but the surrounding
   \(L^4\)/weighted-pressure mechanism is classical and the missing time
   budget remains.
5. **Even-state non-autonomy versus possible estimates:** these are
   compatible.  The sign pair rules out a signed equality from even data; it
   does not rule out absolute or one-sided bounds.
6. **Exponential damping at fixed \(s\) versus \(s^{-1/2}\) parabolic cost:**
   these are compatible.  The latter follows when \(s=\theta L^{-2}\) moves
   with the dilated carrier scale.

## Next bounded research queries

1. Can an explicitly odd third-order heat state be added with a critical norm
   that is not stronger than the R0.73Q/R0.73R exponent line?
2. Can time integration or the \(s\)-Duhamel covariance formula compensate
   for the fixed-slice \(s^{-1/2}\) loss without assuming
   \(L_t^4L_x^6\)?
3. Is there a cancellation-sensitive estimate for
   \(-\tau_s:\nabla v_s\) or the tensor heat-plane flux that survives the
   four-site parity test because it keeps signed data?
4. Can the centered pressure variance be related to a tensor anisotropy or
   alignment quantity that is genuinely controlled by the energy class?
5. Before any stronger public claim, rerun a primary-source collision search
   specifically for Gaussian-filter covariance PDEs and deterministic
   tensor-state non-autonomy.

No query above is asserted to be solvable.  Ordinary translation remains
local and direct; DGX is not used.  No Navier--Stokes simulation is required
for this release, and no entry is a Clay conclusion.
