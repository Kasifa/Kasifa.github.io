# R0.73S claim--source ledger

**Status:** analytic, no-go, literature, final finite-certificate seal, and
formal-figure QA closed; public HTML/PDF publication has not yet been applied

**Finite seal:** 43 rows; 226 primary, 54 independent, and 289 structural
checks; source commit `72e4c12760dc3b837dec328ee96a29736fe93c99`.

**Formal figure:** 179 rows; 236/236 checks; color, grayscale, and independent
PDF-raster visual QA passed; generated artifacts are preserved in commit
`4bb49ecc380e4b41d33e3102af4f47de016b5653`.

**Public boundary:** HTML/PDF generation, local direct translation, and
deployment verification remain release-transaction work;
`translationPath=LOCAL_DIRECT_NO_DGX`.

| ID | Claim | Evidence class | Exact source or proof | Release use |
| --- | --- | --- | --- | --- |
| C1 | (C(h)=\widehat{|f|^2}(h)=\sum_k a(k+h)\cdot\overline{a(k)}) and (Q=\sum_h|C(h)|^2=\|f\|_4^4) | `VERIFIED_CLASSICAL` | Parseval and the standard autocorrelation identity; [analytic proof](r073s_quadratic_autocorrelation_certificate.md), Section 1 | Fixes the quadratic phase statistic |
| C2 | (\|f\|_6^6\le\|C\|_1\|C\|_2^2=AQ), with constant one | `VERIFIED_CLASSICAL` | Hölder/absolute Fourier convergence/Parseval; Edwards 1972 [DOI](https://doi.org/10.1017/S0004972700044427); [analytic proof](r073s_quadratic_autocorrelation_certificate.md), equation (1.4) | Classical endpoint bridge; never call it a new theorem |
| C3 | (A\le ME^2) | `VERIFIED_CLASSICAL` | Triangle and Cauchy--Schwarz; Nessel--Wilmes 1978 finite-spectrum baseline [DOI](https://doi.org/10.1017/S1446788700038878) | Support-count branch |
| C4 | (A\le\sqrt{D_CQ}\le\sqrt{D_\Delta Q}), hence (\|f\|_6\le D_C^{1/12}\|f\|_4) | `VERIFIED_CLASSICAL` | Cauchy--Schwarz; direct collision with Nessel--Wilmes 1978, Theorem 1, (t=|f|^2,p=2,q=3) | Difference-support branch; not novel |
| C5 | (\Theta\le\Gamma\min\{M,\sqrt{D_C\Gamma}\}) | `INTERNAL_NORMALIZATION` | C1--C4 divided by (E^6); [analytic proof](r073s_quadratic_autocorrelation_certificate.md), equation (2.4) | Dimensionless shell interface only |
| C6 | Selected shifts obey (\|f\|_6^6\le A_HQ_H) with a magnitude-only uninspected tail | `INTERNAL_EXACT` | Triangle inequality, (B(h)\le E^2), and exact total magnitude correlation; [analytic proof](r073s_quadratic_autocorrelation_certificate.md), Section 3 | Finite partial-phase certificate |
| C7 | The shell proxy (U_j=Q_j\min\{M_jE_j^2,\sqrt{D_{\Delta,j}Q_j}\}) gives a sufficient upper bound for the critical heat trace | `INTERNAL_COROLLARY` | C5 plus the R0.73R LP--caloric theorem; [analytic proof](r073s_quadratic_autocorrelation_certificate.md), Section 4 | Lower-interaction-order entrance around the fixed R0.73Q orbit |
| C8 | The Dirichlet-spike family has (E=1), (\Gamma\to5/3), (\Theta\sim(11/20)\sqrt m), and (D_C=4m-1) | `INTERNAL_EXACT` | Exact carrier moments and Dirichlet formulas; [analytic proof](r073s_quadratic_autocorrelation_certificate.md), Section 5; [finite certificate](certificates/r073s/README.md) | Shows (D_C^{1/2}) growth is necessary |
| C9 | One can retune the spike so (\Gamma\equiv5/3) while (\Theta\asymp\sqrt{D_C}) | `INTERNAL_EXACT` | Positive root of the exact quadratic in the packet weight; [analytic proof](r073s_quadratic_autocorrelation_certificate.md), equation (5.10) | Removes any continuity loophole in the sharpness claim |
| C10 | (V_m=(0,\Re H_m,\Im H_m)) is real, mean zero, divergence free, lies in (32m\le|k|<36m), preserves (|F_m|), and has zero nonlinearity | `INTERNAL_EXACT` | Direct Fourier support and component calculation; [analytic proof](r073s_quadratic_autocorrelation_certificate.md), equations (5.11)--(5.14) | Transfers the obstruction to the Navier--Stokes field class |
| C11 | An uninspected autocorrelation tail may have (\ell^2\to0) while its cubic contribution diverges | `INTERNAL_EXACT` | Triangular Dirichlet correlation with (x=m^{-\alpha}), (1/2<\alpha<2/3); [analytic proof](r073s_quadratic_autocorrelation_certificate.md), Section 6 | No-go for an (\ell^2)-tail-only selected-shift contract |
| C12 | The seed polynomials (A=1-z-z^2-z^3+z^4), (B=1-z-z^2-z^3-z^4) have common ((L^2)^2=5), (L^4{}^4=37), but (L^6{}^6=311,323) | `INTERNAL_EXACT` | Integer convolution; [analytic proof](r073s_quadratic_autocorrelation_certificate.md), equations (7.1)--(7.3); [finite certificate](certificates/r073s/README.md) | Exact low-summary non-identifiability seed |
| C13 | Base-(q\ge14) lacunary products amplify the (L^6) ratio unboundedly while keeping support, coefficient magnitudes, (L^2), and (L^4) identical | `INTERNAL_EXACT` | No-carry constant-term factorization; [analytic proof](r073s_quadratic_autocorrelation_certificate.md), equations (7.4)--(7.7); independent depth-three expansion in the certificate | Information-theoretic no-go for low-order summaries |
| C14 | A predeclared strict finite set of nonzero shifts can be made identical by dilation | `INTERNAL_EXACT` | Replace (z) by (z^L), (L>\max|H|); [analytic proof](r073s_quadratic_autocorrelation_certificate.md), Section 7 | Quantified selected-shift no-go; never say all finite shifts are insufficient |
| C15 | The complete finite autocorrelation still determines (L^6) exactly | `VERIFIED_CLASSICAL` | Sixfold additive-energy identity; Green's [author notes](https://people.maths.ox.ac.uk/greenbj/papers/additive-combinatorics.pdf); [analytic proof](r073s_quadratic_autocorrelation_certificate.md), equation (7.8) | Hard boundary on C14 |
| C16 | The R0.73R Dirichlet branch makes the autocorrelation proxy sharp in power, while the scaled Rudin--Shapiro proxy decays like (O(m^{-1/2})) | `INTERNAL_EXACT` | Exact fourth/sixth moments and difference support; [analytic proof](r073s_quadratic_autocorrelation_certificate.md), Section 8; [finite certificate](certificates/r073s/README.md) | Confirms the proxy distinguishes the matched phase pair |
| C17 | Rudin--Shapiro (L^4), merit factor, and exact (L^6) are classical | `VERIFIED_CLASSICAL` | Høholdt--Jensen--Justesen 1985 [DOI](https://doi.org/10.1109/TIT.1985.1057071); Doche--Habsieger 2004 [DOI](https://doi.org/10.1007/s00041-004-3049-y); Rodgers 2017 [DOI](https://doi.org/10.1016/j.aim.2017.09.022) | Excludes all RS moment novelty claims |
| C18 | Pair enumeration is (O(M^2)) and triple enumeration (O(M^3)) only in a fixed naive sparse arithmetic model | `MODEL_BOUNDARY` | Direct loop counts; dense padded FFT can make both (O(G\log G)); structured products may be evaluated from recurrences | Say “interaction-order reduction,” not a complexity lower bound |
| C19 | Every sharpness lift used here has zero Navier--Stokes nonlinearity and is globally smooth | `INTERNAL_EXACT` | (V_1=0) and dependence only on (x_1), so (V\cdot\nabla V=0) | A large proxy is not evidence of unsafe dynamics |
| C20 | Arbitrary-data global regularity or a Clay conclusion | `OPEN` | All R0.73S results are finite harmonic-analysis certificates or fixed-orbit sufficient corollaries | Keep explicitly open |

## Evidence rules

1. `VERIFIED_CLASSICAL` claims retain their exact domain and normalization.
2. `INTERNAL_EXACT` means the displayed finite mathematics has a
   self-contained derivation and independent exact reconstruction; it is not
   a novelty or priority claim.
3. The finite certificate uses no interval arithmetic and does not certify
   the continuum PDE proof.
4. The complete autocorrelation is finite for a finite Fourier field.  The
   no-go concerns strict subsets or low-order summaries, never “all finite
   shifts.”
5. “Quadratic versus cubic interaction order” is an algebraic/input-model
   statement.  It is not a word-RAM, oracle, or arithmetic-circuit lower
   bound.
6. The R0.73Q conclusion always retains one fixed a priori global orbit and
   a sufficient radius; it does not extend to arbitrary data.
7. The exact packages bind source commit
   `72e4c12760dc3b837dec328ee96a29736fe93c99`; their generated artifacts are
   preserved in commit `4bb49ecc380e4b41d33e3102af4f47de016b5653`.
8. Ordinary bilingual release translation is performed directly on the local
   workstation (`LOCAL_DIRECT_NO_DGX`).
