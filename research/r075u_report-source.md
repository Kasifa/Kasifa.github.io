# R0.75U source report -- weighted phase cancellation on the complete clock

## 0. Search scope

- Frozen proposition: `research/r075u_two_harmonic_difference_frequency_payment.md`.
- Question: whether a cited phase-mixing, heat-observability, or sparse
  spectral theorem is being used to justify the weighted scalar inequality
  U.13 or the two-harmonic difference-frequency payment U.4.
- Search basis: the bounded primary-source screens already frozen in R0.75S
  and R0.75T, checked against the exact new proof.
- Exclusions: a fresh exhaustive citation graph, general multimode
  observability, the three unclosed self/sum rows, and any regularity claim.

## 1. Primary neighboring records

### Constant/variable shear mixing and enhanced dissipation

- J. Bedrossian, V. Vicol, and F. Wang, *The Sobolev stability threshold for
  2D shear flows near Couette*, arXiv:1604.01831,
  <https://arxiv.org/abs/1604.01831>.
- Relevance: the primary paper is neighboring context for shear-induced phase
  mixing and diffusion.
- Boundary: U.13 is an elementary one-dimensional weighted oscillatory
  inequality for a frozen cutoff, not an imported enhanced-dissipation
  theorem.  The proof keeps its exact finite interval and onset condition.

### Torus spectral observability

- M. Egidi and I. Veselic, *Scale-free unique continuation estimates and
  Logvinenko-Sereda Theorems on the torus*, arXiv:1609.07020v6,
  <https://arxiv.org/abs/1609.07020>.
- Relevance: this is adjacent context for recovering spectrally restricted
  functions from subsets of a torus.
- Boundary: the spatial two-wave coercivity was proved locally in R0.75T;
  U uses that frozen lemma and proves only its missing time-phase row.  No
  scale-free observability constant is inserted into U.13.

### Heat observability from thick sets

- G. Wang, M. Wang, C. Zhang, and Y. Zhang, *Observable set, observability,
  interpolation inequality and spectral inequality for the heat equation in
  R^n*, arXiv:1711.04279,
  <https://arxiv.org/abs/1711.04279>.
- Relevance: it supplies neighboring heat-observability context.
- Boundary: U uses the explicit scalar weight `e^(-Lambda s)`, elementary
  Laplace moments, and one bounded-variation integration by parts.  It does
  not invoke a thick-set heat theorem.

### Official Millennium problem boundary

- C. Fefferman, *Existence and Smoothness of the Navier--Stokes Equation*,
  official Clay Mathematics Institute description,
  <https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf>.
- Relevance: it fixes the global three-dimensional target.
- Boundary: U.4 controls one cross-frequency component of one explicit smooth
  shear subclass.  It proves neither global regularity nor breakdown.

## 2. Claim ledger

| R0.75U claim | literature status | source imported into proof | boundary | status |
|---|---|---|---|---|
| shear can create an oscillatory phase that interacts with diffusion | established neighboring mechanism | none | broad context only | contextual |
| U.13 holds uniformly in `Lambda,sigma,alpha` | no cited theorem used | exact local proof by phase-distance moment, cutoff onset, Laplace moments, and BV integration | interval `[0,4]`, frozen cutoff class | proved locally |
| `|J_(n,R)|/n<=Ca^2R^3` | inherited exact local radial row | R0.75S algebra only | canonical radial cutoff | proved locally |
| U.24 cancels `AC` and has factor `d^(-1)R^(-4/3)` | no source needed | exact nondimensionalization | one difference frequency | proved locally |
| the two-mode difference row obeys the target two-thirds payment | no matching source imported | U.10, U.13, and R0.75T coercivity | one dyadic pair with `maR>=C_0` | proved locally |
| the complete two-mode flux is paid | unsupported | none | self frequencies and sum frequency remain | explicitly open |
| U advances the Clay problem directly | unsupported | none | no arbitrary-field or suitable-weak theorem | explicitly excluded |

## 3. Collision and completeness boundary

The screened primary records support only the surrounding mechanisms:
spectral observability, shear phase mixing, and heat observability.  None
states the onset-weighted scalar inequality U.13 with the phase-node cubic
moment, and none closes the exact radial difference-frequency row U.4.

The U proof is therefore self-contained.  This bounded report is not an
exhaustive novelty or priority search.  It supports the more modest claim
that no external theorem has been silently substituted for U.13.

## 4. Research consequence

The low difference frequency is no longer the missing part of the dyadic-pair
argument.  The next calculation must preserve the algebraic cancellation
among `J_(2k,R)`, `J_(2m,R)`, and `J_(k+m,R)` rather than bound those three
terms separately against the masses of the two component waves.

**Established locally:** complete-clock payment of the single difference
frequency for one exact dyadic pair.

**Open:** the combined self/sum block; complete two-mode payment; low
carriers; three or more modes; arbitrary packets and fields; Version-M
extraction; suitable-weak transfer; regularity; and singularity.
**NOT CLAY.**
