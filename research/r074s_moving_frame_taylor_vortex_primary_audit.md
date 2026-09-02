# R0.74S Step 16 — primary analytic audit

## 0. Frozen object and verdict

The reviewed source is
research/r074s_moving_frame_taylor_vortex_obstruction.md, equations
(S.417)--(S.444), SHA-256
de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0.

**Verdict: PASS within the stated negative-theorem scope.  The quadratic
common-deletion estimate (S.342) is false for every \(p>1\), already on a
smooth periodic exact Navier--Stokes family.  The critical \(p=1\) candidate
(S.444), the hybrid terminal gate, Q.12, Q.1, and regularity remain OPEN.
NOT CLAY.**

## 1. Exact PDE and path identities

For

\[
 W=(\sin x_1\cos x_2,-\cos x_1\sin x_2,0),
 \qquad p_W={\cos2x_1+\cos2x_2\over4},
\]

direct differentiation gives

\[
 \nabla\cdot W=0,\qquad
 \Delta W=-2W,\qquad
 (W\cdot\nabla)W=-\nabla p_W.
\]

Thus \(u_A=Ae^{-2(t-t_0)}W\) and
\(p_A=A^2e^{-4(t-t_0)}p_W\) solve the unforced periodic NSE exactly.
The amplitude freedom is valid because this particular \(W\) is both a
steady Euler field and a Laplace eigenfield; no general amplitude symmetry
is asserted.

All velocity modes have length \(\sqrt2\).  The frozen even radial
mollifier therefore gives one real multiplier \(\mu_R\to1\).  For small
\(R\), \(1/2\le\mu_R\le1\).  With terminal centre
\((\pi/4,0,0)\), uniqueness preserves \(\xi_2=\xi_3=0\), and

\[
 {d\over dt}\log\tan{\xi_1\over2}=\mu_RAe^{-2(t-t_0)}.
\]

Backward integration confirms the sign and exponential in (S.423).

## 2. Exact flux sign and radial multiplier

The steady Euler Bernoulli current obeys
\(\nabla\cdot[(|W|^2/2+p_W)W]=0\).  Hence the fixed-frame kinetic and
pressure fluxes cancel after periodic integration by parts.  The
time-dependent pressure gauge also vanishes by incompressibility.

The remaining Version-M drift has exactly

\[
 \dot F_{k,R}
 ={\gamma_k\mu_R\eta_Rb_A^3\over2R}
   W(\xi)\cdot\nabla_\xi J_{k,R}(\xi).
\]

The final sign follows from
\(\int|W(y+\xi)|^2\nabla\Psi_k^R=-\nabla_\xi J_{k,R}\).

Since

\[
 |W|^2={1-\cos2x_1\cos2x_2\over2},
\]

radiality at the two equal-length modes \((2,\pm2,0)\) gives

\[
 J_{k,R}={m_{k,R}\over2}
 +c_{k,R}\left(|W(\xi)|^2-{1\over2}\right).
\]

There is no missing factor of two.  Once \(N\) is fixed, (S.429) makes
\(\cos((2,2,0)\cdot y)\ge1/2\) on each of the first \(N+1\) cutoff
supports, so \(c_{k,R}\ge m_{k,R}/2>0\).  These are different physical
annuli, not Fourier shells.

## 3. Terminal block, time norm, and deletion

On a terminal interval of length \(\delta/A\), the explicit characteristic
keeps \(\xi_1\in[\pi/8,\pi/4]\), while \(\eta_R=1\).  Therefore

\[
 |\dot F_{k,R}|\ge c_{k,R}'A^3
 \qquad(1\le k\le N+1).
\]

The dimensionless interval has length \(\delta/(AR^2)\), and
\(h=R^2|\dot F|\).  Thus

\[
 \|h_{k,R}\|_p\ge c_{p,k,R}A^{3-1/p}.
\]

Any deletion set of size at most \(N\) leaves one of those \(N+1\)
coordinates.  The lower bound (S.435) follows with the deletion fixed
before the time norm.

## 4. Complete payment and exact quantifier negation

On \(I_{8R}\), \(b_A\le Ae^{128R^2}\).  Translation changes phase but not
uniform size.  The complete rows obey

\[
 \mathcal E^{M,R}\le C_RA^2,\qquad
 \mathcal G_{v_R,\pi_R}^{M,R}\le C_RA^3,
\]

\[
 \Lambda_{2R}^{M,R}\le C_RA^2,\qquad
 \mathcal H_{v_R}^{M,R}\le C_RA^3.
\]

The local Riesz pressure, harmonic remainder, and fixed gauge are included;
the relevant all-copy series converge.  Consequently \(P_R^M\le C_RA^3\).
After a proposed \(p>1,N,C\) is fixed, choose the admissible \(R\) above
and let \(A\to\infty\).  Then

\[
 {\mathfrak H^F_{p,N,R}\over(P_R^M)^{2/3}}
 \ge c_{p,N,R}A^{1-1/p}\to\infty.
\]

This is the correct negation of (S.342).  It does not use a singular
solution and does not refute a weaker signed terminal functional.

## 5. Critical endpoint and claim boundary

At \(p=1\), the characteristic substitution
\(d\xi_1=\mu_Rb_A\sin\xi_1\,dt\) cancels \(\mu_R\) and one amplitude
factor.  The all-shell upper bound is \(C_RA^2\), and the terminal block
gives the matching lower amplitude exponent after fixed \(N\)-deletion.
Good times approaching \(t_0\) yield \(P_R^M\ge c_RA^3\).

Hence the family only saturates the \(2/3\) amplitude exponent at fixed
\((N,R)\); it does not prove uniform constants or (S.444).  Equations
(S.386)--(S.387) include \(p=1\).  Rerunning the Step 15 implication
(S.389)--(S.391) with (S.444) as antecedent would make that open critical
candidate sufficient for the hybrid residual.

The accompanying ABC calculation is a corroborating exact-family screen.
The literature section correctly treats Taylor's field, generalized
Beltrami flows, and ABC flows as classical and makes no priority claim.

The licensed promotion is only

\[
 \boxed{\text{(S.342) is false for every }p>1.}
\]

The critical \(L_t^1\) estimate, hybrid terminal gate, crown route, Q.12,
Q.1, scale contraction, regularity, and the Millennium problem remain
open.
