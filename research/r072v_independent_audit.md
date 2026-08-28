# R0.72V independent analytic audit

**Date:** 2026-08-28

**Audit outcome:** the coefficient-uniform unit-chart theorem and its
whole-line direct-sum globalization are **PASS**.  The scalar gauge, the
two-moment algebra, and the endpoint estimate remain valid without any rate
assumption on \(\lambda\delta\).  Whole-line observability for actual
dissipative solutions is **PASS**.  The separate real-potential truncation
construction, with the two-line energy ledger checked in Section 10,
supplies that energy-solution class for every \(L^2\) datum.
Strict all-data block contraction is therefore **PASS through that separate
construction**; it must not be inferred from maximal distributional graph
membership alone.
The short-time calculation proves only the lower bound
\(C_T\gtrsim T^{-1/3}\).  The present chart proof does not claim a matching
upper bound or a sharp contraction asymptotic.

## 0. Statement and verdict matrix

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

The global estimate under audit is

\[
 \|v\|_{L^2(I\times\mathbb R)}
 \le C_T\left(
 \|v_x\|_{L^2(I\times\mathbb R)}
 +\|P_{c,\sigma}v\|_{L^2(I;H^{-1}(\mathbb R))}
 \right),
 \tag{0.3}
\]

with \(C_T\) independent of \(c\) and \(\sigma\), for each fixed
\(T>0\).

The independent verdicts are

\[
 \boxed{
 \begin{aligned}
 \text{two-parameter unit-chart coercivity}&:\ \mathrm{PASS},\\
 \text{arbitrary-}\lambda\delta\text{ endpoint closure}&:\ \mathrm{PASS},\\
 \text{whole-line }H^{-1}\text{ direct sum}&:\ \mathrm{PASS},\\
 \text{maximal-domain globalization}&:\ \mathrm{PASS},\\
 \text{actual-solution observability}&:\ \mathrm{PASS},\\
 \text{all-}L^2\text{-data energy evolution}&:\ \mathrm{PASS},\\
 \text{energy-solution block contraction}&:\ \mathrm{PASS},\\
 \text{block contraction from graph membership alone}&:\ \mathrm{FAIL},\\
 \text{uniformity as }T\downarrow0&:\ \mathrm{FALSE}.
 \end{aligned}}
 \tag{0.4}
\]

The `FAIL` entry in (0.4) is a claim-boundary warning, not a counterexample
to (0.3).  The report correctly uses the separately constructed energy
evolution, rather than bare maximal graph membership, for its contraction
corollary.

## 1. Function-space audit

The negative space must be

\[
 H^{-1}(\mathbb R):=(H^1(\mathbb R))^*
 \tag{1.1}
\]

with the full norm

\[
 \|\phi\|_{H^1(\mathbb R)}^2
 =\|\phi\|_2^2+\|\phi_x\|_2^2.
 \tag{1.2}
\]

The correct global graph domain is the maximal distributional domain

\[
 \mathcal G_{c,\sigma}(I)
 =\left\{
 v\in L^2(I;H^1(\mathbb R)):
 P_{c,\sigma}v\in L^2(I;H^{-1}(\mathbb R))
 \text{ in }\mathcal D'(I\times\mathbb R)
 \right\}.
 \tag{1.3}
\]

The two terms \(v_t\) and
\(i\sigma[x^3+6(c+t)x]v\) are not required separately to belong to
\(L^2H^{-1}\).  Requiring them separately would define a smaller space and
would not prove (0.3) on the stated maximal graph domain.  Polynomial
multiplication is well defined distributionally, and restriction to a
bounded spatial cell is legitimate.

The local space is

\[
 H_D^{-1}(J):=(H_0^1(J))^*,
 \qquad J=(-1/2,1/2),
 \tag{1.4}
\]

where the \(H_0^1(J)\) norm is also the full inherited \(H^1\) norm.  This
norm convention is needed for the exact constant-one direct-sum statement
in Section 8.

## 2. Independent gauge recomputation

On \(J\), set

\[
 Q_{a,b,\sigma}
 =\partial_t-i\sigma\bigl[y^3+ay^2+(b+6t)y\bigr].
 \tag{2.1}
\]

Choose

\[
 q_0\in C_c^\infty(J),\qquad
 q_0\ge0,\qquad q_0(-y)=q_0(y),\qquad
 \int_Jq_0=1,
 \tag{2.2}
\]

and define

\[
 \mu_2=\int_Jy^2q_0(y)\,dy,
 \qquad
 \mu_4=\int_Jy^4q_0(y)\,dy.
 \tag{2.3}
\]

The nonnegativity, normalization, and nontrivial smooth support give

\[
 \mu_2>0,
 \qquad
 \mu_4-\mu_2^2>0.
 \tag{2.4}
\]

These hypotheses are essential.  An arbitrary even sign-changing probe
would not justify the variance lower bound used later.

Let

\[
 w(t,y)=e^{-i\sigma a\mu_2t}v(t,y).
 \tag{2.5}
\]

Then direct differentiation gives

\[
 \begin{aligned}
 w_t
 &=e^{-i\sigma a\mu_2t}
 \bigl(v_t-i\sigma a\mu_2v\bigr),\\
 e^{-i\sigma a\mu_2t}Q_{a,b,\sigma}v
 &=\left[
 \partial_t-i\sigma\widetilde W_{a,b}(t,y)
 \right]w,
 \end{aligned}
 \tag{2.6}
\]

where

\[
 \widetilde W_{a,b}
 =y^3+a(y^2-\mu_2)+(b+6t)y.
 \tag{2.7}
\]

Thus the sign in (2.5) is correct.  Equivalently one may write
\(v=e^{i\sigma a\mu_2t}w\).  Since the multiplier depends only on time and
has unit modulus, it preserves the spatial derivative norm and every local
negative-Sobolev norm.

Parity and centering yield the exact cancellation

\[
 \int_J\widetilde W_{a,b}(t,y)q_0(y)\,dy=0.
 \tag{2.8}
\]

## 3. Weighted Poincare reduction

After the gauge, rename \(w\) as \(v\), put

\[
 g=(\partial_t-i\sigma\widetilde W_{a,b})v,
 \tag{3.1}
\]

and define

\[
 A(t)=\int_Jv(t,y)q_0(y)\,dy,
 \qquad r(t,y)=v(t,y)-A(t).
 \tag{3.2}
\]

Because \(\int q_0=1\), weighted Poincare modulo constants gives

\[
 \|r\|_{L^2(I\times J)}
 \le C_P\|v_y\|_{L^2(I\times J)}.
 \tag{3.3}
\]

Pairing (3.1) with \(q_0\), and using (2.8), gives

\[
 A'
 =i\sigma\int_J\widetilde W_{a,b}r q_0\,dy
 +\langle g,q_0\rangle.
 \tag{3.4}
\]

This proves \(A\in H^1(I)\).  All endpoint values used below are traces of
scalar \(H^1(I)\) moments.  The proof does not require, and does not imply,
an \(L^2(J)\)-valued endpoint trace of the full function \(v\).

## 4. Bounded coefficient pairs

For an independently normalized contradiction sequence, write

\[
 \|v_n\|_{L^2(I\times J)}=1,
 \qquad
 \delta_n=\|(v_n)_y\|_2\to0,
 \qquad
 \varepsilon_n=\|g_n\|_{L^2H_D^{-1}}\to0.
 \tag{4.1}
\]

If \((a_n,b_n)\) is bounded, pass to a convergent subsequence.  Equations
(3.3)--(3.4) imply

\[
 \|A_n'\|_2\to0,
 \qquad
 \|v_n-A_n\|_2\to0.
 \tag{4.2}
\]

Define

\[
 B_n(t)=\int_Jv_n(t,y)yq_0(y)\,dy.
 \tag{4.3}
\]

Then \(\|B_n\|_2\lesssim\delta_n\), while direct pairing gives

\[
 B_n'
 =i\sigma_n\bigl[\mu_4+(b_n+6t)\mu_2\bigr]A_n+E_n,
 \qquad \|E_n\|_2\to0.
 \tag{4.4}
\]

The \(a_n\) contribution is odd and integrates to zero.  Compactness of
the scalar \(H^1(I)\) sequence makes \(A_n\) converge strongly to a
constant, while \(B_n\to0\) in \(L^2(I)\) implies
\(B_n'\to0\) in \(H^{-1}(I)\).  Hence

\[
 \bigl[\mu_4+(b_\infty+6t)\mu_2\bigr]A_\infty=0.
 \tag{4.5}
\]

The coefficient has slope \(6\mu_2\ne0\), so \(A_\infty=0\), contradicting
(3.3) and the normalization.  The bounded-parameter branch is **PASS**.

## 5. Escaping coefficient pairs: independent moment algebra

Suppose

\[
 \lambda=(a^2+b^2)^{1/2}\to\infty,
 \qquad
 \alpha=a/\lambda,
 \qquad
 \beta=b/\lambda.
 \tag{5.1}
\]

Then \(\alpha^2+\beta^2=1\).  Set

\[
 p(y)=\alpha(y^2-\mu_2)+\beta y,
 \qquad
 B(t)=\int_Jv(t,y)p(y)q_0(y)\,dy.
 \tag{5.2}
\]

Parity gives

\[
 \int_Jpq_0=0,
 \tag{5.3}
\]

and an independent expansion gives

\[
 \begin{aligned}
 \kappa
 :=\int_Jp^2q_0
 &=\alpha^2(\mu_4-\mu_2^2)+\beta^2\mu_2,\\
 \kappa&\ge\kappa_0
 :=\min\{\mu_4-\mu_2^2,\mu_2\}>0.
 \end{aligned}
 \tag{5.4}
\]

Since \(B=\int rpq_0\),

\[
 \|B\|_{L^2(I)}\lesssim\delta.
 \tag{5.5}
\]

The centered potential has the exact decomposition

\[
 \widetilde W_{a,b}
 =\lambda p+y^3+6ty.
 \tag{5.6}
\]

Pairing the equation with \(pq_0\) gives

\[
 B'
 =i\sigma\bigl[\lambda\kappa+\ell_p(t)\bigr]A+E,
 \tag{5.7}
\]

where

\[
 \begin{aligned}
 \ell_p(t)
 &=\int_J(y^3+6ty)pq_0\,dy\\
 &=\beta(\mu_4+6t\mu_2),
 \end{aligned}
 \tag{5.8}
\]

and

\[
 E=\langle g,pq_0\rangle
 +i\sigma\int_J\widetilde W_{a,b}r p q_0\,dy.
 \tag{5.9}
\]

Consequently,

\[
 \|A'\|_2+\|E\|_2
 \lesssim (1+\lambda)\delta+\varepsilon,
 \tag{5.10}
\]

and, using \(\|A\|_2=O(1)\),

\[
 \|B'\|_2\lesssim\lambda+(1+\lambda)\delta+\varepsilon
 \lesssim\lambda
 \tag{5.11}
\]

along the normalized contradiction sequence.  Equations (5.4), (5.7), and
(5.8) independently confirm the leading coefficient, its sign up to the
irrelevant factor \(i\sigma\), and the uniform boundedness of the lower-order
term.

## 6. Endpoint audit with arbitrary \(\lambda\delta\)

The scalar trace inequality

\[
 |h(\pm T)|
 \le C_T\left(
 \|h\|_2+\|h\|_2^{1/2}\|h'\|_2^{1/2}
 \right)
 \tag{6.1}
\]

applied to (5.5), (5.10), and (5.11) gives

\[
 |A(\pm T)|
 \lesssim1+\sqrt{(1+\lambda)\delta+\varepsilon},
 \tag{6.2}
\]

\[
 |B(\pm T)|
 \lesssim\delta+\sqrt{\lambda\delta}.
 \tag{6.3}
\]

Multiplying (5.7) by \(\overline A\), integrating by parts, and dividing by
\(\lambda\) produces the endpoint term

\[
 \lambda^{-1}[B\overline A]_{-T}^{T}.
 \tag{6.4}
\]

The product of (6.2) and (6.3) satisfies

\[
 \frac{|B(\pm T)A(\pm T)|}{\lambda}
 \lesssim
 \delta
 +\sqrt{\frac{\delta}{\lambda}}
 +\sqrt{\frac{\delta\varepsilon}{\lambda}}
 +\frac{\delta^{3/2}}{\sqrt\lambda}
 +\frac{\delta\sqrt\varepsilon}{\lambda}
 +o(1).
 \tag{6.5}
\]

Every term tends to zero when
\(\delta,\varepsilon\to0\) and \(\lambda\to\infty\), with no condition on
the product \(\lambda\delta\).

The bulk integration-by-parts errors satisfy

\[
 \frac{\|B\|_2\|A'\|_2}{\lambda}=o(1),
 \qquad
 \frac{\|E\|_2\|A\|_2}{\lambda}=o(1),
 \qquad
 \frac{\|\ell_p\|_\infty}{\lambda}\|A\|_2^2=o(1).
 \tag{6.6}
\]

Since \(\kappa\ge\kappa_0>0\), equations (5.7) and (6.4)--(6.6) force

\[
 \|A\|_{L^2(I)}\to0.
 \tag{6.7}
\]

Together with (3.3), this contradicts \(\|v\|_2=1\).  The escaping branch,
including its endpoint ledger for arbitrary \(\lambda\delta\), is
**PASS**.

## 7. Translation of the whole line

Partition \(\mathbb R\), modulo endpoints of measure zero, into

\[
 J_k=(k-1/2,k+1/2),\qquad k\in\mathbb Z.
 \tag{7.1}
\]

Writing \(x=k+y\), direct expansion gives

\[
 \begin{aligned}
 x^3+6(c+t)x
 ={}&y^3+3ky^2+(3k^2+6c+6t)y\\
 &+k^3+6(c+t)k.
 \end{aligned}
 \tag{7.2}
\]

Thus

\[
 a_k=3k,
 \qquad
 b_{k,c}=3k^2+6c.
 \tag{7.3}
\]

For

\[
 D_{k,c}(t)=(k^3+6ck)t+3kt^2,
 \qquad
 w_k(t,y)=e^{-i\sigma D_{k,c}(t)}v(t,k+y),
 \tag{7.4}
\]

one has

\[
 D_{k,c}'(t)=k^3+6(c+t)k,
 \tag{7.5}
\]

so the last line of (7.2) is removed with the correct sign.  The local
source is multiplied by the same scalar unitary.  The further gauge (2.5)
centers \(a_k\mu_2\).  Both gauges preserve all norms entering the local
estimate.  This translation algebra is **PASS**.

## 8. Independent \(H^{-1}\) direct-sum proof

For \(g\in H^{-1}(\mathbb R)\), let \(g_k\) be its restriction to
\(H_0^1(J_k)\).  If every local space uses the full inherited norm, zero
extension defines an isometry

\[
 \bigoplus_{k\in\mathbb Z}H_0^1(J_k)
 \longrightarrow H^1(\mathbb R).
 \tag{8.1}
\]

For a finite set \(F\subset\mathbb Z\), duality on this orthogonal direct
sum gives

\[
 \sum_{k\in F}\|g_k\|_{H_D^{-1}(J_k)}^2
 \le\|g\|_{H^{-1}(\mathbb R)}^2.
 \tag{8.2}
\]

Taking an increasing sequence of finite sets yields

\[
 \boxed{
 \sum_{k\in\mathbb Z}\|g_k\|_{H_D^{-1}(J_k)}^2
 \le\|g\|_{H^{-1}(\mathbb R)}^2.}
 \tag{8.3}
\]

The zero-trace condition on the test functions is what prevents boundary
delta terms in their zero extensions.  The functions being estimated need
not have zero traces.

If the local \(H_0^1\) norm were instead defined only by
\(\|\phi'\|_2\), (8.3) would retain a fixed unit-interval Poincare constant
rather than the literal constant one.  This would not invalidate the global
theorem, but mixing those norm conventions would invalidate the exact
statement of (8.3).  With the report's full-norm convention, the direct-sum
claim is **PASS**.

Applying (8.3) for almost every time and integrating gives

\[
 \sum_k\|g_k\|_{L^2(I;H_D^{-1}(J_k))}^2
 \le\|g\|_{L^2(I;H^{-1}(\mathbb R))}^2.
 \tag{8.4}
\]

## 9. Global graph estimate

The unit-chart theorem gives, uniformly in \(k,c,\sigma\),

\[
 \|v\|_{L^2(I\times J_k)}
 \le C_T^{\rm loc}\left(
 \|v_x\|_{L^2(I\times J_k)}
 +\|g_k\|_{L^2(I;H_D^{-1}(J_k))}
 \right).
 \tag{9.1}
\]

Squaring, summing, and using (8.4) gives

\[
 \|v\|_{L^2(I\times\mathbb R)}^2
 \le2(C_T^{\rm loc})^2\left(
 \|v_x\|_2^2+\|P_{c,\sigma}v\|_{L^2H^{-1}}^2
 \right).
 \tag{9.2}
\]

Thus (0.3) holds with, for example,

\[
 C_T=\sqrt2\,C_T^{\rm loc}.
 \tag{9.3}
\]

No spatial cutoff is used in (9.1)--(9.3), so no tail or boundary-flux
assumption is hidden in the globalization.  The whole-line graph theorem is
**PASS** on the maximal distributional domain (1.3).

## 10. All-data energy evolution and observability

### 10.1 Independent audit of the analytic construction

For \(u_-\in L^2(\mathbb R)\), truncate the real potential by

\[
 V_N(t,x)=\chi_N(x)\sigma[x^3+6(c+t)x],
 \tag{10.1}
\]

where \(\chi_N\) is real, compactly supported, and equal to one on
\([-N,N]\).  For fixed \(N,c,T\), multiplication by \(iV_N(t)\) is a
bounded skew perturbation of the heat generator and is norm-continuous in
time.  Standard nonautonomous bounded-perturbation theory therefore gives a
unique truncated evolution \(u_N\).

Taking the real part of the truncated equation independently gives, for
every \(t\in[-T,T]\),

\[
 \|u_N(t)\|_2^2
 +2\int_{-T}^{t}\|(u_N)_x(s)\|_2^2\,ds
 =\|u_-\|_2^2.
 \tag{10.2}
\]

Consequently,

\[
 \sup_{t\in I}\|u_N(t)\|_2^2
 +2\int_I\|(u_N)_x\|_2^2
 \le2\|u_-\|_2^2.
 \tag{10.3}
\]

The distinction between (10.2) and (10.3) is necessary: replacing the
left side of (10.2) by a supremum while retaining equality with only
\(\|u_-\|_2^2\) would be false.  The report now uses the correct two-line
ledger (10.2)--(10.3).

On each compact interval \(K\), once \(N\) contains \(K\),

\[
 (u_N)_t=(u_N)_{xx}+iV u_N
 \tag{10.4}
\]

is uniformly bounded in \(L^2(I;H^{-1}(K))\).  Indeed the first term is
controlled by (10.3), while the untruncated polynomial is bounded on the
fixed compact set.  Together with the local \(L^2H^1\) bound,
Aubin--Lions gives, after a diagonal extraction,

\[
 u_N\to u
 \quad\text{strongly in }L^2(I\times K)
 \tag{10.5}
\]

for every compact \(K\).  This convergence is strong enough to pass
\(Vu_N\) locally.  Weak lower semicontinuity supplies the global
\(L^2H^1\) bound and an initial energy inequality.

For the limit equation, test with \(\eta_R^2u\), where \(\eta_R=1\) on
\([-R,R]\), is supported in \([-2R,2R]\), and
\(\|\eta_R'\|_\infty\lesssim R^{-1}\).  The real part of the potential
term is exactly zero.  The spatial boundary term obeys

\[
 \left|
 2\operatorname{Re}\int_{t_1}^{t_2}\!\int
 \eta_R\eta_R'u_x\overline u\,dx\,dt
 \right|
 \lesssim
 \frac1R
 \|u_x\|_{L^2((t_1,t_2)\times\mathbb R)}
 \|u\|_{L^2((t_1,t_2)\times\mathbb R)}
 \longrightarrow0.
 \tag{10.6}
\]

On compact sets, \(u_t\in L^2H^{-1}\), so Steklov averaging justifies the
localized energy test.  Sending \(R\to\infty\) gives

\[
 \|u(t_2)\|_2^2
 +2\int_{t_1}^{t_2}\|u_x(t)\|_2^2\,dt
 =\|u(t_1)\|_2^2.
 \tag{10.7}
\]

Applying the same identity to the difference of two solutions gives
uniqueness.  Distributional weak continuity, combined with the norm
continuity in (10.7), gives

\[
 u\in C(\overline I;L^2(\mathbb R)).
 \tag{10.8}
\]

Thus the separate truncation--compactness--cutoff argument constructs the
unique energy evolution for every \(L^2\) datum.  This analytic construction
is **PASS**.  It is logically separate from maximal graph coercivity.

### 10.2 Observability

For the constructed solution,

\[
 P_{c,\sigma}u=u_{xx}
 \quad\text{in }\mathcal D'(I\times\mathbb R).
 \tag{10.9}
\]

For every \(\phi\in H^1(\mathbb R)\),

\[
 |\langle u_{xx},\phi\rangle|
 =\left|\int_{\mathbb R}u_x\overline{\phi_x}\,dx\right|
 \le\|u_x\|_2\|\phi\|_{H^1}.
 \tag{10.10}
\]

Hence

\[
 \|u_{xx}\|_{H^{-1}}\le\|u_x\|_2.
 \tag{10.11}
\]

Substitution into (0.3) gives

\[
 \boxed{
 \|u\|_{L^2(I\times\mathbb R)}
 \le2C_T\|u_x\|_{L^2(I\times\mathbb R)}.}
 \tag{10.12}
\]

This observability conclusion is **PASS** for every constructed
\(L^2\)-data solution.

## 11. Energy identity and block contraction boundary

Membership in the maximal graph domain (1.3) does not by itself supply

\[
 u\in C(\overline I;L^2(\mathbb R))
 \tag{11.1}
\]

or the global energy law.  In particular, one may not silently split
\(u_t\) and the unbounded imaginary potential into separate
\(L^2H^{-1}\) terms and invoke the standard Lions trace theorem.  Therefore
block contraction for arbitrary maximal graph solutions is **not proved**.
Section 10 is the separate analytic step that supplies both properties for
the solution issued from every \(u_-\in L^2(\mathbb R)\).

For that constructed energy solution, let

\[
 E(t)=\|u(t)\|_2^2.
 \tag{11.2}
\]

Equation (10.7) makes \(E\) monotone.  It comes from the separate cutoff
energy argument, not from (1.3).  From (10.12),

\[
 \int_{-T}^TE(t)\,dt
 \le4C_T^2\int_{-T}^T\|u_x(t)\|_2^2\,dt.
 \tag{11.3}
\]

Monotonicity gives

\[
 \int_{-T}^TE(t)\,dt\ge2T E(T),
 \tag{11.4}
\]

while the energy inequality gives

\[
 2\int_{-T}^T\|u_x(t)\|_2^2\,dt
 \le E(-T)-E(T).
 \tag{11.5}
\]

Combining (11.3)--(11.5) yields

\[
 E(T)
 \le\frac{C_T^2}{T+C_T^2}E(-T),
 \tag{11.6}
\]

and therefore

\[
 \boxed{
 \|u(T)\|_2
 \le\frac{C_T}{\sqrt{T+C_T^2}}\|u(-T)\|_2.}
 \tag{11.7}
\]

Thus block contraction is **PASS for every \(L^2\) initial datum** through
the independently checked construction in Section 10.  The logical boundary
remains important: it is a theorem about the unique constructed energy
evolution, not an automatic property of every element of the maximal graph
space.

Equivalently, if \(U_{c,\sigma}(T,-T)\) denotes that evolution family, then

\[
 \sup_{c\in\mathbb R,\,\sigma\in\{-1,1\}}
 \|U_{c,\sigma}(T,-T)\|_{L^2\to L^2}
 \le\frac{C_T}{\sqrt{T+C_T^2}}<1.
 \tag{11.8}
\]

## 12. Short-time lower bound and compatibility

At \(c=0\), let

\[
 f_L(x)=L^{-1/2}f(x/L)
 \tag{12.1}
\]

for a fixed real normalized Schwartz function \(f\), and define

\[
 v_{T,L}(t,x)
 =f_L(x)
 \exp\!\left{
 i\sigma\bigl(tx^3+3t^2x-T^2x\bigr)
 \right}.
 \tag{12.2}
\]

Direct differentiation verifies

\[
 P_{0,\sigma}v_{T,L}=0.
 \tag{12.3}
\]

The odd-even time integrals give

\[
 \frac{\|(v_{T,L})_x\|_2^2}{\|v_{T,L}\|_2^2}
 =L^{-2}\|f'\|_2^2
 +3T^2L^4\|x^2f\|_2^2
 +\frac45T^4.
 \tag{12.4}
\]

Taking \(L=T^{-1/3}\) proves

\[
 C_T\ge c_fT^{-1/3}
 \qquad(0<T\le1).
 \tag{12.5}
\]

This is a **lower bound on every admissible graph constant**.  It is fully
compatible with (0.3), because (0.3) fixes \(T>0\) before asserting
uniformity in \(c\) and \(\sigma\).

The unit-chart partition proof may have worse small-time growth than
\(T^{-1/3}\).  Nothing in Sections 2--9 proves

\[
 C_T\lesssim T^{-1/3},
 \tag{12.6}
\]

and no sharp upper asymptotic is claimed.  If a future proof did match
(12.5), formula (11.7) would be consistent with a contraction gap of order
\(T^{5/3}\); that conditional scaling is not part of the present theorem.

## 13. Finite-certificate boundary

A finite exact certificate can independently recompute and compare the
algebraic data used in the proof, including

\[
 \mu_2,\quad \mu_4,\quad
 \kappa=\alpha^2(\mu_4-\mu_2^2)+\beta^2\mu_2,
 \quad
 \ell_p(t)=\beta(\mu_4+6t\mu_2),
 \tag{13.1}
\]

as well as the cell-translation coefficients, rational thresholds, file
hashes, and agreement of independent producers.

It does **not** machine-check the functional-analytic steps: weighted
Poincare, scalar compactness, the arbitrary-\(\lambda\delta\) limiting
argument, the infinite \(H^{-1}\) direct sum, maximal-domain localization,
nonautonomous evolution construction, Aubin--Lions compactness, the
cutoff-energy limit, uniqueness, or strong \(C_tL^2\) continuity.  Those
steps are established by the analytic proof and this independent audit, not
by a finite JSON ledger.  A formal release must keep this distinction
explicit.

## 14. Final claim boundary

The independently verified conclusions are:

1. For each fixed \(T>0\), the exact scalar cubic collision model has a
   whole-line graph constant uniform in \(c\) and \(\sigma\).
2. The separate analytic construction gives a unique
   \(C(\overline I;L^2)\cap L^2H^1\) energy solution for every \(L^2\)
   initial datum.
3. Those all-data solutions satisfy whole-line spacetime observability and
   a strict fixed-block contraction, uniformly in \(c\) and \(\sigma\).
4. The constant cannot be uniform as \(T\downarrow0\), and the present proof
   does not identify its sharp short-time upper behavior.

Maximal graph membership alone still does not imply a time trace or an
energy law; the all-data conclusion uses the separate construction in
Section 10.  This audit does **not** establish a periodic heat-path theorem,
control of higher-order model remainders, a nonlinear Navier--Stokes
closure, or any Clay-level regularity conclusion.  Those claims remain
outside R0.72V.
