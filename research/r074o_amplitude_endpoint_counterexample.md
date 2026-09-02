# R0.74O — amplitude freedom refutes the scalar square-root-log endpoint

## Status and scope

This note proves that the universal scalar-payment estimate

\[
 \mathfrak C_R^\alpha
 \le C(P_R^\alpha)^{2/3}
 \sqrt{1+\log_+P_R^\alpha},
 \qquad \alpha\in\{M,F\},
\tag{0.1}
\]

is false.  Here \(P_R^\alpha\), the two local frames, and the positive
cumulative collar flux \(\mathfrak C_R^\alpha\) are exactly the frozen
R0.74E--H quantities.

The counterexample does not require a new flow geometry.  It uses the
amplitude freedom in the exact R0.74F--N passive-packet family.  The new
amplitude remains below the level at which the packet enlarges the complete
scalar payment beyond its background-shear scale, while the endpoint energy
and signed collar flux grow quadratically in that amplitude.

The main result is stronger than the failure of (0.1).  Define

\[
 q_*=\frac{8024}{11907}
 =\frac23+\frac{86}{11907}.
\tag{0.2}
\]

There is one sequence of smooth periodic mean-zero unforced global
solutions for which, in both frames,

\[
 \boxed{
 X_{R_j}^{\alpha,*}
 \asymp\mathfrak C_{R_j}^{\alpha,*}
 \asymp
 (P_{R_j}^{\alpha,*})^{q_*}
 (1+\log_+P_{R_j}^{\alpha,*})^{7/6}.}
\tag{0.3}
\]

Consequently every scalar majorant

\[
 \Phi(p)
 =o\!\left(p^{q_*}(1+\log_+p)^{7/6}\right)
 \qquad(p\to\infty)
\tag{0.4}
\]

fails as a universal upper bound for either \(X_R^\alpha\) or
\(\mathfrak C_R^\alpha\).

This result refutes one family of internally proposed scalar-payment
inequalities.  It constructs no singularity, proves no blow-up, and does not
exclude estimates with additional structural observables.  Novelty and
priority remain open.  **NOT CLAY.**

## 1. Exact family, constants, and the new amplitude

Retain the exact R0.74F--N constants

\[
 \rho=\frac1{320},
 \qquad
 c_\gamma=\frac8{3969},
 \qquad
 d_E=\frac{98}{29475},
\tag{1.1}
\]

and define

\[
 e_E:=d_E-c_\gamma
 =\frac{17018}{12998475},
\tag{1.2}
\]

\[
 m:=\rho-\frac32c_\gamma
 =\frac1{320}-\frac4{1323}
 =\frac{43}{423360}>0.
\tag{1.3}
\]

For the family index \(j\), put

\[
 L=L_j=\frac{63}{32}2^j,
 \qquad
 R=R_j=e^{-\rho L^2},
 \qquad
 \Gamma=\Gamma_j=e^{-c_\gamma L^2},
\tag{1.4}
\]

and retain the exact contrast amplitude \(B=B_j>0\), for which

\[
 \beta_j:=B_jR_j^2\longrightarrow\frac1{128}.
\tag{1.5}
\]

In particular, after increasing the base index once,

\[
 0<\beta_-\le \beta_j\le\beta_+<\infty
\tag{1.6}
\]

with constants independent of \(j\).

Let \(F=F_j\) be the paired passive field and let
\(\theta=\theta_j\) be the odd heat shear.  For every
\(\mathfrak a>0\),

\[
 u^{(\mathfrak a)}
 =(\mathfrak a F,B\theta,0),
 \qquad p^{(\mathfrak a)}=0
\tag{1.7}
\]

is an exact smooth periodic mean-zero unforced Navier--Stokes solution.
Indeed, the fields are independent of \(x_1\), the shear depends only on
\(x_3\), and the first component solves

\[
 \partial_tF+B\theta\,\partial_2F
 =\Delta_{23}F.
\tag{1.8}
\]

Thus multiplying \(F\) by a spatially constant amplitude preserves the
equation exactly.  The solution is supplied by periodic heat flow and is
smooth for the whole time range used here; no local-existence or unknown
three-dimensional continuation assertion is invoked.

Full inversion oddness and the even radial mollifier give

\[
 X_R(t)\equiv0,
 \qquad
 a_R(t)\equiv0,
 \qquad
 a_R'(t)\equiv0.
\tag{1.9}
\]

Hence Versions M and F coincide, their acceleration payments vanish
exactly, and the physical pressure is identically zero.

The normalized R0.74G--N packet amplitude is

\[
 \mathfrak a_0=B\Gamma^{-1/2}.
\tag{1.10}
\]

To avoid confusion with the fixed inherited geometric constant
\(\kappa=16\), define a new multiplier with a different symbol:

\[
 \boxed{
 \varkappa
 =L^{2/3}\exp\!\left(\frac m3L^2\right),}
\tag{1.11}
\]

and set

\[
 \boxed{
 \mathfrak a_*
 =\varkappa\mathfrak a_0
 =\varkappa B\Gamma^{-1/2}.}
\tag{1.12}
\]

All remaining constants are uniform in \(j\).  No simulation, DNS, DGX
calculation, or asymptotic numerical fit enters the proof.

## 2. Complete payment upper bound at the amplified amplitude

Write

\[
 P_*:=P_R^{M,*}=P_R^{F,*}.
\tag{2.1}
\]

The equality follows from (1.9).  We now rebuild every nonnegative row of
this common payment from the general-amplitude R0.74G inequalities.

### 2.1 Buffered local energy

The inherited general-\(\mathfrak a\) estimate is

\[
 \mathcal E_*
 \le C\left[
 B^2R^2+\mathfrak a_*^2R^2
 \left(e^{-d_EL^2}+e^{-c/R^2}\right)\right].
\tag{2.2}
\]

For the first packet term, divide by \(B^2R^2\) and use
(1.11)--(1.12):

\[
\begin{aligned}
 \varkappa^2\Gamma^{-1}e^{-d_EL^2}
 &=L^{4/3}
 \exp\!\left[
 -\left(e_E-\frac{2m}{3}\right)L^2\right].
\end{aligned}
\tag{2.3}
\]

The exact remaining reserve is

\[
 \boxed{
 e_E-\frac{2m}{3}
 =\frac{1171}{943200}>0.}
\tag{2.4}
\]

Thus the right side of (2.3) tends to zero.  The periodic-copy error is
even smaller:

\[
\begin{aligned}
 \varkappa^2\Gamma^{-1}e^{-c/R^2}
 =L^{4/3}\exp\!\left[
 \left(\frac{2m}{3}+c_\gamma\right)L^2
 -c e^{2\rho L^2}\right]
 \longrightarrow0.
\end{aligned}
\tag{2.5}
\]

Consequently,

\[
 \boxed{
 \mathcal E_*\le CB^2R^2,
 \qquad
 \mathcal E_*^{3/2}\le CB^3R^3.}
\tag{2.6}
\]

### 2.2 Gauge-fixed pressure row

Although the physical pressure is zero, the frozen local pressure gauge is
retained.  The inherited averaged local Riesz estimate gives

\[
 \mathcal G_{p,*}(z_0,2R;1)
 \le C\mathcal E_*(z_0,8R)^{3/2}.
\tag{2.7}
\]

Equation (2.6) therefore yields

\[
 \boxed{
 \mathcal G_{p,*}(z_0,2R;1)
 \le CB^3R^3.}
\tag{2.8}
\]

There is no unrecorded pressure cancellation in this step.

### 2.3 Velocity-cubic row

The complete general-amplitude velocity estimate is

\[
 \mathcal G_{u,*}(z_0,2R;1)
 \le C\left(B^3R^3+\mathfrak a_*^3R^4L^{-2}\right).
\tag{2.9}
\]

The packet-to-background ratio is exactly

\[
\begin{aligned}
 \frac{\mathfrak a_*^3R^4L^{-2}}{B^3R^3}
 &=\varkappa^3R\Gamma^{-3/2}L^{-2}\\
 &=\left(L^2e^{mL^2}\right)
 e^{-\rho L^2}e^{(3/2)c_\gamma L^2}L^{-2}\\
 &=1,
\end{aligned}
\tag{2.10}
\]

where (1.3) was used in the final line.  Hence

\[
 \boxed{
 \mathcal G_{u,*}(z_0,2R;1)
 \le CB^3R^3.}
\tag{2.11}
\]

The pointwise orthogonality of the passive and shear components is already
built into the inherited estimate; no mixed cubic term is omitted.

### 2.4 Algebraic harmonic row

The complete general-amplitude harmonic estimate is

\[
 \mathcal H_{u,*}(z_0,2R)
 \le C\left(B^3R^3+\mathfrak a_*^3R^4L^{-7/2}\right).
\tag{2.12}
\]

This packet-to-background ratio is

\[
\begin{aligned}
 \frac{\mathfrak a_*^3R^4L^{-7/2}}{B^3R^3}
 &=\varkappa^3R\Gamma^{-3/2}L^{-7/2}\\
 &=L^{-3/2}.
\end{aligned}
\tag{2.13}
\]

Therefore

\[
 \boxed{
 \mathcal H_{u,*}(z_0,2R)
 \le CB^3R^3.}
\tag{2.14}
\]

### 2.5 Upper closure

The common Version-M and Version-F payments consist exactly of the rows
in (2.6), (2.8), (2.11), and (2.14); the Version-F acceleration row is zero.
Thus

\[
 \boxed{
 P_*\le CB^3R^3.}
\tag{2.15}
\]

This is an inequality for the complete frozen payment, not a selected
packet denominator.

## 3. Matching payment lower bound and logarithmic rate

The fifth payment annulus contains the fixed shear box from R0.74J.  Since
the passive and shear components are pointwise orthogonal,

\[
 |u^{(\mathfrak a_*)}|^3
 =\left(\mathfrak a_*^2F^2+B^2\theta^2\right)^{3/2}
 \ge B^3|\theta|^3.
\tag{3.1}
\]

The shear-only lower bound is therefore unchanged by the new passive
amplitude:

\[
 \boxed{
 P_*\ge
 \mathcal G_{u,*}(z_0,2R;1)
 \ge8e^{-8}B^3R^3.}
\tag{3.2}
\]

Combining (2.15) and (3.2) gives

\[
 \boxed{
 P_R^{M,*}=P_R^{F,*}
 \asymp B^3R^3.}
\tag{3.3}
\]

Since \(B=\beta_jR^{-2}\), equations (1.4)--(1.6) imply

\[
 B^3R^3=\beta_j^3R^{-3}
 =\beta_j^3e^{3\rho L^2}.
\tag{3.4}
\]

Consequently,

\[
 \boxed{
 \log P_*=3\rho L^2+O(1),}
\tag{3.5}
\]

and \(P_*\to\infty\).  The counterexample is therefore entirely in the
large-payment regime; it does not alter the inherited small-payment bound.

## 4. Matching positive collar flux

Let \(\mathfrak F_0(\tau)\) and \(\mathfrak C_0\) denote the signed flux
and its positive cumulative supremum at the normalized amplitude
\(\mathfrak a_0\).  For the exact zero-frame family, the complete R0.74H
flux identity is

\[
\begin{aligned}
 \mathfrak F^{(\mathfrak a)}_R(\tau)
 =\frac{\mathfrak a^2B}{2R}
 \int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb R^3}
 \theta(t,x_3)F(t,x_2,x_3)^2
 \partial_2\vartheta_R^{\rm ann}(x)\,dx\,dt.
\end{aligned}
\tag{4.1}
\]

The integral in (4.1) does not depend on \(\mathfrak a\).  The pure shear
and \(x_1\)-derivative rows vanish exactly, the physical pressure is zero,
and a time-dependent constant gauge contributes zero by incompressibility.
It follows pointwise in \(\tau\) that

\[
 \mathfrak F_* (\tau)=\varkappa^2\mathfrak F_0(\tau).
\tag{4.2}
\]

Because \(\varkappa^2>0\), positive parts and suprema commute with this
constant multiplication:

\[
 \boxed{
 \mathfrak C_*=\varkappa^2\mathfrak C_0.}
\tag{4.3}
\]

R0.74H proves the normalized-amplitude lower bound

\[
 \mathfrak C_0\ge cB^2LR^2.
\tag{4.4}
\]

The completed R0.74N all-shell theorem estimates the same full signed
packet integral, with all shells, both packets, both collar faces, and all
periodic lifts.  After the exact R0.74K conversion, it gives

\[
 \mathfrak C_0\le CB^2LR^2.
\tag{4.5}
\]

Equations (4.3)--(4.5) yield the matching amplified law

\[
 \boxed{
 \mathfrak C_R^{M,*}
 =\mathfrak C_R^{F,*}
 \asymp\varkappa^2B^2LR^2.}
\tag{4.6}
\]

This step is an exact amplitude scaling of an already proved normalized
packet theorem.  It does not estimate the amplified flux by its absolute
cubic payment.

## 5. Matching endpoint energy and dissipation quantity

The R0.74F terminal-lobe theorem is valid for every passive amplitude and
gives directly

\[
 X_R^{M,*}=X_R^{F,*}
 \ge c\mathfrak a_*^2LR^2\Gamma.
\tag{5.1}
\]

Using (1.12),

\[
 \boxed{
 X_R^{M,*}=X_R^{F,*}
 \ge c\varkappa^2B^2LR^2.}
\tag{5.2}
\]

For the reverse inequality, use the exact signed-flux energy closure from
R0.74H:

\[
 X_R^{\alpha,*}
 \le C\left[(P_R^{\alpha,*})^{2/3}
 +\mathfrak C_R^{\alpha,*}\right].
\tag{5.3}
\]

Equations (2.15) and (4.6) give

\[
 (P_R^{\alpha,*})^{2/3}
 \le CB^2R^2
 \le C\varkappa^2B^2LR^2,
\tag{5.4}
\]

and

\[
 \mathfrak C_R^{\alpha,*}
 \le C\varkappa^2B^2LR^2.
\tag{5.5}
\]

Therefore

\[
 \boxed{
 X_R^{M,*}=X_R^{F,*}
 \asymp\varkappa^2B^2LR^2.}
\tag{5.6}
\]

The reasoning is non-circular.  The lower bound (5.2) is the direct
terminal-lobe theorem.  The collar upper bound (4.5) is the direct
R0.74N packet-integral theorem.  Neither assumes the amplified \(X_R\)
upper bound.  Only after those two independent inputs are fixed is the
R0.74H identity (5.3) used to obtain (5.6).

## 6. Conversion to the scalar frontier

By (1.11),

\[
 \varkappa^2B^2LR^2
 =B^2R^2
 L^{7/3}\exp\!\left(\frac{2m}{3}L^2\right).
\tag{6.1}
\]

Define

\[
 \delta_*:=\frac{2m}{9\rho}
 =\frac{86}{11907},
\tag{6.2}
\]

so that

\[
 3\rho\delta_*=\frac{2m}{3}.
\tag{6.3}
\]

Then

\[
 q_*:=\frac23+\delta_*
 =\frac{8024}{11907}.
\tag{6.4}
\]

From (3.3),

\[
 P_*^{2/3}\asymp B^2R^2.
\tag{6.5}
\]

From (3.4)--(3.5), the boundedness of \(\beta_j\), and (6.3),

\[
 P_*^{\delta_*}
 \asymp
 \exp\!\left(\frac{2m}{3}L^2\right),
\tag{6.6}
\]

while

\[
 (1+\log_+P_*)^{7/6}
 \asymp L^{7/3}.
\tag{6.7}
\]

Combining (4.6), (5.6), and (6.1)--(6.7) proves

\[
 \boxed{
 X_R^{\alpha,*}
 \asymp\mathfrak C_R^{\alpha,*}
 \asymp
 P_*^{\,8024/11907}
 (1+\log_+P_*)^{7/6},
 \qquad \alpha\in\{M,F\}.}
\tag{6.8}
\]

In particular,

\[
\boxed{
 \frac{X_R^{\alpha,*}}
 {P_*^{2/3}\sqrt{1+\log_+P_*}}
 \asymp
 \frac{\mathfrak C_R^{\alpha,*}}
 {P_*^{2/3}\sqrt{1+\log_+P_*}}
 \asymp
 P_*^{86/11907}
 (1+\log_+P_*)^{2/3}
 \longrightarrow\infty.}
\tag{6.9}
\]

Thus the proposed universal scalar square-root-log endpoint fails for the
positive collar flux itself and, independently, for the endpoint quantity
\(X_R^\alpha\).

More generally, (6.8) proves:

### Theorem 6.1 — scalar sub-frontier no-go

If

\[
 \Phi(p)
 =o\!\left(
 p^{8024/11907}(1+\log_+p)^{7/6}
 \right)
 \qquad(p\to\infty),
\tag{6.10}
\]

then there is no constant \(K\), independent of the smooth solution and
scale, for which either

\[
 \mathfrak C_R^\alpha\le K\Phi(P_R^\alpha)
 \quad\hbox{or}\quad
 X_R^\alpha\le K\Phi(P_R^\alpha)
\tag{6.11}
\]

holds for all smooth periodic unforced solutions in either frozen frame.

**Proof.**  Apply (6.10) along the single realized sequence
\(P_*\to\infty\) and compare with (6.8). \(\square\)

The exponent \(8024/11907\) is the strongest power frontier asserted by
this note.  It comes from the exact available general-amplitude payment
ledger.  No optimality claim beyond that ledger is made.

## 7. No fixed logarithmic correction at power \(2/3\)

There is also a simpler corollary which does not use exponential amplitude
growth.

Fix any \(\gamma\in\mathbb R\).  Choose a positive number

\[
 M>\max\left\{0,\gamma-\frac12\right\}
\tag{7.1}
\]

and replace (1.11) by

\[
 \varkappa_{\gamma}=L^M.
\tag{7.2}
\]

The family in this corollary is allowed to depend on \(\gamma\).  It is
still an exact global smooth solution for every \(j\).

The three packet-to-background ratios become

\[
 L^{2M}e^{-e_EL^2}\longrightarrow0
\tag{7.3}
\]

for the buffered energy,

\[
 L^{3M-2}e^{-mL^2}\longrightarrow0
\tag{7.4}
\]

for the velocity-cubic row, and

\[
 L^{3M-7/2}e^{-mL^2}\longrightarrow0
\tag{7.5}
\]

for the harmonic row.  The periodic error remains super-exponentially
small.  Therefore

\[
 P_{\gamma,*}\asymp B^3R^3,
 \qquad
 \log P_{\gamma,*}=3\rho L^2+O(1).
\tag{7.6}
\]

The exact flux scaling, the general-amplitude terminal lower bound, and the
signed-flux closure give

\[
 X_{\gamma,*}^\alpha
 \asymp\mathfrak C_{\gamma,*}^\alpha
 \asymp B^2R^2L^{2M+1}.
\tag{7.7}
\]

On the other hand,

\[
 P_{\gamma,*}^{2/3}
 (1+\log_+P_{\gamma,*})^\gamma
 \asymp B^2R^2L^{2\gamma}.
\tag{7.8}
\]

By (7.1),

\[
 2M+1-2\gamma>0.
\tag{7.9}
\]

Hence

\[
 \boxed{
 \frac{X_{\gamma,*}^\alpha}
 {P_{\gamma,*}^{2/3}
 (1+\log_+P_{\gamma,*})^\gamma}
 \asymp
 \frac{\mathfrak C_{\gamma,*}^\alpha}
 {P_{\gamma,*}^{2/3}
 (1+\log_+P_{\gamma,*})^\gamma}
 \longrightarrow\infty.}
\tag{7.10}
\]

### Corollary 7.1 — every fixed logarithmic power fails

For every fixed \(\gamma\in\mathbb R\), neither

\[
 \mathfrak C_R^\alpha
 \le K(P_R^\alpha)^{2/3}
 (1+\log_+P_R^\alpha)^\gamma
\tag{7.11}
\]

nor the corresponding estimate with \(X_R^\alpha\) on the left can hold
uniformly for all smooth periodic unforced solutions.

The quantifiers are important: for each prescribed \(\gamma\), equation
(7.2) selects a corresponding exact-family amplitude.  Corollary 7.1 does
not claim that one polynomial-amplitude sequence refutes all \(\gamma\)
simultaneously.  The exponential-amplitude sequence in Section 6 is one
fixed stronger sequence.

## 8. Why scalar-payment proof mechanisms stop

The counterexample also locates the failure of several natural proof
attempts.

### 8.1 Coarea and radial BV

For the frozen radial weight, coarea rewrites the signed flux as a collar
average of spherical energy fluxes.  Taking absolute values gives exactly
the inherited linear bound

\[
 \mathfrak C_R^\alpha\le CP_R^\alpha.
\tag{8.1}
\]

An improvement would require radial variation or trace control of the
spherical flux.  The scalar payment contains no such BV norm.  Integrating
by parts in the radius replaces the missing trace by derivatives of the
energy flux, which bring in the time derivative, pressure gradient, or
exterior dissipation and therefore leave the scalar ledger.

### 8.2 Weighted Holder and Lorentz interpolation

At a fixed time, weighted Holder can convert an annular \(L^3\) quantity
to annular \(L^2\).  The scalar payment, however, contains a time integral
of the cubic row, whereas \(X_R^\alpha\) contains an essential time
supremum.  There is no \(L_t^1\) to \(L_t^\infty\) embedding.  The amplified
terminal packet realizes precisely this temporal concentration.  A
logarithmic interpolation would require a second time-maximal, BV, or
Carleson-type norm not present in \(P_R^\alpha\).

### 8.3 Dyadic layer counting

The super-Gaussian shell weight alone suggests the radius
\(2^j\sim\sqrt{\log P}\).  That count controls the shell location, not the
free passive amplitude.  Equations (2.10) and (2.13) show that the
amplitude can grow through the positive reserve \(m\) while the complete
payment remains on the background scale.  No stopping index chosen only
from \(P\) and the shell weights can recover the missing
\(\varkappa^2\).

### 8.4 Pressure decomposition and moving frames

The obstruction has physical pressure \(p=0\), zero mollified trajectory,
zero residual frame velocity, and zero acceleration.  Therefore a sharper
pressure split or a change between Versions M and F cannot repair the
scalar estimate.

These observations do not prove that every augmented endpoint is false.
They show that any repair which retains the rejected square-root-log scale,
or any other scalar sub-frontier covered by Theorem 6.1, must include
information not controlled by \(P_R^\alpha\) alone.  The inherited linear
bound \(\mathfrak C_R^\alpha\le CP_R^\alpha\) remains valid.

## 9. A necessary scale for any additive repair

Suppose an additional nonnegative observable \(Y_R^\alpha\) were proposed
in a repaired estimate

\[
 \mathfrak C_R^\alpha
 \le C\left[
 (P_R^\alpha)^{2/3}
 \sqrt{1+\log_+P_R^\alpha}
 +Y_R^\alpha\right].
\tag{9.1}
\]

Along the amplified family, (6.9) forces

\[
 \boxed{
 Y_R^\alpha
 \ge c\varkappa^2B^2LR^2}
\tag{9.2}
\]

for all sufficiently large \(j\).  Thus an admissible repair must detect
the quadratic passive-amplitude growth which the scalar payment misses.

The already proved exact repair takes

\[
 Y_R^\alpha=\mathfrak C_R^\alpha,
 \qquad
 \widehat P_R^\alpha
 =P_R^\alpha+(\mathfrak C_R^\alpha)^{3/2}.
\tag{9.3}
\]

On the amplified family,

\[
 \frac{(\mathfrak C_R^\alpha)^{3/2}}{P_R^\alpha}
 \asymp\varkappa^3L^{3/2}
 =L^{7/2}e^{mL^2}
 \longrightarrow\infty.
\tag{9.4}
\]

A temporal maximal annular cubic norm, a positive time-variation norm, or
a genuine collar-flux observable may also detect this concentration, but no
sufficiency theorem for those alternatives is claimed here.

## 10. Final claim boundary

### Proved

1. The amplified field is an exact smooth periodic mean-zero unforced
   Navier--Stokes solution for the full required time range.
2. The two frozen frames coincide and all acceleration rows vanish.
3. The complete scalar payment remains comparable to \(B^3R^3\).
4. The positive collar flux and \(X_R^\alpha\) obey the matching amplified
   law (0.3).
5. The square-root-log scalar endpoint and every fixed logarithmic
   correction at power \(2/3\) fail.
6. The stronger scalar sub-frontier (6.10) fails.

### Not proved

1. No singular or blowing-up solution is constructed.
2. No theorem with an additional temporal, geometric, Carleson, BV,
   pressure, or flux hypothesis is refuted unless it reduces to a function
   of \(P_R^\alpha\) alone.
3. The small-payment regularity implication is unchanged.
4. No optimal universal replacement for the failed scalar endpoint is
   identified.
5. Novelty and priority are not claimed.
6. Global regularity and the Millennium problem remain open.

**NOT CLAY.**
