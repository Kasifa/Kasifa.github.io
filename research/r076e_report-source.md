# R0.76E primary-source boundary -- delayed heat-tail split

## 0. Scope and direct answer

- Search date: 2026-09-04.
- Question: whether the `exp(Cq log(q+1))` loss in R0.76D is required by a
  quoted theorem, and which established exponential-sum estimates could
  reduce it.
- Source class: original or author-posted papers on Turan--Nazarov,
  pointwise Remez/Nikolskii inequalities, and complex shift-invariant
  spaces.
- Exclusions: exhaustive citation graph, novelty or priority, arbitrary
  packets, general Navier--Stokes fields, and regularity.

The direct conclusion is narrow.  R0.76E needs no new external theorem.
It reuses the two inputs already audited for R0.76D and changes only the
local organization of the heat clock:

1. use Holder with the full observed mass up to
   `S_N=C_0N log(N+1)`;
2. use the existing centered Turan--Nazarov tail only after `S_N`; and
3. use a last-unit Turan--Nazarov estimate for the finite-time endpoint.

The result is a local improvement from `exp(Cq log(q+1))` to `exp(Cq)`.
No located source states the project-specific collar-flux theorem or this
exact delayed-split argument.

The Deep Research planning helper required by the selected research skill
was unavailable in this environment.  The search scope, evidence ledger,
and stop rule are recorded directly here.

## 1. Imported sources retained from R0.76D

### Measurable-set Turan--Nazarov

F. L. Nazarov, *Local estimates for exponential polynomials and their
applications to inequalities of the uncertainty principle type*, Algebra i
Analiz 5:4 (1993), 3--66; English translation, St. Petersburg Mathematical
Journal 5:4 (1994), 663--717.

Bibliographic record and linked full text:
<https://www.mathnet.ru/eng/aa397>.

Omer Friedland and Yosef Yomdin, *An observation on the Turan--Nazarov
inequality*, Studia Mathematica 218 (2013), 27--39.

Author manuscript: <https://arxiv.org/abs/1107.0039>.
Journal PDF:
<https://www.impan.pl/shop/en/publication/transaction/download/product/89801>.

The original interval/measurable-subset inequality has an absolute base to
the power `N-1`, a real-part factor, and no imaginary-frequency-gap
denominator.  R0.76E uses it in the inherited spatial row, the centered
stable tail E.13, and the fixed-unit endpoint E.19.

### Explicit derivative for pure-imaginary sums

Tamas Erdelyi, *Inequalities for exponential sums*, Sbornik: Mathematics
208:3 (2017), 433--464, DOI 10.1070/SM8670.

Journal record: <https://www.mathnet.ru/eng/sm8670>.
Author manuscript: <https://arxiv.org/abs/1602.02315>.
Author-posted PDF:
<https://people.tamu.edu/~terdelyi/papers-online/sbornik150R.pdf>.

The published and author-posted numbering gives Theorem 2.7.1:

`|f'(0)| <= (lambda+2e(n+1)) ||f||_infinity`.

R0.76E inherits R0.76D's translation and half-scale application.  The older
arXiv organization may label the corresponding result differently; the
statement, not the draft numbering, is the imported fact.

## 2. Adjacent sources checked but not imported

Peter Borwein and Tamas Erdelyi, *Pointwise Remez- and Nikolskii-type
inequalities for exponential sums*, Mathematische Annalen 316:1 (2000),
39--60, DOI 10.1007/s002080050003.

Author PDF:
<https://people.tamu.edu/~terdelyi/papers-online/remez7.pdf>.

Its pointwise Nikolskii theorem gives sharp polynomial-in-dimension interior
control for sums with real exponents.  That class does not cover the
transport-induced complex temporal exponents in E.11, and its point is
strictly inside a finite interval.  R0.76E therefore does not cite it as a
proof of the one-sided endpoint E.19.

Peter Borwein and Tamas Erdelyi, *Nikolskii-type inequalities for shift
invariant function spaces*, Proceedings of the American Mathematical
Society 134:11 (2006), 3243--3246, DOI 10.1090/S0002-9939-06-08533-9.

Erdelyi's author-posted survey states the theorem and its complex
shift-invariant scope:
<https://people.tamu.edu/~terdelyi/papers-online/SP.pdf>.

The theorem controls an interior subinterval for `0<p<=2`.  It is relevant
context for finite-dimensional complex exponential spaces, but it does not
directly give the endpoint from the past-only mass `K_T`.  The present proof
uses the already imported measurable-set theorem instead.

## 3. Local improvement ledger

| claim | evidence | status | boundary |
|---|---|---|---|
| centered stable tail E.13 | Nazarov; Friedland--Yomdin | imported through R0.76D | at most `N` complex exponents, real parts in `[-4,-1]` |
| inherited spatial derivative row E.10 | Erdelyi Theorem 2.7.1 plus Turan--Nazarov | imported through R0.76D | retains `D^(2q)(alpha+q)` |
| existence of `S_N=C_0N log(N+1)` satisfying E.15 | elementary logarithmic domination | local deduction | one sufficiently large absolute `C_0` |
| early weighted bound E.16 | Holder | local deduction | uses the full `K_T`, not `K_1` |
| late weighted bound E.17 | E.13 and monotonicity | local deduction | begins only at `S_N` |
| polynomial weighted clock E.18 | E.16--E.17 | local deduction | `[N log(N+1)]^(4/3)` |
| last-unit endpoint E.19 | Turan--Nazarov on `[T-1,T]` | local corollary | fixed interval length; real-part factor absorbed |
| `exp(CN)` endpoint E.22 | E.19 for `T<=S_N`, E.13 for `T>=S_N` | local deduction | past-only mass `K_T` |
| `exp(Cq)` collar constant E.3--E.4 | E.10, E.18, E.22, complete-real identity | local deduction | exact shear, one dyadic band |
| growing window `q=o(L^2)` | E.33 and frozen `omega` | local deduction | conditional exact-shear asymptotic |

## 4. Disconfirmation and collision screen

The search asked whether a known half-line Nikolskii inequality immediately
replaced the R0.76D factorial.  The real-exponent pointwise theorem does not
match the complex transport exponents.  The complex shift-invariant theorem
is an interior estimate and does not by itself use only mass from the past.
Neither was promoted into the proof.

The improvement instead comes from a defect in the previous bookkeeping:
R0.76D used the first-unit mass `K_1` to control the entire tail and then
integrated a degree-`2(N-1)` polynomial from time one.  E.16 pays the region
where that polynomial may grow by the already available `K_T`; E.17 invokes
the tail formula only once exponential decay dominates.  This removes the
factorial without asserting a new exponential-sum theorem.

The remaining `exp(Cq)` factor is not shown sharp.  The spatial
Turan--Nazarov observation already costs an absolute base to order `q`, and
the one-sided endpoint proof retains the same order.  No matching lower
bound was established.

R0.75R is not a counterexample to E.3.  Its arbitrary packet has a mode count
of exponential scale in `L^2` and uses a different initial short clock; it
does not satisfy `q=o(L^2)` and is outside the exact-family conclusion.

## 5. Stop rule and exact boundary

The search stopped after the two imported claims were reconfirmed, the two
closest Nikolskii variants were classified as non-inputs, and the delayed
split closed both weighted and endpoint rows without a missing source.
Additional approximation-theory variants were unlikely to change the proof
dependencies.

The sources do not prove E.15--E.22, the complete-real energy identity, the
physical mass conversion, the `q=o(L^2)` shear corollary, arbitrary-packet
control, Version-M extraction, suitable-weak transfer, regularity, or
singularity.  Finite arithmetic may audit the split and exponent ledgers but
not any imported continuum inequality.  The bounded search establishes no
literature completeness, novelty, priority, or sharpness.  **NOT CLAY.**
