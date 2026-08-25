# R0.71C literature audit — positive strain, dynamic frequency cutoffs, and localized flux boundaries

**Date:** 2026-08-25

**Scope:** a bounded primary-source audit for three questions:

1. whether an established theorem propagates the R0.71B signed Fourier-output
   coefficient from Leray energy data;
2. whether known positive-part criteria retain the same sign information;
3. what a time--frequency localization must preserve before it can claim a
   genuinely new estimate.

The search covered positive strain criteria, BMO/Besov continuation,
frequency-localized dissipation ranges, positive Carleson square spaces,
localized vorticity estimates, and large-data local energy/enstrophy
estimates.  I found no primary source that derives

\[
 \int_0^T a_+(t)\,dt<\infty
 \tag{1.1}
\]

from the Leray energy inequality or another unconditional a priori estimate.
This is a negative literature finding, not a novelty or priority claim.

## 1. Claim matrix

| Primary source | Established statement used here | R0.71C boundary |
|---|---|---|
| [Miller 2020](https://arxiv.org/abs/1710.05569) | Scale-critical blow-up criteria can be written using the positive part of the middle eigenvalue of the physical-space strain tensor | This is a genuine positive-part criterion, but it assumes the required time integrability and acts pointwise in physical space; it does not propagate the Fourier output coefficient (a_+) |
| [Kozono--Taniuchi 2000](https://doi.org/10.1007/s002090000130) and [Nakai--Yoneda 2012](https://doi.org/10.2969/jmsj/06420399) | BMO and stated dyadic-BMO time norms give continuation criteria through sign-blind norm estimates | Taking absolute values or square functions before the estimate removes the R0.71A output sign |
| [Cheskidov--Shvydkoy 2007](https://arxiv.org/abs/0708.3067) | Continuity, or sufficiently small jumps, in (B^{-1}_{\infty,\infty}) regularize a Leray--Hopf solution | The criterion is frequency localized but depends on amplitude, not the sign of a nonlinear output |
| [Cheskidov--Shvydkoy 2011](https://arxiv.org/abs/1102.1944) | A dynamic dissipation wavenumber (\Lambda(t)=2^{Q(t)}) separates viscous high modes from low modes; (f(t)=\sup_{q\le Q(t)}2^q\|u_q\|_\infty\in L^1_t) gives regularity; every Leray--Hopf solution has (\Lambda\in L^1_t), while (\Lambda\in L^{5/2}_t) suffices for regularity | This is the closest existing dynamic scaffold, but (f\in L^1_t) is already a continuation assumption and the unconditional (L^1_t) bound on (\Lambda) is below the scale-correct power needed for (a_+) |
| [Koch--Tataru 2001](https://doi.org/10.1006/aima.2000.1937) | Small (BMO^{-1}) data give global mild solutions; the solution space contains a positive heat-extension Carleson square norm | The square is positive and sign blind, and the theorem is a small-data fixed-point result rather than an unconditional large-data propagation law |
| [Bradshaw--Grujić 2014](https://arxiv.org/abs/1309.2519) | A localized (L\log L) vorticity estimate follows under an additional geometric vorticity-direction condition | The proof supplies an absolute bound under extra geometry; it does not control signed Fourier-output variation from energy alone |
| [Dascaliuc--Grujić 2013](https://doi.org/10.1007/s00220-012-1595-8) | Physical-scale enstrophy-cascade conclusions follow under stated coherence, modulation, and scale hypotheses | A positive cover-averaged physical flux is not an upper bound for the sum of squared positive Fourier outputs |
| [Tao 2012](https://arxiv.org/abs/1108.1165) | Large-data localization uses explicit localized energy and enstrophy estimates and keeps forcing, boundary, and transport effects | A proposed local signed tent cannot simply localize a global algebraic identity and discard commutator or boundary flux terms |

## 2. Positive part in physical space is not positive Fourier output

Miller's criterion uses the positive part (\lambda_2^+(x,t)) of the
middle eigenvalue of the strain matrix.  It is important evidence that only
one sign of strain production can matter in a continuation theorem.  It does
not identify

\[
 \lambda_2^+(x,t)
 \quad\text{with}\quad
 \frac{(w_k^+(t))^2}
 {4|k|^2|\widehat S(k,t)|_F^2}.
 \tag{2.1}
\]

Physical-space diagonalization, Fourier localization, positive part, and
squaring do not commute.  Therefore the middle-eigenvalue theorem neither
proves nor refutes the R0.71B coefficient's time integrability.

## 3. BMO, Besov, and Carleson estimates lose the relevant sign

The established BMO/Besov arguments estimate nonlinear terms through
triangle inequalities, maximal functions, logarithmic Sobolev estimates, or
positive square functions.  These tools are invariant under a sign change of
one scale coefficient.  The R0.71A pair was built precisely so that the
pointwise covariance is unchanged while the signed work reverses.

Consequently, a proof of the form

\[
 a_+(t)\lesssim \|\omega(t)\|_{\mathrm{BMO}}
 \quad\text{or}\quad
 a_+(t)\lesssim
 \|\omega(t)\|_{\dot B^0_{\infty,\infty}}
 \tag{3.1}
\]

would only reduce the new coefficient to an established continuation
assumption.  It would not propagate (a_+) from energy data.

## 4. The dynamic dissipation-wavenumber comparison must be dimensionally correct

Under Navier--Stokes scaling, (a_+) has inverse-time scaling and
(\Lambda) has wavenumber scaling.  A dimensionally compatible comparison is
therefore of the form

\[
 a_+(t)\lesssim \nu\Lambda(t)^2+R(t),
 \tag{4.1}
\]

not (a_+\lesssim\Lambda).  The unconditional result
(\Lambda\in L^1_t) does not make (\nu\Lambda^2) integrable.  On the other
side, (f\in L^1_t) and (\Lambda\in L^{5/2}_t) are already sufficient
regularity assumptions in the cited work.

This leaves a precise gap.  A useful bridge would have to control the
signed refinement or flux defect by a quantity strictly below those known
regularity-side assumptions, while using only independently propagated
information.

## 5. Localizing the equation creates terms that the signed output does not contain

For a Fourier multiplier (T_j),

\[
 (\partial_t+u\cdot\nabla-\nu\Delta)T_j\omega
 =T_j(S\omega)+[u\cdot\nabla,T_j]\omega.
 \tag{5.1}
\]

Adding a spatial cutoff also creates transport through the cutoff boundary.
At the bottom of a parabolic tent, where (2^j\ell(Q)\simeq1), the multiplier--
cutoff commutator has no small scale ratio.  A correct local balance must
therefore retain at least:

1. transport--filter commutators;
2. cutoff boundary flux;
3. vertical heat flux and viscous product terms;
4. pressure-Hessian contributions inherited from the strain equation.

Tao's localized energy/enstrophy framework supports this design boundary:
large-data localization is an equation with fluxes and error terms, not a
pointwise localization of a global identity.

## 6. Literature stop and next admissible target

After two bounded search waves, additional sources repeated the same split:

- positive-part theorems are conditional and physical-space;
- BMO/Besov/Carleson theorems are sign blind;
- dynamic frequency cutoffs require a separately integrable low-mode or
  dissipation-wavenumber quantity;
- physical localization retains explicit flux and commutator terms.

The next admissible target is therefore not another norm comparison.  It is
an exact local balance with explicit horizontal transport, heat-vertical,
and cutoff fluxes, followed by a proof that the resulting flux terms
telescopically control the nonnegative refinement defect.  If those terms
are paid by an already sufficient BMO/Besov hypothesis, the route is
circular and should stop.
