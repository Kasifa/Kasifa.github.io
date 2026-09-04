# R0.76I source and collision report

## Report frame

- Date: 2026-09-05.
- Question: can a frequency-uniform exterior estimate on the shrinking
  full-plateau gap replace R0.76E's `exp(Cq)` spatial loss?
- Scope: arbitrary real exact constant-shear packets in one dyadic band,
  their full physical plateau mass, and the complete-clock signed collar
  flux.
- Exclusions: exhaustive priority research, an independent reconstruction
  of a new 34-page preprint, arbitrary nonlinear Navier--Stokes packets,
  Version-M extraction, regularity, singularity, and the Clay problem.

## Direct answer

Yes, conditional on one newly located literature theorem.  Proposition 4.2
of Ruizhe Zhang's July 2026 arXiv v1 preprint gives an explicit
frequency-uniform endpoint extrapolation bound at the Chebyshev scale
`exp(O(q sqrt(Delta)))`, with no frequency-separation assumption.  The
frozen full plateau observes `[-1+delta_0/a,1-delta_0/a]`, while the collar
lies only relative distance `Delta_a=O(1/a)` beyond it.  Substitution into
R0.76E's exact energy identity changes `exp(Cq)` into
`q^7 exp(12 sqrt(2) q sqrt(Delta_a))` and enlarges the sufficient mode
window from `q=o(L^2)` to `q=o(L^(5/2))`.

This is not an independent proof of Zhang's proposition.  The preprint is
version 1 and, as of the report date, is an arXiv preprint rather than a
refereed journal result.  R0.76I therefore labels the composite theorem
**CONDITIONAL-LITERATURE** and keeps the local implication separate from
the imported statement.

## Primary-source ledger

| source | verified status | exact input or boundary | use in R0.76I |
|---|---|---|---|
| [R. Zhang, *Optimal Extrapolation Bounds for Sparse Fourier Sums*, arXiv:2607.10501v1](https://arxiv.org/abs/2607.10501v1) ([PDF v1](https://arxiv.org/pdf/2607.10501v1)) | Submitted 2026-07-11; arXiv v1; 34 pages; not treated here as peer reviewed. | Proposition 4.2 gives the stated endpoint upper bound for `0<=delta<=1`, with `A_fr<=8191`. Proposition 8.4 gives matching exponential scale in the full `T_k` class, up to polynomial factors, only in its lower-bound range `k^(-2)<=Delta<=1`. | Imported endpoint estimate; range-qualified full-class sharpness context only. |
| [T. Erdelyi, *Inequalities for exponential sums*, arXiv:1602.02315](https://arxiv.org/abs/1602.02315) ([journal record](https://www.mathnet.ru/eng/sm8670), [official PDF](https://www.mathnet.ru/php/getFT.phtml?jrnid=sm&option_lang=eng&paperid=8670&what=fullteng)) | 2016 arXiv manuscript; published in *Sbornik: Mathematics* 208:3 (2017), 433--464, DOI 10.1070/SM8670. | Journal Theorem 2.3: endpoint Nikolskii estimate for `T_n`. Journal Theorem 2.20 (arXiv v1 Theorem 9.1): Markov-type derivative estimate with `108 n^5 + sum lambda_j^2`. Equation (1.2) records the Kós `E_n^+` endpoint `2n` inequality; equation (1.5) records the sharper `pi n/2` extension. | Interior observation, derivative payment, and terminal-time control. |
| [G. Kós, *Two Turán type inequalities*](https://link.springer.com/article/10.1007/s10474-007-6176-5) | Published in *Acta Mathematica Hungarica* 119 (2008), 219--226, DOI 10.1007/s10474-007-6176-5. | Original source for the `E_n^+` endpoint estimates; the `2n` `L2` form used here is quoted explicitly in Erdelyi equation (1.2). | Attribution and provenance for the terminal-time estimate. |

## Exact imported statements

For a real-frequency `k`-sparse Fourier sum, Zhang Proposition 4.2 states

\[
 |g(1+\delta)|
 \le\sqrt{9A_{\rm fr}/2}\,k
 \exp(3\sqrt2k\sqrt\delta)\|g\|_{L^2[-1,1]},
 \qquad0\le\delta\le1,
\]

and Lemma 2.6 permits `A_fr=8191`.  Squaring and taking at most `2q`
conjugate branches produces the exact R0.76I exponent
`12 sqrt(2) q sqrt(Delta_a)`.

Erdelyi journal Theorem 2.20 (arXiv v1 Theorem 9.1) states, in its
`[0,1]` normalization,

\[
 \|f'\|_\infty
 \le(1+\epsilon_n)
 (108n^5+\textstyle\sum_j\lambda_j^2)^{1/2}\|f\|_\infty.
\]

The same paper records Kós's sufficient estimate

\[
 |f(0)|\le2n\|f\|_{L^2[0,1]},\qquad f\in E_n^+.
\]

These are three different inputs: spatial exterior extrapolation, spatial
differentiation, and reverse-time endpoint control.

## Collision and sharpness audit

The abstract frequency-uniform extrapolation step is already a literature
result; R0.76I makes no novelty claim for it.  Zhang's lower construction
uses a confluent sequence of complex sums on frequencies
`{0,epsilon,...,(k-1)epsilon}` approaching a Chebyshev polynomial.  That
construction, in the stated lower-bound range `k^(-2)<=Delta<=1`, is not
in the narrower class of mean-zero real
conjugate-paired dyadic heat shears I.2.  It therefore proves the
Chebyshev exponent is necessary over all `T_k`, but not that I.5 is sharp
within the exact-shear subclass.

The bounded search found no source stating the composed Navier--Stokes
shear/full-plateau conclusion I.5--I.8.  Absence from this bounded search is
not evidence of novelty or priority.

## Claim-to-evidence ledger

| claim | evidence class | status |
|---|---|---|
| Arbitrary real-frequency sparse Fourier sums obey the explicit endpoint estimate used in I.17. | Zhang Proposition 4.2, arXiv v1. | **LITERATURE; UNREFEREED PREPRINT** |
| The observation interval and collar gap scale as `Delta_a=O(1/a)`. | Frozen shell geometry and exact interval algebra. | **PROVED** |
| The spatial `L-infinity` loss is `q^2 exp(12 sqrt(2) q sqrt(Delta_a))`. | Direct bilateral scaling of Zhang Proposition 4.2 plus Hölder. | **PROVED CONDITIONAL ON LITERATURE** |
| The derivative row costs at most `q^7+q^3 alpha^2`. | Erdelyi Theorem 9.1 plus local interval and frequency scaling. | **PROVED CONDITIONAL ON LITERATURE** |
| The final-time row is polynomial in `q`. | Kós endpoint inequality as recorded by Erdelyi, followed by local `L3` integration. | **PROVED CONDITIONAL ON LITERATURE** |
| R0.76E's energy identity yields I.5 and the `q=o(L^(5/2))` window. | Local four-row estimate and exact physical normalization. | **PROVED CONDITIONAL ON LITERATURE** |
| The exponent is sharp inside the real dyadic heat-shear class. | Zhang's lower witness lies only in the larger `T_k` class. | **OPEN** |
| The result extends to arbitrary nonlinear packets or proves Version-M extraction. | No proof in the sources or locally. | **OPEN** |
| Navier--Stokes regularity or singularity follows. | No proof. | **OPEN; NOT CLAY** |

## Search record and limitations

The search was bounded to primary and official records: arXiv source pages
and PDFs, the MathNet journal record/PDF, and the Springer journal record.
Queries targeted sparse-Fourier endpoint extrapolation without separation,
exponential-sum Nikolskii/Markov bounds, and one-sided `E_n^+` endpoint
inequalities.  The theorem numbers, constants, function classes, interval
normalizations, publication dates, and lower-witness class were checked in
the source texts.

No citation-count argument, search-result snippet, or secondary exposition
is used as mathematical evidence.  The search is not exhaustive, Zhang v1
has not been independently reproved here, and no priority claim is made.
**NOT CLAY.**
