# R0.72V report source: whole-line graph coercivity by coefficient-uniform unit charts

**Date:** 2026-08-28

**Status:** for every fixed block half-length \(T>0\), a nonhomogeneous
whole-line graph estimate is proved for the exact cubic collision model, with a
constant independent of the time center \(c\) and of the sign \(\sigma\).  The
proof first strengthens R0.72U to a unit-chart theorem uniform in both lower
polynomial coefficients, then uses a disjoint spatial partition and an exact
\(H^{-1}\) direct-sum inequality.  Actual dissipative solutions satisfy
whole-line spacetime observability and a strict fixed-block contraction.
Spatial-cutoff commutators are also absorbable after the global theorem.  The
constant is not uniform as \(T\downarrow0\).  Periodic heat-path transfer,
higher-order remainders, nonlinear Navier--Stokes closure, and every Clay-level
consequence remain open.

**Keywords:** cubic collision, whole-line graph coercivity, negative Sobolev
forcing, coefficient-uniform local theorem, scalar moments, disjoint chart
sum, block contraction

---

## 0. Exact decision and claim boundary

Fix

\[
 I=(-T,T),\qquad T>0,
 \tag{0.1}
\]

and define

\[
 P_{c,\sigma}
 =\partial_t-i\sigma\bigl[x^3+6(c+t)x\bigr],
 \qquad c\in\mathbb R,\quad \sigma\in\{-1,1\}.
 \tag{0.2}
\]

The release labels are

\[
 \boxed{
 \begin{aligned}
 \texttt{twoParameterUnitChartCoercivity}&=\texttt{CLOSED},\\
 \texttt{wholeLineGraphCoercivity}&=\texttt{CLOSED},\\
 \texttt{wholeLineSolutionObservability}&=\texttt{CLOSED},\\
 \texttt{wholeLineBlockContraction}&=\texttt{CLOSED},\\
 \texttt{cutoffCommutatorAbsorption}&=\texttt{CLOSED},\\
 \texttt{timeLengthUniformity}&=\texttt{FALSE},\\
 \texttt{higherOrderRemainderStability}&=\texttt{OPEN},\\
 \texttt{periodicTransfer}&=\texttt{OPEN},\\
 \texttt{Clay}&=\texttt{OPEN}.
 \end{aligned}}
 \tag{0.3}
\]

Here `wholeLineBlockContraction=CLOSED` refers only to (0.2), on a fixed
positive time block, for energy solutions of its scalar dissipative equation.
It is not a periodic theorem and not a statement about arbitrary
three-dimensional Navier--Stokes data.

---

## 1. Function spaces and the global theorem

Use

\[
 H^{-1}(\mathbb R):=(H^1(\mathbb R))^*
 \tag{1.1}
\]

with the standard full \(H^1\) norm.  The whole-line graph space is

\[
 \mathcal G_{c,\sigma}(I)
 :=\left\{
 v\in L^2(I;H^1(\mathbb R)):
 P_{c,\sigma}v\in L^2(I;H^{-1}(\mathbb R))
 \right\}.
 \tag{1.2}
\]

The potential and the time derivative in (1.2) are understood together as a
distribution.  Neither term is required separately to lie in the negative
space on the whole line.

### Theorem 1.1: center-uniform whole-line graph coercivity

For every fixed \(T>0\), there is a finite constant \(C_T\), independent of
\(c\in\mathbb R\) and \(\sigma\in\{-1,1\}\), such that

\[
 \boxed{
 \|v\|_{L^2(I\times\mathbb R)}
 \le C_T\left(
 \|v_x\|_{L^2(I\times\mathbb R)}
 +\|P_{c,\sigma}v\|_{L^2(I;H^{-1}(\mathbb R))}
 \right)}
 \tag{1.3}
\]

for every \(v\in\mathcal G_{c,\sigma}(I)\).

The theorem asserts existence of \(C_T\), not an optimal or explicit value.
Section 10 proves that no choice can remain bounded as \(T\downarrow0\).

---

## 2. The coefficient-uniform unit-chart theorem

Let

\[
 J=(-1/2,1/2),
 \qquad
 H_D^{-1}(J):=(H_0^1(J))^*.
 \tag{2.1}
\]

Here \(H_0^1(J)\) carries the full norm inherited from \(H^1(J)\), namely
\(\|\phi\|_{H_0^1(J)}^2=\|\phi\|_{L^2(J)}^2+\|\phi_y\|_{L^2(J)}^2\).
This convention is used unchanged on every translated cell and is essential
for the constant-one direct-sum inequality in Section 7.

For arbitrary \((a,b)\in\mathbb R^2\), set

\[
 W_{a,b}(t,y)=y^3+ay^2+(b+6t)y
 \tag{2.2}
\]

and

\[
 Q_{a,b,\sigma}=\partial_t-i\sigma W_{a,b}(t,y).
 \tag{2.3}
\]

### Theorem 2.1: two-parameter unit-chart coercivity

There is a finite \(C_T^{\rm loc}\), independent of \(a,b,\sigma\), such that

\[
 \boxed{
 \|v\|_{L^2(I\times J)}
 \le C_T^{\rm loc}\left(
 \|v_y\|_{L^2(I\times J)}
 +\|Q_{a,b,\sigma}v\|_{L^2(I;H_D^{-1}(J))}
 \right).}
 \tag{2.4}
\]

No spatial or temporal trace is prescribed.  The strengthening relative to
R0.72U is uniformity in both \(a\) and \(b\).  This is precisely the
uniformity needed after translating arbitrary whole-line unit cells.

---

## 3. Probe, weighted Poincare reduction, and scalar gauge

Choose a real even function

\[
 q_0\in H_0^1(J)\cap L^\infty(J),\qquad q_0\ge0,
 \qquad \int_Jq_0(y)\,dy=1,
 \tag{3.1}
\]

such that the finitely many polynomial multiples paired against the source
below also lie in \(H_0^1(J)\).  A smooth compactly supported probe is one
choice; the exact rational probe in Section 12 is another.  Write

\[
 \mu_2=\int_Jy^2q_0(y)\,dy>0,
 \qquad
 \mu_4=\int_Jy^4q_0(y)\,dy,
 \qquad
 \mu_4-\mu_2^2>0.
 \tag{3.2}
\]

The strict variance inequality follows because \(y^2\) is not constant
\(q_0(y)\,dy\)-almost everywhere for either of the admitted choices.

For \(v\in L^2(I;H^1(J))\), define

\[
 A(t)=\int_Jv(t,y)q_0(y)\,dy,
 \qquad r(t,y)=v(t,y)-A(t).
 \tag{3.3}
\]

Weighted Poincare modulo constants gives

\[
 \|r\|_{L^2(I\times J)}
 \le C_P\|v_y\|_{L^2(I\times J)}.
 \tag{3.4}
\]

The time-only unitary gauge

\[
 w(t,y)=e^{-i\sigma a\mu_2t}v(t,y)
 \tag{3.5}
\]

obeys the exact identity

\[
 e^{-i\sigma a\mu_2t}Q_{a,b,\sigma}v
 =\left(\partial_t-i\sigma\widetilde W_{a,b}\right)w.
 \tag{3.6}
\]

It preserves every norm in (2.4), and the centered potential is

\[
 \widetilde W_{a,b}(t,y)
 =y^3+a(y^2-\mu_2)+(b+6t)y.
 \tag{3.7}
\]

Its \(q_0\)-mean vanishes exactly:

\[
 \int_J\widetilde W_{a,b}(t,y)q_0(y)\,dy=0.
 \tag{3.8}
\]

After the gauge, rename \(w\) as \(v\) and write

\[
 g=(\partial_t-i\sigma\widetilde W_{a,b})v.
 \tag{3.9}
\]

Pairing with \(q_0\) gives

\[
 A'=i\sigma\int_J\widetilde W_{a,b}r q_0\,dy
 +\langle g,q_0\rangle.
 \tag{3.10}
\]

All later endpoint values are traces of scalar \(H^1(I)\) moments.  No
\(L^2(J)\)-valued endpoint trace of \(v\) is used.

---

## 4. Bounded coefficient pairs

Assume, toward a contradiction, that (2.4) fails.  There are
\((a_n,b_n,\sigma_n,v_n)\) such that

\[
 \|v_n\|_{L^2(I\times J)}=1,
 \qquad
 \delta_n:=\|(v_n)_y\|_2\to0,
 \qquad
 \varepsilon_n:=\|g_n\|_{L^2H_D^{-1}}\to0.
 \tag{4.1}
\]

First suppose \((a_n,b_n)\) is bounded.  Pass to a subsequence on which

\[
 (a_n,b_n,\sigma_n)\to(a_\infty,b_\infty,\sigma_\infty).
 \tag{4.2}
\]

Equation (3.9) and (3.4) imply

\[
 \|A_n'\|_{L^2(I)}\to0.
 \tag{4.3}
\]

Define the odd moment

\[
 B_n(t)=\int_Jv_n(t,y)yq_0(y)\,dy.
 \tag{4.4}
\]

Parity and (3.4) give \(\|B_n\|_2\le C\delta_n\to0\).  Direct pairing gives

\[
 B_n'
 =i\sigma_n\bigl[\mu_4+(b_n+6t)\mu_2\bigr]A_n+E_n,
 \qquad
 \|E_n\|_2\to0.
 \tag{4.5}
\]

The \(a_n\) term vanishes by parity.  Compactness in \(H^1(I)\) makes
\(A_n\) converge strongly to a constant \(A_\infty\), while
\(B_n\to0\) in \(L^2(I)\) implies \(B_n'\to0\) in \(H^{-1}(I)\).  Hence

\[
 \bigl[\mu_4+(b_\infty+6t)\mu_2\bigr]A_\infty=0
 \quad\text{in }\mathcal D'(I).
 \tag{4.6}
\]

The affine factor has nonzero slope \(6\mu_2\), so
\(A_\infty=0\).  This contradicts (3.4) and the normalization in (4.1).

---

## 5. Escaping coefficient pairs and the endpoint ledger

It remains to treat

\[
 \lambda_n=(a_n^2+b_n^2)^{1/2}\to\infty.
 \tag{5.1}
\]

Suppress the index and put

\[
 \alpha=a/\lambda,\qquad \beta=b/\lambda,
 \qquad \alpha^2+\beta^2=1,
 \tag{5.2}
\]

\[
 p_{\alpha,\beta}(y)
 =\alpha(y^2-\mu_2)+\beta y.
 \tag{5.3}
\]

The probe is centered:

\[
 \int_Jp_{\alpha,\beta}q_0=0.
 \tag{5.4}
\]

Its exact variance is

\[
 \kappa_{\alpha,\beta}
 :=\int_Jp_{\alpha,\beta}^2q_0
 =\alpha^2(\mu_4-\mu_2^2)+\beta^2\mu_2
 \ge\kappa_0>0,
 \tag{5.5}
\]

where

\[
 \kappa_0=\min\{\mu_4-\mu_2^2,\mu_2\}.
 \tag{5.6}
\]

Define

\[
 B(t)=\int_Jv(t,y)p_{\alpha,\beta}(y)q_0(y)\,dy.
 \tag{5.7}
\]

Then

\[
 \|B\|_2\le C\delta,
 \tag{5.8}
\]

and the exact moment equation is

\[
 B'
 =i\sigma\bigl[\lambda\kappa_{\alpha,\beta}
 +\ell_{\alpha,\beta}(t)\bigr]A+E,
 \tag{5.9}
\]

where parity reduces the bounded term to

\[
 \ell_{\alpha,\beta}(t)
 =\beta(\mu_4+6t\mu_2),
 \qquad
 |\ell_{\alpha,\beta}(t)|\le L_T:=\mu_4+6T\mu_2,
 \tag{5.10}
\]

and

\[
 \|A'\|_2+\|E\|_2
 \le C\bigl[(1+\lambda)\delta+\varepsilon\bigr].
 \tag{5.11}
\]

For \(\lambda\kappa_0\ge2L_T\), the real coefficient in (5.9) is
positive and at least \(\lambda\kappa_0/2\).  Multiplying (5.9) by
\(\overline A\), integrating, and retaining both scalar endpoints gives

\[
 \frac{\kappa_0}{2}\|A\|_2^2
 \le
 \frac{|B(T)A(T)|+|B(-T)A(-T)|}{\lambda}
 +\frac{\|B\|_2\|A'\|_2}{\lambda}
 +\frac{\|E\|_2\|A\|_2}{\lambda}.
 \tag{5.12}
\]

The scalar trace inequality

\[
 |f(\pm T)|
 \le C_T\left(
 \|f\|_2+\|f\|_2^{1/2}\|f'\|_2^{1/2}
 \right)
 \tag{5.13}
\]

is sufficient.  Let

\[
 H=(1+\lambda)\delta+\varepsilon.
 \tag{5.14}
\]

The normalization, (5.8)--(5.11), and (5.13) yield

\[
 |A(\pm T)|\le C(1+\sqrt H),
 \qquad
 |B(\pm T)|\le C(\delta+\sqrt{\delta\lambda}).
 \tag{5.15}
\]

No assumption \(\lambda\delta\to0\) is made.  Expanding the endpoint product
shows

\[
 \frac{|BA|}{\lambda}
 \le C\left(
 \delta+\sqrt{\frac\delta\lambda}
 +\sqrt{\frac{\delta\varepsilon}{\lambda}}
 +\frac{\delta^{3/2}}{\sqrt\lambda}
 +\frac{\delta\sqrt\varepsilon}{\lambda}
 \right)=o(1).
 \tag{5.16}
\]

The remaining two terms in (5.12) satisfy

\[
 \frac{\|B\|_2\|A'\|_2}{\lambda}
 \le C\left(\delta^2+\frac{\delta^2+\delta\varepsilon}{\lambda}\right)=o(1),
 \tag{5.17}
\]

\[
 \frac{\|E\|_2\|A\|_2}{\lambda}
 \le C\left(\delta+\frac{\delta+\varepsilon}{\lambda}\right)=o(1).
 \tag{5.18}
\]

Thus \(A_n\to0\) in \(L^2(I)\), again contradicting (3.4) and (4.1).
Theorem 2.1 follows.

---

## 6. Translation of every whole-line cell

Partition the line, up to measure-zero endpoints, into

\[
 J_k=(k-1/2,k+1/2),\qquad k\in\mathbb Z.
 \tag{6.1}
\]

On \(J_k\), write \(x=k+y\).  The exact polynomial identity is

\[
 \begin{aligned}
 x^3+6(c+t)x
 ={}&y^3+3ky^2+(3k^2+6c+6t)y\\
 &+k^3+6(c+t)k.
 \end{aligned}
 \tag{6.2}
\]

The final line is independent of \(y\).  The time-only phase with derivative

\[
 d_{k,c}(t)=k^3+6(c+t)k
 \tag{6.3}
\]

removes it without changing any spatial or negative-Sobolev norm.  The
remaining unit-chart coefficients are

\[
 a_k=3k,
 \qquad
 b_{k,c}=3k^2+6c.
 \tag{6.4}
\]

More explicitly, with

\[
 D_{k,c}(t)=(k^3+6ck)t+3kt^2,
 \qquad
 w_k(t,y)=e^{-i\sigma D_{k,c}(t)}v(t,k+y),
 \tag{6.5}
\]

the restricted source is exactly multiplied by the same scalar unitary, and
the local operator acting on \(w_k\) is \(Q_{a_k,b_{k,c},\sigma}\).  The
additional centering gauge (3.5) is then applied inside Theorem 2.1.

Theorem 2.1 is uniform over exactly these two coefficients, including every
large \(|k|\), every large \(|c|\), and every cancellation between
\(3k^2\) and \(6c\).

---

## 7. Exact \(H^{-1}\) direct-sum lemma

For \(g\in H^{-1}(\mathbb R)\), let \(g_k\) denote its restriction to
\(H_0^1(J_k)\).  Then

\[
 \boxed{
 \sum_{k\in\mathbb Z}
 \|g_k\|_{H_D^{-1}(J_k)}^2
 \le\|g\|_{H^{-1}(\mathbb R)}^2.}
 \tag{7.1}
\]

To prove (7.1), first take a finite set \(F\subset\mathbb Z\).  For each
\(k\in F\), choose the Riesz representative \(\phi_k\in H_0^1(J_k)\) of
\(g_k\), with the phase chosen so that

\[
 \langle g_k,\phi_k\rangle=\|g_k\|_{H_D^{-1}(J_k)}^2,
 \qquad
 \|\phi_k\|_{H_0^1(J_k)}=\|g_k\|_{H_D^{-1}(J_k)}.
 \tag{7.2}
\]

The zero extensions have disjoint interiors and zero traces, so

\[
 \left\|\sum_{k\in F}\phi_k\right\|_{H^1(\mathbb R)}^2
 =\sum_{k\in F}\|\phi_k\|_{H_0^1(J_k)}^2.
 \tag{7.3}
\]

Duality gives the finite version of (7.1); monotone convergence over finite
sets gives the full statement.  Applied for almost every \(t\) and integrated,

\[
 \sum_k\|g_k\|_{L^2(I;H_D^{-1}(J_k))}^2
 \le\|g\|_{L^2(I;H^{-1}(\mathbb R))}^2.
 \tag{7.4}
\]

---

## 8. Proof of the whole-line theorem

Let \(g=P_{c,\sigma}v\).  Restriction to \(J_k\), translation by \(k\), and
the scalar gauge in Section 6 put the local equation into Theorem 2.1.  Hence

\[
 \|v\|_{L^2(I\times J_k)}
 \le C_T^{\rm loc}\left(
 \|v_x\|_{L^2(I\times J_k)}
 +\|g_k\|_{L^2(I;H_D^{-1}(J_k))}
 \right).
 \tag{8.1}
\]

Square (8.1), sum over \(k\), use \((r+s)^2\le2(r^2+s^2)\), and insert
(7.4).  This gives

\[
 \|v\|_{L^2(I\times\mathbb R)}^2
 \le2(C_T^{\rm loc})^2\left(
 \|v_x\|_{L^2(I\times\mathbb R)}^2
 +\|g\|_{L^2(I;H^{-1}(\mathbb R))}^2
 \right).
 \tag{8.2}
\]

Theorem 1.1 follows, for example, with

\[
 C_T=\sqrt2\,C_T^{\rm loc}.
 \tag{8.3}
\]

No spatial cutoff appears in this proof.  There is therefore no tail term and
no boundary flux to estimate before obtaining (1.3).

---

## 9. Actual solutions, observability, and strict block contraction

### Proposition 9.1: the energy evolution on the whole line

For every \(u_-\in L^2(\mathbb R)\), fixed \(c\), fixed
\(\sigma\in\{-1,1\}\), and fixed \(T>0\), there is a unique solution

\[
 u\in C(\overline I;L^2(\mathbb R))
 \cap L^2(I;H^1(\mathbb R))
 \tag{9.1}
\]

of

\[
 P_{c,\sigma}u=u_{xx},
 \qquad u(-T)=u_-,
 \tag{9.2}
\]

and it satisfies, for every \(-T\le t_1\le t_2\le T\),

\[
 \|u(t_2)\|_2^2
 +2\int_{t_1}^{t_2}\|u_x(t)\|_2^2\,dt
 =\|u(t_1)\|_2^2.
 \tag{9.3}
\]

#### Construction and energy audit

Choose \(\chi_N\in C_c^\infty(\mathbb R)\) equal to one on \([-N,N]\),
and replace the real potential by

\[
 V_N(t,x)=\chi_N(x)\sigma[x^3+6(c+t)x].
 \tag{9.4}
\]

The bounded, time-continuous skew multiplication \(iV_N\) is a bounded
perturbation of the heat generator.  Its solution \(u_N\) obeys, for every
\(t\in I\),

\[
 \|u_N(t)\|_2^2
 +2\int_{-T}^{t}\|(u_N)_x(s)\|_2^2\,ds
 =\|u_-\|_2^2.
 \tag{9.5}
\]

In particular,

\[
 \sup_{t\in I}\|u_N(t)\|_2^2
 +2\int_I\|(u_N)_x\|_2^2
 \le2\|u_-\|_2^2.
 \tag{9.6}
\]

On every fixed compact spatial interval \(K\), the equation bounds
\((u_N)_t\) in \(L^2(I;H^{-1}(K))\) once \(N\) contains \(K\).  Local
Aubin--Lions compactness therefore gives, after a diagonal extraction,
strong convergence in \(L^2(I\times K)\).  This is enough to pass the local
potential term and obtain (9.2) distributionally; weak lower semicontinuity
gives the energy inequality.

The same localized mass identity applied to exterior cutoffs gives a tail
bound uniform in \(N\): for fixed \(t\), the mass outside a radius \(R\) is
bounded by the corresponding initial tail plus
\(O_T(R^{-1})\|u_-\|_2^2\).  Thus no \(L^2\) mass can disappear through
spatial infinity in the diagonal limit.

For the reverse inequality and uniqueness, take a real cutoff \(\eta_R\)
equal to one on \([-R,R]\), supported in \([-2R,2R]\), with
\(|\eta_R'|\le C/R\).  The localized energy identity contains no potential
term in its real part, and its only spatial-boundary error is bounded by

\[
 \frac{C}{R}
 \|u_x\|_{L^2((t_1,t_2)\times\mathbb R)}
 \|u\|_{L^2((t_1,t_2)\times\mathbb R)}
 \longrightarrow0.
 \tag{9.7}
\]

Steklov averaging justifies the local test at energy regularity.  Sending
\(R\to\infty\) proves (9.3).  Applying the same identity to the difference of
two solutions proves uniqueness.  Weak continuity together with (9.3) gives
the strong \(L^2\) continuity in (9.1).  This construction is analytic; it is
not part of the finite algebraic certificate.

Now consider the solution in Proposition 9.1.  It satisfies

\[
 P_{c,\sigma}u=u_{xx}
 \quad\text{in }\mathcal D'(I\times\mathbb R),
 \tag{9.8}
\]

and therefore belongs to the maximal graph space (1.2).  Proposition 9.1 is
the separate step that supplies the time traces and energy identity; neither
is inferred from maximal graph membership alone.  Since

\[
 \|u_{xx}\|_{H^{-1}(\mathbb R)}
 \le\|u_x\|_{L^2(\mathbb R)},
 \tag{9.9}
\]

Theorem 1.1 gives the whole-line solution observability estimate

\[
 \boxed{
 \|u\|_{L^2(I\times\mathbb R)}
 \le2C_T\|u_x\|_{L^2(I\times\mathbb R)}.}
 \tag{9.10}
\]

Let

\[
 E(t)=\|u(t)\|_{L^2(\mathbb R)}^2.
 \tag{9.11}
\]

For a smooth solution, the reality of the potential and a spatial cutoff
limit give

\[
 E(T)+2\int_{-T}^{T}\|u_x(t)\|_2^2\,dt=E(-T).
 \tag{9.12}
\]

The same conclusion below would only need the corresponding energy inequality
and monotonicity.  From (9.10),

\[
 \int_{-T}^{T}E(t)\,dt
 \le4C_T^2\int_{-T}^{T}\|u_x(t)\|_2^2\,dt.
 \tag{9.13}
\]

Since \(E(t)\ge E(T)\) on the block, (9.3) and (9.13) give

\[
 2T E(T)
 \le2C_T^2\bigl[E(-T)-E(T)\bigr].
 \tag{9.14}
\]

Consequently,

\[
 \boxed{
 E(T)\le\frac{C_T^2}{T+C_T^2}E(-T),}
 \tag{9.15}
\]

or, in norm,

\[
 \boxed{
 \|u(T)\|_2
 \le\rho_T\|u(-T)\|_2,
 \qquad
 \rho_T=\frac{C_T}{\sqrt{T+C_T^2}}<1.}
 \tag{9.16}
\]

The factor is uniform in \(c\) and \(\sigma\), but is not asserted to be
optimal.  In terms of the evolution family from Proposition 9.1,

\[
 \boxed{
 \sup_{c\in\mathbb R,\,\sigma\in\{-1,1\}}
 \|U_{c,\sigma}(T,-T)\|_{L^2\to L^2}
 \le\rho_T<1.}
 \tag{9.17}
\]

This is the precise `wholeLineBlockContraction=CLOSED` statement.

---

## 10. Fixed \(T\) is essential

The exact kernel of \(P_{c,\sigma}\) provides a quantitative obstruction to
time-length uniformity.  At \(c=0\), take a fixed real normalized Schwartz
function \(f\), define

\[
 f_L(x)=L^{-1/2}f(x/L),
 \tag{10.1}
\]

and set

\[
 v_{T,L}(t,x)=f_L(x)
 \exp\left\{i\sigma\left(tx^3+3t^2x-T^2x\right)\right\}.
 \tag{10.2}
\]

Then \(P_{0,\sigma}v_{T,L}=0\).  The exact R0.72U phase calculation, now
integrated on the whole line, gives

\[
 \frac{\|(v_{T,L})_x\|_{L^2(I\times\mathbb R)}^2}
 {\|v_{T,L}\|_{L^2(I\times\mathbb R)}^2}
 =L^{-2}\|f'\|_2^2
 +3T^2L^4\|x^2f\|_2^2
 +\frac45T^4.
 \tag{10.3}
\]

Choose \(L=T^{-1/3}\).  For \(0<T\le1\),

\[
 \frac{\|(v_{T,L})_x\|_2}{\|v_{T,L}\|_2}
 \le C_fT^{1/3}.
 \tag{10.4}
\]

Any constant in (1.3) must therefore satisfy

\[
 \boxed{C_T\ge c_fT^{-1/3}\qquad(0<T\le1).}
 \tag{10.5}
\]

This is fully compatible with Theorem 1.1, which fixes \(T>0\) before
claiming center-uniformity.  It rules out a block contraction factor bounded
away from one by the graph argument uniformly over arbitrarily short blocks.

---

## 11. Spatial-cutoff commutators after the global theorem

Although no cutoff is needed for Theorem 1.1, its commutator can now be
absorbed rather than left open.  For a smooth scalar cutoff \(\eta\), put
\(v=\eta u\).  From (9.1),

\[
 P_{c,\sigma}v
 =v_{xx}-\mathcal C_\eta u,
 \qquad
 \mathcal C_\eta u=2\eta'u_x+\eta''u.
 \tag{11.1}
\]

The exact divergence rewrite

\[
 \mathcal C_\eta u
 =\partial_x(2\eta'u)-\eta''u
 \tag{11.2}
\]

gives

\[
 \|\mathcal C_\eta u\|_{H^{-1}}
 \le2\|\eta'u\|_2+\|\eta''u\|_2.
 \tag{11.3}
\]

Applying (1.3) to \(v\), then using
\(v_x=\eta u_x+\eta'u\), yields

\[
 \|\eta u\|_2
 \le2C_T\|\eta u_x\|_2
 +4C_T\|\eta'u\|_2
 +C_T\|\eta''u\|_2.
 \tag{11.4}
\]

Take a smooth square partition \(\{\eta_{k,L}\}_{k\in\mathbb Z}\) with

\[
 \sum_k\eta_{k,L}^2=1,
 \quad
 \left(\sum_k|\eta_{k,L}'|^2\right)^{1/2}\le A_1/L,
 \quad
 \left(\sum_k|\eta_{k,L}''|^2\right)^{1/2}\le A_2/L^2.
 \tag{11.5}
\]

Taking the \(\ell^2\) norm of (11.4) gives

\[
 \|u\|_2
 \le2C_T\|u_x\|_2
 +q_L\|u\|_2,
 \qquad
 q_L=\frac{4C_TA_1}{L}+\frac{C_TA_2}{L^2}.
 \tag{11.6}
\]

For \(L\) large enough, \(q_L<1\), and the cutoff terms are absorbed.  This
corollary is an audit of the localization algebra; it is not needed in the
shorter disjoint-cell proof of (1.3).

---

## 12. Exact rational probe calibration

For the unit interval \(J=(-1/2,1/2)\), an exact admissible probe is

\[
 q_0(y)=\frac{315}{128}(1-4y^2)^4
 \mathbf1_{[-1/2,1/2]}(y).
 \tag{12.1}
\]

It and every polynomial multiple used above belong to \(H_0^1(J)\).  Its
exact moments are

\[
 \int_Jq_0=1,
 \qquad
 \mu_2=\frac1{44},
 \qquad
 \mu_4=\frac3{2288},
 \tag{12.2}
\]

\[
 \mu_4-\mu_2^2=\frac5{6292},
 \qquad
 \kappa_0=\frac5{6292}.
 \tag{12.3}
\]

For \(T=1\),

\[
 L_1=\mu_4+6\mu_2=\frac{315}{2288},
 \tag{12.4}
\]

so the explicit sufficient escaping-pair threshold

\[
 \lambda\ge\frac{2L_1}{\kappa_0}=\frac{693}{2}
 \tag{12.5}
\]

ensures

\[
 \lambda\kappa_{\alpha,\beta}
 +\ell_{\alpha,\beta}(t)
 \ge\frac{\lambda\kappa_0}{2}
 \qquad(|t|\le1).
 \tag{12.6}
\]

These rational identities, the translation map (6.2), and the contraction
algebra (9.8) are finite certificate targets.  The certificate does not
machine-check the compactness contradiction, scalar trace passage, countable
direct-sum functional analysis, or existence theory for the nonautonomous
evolution.

---

## 13. Literature boundary

The closest primary-source results split into three groups.

1. Local vector-field and kinetic Poincare theorems provide the structural
   precedent for an \(H^{-1}\) drift norm, but do not directly state the
   coefficient-uniform, arbitrary-trace, nonautonomous theorem (1.3).

2. Autonomous enhanced-dissipation and purely imaginary-potential results
   cover fixed shear profiles on bounded or unbounded cross-sections.  In
   particular, the 2025 Li--Zhang theorem treats a fixed finite-type profile on
   an unbounded cross-section under a nondegeneracy condition at infinity.
   Applied separately to \(x^3+6ax\), it gives an autonomous benchmark; its
   published statement does not make the constants uniform in \(a\) and does
   not cover \(a=a(t)\).

3. Coble--He's time-dependent shear result assumes slowly moving,
   nondegenerate, separated critical points.  The cubic collision changes the
   number and degeneracy of the critical points, so that theorem does not
   supply R0.72V.

R0.72V uses a model-specific coefficient-uniform scalar-moment proof and an
exact negative-Sobolev direct sum.  A bounded primary-source search did not
locate a theorem that directly replaces this argument.  That search statement
is not a novelty, nonexistence, or priority claim.

---

## 14. Mathematical value and next interface

The strict increment over R0.72U is not merely a tail estimate.  The unit-chart
constant is made uniform under every spatial translation, which permits a
lossless disjoint-cell globalization.  This closes whole-line graph
coercivity, actual-solution observability, fixed-block contraction, and the
cutoff-commutator ledger for the exact cubic collision model.

The result remains linear and model-specific.  It does not yet control the
\(H_5,H_7,R_9\) terms produced by the full heat-path expansion, does not
transfer the estimate to the periodic physical variables, and contains no
three-dimensional pressure, vortex-stretching, nonlinear bootstrap, or
continuation argument.

The next minimal section must test whether (1.3) is stable under the exact
weighted higher-order remainders on a finite collision block.  Only after a
remainder-stable theorem is proved can the periodic exact-heat-path transfer
be attempted.
