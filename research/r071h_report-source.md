# R0.71H — Projective heat geometry isolates the angular source, while a smooth 2D3C family rejects only pointwise control

**Date:** 2026-08-25

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, localized projected Lamb vectors,
Littlewood--Paley transfer, time--frequency occupation, and directional
variation

**Status:** formal release source.  The report contains exact
classical-solution identities, one independently checked elementary
projective-curvature theorem on components of \(\{d>0\}\), an exact
global-smooth pointwise angular no-go, and a finite-Fourier cutoff saturation
calculation.  It contains no Leray-level weighted-BV estimate, no continuation
theorem, no singularity construction, no novelty claim, and no
Millennium-problem claim.

## 1. Direct decision

R0.71G reduced the missing temporal estimate to the variation of the
normalized localized coefficient

\[
 a_{j,Q,\varepsilon}=
 \frac{(\langle F_{j},C_{j,Q}\rangle^+)^2}
 {Y(\|C_{j,Q}\|_2^2+\varepsilon)}.
 \tag{1.1}
\]

R0.71H asks whether the direction of \(C_{j,Q}\) has a non-circular
time-variation estimate strong enough to pay

\[
 \sum_{j,Q}K_j^{-2}\operatorname{Var}_t
 (a_{j,Q,\varepsilon})
 \tag{1.2}
\]

uniformly as \(\varepsilon\downarrow0\).  The present answer has five parts.

1. The normalized derivative is exact.  Radial growth of \(C\) cancels, but
   the complete Lamb acceleration, angular rotation, moving-cutoff term,
   viscous collar, normalization by \(Y\), and all denominator and partition
   faces remain.
2. The heat part has a useful projective geometry.  If
   \(C_t=\nu\Delta C+G\) and \(E=C/\|C\|_2\), then the square angular speed
   is paid by a Rayleigh-quotient drop plus the single positive source ratio

   \[
    \frac{\|P_{E^\perp}G\|_2^2}{\|C\|_2^2}.
    \tag{1.3}
   \]

   This is an exact identity, not an estimate from the Leray energy budget.
3. The clean projective identity is confined to connected components of
   \(\{d>0\}\).  Replacing \(d\) by \(d+\varepsilon\) does not preserve it:
   the soft identity contains \(+\nu r_\varepsilon m_t\), its orthogonal
   form contains \(+\nu m_t r\), and full soft speed adds
   \(m_t^2/(4m)\).  For the linear crossing \(C(t)=(t,0)\), the isolated
   soft source has exact integral \(3\pi/(8\sqrt\varepsilon)\), so it has no
   uniform \(\varepsilon\downarrow0\) bound.
4. A fixed-energy, global-smooth 2D3C family proves that no bound of the form

   \[
    \frac{\|P_{E^\perp}C_t\|_2}{\|C\|_2}
    \le F(\|u_0\|_2^2,\nu)
    \tag{1.4}
   \]

   can hold uniformly over shells and times.  This is an exact no-go for
   unweighted instantaneous angular speed.  On the same family, accumulated
   turning and the \(K^{-2}\)-weighted variation vanish on fixed viscous-time
   windows.  The calculation therefore does not reject the target integrated
   budget (1.2).
5. A matched nonconstant cutoff makes the projective source budget converge
   to a finite positive constant even though the actual direction becomes
   stationary in the heat limit.  The projected source cancels the viscous
   projective curvature.  Estimating those two pieces separately loses this
   exact cancellation.

The route is not closed by the present calculation.  It is narrowed.  A
successful next estimate must control the joint projective evolution and the
Lamb-acceleration, \(Y_t/Y\), and face terms after the full shell and cell
sums.  Replacing any of them by a Serrin/Besov condition,
Cheskidov--Dai occupation hypothesis, a denominator lower bound, or the
desired weighted-BV sum would make the conclusion conditional rather than
derive it from the standard NSE budget.

## 2. Setup and scope

Work first on the periodic torus with normalized Haar measure.  Let \(u\) be
a zero-mean classical solution on a compact interval \(I\):

\[
 \partial_tu+u\cdot\nabla u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0,
 \qquad \omega=\nabla\times u.
 \tag{2.1}
\]

The identities below require enough smoothness to differentiate every
displayed quantity.  For example,

\[
 u\in C(I;H^5)\cap C^1(I;H^3)
 \tag{2.2}
\]

is more than sufficient.  No minimal regularity statement is made.  At the
Leray--Hopf level, finite-shell and space--time regularization would be needed
before passing to a limit, and the required uniform estimates are precisely
part of the open gap.

Set

\[
 L=\mathbb P(u\times\omega)
  =\partial_tu-\nu\Delta u
  =-\mathbb P((u\cdot\nabla)u).
 \tag{2.3}
\]

For a real-even multiplier \(T_j\), heat height \(s\ge0\), and

\[
 A=A_{j,s}=e^{s\Delta}T_j,
 \tag{2.4}
\]

write

\[
 W=A\omega,\qquad F=AL.
 \tag{2.5}
\]

Let \(\chi=\chi_{j,Q}(t,x)\in C_t^1C_x^\infty\), \(0\le\chi\le1\), and
define

\[
 C=\nabla\times(\chi W),\qquad
 B=\langle F,C\rangle,qquad
 d=\|C\|_2^2,qquad
 Y=\|\omega\|_2^2.
 \tag{2.6}
\]

All formulas are first one-shell, one-cell, and one-heat-height statements.
The sums over \(j,Q\), the \(\varepsilon\downarrow0\) limit, and any
partition refresh are separate steps.

Every quotient involving \(Y\) is asserted only on time intervals where
\(Y(t)>0\).  This excludes the trivial zero solution and avoids silently
dividing by zero; no lower bound for \(Y\) is assumed.

## 3. Complete all-shell time ledger

Let \(S_k=T_k^*T_k\) be a tight shell resolution and write

\[
 u_k=S_ku,qquad L_k=S_kL,qquad \omega_k=S_k\omega.
 \tag{3.1}
\]

For every ordered pair \((k,\ell)\), define

\[
 \begin{aligned}
 \mathfrak H_{k\ell}:={}&
 -A\mathbb P((L_k\cdot\nabla)u_\ell)
 -A\mathbb P((u_k\cdot\nabla)L_\ell)\\
 &+2\nu\sum_mA\mathbb P
 ((\partial_m u_k\cdot\nabla)\partial_m u_\ell),\\
 \mathfrak G_{k\ell}:={}&A\bigl(
 (\omega_k\cdot\nabla)u_\ell
 -(u_k\cdot\nabla)\omega_\ell\bigr).
 \end{aligned}
 \tag{3.2}
\]

Finite truncation followed by the smooth limit gives

\[
 \boxed{
 F_t=\nu\Delta F+\sum_{k,\ell}\mathfrak H_{k\ell},
 \qquad
 \nabla\times F=\sum_{k,\ell}\mathfrak G_{k\ell}.}
 \tag{3.3}
\]

The ordered sums retain low--high, high--low, comparable, and
high--high-to-low transfer.  Restricting them to \(k,\ell\simeq j\) would be
an additional theorem, not an algebraic simplification.

For a mollified transport velocity \(V_r\), set

\[
 R=(\partial_t+V_r\cdot\nabla)\chi,
 \qquad
 \mathcal K_\chi W
 =2\sum_m(\partial_m\chi)\partial_mW+(\Delta\chi)W.
 \tag{3.4}
\]

Since \(\chi_t=R-V_r\cdot\nabla\chi\), the exact Eulerian identity is

\[
 \boxed{
 \begin{aligned}
 C_t={}&\nu\Delta C
 +\nabla\times\left(\chi\sum_{k,\ell}\mathfrak G_{k\ell}\right)\\
 &+\nabla\times\bigl((R-V_r\cdot\nabla\chi)W\bigr)
 -\nu\nabla\times(\mathcal K_\chi W).
 \end{aligned}}
 \tag{3.5}
\]

It is convenient to collect the non-heat part as

\[
 C_t=\nu\Delta C+G,
 \tag{3.6}
\]

where

\[
 \begin{aligned}
 G={}&\nabla\times\left(\chi\sum_{k,\ell}\mathfrak G_{k\ell}\right)\\
 &+\nabla\times\bigl((R-V_r\cdot\nabla\chi)W\bigr)
 -\nu\nabla\times(\mathcal K_\chi W).
 \end{aligned}
 \tag{3.7}
\]

The second line contains the Eulerian movement and residual.  Even if
\(R=0\), a flow-transported cutoff has
\(\chi_t=-V_r\cdot\nabla\chi\).  The last term is the viscous collar.  Both
remain in an Eulerian calculation.

## 4. Exact normalized, epsilon, and time-face identities

### 4.1 Unit direction on \(d>0\)

On a connected component \(J\subset\{t:d(t)>0\}\), put

\[
 \rho=\sqrt d,qquad E=C/\rho,qquad
 P=I-E\otimes E,qquad
 \beta=\langle F,E\rangle,
 \tag{4.1}
\]

and

\[
 q=(\beta^+)^2,qquad a=q/Y.
 \tag{4.2}
\]

Differentiation gives

\[
 \boxed{E_t=\rho^{-1}PC_t,}
 \tag{4.3}
\]

\[
 \boxed{
 \beta_t=\langle F_t,E\rangle
 +\rho^{-1}\langle PF,C_t\rangle.}
 \tag{4.4}
\]

Equation (4.4) is the exact radial cancellation.  Replacing \(C_t\) by
\(C_t+\alpha C\) leaves its second term unchanged.  Substitution of
(3.3)--(3.5) gives the complete source ledger

\[
 \begin{aligned}
 \beta_t={}&\nu\langle\Delta F,E\rangle
 +\sum_{k,\ell}\langle\mathfrak H_{k\ell},E\rangle\\
 &+\frac{\nu}{\rho}\langle PF,\Delta C\rangle
 +\frac1\rho\sum_{k,\ell}
 \langle PF,\nabla\times(\chi\mathfrak G_{k\ell})\rangle\\
 &+\frac1\rho\langle PF,
 \nabla\times((R-V_r\cdot\nabla\chi)W)\rangle\\
 &-\frac\nu\rho\langle PF,
 \nabla\times(\mathcal K_\chi W)\rangle.
 \end{aligned}
 \tag{4.5}
\]

The function \(x\mapsto(x^+)^2\) is \(C^1\), so a crossing of
\(\beta=0\) creates no derivative atom.  Almost everywhere on \(J\),

\[
 q_t=2\beta^+\beta_t,
 \qquad
 \boxed{
 a_t=\frac{2\beta^+}{Y}\beta_t-a\frac{Y_t}{Y},}
 \tag{4.6}
\]

where

\[
 Y_t=2\langle\omega,\nabla\times L\rangle
 -2\nu\|\nabla\omega\|_2^2.
 \tag{4.7}
\]

The last term in (4.6) is independent of the radial cancellation.  Absolute
variation asks for \(|Y_t|/Y\), while a one-sided estimate still sees the
unfavorable part of \(-Y_t/Y\).

### 4.2 Global epsilon regularization

For \(\varepsilon>0\), define

\[
 \rho_\varepsilon=(d+\varepsilon)^{1/2},
 \quad E_\varepsilon=C/\rho_\varepsilon,
 \quad \beta_\varepsilon=B/\rho_\varepsilon,
 \quad q_\varepsilon=(\beta_\varepsilon^+)^2,
 \quad a_\varepsilon=q_\varepsilon/Y,
 \tag{4.8}
\]

and

\[
 P_\varepsilon=I-\frac{C\otimes C}{d+\varepsilon}.
 \tag{4.9}
\]

The operator \(P_\varepsilon\) is positive and self-adjoint, but not an
orthogonal projection.  Its radial eigenvalue is
\(\varepsilon/(d+\varepsilon)\).  Globally in time,

\[
 \boxed{(E_\varepsilon)_t
 =\rho_\varepsilon^{-1}P_\varepsilon C_t,}
 \tag{4.10}
\]

\[
 \boxed{
 (\beta_\varepsilon)_t
 =\langle F_t,E_\varepsilon\rangle
 +\rho_\varepsilon^{-1}\langle F,P_\varepsilon C_t\rangle,}
 \tag{4.11}
\]

\[
 \boxed{
 (a_\varepsilon)_t
 =\frac{2\beta_\varepsilon^+}{Y}
 \left[
 \langle F_t,E_\varepsilon\rangle
 +\rho_\varepsilon^{-1}\langle F,P_\varepsilon C_t\rangle
 \right]
 -a_\varepsilon\frac{Y_t}{Y}.}
 \tag{4.12}
\]

On \(d>0\), let

\[
 \sigma_\varepsilon=\frac{d}{d+\varepsilon}.
 \tag{4.13}
\]

Then

\[
 E_\varepsilon=\sqrt{\sigma_\varepsilon}E,
 \quad
 \beta_\varepsilon=\sqrt{\sigma_\varepsilon}\beta,
 \quad
 a_\varepsilon=\sigma_\varepsilon a,
 \tag{4.14}
\]

and the exact derivative splits as

\[
 \boxed{
 (a_\varepsilon)_t
 =\sigma_\varepsilon a_t
 +(\sigma_\varepsilon)_t a,}
 \qquad
 (\sigma_\varepsilon)_t
 =\frac{\varepsilon d_t}{(d+\varepsilon)^2}.
 \tag{4.15}
\]

The first term is the source/angular ledger.  The second is the restored
radial denominator term.  It tends to zero at every fixed point with \(d>0\)
but need not be uniformly integrable near \(d=0\).

### 4.3 Denominator and partition faces

Fix the observation interval \(I=[T_-,T_+]\), let
\(J_m=(\alpha_m,\beta_m)\) be the connected components of
\(\{d>0\}\cap(T_-,T_+)\), and extend \(a\) by zero on \(\{d=0\}\).
When the one-sided traces are finite, the safe quantity for a
uniform-\(\varepsilon\) absolute-variation limit on \(I\) is

\[
 \boxed{
 \operatorname{TV}_{\rm face,I}(a)
 =\sum_m\int_{J_m}|a_t|\,dt
 +\sum_{\alpha_m>T_-}a(\alpha_m+)
 +\sum_{\beta_m<T_+}a(\beta_m-).}
 \tag{4.16}
\]

Thus an outer endpoint of the observation interval is not charged.  If one
instead zero-extends the entire observation to the real line, the two outer
faces must be added.  If a required one-sided trace does not exist, the face
term is understood through the corresponding limsup; an infinite limsup
makes the ledger infinite rather than allowing the face to be discarded.

If \(d\) touches zero at one instant while both one-sided values of \(a\)
equal \(A>0\), the distributional net jump is zero, but
\(a_\varepsilon\) falls and rises, contributing \(2A\) to limiting
variation.  Algebraically cancelling coincident left and right faces is
therefore too weak for the absolute-BV ledger.

If the spatial partition is refreshed at times \(s_n\), the additional
atoms are

\[
 \sum_{n,Q}
 \bigl(a_Q(s_n+)-a_Q(s_n-)\bigr)\delta_{s_n}.
 \tag{4.17}
\]

Linear reconstruction of \(B_Q\) cannot cancel these atoms because
\(B\mapsto(B^+)^2/d\) is nonlinear.

## 5. Projective-curvature theorem

The following elementary Hilbert-space identity is the positive result of
this section.  It is stated here as a local theorem for the present
calculation, not as a novelty claim.

### Theorem 5.1 — Projective heat curvature with forcing

Let \(A_0\) be a fixed self-adjoint nonnegative operator on a real Hilbert
space.  Let \(C\in C^1(J;D(A_0))\) in the graph norm, suppose \(C(t)\ne0\)
on \(J\), and assume

\[
 C_t=-\nu A_0C+G.
 \tag{5.1}
\]

Set

\[
 \rho=\|C\|_2,qquad E=C/\rho,qquad
 r=\langle A_0E,E\rangle,
 \tag{5.2}
\]

\[
 X=P_{E^\perp}A_0E,qquad
 H=\rho^{-1}P_{E^\perp}G.
 \tag{5.3}
\]

For the present choice \(A_0=-\Delta\), this Rayleigh quotient is
\(r=\|\nabla E\|_2^2\).  Then, pointwise on \(J\),

\[
 \boxed{E_t=-\nu X+H,}
 \tag{5.4}
\]

and

\[
 \boxed{
 \|E_t\|_2^2
 +\nu^2\|P_{E^\perp}A_0E\|_2^2
 =-\nu r_t
 +\frac{\|P_{E^\perp}G\|_2^2}{\|C\|_2^2}.}
 \tag{5.5}
\]

Consequently, for \([t_0,t_1]\Subset J\),

\[
 \boxed{
 \begin{aligned}
 &\int_{t_0}^{t_1}\|E_t\|_2^2\,dt
 +\nu^2\int_{t_0}^{t_1}
 \|P_{E^\perp}A_0E\|_2^2\,dt\\
 &\qquad=\nu[r(t_0)-r(t_1)]
 +\int_{t_0}^{t_1}
 \frac{\|P_{E^\perp}G\|_2^2}{\|C\|_2^2}\,dt.
 \end{aligned}}
 \tag{5.6}
\]

#### Proof

The scalar \(\rho(t)\) commutes with \(A_0\).  Projecting (5.1) onto the
tangent space at \(E\) gives

\[
 E_t=\rho^{-1}P_{E^\perp}C_t
 =-\nu P_{E^\perp}A_0E
 +\rho^{-1}P_{E^\perp}G
 =-\nu X+H.
 \tag{5.7}
\]

Since \(E_t\perp E\), differentiation of the Rayleigh quotient gives

\[
 \begin{aligned}
 r_t
 &=2\langle A_0E,E_t\rangle
 =2\langle X,-\nu X+H\rangle\\
 &=-2\nu\|X\|_2^2+2\langle X,H\rangle.
 \end{aligned}
 \tag{5.8}
\]

On the other hand,

\[
 \|E_t\|_2^2
 =\nu^2\|X\|_2^2
 -2\nu\langle X,H\rangle
 +\|H\|_2^2.
 \tag{5.9}
\]

Adding \(\nu^2\|X\|_2^2\) to (5.9) and using (5.8) proves (5.5).
Integration proves (5.6). \(\square\)

For unforced heat flow, \(G=0\).  Then \(r\) is nonincreasing and its drop
pays both square angular speed and spectral projective curvature.  In the
localized NSE calculation, all deviation from this monotonicity is placed in

\[
 \mathfrak S_{j,Q}(J)
 =\int_J
 \frac{\|P_{E^\perp}G\|_2^2}{d}\,dt.
 \tag{5.10}
\]

This isolation is exact, but it does not bound \(\mathfrak S_{j,Q}\).

### 5.2 Independent audit and the soft-denominator defect

An independent Hilbert-space and Fourier audit checked (5.4)--(5.6).  A
forced three-dimensional finite model gave pointwise residual below
\(2\times10^{-16}\), and a four-eigenmode pure-heat calculation reduced the
identity to the spectral-variance formula

\[
 r_t=-2\nu\operatorname{Var}_p(\mu),
 \qquad
 \|E_t\|_2^2=\nu^2\operatorname{Var}_p(\mu).
 \tag{5.11}
\]

These are finite checks of the algebra, not a PDE estimate.  The theorem
remains restricted to each connected component of \(\{d>0\}\).  Its
integrated form is automatic only on compact subintervals of such a
component; approaching a zero face requires the limits and face terms from
Section 4.

In particular, the clean theorem does **not** extend by replacing \(d\) with
\(d+\varepsilon\).  Define

\[
 R_\varepsilon=(d+\varepsilon)^{1/2},
 \qquad Z=C/R_\varepsilon,
 \qquad m=\|Z\|_2^2=\frac d{d+\varepsilon},
 \tag{5.12}
\]

\[
 Q=I-Z\otimes Z,
 \quad X_\varepsilon=QA_0Z,
 \quad H_\varepsilon=Q(G/R_\varepsilon),
 \quad r_\varepsilon=\langle A_0Z,Z\rangle.
 \tag{5.13}
\]

Here \(Z\) is not a unit vector and \(Q\) is not an orthogonal projection.
The exact soft identity is

\[
 \boxed{
 \|Z_t\|_2^2+\nu^2\|X_\varepsilon\|_2^2
 =-\nu(r_\varepsilon)_t+\|H_\varepsilon\|_2^2
 +\nu r_\varepsilon m_t,}
 \tag{5.14}
\]

where

\[
 m_t=\frac{\varepsilon d_t}{(d+\varepsilon)^2}.
 \tag{5.15}
\]

The added term has no fixed sign.  On \(d>0\), an orthogonal decomposition
with \(e=C/\sqrt d\), \(P_e=I-e\otimes e\), and
\(r=\langle A_0e,e\rangle\) gives

\[
 \boxed{
 \|P_eZ_t\|_2^2+\nu^2\|P_eA_0Z\|_2^2
 =-\nu(r_\varepsilon)_t
 +\frac{\|P_eG\|_2^2}{d+\varepsilon}
 +\nu m_t r.}
 \tag{5.16}
\]

If the full soft speed \(\|Z_t\|_2^2\) is used, the additional radial term
is

\[
 \frac{m_t^2}{4m}.
 \tag{5.17}
\]

The lack of a uniform soft-source estimate is already visible in a linear
crossing.  Take a finite-dimensional Hilbert space, \(A_0=0\),
\(C(t)=(t,0)\), and \(G=(1,0)\).  Then

\[
 \|H_\varepsilon(t)\|^2
 =\frac{\varepsilon^2}{(t^2+\varepsilon)^3},
 \tag{5.18}
\]

and exactly

\[
 \boxed{
 \int_{\mathbb R}\|H_\varepsilon(t)\|^2dt
 =\frac{3\pi}{8\sqrt\varepsilon}.}
 \tag{5.19}
\]

Thus the algebraically global soft identity has no source bound uniform in
\(\varepsilon\downarrow0\), even for this elementary crossing.  The valid
\(q_\varepsilon\) derivative ledger (4.10)--(4.15) and the clean unit-sphere
projective identity (5.5) must remain separate.  Neither one removes the
zero-face burden of the other.

## 6. What the projective identity gives to the signed quotient

The normalized work satisfies

\[
 \beta_t=\langle F_t,E\rangle
 +\langle P_{E^\perp}F,E_t\rangle.
 \tag{6.1}
\]

The pointwise inequality

\[
 2\beta^+\|P_{E^\perp}F\|_2\le\|F\|_2^2
 \tag{6.2}
\]

therefore gives

\[
 |q_t|
 \le2\sqrt q\,\|F_t\|_2
 +\|F\|_2^2\|E_t\|_2,
 \tag{6.3}
\]

and

\[
 |a_t|
 \le2\sqrt{\frac qY}\frac{\|F_t\|_2}{\sqrt Y}
 +\frac{\|F\|_2^2}{Y}\|E_t\|_2
 +a\left|\frac{Y_t}{Y}\right|.
 \tag{6.4}
\]

Suppose an event interval \(I\Subset J\) has the critical residence length

\[
 |I|\le\frac{C_{\rm res}}{\nu K^2}.
 \tag{6.5}
\]

Then Theorem 5.1 and Cauchy--Schwarz imply

\[
 \int_I\|E_t\|_2\,dt
 \le
 \left\{
 \frac{C_{\rm res}}{\nu K^2}
 \left[
 \nu r(t_-)
 +\int_I\frac{\|P_{E^\perp}G\|_2^2}{d}\,dt
 \right]
 \right\}^{1/2}.
 \tag{6.6}
\]

A dimensionless arc-length estimate would follow from both

\[
 K^{-2}r(t_-)=O(1),
 \qquad
 (\nu K^2)^{-1}
 \int_I\frac{\|P_{E^\perp}G\|_2^2}{d}\,dt=O(1).
 \tag{6.7}
\]

Neither condition follows automatically after localization.  Moreover,
(6.6) alone does not pay the amplitude-weighted factor in (6.4), the
\(F_t\) term, or \(Y_t/Y\), and it says nothing about denominator and refresh
faces.

Under the covariant whole-space NSE scaling,

\[
 u_\lambda(t,x)=\lambda u(\lambda^2t,\lambda x),
 \qquad K_\lambda=\lambda K,
 \tag{6.8}
\]

the three quantities

\[
 K^{-2}\int\|E_t\|_2^2dt,
 \qquad
 K^{-2}\int\frac{\|P_{E^\perp}G\|_2^2}{d}dt,
 \qquad
 \int\|E_t\|_2dt
 \tag{6.9}
\]

are scale invariant.  Scaling is therefore compatible with the desired
critical projective budget.  It neither proves nor disproves it.

## 7. Nominal damping and the two-frequency-power gap

For an arbitrary positive reference frequency \(K^2\), add and subtract the
corresponding heat rate.  Because \(PC=0\), equation (4.4) becomes

\[
 \boxed{\beta_t+\nu K^2\beta=\mathcal R,}
 \tag{7.1}
\]

where

\[
 \begin{aligned}
 \mathcal R={}&
 \nu\langle(\Delta+K^2)F,E\rangle
 +\sum_{k,\ell}\langle\mathfrak H_{k\ell},E\rangle\\
 &+\frac\nu\rho\langle PF,(\Delta+K^2)C\rangle\\
 &+\frac1\rho\sum_{k,\ell}
 \langle PF,\nabla\times(\chi\mathfrak G_{k\ell})\rangle\\
 &+\frac1\rho\langle PF,
 \nabla\times((R-V_r\cdot\nabla\chi)W)\rangle\\
 &-\frac\nu\rho\langle PF,
 \nabla\times(\mathcal K_\chi W)\rangle.
 \end{aligned}
 \tag{7.2}
\]

Thus

\[
 q_t+2\nu K^2q=2\beta^+\mathcal R,
 \tag{7.3}
\]

\[
 \boxed{
 a_t+2\nu K^2a
 =\frac{2\beta^+}{Y}\mathcal R-a\frac{Y_t}{Y}.}
 \tag{7.4}
\]

The displayed \(-2\nu K^2a\) is nominal damping, not a proved coercive
term.  A standard annulus has fixed relative width, so
\((\Delta+K^2)F=O(K^2F)\), not \(o(K^2F)\).  A matched cutoff broadens
\(C\), and \(P(\Delta+K^2)C/\rho\) is also an angular term of order
\(K^2\).  The remaining shell, movement, and collar terms have no universal
sign.

For a scale audit, let

\[
 f=\|F\|_2,qquad f_\perp=\|PF\|_2,
 \tag{7.5}
\]

and define

\[
 \kappa_F=\frac{|\langle F_t,E\rangle|}{\nu K^2f},
 \quad
 \kappa_C=\frac{\|PC_t\|_2}{\nu K^2\rho},
 \quad
 \rho_F=\frac{f_\perp}{f},
 \quad
 \Gamma=\kappa_F+\rho_F\kappa_C.
 \tag{7.6}
\]

These ratios are first defined when \(f>0\).  The product appearing below
has the equivalent nonsingular definition

\[
 f^2\Gamma^2:=\frac1{\nu^2K^4}
 \left(
 |\langle F_t,E\rangle|
 +\frac{f_\perp}{\rho}\|PC_t\|_2
 \right)^2.
 \tag{7.6a}
\]

If \(f=0\), then \(F=0\), \(\beta=q=a=0\), and the exact positive-part
formula gives \(a_t=0\) at that time; (7.7) is therefore trivial with the
extension (7.6a).  For every \(\delta>0\), (4.4)--(4.6) give

\[
 \boxed{
 K^{-2}|a_t|
 \le\nu\delta a
 +\frac\nu\delta\frac{f^2}{Y}\Gamma^2
 +K^{-2}a\frac{|Y_t|}{Y}.}
 \tag{7.7}
\]

The prior heat-bulk endpoint controls only the scale

\[
 K^{-2}\frac{f^2}{Y}
 \tag{7.8}
\]

after the required sums.  An \(O(1)\) dimensionless curvature rate in (7.7)
leaves \(f^2/Y\).  There is therefore an exact two-frequency-power gap
between this direct Young estimate and (7.8).  Schematically, the direct
route would need two powers of curvature depletion after summation, such as

\[
 \Gamma^2\lesssim K^{-2}.
 \tag{7.9}
\]

Scaling, annular localization, and radial cancellation do not supply
(7.9).  In coarse form, the acceleration row asks for

\[
 K^{-4}\frac{\|F_t\|_2^2}{Y},
 \tag{7.10}
\]

up to viscosity constants.  The Leray bounds

\[
 u\in L_t^\infty L_x^2\cap L_t^2H_x^1
 \tag{7.11}
\]

provide neither (7.10), a positive lower bound for \(d\), nor absolute
logarithmic variation of \(Y\).

## 8. Exact global-smooth 2D3C pointwise angular no-go

Use normalized Haar measure on \(\mathbb T^3\).  For \(a>0\) and integer
\(K\ge1\), take

\[
 u_0(x)=\left(
 0,-2aK\cos(Kx_1),
 -2aK\sin(Kx_1+Kx_2)-2aK\cos(Kx_2)
 \right).
 \tag{8.1}
\]

The horizontal shear solves the heat equation, and the third component
solves a passive advection--diffusion equation.  This is therefore an exact
global-smooth 2D3C NSE solution for every \(a,K,\nu>0\).

Let \(T_K\) retain the four modes with \(|k|=K\), take \(\chi\equiv1\), and
evaluate at the true initial time.  Exact Fourier algebra gives

\[
 \|u_0\|_2^2=6a^2K^2,
 \quad B=2a^3K^6,
 \quad d=4a^2K^6,
 \quad q=a^4K^6,
 \quad Y=8a^2K^4.
 \tag{8.2}
\]

The denominator is strictly positive.  Further,

\[
 \|T_K\partial_tL\|_2^2
 =2a^4(3\nu+2a)^2K^{10},
 \tag{8.3}
\]

and

\[
 \|P_{E^\perp}C_t\|_2^2=a^4K^{10}.
 \tag{8.4}
\]

Hence the instantaneous unit-direction speed is

\[
 \boxed{
 \Omega_K(0):=
 \frac{\|P_{E^\perp}C_t\|_2}{\|C\|_2}
 =\frac12aK^2.}
 \tag{8.5}
\]

### Theorem 8.1 — No energy-only pointwise angular bound

Fix \(\nu>0\) and \(\mathcal E>0\).  There is no finite function
\(F(\mathcal E,\nu)\) such that

\[
 \Omega_{T_K}(t)\le F(\mathcal E,\nu)
 \tag{8.6}
\]

for every integer \(K\), every smooth NSE solution with
\(\|u_0\|_2^2=\mathcal E\), and every time at which the denominator of the
explicit low-sphere multiplier \(T_K\) specified above is positive.

#### Proof

Put

\[
 U=\sqrt{\mathcal E/6},\qquad a_K=U/K.
 \tag{8.7}
\]

Then every member of (8.1) is global and smooth,

\[
 \|u_0^{(K)}\|_2^2=\mathcal E,
 \qquad d_K(0)=4U^2K^4>0,
 \tag{8.8}
\]

while

\[
 \Omega_K(0)=\frac12UK\longrightarrow\infty.
 \tag{8.9}
\]

Choosing \(K>2F(\mathcal E,\nu)/U\) contradicts (8.6). \(\square\)

The theorem applies to the declared low-sphere multipliers and therefore
rejects an energy-only estimate that is required to cover them.  It does not,
without a separate multiplier comparison, assert the same witness for every
preassigned smooth matched frame or cell partition.

This theorem is deliberately narrow.  To state the time-integrated boundary,
use the exact sideband chain of the global 2D3C solution.  In rescaled time,
let \(c_m(\theta;\mu)\) solve

\[
 c_m'=-(m^2+1)c_m
 +i\mu e^{-\theta}(c_{m-1}+c_{m+1}),
 \quad c_0(0)=-1,\quad c_1(0)=i,
 \tag{8.9a}
\]

with all other initial coefficients zero, and define

\[
 \begin{aligned}
 H_\mu&=\operatorname{Re}\!\left[
 \overline{c_0}\,i e^{-\theta}(c_{-1}+c_1)\right],\\
 G_\mu&=|c_0|^2+e^{-2\theta},\\
 \mathcal E_\mu&=e^{-2\theta}
 +\sum_m(m^2+1)|c_m|^2,\\
 h_\mu&=\frac{(H_\mu^+)^2}{G_\mu\mathcal E_\mu}.
 \end{aligned}
 \tag{8.9b}
\]

With
\(\theta=\nu K^2t\) and \(\mu_K=U/(\nu K)\), the exact sideband dynamics
give, on every fixed \(0\le\theta\le M\),

\[
 A_K(t)=\frac{q_K(t)}{Y(t)}
 =U^2h_{\mu_K}(\theta),
 \tag{8.10}
\]

The denominator is bounded away from zero on this fixed window.  Duhamel's
formula for (8.9a), and the differentiated equation, give convergence
uniformly in \(C^1([0,M])\): \(h_{\mu}\to h_0\), where

\[
 h_0(\theta)=\frac{e^{-4\theta}}{4(1+e^{-2\theta})}.
 \tag{8.11}
\]

The limiting profile is strictly decreasing and the denominator remains
positive.  Therefore

\[
 K^{-2}\operatorname{TV}_{[0,M/(\nu K^2)]}(A_K)
 \longrightarrow0.
 \tag{8.12}
\]

On the same interval,

\[
 \int_0^{M/(\nu K^2)}\Omega_K(t)\,dt=O(K^{-1}).
 \tag{8.13}
\]

Here the normalized low-shell direction satisfies
\(\|\partial_\theta E_K\|_{L^\infty_\theta L_x^2}=O(\mu_K)\), again by
the differentiated sideband equation and the uniform denominator bound.
Thus (8.12)--(8.13) are uniform fixed-window asymptotics, not consequences
of the initial-time symbolic audit alone.

The scalar angular contribution to \(A_K'\),

\[
 \mathcal A_{\rm ang}
 =\frac{2\beta^+}{Y}
 \langle P_{E^\perp}F,E_t\rangle,
 \tag{8.14}
\]

also diverges instantaneously: at \(t=0\),

\[
 \mathcal A_{\rm ang}(0)=\frac18a^3K^4
 =\frac18U^3K.
 \tag{8.15}
\]

Its accumulated contribution on a viscous-time interval is only
\(O(K^{-1})\).  Thus neither the bare speed (8.5) nor the instantaneous
scalar factor (8.15) is the integrated weighted-BV target.

## 9. A nonconstant cutoff saturates the source ratio and exposes cancellation

At \(t=0\), in the rescaled variables

\[
 X=Kx_1,qquad Y=Kx_2,qquad Z=Kx_3,
 \tag{9.1}
\]

the retained vorticity is proportional to

\[
 w(X,Y,Z)=(2\sin Y,0,2\sin X).
 \tag{9.2}
\]

Take the nonnegative nonconstant cutoff

\[
 \chi_\delta(Z)=\frac{1+\delta\cos Z}{2},
 \qquad0<\delta\le1,
 \tag{9.3}
\]

and set

\[
 \mathcal C_\delta
 =\nabla_{X,Y,Z}\times(\chi_\delta w).
 \tag{9.4}
\]

Exact Fourier orthogonality gives

\[
 D_\delta:=\|\mathcal C_\delta\|_2^2
 =\frac{3\delta^2+4}{4},
 \tag{9.5}
\]

\[
 R_\delta:=
 \frac{\|\nabla\mathcal C_\delta\|_2^2}
 {\|\mathcal C_\delta\|_2^2}
 =\frac{2(3\delta^2+2)}{3\delta^2+4},
 \tag{9.6}
\]

and

\[
 J_\delta:=
 \frac{
 \|P_{\mathcal C_\delta^\perp}
 (\Delta+1)\mathcal C_\delta\|_2^2}
 {\|\mathcal C_\delta\|_2^2}
 =\frac{12\delta^2}{(3\delta^2+4)^2}.
 \tag{9.7}
\]

For every fixed \(\delta>0\),

\[
 D_\delta>0,qquad1\le R_\delta\le10/7,
 \qquad J_\delta>0.
 \tag{9.8}
\]

Use again the fixed-energy sequence \(a_K=U/K\).  On a fixed rescaled
interval \(0\le\theta\le M\), the low-shell dynamics approach pure heat.
More precisely, after factoring out the scalar amplitude,
\(C_K\) converges in \(C^1_\theta L_x^2\), uniformly on the fixed window,
to \(e^{-\theta}\mathcal C_\delta\).  The denominator is then uniformly
positive.  After normalization, the limiting direction is stationary, and
the projected source satisfies, uniformly in \(L_x^2\),

\[
 \frac{P_{E^\perp}G}{\sqrt d}
 =\nu K^2
 P_{\mathcal C_\delta^\perp}
 (-\Delta-1)
 \frac{\mathcal C_\delta}{\sqrt{D_\delta}}
 +o(K^2).
 \tag{9.9}
\]

Define the scale-critical projective source budget

\[
 \mathcal P_K(I)
 =K^{-2}\int_I
 \frac{\|P_{E^\perp}G\|_2^2}{d}\,dt.
 \tag{9.10}
\]

Also set

\[
 r_K(t)=\langle-\Delta E_K(t),E_K(t)\rangle.
 \tag{9.10a}
\]

Then

\[
 K^{-2}r_K(0)\longrightarrow R_\delta,
 \tag{9.11}
\]

\[
 \boxed{
 \mathcal P_K([0,M/(\nu K^2)])
 \longrightarrow\nu M J_\delta,}
 \tag{9.12}
\]

while

\[
 \int_0^{M/(\nu K^2)}\|E_t\|_2\,dt=O(K^{-1}).
 \tag{9.13}
\]

The projected source in (9.9) cancels the viscous projective curvature in
(5.4).  The separate positive source ratio therefore saturates at a finite
constant even though the actual angular arc tends to zero.  This does not
disprove Theorem 5.1 or the target BV budget.  It shows that a triangle
inequality applied separately to the two terms in (5.4) can lose the leading
order cancellation.

For a fixed matched template

\[
 \chi_K(x)=\chi_0(K(x-x_Q)),
 \tag{9.14}
\]

phase translation of this finite-mode field also does not produce a small
denominator.  In rescaled coordinates, the phase ranges over a compact torus
and the relevant numerator and denominator are fixed quadratic forms.  If

\[
 w_\phi=(2\sin(Y+\phi_2),0,2\sin(X+\phi_1)),
 \tag{9.15}
\]

then \(\nabla\times(\chi_0w_\phi)=0\) cannot hold for a nonzero cutoff:
on an open set where \(\chi_0>0\), \(\sin(X+\phi_1)\ne0\), and
\(\cos(Y+\phi_2)\ne0\), one curl component forces
\(\partial_Y\chi_0=0\), while another forces
\(\chi_0\cos(Y+\phi_2)=0\), a contradiction.  Compactness then gives a
uniform positive denominator for this fixed family.

This finite-template statement does not cover increasing Fourier dimension,
degenerating cutoff templates, or an approach to a genuine denominator
kernel.

## 10. What is ruled out, and what remains open

### 10.1 Ruled out by exact calculations

1. There is no uniform pointwise bound for unweighted angular speed in terms
   of initial kinetic energy and viscosity alone, even among global-smooth
   solutions with strictly positive localized denominator.
2. The displayed \(-\nu K^2\beta\) in the nominal decomposition does not by
   itself prove damping.  The remainder contains terms of the same nominal
   size and has no universal sign.
3. The positive projective source ratio is not identical to actual angular
   turning.  A nonconstant cutoff can make the ratio saturate while the heat
   direction is stationary because of exact cancellation with viscous
   projective curvature.
4. Radial normalization does not remove \(F_t\), \(Y_t/Y\), epsilon
   denominator variation, internal zero faces, or partition-refresh faces.
### 10.2 Not ruled out

1. A joint time-integrated estimate exploiting cancellation between viscous
   projective curvature and the complete source \(G\).
2. A scale-critical bound for accumulated angular turning, the signed scalar
   angular contribution, or the full \(K^{-2}\)-weighted BV sum.
3. A nonlinear depletion mechanism that is invisible in the separate
   positive source ratio.
4. A theorem using additional information that is independently controlled
   below known continuation thresholds.
5. A counterexample to the full weighted-BV budget.  The present 2D3C family
   has vanishing weighted variation on fixed viscous windows and does not
   supply an unbounded shell sum.
6. A Leray-level passage for the classical identities.  No such passage is
   made here.

Accordingly, “the elementary estimate does not close” must not be rewritten
as “the estimate is impossible.”  The only impossibility theorem in this
report is Theorem 8.1, with its stated instantaneous scope.

## 11. Primary-source boundary

The literature check was deliberately bounded to primary papers and official
arXiv or journal pages.  It is not a systematic review and does not establish
originality, priority, or global nonexistence of related results.

| Primary source | Exact nearby result | Boundary relative to R0.71H |
|---|---|---|
| [Gibbon--Holm--Kerr--Roulstone, arXiv:nlin/0512034](https://arxiv.org/abs/nlin/0512034), [DOI](https://doi.org/10.1088/0951-7715/19/8/011) | For Euler material vorticity direction, \(D_t\widehat\omega=\chi\times\widehat\omega\); pressure-Hessian source curvature enters the quaternion Riccati system.  Their continuation condition uses \(\int\|\chi_p\|_\infty dt\). | Exact temporal direction precedent, but Euler, material, unlocalized, and conditional; no weighted BV or crossing control. |
| [Beirão da Veiga--Berselli](https://people.dm.unipi.it/beiraodaveiga/pdf/hbv-79.pdf), [DOI](https://doi.org/10.57262/die/1356060864) | Critical spatial vorticity-direction coherence and the weighted spatial quantity \(\int|\omega||\nabla\xi|^2\). | Spatial direction control does not supply temporal variation of the localized projected-Lamb direction. |
| [Vasseur, arXiv:0705.2446](https://arxiv.org/abs/0705.2446) | Regularity from \(\operatorname{div}(u/|u|)\in L_t^pL_x^q\), \(2/p+3/q\le1/2\), \(q\ge6\). | A spatial velocity-direction condition, not a shellwise time-BV estimate. |
| [Dascaliuc--Grujić, arXiv:1107.0058](https://arxiv.org/abs/1107.0058), [DOI](https://doi.org/10.1007/s00220-012-1595-8) | Critical \(1/2\)-Hölder vorticity-direction coherence plus Kraichnan-scale and terminal-modulation assumptions yields a local enstrophy-cascade estimate. | The temporal modulation is assumed; no angular crossing or projected-Lamb quotient. |
| [Cheskidov--Shvydkoy, arXiv:1102.1944](https://arxiv.org/abs/1102.1944), [DOI](https://doi.org/10.1007/s00021-014-0167-4) | Dynamic dissipation wavenumber; every Leray--Hopf solution has \(\Lambda\in L_t^1\), while stronger low-mode conditions imply regularity. | The unconditional mean gives only a \(K^{-1}\) occupation tail by Chebyshev and contains no directional variation. |
| [Cheskidov--Dai, arXiv:1507.06611](https://arxiv.org/abs/1507.06611) | Scale-critical amplitude-weighted time--frequency occupation condition \(\int\mathbf1_{\{q\le Q_r(t)\}}\|\Delta_q\omega\|_\infty dt\). | Closest occupation formula, but it is a regularity hypothesis, not a Leray-derived unweighted episode or BV bound. |
| [Cheskidov--Shvydkoy, arXiv:0708.3067](https://arxiv.org/abs/0708.3067), [DOI](https://doi.org/10.1007/s00205-009-0265-2) | Critical \(B^{-1}_{\infty,\infty}\) left-jump and shell-amplitude criteria. | Small jumps do not sum all jumps and do not control angular total variation. |
| [Bradshaw--Grujić, arXiv:1501.01043](https://arxiv.org/abs/1501.01043), [DOI](https://doi.org/10.1007/s00205-016-1069-9) | Dynamic frequency-window and critical Besov-amplitude criteria. | Controls amplitudes, not direction or zero-denominator faces. |
| [Gibbon--Doering, arXiv:math/0406146](https://arxiv.org/abs/math/0406146), [DOI](https://doi.org/10.1007/s00205-005-0382-5) | Reynolds-dependent widths for global higher-derivative bad and dangerous intervals. | A genuine event-width precedent, but not fixed-shell angular residence or crossing count. |
| [Łochowski, arXiv:1503.01746](https://arxiv.org/abs/1503.01746), [DOI](https://doi.org/10.4064/cm6583-3-2017) | Banach-indicatrix generalization: total or truncated variation equals the integrated crossing count. | Gives the exact BV--crossing interface but no PDE estimate producing BV. |
| [Cheskidov--Dai, arXiv:1510.00379](https://arxiv.org/abs/1510.00379), [DOI](https://doi.org/10.1017/PRM.2018.33) | Long-time mean determining wavenumber bounded by an intermittency-adjusted Kolmogorov scale. | Long-time attractor statistics do not control a terminal candidate-singular interval or angular variation. |

The bounded search found no theorem that derives (1.2), including its
epsilon and face terms, from the standard Leray budget.  This is a bounded
negative finding only.  A broader originality review would still require
expanded keywords, citation-network checks, MathSciNet/zbMATH, and expert
review.

## 12. Route verdict and next gate

R0.71H establishes an exact but limited separation.

1. Radial cancellation is complete on \(d>0\).
2. In the quotient ledger, epsilon regularization restores one radial
   denominator term whose limiting cost is a crossing/face budget.  A soft
   projective identity has the additional radial defects in
   (5.14)--(5.17), so it is not obtained by the substitution
   \(d\mapsto d+\varepsilon\).
3. Heat evolution has a projective dissipation identity, but the localized
   NSE source enters through a scale-critical positive ratio divided by the
   same potentially small denominator.
4. Standard direct estimates have a two-frequency-power gap relative to the
   available heat-bulk endpoint.
5. Energy-only pointwise angular control is false on an exact global-smooth
   family, while the corresponding integrated critical budget remains
   unrefuted.
6. A nonconstant matched cutoff exposes a leading-order cancellation that a
   separate source estimate would discard.

The next gate should therefore test the **joint** evolution rather than seek
a bound for \(\|P_{E^\perp}G\|^2/d\) in isolation.  A candidate estimate must
meet all of the following conditions:

\[
 \begin{aligned}
 &\text{retain every }(k,\ell)\text{ shell pair};\\
 &\text{retain cutoff movement and the viscous collar};\\
 &\text{use the cancellation between }-\nu P_{E^\perp}A_0E
   \text{ and }P_{E^\perp}G/\rho;\\
 &\text{control the }F_t\text{ and }Y_t/Y\text{ rows independently};\\
 &\text{remain uniform through }\varepsilon\downarrow0
   \text{ and pay every time face};\\
 &\text{sum over all shells and cells without assuming the target BV or a
 known continuation norm.}
 \end{aligned}
 \tag{12.1}
\]

The immediate technical question is whether an amplitude-weighted joint
projective identity can replace the separate estimate (6.4) and recover the
two missing frequency powers.  If every such attempt still requires a
Serrin/Besov norm, Cheskidov--Dai occupation, a denominator nondegeneracy
hypothesis, or the weighted-BV sum itself, then the temporal-residence route
should be recorded as conditional and stopped.  No stronger negative claim
is justified by the present evidence.

## 13. Reproduction and evidence map

The release separates symbolic production, independent checking, literature
scope, and figure generation.

- `research/r071h_exact_audit.py` reconstructs the declared low-sphere
  2D3C witness from exact Fourier convolution and checks the initial angular,
  scalar, scaling, and nonconstant-cutoff formulas.
- `research/r071h_independent_audit.py` uses only the Python standard library.
  It checks the unit projective identity on a forced finite-dimensional path,
  the pure Fourier-heat identity, both corrected soft-denominator forms, the
  linear crossing integral, and the critical scaling exponents.
- `research/certificates/r071h/` archives canonical JSON outputs, commands,
  environment metadata, claim boundaries, and SHA-256 hashes.
- `research/r071h_literature_audit.md` records the bounded primary-source
  search; `research/r071h_independent_audit.md` records the independent
  mathematical review.
- `figures/r071h-angular/fig-r071h-angular-curvature/` contains 391
  closed-form data rows, producer and independent validators, a manifest,
  caption, hashes, and PDF/SVG/600-dpi PNG exports.  It contains no DNS,
  fitting, or three-dimensional PDE time stepping.

The machine checks certify the finite algebra and displayed elementary
identities.  The fixed-window asymptotics in Sections 8--9 also use the exact
sideband equation and its Duhamel estimates, as stated there.  None of these
artifacts supplies the open Leray-level weighted-BV estimate.
