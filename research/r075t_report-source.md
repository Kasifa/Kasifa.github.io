# R0.75T source report -- sparse local observability and the two-wave beat defect

## 0. Search scope

- Frozen proposition: `research/r075t_two_harmonic_collar_coercivity.md`.
- Question: whether a published sparse-exponential or torus spectral
  inequality already supplies the carrier-uniform, phase-sharp lower bound
  T.3 for exactly two real harmonics on the canonical radial plateau.
- Search date: 2026-09-04.
- Sources admitted to the mathematical ledger: primary papers/preprints and
  the official Clay problem description.
- Exclusions: citation-count claims, an exhaustive priority search,
  subscription-only theorem reconstruction, the unproved temporal estimate
  T.31, and any regularity conclusion.

## 1. Primary records

### Kovrizhkin: Logvinenko--Sereda for bounded unions of frequency intervals

- O. Kovrizhkin, *Some results related to the Logvinenko-Sereda theorem*,
  arXiv:math/0012186 (2000),
  <https://arxiv.org/abs/math/0012186>.
- The primary abstract states polynomial determining-set bounds for Fourier
  support in one interval and extensions to a bounded number of intervals.
- Relevance: it confirms that local norm recovery for a bounded number of
  spectral pieces is an established uncertainty-principle mechanism.
- Boundary: the source does not state the exact two-real-wave defect
  `(A-C)^2+AC min{1,(d ell)^2+delta_pi^2}`, does not use the project's radial
  fibre, and does not supply T.31.

### Egidi--Veselic: scale-free torus spectral inequalities

- M. Egidi and I. Veselic, *Scale-free unique continuation estimates and
  Logvinenko-Sereda Theorems on the torus*, arXiv:1609.07020v6 (2020),
  <https://arxiv.org/abs/1609.07020>.
- The primary record treats torus spectral subspaces whose Fourier support is
  contained in a finite number of parallelepipeds, with constants depending
  on the observation geometry and the number of spectral pieces.
- Relevance: it is adjacent to observing a dyadic pair on a physical subset
  of the torus.
- Boundary: the R0.75T observation set shrinks with `R`, and T.3 retains the
  exact cancellation phase and beat distance.  The note therefore proves its
  fixed two-dimensional estimate directly rather than importing a general
  thick-set constant.

### Official Millennium problem boundary

- C. Fefferman, *Existence and Smoothness of the Navier--Stokes Equation*,
  official Clay Mathematics Institute problem description,
  <https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf>.
- Relevance: it fixes the global three-dimensional existence/smoothness or
  breakdown target against which the local exact-shear results must be
  bounded.
- Boundary: T.3 is a deterministic local inequality for a two-harmonic exact
  shear subfamily.  It proves neither global regularity nor finite-time
  breakdown.

## 2. Claim ledger

| R0.75T claim | literature status | source imported into proof | boundary | status |
|---|---|---|---|---|
| local recovery for finitely many spectral pieces is a known neighboring mechanism | supported | none | general constants do not retain the sharp beat defect | contextual only |
| the plateau fibre on `|x_2|<=aR/2` has area `4 pi a delta_0 R^2` | no external source needed | exact local geometry | Euclidean chart and frozen radial shell only | proved locally |
| slow carrier-envelope sampling T.13 is uniform as `d ell` tends to zero | no matching source used | elementary two-dimensional Gram compactness and one integration by parts | exactly two envelope modes | proved locally |
| T.3 has the sharp defect `(A-C)^2+AC q^2` | no matching source found in the bounded screen | exact local trigonometric calculation | one dyadic pair and `m aR>=C_0` | proved locally |
| T.6 retains unequal heat rates | no source imported | pointwise application of T.3 to the exact solution | constant shear and two horizontal modes | proved locally |
| the complete two-mode flux is paid by T.6 | unsupported | none | requires T.31 and the self/sum rows | explicitly open |
| R0.75T advances the Clay problem directly | unsupported | none | no arbitrary field, suitable-weak transfer, regularity, or singularity theorem | explicitly excluded |

## 3. Collision and novelty boundary

The bounded search found general local observability theorems that are
compatible with a positive two-mode result.  They are deliberately broader
in spectral support and coarser in the dependence on the observation set.
They do not replace the local proof of the phase-sharp beat defect, and they
do not close the moving-phase flux estimate T.31.

This source report is not a completeness, novelty, or priority certificate.
The defensible statement is narrower: T.3 is proved self-contained in the
frozen project, while the screened primary records provide adjacent
uncertainty-principle context.

## 4. Research consequence

The literature screen does not justify abandoning the dyadic-pair route, but
it also does not turn the spatial lemma into a general multimode theorem.
The next nonredundant step is local and analytic: combine the exact radial
coefficient `J_(d,R)`, the frozen onset bound for `eta`, unequal heat damping,
and the scalar defect `H_(d,aR)(t)` in T.31.  A generic spectral inequality is
unlikely to preserve all four structures simultaneously.

**Established locally:** one sharp spatial coercivity row for exactly two
dyadic harmonics and its diffusive time-slice corollary.

**Still open:** T.31; complete two-harmonic payment; low carriers; three or
more modes; arbitrary packets and fields; Version-M extraction; suitable
weak solutions; regularity; and singularity.  **NOT CLAY.**
