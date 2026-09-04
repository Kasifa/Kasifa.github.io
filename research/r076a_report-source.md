# R0.76A source and collision report

- Date: 2026-09-04
- Audience: mathematical analysts auditing the clustered-frequency route
- Scope: positivity of the frozen radial primitive, localization of the
  one-sided Fourier current, and the complete-clock two-mode counterexample
- Exclusions: a general Toeplitz or Hardy-space theorem, full cluster-flux
  payment, arbitrary Navier--Stokes fields, novelty, and priority

## Direct answer

The R0.76A result is an explicit calculation from the frozen profile and one
exact two-mode diffusive shear.  It does not import an external theorem.
The calculation shows that positive Fourier support makes the current
nonnegative only after full-period integration; multiplication by the actual
nonnegative collar primitive can expose a strictly negative local current
throughout the complete clock.

The closest literature retained in R0.75Z concerns local observation of
exponential polynomials and Fourier support in finitely many intervals.  Such
results control norms or propagation of smallness.  They do not assert that
the local density `Im(conj(Z) Z_y)` has a fixed sign, and they do not replace
the explicit sign calculation in R0.76A.

## Evidence ledger

| question | evidence | use in R0.76A | boundary |
|---|---|---|---|
| Is local observation of finite exponential sums established? | Nazarov's local estimates and the Turan--Nazarov line of work | Context only; no such theorem is needed for A.1--A.34. | Norm observation does not imply pointwise or weighted-current positivity. |
| Can a bounded number of spectral intervals be observed independently of their locations? | Kovrijkine and the torus result of Egidi--Veselic | A possible later tool for joint cluster observability. | These are not signed current or collar-flux estimates. |
| Did a targeted search locate a theorem asserting local positivity of `Im(conj(Z) Z_y)` for positive-frequency polynomials? | Searches combining `analytic trigonometric polynomial`, `positive frequency`, `localized current`, `momentum density`, `Hardy`, and `Toeplitz` returned unrelated physics uses or general Hardy/Toeplitz material. | No external claim is imported; the explicit counterexample remains decisive for the stated sign rule. | Absence in a bounded search is not a novelty or priority finding. |

## Claim-to-source ledger

1. F. L. Nazarov, “Local estimates for exponential polynomials and their
   applications to inequalities of the uncertainty principle type,”
   *Algebra i Analiz* 5:4 (1993), 3--66; English version,
   *St. Petersburg Mathematical Journal* 5:4 (1994), 663--717.
   [Math-Net record](https://www.mathnet.ru/eng/aa397).

2. Oleg Kovrijkine, “Some results related to the Logvinenko--Sereda
   theorem,” *Proceedings of the American Mathematical Society* 129 (2001),
   3037--3047.
   [arXiv:math/0012186](https://arxiv.org/abs/math/0012186).

3. Michela Egidi and Ivan Veselic, “Scale-free unique continuation estimates
   and Logvinenko--Sereda theorems on the torus,” 2016 preprint.
   [arXiv:1609.07020](https://arxiv.org/abs/1609.07020).

4. Philippe Jaming and Chadi Saba, “From Ingham to Nazarov's inequality: a
   survey on some trigonometric inequalities,” 2023.
   [arXiv:2311.17714](https://arxiv.org/abs/2311.17714).

## Stop rule and exact boundary

The focused search did not produce a directly matching local-current sign
theorem; broader variants rapidly left harmonic analysis and returned
unrelated uses of momentum density.  The search stopped because R0.76A is
settled by the exact two-term formula and because another terminology scan
would not change its validity or boundary.

The literature is not represented as proving R0.76A.  The bounded negative
search is not represented as evidence of novelty.  The note rules out only
localized sign-dropping.  Error estimates, joint multipliers, full cluster
payment, Version-M transfer, regularity, and singularity remain open.
**NOT CLAY.**
