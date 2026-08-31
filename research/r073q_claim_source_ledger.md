# R0.73Q claim--source ledger

**Status:** analytic claims independently audited; finite certificate is
pre-sealed and awaiting immutable source binding; publication package pending

| ID | Claim | Evidence class | Exact source or proof | Release use |
| --- | --- | --- | --- | --- |
| C1 | \(M[u]=\|u\|_{L^4(0,\infty;L^6)}<\infty\) | Internal corollary | R0.73P \(\mathcal A_{1/2}[u]<\infty\) plus periodic \(H^1\hookrightarrow L^6\); `r073q_heat_flow_stability_proof.md` Section 2 | Uniform reference action |
| C2 | Periodic Duhamel map \(\mathcal B:E\times E\to E\), \(E=L^4_tL^6_x\) | Classical estimate, internally derived | Periodic Stokes heat bound plus one-dimensional HLS; proof Section 3 | Critical bilinear closure |
| C3 | \(I+\mathcal L_{U_{t_0}}\) has one inverse bound \(K[u]\) for every \(t_0\) | Internal analytic proof | Finite causal action partition and recurrence; proof Section 4 | All-restart quantifier |
| C4 | \(\rho_{\mathfrak X}[u]=1/(8C_BK[u]^2)>0\) gives a global \(E\) difference | Internal fixed point | Proof Section 5 | New heat-flow tube |
| C5 | Smooth data in the tube remain global \(H^3\) | Classical/internal | Full \(L^4((t_0,T_*);L^6)\) bound plus Serrin continuation; proof Section 6 | Strong-solution conclusion |
| C6 | \(H^{1/2}\hookrightarrow\mathfrak X\simeq\dot B^{-1/2}_{6,4}\) | Classical embedding, internally displayed | Periodic Bernstein, \(\ell^2\hookrightarrow\ell^4\), negative heat-semigroup characterization; proof Section 7 | Relates old and new topology |
| C7 | \(w_N=N^{-1/4}e_2\sin(Nx_1)\) has \(L^2\to0\), \(\mathfrak X\to0\), and \(H^{1/2}\to\infty\) | Exact analytic witness | Direct normalized-Haar and heat integral; proof equations (7.3)--(7.7) | Strictness certificate |
| C8 | \(\mathcal D_Q[u]=\mathcal D_P[u]\cup B_{\mathfrak X}(\rho_{\mathfrak X})\) strictly contains the R0.73P domain | Exact set corollary | C4 plus C7; proof equations (7.9)--(7.10) | Safe strict-domain claim |
| C9 | Whole-space critical Besov global-data set is open and locally Lipschitz | Published primary theorem | Gallagher--Iftimie--Planchon 2003, Theorem 3.1, DOI 10.5802/aif.1983 | Direct collision; no novelty claim |
| C10 | Periodic anisotropic stable domains broader than \(H^{1/2}\) exist around two-dimensional components | Published primary theorem plus elementary Fourier-weight comparison | Iftimie 1999, Theorems 2.1--2.2, DOI 10.24033/bsmf.2358; Theorem 2.1 uses the vertical average, while Theorem 2.2 permits a separately prescribed 2D component | Geometric collision; strictness is not attributed as a verbatim theorem sentence |
| C11 | Small \(L^3\) and small \(BMO^{-1}\) critical theories | Published primary theorems | Kato 1984, DOI 10.1007/BF01174182; Koch--Tataru 2001, Theorems 2--3, DOI 10.1006/aima.2000.1937 | Background and endpoint definition |
| C12 | The corresponding whole-space Cauchy-data set is reported open in \(BMO^{-1}\), with decay and analytic data dependence for the stated global class | Publisher abstract of primary article | Auscher--Dubois--Tchamitchian 2004, DOI 10.1016/j.matpur.2004.01.003 | Abstract-only endpoint collision; no radius, full perturbation quantifiers, or constants imported |
| C13 | Nonperturbative periodic \(BMO^{-1}\) data may have two distinct global finite-\(X_{KT}\) solutions smooth for \(t>0\) | Published primary theorem | Coiculescu--Palasek, Theorem 1.2 and Remarks 1.3--1.5, DOI 10.1007/s00222-025-01396-z; “nonperturbative around zero” is not a numerical norm lower bound | Hard endpoint exclusion |
| C14 | Mucha's verified \(L^2\)-small theorem retains higher Besov trace dependence | Published primary theorem | Mucha 2008, Theorem 1.2, DOI 10.4064/bc81-0-18 | Excludes promotion to \(L^2\)-only radius |
| C15 | Mucha 2001 exact periodic threshold dependence | Unresolved source detail | DOI 10.1006/jdeq.2000.3863; publisher abstract only in bounded pass | Closest periodic collision; no inference from missing text |
| C16 | Bare Kato-sup proof from only \(u\in L^4_tL^6_x\) fails at the cross-term endpoint | Exact negative route audit | \(I_{1/4}:L^4\not\to L^\infty\); endpoint logarithm in analytic audit | Does not assert endpoint stability is false |
| C17 | Unrestricted \(L^2\)-only strong radius | Open claim | R0.73P/R0.73Q do not control arbitrary initial heat trace | Must remain `OPEN_COLLISION_SENSITIVE` |
| C18 | Arbitrary-data Clay conclusion | Open problem | Outside all proved stable domains | Must remain `OPEN_NOT_CLAY` |

## Evidence rules

1. `Published primary theorem` claims retain their original domain, topology,
   time range, and uniqueness class.
2. The R0.73Q theorem is labeled an internal periodic corollary/synthesis;
   it does not acquire novelty merely by combining classical ingredients.
3. The explicit \(K[u]\) is an upper bound, not an optimized or numerically
   sharp stability radius.
4. The old \(H^{1/2}\) radius and new heat-flow radius are not ordered.  Only
   their union supports the strict comparison with the full R0.73P domain.
5. Exact Fourier values certify norm geometry and a family of safe structured
   perturbations.  They do not certify arbitrary \(L^2\)-small data.
6. An abstract-only source is never reconstructed into an unavailable
   theorem.
