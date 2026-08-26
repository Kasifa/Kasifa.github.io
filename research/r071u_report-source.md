# R0.71U -- A second-time-jet theorem sums global-shell entries, while an exact 2.5D NSE family realizes arbitrary finite recurrence

**Date:** 2026-08-26

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, Littlewood--Paley shell observables, temporal zero
sampling, occupation measures, and recurrence packing

**Status:** release source.  This report proves a zero-count-independent
Hilbert-valued sampling lemma and applies it to all positive global-shell
entries on a compact classical interval.  The resulting estimate is exactly
scale matched.  Its first row is controlled by the normalized Leray--Lamb
ledger after an inverse-window factor; its second row contains a genuine
second-time-jet recurrence tax.  The report also constructs, inside an exact
globally smooth 2.5D invariant class of the unforced three-dimensional NSE,
solutions with any prescribed finite set of simple positive entries of one
fixed compact annular multiplier.  Initial energy and enstrophy can remain
uniformly bounded as the number of entries grows.  The construction rules out
a uniform raw-count bound on that bounded energy--enstrophy class, but its
weighted atoms may tend
to zero and therefore do not disprove the second-jet theorem or an unknown
weighted Leray-level packing law.  No weak-solution trace theorem,
continuation criterion, singularity, global regularity, novelty, or priority
claim is made.

## 0. Direct decision

R0.71T left two possibilities for the scale-zero global-shell jet

\[
 q^{\rm jet}_{j,\beta}
 =\kappa_j^{-6}
 \frac{\|C_{j,t}(t_\beta)\|_2^2}{Y(t_\beta)}:
 \tag{0.1}
\]

either a summed estimate exists, or temporal recurrence defeats it.  R0.71U
shows that both statements need qualification.

First, there is a true summed theorem.  If \(K\) is a compact classical time
interval of length \(\ell\), then every finite shell family satisfies

\[
\boxed{
\begin{aligned}
 \sum_{j,\,t_\beta\in K}J_{j,\beta}
 \le C_{\rm ann}\mathcal R_Y(K)
 \Bigg[&\frac2\ell
 \int_K\frac1Y\sum_j\kappa_j^{-6}
 \|C_{j,t}\|_2^2\,dt\\
 &+\frac{7\ell}{3}
 \int_K\frac1Y\sum_j\kappa_j^{-6}
 \|C_{j,tt}\|_2^2\,dt\Bigg],
\end{aligned}}
 \tag{0.2}
\]

where \(J_{j,\beta}=\kappa_j^{-2}A_{j,+}(t_\beta)\) and

\[
 \mathcal R_Y(K)=\frac{\sup_KY}{\inf_KY}.
 \tag{0.3}
\]

The constant in (0.2) is independent of the number of zeros and their minimum
separation.  The proof is one-dimensional but Hilbert valued.  Consecutive
zeros make the mean of \(C_{j,t}\) vanish on every intervening gap, so all but
one sample can be charged to \(C_{j,tt}\) on disjoint intervals.  No
vector-valued Rolle theorem is used.

The first row of (0.2) obeys

\[
 \sum_j\kappa_j^{-6}\|C_{j,t}\|_2^2
 \lesssim \nu^2Y+\|L\|_{\dot H^{-1}}^2.
 \tag{0.4}
\]

The second row obeys only the stronger classical estimate

\[
 \sum_j\kappa_j^{-6}\|C_{j,tt}\|_2^2
 \lesssim \nu^2\|\omega_t\|_2^2
 +\|L_t\|_{\dot H^{-1}}^2.
 \tag{0.5}
\]

Thus (0.2) is a trajectory-wise theorem for classical solutions satisfying
the displayed positive enstrophy-floor hypothesis, but not a Leray-level
closure.  The two rows have the correct NSE scaling: the inverse
window in the first row and the direct window in the second are not optional
dimensional decorations.

Second, recurrence is genuinely present in the NSE.  For every integer
\(N\ge1\) and every

\[
 0<t_1<\cdots<t_N<T,
 \tag{0.6}
\]

there is a globally smooth unforced periodic solution in the invariant class

\[
 u(x,y,z,t)=(f(y,z,t),0,v(y,t))
 \tag{0.7}
\]

for which the same declared compact annular projection vanishes simply and
positively at all \(t_m\).  A modular Fourier support condition makes the
target annulus contain only one conjugate mode pair of this solution, so the
construction zeros the complete declared shell, not merely one coordinate.
The initial energy and enstrophy can be bounded independently of \(N\).

This proves that raw entry count and minimum separation have no uniform bound
on the class
\(\{\|u_0\|_2^2\le1,\ \|\omega_0\|_2^2\le1\}\).  It does not contradict
(0.2).  Along the small
implicit-function curve, each atom has the expansion

\[
 J_{j,m}(s)=c_{j,m}s^2+O(s^3),\qquad c_{j,m}>0,
 \tag{0.8}
\]

and the constants and admissible parameter radius may deteriorate with
\(N\).  The remaining question is therefore weighted recurrence, not raw
recurrence.

## 1. Global-shell setting and the jet atom

Work on the normalized three-torus.  Let \(u\) be a nontrivial zero-mean
classical solution on an open interval containing a compact interval
\(K=[a,b]\), and write

\[
 \omega=\operatorname{curl}u,
 \qquad
 Y=\|\omega\|_2^2,
 \qquad
 L=\mathbb P(u\times\omega).
 \tag{1.1}
\]

Let \(T_j\) be real-even, time-independent annular Fourier multipliers with
nominal frequencies \(\kappa_j\), and put

\[
 W_j=T_j\omega,
 \qquad
 F_j=T_jL,
 \qquad
 C_j=\operatorname{curl}W_j.
 \tag{1.2}
\]

Assume that the nonzero symbol of every multiplier lies in

\[
 c_0\kappa_j\le |k|\le c_1\kappa_j,
 \qquad 0<c_0<c_1<\infty,
 \tag{1.3}
\]

and that the declared family has the upper square-function bound

\[
 \sum_j\kappa_j^{-2}\|T_jh\|_2^2
 \le C_T\|h\|_{\dot H^{-1}}^2.
 \tag{1.4}
\]

At a global root \(C_j(t_*)=0\), annular support, zero mean, and
incompressibility give \(W_j(t_*)=0\), equivalently \(T_ju(t_*)=0\).  The
filtered velocity equation then gives

\[
 \boxed{C_{j,t}(t_*)=-\Delta F_j(t_*).}
 \tag{1.5}
\]

If the right entry atom is positive, R0.71T showed that the zero must be
first order.  Its exact value is

\[
 A_{j,+}(t_*)
 =\frac{\|\nabla F_j(t_*)\|_2^4}
 {Y(t_*)\|\Delta F_j(t_*)\|_2^2},
 \qquad A_{j,-}(t_*)=0.
 \tag{1.6}
\]

Define

\[
 J_j(t_*)=\kappa_j^{-2}A_{j,+}(t_*).
 \tag{1.7}
\]

The Cauchy inequality

\[
 \|\nabla F_j\|_2^4
 \le \|F_j\|_2^2\|\Delta F_j\|_2^2
 \tag{1.8}
\]

and the lower annular radius give

\[
\boxed{
 J_j(t_*)
 \le \kappa_j^{-2}\frac{\|F_j(t_*)\|_2^2}{Y(t_*)}
 \le c_0^{-4}\kappa_j^{-6}
 \frac{\|C_{j,t}(t_*)\|_2^2}{Y(t_*)}.}
 \tag{1.9}
\]

The reverse comparison also holds with a constant depending only on
\(c_0,c_1\).  On one Laplace eigenshell \(|k|=\rho_j\),

\[
 J_j(t_*)
 =\kappa_j^{-2}\rho_j^{-4}
 \frac{\|C_{j,t}(t_*)\|_2^2}{Y(t_*)}.
 \tag{1.10}
\]

For the R0.71T normalization \(\rho_j^2=2\kappa_j^2\), the coefficient is
\(1/4\).

At one fixed time, (1.8) and (1.4) already give the pointwise batching

\[
\boxed{
 \sum_{j:t\in Z_j^+}J_j(t)
 \le C_T\frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)}.}
 \tag{1.11}
\]

The remaining issue is sampling at distinct times.

## 2. A zero-count-independent Hilbert sampling lemma

The key estimate does not require analyticity or zero separation.

### Lemma 2.1 -- first derivatives at vector zeros

Let \(H\) be a real or complex Hilbert space, let \(I=(a,b)\) have length
\(\ell=b-a\), and let \(X\in H^2(I;H)\).  For any finite ordered set

\[
 a\le t_1<\cdots<t_N\le b,
 \qquad X(t_k)=0,
 \tag{2.1}
\]

one has

\[
\boxed{
 \sum_{k=1}^N\|X'(t_k)\|_H^2
 \le \frac2\ell\int_I\|X'\|_H^2\,dt
 +\frac{7\ell}{3}\int_I\|X''\|_H^2\,dt.}
 \tag{2.2}
\]

Endpoint values in (2.1) are the canonical (H^2) traces.

The interval length in (2.2) is the length of the audited time window.  It is
not the minimum zero spacing, a Voronoi radius, or an assumed forward window.

#### Proof

Put \(V=X'\).  The elementary Hilbert-valued point trace gives, at the first
zero,

\[
 \|V(t_1)\|_H^2
 \le \frac2\ell\int_I\|V\|_H^2
 +2\ell\int_I\|V'\|_H^2.
 \tag{2.3}
\]

For \(k\ge2\), set \(I_k=(t_{k-1},t_k)\) and
\(\ell_k=t_k-t_{k-1}\).  Since both endpoints are zeros,

\[
 \int_{I_k}V(t)\,dt=0.
 \tag{2.4}
\]

Consequently,

\[
 V(t_k)=\frac1{\ell_k}
 \int_{t_{k-1}}^{t_k}(s-t_{k-1})V'(s)\,ds.
 \tag{2.5}
\]

Cauchy--Schwarz yields

\[
 \|V(t_k)\|_H^2
 \le\frac{\ell_k}{3}\int_{I_k}\|V'\|_H^2\,dt.
 \tag{2.6}
\]

The gaps \(I_k\) are disjoint and \(\ell_k\le\ell\).  Summing (2.6) and
adding (2.3) proves (2.2).  The proof uses only the Bochner integral and
Cauchy--Schwarz.  In particular, it does not invoke a false vector-valued
Rolle theorem. \(\square\)

The same estimate applies to any finite subset of an infinite zero set.
Monotone convergence therefore gives the corresponding extended sum whenever
the right side is finite.

## 3. The all-shell second-time-jet theorem

Let \(Z_j^+(K)\) denote the positive global-shell roots in \(K\), and define

\[
 \mu_{J,\Lambda}(K)
 =\sum_{j\in\Lambda}
 \sum_{t_*\in Z_j^+(K)}J_j(t_*)
 \tag{3.1}
\]

for a finite shell family \(\Lambda\).

### Theorem 3.1 -- finite/all-shell second-jet packing

Assume \(0<\inf_KY\le\sup_KY<\infty\).  Then

\[
\boxed{
\begin{aligned}
 \mu_{J,\Lambda}(K)
 \le c_0^{-4}\mathcal R_Y(K)
 \Bigg[&\frac2\ell
 \int_K\frac1Y
 \sum_{j\in\Lambda}\kappa_j^{-6}\|C_{j,t}\|_2^2\,dt\\
 &+\frac{7\ell}{3}
 \int_K\frac1Y
 \sum_{j\in\Lambda}\kappa_j^{-6}\|C_{j,tt}\|_2^2\,dt
 \Bigg].
\end{aligned}}
 \tag{3.2}
\]

#### Proof

Apply Lemma 2.1 to each \(X=C_j\), multiply by \(\kappa_j^{-6}\),
and use (1.9).  At a sample time,

\[
 \frac1{Y(t_*)}\le\frac1{\inf_KY}.
 \tag{3.3}
\]

For every nonnegative integrand \(h\),

\[
 \frac1{\inf_KY}\int_Kh(t)\,dt
 \le \mathcal R_Y(K)\int_K\frac{h(t)}{Y(t)}\,dt.
 \tag{3.4}
\]

Summing over \(j\) proves (3.2). \(\square\)

The constant is independent of the number of entries, the smallest distance
between them, and the finite shell truncation.  If the full right side is
finite, monotone convergence gives the countable-shell form.  For a smooth
solution on \(K\), the frame estimates below make that right side finite.

Theorem 3.1 applies on every compact subinterval \(J\) of the classical
interval, with \(\ell=|J|\).  This is a local second-jet packing theorem.  It
is not a classical \(|J|\)-Carleson estimate because the first row contains
\(|J|^{-1}\) and the second row contains a stronger time derivative.

## 4. NSE payment ledger and scaling

For the global observable,

\[
 C_j=-\Delta T_ju,
 \qquad
 C_{j,t}=-\Delta T_ju_t,
 \qquad
 C_{j,tt}=-\Delta T_ju_{tt}.
 \tag{4.1}
\]

The annular Bernstein bound and (1.4) imply

\[
 \sum_j\kappa_j^{-6}\|C_{j,t}\|_2^2
 \le C_{\rm ann,T}\|u_t\|_{\dot H^{-1}}^2.
 \tag{4.2}
\]

Since

\[
 u_t=\nu\Delta u+L,
 \tag{4.3}
\]

one has

\[
\boxed{
 \sum_j\kappa_j^{-6}\|C_{j,t}\|_2^2
 \le 2C_{\rm ann,T}
 \left(\nu^2Y+\|L\|_{\dot H^{-1}}^2\right).}
 \tag{4.4}
\]

This is the Leray-level row.  After division by \(Y\), its time integral is
controlled by

\[
 \nu^2|K|+
 \int_K\frac{\|L\|_{\dot H^{-1}}^2}{Y}\,dt.
 \tag{4.5}
\]

The inverse factor \(|K|^{-1}\) in (3.2) pays the trace of the first entry in
each shell.  R0.71T's scaling family does not contradict this term: under
parabolic dilation \(|K|^{-1}\) supplies exactly the two powers missing from
the bare time integral.

Differentiating once more gives

\[
 u_{tt}=\nu\Delta u_t+L_t
 \tag{4.6}
\]

and hence

\[
\boxed{
 \sum_j\kappa_j^{-6}\|C_{j,tt}\|_2^2
 \le 2C_{\rm ann,T}
 \left(\nu^2\|\omega_t\|_2^2
 +\|L_t\|_{\dot H^{-1}}^2\right).}
 \tag{4.7}
\]

Combining (3.2), (4.4), and (4.7) yields

\[
\boxed{
\begin{aligned}
 \mu_J(K)\lesssim \mathcal R_Y(K)
 \Bigg[&\frac1{|K|}
 \int_K\left(\nu^2+
 \frac{\|L\|_{\dot H^{-1}}^2}{Y}\right)dt\\
 &+|K|\int_K
 \frac{\nu^2\|\omega_t\|_2^2
 +\|L_t\|_{\dot H^{-1}}^2}{Y}\,dt\Bigg].
\end{aligned}}
 \tag{4.8}
\]

The second row is the recurrence tax.  It is finite for a classical solution
but is not controlled by the Leray energy inequality.

Under the exact torus dilation, with integer \(\lambda\ge1\), covariantly
transported time window and multiplier,

\[
 u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t),
 \tag{4.9}
\]

the four quantities

\[
 J_j,qquad
 |K|^{-1}\int_K\kappa_j^{-6}\frac{\|C_{j,t}\|_2^2}{Y},
 \qquad
 |K|\int_K\kappa_j^{-6}\frac{\|C_{j,tt}\|_2^2}{Y},
 \qquad
 \mathcal R_Y(K)
 \tag{4.10}
\]

all have total scale exponent zero.  For a fixed dyadic frame one takes
\(\lambda=2^m\).  The theorem is not rescued by a dimensionally incorrect
norm.

## 5. Why the second-time jet cannot be deleted abstractly

Let \(e\) be a divergence-free Laplace eigenmode with \(-\Delta e=e\), and
on a fixed interval put

\[
 C_N(t)=N^{-1}\sin(Nt)e,
 \qquad
 F_N(t)=C_{N,t}(t)+\nu C_N(t).
 \tag{5.1}
\]

Then

\[
 C_{N,t}-\nu\Delta C_N=-\Delta F_N.
 \tag{5.2}
\]

At every zero, \(F_N=C_{N,t}=\pm e\), so the jet atom is bounded below by a
fixed positive constant.  The number of zeros grows like \(N\), while

\[
 \int\|C_{N,t}\|_2^2dt=O(1),
 \qquad
 \int\|F_N\|_2^2dt=O(1),
 \tag{5.3}
\]

and

\[
 \int\|C_{N,tt}\|_2^2dt=O(N^2).
 \tag{5.4}
\]

Thus the exact forced shell equation and a first-jet time integral alone do
not imply temporal sampling.  This is an analytic forced-path method test,
not an NSE trajectory.  Section 6 supplies the genuine NSE recurrence result,
but with shrinking atom sizes.

## 6. An exact 2.5D NSE recurrence class

Use coordinates \((x,y,z)\) and consider

\[
 u(x,y,z,t)=(f(y,z,t),0,v(y,t)).
 \tag{6.1}
\]

Then

\[
 \operatorname{div}u=0,
 \qquad
 (u\cdot\nabla)u=(v f_z,0,0).
 \tag{6.2}
\]

The nonlinear vector in (6.2) is divergence free.  With constant pressure,
the unforced three-dimensional NSE is therefore exactly equivalent in this
class to

\[
\boxed{
 v_t=\nu v_{yy},
 \qquad
 f_t+v f_z=\nu(f_{yy}+f_{zz}).}
 \tag{6.3}
\]

The first equation is a finite Fourier heat flow below.  The second is a
linear uniformly parabolic equation with a smooth divergence-free drift.
Every finite Fourier datum used here therefore generates a global smooth
three-dimensional NSE solution.  The passive-scalar form is an exact
invariant subclass, not an externally forced surrogate.

The standard 2D3C reduction is recorded explicitly in
[Linkmann--Buzzicotti--Biferale (2018)](https://doi.org/10.1140/epje/i2018-11612-1).
That source does not state the prescribed-zero theorem proved below.

## 7. Arbitrary prescribed finite recurrence

Fix integers \(K>0\), \(L\ne0\), a compactly supported real-even annular
multiplier \(T_*\), and

\[
 k_*=(0,K,L),
 \qquad m_*=m_*(k_*)\ne0.
 \tag{7.1}
\]

Let \(R_*\) be the largest frequency radius on which the symbol is nonzero.
Choose an integer

\[
 d>R_*+|K|
 \tag{7.2}
\]

and distinct positive integers \(M_1,\ldots,M_{2N+1}\).  Put

\[
 n_\ell=dM_\ell>K.
 \tag{7.3}
\]

All parameters below are real.  Define

\[
 v_p(y,t)=\sum_{\ell=1}^{2N+1}
 \left(p_\ell e^{-\nu n_\ell^2t}e^{in_\ell y}
 +p_\ell e^{-\nu n_\ell^2t}e^{-in_\ell y}\right),
 \tag{7.4}
\]

and take

\[
 f_0(y,z)=\sum_{\ell=1}^{2N+1}
 \left(A_\ell e^{i((K-n_\ell)y+Lz)}
 +\overline{A_\ell}e^{-i((K-n_\ell)y+Lz)}\right),
 \tag{7.5}
\]

where

\[
 A_\ell=i\quad(1\le\ell\le N+1),
 \qquad
 A_\ell=1\quad(N+2\le\ell\le2N+1).
 \tag{7.6}
\]

Let \(f_p\) be the solution of (6.3), and define the target coefficient

\[
 a_p(t)=\widehat f_p(K,L,t).
 \tag{7.7}
\]

### Lemma 7.1 -- exact parameter derivative

Let

\[
 \mu=\nu(K^2+L^2),
 \qquad
 \beta_\ell=2\nu n_\ell(n_\ell-K)>0.
 \tag{7.8}
\]

Then \(a_0(t)=0\) and

\[
\boxed{
 D_{p_\ell}a_p(t)\big|_{p=0}
 =-iLA_\ell\phi_\ell(t),
 \qquad
 \phi_\ell(t)=e^{-\mu t}
 \frac{1-e^{-\beta_\ell t}}{\beta_\ell}.}
 \tag{7.9}
\]

Indeed, the positive shear mode \(n_\ell\) and the initial scalar mode
\((K-n_\ell,L)\) are the unique first-order pair that convolves to
\((K,L)\).  Duhamel's formula gives (7.9).

### Lemma 7.2 -- the response functions form a T-system

For distinct positive \(\beta_1,\ldots,\beta_M\), every nonzero combination
of

\[
 \phi_\ell(t)=e^{-\mu t}(1-e^{-\beta_\ell t})/\beta_\ell
 \tag{7.10}
\]

has at most \(M-1\) positive zeros, counted with multiplicity.

To see this, remove the nonzero factor \(e^{-\mu t}\) and write

\[
 h(t)=\sum_{\ell=1}^M c_\ell
 \frac{1-e^{-\beta_\ell t}}{\beta_\ell}.
 \tag{7.11}
\]

Here \(h(0)=0\) and

\[
 h'(t)=\sum_{\ell=1}^M c_\ell e^{-\beta_\ell t}.
 \tag{7.12}
\]

The exponentials form an extended Chebyshev system; the usual induction by
Rolle after multiplication by one exponential shows that (7.12) has at most
\(M-1\) real zeros.  If (7.11) had \(M\) positive zeros, its additional zero
at the origin would force at least \(M\) zeros of (7.12), a contradiction.

### Theorem 7.3 -- arbitrary finite exact NSE recurrence

For every

\[
 0<t_1<\cdots<t_N<T,
 \tag{7.13}
\]

there is \(s_0>0\) and a smooth curve

\[
 p:(-s_0,s_0)\to\mathbb R^{2N+1},
 \qquad p(0)=0,
 \qquad p'(0)\ne0,
 \tag{7.14}
\]

such that

\[
\boxed{T_*u_{p(s)}(t_m)=0
 \quad\text{for }m=1,\ldots,N.}
 \tag{7.15}
\]

For every sufficiently small \(s\ne0\), all these roots are first order and
have positive right-entry atoms.

#### Proof

Define

\[
 H(p)=\big(\operatorname{Re}a_p(t_m),
 \operatorname{Im}a_p(t_m)\big)_{m=1}^N
 \in\mathbb R^{2N}.
 \tag{7.16}
\]

The first \(N+1\) parameter columns in \(DH(0)\) are real because
\(-iA_\ell=1\); the last \(N\) columns are imaginary because
\(-iA_\ell=-i\).  Lemma 7.2 makes every \(N\)-column evaluation matrix at
the times (7.13) invertible.  After fixing \(p_1=s\), the derivative of
\(H\) with respect to \((p_2,\ldots,p_{2N+1})\) is therefore an invertible
\(2N\)-by-\(2N\) real matrix.  The ordinary finite-dimensional implicit
function theorem gives (7.14) and exact equations \(H(p(s))=0\).

Let \(c=p'(0)\).  The last \(N\) entries of \(c\) vanish, while

\[
 g(t)=L\sum_{\ell=1}^{N+1}c_\ell\phi_\ell(t)
 \tag{7.17}
\]

vanishes at all \(t_m\).  It is a nonzero combination of \(N+1\) T-system
elements and already has \(N\) positive zeros.  Lemma 7.2 shows that every
one is simple.  Smooth parameter dependence in \(C_t^1\) gives

\[
 a_{p(s)}(t)=s g(t)+O(s^2),
 \qquad
 \partial_ta_{p(s)}(t_m)=s g'(t_m)+O(s^2)\ne0.
 \tag{7.18}
\]

It remains to check the complete annulus rather than one coefficient.  The
modular support is invariant:

\[
\begin{aligned}
 \operatorname{supp}\widehat u(t)\subset{}&
 \{(0,K+dr,L):r\in\mathbb Z\}\\
 &\cup\{(0,-K+dr,-L):r\in\mathbb Z\}\\
 &\cup\{(0,dr,0):r\in\mathbb Z\}.
\end{aligned}
 \tag{7.19}
\]

Multiplication by \(v\) only shifts the \(y\)-frequency by \(d\mathbb Z\)
and never changes the \(z\)-frequency.  Condition (7.2) makes the
intersection of (7.19) with the multiplier support equal to
\(\{k_*,-k_*\}\).  Thus \(a_p(t_m)=0\) zeros the entire declared annulus.

At such a root,

\[
 C_{*,t}=-\Delta F_*=\rho^2F_*,
 \qquad \rho^2=K^2+L^2.
 \tag{7.20}
\]

Equation (7.18) makes \(F_*\ne0\), and hence

\[
 \langle F_*,C_{*,t}\rangle
 =\rho^2\|F_*\|_2^2>0.
 \tag{7.21}
\]

Each prescribed root is therefore a simple positive global-shell entry.
\(\square\)

If the multiplier has a noncompact Fourier tail, modular isolation produces
only a small tail, not an exact shell zero.  Compact annular support is an
essential hypothesis of Theorem 7.3.

## 8. Uniform energy/enstrophy and shrinking atom mass

Multiply every \(A_\ell\) in (7.5) by an arbitrary positive amplitude
\(\varepsilon_N\).  Because (6.3) is linear in \(f\) for fixed \(v\), the
zero map is multiplied by \(\varepsilon_N\) and its zero manifold is
unchanged.  Choose \(\varepsilon_N\) so that the initial scalar contribution
to energy and enstrophy is at most \(1/2\).  Then choose a sufficiently small
nonzero point on the implicit curve so that the initial shear contribution is
also at most \(1/2\).  This gives

\[
 \|u_0\|_2^2\le1,
 \qquad
 \|\omega_0\|_2^2\le1,
 \tag{8.1}
\]

while retaining at least \(N\) prescribed positive entries.  Therefore the
raw global-shell entry count is unbounded on the unit energy--enstrophy ball,
uniformly over smooth solutions and declared compact annuli.  This statement
does not claim that the actual numerical pair
\((\|u_0\|_2^2,\|\omega_0\|_2^2)\), which varies with \(N\) here, determines no
possible nonuniform function.

This is not a weighted-atom counterexample.  With normalized torus Parseval,

\[
 \|F_*(t_m)\|_2^2
 =2|m_*|^2|\partial_ta_{p(s)}(t_m)|^2,
 \tag{8.2}
\]

and hence, with \(g\) and \(Y_0\) understood after the chosen
\(\varepsilon_N\) rescaling,

\[
\boxed{
 J_{*,m}(s)
 =\frac{2|m_*|^2|g'(t_m)|^2}
 {\kappa_*^2Y_0(t_m)}s^2+O(s^3)>0.}
 \tag{8.3}
\]

The admissible \(s\), the interpolation slopes, and the scalar amplitude may
all decay with \(N\).  Theorem 7.3 defeats raw counting, uniform separation,
and generic-transversality arguments.  It leaves open a uniform estimate for
the weighted sum in (3.2).

## 9. Outgoing occupation

Every positive global-shell root in this report is first order.  R0.71T's
outgoing-coarea identity therefore represents the same measure

\[
 \mu_J=\sum_{j,\beta}J_{j,\beta}\delta_{t_\beta}.
 \tag{9.1}
\]

Combining that identity with Theorem 3.1 gives a summed bound for its
zero-level limit whenever the second-jet right side is finite.  It does not
provide a \(\delta\)-uniform pointwise domination of
\(\rho_\delta(\|C_j\|)(\|C_j\|_t)_+\) by a Leray density.  Standard coarea,
Banach indicatrix, and local-time results integrate crossing information over
the level.  A distinguished zero level can remain exceptional.

## 10. Clarification of the R0.71T target projection

R0.71T wrote the internal implicit-function construction using the exact
four-mode real-conjugate target projection \(P_*\).  In that formulation,
\(T_*\) must be understood as the corresponding exact thin annular
projection.  Four-mode cancellation alone would not zero an unrelated broad
multiplier containing additional active lattice modes.

The analytic construction extends to a full finite target support as follows.
Let \(S_j\) be every lattice mode on which a compact target multiplier is
nonzero, assume the seed shell is excluded, and let \(E_j\) be the complete
finite-dimensional real divergence-free velocity space on \(S_j\).  For the
support projection \(P_j\), define

\[
 \Phi(a,z)=P_jS_\tau(aU+z),
 \qquad z\in E_j.
 \tag{10.1}
\]

Then

\[
 D_z\Phi(0,0)=e^{\nu\tau\Delta}|_{E_j}
 \tag{10.2}
\]

is a diagonal invertible finite matrix.  The implicit-function theorem zeros
every target-support mode.  The leading quadratic correction remains on the
four forced modes; the remaining target components are higher-order
corrections.  Under compatible integer dilation, non-sublattice modes of the
scaled annulus vanish automatically, while sublattice modes correspond to
the base support.  This supplies the full-support version when the declared
annulus is separated from the seed shell.

The R0.71T source and public note are corrected in this release to state this
boundary explicitly.  The correction does not change its thin-shell theorem
or scaling no-go.

## 11. Primary-literature boundary

The checked literature supports the surrounding tools but not the complete
R0.71U theorem.

1. [Masuda (1967)](https://doi.org/10.3792/pja/1195521421),
   [Temam's monograph](https://ftp.mi.fu-berlin.de/pub/klima/NavierStokes/Temam-NavierStokesEquationsAndNonlinearFunctionalAnalysis.pdf),
   and the time-analyticity results used in R0.71Q make fixed finite-shell
   zeros trajectory-wise finite on compact classical intervals.  They give no
   energy-uniform count, separation, or jet sum.
2. [Linkmann--Buzzicotti--Biferale (2018)](https://doi.org/10.1140/epje/i2018-11612-1)
   records the exact 2D3C passive-component reduction.  The prescribed-time
   implicit-function construction is proved directly here; no novelty claim
   is inferred from the bounded search.
3. [Biferale--Buzzicotti--Linkmann (2017)](https://doi.org/10.1063/1.4990082)
   gives further 2D3C context, while the exponential evaluation matrices are
   standard Chebyshev-system interpolation in the sense of
   [Karlin--Studden](https://books.google.com/books?id=P7Y-AAAAIAAJ).  Neither
   source states the unforced prescribed-time construction used here.
4. [Agrachev--Sarychev (2005)](https://doi.org/10.1007/s00021-004-0110-1)
   and [Shirikyan (2007)](https://doi.org/10.1016/J.ANIHPC.2006.04.002)
   establish finite-dimensional projection controllability with external
   controls.  The present quantifiers are different: only initial data are
   selected, the evolution is unforced, and a new solution may depend on the
   prescribed finite time set.
5. [Koch--Tataru (2001)](https://math.berkeley.edu/~tataru/papers/nas.pdf)
   gives an upper parabolic Carleson norm for small critical data, not a lower
   mass attached to every zero.
6. [Banach's indicatrix theorem](https://doi.org/10.4064/fm-7-1-225-236),
   [Lochowski's generalization](https://doi.org/10.4064/cm6583-3-2017),
   and [Bertoin--Yor](https://doi.org/10.1112/blms/bdu014) control
   level-integrated crossings, truncated variation, or local time.  They do
   not bound a distinguished zero-level derivative sample.
7. [Hirsch](https://doi.org/10.1007/978-1-4684-9449-5) and
   [Smale](https://doi.org/10.2307/2373250) clarify a terminology boundary:
   for a one-dimensional time curve into a shell space of dimension greater
   than one, \(C_t\ne0\) is a first-order vector zero, not transversality to
   the point \(0\) in the differential-topology sense.
8. [CKN](https://doi.org/10.1002/cpa.3160350604) concerns suitable weak
   solutions, local energy, and singular sets.  It does not make
   \(C_t(t_\beta)\) or \(Y(t_\beta)\) well defined at an arbitrary weak zero
   time.

The bounded two-wave search located no deterministic NSE theorem that sums
the normalized derivative mass at a fixed zero level.  This is a scoped
negative finding, not a statement of nonexistence, originality, or priority.

## 12. Computational corroboration boundary

The formal figure uses the modular example

\[
 \nu=0.02,
 \quad K=L=1,
 \quad d=8,
 \quad N=3,
 \quad(t_1,t_2,t_3)=(0.01,0.03,0.07).
 \tag{12.1}
\]

It fixes \(p_1=0.002\), solves the remaining six real shooting equations,
and integrates the invariant Fourier lattice at several cutoffs.  The main
cutoff is 24 lattice steps and the independent refinement uses at least 30.
The three complex target residuals are below floating-point rounding scale,
the target derivatives are nonzero, and the refined cutoffs agree on the
reported slopes.  The computation is a reproducible illustration of the
analytic theorem.  It is not used to prove the infinite-dimensional
implicit-function result or the zero-sampling lemma.

## 13. Exact result boundary

### Proved in R0.71U

1. annular comparability between the positive global-shell atom and the
   scale-zero first-time jet;
2. unconditional same-time all-shell batching by the normalized
   \(\dot H^{-1}\)-Lamb square sum;
3. the Hilbert-valued zero-sampling lemma (2.2), with no zero-count or
   separation constant;
4. the finite and countable all-shell second-time-jet theorem (3.2) on
   compact classical intervals;
5. the Leray-level first-row ledger and the stronger \(\omega_t,L_t\)
   recurrence row;
6. exact scale covariance of both rows;
7. a globally smooth unforced 2.5D NSE family with any prescribed finite set
   of simple positive entries of one declared compact annular multiplier;
8. a uniform initial-energy/enstrophy bound with unbounded raw entry count;
9. the quadratic small-curve asymptotic showing why this is not a weighted
   atom counterexample;
10. the exact-thin/full-support clarification of the R0.71T internal IFT.

### Not proved

1. removal of the second-time-jet recurrence tax from (3.2);
2. control of \(\omega_t\) or \(L_t\) by the Leray energy inequality;
3. a counterexample to every scale-zero weighted jet or outgoing-occupation
   estimate;
4. a uniform lower bound on the atom masses in the recurrence family;
5. a localized-cell recurrence theorem with cutoff commutators;
6. a definition or estimate for the jet at arbitrary Leray--Hopf or suitable
   weak zero times;
7. a single fixed trajectory realizing an infinite or arbitrarily extensible
   prescribed time set; Theorem 7.3 chooses a new solution for each finite
   set and each \(N\);
8. a continuation criterion, finite-time singularity, or global regularity.

## 14. Route verdict and next finite gate

R0.71U closes the raw recurrence question: exact globally smooth NSE
trajectories can return to one target annulus at any prescribed finite set of
times, even with uniformly bounded initial energy and enstrophy.  Analyticity,
simplicity, and a uniform count on that bounded class cannot supply the
missing packing law.

At the same time, weighted jets do have a rigorous summed theorem once one
pays a second-time derivative.  The next finite gate is therefore not another
zero count.  R0.71V should quantify the recurrence family's atom mass against
the two rows of (3.2), and test whether level-integrated or
amplitude-thresholded excursions can replace the \(C_{tt}\) tax with a
genuine Leray-paid quantity.  A negative result must keep the atom mass from
collapsing; a positive result must control the level-zero boundary rather than
only almost every positive level.
