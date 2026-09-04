# R0.76J source, reconstruction, and collision report

## Report frame

- Date: 2026-09-05.
- Audience: analysts and PDE researchers auditing the exact-shear branch.
- Question: can the R0.76I Chebyshev-scale full-plateau window be retained
  without treating a July 2026 arXiv v1 proposition as a black box?
- Scope: arbitrary real-frequency finite Fourier sums and their insertion
  into the frozen one-band, real, constant-shear Navier--Stokes solution.
- Assumptions: the frozen R0.76I downstream Markov, reverse-time endpoint,
  energy-identity, plateau-geometry, and physical-normalization chain is
  imported only under its recorded hashes.
- Exclusions: an exhaustive priority search, arbitrary nonlinear packets,
  a suitable-weak transfer, regularity, singularity, and the Clay problem.

## Direct answer

Yes.  R0.76J locally proves the only edge-extrapolation statement needed
by R0.76I.  For every real-frequency sum with at most `N` complex terms,

\[
 \max\{|g(1+d)|,|g(-1-d)|\}
 \le\sqrt{\frac{250}{19}}N
 e^{5\sqrt2N\sqrt d}\|g\|_{L^2[-1,1]},
 \qquad d\ge0.
\]

The proof constructs the finite vertical-line Takenaka--Malmquist basis,
derives both negative- and positive-time Laguerre majorants, and uses the
positive-time estimate to prove its own weighted tail bound

\[
 \int_0^\infty|F(t)|^2e^{-\alpha t}dt
 \le\frac{20}{19}\int_0^{25N/\alpha}
 |F(t)|^2e^{-\alpha t}dt.
\]

Thus neither Zhang Proposition 4.2 nor Erdelyi's weighted
infinite--finite range theorem is an imported premise.  The price relative
to Zhang's stated constant is only a larger exponent coefficient:
`5sqrt(2)` instead of `3sqrt(2)` before squaring.  After `N<=2q`, the
R0.76J observation exponent is
`20sqrt(2)q sqrt(Delta_a)`.  Since `Delta_a=O(L^(-1))`, the sufficient
window remains exactly `q=o(L^(5/2))` and the frozen normalized quadratic
rate remains `-2/11907`.

## Primary-source ledger

| source | verified status | exact role in R0.76J |
|---|---|---|
| [R. Zhang, *Optimal Extrapolation Bounds for Sparse Fourier Sums*, arXiv:2607.10501v1](https://arxiv.org/abs/2607.10501v1) ([v1 PDF](https://arxiv.org/pdf/2607.10501v1)) | Submitted 2026-07-11; version 1; the arXiv record states arbitrary real frequencies, no separation, and endpoint scale `exp(O(k sqrt(delta)))`. | Attribution for the Sections 2--4 architecture and comparison with Proposition 4.2.  No theorem from the preprint is assumed in the R0.76J proof. |
| [T. Erdelyi, *Inequalities for exponential sums*](https://www.mathnet.ru/eng/sm8670) ([journal PDF](https://www.mathnet.ru/links/5e053ba70d2cde7e4d5cd0feaa545c86/sm8670_eng.pdf)) | *Sbornik: Mathematics* 208:3 (2017), 433--464, DOI 10.1070/SM8670.  The official record defines `E_n^+`, `E_n^-`, and `T_n` and identifies Nikol'skii, Markov, and infinite--finite range inequalities as its subject. | Journal Theorem 2.20 supplies the spatial derivative estimate and equation (1.2) records the Kós endpoint estimate used in the already-frozen downstream chain.  Its finite-range theorem is contextual only, not used by the new edge proof. |
| [S. R. Garcia and W. T. Ross, *Model spaces: a survey*, arXiv:1312.5018](https://arxiv.org/abs/1312.5018) | Submitted 2013; later published in AMS Contemporary Mathematics 638 (2015), 197--245. | Background attribution for model spaces and Takenaka--Malmquist systems.  R0.76J directly proves the finite basis formulas, orthogonality, and spanning that it uses. |
| [P. Borwein, T. Erdelyi, and J. Zhang, *Muentz systems and orthogonal Muentz--Legendre polynomials*](https://doi.org/10.1090/S0002-9947-1994-1227091-4) | *Transactions of the AMS* 342 (1994), 523--542, DOI as linked. | Earlier algebraic ancestry for the orthogonal exponential/Muentz basis.  It is not an imported premise. |
| [G. Kós, *Two Turan type inequalities*](https://doi.org/10.1007/s10474-007-6176-5) | *Acta Mathematica Hungarica* 119 (2008), 219--226. | Original attribution for the reverse-time endpoint estimate already recorded and range-audited in R0.76I. |

## Reconstruction ledger

| step | evidence | status |
|---|---|---|
| Boundary Laplace Plancherel and its finite rational reproducing kernels | Standard Fourier/Hardy identity, with the kernel identity derived directly in J.14--J.15. | **ESTABLISHED STANDARD FACT** |
| Vertical-line Takenaka--Malmquist basis | J.16--J.20: boundary-unimodular factors, kernel zero, and triangular partial fractions. | **PROVED LOCALLY** |
| Exterior Laguerre majorant | J.21--J.29: Volterra multiplier and negative-time induction. | **PROVED LOCALLY** |
| Positive Laguerre majorant | J.30--J.31: the same Volterra recurrence on the positive half-line. | **PROVED LOCALLY** |
| Weighted tail with cutoff `25N/alpha` | J.32--J.34: basis expansion, Cauchy--Schwarz, and `5N exp(-5N)<1/20`. | **PROVED LOCALLY** |
| Bilateral edge theorem | J.35--J.41 plus reflection. | **PROVED LOCALLY** |
| Exact-shear observation and flux theorem | J.42--J.46 plus the frozen, hash-bound R0.76I downstream chain. | **PROVED LOCALLY FROM ESTABLISHED LITERATURE** |

## Collision and prior-art boundary

The bounded search found no pre-2026 source that states, as one directly
applicable theorem, the arbitrary-real-frequency, no-separation,
near-endpoint `L2`-to-pointwise estimate with
`exp(C N sqrt(d))` loss.  The 1994 Muentz--Legendre construction together
with Erdelyi's 2017 weighted range theorem can be assembled into such an
estimate, but doing so requires a local change of variables and analytic
continuation argument.  R0.76J instead proves a slightly less optimized
weighted tail directly from its constructed basis.

Fixed-base Turan--Nazarov/Remez bounds, same-interval endpoint
Nikol'skii inequalities, real-exponent Muentz results, and interior
shift-invariant estimates are related but do not by themselves state the
shrinking-gap edge theorem used here.  Absence from this bounded search
is not evidence of novelty or priority.  The proof architecture is
explicitly attributed to Zhang; the positive-tail closure is presented
only as a local reconstruction and simplification.

## Claim-to-evidence boundary

| claim | status |
|---|---|
| The edge theorem is valid for complex coefficients, arbitrary real frequencies, collisions after merging, and no gap assumption. | **PROVED LOCALLY** |
| The new proof removes the R0.76I dependence on Zhang Proposition 4.2 and on any specialized finite-range black box. | **PROVED LOCALLY** |
| The exact one-band real constant shear retains `q=o(L^(5/2))` and rate `-2/11907`. | **PROVED LOCALLY FROM ESTABLISHED LITERATURE** |
| The numerical coefficient `5sqrt(2)` is optimal. | **OPEN** |
| The full flux upper bound is sharp in the real dyadic heat-shear class. | **OPEN** |
| The result transfers to arbitrary nonlinear three-dimensional fields. | **OPEN** |
| Regularity or singularity follows. | **OPEN; NOT CLAY** |

## Search limits and stop reason

The search was bounded to official arXiv version records/source, the
MathNet journal record/PDF, AMS bibliographic records, and the original
Kós journal DOI.  Statements, dates, ranges, frequency classes, and the
roles of separation and finite-range inputs were checked against those
primary or publisher-hosted records.  Search stopped after (i) the 2026
architecture was traced to its exact half-line, Laguerre, and range
components; (ii) the nearest pre-2026 Muentz/exponential-sum chain was
identified; and (iii) two independent audits verified a fully local
positive-tail substitute.  Further browsing would not change the proof's
dependency boundary.

This was not an exhaustive historical or priority search.  No citation
count, secondary summary, or search-result snippet is used as proof.
R0.76J remains an exact-shear intermediate theorem, not a solution of the
millennium problem.  **NOT CLAY.**
