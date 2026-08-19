# A width-\(10^{-40}\) global bound for the affine charge-weight family

## R0.52 research note

### Status

This note proves a global lower-and-upper bound for one two-parameter family
inside the reduced canonical edge generating system.  For the exact
degree-80 center and

\[
  \omega_s(c,\lambda)=c^s(1+\lambda |s|),
  \qquad c>0,\quad \lambda\ge 0,
\]

let \(R_{\mathrm{aff}}\) be the largest threshold radius obtained after
optimizing over the complete \((c,\lambda)\) domain.  The exact certificate
gives

\[
\frac{3826244718485988314760952288871012330925}{10^{40}}
<R_{\mathrm{aff}}<
\frac{3826244718485988314760952288871012330926}{10^{40}}.
\]

The interval width is exactly \(10^{-40}\).  A simultaneous active/zero
stationary root exists uniquely in the accompanying three-dimensional
rational box, is a strict constrained local maximum, and has every inactive
finite-charge and all-order sector strictly below one.  A separate eliminated
polynomial argument excludes every affine weight at the upper endpoint.

This is a theorem about the finite degree-80 reduced generating system.  It
does not identify the enclosed local root with the unique global maximizer as
an exact real number.  It does not optimize over every possible Banach weight,
control arbitrary three-dimensional divergence-free data, or prove or
disprove three-dimensional Navier--Stokes regularity.

---

## 1. Why R0.51 left a genuine two-constraint problem

R0.50 optimized the multiplicative character \(c^s\) globally.  R0.51 fixed
one rational affine correction and increased the certified threshold to

\[
  0.382624471846022<r_*^{(51)}<0.382624471846023.
\]

At that fixed weight the true \((j,s)=(81,162)\) column was active, while the
zero-charge sector was the nearest competitor.  The remaining gap was about
\(1.78\times10^{-5}\).  This suggested that further optimization should not
follow the active column alone: increasing the affine parameter helps that
column but eventually makes the zero sector active.

The R0.51 floating-point localization placed the balance near

\[
  r\approx0.3826244718485988,\qquad
  c\approx0.7975595104326214,\qquad
  \lambda\approx0.7653268804061606.
\]

Those decimals selected the rational audit box.  They do not decide any sign
in the proof.

---

## 2. The affine weight keeps algebra constant one

For every pair of integer charges \(a,b\),

\[
\begin{aligned}
1+\lambda|a+b|
&\le 1+\lambda|a|+\lambda|b|\\
&\le (1+\lambda|a|)(1+\lambda|b|).
\end{aligned}
\]

Consequently

\[
  \omega_{a+b}(c,\lambda)
  \le \omega_a(c,\lambda)\omega_b(c,\lambda)
\]

with algebra constant one throughout \(c>0,\lambda\ge0\).  The optimization
therefore changes the norm without paying an extra bilinear algebra constant.

For the positive active input charge \(s=162\), introduce

\[
  \alpha=\frac{\lambda}{1+162\lambda},\qquad
  \delta=1-162\alpha.
\]

Then

\[
  0\le\alpha<\frac1{162},\qquad
  \lambda=\frac{\alpha}{\delta},
\]

and every center charge satisfies \(q\ge-1\).  Hence

\[
  \frac{1+\lambda|162+q|}{1+162\lambda}
  =1+\alpha q.
\]

The active column becomes exactly linear in \(\alpha\).

---

## 3. Exact moment system

Let \(b_{iq}>0\) denote the active-column Laurent coefficients of the exact
degree-80 center and define

\[
  M_k(r,c)=\sum_{i,q} b_{iq}q^k r^i c^q,
  \qquad k=0,1,2.
\]

The active column is

\[
  B(r,c,\alpha)=M_0+\alpha M_1.
\]

For the zero sector, absorb its fixed degree and derivative factors into
positive coefficients \(z_{iq}\).  Define

\[
\begin{aligned}
U_0&=\sum_{i,q}z_{iq}r^ic^q,
&U_1&=\sum_{i,q}|q|z_{iq}r^ic^q,\\
T_0&=\sum_{i,q}qz_{iq}r^ic^q,
&T_1&=\sum_{i,q}q|q|z_{iq}r^ic^q.
\end{aligned}
\]

Its column is

\[
  Z(r,c,\alpha)
  =U_0+\frac{\alpha}{\delta}U_1.
\]

Writing \(t=\log c\), a simultaneous active/zero stationary point satisfies

\[
  B=1,\qquad Z=1,\qquad
  (\partial_tB)(\partial_\alpha Z)
  -(\partial_\alpha B)(\partial_t Z)=0.
\]

Multiplication by positive Laurent-clearing factors gives the exact system

\[
\begin{aligned}
F&=c(M_0+\alpha M_1-1),\\
G&=c\{\delta(U_0-1)+\alpha U_1\},\\
H&=c^2\{(M_1+\alpha M_2)U_1
       -\delta^2M_1T_0-\alpha\delta M_1T_1\}.
\end{aligned}
\]

In particular,

\[
  H=c^2\delta^2
  \bigl[(\partial_tB)(\partial_\alpha Z)
  -(\partial_\alpha B)(\partial_tZ)\bigr].
\]

No numerical differentiation enters this system.

---

## 4. Exact simultaneous root box

The pinned box is

\[
\begin{aligned}
0.3826244718485988314760952288871012330925
&<r<
0.3826244718485988314760952288871012330926,\\
0.7975595104326214175951774729017091063394
&<c<
0.7975595104326214175951774729017091063395,\\
0.0061234500552300731923346973685049743915
&<\alpha<
0.0061234500552300731923346973685049743916.
\end{aligned}
\]

The corresponding \(\lambda\) interval is obtained exactly from
\(\lambda=\alpha/(1-162\alpha)\).  Its decimal midpoint is approximately

\[
  \lambda=0.76532688040616062504794984396180944069\ldots.
\]

At the rational box midpoint I form the exact Jacobian \(J_0\), invert it over
GMP rationals, and evaluate an interval Jacobian \([J(X)]\) over the complete
box.  With \(Y=J_0^{-1}\), the Krawczyk operator is

\[
  K(x_0,X)=x_0-Yf(x_0)+\{I-Y[J(X)]\}(X-x_0).
\]

All three Krawczyk image radii are below \(7.2\times10^{-79}\), while each
input-box width is \(10^{-40}\).  The exact image is strictly inside the box.
The Krawczyk theorem therefore gives existence and uniqueness of a zero of
\(F=G=H=0\) in this box.

The high-precision diagnostic localization is

\[
\begin{aligned}
r&=0.3826244718485988314760952288871012330925739415578\ldots,\\
c&=0.7975595104326214175951774729017091063394333241328\ldots,\\
\alpha&=0.0061234500552300731923346973685049743915742891620\ldots,\\
\lambda&=0.7653268804061606250479498439618094406929144059430\ldots.
\end{aligned}
\]

These values summarize the certified box; they are not proof endpoints.

---

## 5. The root is a strict constrained local maximum

I use the polynomialized inequalities \(F\le0\) and \(G\le0\).  At their
simultaneous root the determinant equation \(H=0\) supplies the missing KKT
stationarity relation.  Exact interval arithmetic gives positive multiplier
boxes with midpoint diagnostics

\[
  \mu\approx0.2613978758364294,qquad
  \nu\approx2.22569667150497\times10^{-5}.
\]

Thus strict complementarity holds.  The certified LICQ minor has lower bound
greater than \(261.21\).  On the one-dimensional critical tangent space I use

\[
  \tau=(0,G_\alpha,-G_c).
\]

The exact interval bound gives

\[
  \tau^T\{\mu\nabla^2F+\nu\nabla^2G\}\tau>1825.13.
\]

Since the objective is the linear coordinate \(r\), its Hessian vanishes and
the Lagrangian Hessian is strictly negative on the critical tangent.  This is
the strict second-order sufficient condition for a constrained local maximum.

---

## 6. Every inactive sector stays below one

The local root has two active equalities:

\[
  (j,s)=(81,162),\qquad s=0.
\]

For every other sector I bound \(r\), \(c^q\), and the affine ratio at exact
box endpoints.  Positivity makes the resulting coefficientwise envelopes
simultaneous over the complete root box.

The audit covers:

1. all 239 fixed positive charges \(2\le s<241\), using the exact convex
   degree endpoints;
2. the plus-one sector with its termwise all-degree bound;
3. the minus-one sector with a uniform derivative argument;
4. both infinite parity branches for \(s\ge241\), using the established
   Bernstein lattice theorem.

There are 242 inactive records after removing the two active equalities.  The
nearest inactive sector is

\[
  s=164,\qquad j=82,
\]

with the uniform upper bound

\[
  0.99985472349002423803\ldots,
\]

so its gap below one exceeds

\[
  1.4527650997576197\times10^{-4}.
\]

The former R0.51 bottleneck \(s=0\) is now exactly the second active
constraint; the next inactive bottleneck has a much larger certified gap.

---

## 7. Eliminating \(\alpha\) from global feasibility

It remains to exclude a larger threshold elsewhere in
\(c>0,\lambda\ge0\).  This is the step that turns the local certificate into a
global bound.

At the rational upper radius \(r_U\), the R0.50 global theorem implies

\[
  M_0(r_U,c)>1\qquad\text{for every }c>0,
\]

because \(r_U\) is strictly above the globally optimized multiplicative
threshold and \(M_0\) strictly increases in \(r\).

If an affine parameter were feasible at \(r_U\), then

\[
  M_1<0,\qquad U_0<1.
\]

Indeed, \(B=M_0+\alpha M_1\le1\) cannot hold with \(M_1\ge0\), and the
positive zero-sector correction forces \(U_0<1\).  The active inequality then
requires

\[
  \alpha\ge\frac{M_0-1}{-M_1},
\]

while the zero inequality requires

\[
  \alpha\le
  \frac{1-U_0}{U_1+162(1-U_0)}.
\]

Consequently feasibility implies

\[
\boxed{
E(r,c)=(-M_1)(1-U_0)
-(M_0-1)\{U_1+162(1-U_0)\}\ge0.
}
\]

For fixed rational \(r=r_U\), multiplication by \(c^2\) turns \(E\) into an
ordinary degree-316 polynomial.

---

## 8. Exact positive-axis sign theorem for \(E(r_U,c)\)

Let

\[
  Q(c)=c^2\partial_{\log c}E(r_U,c).
\]

The coefficient sequence of \(Q\) has exactly three sign variations.  By
Descartes' rule, \(Q\) has at most three positive roots, counted with
multiplicity.  The exact audit supplies three disjoint sign-changing boxes:

\[
\begin{aligned}
c_1&\in
(0.209259689509981531418051886110,
 0.209259689509981531418051886111),\\
c_2&\in
(0.7975595104326214175951774729017091063394,
 0.7975595104326214175951774729017091063395),\\
c_3&\in
(1.239043039314477659185496131618,
 1.239043039314477659185496131619).
\end{aligned}
\]

The endpoint signs are respectively \((- ,+)\), \((+,-)\), and \((- ,+)\).
There are therefore at least three distinct positive roots.  Descartes' upper
bound makes these all the positive roots and proves each is simple.  The
monotonicity pattern of \(E\) is consequently

\[
  \text{decreasing},\quad
  \text{increasing},\quad
  \text{decreasing},\quad
  \text{increasing}.
\]

Only \(c_2\) can be the relevant interior maximum.

Two elementary monotonic exclusions compactify the remaining domain:

- at \(c_L=0.1337\), \(U_0>1\) and \(T_0<0\); strict convexity in
  \(\log c\) gives \(U_0>1\) for every \(c\le c_L\);
- at \(c_U=0.803\), \(M_1>0\); since \(M_1\) strictly increases in
  \(\log c\), the active constraint is impossible for every \(c\ge c_U\).

On \([c_L,c_U]\), the only possible maxima are the two endpoints or the
\(c_2\) box.  Both endpoint values of \(c^2E\) are strictly negative.  On the
complete \(c_2\) box, all 317 exact Bernstein coefficients of \(c^2E\) are
negative; the largest is still below

\[
  -6.8068\times10^{-39}.
\]

It follows that

\[
  E(r_U,c)<0\qquad\text{for every }c>0.
\]

This contradicts the necessary feasibility inequality.  No affine weight is
feasible at \(r_U\).  Since both active columns strictly increase with \(r\),
no larger radius is feasible either.

---

## 9. Global enclosure and comparison

The Krawczyk root and inactive-sector theorem give a feasible affine threshold
strictly above the lower endpoint \(r_L\).  The eliminated feasibility theorem
excludes \(r_U\) and every larger radius.  Therefore

\[
  r_L<R_{\mathrm{aff}}<r_U,
  \qquad r_U-r_L=10^{-40}.
\]

Relative to the R0.51 upper root, the conservative gain factor is greater than

\[
  1.0000000000067320092\ldots.
\]

The extra improvement is only about \(6.732\times10^{-12}\) in relative
radius.  Its numerical size is not the main result.  The mathematical value is
that the complete two-parameter affine family is now bounded globally rather
than sampled, and that the limiting mechanism is proved to be the balance of
two exact all-order columns.

The width-\(10^{-40}\) interval is already far smaller than any numerical
interpretation justified by the reduced model.  I retain the interval rather
than claiming exact-real uniqueness: the present proof does not rule out a
different global maximizer whose radius lies inside the same tiny enclosure.

---

## 10. What this contributes, and what it does not

R0.52 contributes four exact facts inside the reduced system.

1. The active/zero balance is an actual simultaneous root, not a floating
   crossing.
2. The root is a strict constrained local maximum, not a saddle point.
3. Every inactive finite and all-order sector remains separated there.
4. The complete affine parameter domain has global optimum radius inside one
   rational interval of width \(10^{-40}\).

The result also closes the specific R0.51 question: continuing to tune
\((c,\lambda)\) inside this affine family cannot yield a materially larger
threshold.

Its relevance to the Millennium problem remains indirect.  The reduced edge
system does not yet supply a norm equivalence or a priori estimate for
arbitrary three-dimensional divergence-free velocity fields.  It suppresses
most Fourier interaction geometry and treats one exact finite center.  The
number \(R_{\mathrm{aff}}\) is not a regularity time, singularity location,
critical Reynolds number, or PDE threshold.

The next useful mathematical question is therefore not to add more decimal
places.  It is to test whether a substantially richer submultiplicative weight
family can preserve the same all-order closure, or whether the reduced model
can be connected to a scale-critical three-dimensional estimate.

---

## 11. Reproducibility and classification

The formal certificate is generated with GMP rationals.  The 100-digit
`mpmath` solve is diagnostic only.  Randomness and GPU arithmetic are absent.
The monitored command, source commit, certificate hash, wall time, CPU/RSS
trace, and figure provenance are recorded in the R0.52 certificate archive.

The certificate separates the claims as follows.

- **Formal exact finite theorem:** degree-80 construction, root box, Krawczyk
  inclusion, KKT/second-order test, inactive-sector envelopes, eliminated
  degree-316 polynomial, Descartes root count, and Bernstein sign.
- **All-order sector theorem reused:** fixed-charge convex endpoints,
  plus/minus exceptional sectors, and infinite large-charge parity branches.
- **Diagnostic only:** displayed 100-digit root approximation.
- **Not claimed:** exact uniqueness of the global maximizer, optimization over
  all Banach weights, a three-dimensional critical-space bridge, or a solution
  of the Navier--Stokes Millennium problem.
