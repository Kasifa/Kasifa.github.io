# R0.69V — Two-scale affine annuli: exact cubic law and asymptotic decoupling

## 1. Result

Let \(q\) be the quantitative smooth cutoff from R0.69U and put

\[
 U_R(x)=\nabla\times\bigl(q(|x|/R)B_A(x)\bigr),
 \qquad
 B_A(x)=-\frac13x\times(Ax).
 \tag{1.1}
\]

Thus \(U_R(x)=R\,U_1(x/R)\), its vorticity is \(e_3\) on \(B_R\),
and it vanishes outside \(B_{2R}\).  For

\[
 \varepsilon=2^{-N},\qquad 0\le a\le1,\qquad b=1-a,
 \tag{1.2}
\]

consider the genuinely two-scale family

\[
 \boxed{u_{\varepsilon,a}=aU_1+bU_\varepsilon.}
 \tag{1.3}
\]

On \(B_\varepsilon\), the two affine gradients add to
\((a+b)A=A\).  The inner core is therefore fixed.  At the same time the two
transition shells have radii comparable to \(\varepsilon\) and one.  Their
dimensionless radius ratio is \(1/\varepsilon=2^N\), which cannot be changed
by a common dilation.  Hence (1.3) leaves the single self-similar orbit from
R0.69U.

Write

\[
 \mathcal V(u)=\int_{\mathbb R^3}\omega_u\cdot S_u\omega_u\,dx
 \tag{1.4}
\]

and let \(V_q=\mathcal V(U_1)\).  There is a cutoff-dependent constant

\[
 C_q=\int_{\mathbb R^3}
 \left[\omega_q\cdot S\omega_q
       +2e_3\cdot S_q\omega_q\right]dx,
 \tag{1.5}
\]

where \(\omega_q=\nabla\times U_1\), \(S_q\) is the strain of \(U_1\), and
\(S=\operatorname{diag}(-1,-1,2)/\sqrt6\).  For every
\(0<\varepsilon\le1/2\),

\[
 \boxed{
 \mathcal V(u_{\varepsilon,a})
 =V_q\bigl(a^3+\varepsilon^3b^3\bigr)
  +\varepsilon^3ab^2C_q.}
 \tag{1.6}
\]

No \(a^2b\) term occurs.

Let \(\mathcal A_j(u)\) be the full-space two-increment physical annulus from
R0.69T and define

\[
 L_q=\sum_{j\in\mathbb Z}|\mathcal A_j(U_1)|,\qquad
 \Gamma_q=\frac{|V_q|}{L_q}.
 \tag{1.7}
\]

Then the two-scale family has the uniform asymptotic law

\[
 \boxed{
 \sup_{0\le a\le1}
 \left|\Gamma_{\rm ann}(u_{\varepsilon,a})-\Gamma_q\right|
 \longrightarrow0
 \quad(\varepsilon=2^{-N}\downarrow0).}
 \tag{1.8}
\]

Thus scale separation by itself cannot improve the limiting full-space
annular cancellation ratio, even though the radius ratio changes and the
fixed core is preserved.  A finite separation can still rearrange signs, so
(1.8) does not exclude a finite-\(N\) saturating parameter.

Equations (1.6) and (1.8) are not regularity or singularity theorems and do
not solve the Millennium Problem.

## 2. Exact cubic production law

For \(\varepsilon\le1/2\), the outer field is exactly affine on the whole
support of \(U_\varepsilon\):

\[
 \omega_1=e_3,\qquad S_1=S\qquad\hbox{on }B_{2\varepsilon}.
 \tag{2.1}
\]

After scaling the inner support by \(x=\varepsilon X\), write
\(\eta=\omega_q(X)\) and \(T=S_q(X)\).  Pointwise expansion gives

\[
\begin{aligned}
 &(ae_3+b\eta)\cdot(aS+bT)(ae_3+b\eta)\\
 &\quad=a^3e_3\cdot Se_3\\
 &\qquad+a^2b\left(2\eta\cdot Se_3+e_3\cdot Te_3\right)\\
 &\qquad+ab^2\left(\eta\cdot S\eta+2e_3\cdot T\eta\right)
 +b^3\eta\cdot T\eta.
\end{aligned}
\tag{2.2}
\]

Compact support and integration by parts imply

\[
 \int_{\mathbb R^3}\eta\,dX
 =\int_{\mathbb R^3}\nabla\times U_1\,dX=0,
 \qquad
 \int_{\mathbb R^3}e_3\cdot Te_3\,dX
 =\int_{\mathbb R^3}\partial_3(U_1)_3\,dX=0.
 \tag{2.3}
\]

The integral of the \(a^2b\) line is therefore exactly zero.  The last line
scales as \(\varepsilon^3b^3V_q\), the \(ab^2\) line gives
\(\varepsilon^3ab^2C_q\), and the outer field contributes \(a^3V_q\).
This proves (1.6).

For the balanced amplitude \(a=\varepsilon/(1+\varepsilon)\),
\(b=1/(1+\varepsilon)\), (1.6) becomes

\[
 \boxed{
 \mathcal V(u_{\varepsilon,\mathrm{bal}})
 =\frac{\varepsilon^3}{(1+\varepsilon)^3}
 \left(2V_q+\varepsilon C_q\right).}
 \tag{2.4}
\]

Deterministic axisymmetric Gauss audits of the fixed mollified profile give

\[
 V_q\approx1.95690,\qquad C_q\approx-2.80462,
 \tag{2.5}
\]

with the \(a^2b\) coefficient oscillating around zero at the radial
quadrature error scale.  These decimals diagnose the finite parameter
experiments; the exact vanishing in (2.3) does not depend on them.

## 3. Pure annular profiles

The R0.69U scaling law gives, for \(\varepsilon=2^{-N}\),

\[
 \mathcal A_{-N+k}(U_\varepsilon)
 =\varepsilon^3\mathcal A_k(U_1).
 \tag{3.1}
\]

Consequently the pure outer and inner parts of the two-scale annular
sequence are

\[
 a^3A,\qquad \varepsilon^3b^3\tau_NA,
 \quad
 A=(\mathcal A_j(U_1))_{j\in\mathbb Z},
 \tag{3.2}
\]

where \(\tau_N\) translates an \(\ell^1(\mathbb Z)\) sequence by \(N\)
indices.

For any \(A\in\ell^1(\mathbb Z)\), translations separate in \(\ell^1\):
uniformly for \(c,d\ge0\),

\[
 \bigl\|cA+d\tau_NA\bigr\|_{\ell^1}
 =(c+d)\|A\|_{\ell^1}+o(c+d).
 \tag{3.3}
\]

Indeed, approximate \(A\) in \(\ell^1\) by a finitely supported sequence.
For a sufficiently large translation the two finite supports are disjoint,
where equality is exact; the discarded tails cost at most a uniform
multiple of their \(\ell^1\) norm.

## 4. Uniform control of all mixed annuli

Expand the symmetric R0.69T two-increment kernel cubically in the outer and
inner vorticities.  Denote the sum of all \(a^2b\) and \(ab^2\) annular
pieces by \(X_{\varepsilon,a}\).

The annular partition is nonnegative.  Therefore any mixed kernel \(F\)
satisfies

\[
 \sum_j\left|\iint\psi_j(y-x)F(x,y)\,dy\,dx\right|
 \le\iint|F(x,y)|\,dy\,dx.
 \tag{4.1}
\]

A mixed term requires at least one point in \(B_{2\varepsilon}\).  For
\(\varepsilon\le1/4\), the inner support is separated from the outer
transition shell.  If the
other point lies in \(B_1\), the outer vorticity increment vanishes.  The
only logarithmic radial integral is then
\(\int_{2\varepsilon}^{1}dr/r\), and it multiplies \(ab^2\).  If the other
point lies in the outer transition shell, its distance from
\(B_{2\varepsilon}\) is bounded below and the remaining mixed terms cost
only the small volume \(O(\varepsilon^3)\).  Hence

\[
 \boxed{
 \|X_{\varepsilon,a}\|_{\ell^1}
 \le C_q^\ast\varepsilon^3
 \left[
   ab^2\bigl(1+\log(1/\varepsilon)\bigr)+a^2b
 \right].}
 \tag{4.2}
\]

Put

\[
 M_{\varepsilon,a}=a^3+\varepsilon^3b^3.
 \tag{4.3}
\]

If \(0<a,b<1\), set \(t=a/(\varepsilon b)\).  Then

\[
 \frac{\varepsilon^3ab^2}{M_{\varepsilon,a}}
 =\frac{\varepsilon t}{1+t^3},
 \qquad
 \frac{\varepsilon^3a^2b}{M_{\varepsilon,a}}
 =\frac{\varepsilon^2t^2}{1+t^3}.
 \tag{4.4}
\]

Both rational functions of \(t\) are uniformly bounded.  The endpoint cases
\(a=0,1\) have no mixed term.  Thus

\[
 \sup_{0\le a\le1}
 \frac{\|X_{\varepsilon,a}\|_{\ell^1}}{M_{\varepsilon,a}}
 \le C_q^{\ast\ast}\varepsilon\bigl(1+\log(1/\varepsilon)\bigr)
 \longrightarrow0.
 \tag{4.5}
\]

Combining (3.2), (3.3), and (4.5) gives

\[
 \sum_j|\mathcal A_j(u_{\varepsilon,a})|
 =M_{\varepsilon,a}L_q+o(M_{\varepsilon,a})
 \tag{4.6}
\]

uniformly in \(a\).  The signed sum is

\[
 \sum_j\mathcal A_j(u_{\varepsilon,a})
 =M_{\varepsilon,a}V_q+o(M_{\varepsilon,a}),
 \tag{4.7}
\]

also directly visible in (1.6).  Division proves (1.8).

## 5. Finite-separation audit

The asymptotic theorem does not decide whether a finite value of \(N\) and
\(a\) aligns all important annular signs.  R0.69V therefore uses two
independent numerical estimators.

1. A radial-zone point-pair estimator covers every unordered pair of
   inner core, inner transition, intermediate plateau, and outer transition
   zones.  It provides an exact samplewise annular reconstruction but has
   high variance for rare close pairs in the outer transition.
2. An annulus-importance estimator samples \(x\) by radial zone and samples
   \(z=y-x\) directly in the support
   \(2^j<|z|<2^{j+2}\).  Pair symmetry retains only the ordered radial half
   and doubles distinct-zone pairs.  It records every transition--transition
   contribution without treating fine annuli as rare events.

The first lower-resolution balanced-amplitude run reported a ratio of annular
means near \(0.999\), but its sampled signed sum missed the independently
known production by a material fraction.  That number is therefore retained
only as a variance diagnostic.  In the final scan the numerator is never
estimated from the point-pair samples: it is supplied by the exact cubic law
(1.6).

At \(N=2\), a source-locked common-sample cubic run used sixteen independent
scrambles and \(2^{18}\) points in each annulus--zone stratum, for
\(167{,}772{,}160\) stratified point pairs.  Four amplitude nodes reconstruct
every annular carrier as a cubic at sample level.  The best point on a
4001-point grid was

\[
 a=0.1595,\qquad
 \frac{|\mathcal V_{\rm exact}|}
      {\sum_j|\widehat{\mathcal A}_j|}
 =0.9635537.
 \tag{5.1}
\]

The sampled signed sum at this amplitude was within \(0.023\) reported
scramble standard errors of the exact cubic numerator.  One mean annulus was
still negative, but the importance parameterization had relatively large
variance on the coarse outer-transition self-pairs.

An independent direct zone-pair run therefore sampled every one of the ten
unordered radial-zone pairs with sixteen scrambles and \(2^{19}\) points per
pair.  At the same amplitude it gave

\[
 \widehat{\mathcal A}_0
 =-6.2918609\times10^{-4},\qquad
 {\rm SE}=1.0343137\times10^{-5},
 \tag{5.2}
\]

placing the negative mean about 61 reported standard errors from zero.  The
dominant contribution is the outer-transition--outer-transition pair.

Finally, a second common-sample cubic audit used the direct zone-pair
parameterization to reconstruct only \(\mathcal A_{-2}(a)\) and
\(\mathcal A_0(a)\).  Its \(j=0\) mean polynomial is

\[
 \widehat{\mathcal A}_0(a)
 =a\left(-0.0016401859
          +0.0041314598a
          -0.1360513164a^2\right).
 \tag{5.3}
\]

The quadratic factor has negative mean discriminant and negative leading
coefficient.  At \(a=0\), where \(\mathcal A_0=0\) by support,

\[
 \widehat{\mathcal A}_{-2}(0)
 =-0.0019467840,qquad
 {\rm SE}=8.6779726\times10^{-5}.
 \tag{5.4}
\]

No point of the 4001-point grid makes both mean carriers nonnegative.  The
maximized minimum is still \(-2.9486752\times10^{-4}\) at \(a=0.107\), and
at every grid point at least one pointwise 95% upper scramble band is below
zero.  These bands are neither simultaneous nor rigorous interval
enclosures; (5.2)--(5.4) identify a sharply localized certification target,
not a proved finite-parameter sign obstruction.

## 6. Route decision

R0.69V establishes two exact facts and one numerical route decision.

1. The fixed-core two-scale construction genuinely changes shape and has an
   exact cubic production law.
2. Sending the two scales infinitely far apart cannot improve the limiting
   full-space annular ratio: all amplitude choices return to the single-profile
   value \(\Gamma_q\).
3. At the most favorable tested finite separation, the corrected
   exact-numerator scan does not saturate, and an independent estimator finds
   a robust negative coarse annulus.  The earlier near-one screening value was
   a variance artifact, not evidence of exact sign alignment.

The next nonredundant task, R0.69W, is not another broad parameter scan.  It is
the rigorous enclosure of the four quantities isolated by (5.3)--(5.4): the
three nonzero coefficients of \(\mathcal A_0(a)/a\) and the constant
\(\mathcal A_{-2}(0)\).  If interval arithmetic proves that the quadratic
factor in (5.3) has negative leading coefficient and negative discriminant,
then \(\mathcal A_0(a)<0\) for every \(a>0\); a certified negative value in
(5.4) handles \(a=0\).  That would close exact one-sign saturation throughout
this one-parameter, separation-four family.  The interval construction must
also enclose the declared smooth mollification rather than silently certify
only its floating-point quadrature.

## 7. Claim boundary

The strict results are the shape criterion, exact production law (1.6), zero
\(a^2b\) coefficient, mixed-annulus estimate (4.2), and uniform decoupling
limit (1.8).  Equations (5.1)--(5.4), the grid exclusion, and all scramble
bands are randomized numerical evidence.  They are not interval enclosures
and do not yet prove a finite-parameter sign obstruction, exact annular
saturation, a dynamically propagated depletion mechanism, global regularity,
finite-time singularity, or the Millennium Problem.
