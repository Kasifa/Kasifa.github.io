# R0.76D primary-source boundary -- quantitative modal entropy

## 0. Scope and direct answer

- Search date: 2026-09-04.
- Question: which established inequalities make the fixed-mode constant in
  R0.76C quantitative, and whether the resulting
  `exp(Cq log(q+1))` collar estimate is already a quoted theorem.
- Search class: original, journal, or author-posted mathematical sources on
  measurable-set and derivative inequalities for complex exponential sums.
- Exclusions: exhaustive citation graph, novelty or priority, arbitrary
  packets, general Navier--Stokes fields, and regularity.

R0.76D imports two external inequalities:

1. Nazarov's measurable-set Turan--Nazarov inequality, with an absolute
   base raised to the term count and no imaginary-frequency or gap factor;
2. Erdelyi's pointwise Bernstein-type inequality for a complex exponential
   sum with purely imaginary exponents, whose derivative constant is linear
   in the maximal frequency and the number of terms.

Everything after those two inputs -- the spatial interval placement, the
factorial heat-tail count, the `lambda` split, the complete real-square
energy payment, physical scaling, and the growing-mode condition
`q(L)log(q(L)+1)=o(L^2)` -- is derived in R0.76D.  No located source states
that project-specific chain.

The Deep Research planning helper required by the selected research skill was
not available in this environment.  The bounded primary-source search,
claim ledger, and stop rule are recorded directly here.

## 1. Imported primary sources

### Measurable-set observation

F. L. Nazarov, *Local estimates for exponential polynomials and their
applications to inequalities of the uncertainty principle type*, Algebra i
Analiz 5:4 (1993), 3--66; English translation, St. Petersburg Mathematical
Journal 5:4 (1994), 663--717.

Bibliographic record and linked full text:
<https://www.mathnet.ru/eng/aa397>.

The interval/measurable-subset inequality controls an `N`-term complex
exponential polynomial by an absolute base to the power `N-1`, an exponential
factor determined by the real parts, and the supremum on a positive-measure
subset.  This is used in D.17, D.21, and D.27.

Omer Friedland and Yosef Yomdin, *An observation on the Turan--Nazarov
inequality*, Studia Mathematica 218 (2013), 27--39.

Author manuscript: <https://arxiv.org/abs/1107.0039>.
Journal PDF: <https://www.impan.pl/shop/en/publication/transaction/download/product/89801>.

Theorem 1.1 gives an accessible primary restatement.  The abstract and the
discussion after the theorem explicitly distinguish the real-part factor
from the absent imaginary-frequency dependence of the original
positive-measure inequality.  R0.76D uses that original theorem, not the
metric-span extension.

### Explicit derivative bound for pure-imaginary sums

Tamas Erdelyi, *Inequalities for exponential sums*, Sbornik: Mathematics
208:3 (2017), 433--464, DOI 10.1070/SM8670.

Journal record: <https://www.mathnet.ru/eng/sm8670>.
Author manuscript: <https://arxiv.org/abs/1602.02315>.
Author-posted PDF:
<https://people.tamu.edu/~terdelyi/papers-online/sbornik150R.pdf>.

The paper defines

`T_n={sum_(j=1)^n a_j exp(i lambda_j t): a_j in C}`

for ordered real frequencies.  Theorem 2.7.1 states, on `[-1,1]`,

`|f'(0)| <= (lambda+2e(n+1)) ||f||_infinity`,

where `lambda=max_j|lambda_j|`.  Translation and the half-scale
`f(t)=g(z_0+t/2)` give D.18 and the `alpha+q` derivative row.  Repeated
frequencies are combined and zero terms removed before the theorem is used.

## 2. Adjacent results checked but not imported

The same Erdelyi paper contains Nikolskii and Markov-type inequalities for
pure-imaginary and more general exponential sums.  They support the broader
approximation-theory context but are not needed for D.4.

Peter Borwein and Tamas Erdelyi, *Upper bounds for the derivative of
exponential sums*, Proceedings of the American Mathematical Society 123
(1995), studies sharp endpoint and interior derivative bounds for other
real-exponent classes.  Author copy:
<https://people.tamu.edu/~terdelyi/papers-online/upper.pdf>.

Those results are neighboring evidence only.  R0.76D quotes the
pure-imaginary complex-coefficient theorem from Erdelyi 2017 because it
matches the spatial Fourier sum directly.

## 3. Claim-to-source ledger

| claim | primary evidence | use | exact boundary |
|---|---|---|---|
| positive-measure control of an `N`-term complex exponential polynomial | Nazarov; Friedland--Yomdin Theorem 1.1 | D.17, D.21, D.27 | absolute base to `N-1`; real-part factor retained |
| original inequality has no imaginary-frequency or gap denominator | Friedland--Yomdin abstract and discussion | arbitrary carrier, speed, and collisions | not uniform after the term count grows |
| point derivative of a pure-imaginary `N`-term sum is bounded by maximal frequency plus `O(N)` times the local supremum | Erdelyi Theorem 2.7.1 | D.18--D.19 | center of a fixed interval; transferred by translation and scaling |
| spatial observation costs at most `D^(2q)(alpha+q)` | D.16--D.19 | quantitative gradient row | local deduction |
| weighted heat tail costs at most `exp(Cq log(q+1))` | D.21--D.26 | ultra-high branch | local factorial estimate |
| full collar constant has the same modal-entropy loss | D.32--D.39 together with D.5 | D.4 and D.6 | local energy and scale calculation |
| D.7 retains the frozen negative rate | D.40 and frozen value of `c_gamma` | D.8 | exact-shear corollary only |

## 4. Bounded collision screen

The search combined `Turan Nazarov measurable exponential polynomial`,
`Bernstein inequality imaginary exponents`, `derivative exponential sum
interval`, `modal entropy heat observability`, and `Navier Stokes shear
localized flux`.  It found the two generic approximation-theory inputs and
related Nikolskii/Markov estimates, but no source in the bounded screen
stated the combined result:

1. a plateau-to-collar observation with explicit term-count loss;
2. an onset-weighted heat-time rescaling with a counted factorial tail;
3. the split of the gradient loss into `lambda+q^2/a^2`;
4. insertion into the frozen complete real-square collar identity; and
5. the normalized growing-mode window D.7.

This negative screen is not evidence of novelty or priority.  The search was
stopped when both imported claims had direct primary support and additional
variants did not change the proof dependencies.

## 5. Exact source boundary

The sources prove only the generic measurable-set and point-derivative
inequalities.  They do not prove the factorial estimate D.24, the stable
clock lemma D.23 as packaged here, the cutoff-onset payment, the radial
energy identity, the physical mass conversion, the
`q(L)log(q(L)+1)=o(L^2)` Navier--Stokes shear corollary, arbitrary-packet
control, Version-M extraction, suitable-weak transfer, regularity, or
singularity.

Finite arithmetic may audit the factorial bounds and exponent ledgers, but
not either imported continuum theorem.  R0.76D makes no completeness,
novelty, priority, or sharpness claim.  **NOT CLAY.**
