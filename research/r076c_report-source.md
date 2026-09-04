# R0.76C primary-source boundary -- stable heat-clock observation

## 0. Scope and direct answer

- Search date: 2026-09-04.
- Question: which established theorem supports the gap-independent temporal
  observation used for ultra-high fixed finite shear families, and which
  parts of the resulting collar-flux payment are local deductions.
- Search class: original or author-posted mathematical sources on the
  Turan--Nazarov measurable-set inequality for complex exponential
  polynomials.
- Exclusions: an exhaustive citation graph, novelty or priority, constants
  uniform for a growing number of modes, arbitrary Navier--Stokes fields,
  and regularity.

The sole external theorem imported into R0.76C is again the
Turan--Nazarov measurable-set inequality.  Its dependence on the number of
terms, interval/subset ratio, and real parts -- but not on imaginary parts or
exponent gaps -- permits a fixed-order exponential polynomial whose real
parts lie in `[-4,-1]` to be controlled at late heat time by its first unit
of `L^3` mass.

The polynomial-times-exponential decay C.13, the weighted integral and
endpoint consequences C.15, the change of clock `tau=lambda s`, the cutoff
onset gain, the complete real-square energy identity, and the physical scale
conversion are deductions written out in R0.76C.  They are not attributed to
the cited sources.

The Deep Research planning helper required by the selected research skill was
not available in this environment.  The bounded primary-source search,
claim ledger, and stop rule are therefore recorded directly here.

## 1. Primary sources

### Nazarov's original local estimate

F. L. Nazarov, *Local estimates for exponential polynomials and their
applications to inequalities of the uncertainty principle type*, Algebra i
Analiz 5:4 (1993), 3--66; English translation, St. Petersburg Mathematical
Journal 5:4 (1994), 663--717.

Bibliographic record and linked full text:
<https://www.mathnet.ru/eng/aa397>.

The record states the interval/measurable-subset estimate for

`p(t)=sum_(k=1)^n c_k exp(lambda_k t)`

with complex coefficients and exponents.  The displayed factor is

`exp(max_k |Re lambda_k| |I|) (A |I|/|E|)^(n-1)`.

This is exactly the generic input used in C.18.  R0.76C does not import any
Navier--Stokes or heat-equation theorem from the paper.

### Accessible primary restatement

Omer Friedland and Yosef Yomdin, *An observation on the Turan--Nazarov
inequality*, Studia Mathematica 218 (2013), 27--39.

Author manuscript: <https://arxiv.org/abs/1107.0039>.
Journal PDF: <https://www.impan.pl/shop/en/publication/transaction/download/product/89801>.

The abstract explicitly records that imaginary parts do not enter the
original inequality.  Theorem 1.1 restates the measurable-subset form for a
complex exponential polynomial.  R0.76C uses only this positive-measure
version, not the paper's later metric-span extension.

## 2. Claim-to-source ledger

| claim | evidence | use in R0.76C | exact boundary |
|---|---|---|---|
| measurable-set control for an `N`-term complex exponential polynomial | Nazarov; Friedland--Yomdin Theorem 1.1 | C.18 | external theorem only |
| no imaginary-frequency or exponent-gap denominator | Friedland--Yomdin abstract and theorem | arbitrary constant speed and colliding scaled frequencies | fixed `N<=2q`; real-part factor remains |
| centered exponent band `[-3/2,3/2]` | algebra from C.12 and C.17 | converts the theorem's exponential factor to net `e^(-tau)` | local deduction |
| pointwise stable heat-clock estimate C.13 | C.16--C.18 | late-time control from the first unit interval | local corollary, not quoted |
| weighted integral and endpoint estimates C.15 | C.19--C.21 | pays the cutoff onset and terminal energy | local Holder and tail calculation |
| ultra-high gain `lambda^(-1/3)` | C.22--C.27 | removes `n_1R<=1` for fixed `q` | local change of variables |
| full-frequency collar payment C.4 | C.28--C.34 plus R0.76B | theorem for the exact shear family | not supplied by an external source |

## 3. Bounded collision screen

The search combined `Turan Nazarov exponential polynomial measurable set`,
`stable exponential polynomial heat decay`, `frequency-gap independent`,
`weighted time observability`, and `Navier Stokes shear localized flux` with
the primary-source classes above.  It recovered the generic
Turan--Nazarov theorem and neighboring spectral-observability language, but
no source in the bounded screen stated the project-specific chain:

1. center the temporal exponents by `5/2`;
2. propagate the first heat-time unit to arbitrary later time with a fixed
   term count;
3. integrate the resulting polynomial-exponential tail with the onset
   weight `tau`;
4. obtain the exact `lambda^(-1/3)` payment after `tau=lambda s`; and
5. insert it into the complete real-square collar identity and plateau-mass
   scaling.

This negative screen is not evidence of novelty or priority.  The search was
stopped when the only imported theorem had direct primary support and further
variants did not change any proof dependency.

## 4. Exact source boundary

The sources justify only the generic measurable-set inequality and its lack
of dependence on imaginary frequencies or exponent gaps.  They do not prove
C.13 or C.15 as written, the cutoff-onset gain, the radial energy identity,
the physical mass conversion, growing-packet control, Version-M extraction,
suitable-weak transfer, regularity, or singularity.  Finite certificates may
audit the algebra and one ultra-high exact family, but not the continuum
Turan--Nazarov theorem.  R0.76C makes no completeness, novelty, or priority
claim.  **NOT CLAY.**
