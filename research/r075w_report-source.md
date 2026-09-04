# R0.75W source report

- Audience: a mathematically expert reader auditing the R0.75W proof.
- Date: 2026-09-04.
- Scope: the primary-source boundary for the frequency-gap-free temporal
  trace and the Navier--Stokes problem statement.
- Assumption: the spatial confluent observation lemma and the local energy
  identity are proved directly in the R0.75W note; they are not attributed
  to an external source.

## Direct answer

The only external theorem used in the new low-carrier proof is the
Turan--Nazarov inequality for an exponential polynomial on an interval and
a positive-measure subset.  Its decisive feature here is that the bound
depends on the number of exponential terms and the real parts of their
exponents, but not on the imaginary frequencies or their separation.
R0.75W uses it only for four terms on `[0,4]` and derives the endpoint
`L^3` trace by a sublevel-set argument.

## Primary-source checks

1. F. L. Nazarov, *Local estimates for exponential polynomials and their
   applications to inequalities of the uncertainty principle type*,
   Algebra i Analiz 5:4 (1993), 3--66; English translation, St. Petersburg
   Mathematical Journal 5:4 (1994), 663--717.
   Primary record and formula:
   <https://www.mathnet.ru/eng/aa397>.

   The MathNet record states the interval-to-measurable-set inequality for
   `sum c_k exp(lambda_k t)`.  The displayed factor contains the interval
   length, subset measure, number of terms, and
   `max |Re lambda_k|`; it contains no imaginary-frequency or frequency-gap
   factor.  This supports W.17 and its collision-uniform use.

2. Omer Friedland and Yosef Yomdin, *An observation on the Turan--Nazarov
   inequality*, Studia Mathematica 218 (2013), 27--41,
   DOI 10.4064/sm218-1-2.  Author manuscript:
   <https://arxiv.org/abs/1107.0039>.

   Theorem 1.1 restates Nazarov's measurable-set inequality with complex
   coefficients and exponents.  The paper explicitly notes that imaginary
   parts do not enter the original inequality.  This is an accessible
   cross-check of the exact form used in W.15--W.19, not an additional
   hypothesis.

3. Charles L. Fefferman, *Existence and Smoothness of the Navier--Stokes
   Equation*, official Clay Mathematics Institute problem description:
   <https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf>.

   The official problem asks for a global smoothness or breakdown result in
   the stated three-dimensional setting.  A finite-dimensional exact shear
   estimate such as W.2 does not meet that target.

## Claim-to-source ledger

| claim | source | support | boundary |
|---|---|---|---|
| Exponential-polynomial propagation is independent of imaginary frequencies and gaps | Nazarov 1993/1994; Friedland--Yomdin 2013, Theorem 1.1 | Primary theorem and primary restatement | R0.75W uses only `N<=4` on a fixed interval |
| The Millennium problem requires a general 3D result, not an exact two-mode calculation | Fefferman, Clay Mathematics Institute | Official problem statement | W.2 is not evidence of a general regularity theorem |

## Search boundary

The search was intentionally bounded to the exact exponential-polynomial
inequality needed by the proof and the official Clay statement.  It was not
a novelty search for all two-mode Navier--Stokes estimates.  The direct ODE
compactness argument, scaled kernel identity, and power ledger were checked
locally and receive no external priority attribution.
