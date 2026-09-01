# R0.73W evidence and gap matrix

**Status:** parent derivation, independent analytic audit, commit-bound finite
seal, and immutable formal-figure source/package seal complete; the public
release transaction is ready

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

| Claim slot | Best current evidence | Confidence | Collision, contradiction, or unresolved gap | Required treatment |
|---|---|---:|---|---|
| Gaussian stress scale equation | Exact heat-product rule and Johnson 2020 equations (9)--(10) after normalization | classical, high | No substantive collision | Attribute Johnson; do not claim novelty |
| Stress positivity | Heat-kernel variance formula | exact | A positive semidefinite stress contracted with trace-free strain has no fixed sign | State positivity and the sign limitation together |
| Deviatoric production formula | \(\operatorname{tr}S_s=0\), so the isotropic stress cancels | exact | The remaining deviatoric alignment is indefinite | Treat alignment as the obstruction, not covariance positivity as a cure |
| Local heat-plane identity | Filtered energy balance minus the heat-scale identity | exact, independently audited | Weak-solution use must stay away from \(s=0\) unless endpoint equality is known | Preserve the weak-solution boundary in public prose |
| Spatial characteristic payment | Integrate the local identity and follow \(s'(t)=-\nu\) | exact parent derivation | It controls only signed spatial mean; a characteristic ending at \(s=0\) needs care for weak solutions | State smooth endpoint theorem and positive-scale Leray--Hopf version separately |
| Fixed-scale energy-class absolute bound | Stress Duhamel gives \(\|\tau_s\|_1\lesssim s\|\nabla u\|_2^2\), while one differentiated heat kernel gives \(\|\nabla P_su\|_\infty\lesssim s^{-5/4}\|u\|_2\) | exact, independently audited | The bound grows like \(s^{-1/4}\); exponent optimality has not been proved | Publish as an unconditional bound with no optimality claim |
| Heat-scale integral | \(\int_0^S s^{-1/4}ds=(4/3)S^{3/4}\) | exact consequence | Scale integrability alone is not a scale-invariant epsilon criterion | State exactly what is integrated and what remains uncontrolled |
| Centered third-moment split | Differentiate \(K_j=\frac12\int g_sa_j|a|^2\) and integrate by parts in the kernel variable | exact, independently audited | Related increment formulas are classical; weak physical-time trace equality can carry an energy defect | Keep the full calculation, coefficient, attribution, and weak boundary |
| Trace flux cancellation | Substitute \(\Pi=\nabla\cdot K+\mathscr S\) into the complete R0.73V trace equation | exact parent derivation | A sign error in either convention would reverse the conclusion | Audit against the frozen R0.73V equation, not a retyped surrogate |
| Positive carré-du-champ row | Apply the heat covariance identity to all gradient components | exact parent derivation | Positivity belongs to \(D_{ii,s}\), not generally to \(\partial_s\tau_s\) or its strain contraction | Preserve the exact object in every public statement |
| Weighted spatial mean | Self-adjoint heat filtering gives \(\langle\Pi_s\rangle=\langle P_{2s}u,(u\cdot\nabla)u\rangle\) | exact parent derivation | Requires periodicity or boundary decay; removes spatial localization | Present as a global mean identity only |
| Critical \(s^{-1/2}\) scale weight | Spectral multiplier is \(\sqrt{\pi/2}L^{-1/2}\) | exact parent derivation | It returns the classical \(H^{1/2}\) cubic threshold, not an arbitrary-energy estimate | Use as a sharp diagnosis of the remaining critical obstruction |
| Time integral of the critical scale average | Energy inequality and \(L^3\) interpolation give \(\|u_0\|_2^3\nu^{-3/4}T^{1/4}\) | high | Absolute value follows signed space--scale integration | Never relabel it as \(\int\!\int\!\int |\Pi_s|\) |
| Universal one-sided sign | Parity \(u\mapsto-u\) plus the nonzero finite production coefficient | exact, two-path sealed | Commit-bound producers agree; the result is a counterexample to a universal rule, not pointwise sign variation of one witness | Publish only the stated quantified negation |
| Same-time viscous absorption | Cubic production versus quadratic \(D_{ii,s}\) under amplitude scaling | exact, two-path sealed | Refutes only the displayed amplitude-independent inequality | Do not generalize to time-integrated, nonlinear, conditional, or localized payments |
| Finite witness geometry | Public field has Fourier-support rank three; rank-two and 2D3C fields remain as diagnostic cross-checks | exact, two-path sealed | Rank three is not generic turbulence and cannot address blow-up | Say “universal-sign counterexample,” never “singularity witness” |
| Leray--Hopf extension | Every factor in the absolute estimate is defined a.e.; positive heat scale regularizes space | high | Full endpoint equality at \(s=0\) is not automatic | Restrict exact weak characteristic use to \(s\ge\sigma>0\) unless separately justified |
| Literature ownership | Johnson 2020/2021 own Gaussian stress diffusion/decomposition; standard coarse-graining owns local energy flux; Germano and increment literature own the central-moment lineage | high, primary sources, bounded audit complete | The exact combined, fixed-scale, and critical-weighted displays may be routine consequences even if not found verbatim | Record bounded negative findings only; forbid priority claims |
| Formal figure | Deterministic panels for the characteristic, analytic scale envelopes, and exact sign witness; 49/49 checks over 1,416 source-data rows | exact rendering, source/package sealed | Source commit `ac6293ac4d0c46c696d2ec8e29d3fb1350e341f1` and package commit `60b0e869bbaa3a0ace185bf450e067d79fcd79b3`; no figure-package blocker remains | Treat the plots as exact identities, upper-bound shapes, and finite formulas, never DNS, fitted data, a Navier--Stokes time solution, or a PDE theorem |
| Clay relevance | The section isolates a signed scalar obstruction and an energy-level estimate | structurally useful | No zero-scale uniform control, localized coercivity, or continuation criterion | Rate as a rigorous structural step, not a solution or near-solution |

## Release boundary

The current positive information is exact but limited.  The heat-plane
characteristic identifies where viscosity cancels scale diffusion, and the
energy estimate proves that absolute production is integrable over heat
scale.  The remaining mathematical loss is local and zero-scale: signed
cancellation does not control concentration, while the unconditional absolute
bound is not uniform as \(s\downarrow0\).

The analytic audit, literature readback, local direct translation, exact
finite seal, and formal-figure source/package seal now pass.  The release
transaction is ready, but publication is not complete until HTML/PDF parity
and the GitHub Pages gate also pass.
