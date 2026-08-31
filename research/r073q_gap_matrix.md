# R0.73Q research gap matrix

**Status:** bounded primary-source audit and independent analytic readback
complete; finite package awaiting immutable source seal

| Question | Closest verified source | Domain / solution class | What the source already settles | R0.73Q disposition |
| --- | --- | --- | --- | --- |
| Small critical \(L^3\) data | Kato 1984, DOI [10.1007/BF01174182](https://doi.org/10.1007/BF01174182) | \(\mathbb R^3\), Kato Theorem 1 weighted smoothing/uniqueness class | Local theory for all \(L^3\) data and global theory under a small critical norm | `KNOWN`; not a periodic relative-orbit theorem or unconditional bare-\(C_tL^3_x\) uniqueness statement |
| Small \(BMO^{-1}\) data | Koch--Tataru 2001, [author PDF](https://math.berkeley.edu/~tataru/papers/nas.pdf), DOI [10.1006/aima.2000.1937](https://doi.org/10.1006/aima.2000.1937) | \(\mathbb R^n\), unique **small** solution in the Koch--Tataru \(X\) class | Global small-data and local \(VMO^{-1}\) theory using a Carleson/tent-space norm | `KNOWN`; the word "small" and the solution class cannot be removed |
| Stability around a large a priori global solution in critical Besov topology | Gallagher--Iftimie--Planchon 2003, Theorem 3.1, [primary PDF](https://www.numdam.org/item/10.5802/aif.1983.pdf), DOI [10.5802/aif.1983](https://doi.org/10.5802/aif.1983) | \(\mathbb R^3\), global solution continuous in \(\dot B^{3/p-1}_{p,q}\), finite stated indices | Openness and Lipschitz stability in the critical Besov norm; time subdivision is explicit in the proof | `DIRECT_COLLISION`; R0.73Q does not claim a new whole-space openness theorem |
| Stability around a global \(VMO^{-1}\) solution in \(BMO^{-1}\) topology | Auscher--Dubois--Tchamitchian 2004, DOI [10.1016/j.matpur.2004.01.003](https://doi.org/10.1016/j.matpur.2004.01.003) | \(\mathbb R^3\); publisher abstract for the stated global-solution class | The abstract reports decay, analytic data dependence, and openness of the corresponding Cauchy-data set in \(BMO^{-1}\) topology | `ABSTRACT_ONLY_COLLISION`; no radius, full perturbation quantifiers, or periodic endpoint theorem is imported |
| Periodic anisotropic stable domain beyond isotropic \(H^{1/2}\) | Iftimie 1999, Theorems 2.1--2.2, DOI [10.24033/bsmf.2358](https://doi.org/10.24033/bsmf.2358) | \(\mathbb T^3\), perturbations of a vertical-average or separately prescribed two-dimensional component | Global anisotropic control; for \(0<\delta<1/2\), an elementary Fourier-weight comparison shows the domain is strictly broader than isotropic \(H^{1/2}\) | `PRIMARY_THEOREM_PLUS_ELEMENTARY_COMPARISON`; direct geometric collision, not the paper's verbatim strictness claim |
| Periodic \(\dot B^{-1/2}_{6,4}\) tube around one fixed global \(H^3\) orbit | No exact source found with the same fixed-torus, all-restart, explicit-action quantifiers | \(\mathbb T^3\), smooth initial data, mild/Serrin \(L^4_tL^6_x\) branch | Classical components are known; the precise periodic orbitwise packaging is not found as a source theorem | `PROVED_INTERNAL_COROLLARY`; no novelty or priority claim |
| Uniform radius for every restart time \(t_0\ge0\) | Whole-space openness results above do not state the present periodic quantitative radius | Fixed orbit with \(M[u]=\|u\|_{L^4_tL^6_x}<\infty\) | Tail action is bounded by the full action | `PROVED_INTERNAL`: finite causal partition and explicit inverse bound \(K[u]\) |
| A stable domain strictly extending the R0.73P \(H^{1/2}\) domain | Standard embeddings plus the explicit Fourier shear family | Smooth, mean-zero, divergence-free periodic perturbations | \(H^{1/2}\hookrightarrow\dot B^{-1/2}_{6,4}\); weaker norm can be small while \(H^{1/2}\) is large | `PROVED_INTERNAL`: use the union of the old and new tubes; do not order unrelated radii |
| Bare Kato-sup closure from only \(u\in L^4_tL^6_x\) | Endpoint time fractional integration | Candidate norm \(\sup_t t^{1/4}\|w(t)\|_6\) | The cross-term estimate would require \(I_{1/4}:L^4\to L^\infty\), which fails logarithmically | `NEGATIVE_PROOF_ROUTE`; not a theorem that Kato or \(BMO^{-1}\) stability is false |
| Unrestricted nonperturbative \(BMO^{-1}\) uniqueness | Coiculescu--Palasek 2025/2026, Theorem 1.2, [arXiv v2](https://arxiv.org/pdf/2503.14699), DOI [10.1007/s00222-025-01396-z](https://doi.org/10.1007/s00222-025-01396-z) | \(\mathbb T^3\), two distinct global finite-\(X_{KT}\) solutions, smooth for \(t>0\), with initial datum outside \(L^2\) | Unrestricted uniqueness in the natural critical path class is false in general; Remark 1.3 calls the construction nonperturbative around zero, without a quantitative norm lower bound | `FALSE_IN_GENERAL`; R0.73Q stops at finite-index Besov/Serrin data |
| Strong regularity from a uniform \(L^2\)-only smallness condition | No verified theorem; R0.73P explains the supercritical obstruction | Arbitrary smooth perturbations with no heat/frequency/higher-norm control | Weak relative energy and delayed regularity do not close the early strong interval | `OPEN_COLLISION_SENSITIVE` |
| Clay global regularity | Clay problem | Arbitrary smooth finite-energy data | None of the stable neighborhoods covers arbitrary data | `OPEN_NOT_CLAY` |

## Release decision

The positive R0.73Q result is the finite-index heat-flow row, not the
\(BMO^{-1}\) endpoint.  The primary collision audit shows that the underlying
whole-space idea is classical.  The defensible value of the release is the
fixed-torus proof with a radius uniform in all restart times, an explicit
linearized inverse bound, and an exact smooth sequence satisfying

\[
 \|w_N\|_2\to0,
 \qquad
 \|w_N\|_{\mathfrak X}\to0,
 \qquad
 |w_N|_{1/2}\to\infty.
\]

This closes one structured high-frequency entrance left open by R0.73P.  It
does not close the unrestricted \(L^2\)-only entrance and does not change the
status of the Millennium problem.
