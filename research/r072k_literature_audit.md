# R0.72K bounded literature audit -- directional zero sampling

**Search cutoff:** 2026-08-27

## 1. Direct decision

The bounded search found several neighboring theories but no checked source
that directly states the following fixed-level endpoint-slope packing formula
for arbitrary real or complex Banach-valued curves:

\[
 \sum_{j=2}^m\|X'(t_j)\|^2
 \le 2\int_I\|X'(t)\|\,\|X''(t)\|\,dt,
 \qquad X(t_j)=0.
\]

The proof used in R0.72K is elementary and self-contained.  I do not claim
that the lemma, its constant, or its proof is new.  The search result is only
a non-collision check for the wording and citation boundary of this project.

## 2. Primary-source matrix

| Source | What it proves | Relation to R0.72K |
|---|---|---|
| R. M. McLeod, [*Mean Value Theorems for Vector Valued Functions*](https://doi.org/10.1017/S0013091500008786), *Proceedings of the Edinburgh Mathematical Society* 14 (1965), 197--209 | Formulates vector-valued mean-value conclusions through linear functionals and closed convex hulls, and records why a pointwise vector derivative analogue fails. | It supports the Hahn--Banach projection viewpoint, but does not state the weighted sum of squared endpoint derivatives over an arbitrary root set. |
| Z. Opial, [*Sur une inégalité*](https://doi.org/10.4064/ap-8-1-29-32), *Annales Polonici Mathematici* 8 (1960), 29--32 | The classical integral inequality controlling \(\int|ff'|\) for a real scalar function with endpoint conditions. | It is the closest classical integral-inequality family, but it does not sum \(|X'(t_j)|^2\) at an arbitrary number of fixed-level roots. |
| G. G. Vrânceanu, *On an inequality of Opial*, *Bull. Math. Soc. Sci. Math. R. S. Roumanie* 17(65) (1973), 315--316 (published 1975) | Extends an Opial inequality to Hilbert-space-valued functions. | It controls an integral inner-product quantity from endpoint data, not the discrete derivative mass at every endogenous zero. |
| W. Stadje, [*On functions with derivative of bounded variation: an analogue of Banach's indicatrix theorem*](https://doi.org/10.1017/S0013091500017417), 1986 | Gives an indicatrix-type description for primitives whose derivative has bounded variation. | Indicatrix results average crossings over levels; R0.72K fixes the exceptional level zero and weights its derivative values. |
| S. Banach, [*Sur les lignes rectifiables et les surfaces dont l'aire est finie*](https://doi.org/10.4064/fm-7-1-225-236), 1925 | Relates variation to crossing counts integrated over the level. | It does not provide a deterministic squared-slope sum at one selected level. |
| F. J. Narcowich, J. D. Ward, and H. Wendland, [*Sobolev bounds on functions with scattered zeros*](https://doi.org/10.1090/S0025-5718-04-01708-9), 2005 | Controls lower Sobolev norms of functions vanishing on an externally prescribed set with fill-distance geometry. | The R0.72K roots are endogenous, need no separation or fill distance, and the sampled object is the derivative at the roots. |
| D. Novikov and S. Yakovenko, [*A complex analogue of the Rolle theorem and polynomial envelopes of irreducible differential equations in the complex domain*](https://doi.org/10.1112/S002461079700536X), 1997 | Bounds complex zeros for solutions of special analytic differential equations using complex growth and equation structure. | R0.72K neither finds a zero of the complex derivative nor counts complex-domain zeros; it projects the real-time derivative separately on each root gap. |
| Y. Il'yashenko and S. Yakovenko, [*Counting real zeros of analytic functions satisfying linear ordinary differential equations*](https://doi.org/10.1006/jdeq.1996.0045), 1996 | Gives generalized Jensen/Bernstein-index bounds in nested complex domains, with an explicit growth gap. | The growth ratio plays the role of an analytic anchor. The directional lemma needs no complex domain and does not count zeros. |
| M. Voorhoeve, *On the oscillation of exponential polynomials*, *Mathematische Zeitschrift* 151 (1976), 277--294 | Introduces an oscillation index used as a complex replacement for zero-number Rolle arguments in exponential-polynomial settings. | It is a complex analytic counting framework, not the fixed-level derivative-mass inequality used here. |
| K. Masuda, [*On the Analyticity and the Unique Continuation Theorem for Solutions of the Navier--Stokes Equation*](https://doi.org/10.3792/pja/1195521421), 1967 | Proves analyticity and unique continuation for classical Navier--Stokes solutions. | Time analyticity isolates nontrivial scalar zeros but does not sum all root slopes from the mixed-row and cubic actions. |
| Y. Giga, K. Jo, A. Mahalov, and T. Yoneda, [*On time analyticity of the Navier--Stokes equations with spatially almost periodic data*](https://doi.org/10.1016/j.physd.2008.03.007), 2008 | Gives complex-time sectors and a no-sudden-creation statement for a Fourier class. | It supplies no root-separation-free weighted slope ledger. |

## 3. Why this is not a complex Rolle theorem

The curve

\[
 X(t)=e^{2\pi it}-1,
 \qquad 0\le t\le1,
\]

has two endpoint roots but \(X'(t)=2\pi i e^{2\pi it}\) never vanishes.
Therefore a literal complex-valued Rolle step is false.  R0.72K chooses a
different norming functional on each root gap.  Its real projection has mean
zero because the curve has equal endpoint values.  Only that real projection
is asserted to vanish.

The argument is consequently outside the zero-counting objectives of
Novikov--Yakovenko and Voorhoeve.  It also needs no holomorphic extension,
complex radius, lower anchor, or root separation.

## 4. Why Opial and indicatrix estimates do not already close the ledger

Classical Opial inequalities estimate an integral involving a function and
its derivative.  The R0.72K lemma instead begins with the endpoint derivative
direction, uses the zero-area constraint on its real projection, and charges
one endpoint value to

\[
 \int_{t_{j-1}}^{t_j}\|X'\|\,\|X''\|.
\]

The disjointness of the root gaps then removes both root count and minimum
spacing.  Banach-indicatrix results integrate crossing counts over levels,
whereas zero is a fixed endogenous level here.  Scattered-zero estimates pay
fill distance and control a continuous Sobolev norm, not this atomic endpoint
mass.

## 5. Project-specific Navier--Stokes interface

The abstract lemma alone does not know the Navier--Stokes equation.  The
closure uses the exact target identities

\[
 F_0'+\lambda_0F_0=\delta h,
 \qquad
 h'+\lambda_0h=QF+\delta P_0V^2F.
\]

The integrating factor places \(QF\) and the true cubic row in \(X''\).
R0.72H already paid \(\int|hQF|\) with the reciprocal critical-log shear
moment, and R0.72J already paid the true cubic integral by the minimum of an
action branch and a joint heat-exposure branch.  None of the cited sources
contains this exact combination.

## 6. Search boundary

The search covered:

- Opial, Beesack--Opial, and Hilbert-valued Opial inequalities;
- vector-valued mean-value theorems and Hahn--Banach scalarization;
- Banach indicatrix, bounded-variation crossing, and fixed-level sampling;
- scattered-zero Sobolev estimates;
- complex Rolle, Voorhoeve index, Jensen, and analytic zero counting;
- Hilbert/Banach-valued mean-value and endpoint inequalities;
- Navier--Stokes time analyticity and Fourier-mode zero statements.

Further searches repeated the same source families or returned surveys and
lecture notes.  The search therefore stopped at saturation.  Absence from
this bounded search is not evidence of global novelty or priority.
