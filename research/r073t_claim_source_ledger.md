# R0.73T claim--source ledger

**Status:** analytic and exact no-go audits closed; primary-source collision
labels aligned; finite package, formal figure, and public release bindings
remain to be assigned

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

| ID | Claim | Evidence class | Exact source or proof | Release use |
|---|---|---|---|---|
| C1 | \(C_h=\widehat{|u|^2}(h)\), \(Q=\sum_h|C_h|^2=\|u\|_4^4\) | `VERIFIED_CLASSICAL` | Fourier convention and Parseval; [dynamic proof](r073t_dynamic_autocorrelation_budget.md), Section 1 | Fixes the state variables |
| C2 | \(\dot C_h=-\nu|h|^2C_h-2\nu\widehat{|\nabla u|^2}(h)-ih\cdot\widehat{u(|u|^2+2p)}(h)\) | `VERIFIED_CLASSICAL_RECONSTRUCTION` | Spatial Fourier transform of the classical local-energy identity; Tran--Yu--Dritschel 2021 [DOI](https://doi.org/10.1017/jfm.2020.1033); two independent derivations in [dynamic proof](r073t_dynamic_autocorrelation_budget.md), (2.3), and [independent audit](r073t_independent_analytic_audit.md) | Exact non-autonomous law: \(C\) misses the signed flux \(u(w+2p)\), while reconstructing \(p=R_iR_j(u_i u_j)\) generally requires the full tensor, not only its trace; literal packaging is not a novelty basis |
| C3 | \(Q'+4\nu Y+2\nu X^2=4\int p u\cdot\nabla|u|^2\) | `VERIFIED_CLASSICAL_RECONSTRUCTION` | Direct \(L^4\) integration by parts; exact \(L^q\)/pressure collision in Tran--Yu--Dritschel 2021 [DOI](https://doi.org/10.1017/jfm.2020.1033); Kato 1990 [Springer volume](https://link.springer.com/book/10.1007/BFb0084893); [proof](r073t_dynamic_autocorrelation_budget.md), Section 3 | Classical dynamic baseline |
| C4 | \(\|p\|_3\le C_R\|u\|_6^2\) | `VERIFIED_CLASSICAL` | Periodic double-Riesz/Calderón--Zygmund boundedness | Pressure estimate; no novelty claim |
| C5 | \(Q'+4\nu Y+\nu X^2\le4C_R^2\nu^{-1}AQ\) | `INTERNAL_COROLLARY` | C3--C4, Young, and R0.73S \(\|u\|_6^6\le AQ\); [proof](r073t_dynamic_autocorrelation_budget.md), (4.4); independent constant audit. Tran--Yu--Dritschel 2021 is the nearest direct \(L^4\)/pressure collision [DOI](https://doi.org/10.1017/jfm.2020.1033) | Main positive R0.73T result; not a new \(L^p\) identity |
| C6 | \(A\in L_t^1\) gives a Gronwall bound for \(Q\) | `INTERNAL_COROLLARY` | C5; [proof](r073t_dynamic_autocorrelation_budget.md), (4.5) | Conditional consequence only |
| C7 | \(\int A\,dt\) is scale invariant and \(A\ge\|u\|_\infty^2\) | `INTERNAL_EXACT_SCALING` | Integer torus dilation and Fourier inversion; [proof](r073t_dynamic_autocorrelation_budget.md), Section 5 | Shows the missing budget is critical, at least as restrictive as, and directly implies classical endpoint control |
| C8 | \(u\in L_t^2L_x^\infty\) is the spatial-\(L^\infty\) critical-equality end of the classical LPS line | `VERIFIED_CLASSICAL` | \(\int A\,dt<\infty\Rightarrow\int\|u\|_\infty^2dt<\infty\); Serrin 1962 [DOI](https://doi.org/10.1007/BF00253344); Kato 1984 [DOI](https://doi.org/10.1007/BF01174182). The time exponent is \(2\) and the space exponent is \(\infty\); this is not the hard \(L_t^\infty L_x^3\) endpoint | Forbids a “new criterion” interpretation of C5--C7; requires full-field \(A\), not one shell |
| C9 | Differentiating \(A\) introduces stronger derivative Wiener norms | `INTERNAL_EXACT` | Upper-Dini estimate from C2; [proof](r073t_dynamic_autocorrelation_budget.md), Section 6 | Exact dynamic non-closure ledger |
| C10 | \(Q'\le C(\nu^{-7}Q^3+\nu^{-1}Q^{3/2})\) | `VERIFIED_STANDARD_LOCAL_ESTIMATE` | Periodic Gagliardo--Nirenberg and Young; two analytic reconstructions | Resolution-uniform local fallback, not global control |
| C11 | Rotating shears have identical complete \(C\) but \(\dot C_0=-2\nu N^2\) | `INTERNAL_EXACT` | Exact heat solution; [proof](r073t_dynamic_autocorrelation_budget.md), Section 7 | Carrier-scale non-autonomy |
| C12 | The six-mode field has \(\mathcal E=42,Q=2918,A=164,D_C=15\), \(X^2=4296,Y=1986\), and \(\mathcal N_4=-384\) | `INTERNAL_EXACT` | Two independent rational Fourier reconstructions; [no-go audit](r073t_no_go_audit.md); [crosscheck](r073t_crosscheck_no_go.md) | Exact signed pressure-pairing witness |
| C13 | \(u_L,-u_L\) have identical complete scalar \(C\), identical \(u\otimes u\), identical mean-zero pressure, and pressure work \(\mp384L\) | `INTERNAL_EXACT` | C12 plus integer dilation and sign parity; \(u\mapsto-u\) leaves \(u\otimes u\) and \(p=R_iR_j(u_i u_j)\) unchanged | Signed velocity-phase non-identifiability in the pressure pairing; not a pressure-tensor-polarization witness |
| C14 | The common full derivative is dominated by \(-16536\nu L^2\) with signed separation \(-768L\) | `INTERNAL_EXACT` | C12 and exact quartic balance | Shows C13 is compatible with the one-sided upper estimate |
| C15 | Fixed summaries cannot bound \(|Q'|\) | `INTERNAL_EXACT` | Scalar shear: \((\mathcal E,Q,A,D_C)=(1/2,3/8,1,3)\), \(Q'=-(3/2)\nu L^2\) | Two-sided/absolute no-go only |
| C16 | Periodic frequency-localized scalar nonlinear Bernstein at \(p=4,s=2\) | `VERIFIED_CLASSICAL` | Li 2013 [DOI](https://doi.org/10.4310/MRL.2013.v20.n5.a9); Li--Sire, Trans. AMS 376 (2023), Theorem 4.2 [DOI](https://doi.org/10.1090/tran/8708), [arXiv](https://arxiv.org/abs/2109.07952) | Classical scalar shell coercivity input; constant depends on the fixed cutoff |
| C17 | The vector shell coercivity follows componentwise from C16 | `VERIFIED_CLASSICAL_WITH_ADAPTATION` | Apply scalar Theorem 4.2 to each component; \(Q_j\le3\sum_i\|u_{j,i}\|_4^4\), \(\mathcal D_j\ge\sum_i\int u_{j,i}^2|\nabla u_{j,i}|^2\), and \(-\int(\Delta u_{j,i})u_{j,i}^3=3\int u_{j,i}^2|\nabla u_{j,i}|^2\); [proof](r073t_dynamic_autocorrelation_budget.md), Section 8 | Theorem 4.2 is scalar; Remark 4.1 is not a literal frequency-localized vector theorem. Display the adaptation and keep cutoff/low-shell qualifications |
| C18 | Shell Duhamel inequalities for \(Q_j^{1/2}\) and \(Q_j^{1/4}\) | `INTERNAL_CONDITIONAL` | Exact projected equation, C16--C17, and R0.73S; the \(Q_j^{1/4}\) branch uses the fixed projection-support difference count \(\overline D_j=|\Sigma_j-\Sigma_j|\), so it remains valid through \(Q_j=0\) and its coefficient may stay outside the Duhamel integral; [proof](r073t_dynamic_autocorrelation_budget.md), (8.7)--(8.10) | Conditional transport only; an instantaneous active-support count is forbidden at shell zero crossings |
| C19 | \(F_j\lesssim2^j\|u\|_4^2\) or \(F_j\lesssim2^{5j/2}\|u\|_2^2\) | `VERIFIED_CLASSICAL` | Bernstein, Leray boundedness, and product norms | Identifies circular versus supercritical forcing branches |
| C20 | Velocity-heat law \((\partial_t-\nu\partial_s)Q_s=-4\int|v_s|^2v_s\cdot R_s\) and \(\partial_sQ_s\le0\) | `INTERNAL_EXACT` | Semigroup differentiation and quartic integration by parts | Opens a scale-aware route; does not close the commutator |
| C21 | Weighted scalar sign-pair separation is \(-768Le^{-8\tau L^2}\) | `INTERNAL_EXACT` | Rational convolution grouped by \(|h|^2\) | Shows scalar heat weighting still loses signed velocity phase, even though the pair has the same tensor and pressure |
| C22 | An identical prior \(AQ\)+two-witness package was not located | `NOT_ESTABLISHED` | Only a bounded search. Direct \(L^4\)/pressure collision: Tran--Yu--Dritschel 2021 [DOI](https://doi.org/10.1017/jfm.2020.1033). Related velocity-Wiener branch: Ambrose--Lopes Filho--Nussenzveig Lopes 2024 [DOI](https://doi.org/10.1090/proc/16615), [arXiv](https://arxiv.org/abs/2205.12383) | “Not located” is not a novelty, priority, or non-existence proof; novelty claim forbidden |
| C23 | Arbitrary-data global regularity or Clay conclusion | `OPEN` | C5 still needs a classical-strength critical budget; C18 still needs signed flux control | Keep explicitly open |

## Evidence rules

1. `INTERNAL_EXACT` means the displayed algebra has a self-contained proof
   and an independent reconstruction.  It is not a novelty label.
2. The six-mode package is a finite exact diagnostic, not a Navier--Stokes
   simulation and not a proof of the continuum derivation.
3. The one-sided inequality and the two-sided no-go must always be stated
   together; they are compatible.
4. The six-mode field is planar and smooth.  It cannot be described as a
   vortex-stretching, singular, near-singular, or blow-up example.
5. The sign pair has identical \(u\otimes u\) and pressure.  It cannot be
   cited by itself as proof of pressure-tensor-polarization or pressure
   non-identifiability; it isolates the signed velocity phase in the pairing.
6. Li--Sire 2023 Theorem 4.2 is used in its scalar form.  The three-component
   step is displayed locally rather than silently attributed to Theorem 4.2 or
   Remark 4.1.
7. A bounded collision search cannot establish novelty, priority, or
   non-existence.
8. Ordinary bilingual copy is translated directly on the local workstation;
   DGX is not used for translation.
