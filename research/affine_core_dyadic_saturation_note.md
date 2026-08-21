# R0.69U — Dyadic saturation of the affine-core boundary carrier

## 1. Result

R0.69T writes total vortex stretching as an absolutely summable signed
physical-space annular series and shows that the positive production inside a
constant-vorticity affine core is carried entirely by pairs that cross the
cutoff boundary.  Its first explicit cutoff produced the exploratory ratio

\[
 \Gamma_{\rm core}=0.996478\ldots,
\]

but one numerical field could not decide whether a scale-independent deficit
\(\Gamma_{\rm core}\le 1-\delta\) exists.

R0.69U gives a rigorous negative answer for the **core-restricted boundary
carrier**.  There is a radial cutoff \(q\in C^\infty([0,\infty))\), with

\[
 0\le q\le1,\qquad q=1\ \hbox{on }[0,1],\qquad
 q=0\ \hbox{on }[2,\infty),
 \tag{1.1}
\]

and a dyadic family of compactly supported smooth divergence-free fields

\[
 u_R=\nabla\times\bigl(q(|x|/R)B_A(x)\bigr),
 \qquad R=2^m,
 \tag{1.2}
\]

for which the affine core \(B_1\) has the fixed strain and vorticity

\[
 S=\frac1{\sqrt6}\operatorname{diag}(-1,-1,2),
 \qquad \omega_0=e_3.
 \tag{1.3}
\]

Let \(\mathcal C_j(R)\) denote the R0.69T signed annular carrier with the
\(x\)-integration restricted to \(B_1\).  Then, for all sufficiently large
dyadic \(R\), only \(j=m-1,m\) can contribute, both contributions are
strictly positive, and

\[
 \boxed{
 \Gamma_{\rm core}(R)
 :=\frac{|\sum_j\mathcal C_j(R)|}
 {\sum_j|\mathcal C_j(R)|}=1.}
 \tag{1.4}
\]

Thus no universal strict deficit can follow from static dyadic labels for the
core boundary carrier alone.

There is an equally important limitation.  The whole field obeys

\[
 u_R(x)=R\,u_1(x/R).
 \tag{1.5}
\]

Amplitude invariance together with the dyadic physical scaling from R0.69T
gives

\[
 \boxed{
 \mathcal A_{m+k}(u_R)=R^3\mathcal A_k(u_1),
 \qquad
 \Gamma_{\rm ann}(u_R)=\Gamma_{\rm ann}(u_1).}
 \tag{1.6}
\]

Consequently, moving a self-similar cutoff farther away saturates the
core-restricted observable but cannot improve or worsen the full-space
two-increment annular ratio.  A full-space saturating family must change
shape, not merely scale.

Equation (1.4) is not a global regularity or singularity theorem.  It does not
give \(\Gamma_{\rm ann}=1\), and it does not solve the Millennium Problem.

## 2. A smooth cutoff with a quantitative margin

The cutoff is built from a nonnegative symmetric transition density.  Put

\[
 a=\frac1{20},\qquad b=\frac{19}{20},\qquad L=b-a=\frac9{10},
\]

and, with \(z=(t-a)/L\), define the compactly supported probability density

\[
 h(t)=\frac{30}{L}z^2(1-z)^2\mathbf 1_{[a,b]}(t).
 \tag{2.1}
\]

Let \(\rho_\varepsilon\in C_c^\infty(-\varepsilon,\varepsilon)\) be any
nonnegative even mollifier of mass one, where \(0<\varepsilon<1/20\), and set

\[
 \eta=h*\rho_\varepsilon.
 \tag{2.2}
\]

Then \(\eta\in C_c^\infty(0,1)\), \(\eta\ge0\), it is symmetric about
\(1/2\), and \(\int_0^1\eta=1\).  Define

\[
 q(s)=
 \begin{cases}
 1,&s\le1,\\
 \displaystyle\int_{s-1}^{1}\eta(t)\,dt,&1<s<2,\\
 0,&s\ge2.
 \end{cases}
 \tag{2.3}
\]

Because \(\eta\) is supported away from the endpoints, this extension is
\(C^\infty\) and its derivatives are supported in a closed subinterval of
\((1,2)\).

The exact beta integrals and Young's convolution inequality give

\[
 \int h=1,
 \qquad
 \|h\|_2^2=\frac{100}{63},
 \qquad
 \|\eta\|_2^2\le\frac{100}{63}.
 \tag{2.4}
\]

Symmetry therefore yields the strict transition-energy bound

\[
 \boxed{
 E:=\int_1^2s\,q'(s)^2\,ds
 =\frac32\|\eta\|_2^2
 \le\frac{50}{21}<\frac52.}
 \tag{2.5}
\]

The numerical value of a chosen mollifier is irrelevant: the rational margin
\(5/2-50/21=5/42\) is already rigorous.

## 3. Exact affine field and core carrier

Write \(A=S+W\), where

\[
 W=\begin{pmatrix}0&-1/2&0\\1/2&0&0\\0&0&0\end{pmatrix},
 \qquad
 B_A(x)=-\frac13x\times(Ax).
 \tag{3.1}
\]

Then \(\operatorname{tr}A=0\), \(\nabla\times(Ax)=e_3\), and
\(\nabla\times B_A=Ax\).  Hence \(u_R=Ax\) wherever \(q(|x|/R)=1\).
In particular, on \(B_1\),

\[
 \omega_R=e_3,
 \qquad
 \omega_R\cdot S_R\omega_R=\frac2{\sqrt6}.
 \tag{3.2}
\]

With \(e=(y-x)/|y-x|\), let

\[
 J_R(x,y)=(e\cdot e_3)\bigl(e\cdot(\omega_R(y)\times e_3)\bigr).
 \tag{3.3}
\]

The core carrier is

\[
 \mathcal C_j(R)=\frac3{4\pi}
 \int_{B_1}\int_{\mathbb R^3}
 \psi_j(y-x)\frac{J_R(x,y)}{|x-y|^3}\,dy\,dx,
 \tag{3.4}
\]

where \(\psi_j(z)=q(2^{-j-1}|z|)-q(2^{-j}|z|)\).  The exact pointwise
Biot--Savart formula gives

\[
 \boxed{
 \sum_j\mathcal C_j(R)
 =|B_1|\frac2{\sqrt6}
 =\frac{8\pi}{3\sqrt6}}
 \tag{3.5}
\]

for every \(R>1\).  Constant-vorticity pairs vanish, so only the transition
region where \(q'\ne0\) can carry this value.

## 4. The two limiting annuli

Put \(y=Rsn\), with \(n\in\mathbb S^2\) and \(1<s<2\).  For fixed
\(x\in B_1\), the direction \((y-x)/|y-x|\) converges uniformly to \(n\).
The transverse part of the analytic vorticity formula gives

\[
 n_1(\omega_R)_2-n_2(\omega_R)_1
 =-\frac{s}{\sqrt6}n_3(1-n_3^2)
 \bigl(6q'(s)+sq''(s)\bigr)
 \tag{4.1}
\]

after the radial scaling is taken into account.  The factor \(s\) cancels
exactly with \(ds/s\) from \(dy/|y|^3\).  The angular moment is

\[
 \int_{\mathbb S^2}n_3^2(1-n_3^2)\,d\sigma(n)=\frac{8\pi}{15}.
 \tag{4.2}
\]

Because \(R=2^m\), the only limiting annular weights on \(1<s<2\) are

\[
 \psi_{m-1}(Rs)\longrightarrow q(s),
 \qquad
 \psi_m(Rs)\longrightarrow1-q(s).
 \tag{4.3}
\]

Define the two radial coefficients

\[
 I_-=-\int_1^2\bigl(6q'(s)+sq''(s)\bigr)q(s)\,ds,
 \qquad
 I_+=-\int_1^2\bigl(6q'(s)+sq''(s)\bigr)(1-q(s))\,ds.
 \tag{4.4}
\]

Two integrations by parts, using flatness at both endpoints, give the exact
identities

\[
 \boxed{
 I_-=\frac52+E,
 \qquad
 I_+=\frac52-E,
 \qquad
 I_-+I_+=5.}
 \tag{4.5}
\]

Combining (2.5) and (4.5),

\[
 I_+\ge\frac5{42}>0,
 \qquad
 I_->0.
 \tag{4.6}
\]

Dominated convergence now gives

\[
 \boxed{
 \begin{aligned}
 \mathcal C_{m-1}(2^m)&\longrightarrow
 |B_1|\frac{2}{5\sqrt6}\left(\frac52+E\right),\\
 \mathcal C_m(2^m)&\longrightarrow
 |B_1|\frac{2}{5\sqrt6}\left(\frac52-E\right).
 \end{aligned}}
 \tag{4.7}
\]

The derivative support of \(q\) stays a positive distance from \(s=1,2\).
For large \(m\), \(|2^msn-x|/2^m\) therefore remains strictly between one
and two on the entire carrier support.  Hence every annulus except
\(m-1,m\) vanishes exactly.  The strict positive limits in (4.7) imply that
both surviving terms are positive for all sufficiently large \(m\).  Equation
(1.4) follows from (3.5).

The limiting shares have the explicit safety margin

\[
 \frac{\lim\mathcal C_m}{\sum_j\mathcal C_j}
 =\frac12-\frac E5\ge\frac1{42},
 \qquad
 \frac{\lim\mathcal C_{m-1}}{\sum_j\mathcal C_j}
 \le\frac{41}{42}.
 \tag{4.8}
\]

## 5. Why this does not settle the full annular ratio

The same radial family is self-similar.  Homogeneity of \(B_A\) gives (1.5),
and therefore its vorticity and strain obey

\[
 \omega_R(x)=\omega_1(x/R),
 \qquad S_R(x)=S_1(x/R).
 \tag{5.1}
\]

After \(x=RX\), \(y=RY\), the full two-increment annular integral satisfies

\[
 \mathcal A_{m+k}(u_R)=R^3\mathcal A_k(u_1).
 \tag{5.2}
\]

Every signed shell and its absolute value receive the same factor.  Thus
\(\Gamma_{\rm ann}\) is constant along this family.  Core saturation is a
real obstruction to a core-only deficit, but it supplies no full-space
counterexample.

This distinction prevents a false conclusion: the transition shell occupies
volume \(O(R^3)\), so its own \(x\)-contribution to the full double integral
does not disappear when the boundary is moved outward.

## 6. Route decision

R0.69U closes two possibilities.

1. A universal strict cancellation factor cannot be derived from the static
   annular signs of the affine-core boundary carrier: a smooth compact family
   has \(\Gamma_{\rm core}=1\) for all sufficiently large dyadic radii.
2. Pure self-similar dilation cannot decide the full-space question, because
   \(\Gamma_{\rm ann}\) is exactly dilation invariant.

The next mathematically nonredundant target is therefore a **shape-changing
two-scale extension**: keep the affine core fixed, vary the transition law in
logarithmic radius, and audit the complete \(x,y\) double-increment integral.
Any claimed full-space saturation must include transition-transition pairs,
not only core-transition pairs.

## 7. Claim boundary

The new theorem is the dyadic saturation of the core-restricted boundary
carrier, the exact limiting coefficients (4.7), and the scale-invariance
obstruction (5.2).  The cutoff construction is smooth and quantitative; the
strict sign margin is rational and does not rely on floating-point
quadrature.

The theorem does not prove a universal statement about
\(\Gamma_{\rm ann}\), a dynamically propagated depletion mechanism, global
regularity, finite-time singularity, or a solution of the Millennium
Problem.  Its value is to remove a plausible but insufficient static route
before more computation is spent on it.
