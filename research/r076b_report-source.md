# R0.76B primary-source boundary -- fixed-term high-carrier observation

## 0. Scope and direct answer

- Search date: 2026-09-04.
- Question: which established results justify the measurable-set observation
  used after carrier scaling, and whether the combined inverse-radius collar
  payment is already supplied by those sources.
- Search class: original or author-posted mathematical sources on
  Turan--Nazarov, exponential sums, and Bernstein/Markov-type inequalities.
- Exclusions: an exhaustive citation graph, novelty or priority, arbitrary
  growing packets, general Navier--Stokes fields, and regularity.

The only external theorem imported into R0.76B is the Turan--Nazarov
measurable-set inequality for a finite exponential polynomial.  It propagates
the value of the carrier-scaled polynomial from a positive-measure subset of
`alpha I` to `alpha J^+` with a constant depending on the number of terms and
the interval/subset ratio, but not on imaginary frequencies or gaps.

The local derivative bound is proved in R0.76B from compactness of the
finite-order companion ODE after scaling all frequencies into `[1,2]`.  The
complete-clock endpoint trace is a second direct corollary of the same
Turan--Nazarov theorem.  None of the sources below states the full-real-field
local energy identity, the `alpha/a<=1` gradient absorption, the plateau mass
conversion, or the signed-flux estimate B.5.

The Deep Research planning helper required by the selected research skill was
not available in this environment.  The two-wave bounded search, primary
records, claim ledger, and stop rule are therefore recorded directly here.

## 1. Primary sources

### Nazarov's original local estimate

F. L. Nazarov, *Local estimates for exponential polynomials and their
applications to inequalities of the uncertainty principle type*, Algebra i
Analiz 5:4 (1993), 3--66; English translation, St. Petersburg Mathematical
Journal 5:4 (1994), 663--717.

Bibliographic record and linked full text:
<https://www.mathnet.ru/eng/aa397>.

This is the original source of the positive-measure local estimate used in
B.18 and B.23.  The exact displayed dependence was cross-checked through the
accessible primary restatement below.

### Accessible primary restatement

Omer Friedland and Yosef Yomdin, *An observation on the Turan--Nazarov
inequality*, Studia Mathematica 218 (2013), 27--41.

Author manuscript: <https://arxiv.org/abs/1107.0039>.

The abstract records that the imaginary parts of the exponents do not enter
the original inequality.  Theorem 1.1 gives the interval/measurable-subset
form for complex exponential polynomials.  Its factor depends on the number
of terms, the interval length, the subset measure, and the real parts; it has
no imaginary-frequency or exponent-gap denominator.  R0.76B uses the original
positive-measure theorem, not the later metric-span extension.

## 2. Adjacent literature checked, but not imported

Tamas Erdelyi, *Inequalities for exponential sums*, studies endpoint,
Nikolskii, Bernstein, and Markov-type inequalities for finite exponential-sum
classes.  Primary records:
<https://www.mathnet.ru/eng/sm8670> and
<https://arxiv.org/abs/1602.02315>.

Alexander Brudnyi, *Bernstein Type Inequalities for Quasipolynomials*, Journal
of Approximation Theory 112 (2001), 28--43.
Primary DOI record: <https://doi.org/10.1006/jath.2001.3576>.

These sources confirm that derivative inequalities for exponential sums and
quasipolynomials are an established neighboring subject.  R0.76B does not
quote a quantitative derivative constant from them.  Its needed statement is
only a fixed-order, compact-frequency, unit-window estimate, and the note
proves that statement directly by companion-matrix compactness, including
colliding-root limits.

For terminology and historical cross-checking, the survey by Philippe Jaming
and Chadi Saba was also retained:
<https://arxiv.org/abs/2311.17714>.  It is contextual, not a proof dependency.

## 3. Claim-to-source ledger

| claim | evidence | use | exact boundary |
|---|---|---|---|
| measurable-set control of an `N`-term exponential polynomial | Nazarov; Friedland--Yomdin Theorem 1.1 | B.18 and B.23 | constant depends on `N` and real parts |
| no imaginary-frequency or frequency-gap factor | Friedland--Yomdin abstract and theorem | permits arbitrary shear speed and collisions | not uniform as `N` grows |
| high-carrier value observation after scaling | R0.76B B.16--B.18 | ratio `|alpha J^+|/|E|<=8` | fixed `q` only |
| local first-derivative observation | R0.76B B.19--B.20 | compact companion ODE | no quantitative `q` growth claimed |
| terminal `L^3` trace | R0.76B B.22--B.25 | half-measure corollary | requires the bounded real parts supplied by `alpha<=a` |
| collar-flux payment B.5 | R0.76B B.28--B.37 | full-field energy identity and scaling | not attributed to an external source |

## 4. Collision screen

The focused search combined `Turan Nazarov measurable set`, `exponential
polynomial local observation`, `Bernstein exponential sums`, `frequency gap
independent`, `dyadic trigonometric polynomial`, and `localized flux` with
the primary-source classes above.  It located the generic observation and
derivative-inequality literature, but no source in the bounded screen stated
the project-specific combination:

1. carrier scaling on a fixed dyadic band;
2. fixed-term value propagation from the plateau interval;
3. a local companion-ODE derivative row;
4. the complete real-square transport identity with the frozen radial
   primitive; and
5. the physical plateau-mass conversion in B.37.

This negative result is not evidence of novelty or priority.  The search was
stopped because both imported external claims had direct primary support and
broader keyword variants ceased to change the proof dependencies.

## 5. Exact source boundary

The sources support only the generic exponential-polynomial observation and
the absence of an imaginary-frequency or gap penalty.  They do not prove the
local ODE compactness lemma, the radial energy identity, the inverse-radius
gradient absorption, arbitrary-packet control, Version-M extraction,
suitable-weak transfer, regularity, or singularity.  R0.76B makes no
completeness, novelty, or priority claim.  **NOT CLAY.**
