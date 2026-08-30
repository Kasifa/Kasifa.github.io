# R0.73K literature audit: vanishing-viscosity spectral persistence

**Status:** bounded primary-source audit complete

**Search boundary:** sources directly bearing on isolated inviscid eigenvalues,
singular viscous limits, Riesz projections, periodic Evans functions, and
complementary semigroup control

**Claim discipline:** “not found in the sources checked” is not an absolute
nonexistence claim

## 1. Literature decision

The general phenomenon behind R0.73K is known: an isolated unstable
Euler/Rayleigh spectral cluster can persist under vanishing viscosity, with
algebraic multiplicity preserved.  The proposed theorem is therefore not a
first general vanishing-viscosity persistence theorem.

The profile-specific contribution is narrower.  In the primary sources
checked, no theorem was found that simultaneously supplies, for the present
fixed Fourier row and the whole compact heat-profile interval,

\[
 \operatorname{rank}P_\varepsilon(d)=1,
 \qquad
 \sup_d\|P_\varepsilon(d)-P_0(d)\|\to0,
 \tag{1.1}
\]

\[
 \sup_d|\lambda_\varepsilon(d)-\lambda_0(d)|=O(\varepsilon),
 \tag{1.2}
\]

together with a full fixed-half-plane reduced-resolvent and complementary
semigroup bound.  Those are the exact R0.73K proof obligations.

## 2. Closest general periodic theorem

Shvydkoy and Friedlander prove a general unstable-spectrum persistence
theorem for Navier--Stokes operators on tori.  Their Theorem 2.1 states that
an isolated Euler eigenvalue to the right of the essential spectral threshold
is approached by viscous eigenvalues; total algebraic multiplicity is
preserved, and the associated Riesz spectral subspaces converge.  The proof
uses strong resolvent convergence and finite-dimensional reduction.

- R. Shvydkoy and S. Friedlander,
  [*The unstable spectrum of the Navier--Stokes operator in the limit of
  vanishing viscosity*](https://www.numdam.org/articles/10.1016/j.anihpc.2007.05.004/),
  Ann. Inst. H. Poincaré C 25 (2008), 713--724;
  [arXiv version](https://arxiv.org/abs/math/0509538).

This is the correct general precedent.  It does not state the operator-norm
projection convergence in (1.1), does not retain a second compact profile
parameter with common constants, and gives no rate of the form (1.2).

## 3. Why full Kato norm-resolvent convergence is unavailable

Kato's generalized convergence of closed operators, when a common resolvent
point exists, is equivalent to operator-norm convergence of the resolvent at
one such point.  Under that hypothesis separated spectral sets and their
Riesz projections are stable.  Kato also proves that a generalized limit of
operators with compact resolvent has compact resolvent.

- T. Kato,
  [*Perturbation Theory for Linear Operators*, second edition](https://doi.org/10.1007/978-3-642-66282-9),
  Chapter IV, Theorems 2.25, 2.26, and 3.16; Chapter VII, Sections 1--2.

That hypothesis is impossible here.  For \(\varepsilon>0\),
\(B_\varepsilon(d)\) has compact resolvent because of the elliptic term.
At \(\varepsilon=0\), \(B_0(d)=M_d+K_d\) retains the noncompact multiplication
resolvent and essential spectrum.  A norm limit of compact resolvents would
be compact, which contradicts the inviscid structure.  Kato's type-A theory
does apply in the profile variable \(d\) for each fixed positive viscosity,
because the domain is then the common space \(H^2_{\rm per}\).  It does not
make the family analytic in \(\varepsilon\) through zero.

## 4. Collective compactness and the two-sided sandwich

Anselone and Palmer show that strong convergence plus collective compactness
controls resolvents and spectral subspaces.  Their Hilbert-space norm
convergence criterion also explains why control of the adjoint family is
needed to upgrade strong convergence to operator-norm convergence.

- P. M. Anselone and T. W. Palmer,
  [*Spectral analysis of collectively compact, strongly convergent operator
  sequences*](https://doi.org/10.2140/pjm.1968.25.423),
  Pacific J. Math. 25 (1968), 423--431;
  [journal PDF](https://msp.org/pjm/1968/25-3/pjm-v25-n3-p02-s.pdf).

R0.73K uses a more concrete version of this mechanism.  The dissipative base
resolvents and their adjoints converge jointly strongly; the norm-continuous
compact family \(K_d\) is then placed on both sides.  This gives operator-norm
convergence only for the compact Fredholm correction, not for the full base
resolvent.

Gohberg--Sigal operator Rouché theory supplies an alternative way to preserve
the total multiplicity once the Fredholm factor is uniformly close on a
contour:

- I. C. Gohberg and E. I. Sigal,
  [*An operator generalization of the logarithmic residue theorem and the
  theorem of Rouché*](https://doi.org/10.1070/SM1971v013n04ABEH003702),
  Math. USSR-Sb. 13 (1971), 603--625.

That theorem counts characteristic values; it does not by itself give the
projection norm, the \(O(\varepsilon)\) eigenvalue rate, or the complement
semigroup estimate.  The direct Riesz-integral proof is retained for those
reasons.

## 5. Orr--Sommerfeld precedents and their geometry mismatch

Several primary papers continue unstable Rayleigh modes to viscous
Orr--Sommerfeld modes, but their boundary-layer geometry changes the scale.

1. Li and Lin use a fourth-order Evans determinant and Rouché's theorem for
   oscillatory Couette profiles in a no-slip channel:
   Y. C. Li and Z. Lin,
   [*A Resolution of the Sommerfeld Paradox*](https://doi.org/10.1137/100794912),
   SIAM J. Math. Anal. 43 (2011), 1923--1954;
   [arXiv](https://arxiv.org/abs/0904.4676).
   The result is local to a fixed profile and mode and does not provide the
   Riesz projection or compact-profile uniformity required here.

2. Quarisa and Rodrigo give an exact multiplicity count and eigenvalue scale
   near a Rayleigh root for a half-line problem with viscosity-dependent
   Navier boundary conditions:
   L. Quarisa and J. L. Rodrigo,
   [*The adjoint Rayleigh and Orr--Sommerfeld equations: Green function and
   eigenmodes*](https://arxiv.org/abs/2304.08696),
   J. Math. Anal. Appl. 543 (2025), 128884.
   Its wall modes naturally yield fractional viscosity scales.  Those scales
   neither prove nor disprove the \(O(\varepsilon)\) rate in the present
   boundaryless periodic problem.

3. Grenier and Nguyen construct viscous modes near a simple unstable Euler
   mode in a Prandtl-layer setting, again with fractional boundary-layer
   scales:
   E. Grenier and T. T. Nguyen,
   [*\(L^\infty\) Instability of Prandtl Layers*](https://arxiv.org/abs/1803.11024),
   Ann. PDE 5 (2019), Article 18.

4. Li obtains an explicit positive viscous eigenvalue for a periodic
   Kolmogorov flow and proves its zero-viscosity convergence for fixed aspect
   ratio:
   Y. C. Li,
   [*Invariant Manifolds and Their Zero-Viscosity Limits for Navier--Stokes
   Equations*](https://doi.org/10.4310/DPDE.2005.v2.n2.a4),
   Dynamics of PDE 2 (2005), 159--186;
   [arXiv](https://arxiv.org/abs/math/0505390).
   The recurrence is profile-specific and the theorem gives neither a compact
   profile family nor projection-norm convergence.

## 6. Recent periodic long-wave result

Colombo, Dolce, Montalto, and Ventura prove a unique simple unstable mode and
a stable remainder for general periodic shears in the regime
\(\alpha|k|=O(\nu)\):

- M. Colombo, M. Dolce, R. Montalto, and P. Ventura,
  [*Long-wave instability of periodic shear flows for the 2D Navier--Stokes
  equations*](https://arxiv.org/abs/2509.18070), 2025 preprint.

The result is important but disjoint from R0.73K.  Here the streamwise wave
number is fixed at \(\gamma=1/2\) while viscosity tends to zero, so the
long-wave assumption eventually fails.  Its rank-one reduction can inform
proof organization but cannot be cited as the present persistence theorem.

## 7. Periodic Evans functions

For fixed-order periodic differential operators, the periodic monodromy
Evans function is analytic and its zero order equals algebraic multiplicity;
it can be compared with a Fredholm determinant:

- K. Zumbrun,
  [*2-Modified Characteristic Fredholm Determinants, Hill's Method, and the
  Periodic Evans Function of Gardner*](https://doi.org/10.4171/ZAA/1469),
  Z. Anal. Anwend. 31 (2012), 463--472.

This does not justify taking a raw fourth-order viscous Evans determinant to
the second-order Rayleigh determinant.  Two viscous fast modes appear when
the order drops at \(\varepsilon=0\); a separate balancing factor and uniform
asymptotics would be required.  R0.73K therefore uses the compact--Fredholm
factorization instead of a singular Evans limit.

## 8. Complementary semigroup boundary

Prüss's Hilbert-space spectral characterization makes the final logical
boundary explicit: an isolated Riesz circle or a spectral gap is not enough
to control a nonnormal semigroup.  A complete vertical-line resolvent bound
is needed.

- J. Prüss,
  [*On the spectrum of \(C_0\)-semigroups*](https://doi.org/10.1090/S0002-9947-1984-0743749-9),
  Trans. Amer. Math. Soc. 284 (1984), 847--857.

R0.73K consequently joins compact-rectangle Fredholm convergence to explicit
high-imaginary and high-real-part estimates before invoking an inverse-Laplace
argument on the reduced space.

## 9. Originality and wording ledger

The strongest evidence-supported wording is:

> For the certified two-harmonic periodic shear family, the section gives a
> self-contained, compact-parameter-uniform specialization of unstable
> vanishing-viscosity spectral persistence, including operator-norm Riesz
> projection convergence, uniform rank-one conditioning, an
> \(O(\varepsilon)\) eigenvalue rate, and fixed-half-plane complement control.

The following wording is not supported:

- “the first vanishing-viscosity instability theorem”;
- “the first Rayleigh-to-Orr--Sommerfeld continuation”;
- “Kato norm-resolvent convergence”;
- “an explicit viscosity threshold”;
- “a proof of nonlinear Navier--Stokes instability”;
- “progress on the Clay regularity problem” without the explicit chain of
  still-open nonlinear and three-dimensional gates.

## 10. Search saturation

The bounded audit covered six directly relevant slots: general periodic
Navier--Stokes spectral persistence, Kato closed-operator convergence,
collectively compact approximation, operator Rouché theory, periodic Evans
functions, and Hilbert-space semigroup resolvent criteria.  Further broad
search is unlikely to change the proof route.  The remaining uncertainty is
mathematical: the project-specific uniform proof and its independent audit.
