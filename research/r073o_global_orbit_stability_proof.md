# R0.73O proof: every global unforced periodic \(H^3\) orbit has a positive asymptotic stability tube

**Status:** continuum proof; the independent analytic audit passed after the
two expository repairs incorporated below.  The literature audit classifies
the phenomenon as classical and the present proof as a topology-matched route
closure, not a priority claim.

**Depends on:** standard local \(H^3\) strong well-posedness and continuation
for periodic Navier--Stokes; no finite computation is used in the theorem

## 1. Theorem

On the normalized standard three-torus, consider

\[
 \partial_tu-\Delta u+P(u\cdot\nabla u)=0,
 \qquad \nabla\cdot u=0,
 \qquad \int_{\mathbb T^3}u\,dx=0.
 \tag{1.1}
\]

Let

\[
 u\in C([0,\infty);H^3_{\sigma,0})
 \cap L^2_{\rm loc}([0,\infty);H^4_{\sigma,0})
 \tag{1.2}
\]

be an a priori global strong solution.  Then:

1. its accumulated \(H^4\) action is finite,

   \[
   \mathcal A_4[u]:=\int_0^\infty|u(t)|_4\,dt<\infty;
   \tag{1.3}
   \]

2. there are universal constants \(C_*\ge1\) and a radius in the homogeneous
   Stokes \(H^3\) norm,

   \[
   R_A[u]={1\over4C_*}e^{-C_*\mathcal A_4[u]}>0,
   \tag{1.4}
   \]

   such that, for every \(t_0\ge0\), every mean-zero divergence-free
   \(v(t_0)\in H^3\) satisfying

   \[
   |v(t_0)-u(t_0)|_3<R_A[u]
   \tag{1.5}
   \]

   generates a unique global forward strong solution and obeys

   \[
   \boxed{
   |v(t)-u(t)|_3
   \le e^{C_*\mathcal A_4[u]}
   e^{-(t-t_0)/2}|v(t_0)-u(t_0)|_3,
   \qquad t\ge t_0.}
   \tag{1.6}
   \]

Here \(|z|_m=\|A^{m/2}z\|_2\), with \(A=-P\Delta\) on the mean-zero
divergence-free phase space.  Fix \(\kappa_3\ge1\) so that

\[
 \kappa_3^{-1}\|z\|_{H^3}\le |z|_3
 \le\kappa_3\|z\|_{H^3}.
 \tag{1.7}
\]

Then \(R_{H^3}[u]:=\kappa_3^{-1}R_A[u]\) is a radius in the usual
inhomogeneous \(H^3\) norm, and (1.6) implies the same estimate there with
the prefactor multiplied by at most \(\kappa_3^2\).  Thus the topology is
unchanged, but the two numerical radii are not identified.

## 2. Stokes-scale preliminaries

The Fourier spectrum of \(A\) lies in \(\{1,2,3,\ldots\}\).  Hence

\[
 |z|_{m+1}\ge |z|_m
 \tag{2.1}
\]

and logarithmic convexity gives

\[
 |z|_m^2\le |z|_{m-1}|z|_{m+1}.
 \tag{2.2}
\]

The following periodic product estimates are standard consequences of
Sobolev multiplication in three dimensions in the specializations used
below:

\[
\begin{aligned}
 |(B(u,u),Au)|
 &\le C|u|_1^{3/2}|u|_2^{3/2},\\
 \|B(a,b)\|_{H^1}
 &\le C\|a\|_{H^2}\|b\|_{H^2},\\
 \|B(a,b)\|_{H^2}
 &\le C\|a\|_{H^3}\|b\|_{H^3},
\end{aligned}
\tag{2.3}
\]

where \(B(a,b)=P(a\cdot\nabla b)\).  Fixed norm-equivalence constants are
absorbed into the symbols \(C_j\) below.

For a smooth solution of (1.1), the \(H^1\) estimate is

\[
 {1\over2}{d\over dt}|u|_1^2+|u|_2^2
 \le C_1|u|_1^{3/2}|u|_2^{3/2}.
 \tag{2.4}
\]

At level two, duality between one and three derivatives, (2.3), and (2.2)
give

\[
\begin{aligned}
 {1\over2}{d\over dt}|u|_2^2+|u|_3^2
 &\le \|B(u,u)\|_{H^1}|u|_3\\
 &\le C_2|u|_2^2|u|_3\\
 &\le C_2|u|_1|u|_3^2.
\end{aligned}
\tag{2.5}
\]

Similarly, at level three,

\[
\begin{aligned}
 {1\over2}{d\over dt}|u|_3^2+|u|_4^2
 &\le \|B(u,u)\|_{H^2}|u|_4\\
 &\le C_3|u|_3^2|u|_4\\
 &\le C_3|u|_2|u|_4^2.
\end{aligned}
\tag{2.6}
\]

The estimates extend from smooth solutions to (1.2) by the usual Galerkin
approximation or positive-time smoothing and limiting argument.

## 3. The global orbit eventually enters a small \(H^1\) ball

The energy equality and Poincare inequality yield

\[
 {1\over2}\|u(t)\|_2^2
 +\int_0^t|u(s)|_1^2\,ds
 ={1\over2}\|u(0)\|_2^2,
 \tag{3.1}
\]

and therefore

\[
 \int_0^\infty|u(s)|_1^2\,ds<\infty.
 \tag{3.2}
\]

Young's inequality in (2.4) gives a constant \(K_1\) such that

\[
 {1\over2}{d\over dt}|u|_1^2
 +{1\over2}|u|_2^2
 \le K_1|u|_1^6.
 \tag{3.3}
\]

Choose \(\eta>0\) so small that

\[
 K_1\eta^4\le{1\over4},
 \qquad
 C_2\eta\le{1\over2}.
 \tag{3.4}
\]

By (3.2), there exists \(T_1\) with \(|u(T_1)|_1<\eta\).  On any interval
where \(|u|_1\le\eta\), (3.3), (3.4), and \(|u|_2\ge|u|_1\) imply

\[
 {1\over2}{d\over dt}|u|_1^2
 +{1\over4}|u|_2^2\le0.
 \tag{3.5}
\]

The inequality strictly preserves the ball, so the usual continuity
bootstrap makes (3.5) valid for every \(t\ge T_1\).  In particular,
\(|u(t)|_1\) decays exponentially.

## 4. Decay climbs from \(H^1\) to \(H^3\)

Since \(C_2|u(t)|_1\le1/2\) for \(t\ge T_1\), (2.5) gives

\[
 {1\over2}{d\over dt}|u|_2^2
 +{1\over2}|u|_3^2\le0.
 \tag{4.1}
\]

Poincare therefore makes \(|u(t)|_2\) exponentially decreasing.  Choose
\(T_2\ge T_1\) so large that

\[
 C_3|u(T_2)|_2\le{1\over2}.
 \tag{4.2}
\]

The monotonicity supplied by (4.1) preserves (4.2).  Equation (2.6) then
gives, for every \(t\ge T_2\),

\[
 {1\over2}{d\over dt}|u|_3^2
 +{1\over2}|u|_4^2\le0.
 \tag{4.3}
\]

Thus \(|u(t)|_3\) also decreases exponentially.

## 5. The accumulated \(H^4\) action is finite

Put \(Q(t)=|u(t)|_3^2\) and \(W(t)=|u(t)|_4^2\).  After multiplying (4.3)
by two,

\[
 Q'(t)+W(t)\le0,
 \qquad W(t)\ge Q(t),
 \quad t\ge T_2.
 \tag{5.1}
\]

Fix \(0<\alpha<1\).  Multiplication by
\(e^{\alpha(t-T_2)}\) yields

\[
 {d\over dt}\left(e^{\alpha(t-T_2)}Q(t)\right)
 +(1-\alpha)e^{\alpha(t-T_2)}W(t)\le0.
 \tag{5.2}
\]

Consequently,

\[
 \int_{T_2}^\infty e^{\alpha(t-T_2)}|u(t)|_4^2\,dt
 \le {Q(T_2)\over1-\alpha}.
 \tag{5.3}
\]

Weighted Cauchy--Schwarz gives the explicit finite tail bound

\[
\begin{aligned}
 \int_{T_2}^\infty|u(t)|_4\,dt
 &\le
 \left(\int_0^\infty e^{-\alpha s}\,ds\right)^{1/2}
 \left(\int_{T_2}^\infty
 e^{\alpha(t-T_2)}|u(t)|_4^2\,dt\right)^{1/2}\\
 &\le { |u(T_2)|_3\over\sqrt{\alpha(1-\alpha)}}.
\end{aligned}
\tag{5.4}
\]

On the finite interval \([0,T_2]\), assumption (1.2) and
Cauchy--Schwarz give

\[
 \int_0^{T_2}|u(t)|_4\,dt
 \le T_2^{1/2}
 \left(\int_0^{T_2}|u(t)|_4^2\,dt\right)^{1/2}<\infty.
 \tag{5.5}
\]

Equations (5.4)--(5.5) prove (1.3).

## 6. The perturbation inequality around the complete orbit

Fix \(t_0\ge0\).  Let \(v\) be the maximal local \(H^3\) strong solution
from \(v(t_0)\), and set \(w=v-u\).  Then

\[
 \partial_tw+Aw+B(u,w)+B(w,u)+B(w,w)=0.
 \tag{6.1}
\]

Set

\[
 X(t)=|w(t)|_3^2,
 \qquad
 Y(t)=|w(t)|_4^2.
 \tag{6.2}
\]

To expose the endpoint derivative count, first work with smooth fields and
write \(\Lambda^3\) for any equivalent periodic order-three multiplier.  The
leading term in the first transport contribution cancels:

\[
 \langle u\cdot\nabla\Lambda^3w,\Lambda^3w\rangle=0.
 \tag{6.3}
\]

The remaining commutator and product terms obey

\[
\begin{aligned}
 |\langle[\Lambda^3,u\cdot\nabla]w,\Lambda^3w\rangle|
 &\le C\|u\|_{H^3}\|w\|_{H^3}^2,\\
 |\langle\Lambda^3(w\cdot\nabla u),\Lambda^3w\rangle|
 &\le C\|u\|_{H^4}\|w\|_{H^3}^2,\\
 |\langle\Lambda^3(w\cdot\nabla w),\Lambda^3w\rangle|
 &\le C\|w\|_{H^3}^3.
\end{aligned}
\tag{6.4}
\]

These are the standard periodic commutator/Moser estimates; the first line
uses the transport cancellation rather than an unavailable \(H^4\) norm of
\(w\).  Mean-zero norm equivalence, Poincare, and \(X\le Y\) now give a
universal \(C_*\ge1\) such that, a.e. on the local strong-solution interval,

\[
 {1\over2}X'(t)+Y(t)
 \le C_*|u(t)|_4X(t)+C_*X(t)^{1/2}Y(t).
 \tag{6.5}
\]

The local regularity of \(u,w\) justifies the same inequalities by smoothing
or Galerkin approximation.  No finite-dimensional approximation enters the
statement, and no spectral assumption or explicit formula for \(u\) appears
in (6.5).

## 7. Uniform bootstrap, continuation, and exponential convergence

Work on the maximal interval on which

\[
 X(t)^{1/2}\le {1\over2C_*}.
 \tag{7.1}
\]

Equation (6.5) then implies

\[
 X'(t)+Y(t)
 \le2C_*|u(t)|_4X(t).
 \tag{7.2}
\]

Dropping \(Y\) and using

\[
 \int_{t_0}^t|u(s)|_4\,ds\le\mathcal A_4[u]
 \tag{7.3}
\]

gives

\[
 X(t)^{1/2}
 \le e^{C_*\mathcal A_4[u]}X(t_0)^{1/2}.
 \tag{7.4}
\]

If (1.5) holds with (1.4), then the right-hand side is strictly less than
\(1/(4C_*)\), which is a strict improvement of (7.1).  The bootstrap cannot
terminate.

Since \(Y\ge X\), retaining the dissipative term in (7.2) gives

\[
 X'(t)
 \le\left(2C_*|u(t)|_4-1\right)X(t).
 \tag{7.5}
\]

Integration proves exactly (1.6).  In particular \(w\) is bounded in
\(H^3\) on every finite interval.  The reference solution is also bounded
in \(H^3\) on every finite interval, so

\[
 |v(t)|_3\le|u(t)|_3+|w(t)|_3
 \tag{7.6}
\]

cannot blow up at the maximal endpoint.  The standard \(H^3\) continuation
alternative makes \(v\) global.  Because the bound (7.3) uses the complete
action rather than a particular tail, the same radius works for every
starting time \(t_0\ge0\).

## 8. Topological and route-exclusion corollaries

Let

\[
 \mathcal G_3
 =\{u_0\in H^3_{\sigma,0}:
 u_0\hbox{ generates a global strong solution}\}.
 \tag{8.1}
\]

Taking \(t_0=0\) in the theorem shows that every point of \(\mathcal G_3\)
has a positive \(H^3\) ball contained in \(\mathcal G_3\).  Hence
\(\mathcal G_3\) is open.  Its complement, if nonempty, is closed.

For every \(\epsilon>0\), (1.6) and norm equivalence provide a positive
\(\delta(u,\epsilon)\) such that

\[
 \|v(t_0)-u(t_0)\|_{H^3}<\delta(u,\epsilon)
 \Longrightarrow
 \sup_{t\ge t_0}\|v(t)-u(t)\|_{H^3}<\epsilon.
 \tag{8.2}
\]

This is full-three-dimensional forward synchronized
\((H^3,H^3)\) stability.  It implies the custom
\(H^3\)-input/\(L^2\)-output corollary because
\(\|z\|_2\le\|z\|_{H^3}\).  It does not prove full-three-dimensional FPS
\((H^3,L^2)\), which would require global \(H^3\) continuation for data
small only in \(L^2\) and possibly arbitrarily large in \(H^3\).

Therefore an \(H^3\)-small fixed-background Lyapunov-instability search
cannot succeed around any reference trajectory already known to satisfy
(1.2).  This closes that route inside the unforced periodic equation.  It
does not decide whether every smooth reference trajectory satisfies (1.2),
which is precisely where the Clay problem remains.

## 9. What the theorem does not say

The proof uses the global reference orbit twice: first to reach a late
small \(H^1\) state, and second to guarantee the finite-interval
\(L^2H^4\) regularity needed in (5.5).  It cannot be used as an a priori
continuation argument for an arbitrary local trajectory without already
knowing that the reference survives to the entry time.

The theorem also does not cover nonzero forcing.  A nondecaying forced
equilibrium can have

\[
 \int_0^\infty\|u(t)\|_{H^4}\,dt=\infty,
\]

so the action mechanism above gives no positive all-time radius.  This is
consistent with autonomous spectral-instability theorems for forced steady
flows, but those theorems concern a different equation from (1.1).
