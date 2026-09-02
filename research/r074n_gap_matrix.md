# R0.74N gap matrix — complete annular shell synthesis

## Scope

This matrix tracks the full signed annular condition for the exact
R0.74F--H smooth periodic unforced family.  It distinguishes the proved
familywise collar-flux and weighted kinetic--dissipation results from the
still-open universal endpoint control and the three-dimensional regularity
problem.  **NOT CLAY.**

| ID | Statement | Evidence | Status | Exact boundary |
|---|---|---|---|---|
| N1 | The full object is \(\mathcal I_j=\sum_{k\ge1}\mathcal J_{j,k}\), with the periodic packet lift tested against compact Euclidean shell cutoffs. | Problem freeze (F.5)--(F.8); proof (1.2) | FROZEN | No shell or periodic copy may be discarded. |
| N2 | The index set splits exactly into \(k\le j-1\), \(k=j\), and \(k\ge j+1\). | Proof (1.3)--(1.4); independent audit Section 2 | PROVED / INDEPENDENTLY AUDITED | These three ranges are disjoint and exhaustive. |
| N3 | Taking the positive part of the inward sum is safely bounded by the sum of the pointwise positive shell integrands. | Proof (2.10); independent audit A.1 | PROVED / INDEPENDENTLY AUDITED | This loses possible shell cancellation and is therefore a majorant. |
| N4 | Inversion plus \(|F^++F^-|^2\le2(|F^+|^2+|F^-|^2)\) reduces the complete inward sum to four times one positive-packet majorant. | Lemma 2.2; independent audit A.2 | PROVED / INDEPENDENTLY AUDITED | No packet cancellation is assumed. |
| N5 | Each inward shell chord is \(O(2^k)\), so the weighted combined chord is uniformly bounded by \(C\sum2^k\Gamma_k<\infty\). | Lemma 2.1; independent audit A.3--A.4; finite certificate | PROVED / INDEPENDENTLY AUDITED / FINITE | The bound is independent of \(j\); the certificate gives the safe majorant \(22\). |
| N6 | The union of all inward derivative supports stays inside \(r_-=2^jR+R/8\), and periodization activates at most one lift per coordinate for large \(j\). | Lemma 2.1; independent audit A.5 | PROVED / INDEPENDENTLY AUDITED | This is the same geometric tube as R0.74M. |
| N7 | Jensen, Tonelli, exact periodization, and the R0.74L common-forward law give \(\mathcal P_<\) without losing bridge/shear correlation. | Lemma 2.2; independent audit A.6 | PROVED / INDEPENDENTLY AUDITED | All heat-kernel windings remain. |
| N8 | On inward support and the good final Brownian segment, R0.74M yields \(\mathfrak S_t^\leftarrow\ge\Sigma_L\) and \({\rm dist}_{\mathbb T}(u,0)\ge\Sigma_L/2\). | Proof (3.1)--(3.7); inherited audited R0.74M lemmas; independent audit A.7--A.11 | PROVED / INHERITED / INDEPENDENTLY AUDITED | The displacement is support-conditioned, not deterministic for every path. |
| N9 | Bad final segments cost \(CR^4e^{-L^2/16}\) and pay the full target weight and one factor \(R\). | Proof (3.9)--(3.11); independent audit A.12--A.13; finite certificate | PROVED / INDEPENDENTLY AUDITED / FINITE | Exact reserve \(72851/1270080>0\). |
| N10 | Good final segments are super-Gaussian and pay \(\Gamma_jR^2\). | Proof (3.12)--(3.16); independent audit A.14--A.15 | PROVED / INDEPENDENTLY AUDITED / FINITE RATE | \(\Sigma_L^2/R^2=2^{-30}e^{L^2/320}\). |
| N11 | All inward shells together satisfy \(\sup_\tau[\mathcal I_<]_+\le C\Gamma_jLR^5\). | Proof (3.17); independent audit A.7--A.15 | PROVED / INDEPENDENTLY AUDITED | This includes and strengthens the separate use of the \(j-1\) row. |
| N12 | The target row obeys \(\sup_\tau|\mathcal I_=|\le C\Gamma_jLR^5\). | R0.74L; proof (4.1)--(4.2) | INHERITED / INDEPENDENTLY AUDITED IN R0.74L | Absolute estimate for the full true packet. |
| N13 | The true packet is uniformly bounded and each full outer cutoff has derivative mass \(O(4^kR^2)\). | Lemma 5.1; independent audit A.18--A.19 | PROVED / INDEPENDENTLY AUDITED | Both radial faces and all Euclidean lifts are included. |
| N14 | The infinite outer tail satisfies \(\sup_\tau|\mathcal I_>|\le C\Gamma_jLR^5\). | Proof (5.4)--(5.10); independent audit A.20--A.24; finite certificate | PROVED / INDEPENDENTLY AUDITED / FINITE | Exact exponential reserve \(1237/423360>0\). |
| N15 | The finite-shell observables converge uniformly and the full R0.74K condition holds. | Theorem 6.1; independent audit A.20--A.24 and Section 9 | PROVED / INDEPENDENTLY AUDITED | Outer absolute summability justifies \(N\to\infty\). |
| N16 | The exact family has \(\mathfrak C_j\asymp B_j^2L_jR_j^2\asymp P_j^{2/3}\sqrt{1+\log_+P_j}\). | Theorem 6.1 plus R0.74H, J, K; independent audit Section 9 | PROVED FAMILYWISE / INDEPENDENTLY AUDITED | This is a collar-flux observable, not a universal endpoint theorem. |
| N17 | Existing weighted-energy or shear-mixing papers directly imply N15. | Bounded primary-source audit | NO DIRECT HIT FOUND | The finite non-hit is not novelty or priority evidence. |
| N18 | Combining the completed collar bound with the pre-existing signed-flux energy closure gives \(X_j\asymp B_j^2L_jR_j^2\asymp P_j^{2/3}\sqrt{1+\log_+P_j}\). | Corollary 6.2; R0.74H Theorem 5.1; R0.74J Theorem 3.3 and (4.6); N15--N16 | PROVED FAMILYWISE / CROSS-NOTE AUDITED | This is a non-circular synthesis: H5.1, the J payment law, and N15 do not assume the \(X_j\) upper bound. |
| N18a | The components satisfy \(cT_j\le\mathcal U_j\le X_j\le CT_j\) and \(0\le\mathcal D_j\le CT_j\), where \(T_j=B_j^2L_jR_j^2\). | Corollary 6.2; R0.74F Theorem 6.2; R0.74H (5.1a)--(5.1b) | PROVED FAMILYWISE / CROSS-NOTE AUDITED | No matching lower bound is claimed for the dissipation component \(\mathcal D_j\) alone. |
| N19 | Arbitrary smooth solutions satisfy a universal square-root-log endpoint bound for \(X_R^\alpha\) in terms of \(P_R^\alpha\). | No arbitrary-flow control of the positive collar flux at this scale | OPEN / NOT CLAIMED | Exact-family saturation is neither a proof nor a refutation of the universal endpoint. |
| N20 | N15--N18 imply regularity, singularity exclusion, or global smoothness for arbitrary 3D data. | None | OPEN / NOT CLAIMED | **NOT CLAY.** |

## Finite certificate

The Python Fraction producer and independent Ruby Rational reconstruction
return 84/84 exact checks.  They verify the two exponent reserves, the
combined-chord majorant, the outer half-ratio tail, the dyadic normalization,
and raw \(L,R\) powers.  Their scope is finite arithmetic only; they do not
promote stochastic identities, heat-kernel estimates, maximum principles,
support geometry, or the analytic theorem.
