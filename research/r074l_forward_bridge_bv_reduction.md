# R0.74L — common-forward-law and positive-clock reduction

## Status

This note develops the main-collar question frozen in
r074l_problem_freeze.md.  Two statements are proved directly here:

1. the terminal-time-dependent normalized bridges admit one exact
   common-forward-law disintegration after the endpoint variable is
   integrated; and
2. paths which approach the shear transition have enough explicit
   exponential rarity to pay the one missing factor of \(R\).

The remaining good-path estimate is reduced to a short clock-support
interval.  Its physical duration is \(O(LR^3)\), so a stopping-time
Brownian modulus estimate freezes the transverse slice at cost
\(e^{-c/(LR)}\).  Section 6 gives the resulting pathwise closure.
An independent analytic reconstruction has checked its stopping times,
thickened-slice geometry, all-copy bookkeeping, and final power ledger.
Accordingly, the R0.74L main-target-collar estimate is **PROVED IN THIS
VERSION**.  The nearest inward collar and every universal
Navier--Stokes conclusion remain outside this note.  **NOT CLAY.**

Throughout, write

\[
 R=R_j,\qquad L=L_j,\qquad h=c_hLR,\qquad c_h=\frac{15}{16},
 \qquad \rho=\frac1{320},
\]

and retain the inherited R0.74G calibration bounds

\[
 R=e^{-\rho L^2},\qquad
 \frac1{128R^2}\le B\le\frac1{64R^2},
 \qquad B^{-1}\le128R^2
\tag{1.1}
\]

for all sufficiently large \(j\).

---

## 1. Exact periodic unfolding of the frozen majorant

Let

\[
 M(x_2,x_3)=\int_{\mathbb R}
 |\partial_2\psi_j^R(x_1,x_2,x_3)|\,dx_1
\tag{1.2}
\]

and define its two-variable periodization

\[
 \overline M(\bar x_2,\bar x_3)
 =\sum_{n_2,n_3\in\mathbb Z}
 M(x_2+2\pi n_2,x_3+2\pi n_3).
\tag{1.3}
\]

For large \(j\), the lifted target collar has diameter less than one.
Consequently, for each fixed torus \(x_3\), at most one \(n_3\)-lift in
(1.3) is nonzero.  Unfolding the \(n_2\)-sum and then using R0.74K (3.4)
give

\[
 \sup_{\bar x_3\in\mathbb T}
 \int_{\mathbb T}\overline M(\bar x_2,\bar x_3)\,d\bar x_2
 \le C LR.
\tag{1.4}
\]

The support radius is \(O(LR)\), while

\[
 |\partial_2\psi_j^R|\le C/R.
\]

Thus the elementary pointwise bound

\[
 0\le\overline M\le C L
\tag{1.5}
\]

also holds.  This deliberately crude bound is used only on an
exponentially rare event; the sharp good-path estimate uses (1.4).

For the clock argument, define the thickened slice

\[
 M^\sharp(x_2,x_3)
 =\int_{\mathbb R}
   \sup_{|z-x_3|\le R/16}
   |\partial_2\psi_j^R(x_1,x_2,z)|\,dx_1
\tag{1.6}
\]

and let \(\overline M^\sharp\) be its two-variable periodization.  Then

\[
 \sup_{\bar x_3\in\mathbb T}
 \int_{\mathbb T}
 \overline M^\sharp(\bar x_2,\bar x_3)\,d\bar x_2
 \le C LR.
\tag{1.7}
\]

Indeed, \(\partial_2\psi_j^R\) is supported in two radial collars of
thickness \(O(R)\) and radii \(O(LR)\).  At a fixed \(x_3\), allowing
\(|z-x_3|\le R/16\) projects each thickened three-dimensional collar to a
planar annulus or disk of area \(O((LR)R)\).  Multiplication by the
derivative bound \(C/R\) proves (1.7).  This argument is uniform at a
spherical tangent, where a pointwise chord estimate would be wasteful.

For every \(L\ge63/8\), one may take

\[
 C_{\rm pr}=\frac{65}{63}
\]

so that

\[
 \overline M(x_2,x_3)\ne0
 \quad\Longrightarrow\quad
 {\rm dist}_{\mathbb T}(x_2,0)\le C_{\rm pr}LR.
\tag{1.8}
\]

Indeed, the outer target-shell radius is
\(2^{j+1}R=(64/63)LR\), and
\(R/8\le LR/63\).

Folding the lifted \(y\)- and \(u\)-integrals in the frozen expression
(F.5) gives exactly

\[
\begin{aligned}
 \mathscr B_j(\tau)
 ={}&R^6\int_{I_{2R}\cap(-\infty,\tau]}
 \int_{\mathbb T}|\theta(t,h+y)|K_T(y)^2
 \\
 &\quad\times\mathbb E_{t,y}^{\rm br}\!\left[
   \int_{\mathbb T}|\partial K_T(u)|^2
   \overline M\!\left(
      Q(t)-\mathfrak S_t^y+u,h+y
   \right)du
 \right]dy\,dt,
\end{aligned}
\tag{1.9}
\]

where \(T=R^2+t\).  Formula (1.9) is an exact unfolding identity, not a
central-copy approximation.  Every winding of the heat kernel, bridge,
and lifted collar remains present.

Since the integrand in (1.9) is nonnegative,
\(\tau\mapsto\mathscr B_j(\tau)\) is nondecreasing.  Hence the supremum in
(F.6) introduces no separate first-passage issue.

---

## 2. Why the displayed backward bridge cannot be differentiated in time

The bridge law in (1.9) depends on its terminal horizon \(t\).  There is no
single backward path on which one may differentiate

\[
 Q(t)-\mathfrak S_t^y
\]

and write \(d(Q-\mathfrak S)=B\theta\,dt\).

An explicit formal-history test already shows the obstruction.  Let

\[
 \theta(t,x)=e^{-t}\sin x,
\]

which is an exact solution of the torus heat equation, and take the fixed
history \(Y_s=s\).  With \(B=1\) and with the irrelevant reference term
suppressed, put

\[
 q(t)=\int_0^t\theta(t-s,Y_s)\,ds.
\]

Then

\[
 q(t)=\frac{\sin t-\cos t+e^{-t}}2,
 \qquad
 q'(t)=\frac{\cos t+\sin t-e^{-t}}2,
\tag{2.1}
\]

whereas

\[
 \theta(t,Y_t)=e^{-t}\sin t.
\]

The two are not equal.  In fact \(q'\) vanishes at some
\(t_*\in(\pi/2,\pi)\), while \(\theta(t_*,Y_{t_*})>0\).  This refutes only
the illegal backward-history differentiation.  It says nothing against
the exact frozen family or (F.6).

---

## 3. Exact common-forward-law disintegration

Let \(X\) be periodic Brownian motion with generator \(\partial_x^2\),
whose initial law has density \(K_{R^2}\):

\[
 X_0\sim K_{R^2}(x)\,dx.
\tag{3.1}
\]

Equivalently, on the real lift one may take a Brownian motion
\(\widetilde X\) with generator \(\partial_x^2\), start it at zero at time
\(-R^2\), and put

\[
 X_t=\widetilde X_t\pmod{2\pi},\qquad t\ge0.
\tag{3.2}
\]

### Lemma 3.1 — integrated bridge reversal

For every nonnegative measurable path functional
\(\Phi_t(y,(Y_s)_{0\le s\le t})\),

\[
\begin{aligned}
 &\int_{\mathbb T}K_T(y)^2
   \mathbb E_{t,y}^{\rm br}
   \Phi_t(y,(Y_s)_{0\le s\le t})\,dy
 \\
 &\quad=
 \mathbb E^{\rm fw}\!\left[
   K_T(X_t)
   \Phi_t(X_t,(X_{t-s})_{0\le s\le t})
 \right].
\end{aligned}
\tag{3.3}
\]

**Proof.**  By the normalized bridge definition,

\[
 K_T(y)^2\mathbb E_{t,y}^{\rm br}\Phi_t
 =K_T(y)\mathbb E_y[\Phi_t K_{R^2}(Y_t)].
\tag{3.4}
\]

For a cylinder functional, expand the right side of (3.4) into a product
of periodic heat kernels.  Symmetry
\(K_s(a-b)=K_s(b-a)\) reverses the product, the terminal factor
\(K_{R^2}\) becomes the initial density (3.1), and \(K_T(y)\) becomes the
forward endpoint weight \(K_T(X_t)\).  This gives (3.3) for cylinders.
The monotone-class theorem and monotone convergence extend it to every
nonnegative measurable \(\Phi_t\).  No bridge at one terminal time is
identified with a bridge at another terminal time.  \(\square\)

Under path reversal, the backward functional becomes

\[
 \mathfrak S_t^{\leftarrow}[X]
 :=B\int_0^t
 [\theta(s,h)-\theta(s,h+X_s)]\,ds.
\tag{3.5}
\]

Consequently,

\[
\begin{aligned}
 Q(t)-\mathfrak S_t^{\leftarrow}[X]
 &=q_{\rm pre}
   +B\int_0^t\theta(s,h+X_s)\,ds
 =:q_\omega(t).
\end{aligned}
\tag{3.6}
\]

Therefore (1.9) becomes the exact common-time formula

\[
\begin{aligned}
 \mathscr B_j(\tau)
 ={}&R^6\int_{I_{2R}\cap(-\infty,\tau]}
 \int_{\mathbb T}|\partial K_T(u)|^2
 \\
 &\quad\times\mathbb E^{\rm fw}\!\left[
   |\theta(t,h+X_t)|K_T(X_t)
   \overline M(q_\omega(t)+u,h+X_t)
 \right]du\,dt.
\end{aligned}
\tag{3.7}
\]

Unlike the false backward differentiation in Section 2, (3.6) is one
ordinary pathwise integral on one common probability space.  Wherever
\(\theta(t,h+X_t)>0\), it has the legitimate differential

\[
 dq_\omega(t)=B\theta(t,h+X_t)\,dt.
\tag{3.8}
\]

---

## 4. A rare transition-approach event

Put

\[
 \delta_R=\arcsin(16R),\qquad
 d_R=h-\delta_R-32R.
\tag{4.1}
\]

For \(R\le1/32\), R0.74F proves \(\delta_R\le32R\).  Realize the initial
heat density and the subsequent forward Brownian motion by one real
Brownian path \(Z_s\), with generator \(\partial_x^2\), over
\(0\le s\le66R^2\).  Thus \(X_t=Z_{R^2+t}\pmod{2\pi}\).  Define

\[
 \mathcal G
 =\left\{\sup_{0\le s\le66R^2}|Z_s|<d_R\right\}.
\tag{4.2}
\]

For

\[
 L\ge\frac{262144}{15},
\tag{4.3}
\]

one has

\[
 d_R\ge(c_hL-64)R
 \ge\frac{255}{256}c_hLR.
\tag{4.4}
\]

The reflection principle and the Gaussian tail bound give

\[
 \mathbb P(\mathcal G^c)
 \le4\exp\!\left(-\frac{d_R^2}{264R^2}\right)
 \le4e^{-A L^2},
\tag{4.5}
\]

where

\[
 A=\frac{(255/256)^2c_h^2}{264}
 =\frac{4876875}{1476395008}.
\tag{4.6}
\]

The exact reserve over the packet exponent is

\[
 A-\rho
 =\frac{1315703}{7381975040}>0.
\tag{4.7}
\]

Hence

\[
 \mathbb P(\mathcal G^c)\le4R
\tag{4.8}
\]

for all indices satisfying (4.3).  Since
\(L_{14}=(63/32)2^{14}=32256\), it is enough to take \(j\ge14\).

On \(\mathcal G\), the lower endpoint obeys
\(h+Z_{R^2+t}>\delta_R+32R\).  The upper endpoint is also safe because
R0.74F gives \(h\le LR\le5/144\), hence \(2h<\pi\).  Thus every
\(h+X_t\) stays at circular distance at least \(32R\) from the defect
set \(P_R^c\), for \(0\le t\le65R^2\).  The
periodic heat-tail estimate from R0.74F therefore gives

\[
 1-\theta(t,h+X_t)
 \le4\exp\!\left(-\frac{(32R)^2}{4(65R^2)}\right)
 =4e^{-256/65}<\frac18.
\tag{4.9}
\]

The last strict inequality follows without decimal evaluation from

\[
 1+x+\frac{x^2}{2}+\frac{x^3}{6}+\frac{x^4}{24}>32,
 \qquad x=\frac{256}{65},
\tag{4.10}
\]

and \(e^x\) being larger than its fourth Taylor partial sum.  Thus

\[
 \theta(t,h+X_t)>\frac78
 \quad\hbox{on }\mathcal G.
\tag{4.11}
\]

### Lemma 4.1 — the bad paths already have the target scale

Let \(\mathscr B_j^{\rm bad}\) denote the part of (3.7) with the indicator
\(1_{\mathcal G^c}\).  Then

\[
 \mathscr B_j^{\rm bad}(\tau)\le C LR^5
\tag{4.12}
\]

uniformly in \(\tau\in I_R\).

**Proof.**  Uniformly for \(R^2\le T\le66R^2\),

\[
 \|K_T\|_\infty\le C/R,
 \qquad
 \int_{\mathbb T}|\partial K_T(u)|^2\,du\le C/R^3.
\tag{4.13}
\]

Use \(|\theta|\le1\), (1.5), the time length \(4R^2\), and (4.8) in
(3.7).  The result is

\[
 R^6\cdot R^{-1}\cdot L\cdot R^{-3}\cdot R^2
 \mathbb P(\mathcal G^c)
 \le C LR^5.
\tag{4.14}
\]

This is the only place where the crude pointwise chord estimate is used.
\(\square\)

---

## 5. Positive-clock reduction on the good paths

Define the clipped coefficient

\[
 \widehat\theta(t,x)=\max\{\theta(t,x),3/4\}
\tag{5.1}
\]

and the globally increasing clock

\[
 \widehat q(t)
 =q_{\rm pre}+B\int_0^t\widehat\theta(s,h+X_s)\,ds.
\tag{5.2}
\]

On \(\mathcal G\), equations (4.11) and (5.1) imply
\(\widehat q=q_\omega\).  Let \(t=t(q)\) be the inverse of (5.2), and let

\[
 \widehat X_q=X_{t(q)}.
\tag{5.3}
\]

All clock values needed for \(0\le t\le65R^2\) lie in the deterministic
interval

\[
 J=[q_{\rm pre},q_{\rm pre}+65BR^2].
\tag{5.4}
\]

By (1.1), \(|J|\le65/64<2\pi\).

Because the integrand is nonnegative, change variables by (3.8) on
\(\mathcal G\), replace \(q_\omega\) by \(\widehat q\), drop the indicator,
and enlarge the random clock interval to \(J\).  This reduces the good
part of (3.7) to

\[
\begin{aligned}
 \mathscr B_j^{\rm good}(\tau)
 \le{}&\frac{R^6}{B}\frac{C}{R}
 \int_{\mathbb T}H_R(u)
 \int_J
 \mathbb E\,\overline M(q+u,h+\widehat X_q)
 \,dq\,du,
\end{aligned}
\tag{5.5}
\]

where one may take

\[
 H_R(u)=\sup_{R^2\le T\le66R^2}|\partial K_T(u)|^2,
 \qquad
 \int_{\mathbb T}H_R(u)\,du\le C R^{-3}.
\tag{5.6}
\]

Thus it remains to prove, uniformly in \(u\),

\[
 \boxed{
 \int_J\mathbb E\,
 \overline M(q+u,h+\widehat X_q)\,dq
 \le C LR.}
\tag{5.7}
\]

This is the exact occupation statement which slice BV alone cannot
replace.

---

## 6. Short clock support and pathwise BV

The occupation bound (5.7) can be proved without a marginal-density
theorem.  Fix \(u\in\mathbb T\) and set

\[
 \mathcal A_u
 =\left\{q\in J:
 {\rm dist}_{\mathbb T}(q+u,0)\le C_{\rm pr}LR\right\}.
\tag{6.1}
\]

By (1.8), the integrand in (5.7) vanishes outside \(\mathcal A_u\).
Since \(|J|<2\pi\) and \(LR\to0\), the set \(\mathcal A_u\) has at most
two connected components, and

\[
 |\mathcal A_u|\le C LR.
\tag{6.2}
\]

Write these components as \(A_\nu=[a_\nu,b_\nu]\), with
\(\nu\in\{1,2\}\), omitting empty components.  Extend \(X\) and the
positive clock (5.2) beyond \(65R^2\), if necessary, until all of \(J\)
has been reached.  The entry times

\[
 \sigma_\nu=t(a_\nu)
\tag{6.3}
\]

are stopping times for the Brownian filtration: for every \(r\ge0\),

\[
 \{\sigma_\nu\le r\}
 =\{\widehat q(r)\ge a_\nu\}\in\mathcal F_r.
\tag{6.4}
\]

Moreover, because \(\widehat\theta\ge3/4\),

\[
 0\le t(b_\nu)-t(a_\nu)
 \le\frac{4|A_\nu|}{3B}
 \le C L R^3.
\tag{6.5}
\]

Here the last inequality uses \(B^{-1}\le CR^2\).

For the real Brownian lift, define the modulus event

\[
 \mathcal H_{\nu,u}
 =\left\{
 \sup_{a_\nu\le q\le b_\nu}
 |\widehat X_q-\widehat X_{a_\nu}|
 \le R/16
 \right\}.
\tag{6.6}
\]

The strong Markov property at \(\sigma_\nu\), (6.5), the reflection
principle, and the Gaussian tail bound imply

\[
 \mathbb P(\mathcal H_{\nu,u}^c)
 \le4\exp\!\left(-\frac{c}{LR}\right)
\tag{6.7}
\]

with an absolute \(c>0\), uniformly in \(u,\nu,j\).  The random terminal
time \(t(b_\nu)\) causes no problem because its elapsed time is bounded by
the deterministic right side of (6.5).

On \(\mathcal H_{\nu,u}\), the definition (1.6) of the thickened slice
gives

\[
\begin{aligned}
 &\int_{A_\nu}
 \overline M(q+u,h+\widehat X_q)\,dq
 \\
 &\quad\le
 \int_{A_\nu}
 \overline M^\sharp
 (q+u,h+\widehat X_{a_\nu})\,dq
 \le C LR
\end{aligned}
\tag{6.8}
\]

by (1.7).  On the complementary modulus event, the pointwise bound (1.5)
and (6.2) give the deterministic estimate

\[
 \int_{A_\nu}
 \overline M(q+u,h+\widehat X_q)\,dq
 \le C L^2R.
\tag{6.9}
\]

Therefore

\[
\begin{aligned}
 \mathbb E\int_{A_\nu}
 \overline M(q+u,h+\widehat X_q)\,dq
 &\le CLR+
 CL^2R\,e^{-c/(LR)}
 \\
 &\le C LR
\end{aligned}
\tag{6.10}
\]

for all sufficiently large \(j\).  Summing the at most two components
proves (5.7).

Substitution into (5.5) yields

\[
 \mathscr B_j^{\rm good}(\tau)
 \le\frac{CR^6}{B}\,R^{-1}R^{-3}(LR)
 \le C LR^5.
\tag{6.11}
\]

Together with Lemma 4.1, the argument proves

\[
 \sup_{\tau\in I_R}\mathscr B_j(\tau)\le C LR^5.
\tag{6.12}
\]

The independent audit recorded in
r074l_main_collar_independent_audit.md reconstructs the exact reversal
(3.3), the stopping-time statement (6.4), the thickened-slice geometry
(1.7), and the periodized support count (6.2).

---

## 7. Discarded marginal-projection alternative

A separate bounded primary-source audit checked whether the inverse-clock
process could instead be closed by a one-time marginal density bound.
Brunick--Shreve, Theorem 3.6 and Corollary 3.7, support mimicking the
one-time marginals of an Itô process with adapted coefficients and a random
initial value:

- G. Brunick and S. Shreve,
  [Mimicking an Itô process by a solution of a stochastic differential
  equation](https://arxiv.org/abs/1011.0111).

Kobayashi's time-change calculus supports using the inverse of a continuous
strictly increasing adapted clock:

- K. Kobayashi,
  [Stochastic Calculus for a Time-changed Semimartingale and the Associated
  Stochastic Differential Equations](https://arxiv.org/abs/0906.5385).

That route was not used.  The projected density satisfies a forward
equation of the form

\[
 \partial_s p=\partial_x^2(a(s,x)p)
\tag{7.1}
\]

with only measurable \(a\).  The classical measurable-coefficient
Aronson theorem checked in the audit is stated for a divergence-form
equation and does not directly supply the required Gaussian bound for
(7.1) without additional coefficient regularity.  Quoting Markovian
projection plus Aronson as a completed proof would therefore leave a
theorem mismatch.  Section 6 avoids that mismatch entirely.

## 8. Adversarial boundary of the mechanism

The inherited slice estimate (1.4), a one-sided lower bound on
\(\mathfrak S\), and a bounded shift range do not by themselves imply
(F.6).  A deterministic proxy can keep \(Q-S\) fixed in one positive
collar slice for a time \(R^2\).  Its scale is

\[
 R^6\cdot R^{-1}\cdot R^{-3}\cdot R^2=R^4,
\tag{8.1}
\]

whereas the desired scale is

\[
 LR^5=(LR)R^4.
\tag{8.2}
\]

The proxy therefore loses \(1/(LR)\).  It is not the frozen stochastic
shift and is not a counterexample to (F.6).  It only verifies that the
short-clock occupation input in Section 6 is genuinely structural rather than
an ornamental reformulation of slice BV.

## 9. Current conclusion

At the present audit boundary:

- **PROVED HERE:** exact periodic unfolding, common-forward-law reversal,
  the legitimate forward clock identity, and the bad-path estimate at
  \(CLR^5\);
- **PROVED AND INDEPENDENTLY AUDITED:** the good-path closure through the
  short clock-support modulus argument in Section 6 and the resulting
  main-collar estimate (6.12);
- **OPEN OUTSIDE THIS FREEZE:** nearest inward expulsion, the total signed
  packet condition, matching \(\mathfrak C_j\), the \(X_j\) upper bound,
  and every universal regularity statement.

No statement in this note is a solution of the Navier--Stokes Millennium
problem.  **NOT CLAY.**
