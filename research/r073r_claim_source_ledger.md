# R0.73R claim--source ledger

**Status:** literature boundary fixed; analytic identities drafted; immutable
formula certificate and publication package still pending

| ID | Claim | Evidence class | Exact source or proof | Release use |
| --- | --- | --- | --- | --- |
| C1 | On mean-zero \(\mathbb T^3\), \(\|e^{t\Delta}f\|_{L^4_tL^6_x}\) is equivalent to the periodic \(B^{-1/2}_{6,4}\) norm | `VERIFIED_CLASSICAL` | Chemin--Gallagher 2006, Definition 1.1 with \((s,p,q)=(1/2,6,4)\), [primary PDF](https://www.numdam.org/article/ASENS_2006_4_39_4_679_0.pdf), [DOI](https://doi.org/10.1016/j.ansens.2006.07.002) | Direct collision; never describe the caloric space as new |
| C2 | The same norm is equivalent to \((\sum_j2^{-2j}\|P_jf\|_6^4)^{1/4}\) | `VERIFIED_CLASSICAL` | Chemin--Gallagher 2006, Definitions 2.1--2.2; Xiong--Xu--Yin 2018, Theorem 3.15, [arXiv manuscript](https://arxiv.org/pdf/1507.01789), [DOI](https://doi.org/10.1090/memo/1203) | Fixes the exact \(\ell^4\) shell topology |
| C3 | Uniform annular heat decay and the inverse multiplier on \(t\asymp4^{-j}\) give a direct two-sided periodic proof | `INTERNAL_EXACT` | Chemin--Gallagher 2006, Lemma 4.2 supplies the decay; the inverse multiplier and bounded-overlap argument are proved in [the R0.73R analytic proof](r073r_lp_caloric_certificate_proof.md), Sections 2--3 | Self-contained certificate proof; not a new Besov theorem |
| C4 | \(\Theta_j^{2/3}E_j^4=\|P_jf\|_6^4\), so the shell-concentration budget is exactly a reparameterization of the classical Besov norm | `INTERNAL_EXACT` | Algebra from the definitions of \(E_j\) and \(\Theta_j\); [analytic proof](r073r_lp_caloric_certificate_proof.md), equations (1.4)--(1.7) | Energy/concentration bookkeeping interface only |
| C5 | \(\ell^\infty\) shell control cannot replace \(\ell^4\); \(n\) normalized separated shells force at least \(n^{1/4}\) growth | `INTERNAL_EXACT` | Lower half of the two-sided LP--caloric proof; [analytic proof](r073r_lp_caloric_certificate_proof.md), Section 3 | Sharpness of the shell sequence exponent for this trace |
| C6 | The component-safe identity \(\|f_j\|_6^6=\sum_m\|\sum_r A_{j,r}*\widetilde A_{j,r}*A_{j,m}\|_{\ell^2}^2\) is exact | `INTERNAL_EXACT` | Fourier transform of \(\lvert f_j\rvert^2f_j\) plus Parseval; [analytic proof](r073r_lp_caloric_certificate_proof.md), equation (4.4) | Preferred phase-sensitive finite certificate |
| C7 | Triple additive multiplicity gives \(\|f_j\|_6\le R_j^{1/6}E_j\) | `INTERNAL_EXACT` | Cauchy--Schwarz on each triple sum, followed by Parseval and the component \(\ell^2\) sum; [analytic proof](r073r_lp_caloric_certificate_proof.md), Section 4.2 | Phase-blind geometric upper certificate |
| C8 | Support cardinality gives \(\|f_j\|_6\le M_j^{1/3}E_j\) | `INTERNAL_EXACT` | Hausdorff--Young and finite-support \(\ell^{6/5}\)-to-\(\ell^2\) comparison; [analytic proof](r073r_lp_caloric_certificate_proof.md), Section 4.3 | Cheapest modal-count upper certificate |
| C9 | The exponent \(M^{1/3}\) cannot improve from cardinality and divergence-free structure alone | `INTERNAL_EXACT` | The two-dimensional Dirichlet patch in the \(e_3\) direction has \(M\asymp m^2\) and \(\|W_D\|_6/\|W_D\|_2\asymp m^{2/3}=M^{1/3}\); [analytic proof](r073r_lp_caloric_certificate_proof.md), equation (6.2) | Sharpness boundary for the coarse certificate |
| C10 | Dyadic Rudin--Shapiro polynomials have \(\pm1\) coefficients and satisfy \(\lvert P_m\rvert^2+\lvert Q_m\rvert^2=2m\), hence \(\|P_m\|_\infty\le\sqrt{2m}\) | `VERIFIED_CLASSICAL` | Rudin 1959, [official AMS scan](https://www.ams.org/journals/proc/1959-010-06/S0002-9939-1959-0116184-5/S0002-9939-1959-0116184-5.pdf), [DOI](https://doi.org/10.1090/S0002-9939-1959-0116184-5); Balister 2019, Proposition 4, [author PDF](https://www.memphis.edu/msci/people/pbalistr/shapiro.pdf) | Classical input; direct induction retained locally |
| C11 | \(W_{D,m}\) and \(W_{P,m}\) are real, mean zero, divergence free, and have the same \(2m^2\) Fourier sites, coefficient magnitudes, \(L^2\) norm, and every quadratic Fourier-weighted norm | `INTERNAL_EXACT` | Direct expansion of the real carrier field; [analytic proof](r073r_lp_caloric_certificate_proof.md), Lemma 5.1 | Matched phase-only comparison |
| C12 | If \(N>6(m-1)\), then \(\|W_{R,m}\|_6^6=(5/(2m^6))\|R_m\|_6^{12}\) | `INTERNAL_EXACT` | Neutral carrier coefficient \(2^{-6}\binom63=5/16\) and envelope support exclusion; [analytic proof](r073r_lp_caloric_certificate_proof.md), Lemma 5.2 | Exact carrier-moment certificate |
| C13 | \(\|D_m\|_6^6=(11m^5+5m^3+4m)/20\) | `INTERNAL_EXACT` | Square-sum of the bounded triple-count function and exact piecewise-polynomial summation; [analytic proof](r073r_lp_caloric_certificate_proof.md), equations (5.8), (5.11)--(5.12) | Exact coherent branch value |
| C14 | The matched fields obey \(\|W_{D,m}\|_6\asymp m^{2/3}\) and \((5/2)^{1/6}\le\|W_{P,m}\|_6\le40^{1/6}\) | `INTERNAL_EXACT` | C12--C13 plus the classical Rudin--Shapiro bound C10; [analytic proof](r073r_lp_caloric_certificate_proof.md), Lemma 5.2 | Quantifies phase separation at fixed quadratic data |
| C15 | Their common support lies in \(N\le\lvert k\rvert<1.14N\), and \(\|W_{R,m}\|_{\mathfrak X}\asymp N^{-1/2}\|W_{R,m}\|_6\) uniformly | `INTERNAL_EXACT` | Direct support bound and smooth annular heat/inverse multipliers; [analytic proof](r073r_lp_caloric_certificate_proof.md), Lemma 5.3 | Transfers the sixth-moment separation into the caloric norm |
| C16 | With \(\alpha_m=N^{1/2}m^{-2/3}\), both \(L^2\) norms vanish, while the Dirichlet caloric norm stays order one and the Rudin--Shapiro caloric norm is order \(m^{-2/3}\) | `INTERNAL_EXACT` | Algebraic consequence of C11, C14, and C15; [analytic proof](r073r_lp_caloric_certificate_proof.md), Theorem 5.4 | Shows quadratic spectral data do not determine heat-ball entry |
| C17 | Every matched field has zero Navier--Stokes nonlinearity and evolves by the heat equation | `INTERNAL_EXACT` | \((e_3g(x_1,x_2)\cdot\nabla)e_3g=g\partial_3(e_3g)=0\); [analytic proof](r073r_lp_caloric_certificate_proof.md), Section 6 | Hard exclusion: failing the sufficient norm does not imply unsafe dynamics |
| C18 | For the fixed R0.73Q global orbit, \(C_+(\sum_j2^{-2j}\Theta_j^{2/3}E_j^4)^{1/4}<\rho_{\mathfrak X}[u]\) is sufficient at every restart | `INTERNAL_COROLLARY` | C1--C4 plus [R0.73Q Theorem 1.1](r073q_heat_flow_stability_proof.md), which fixes the a priori global orbit and radius | Computable sufficient entrance; not an arbitrary-data theorem |
| C19 | At \(p=6\), the all-positive coefficients majorize all phase choices with the same coefficient bounds | `VERIFIED_CLASSICAL` | Green--Ruzsa 2004, equation (1), [author manuscript](https://arxiv.org/pdf/math/0303244), [DOI](https://doi.org/10.1017/S0305004104007911); historical source Hardy--Littlewood 1935, [DOI](https://doi.org/10.1093/qmath/os-6.1.304) | Direct novelty boundary for the phase-coherence narrative |
| C20 | Large structured periodic data can generate global smooth Navier--Stokes solutions under nonlinear conditions | `VERIFIED_CLASSICAL` | Chemin--Gallagher 2006, Theorems 1--2, [primary PDF](https://www.numdam.org/article/ASENS_2006_4_39_4_679_0.pdf) | Do not claim that “structure permits large safe data” is new |
| C21 | Openness around a whole-space a priori global solution in critical \(\dot B^{3/p-1}_{p,q}\), including \((p,q)=(6,4)\), is classical | `VERIFIED_CLASSICAL` | Gallagher--Iftimie--Planchon 2003, Theorem 3.1, [primary PDF](https://www.numdam.org/item/10.5802/aif.1983.pdf), [DOI](https://doi.org/10.5802/aif.1983) | R0.73R is a periodic computable corollary, not a new openness principle |
| C22 | A uniform strong entrance depending only on arbitrary three-dimensional \(L^2\) size | `OPEN` | Neither R0.73Q nor R0.73R controls the caloric norm from \(L^2\) alone | Must remain open and collision-sensitive |
| C23 | Arbitrary-data global regularity or a Clay conclusion | `OPEN` | [Clay Mathematics Institute current problem page](https://www.claymath.org/millennium/Navier-Stokes-Equation/); all internal results are conditional or perturbative | Keep the evidence class `OPEN` and state explicitly that R0.73R is not a Clay result |

## Evidence rules

1. `VERIFIED_CLASSICAL` retains the source's domain, low-frequency
   convention, index range, solution branch, and quantifiers.  A whole-space
   theorem is not silently converted into a torus theorem.
2. The mean-zero periodic space in the inspected source is written
   \(B^{-1/2}_{6,4}\) with one low block.  The dotted notation in R0.73R is a
   zero-mode convention and must be explained if retained.
3. `INTERNAL_EXACT` means the displayed mathematics has a self-contained
   derivation.  Public release still requires an immutable certificate,
   independent readback, and source-bound checksums.
4. Exact finite examples certify norm geometry only.  They do not make the
   R0.73Q radius necessary and do not diagnose blow-up, instability, or
   singularity.
5. The matched Dirichlet/Rudin--Shapiro tensor pair was not found in the
   bounded collision search.  This is not a novelty or priority result.
6. `INTERNAL_COROLLARY` C18 cannot outlive its hypotheses: one fixed a priori
   global reference orbit, an \(H^3\) perturbation, and the R0.73Q sufficient
   heat-flow radius.
