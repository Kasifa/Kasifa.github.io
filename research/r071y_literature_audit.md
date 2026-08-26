# R0.71Y bounded primary-source literature audit

**Search date:** 2026-08-26  
**Scope:** quantitative Chebyshev/total-positivity structure, Vandermonde
conditioning, exponential-sum sampling, biorthogonal moment estimates, and
quantitative inverse/implicit-function radii. The search is bounded and makes
no novelty or priority claim.

## 1. Direct literature decision

The checked sources support four limited statements.

1. Exponentials and their integrated responses form qualitative finite-
   dimensional Chebyshev/strictly totally positive systems.
2. Positive-real Vandermonde systems can have rapidly deteriorating inverse
   norms as dimension grows.
3. Exponential-sum Markov/Nikolskii and moment-method estimates record
   explicit dimension, gap, and observation-time losses.
4. Quantitative inverse/implicit-function theorems expose inverse-Jacobian
   and Lipschitz constants in a **certified sufficient radius**.

None of the sources proves the R0.71Y Navier--Stokes sampling theorem, the
matched-background ledger, the exact root-coordinate identity, or the
\(N^{-1}\) payment. Those are internal arguments in
r071y_report-source.md. Conversely, no checked source licenses a universal
claim that every Vandermonde-like matrix is exponentially ill-conditioned or
that a certified IFT radius is the largest true branch radius.

## 2. Claim--source--gap ledger

| ID | primary or canonical source | checked content | what it licenses here | what it does not license |
|---|---|---|---|---|
| S1 | Samuel Karlin and William J. Studden, *Tchebycheff Systems: With Applications in Analysis and Statistics*, Interscience (1966), Chapter I and Chapter XI; [catalogue/preview](https://books.google.com/books/about/Tchebycheff_Systems.html?id=P7Y-AAAAIAAJ) | Definitions, determinant/Wronskian criteria, interpolation nondegeneracy, and zero counting for T/ET/ECT systems. | The qualitative fixed-\(N\) mechanism already used in R0.71W. | No \(N\)-uniform smallest singular value, coefficient bound, slope bound, or IFT radius. |
| S2 | Allan Pinkus, *Totally Positive Matrices*, Cambridge University Press (2009), Chapter 4, especially §4.1--4.2, pp. 87--92; [publisher chapter](https://www.cambridge.org/core/books/abs/totally-positive-matrices/examples/455BC3C6529C3AB981E177E79D3E8176) | The kernel \(e^{xy}\) is strictly totally positive for strictly ordered arguments; generalized exponential evaluation matrices have positive minors. | A second canonical route to finite-dimensional nondegeneracy and sign structure. | Strict total positivity alone does not give dimension-uniform stability. |
| S3 | Walter Gautschi, “On inverses of Vandermonde and confluent Vandermonde matrices,” *Numerische Mathematik* 4 (1962), 117--123, Theorem 1, pp. 119--120; [author PDF](https://www.cs.purdue.edu/homes/wxg/selected_works/section_01/016.pdf) | Explicit product estimates for rows/norms of a Vandermonde inverse; for positive nodes the displayed product bound is attained in the stated norm. | Once an exact response factorization is known, node separation can be converted into a genuine inverse estimate. | Its norm cannot be copied to the integrated-response matrix without the cumulative and diagonal factors. |
| S4 | Walter Gautschi and Gabriele Inglese, “Lower Bounds for the Condition Number of Vandermonde Matrices,” *Numerische Mathematik* 52 (1988), 241--250, Theorem 2.1 and Theorem 3.2; [DOI](https://doi.org/10.1007/BF01398878), [EuDML record](https://eudml.org/doc/133234) | Positive-real ordinary Vandermonde condition numbers have explicit exponentially growing lower bounds in the studied norms/configurations. | A literature-level warning consistent with the exact R0.71Y determinant squeeze. | It is not a theorem about every basis, preconditioning, node geometry, or the full nonlinear IFT. |
| S5 | Peter Borwein and Tamás Erdélyi, “Pointwise Remez- and Nikolskii-type inequalities for exponential sums,” Theorems 2.1--2.3, pp. 4--5; [author PDF](https://people.tamu.edu/~terdelyi/papers-online/remez7.pdf) | Pointwise and derivative values of real exponential sums are controlled by continuous norms with explicit degree and distance-to-boundary factors. | Sampling bounds must pay dimension and boundary distance; roots moving to the launch boundary require separate treatment. | These inequalities do not identify the coefficient Gram norm with \(K_v\), and do not prove the exact NSE root-slope bound. |
| S6 | Piermarco Cannarsa, Patrick Martinez, and Judith Vancostenoble, “Precise estimates for biorthogonal families under asymptotic gap conditions,” *DCDS-S* 13 (2020), 1441--1472, Theorems 2.1--2.2; [journal DOI](https://doi.org/10.3934/dcdss.2020082), [arXiv](https://arxiv.org/abs/1706.02435) | Upper and lower biorthogonal-family estimates make observation time, bad finite gaps, and good asymptotic gaps explicit. | Independent evidence that exponential moment inverses naturally deteriorate with time/gap geometry. | The infinite-sequence moment problem is not the finite R0.71Y response matrix; its constants cannot be transplanted without verifying hypotheses and normalization. |
| S7 | Phan Phien, “Some quantitative results on Lipschitz inverse and implicit functions theorems,” arXiv:1204.4916, Theorems 3.1, 3.5, and 3.8, pp. 5--11; [arXiv](https://arxiv.org/abs/1204.4916) | Quantitative inverse/implicit neighborhoods depend explicitly on inverse generalized-Jacobian and Lipschitz data. | R0.71Y correctly keeps Dyson exposure, inverse Jacobian, and derivative-Lipschitz constants separate. | A sufficient certified radius is not a necessary upper bound on the largest actual nonlinear branch. |
| S8 | Plamen Koev, “Accurate Eigenvalues and SVDs of Totally Nonnegative Matrices,” *SIAM J. Matrix Anal. Appl.* 27 (2005), 1--23; [DOI](https://doi.org/10.1137/S0895479803438225) | Given accurate bidiagonal factors, TN eigenvalues/SVDs can be computed to high relative accuracy even when conventional conditioning is large. | Large condition number means perturbation sensitivity, not automatic impossibility of structured numerical certification. | It does not remove the analytic inverse-Jacobian cost in an IFT. |

## 3. How the sources constrain the R0.71Y wording

### 3.1 Qualitative ECT is not quantitative stability

S1--S2 justify finite-\(N\) zero counting and interpolation
nondegeneracy. S3--S4 show why those qualitative statements must not be
upgraded to a uniform inverse bound. R0.71Y therefore derives its main
sampling estimate before using any ECT inverse.

### 3.2 Conditioning is geometry dependent

S4 gives rapid deterioration for positive-real Vandermonde configurations,
but this is not universal over all node sets and bases. Fourier/root-of-unity
Vandermonde matrices can be perfectly conditioned, and structured TN
algorithms in S8 can remain accurate. The internal equal-grid determinant
factorization is consequently stated only for its declared positive heat
nodes \(x_l=e^{-bhr_l^2}\).

### 3.3 Function-space sampling does not replace coefficient accounting

S5 can control pointwise derivatives by continuous exponential-sum norms,
but the map from coefficients to those norms may itself be ill-conditioned.
The R0.71Y proof avoids that missing Gram comparison: the exact skew energy
identity controls the evolving scalar and the Fourier multiplier bounds
compare the shear directly with \(K_v\).

### 3.4 A quantitative IFT theorem supplies a certificate, not a no-go theorem

S7 explains why inverse-Jacobian and Lipschitz constants enter a sufficient
radius. It does not allow the inference that no branch exists outside the
certified ball. Accordingly, the inverse lower bound (5.10) is called a
conditioning squeeze, not a proof that the nonlinear branch terminates.

### 3.5 Observation time and gaps remain real costs

S5--S6 independently support the need to track distance from the launch
boundary, root spacing, and spectral gaps. The internal Lemma 1.1 is stronger
for the declared heat lattice in one direction:
\(\delta_{\rm obs}\le C_{A_0,\nu,d}\eta_{\rm Dyson}\) for fixed \(A_0>0\).
Its constant degenerates when \(A_0\downarrow0\), consistent with the
boundary sensitivity in S5--S6.

## 4. Falsification ledger

The following statements are rejected.

| overclaim | falsifying boundary |
|---|---|
| “ECT implies a dimension-uniform inverse.” | S1--S2 give qualitative nondegeneracy; S3--S4 expose dimension/node losses. |
| “Every Vandermonde matrix is exponentially ill-conditioned.” | The claim depends on node geometry, basis, norm, and preconditioning; S4 is restricted, and S8 shows structured high-relative-accuracy computation can remain possible. |
| “Markov/Nikolskii already proves \(G_N\lesssim K_v\).” | S5 controls function values by function norms, not the coefficient-to-function Gram map used here. |
| “The moment-method literature gives the current finite inverse constant.” | S6 has different sequence, gap, time, and norm hypotheses. |
| “A quantitative IFT radius is the maximal true radius.” | S7 supplies a sufficient certified neighborhood only. |
| “Large conventional condition number makes certification impossible.” | S8 distinguishes analytic sensitivity from structured numerical accuracy. |
| “The literature proves the R0.71Y NSE theorem.” | No checked source contains the exact triangular root identity, matched background, optimized atom ledger, or \(N^{-1}\) payment. |

## 5. Remaining literature gap

The principal unresolved literature-facing question is no longer a generic
ECT inverse for the selected-root branch. It is whether a theorem can control
the **total** number of exact nonlinear target zeros in terms of carrier
dimension and observation-layer coupling, or control a floor-free complete
\(\mathcal R_Y\)-weighted ledger. No checked source supplies that
Navier--Stokes-specific all-root count.
