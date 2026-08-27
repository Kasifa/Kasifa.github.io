# R0.72G -- complete-root packing on the exact one-carrier ray

**Date:** 2026-08-27

**Status:** analytic theorem in the exact real one-carrier triangular
Navier--Stokes class.  The result closes the complete-root estimate for this
test family and proves sharp saturation of the R0.72F critical-log payment
along the R0.72E Bessel sequence.  It does not prove the estimate for a
general triangular flow or for a general three-dimensional solution.

**Keywords:** Navier--Stokes regularity, triangular 2.5D flow, temporal
zeros, Rolle theorem, bounded variation, projected Lamb vector, negative
Sobolev action, Bessel functions

---

## 0. Direct decision

R0.72F selected the critical-log initial-layer weight

\[
 w_*(s)=s^{-1/3}[1+\log(1/s)]
 \tag{0.1}
\]

but left open whether roots outside the selected Bessel neighborhoods could
make the complete ledger larger.  On the exact R0.72E one-carrier ray, they
cannot.

Fix an integer \(q_0\) larger than the radius of the declared target
multiplier, put \(\mu=q_0^{-2}\), fix \(\delta\ge1\), and consider

\[
 F_x=-A_\mu F+\delta V(x)F,
 \qquad
 (A_\mu F)_r=(r^2+\mu)F_r,
 \qquad
 (V(x)F)_r=-ie^{-x}(F_{r-1}+F_{r+1}),
 \tag{0.2}
\]

with \(F(0)=ie_{-1}\).  Let

\[
 f(x)=F_0(x),\qquad
 h(x)=P_0V(x)F(x),\qquad
 q(x)=\|V(x)F(x)\|_{A_\mu^{-1}}^2,
 \tag{0.3}
\]

and define the launch-inclusive complete root-slope mass on \([0,X)\) by

\[
 G_{\rm all}(\delta;X)
 :=\sum_{\substack{x\in[0,X)\\ f(x)=0}}|h(x)|^2.
 \tag{0.4}
\]

The sum in (0.4) is the monotone supremum over finite root subsets.  This
definition does not assume that the root set is finite or separated.

The main estimate is

\[
\boxed{
 G_{\rm all}(\delta;X)
 \le 1+2\left[(2+\mu)\mu
 +\delta\sqrt{2\mu(1+\mu)}\right]
 Q_{0,0,\delta,q_0}(X),}
 \tag{0.5}
\]

where

\[
 Q_{0,0,\delta,q_0}(X)=\int_0^Xq(x)\,dx.
 \tag{0.6}
\]

R0.72E proved

\[
 Q_{0,0,\delta,q_0}(X)
 \le C_{X,q_0}\frac{1+\log(2+\delta)}{\delta}.
 \tag{0.7}
\]

Consequently

\[
 \boxed{
 G_{\rm all}(\delta;X)
 \le C_{X,q_0}[1+\log(2+\delta)].}
 \tag{0.8}
\]

This bound is independent of the number and separation of roots.  Along
\(\delta_R=R^4\), the selected Bessel roots from R0.72E give

\[
 G_R^{\rm sel}
 =\frac8{\pi^2}\log R+O_{q_0}(1)
 =\frac2{\pi^2}\log\delta_R+O_{q_0}(1).
 \tag{0.9}
\]

Because selected roots are a subset of complete roots,

\[
 \boxed{
 G_{\rm all}(\delta_R;X)\asymp_{X,q_0}\log\delta_R.}
 \tag{0.10}
\]

Thus additional roots may change a bounded multiplicative constant, but
they cannot create a hidden super-logarithmic slope mass in this exact
family.

There is also a direct physical consequence.  The root ledger below uses
the half-open observation window \([0,T)\), while its continuous integrals
are taken over the closure \([0,T]\); this prevents a terminal root from
being counted differently in the two sides.  Keep the exact shear
amplitude \(P=q_0^2\delta\), let the active squared amplitude be
\(A_\delta=S_\delta^2\le C_A\delta\), and fix \(I=[0,T]\).  For all
sufficiently large \(\delta\), the exact one-carrier solutions obey

\[
 \boxed{
 \mathcal J_{\rm all}(I)
 \le C_{T,q_0,C_A}
 D^{1/3}\Lambda_{1,*}(I;u),}
 \tag{0.11}
\]

where \(\Lambda_{1,*}=\mathcal R_Y[1+\mathscr A_*]\) and \(\mathscr A_*\)
uses (0.1).  This proves the R0.72F candidate only on the displayed exact
one-carrier ray.  It is not a theorem for arbitrary launch data,
multi-carrier triangular flows, or general Navier--Stokes solutions.

For the original R0.72E choice

\[
 A_R=S_R^2=\frac{\delta_R}{\log(2+\delta_R)},
 \tag{0.12}
\]

both sides of (0.11) have the same order:

\[
 \boxed{
 \mathcal J_{{\rm all},R}\asymp\delta_R,
 \qquad
 D_R^{1/3}\Lambda_{1,*}(I;u_R)\asymp\delta_R,
 \qquad
 \frac{\mathcal J_{{\rm all},R}}
 {D_R^{1/3}\Lambda_{1,*}(I;u_R)}\asymp1.}
 \tag{0.13}
\]

The critical-log payment is therefore sharp on the complete root set of
this test sequence, not only on the roots selected in advance.

---

## 1. Exact class and real phase gauge

The physical velocity is the globally smooth triangular solution

\[
 u=(f_{\rm phys}(y,z,t),0,v(y,t)),
 \qquad
 v_t=v_{yy},
 \qquad
 (f_{\rm phys})_t+v(f_{\rm phys})_z
 =(f_{\rm phys})_{yy}+(f_{\rm phys})_{zz}.
 \tag{1.1}
\]

Its vorticity and projected Lamb vector satisfy the exact identity

\[
 \omega=(v_y,(f_{\rm phys})_z,-(f_{\rm phys})_y),
 \qquad
 \mathbb P(u\times\omega)=(-v(f_{\rm phys})_z,0,0).
 \tag{1.2}
\]

The positive \(z\)-frequency sector reduces to (0.2) after
\(x=q_0^2t\).  The negative sector is its conjugate, so the physical field
is real.

The scalar target in (0.3) is also real.  Write

\[
 F_r(x)=i^{-r}a_r(x).
 \tag{1.3}
\]

Then \(a_{-1}(0)=1\), all other launch coefficients vanish, and (0.2)
becomes

\[
 a_r'=-(r^2+\mu)a_r
 +\delta e^{-x}(a_{r-1}-a_{r+1}).
 \tag{1.4}
\]

The system has real coefficients and real initial data.  Hence every
\(a_r\) is real, in particular

\[
 f=F_0=a_0\in\mathbb R,
 \qquad
 h=e^{-x}(a_{-1}-a_1)\in\mathbb R.
 \tag{1.5}
\]

This real-phase property is what permits the use of Rolle's theorem below.
It is not asserted for an arbitrary complex target coordinate.

At launch,

\[
 f(0)=0,
 \qquad
 h(0)=P_0V(0)(ie_{-1})=1.
 \tag{1.6}
\]

---

## 2. Two exact target-row identities

The target row of (0.2) gives

\[
 \boxed{f'+\mu f=\delta h.}
 \tag{2.1}
\]

Put

\[
 z=VF,
 \qquad
 b=P_0Vz=P_0V^2F.
 \tag{2.2}
\]

Since \(V'=-V\),

\[
\begin{aligned}
 h'
 &=P_0V'F+P_0VF'\\
 &=-h-P_0VA_\mu F+\delta P_0V^2F.
\end{aligned}
 \tag{2.3}
\]

Only input rows \(r=\pm1\) enter \(P_0V\), and both have diagonal
eigenvalue \(1+\mu\).  Therefore

\[
 P_0VA_\mu F=(1+\mu)P_0VF=(1+\mu)h,
 \tag{2.4}
\]

and

\[
 \boxed{h'=-(2+\mu)h+\delta b.}
 \tag{2.5}
\]

The two coordinates needed in (2.5) are controlled pointwise by the full
negative-Sobolev observation.  From the \(r=0\) term of

\[
 q=\langle A_\mu^{-1}z,z\rangle
 =\sum_{r\in\mathbb Z}\frac{|z_r|^2}{r^2+\mu},
 \tag{2.6}
\]

one gets

\[
 \boxed{|h|^2\le\mu q.}
 \tag{2.7}
\]

Also

\[
 b=-ie^{-x}(z_{-1}+z_1),
 \tag{2.8}
\]

so the \(r=\pm1\) terms give

\[
 \boxed{|b|^2\le2(1+\mu)q.}
 \tag{2.9}
\]

No estimate of the root count appears in these identities.

---

## 3. Rolle--BV sampling of every root

### Lemma 3.1 -- root-slope mass from one continuous action

Let \(0<x_1<\cdots<x_N<X\) be any finite set of positive roots of
\(f\), and set \(x_0=0\).  Then

\[
 \sum_{j=1}^N|h(x_j)|^2
 \le2\int_0^X|h(x)h'(x)|\,dx.
 \tag{3.1}
\]

#### Proof

Define the integrating-factor target

\[
 \psi(x)=e^{\mu x}f(x).
 \tag{3.2}
\]

By (2.1),

\[
 \psi'(x)=\delta e^{\mu x}h(x).
 \tag{3.3}
\]

For each \(j\), the real function \(\psi\) vanishes at both endpoints of
\([x_{j-1},x_j]\).  Rolle's theorem provides
\(c_j\in(x_{j-1},x_j)\) with \(h(c_j)=0\).  Hence

\[
 |h(x_j)|^2
 =\left|2\int_{c_j}^{x_j}h(x)h'(x)\,dx\right|
 \le2\int_{c_j}^{x_j}|hh'|\,dx.
 \tag{3.4}
\]

The intervals \([c_j,x_j]\) are disjoint.  Summing proves (3.1).
\(\square\)

The lemma holds for an arbitrary finite root subset, even when other roots
lie between its listed endpoints.  A multiple root satisfies \(f=f'=0\),
so (2.1) gives \(h=0\) and it contributes no slope mass.  Taking the
monotone supremum over finite subsets covers the complete extended root
sum.  The launch root contributes the separate quantity \(|h(0)|^2=1\).

Insert (2.5), (2.7), and (2.9) into (3.1):

\[
\begin{aligned}
 \sum_{j=1}^N|h(x_j)|^2
 &\le2(2+\mu)\int_0^X|h|^2\,dx
 +2\delta\int_0^X|hb|\,dx\\
 &\le2\left[(2+\mu)\mu
 +\delta\sqrt{2\mu(1+\mu)}\right]
 \int_0^Xq(x)\,dx.
\end{aligned}
 \tag{3.5}
\]

Adding the launch root and taking the supremum proves (0.5).

Two features are important.  First, (3.5) pays for all roots at once; it
does not divide by a minimum spacing.  Second, it uses the full
\(A_\mu^{-1}\) observation \(q\), not a target-shell proxy.

---

## 4. Complete logarithmic packing and sharpness

Apply the R0.72E action theorem (0.7) to (0.5).  For \(\delta\ge1\),

\[
\begin{aligned}
 G_{\rm all}(\delta;X)
 &\le1+C_{q_0}\delta
 Q_{0,0,\delta,q_0}(X)\\
 &\le C_{X,q_0}[1+\log(2+\delta)].
\end{aligned}
 \tag{4.1}
\]

This is (0.8).

For \(\delta_R=R^4\), R0.72E constructed one simple exact root near each
of the first \(R\) positive zeros of \(J_1(2\tau)\) and proved (0.9).
Therefore

\[
 c_{X,q_0}\log\delta_R
 \le G_R^{\rm sel}
 \le G_{\rm all}(\delta_R;X)
 \le C_{X,q_0}\log\delta_R
 \tag{4.2}
\]

for all sufficiently large \(R\).  This proves (0.10).

The theorem determines the order of the complete mass.  It does not
determine a leading constant.  In particular, finite computations may find
many additional small-slope roots without contradicting (4.2).

---

## 5. Conversion to the critical-log physical ledger

Let

\[
 Q_{*,\delta,q_0}(X)
 :=\int_0^X
 w_*\!\left(\frac{x}{X}\right)q(x)\,dx.
 \tag{5.1}
\]

R0.72F proved the two-sided estimate

\[
 \boxed{
 Q_{*,\delta,q_0}(X)
 \asymp_{X,q_0}
 \delta^{-2/3}\log\delta.}
 \tag{5.2}
\]

Combining the upper bound (4.1) with the lower bound in (5.2) gives, for
all sufficiently large \(\delta\),

\[
 \boxed{
 G_{\rm all}(\delta;X)
 \le C_{X,q_0}\delta^{2/3}Q_{*,\delta,q_0}(X).}
 \tag{5.3}
\]

Equation (5.3) is a consequence of the two already proved action estimates;
it is not a new pointwise domination of the unweighted integrand by the
critical weight.

Now take physical shear amplitude \(P=q_0^2\delta\) and active squared
amplitude \(A_\delta=S_\delta^2\le C_A\delta\).  Root atoms are sampled on
\([0,T)\), and the action is integrated on \([0,T]\).  The exact enstrophy
decomposition inherited from R0.72E and its first-moment barrier give, on
every fixed \(I=[0,T]\),

\[
 c_{T,q_0}P^2\le Y(t)\le C_{q_0,C_A}P^2,
 \qquad
 \mathcal R_Y(I)\le C_{T,q_0,C_A},
 \tag{5.4}
\]

because the active contribution is at most
\(C A_\delta(1+\delta^{2/3})=o(\delta^2)\).  The launch data size satisfies

\[
 D=2P^2(1+q_0^2)+2A_\delta(q_0^2+2)
 \asymp_{q_0,C_A}\delta^2.
 \tag{5.5}
\]

The exact projected-Lamb Fourier identity and (5.4) yield

\[
 \mathscr A_*(I;u)
 \asymp_{T,q_0,C_A}
 A_\delta Q_{*,\delta,q_0}(q_0^2T).
 \tag{5.6}
\]

At every target root, (2.1) gives \(f_x=\delta h\).  If \(h\ne0\), the
root is simple, and the inherited global target-shell identity
\(C_{*,t}=-\Delta F_*\) makes it a positive right entry.  If \(h=0\), the
root atom is zero.  Thus the fixed multiplier gives, for every complete
root and not only for the preselected Bessel roots,

\[
 J_*(t_x)
 =c_*\frac{A_\delta P^2|h(x)|^2}{Y(t_x)}.
 \tag{5.7}
\]

Multiple roots have \(h=0\).  Summing (5.7), using the lower enstrophy
floor and then (5.3), gives

\[
\begin{aligned}
 \mathcal J_{\rm all}(I)
 &\le C_{T,q_0,C_A}A_\delta
 G_{\rm all}(\delta;q_0^2T)\\
 &\le C_{T,q_0,C_A}
 \delta^{2/3}A_\delta Q_{*,\delta,q_0}(q_0^2T)\\
 &\le C_{T,q_0,C_A}
 D^{1/3}\Lambda_{1,*}(I;u).
\end{aligned}
 \tag{5.8}
\]

This proves (0.11).

For \(A_R=\delta_R/\log(2+\delta_R)\), equations (0.10), (5.2), and
(5.4)--(5.7) give

\[
 \mathcal J_{{\rm all},R}
 \asymp A_RG_{\rm all}
 \asymp\delta_R,
 \tag{5.9}
\]

\[
 \mathscr A_*(I;u_R)
 \asymp A_RQ_{*,\delta_R,q_0}
 \asymp\delta_R^{1/3},
 \tag{5.10}
\]

and therefore (0.13).  The selected Bessel lower bound supplies the positive
lower constant; the complete-root theorem supplies the upper constant.

---

## 6. Finite numerical audit

The numerical archive has two independent finite-precision routes.

1. The producer evolves the real invariant lattice with fixed-step
   binary64 RK4, refines every detected target crossing by cubic Hermite
   interpolation and Brent's method, evaluates the complete root-slope
   mass, and records dyadic mass packets.
2. The independent route evolves the Fourier-angle equation by a
   time-dependent Strang split step, uses a different root interpolant, and
   repeats the calculation under mode and step refinement.

Both routes are binary64 diagnostics.  They test signs, scaling, root
handling, solver pressure, and agreement of complete mass.  They do not
certify infinitely many \(\delta\), prove (0.5), or replace the R0.72E
action theorem.

The archived scope flags state

```text
intervalArithmetic: false
completeRootUpperBoundInExactOneCarrier: true   # analytic theorem
generalTriangularCompleteRootBound: false
arbitraryNSECompleteRootBound: false
continuationCriterion: false
provesNSERegularity: false
```

---

## 7. Literature boundary

The Bessel lower family uses the standard Jacobi--Anger expansion and
fixed-order Bessel asymptotics; the primary reference checked here is the
[NIST Digital Library of Mathematical Functions, Sections 10.12, 10.17,
and 10.21](https://dlmf.nist.gov/10).

The negative-moment input behind the inherited R0.72E action estimate is
Kusuoka--Stroock, *Applications of the Malliavin calculus, Part II*,
Corollary (3.25) and inequality (3.27),
[DOI 10.15083/00039520](https://doi.org/10.15083/00039520).

Angenent, *The zero set of a solution of a parabolic equation*, Journal
fur die reine und angewandte Mathematik 390 (1988), 79--96,
[DOI 10.1515/crll.1988.390.79](https://doi.org/10.1515/crll.1988.390.79),
controls spatial zero sets for scalar parabolic equations.  It does not
state the temporal fixed-Fourier-coordinate slope-sum estimate (0.5).

The new step in this report is elementary once the R0.72E observation is
available: the real phase gauge, the two target-row identities, and a
Rolle--bounded-variation sampling argument.  The checked sources do not
state (0.5), (0.10), or the exact-family physical bridge (0.11).  This is a
bounded non-collision statement, not a claim of novelty, priority, or an
exhaustive literature search.

---

## 8. Claim--evidence boundary

### Proved

1. The gauge \(F_r=i^{-r}a_r\) makes the one-carrier target \(f\) and its
   coupling slope \(h\) real.
2. The exact identities (2.1) and (2.5) hold.
3. The full negative-Sobolev observation controls \(h\) and \(b\) as in
   (2.7) and (2.9).
4. Rolle sampling controls every target root by (3.1), independently of
   root count and separation.
5. The complete root-slope mass satisfies (0.5) and the logarithmic upper
   bound (0.8).
6. Along \(\delta_R=R^4\), the complete mass is exactly logarithmic in
   order, as in (0.10).
7. For the displayed one-carrier physical family with
   \(A_\delta\le C_A\delta\), the critical-log candidate holds as (0.11).
8. For \(A_R=\delta_R/\log(2+\delta_R)\), both sides of the complete-root
   payment are order \(\delta_R\), so the bound is sharp in order.

### Not proved

1. A complete-root estimate uniform in the number of shear carriers.
2. A dimension-free phase gauge or replacement for complex target
   coordinates.
3. A restart covering theorem for arbitrary strong or Leray--Hopf
   solutions.
4. A bound uniform as \(q_0\to\infty\).
5. The candidate (0.11) for the full triangular class.
6. The candidate for arbitrary three-dimensional Navier--Stokes solutions.
7. A new continuation criterion, finite-time singularity, or global
   regularity.
8. Originality, priority, or an exhaustive literature claim.

---

## 9. Research value and next finite gate

R0.72G removes one specific uncertainty left by R0.72F.  The extra roots of
the strongest exact one-carrier counterfamily do not produce an unpaid
mass.  The critical-log action pays the complete root set there, and the
payment is sharp in order.

This is a route-validation theorem, not a regularity theorem.  It says that
the exact Bessel family no longer refutes the fixed critical-log candidate.
The remaining obstruction is portability: the proof uses one real carrier,
one real target coordinate, a fixed \(q_0\), and the inherited action decay.

The next finite gate, R0.72H, should therefore keep \(w_*\) fixed and ask
whether the complete-root constant can remain dimension-free under a
finite real multi-carrier shear.  The real Rolle step itself survives for
a real target coordinate.  What ceases to close automatically is the mixed
target-row term

\[
 \mathcal E_Q=\int_0^X |h\,QF|\,dx,
 \qquad
 Q=P_0[V'+V(D+\lambda_0)].
 \tag{9.1}
\]

For one carrier, the two neighboring input rows have the same heat rate and
\(QF\) is a fixed multiple of \(h\).  Multiple carriers generally destroy
that proportionality.  R0.72H must either pay (9.1) from the existing data
and critical-log action with a carrier-count-independent constant, or give
an explicit growing-carrier counterfamily.  That is the smallest new
interface; it does not yet ask for a general three-dimensional trace
theorem.
