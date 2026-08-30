# R0.73H proof: gain-normalized planar departure by harmonic energy localization

**Date:** 2026-08-30  
**Parent release:** R0.73G  
**Scope:** the exact periodic planar subsystem, the selected real
\(K_z=\pm1\) moving-bundle launch, and the family
\(\Lambda\to+\infty\)  
**Evidence class:** continuum theorem, conditional only on the certified
R0.73F moving-bundle theorem and its inherited R0.73C/R0.73E inputs

## 1. Statement

Let

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin 2x,
 \qquad W_d=W_{xx},
 \tag{1.1}
\]

and let

\[
 \overline U_\Lambda(t,y)
 =\bigl(0,0,2\Lambda W(4t,2y)\bigr).
 \tag{1.2}
\]

R0.73F supplies constants \(d_0,K_{\rm F},\alpha,\eta>0\) and a
moving unstable bundle on the real \(K_z=\pm1\) pair.  Put

\[
 r=\alpha+\eta>0.17035,
 \qquad D=\min\{d_0,1/450\},
 \qquad T=D/4.
 \tag{1.3}
\]

For every sufficiently large \(\Lambda\), choose the real unit
\(K_z=\pm1\) conjugate launch \(\phi_\Lambda\) constructed in R0.73G from
a normalized frozen top eigenvector at \(d=0\), and define

\[
 G_\Lambda
 =\|S_{1,\Lambda}(D,0)\phi_\Lambda\|_2.
 \tag{1.4}
\]

Then there is a number \(\delta_0>0\), independent of sufficiently large
\(\Lambda\), such that for every \(0<\delta\le\delta_0\) the exact
Navier--Stokes solution with perturbation, written below in profile time,

\[
 u_\Lambda^\delta(0)=\frac{\delta}{G_\Lambda}\phi_\Lambda
 \tag{1.5}
\]

is globally smooth and satisfies

\[
 \boxed{
 \|\Pi_{\{K_z=\pm1\}}u_\Lambda^\delta(D)\|_2
 \ge \frac\delta2.}
 \tag{1.6}
\]

The profile endpoint \(d=D\) is the physical time \(t=T=D/4\).

At the same time,

\[
 \boxed{
 \|u_\Lambda^\delta(0)\|_2
 \le K_{\rm F}\delta e^{-r\Lambda D}\longrightarrow0,}
 \tag{1.7}
\]

and the R0.73G smooth top-vector estimate also gives

\[
 \|u_\Lambda^\delta(0)\|_{H^3}
 \le C\delta\Lambda^2e^{-r\Lambda D}\longrightarrow0.
 \tag{1.8}
\]

This is a fixed-distance, family-level nonlinear departure.  The initial
scale is \(\delta/G_\Lambda\), normalized by the actual selected gain.
No matching asymptotic formula for \(G_\Lambda\) is proved here, so (1.6)
must not be restated for the prescribed seed
\(\delta e^{-r\Lambda D}\).  The backgrounds also vary with \(\Lambda\).

## 2. Exact planar equation and backward localization

Use physical velocity coordinates and profile time \(d=4t\).  Define

\[
 \mathcal B(f,g)=-\frac14\mathbb P[(f\cdot\nabla)g].
 \tag{2.1}
\]

The exact perturbation equation is

\[
 \partial_du=\mathcal L_\Lambda(d)u+\mathcal B(u,u),
 \qquad \nabla\cdot u=0.
 \tag{2.2}
\]

The factor in (2.1) is \(1/4\) because only time has been changed from
\(t\) to \(d=4t\).  In fast time \(\theta=\Lambda d\), the same factor is
\(\varepsilon_\nu/4\), where \(\varepsilon_\nu=\Lambda^{-1}\).  The
Taylor amplitude used below is a different parameter and is denoted by
\(\delta\).

The subspace

\[
 \mathcal S_{2D}
 =\{(0,u_2(y,z),u_3(y,z)):
 \partial_yu_2+\partial_zu_3=0\}
 \tag{2.3}
\]

is invariant.  Within this subspace the equation is the periodic
two-dimensional Navier--Stokes equation, so every smooth orbit used below
exists globally.

Set

\[
 a(d)=G_\Lambda^{-1}S_{1,\Lambda}(d,0)\phi_\Lambda.
 \tag{2.4}
\]

The selected orbit stays in the moving unstable fiber.  Applying the
R0.73F inverse-evolution bound from the endpoint \(D\) back to \(s\) gives

\[
 \boxed{
 \|a(s)\|_2\le K_{\rm F}e^{-r\Lambda(D-s)},
 \qquad 0\le s\le D,}
 \tag{2.5}
\]

and, by definition,

\[
 \|a(D)\|_2=1.
 \tag{2.6}
\]

Equation (2.5) is an upper bound on one normalized unstable orbit.  It is
not obtained by reversing an operator-norm lower bound.

## 3. Row energy and a strict doubled-row bound

For a nonzero \(K_z=q\) row, write \(\gamma=|q|/2\) and let \(v(x)\) be
its wall-normal profile in \(x=2y\).  Up to the exact row-dependent factor
that identifies profile energy with physical kinetic energy, put

\[
 E_\gamma(v)=\|v'\|_2^2+\gamma^2\|v\|_2^2.
 \tag{3.1}
\]

The inviscid numerical form is

\[
 \operatorname{Re}\langle A_\gamma(d)v,v\rangle_{E_\gamma}
 =\gamma\operatorname{Im}\int_{\mathbb T}
 W_x(d,x)v'(x)\overline{v(x)}\,dx.
 \tag{3.2}
\]

Consequently,

\[
 \omega_\gamma(d)
 \le\frac12\|W_x(d)\|_\infty\le\frac12.
 \tag{3.3}
\]

The \(q=0\) component generated later is a zero-mean tangential shear and
evolves by the heat equation.  The \(q=\pm2\) component needs a sharper
bound.

### 3.1 Gauge reduction at \(\gamma=1\)

For either sign \(\sigma\in\{-1,1\}\), completing the square gives

\[
 \begin{aligned}
 E_1(v)+3\sigma\operatorname{Im}\int W_xv'\bar v
 ={}&\left\|v'+\frac{3i\sigma}{2}W_xv\right\|_2^2\\
 &+\int\left(1-\frac94W_x^2\right)|v|^2.
 \end{aligned}
 \tag{3.4}
\]

Because \(W\) is periodic, the gauge
\(v=e^{-3i\sigma W/2}f\) is periodic and unitary.  Thus

\[
 E_1(v)+3\sigma\operatorname{Im}\int W_xv'\bar v
 =\langle H_df,f\rangle,
 \tag{3.5}
\]

where

\[
 H_d=-\partial_x^2+1-\frac94W_x(d,x)^2.
 \tag{3.6}
\]

It remains to prove \(H_d\ge0\) on \(0\le d\le D\).

### 3.2 Exact rational lower bound at \(d=0\)

At \(d=0\),

\[
 W_x(0,x)=-\frac12\cos x+\frac12\cos2x,
 \tag{3.7}
\]

and

\[
 \begin{aligned}
 1-\frac94W_x(0,x)^2
 ={}&\frac7{16}
 +\frac9{16}(\cos x+\cos3x)\\
 &-\frac9{32}(\cos2x+\cos4x).
 \end{aligned}
 \tag{3.8}
\]

Let \(P\) project onto \(|m|\le4\) and \(Q=I-P\).  In the ordered Fourier
basis \(m=-4,\ldots,4\), exact rational \(LDL^*\) elimination for
\(PH_0P-\frac15P\) has the positive pivots

\[
 \begin{gathered}
 \frac{1299}{80},\quad
 \frac{1279273}{138560},\quad
 \frac{1730627313}{409367360},\quad
 \frac{893977998489}{738400986880},\\
 \frac{2362447339523}{15892942195360},\quad
 \frac{164790587851929}{377991574323680},\quad
 \frac{280836393586857}{122067102112540},\\
 \frac{42494808061754213}{9985293994199360},\quad
 \frac{159556626958599229873}{13598338579761348160}.
 \end{gathered}
 \tag{3.9}
\]

Hence

\[
 PH_0P\ge\frac15P.
 \tag{3.10}
\]

The sum of the absolute nonconstant Fourier coefficients in (3.8) is
\(27/16\).  Therefore

\[
 QH_0Q\ge\left(25+\frac7{16}-\frac{27}{16}\right)Q
 =\frac{95}{4}Q,
 \tag{3.11}
\]

and

\[
 \|PH_0Q\|\le\frac{27}{16}.
 \tag{3.12}
\]

For \(f=p+q\), (3.10)--(3.12) reduce the lower bound to the exact matrix

\[
 \begin{pmatrix}
 1/5&-27/16\\
 -27/16&95/4
 \end{pmatrix}.
 \tag{3.13}
\]

After subtracting \(1/20\), its first pivot is \(3/20\) and its determinant
is

\[
 \frac3{20}\frac{237}{10}-\left(\frac{27}{16}\right)^2
 =\frac{4527}{6400}>0.
 \tag{3.14}
\]

Thus the infinite-dimensional operator satisfies

\[
 \boxed{H_0\ge\frac1{20}I.}
 \tag{3.15}
\]

The finite block in (3.9) is only one exact subcertificate inside the
analytic tail argument; it is not a Fourier-truncation proof of the PDE.

### 3.3 Persistence for \(0\le d\le D\)

The explicit two-harmonic profile gives

\[
 \|W_x(d)-W_x(0)\|_\infty
 \le\frac12\bigl[(1-e^{-d})+(1-e^{-4d})\bigr]
 \le\frac52d.
 \tag{3.16}
\]

Both \(\|W_x(d)\|_\infty\) and \(\|W_x(0)\|_\infty\) are at most one, so

\[
 \|W_x(d)^2-W_x(0)^2\|_\infty\le5d.
 \tag{3.17}
\]

For \(d\le1/450\),

\[
 \|H_d-H_0\|\le\frac94\,5d\le\frac1{40}.
 \tag{3.18}
\]

Equations (3.15) and (3.18) prove

\[
 H_d\ge\frac1{40}I>0,
 \qquad0\le d\le D.
 \tag{3.19}
\]

Returning through (3.4)--(3.6) yields

\[
 \boxed{
 \omega_1(d)\le\frac13,
 \qquad0\le d\le D.}
 \tag{3.20}
\]

The strict exponent budgets used below are

\[
 \frac13<2r,
 \qquad \frac12<3r,
 \qquad \frac12<4r.
 \tag{3.21}
\]

They follow already from \(r>0.17035\); the first two margins exceed
\(221/30000\) and \(221/20000\), respectively.

## 4. A Stieltjes localization lemma

The energy arguments use the following elementary form of exponential
localization.

**Lemma 4.1.**  Let \(a,b,c\ge0\), \(\Lambda>0\), and let
\(M:[0,D]\to[0,\infty)\) be nondecreasing with \(M(0)=0\).  Suppose

\[
 X(t)\le C_Xe^{-a\Lambda(D-t)},
 \qquad
 M(t)\le C_Me^{-b\Lambda(D-t)}.
 \tag{4.1}
\]

If \(c<a+b\), then

\[
 \int_{[0,s]}e^{c\Lambda(s-t)}X(t)\,dM(t)
 \le C_*e^{-(a+b)\Lambda(D-s)},
 \tag{4.2}
\]

where \(C_*\) depends on \(C_X,C_M,a,b,c\), but not on \(\Lambda\) or
\(s\).

**Proof.**  Insert the first bound in (4.1).  If \(a\ge c\), the remaining
weight is increasing in \(t\), and its endpoint times \(M(s)\) proves
(4.2).  If \(a<c\), Stieltjes integration by parts gives an endpoint term
plus

\[
 (c-a)\Lambda\int_0^s
 e^{c\Lambda(s-t)}e^{-a\Lambda(D-t)}M(t)\,dt.
 \tag{4.3}
\]

The second bound in (4.1) changes the integrand into the desired endpoint
envelope times
\(e^{-(a+b-c)\Lambda(s-t)}\).  Its integral is bounded because
\(a+b-c>0\).  \(\square\)

Repeated use of the same proof also applies when \(X\,dM\) is replaced by
a finite sum of product measures such as \(A\,dM_b+B\,dM_a\).

## 5. First-order kinetic energy and cumulative dissipation

For a planar field \(h\), write

\[
 Y_h(s)=\|h(s)\|_2^2,
 \qquad
 M_h(s)=\frac14\int_0^s\|\nabla h(\tau)\|_2^2\,d\tau.
 \tag{5.1}
\]

The fixed coefficient \(1/4\) is immaterial for the exponential rates but
keeps the slow-time dissipation exact.  From (2.5),

\[
 Y_a(s)\le K_{\rm F}^2e^{-2r\Lambda(D-s)}.
 \tag{5.2}
\]

The linear energy identity and (3.3) give

\[
 \frac12Y_a'(s)+\frac{dM_a}{ds}
 \le\frac\Lambda2Y_a(s).
 \tag{5.3}
\]

Integrating (5.3), then using (5.2), gives

\[
 \begin{aligned}
 M_a(s)
 &\le\frac12Y_a(0)+\frac\Lambda2\int_0^sY_a(\tau)\,d\tau\\
 &\le C_ae^{-2r\Lambda(D-s)}.
 \end{aligned}
 \tag{5.4}
\]

Hence

\[
 \boxed{
 Y_a(s)+M_a(s)
 \le C_ae^{-2r\Lambda(D-s)}.}
 \tag{5.5}
\]

No pointwise \(H^1\), uniform \(H^s\), or full-space sharp semigroup
bound has been used.

## 6. Exact harmonic hierarchy

Define

\[
 \begin{aligned}
 \partial_db&=\mathcal L_\Lambda(d)b+\mathcal B(a,a),
 &b(0)&=0,\\
 \partial_dc&=\mathcal L_\Lambda(d)c
 +\mathcal B(a,b)+\mathcal B(b,a),
 &c(0)&=0.
 \end{aligned}
 \tag{6.1}
\]

The background is independent of \(z\), so the linear evolution preserves
\(K_z\).  Fourier labels add under each bilinear interaction.  Starting
from \(K_z=\pm1\), induction gives

\[
 \boxed{
 \operatorname{supp}_{K_z}a\subset\{\pm1\},\quad
 \operatorname{supp}_{K_z}b\subset\{0,\pm2\},\quad
 \operatorname{supp}_{K_z}c\subset\{\pm1,\pm3\}.}
 \tag{6.2}
\]

The complete positive target return at cubic order contains the four
ordered paths

\[
 (1,0),\quad(0,1),\quad(-1,2),\quad(2,-1),
 \tag{6.3}
\]

plus their conjugates.  In particular,

\[
 \Pi_{\{K_z=\pm1\}}b=0.
 \tag{6.4}
\]

More generally, the coefficient of order \(j\) can contain only
\(-j,-j+2,\ldots,j-2,j\).  Therefore the target pair has no even-order
Taylor coefficient; after the cubic correction the next possible return is
quintic.

## 7. Localized quadratic and cubic coefficients

All fields in (6.1) are mean-zero planar fields.  Indeed, the initial
carrier has nonzero \(K_z\), every bilinear forcing is the divergence of a
periodic tensor, and the linearized background terms also have zero spatial
average because

 \[
 (\overline U_\Lambda\cdot\nabla)h
 =\nabla\cdot(h\otimes\overline U_\Lambda),
 \qquad
 (h\cdot\nabla)\overline U_\Lambda
 =\nabla\cdot(\overline U_\Lambda\otimes h).
 \tag{7.0}
\]

The exact perturbation \(u_\Lambda^\delta\) has the same conserved zero
mean.  Hence the approximate solution and the error \(e\) are also
mean-zero.  The homogeneous two-dimensional Ladyzhenskaya inequality gives

\[
 \|h\|_4^2\le C_L\|h\|_2\|\nabla h\|_2.
 \tag{7.1}
\]

### 7.1 Second order

Pair the first equation in (6.1) with \(b\).  After moving the derivative
onto \(b\), (7.1) and Young's inequality yield

\[
 \frac12dY_b+\frac12dM_b
 \le\frac13\Lambda Y_b\,ds+C Y_a\,dM_a.
 \tag{7.2}
\]

The zero row is purely dissipative and the doubled rows use (3.20), so the
same inequality controls their orthogonal sum.  Lemma 4.1 with squared
energy rate \(2/3\) and source exponent \(4r\) applies because
\(1/3<2r\).  It first gives the pointwise estimate; integration of (7.2)
then gives the cumulative dissipation estimate:

\[
 \boxed{
 Y_b(s)+M_b(s)
 \le C_be^{-4r\Lambda(D-s)}.}
 \tag{7.3}
\]

### 7.2 Third order

Let \(A=Y_a\) and \(B=Y_b\).  Pair the second equation in (6.1) with
\(c\).  Its forcing is controlled by

\[
 \|a\|_4\|b\|_4\|\nabla c\|_2.
 \tag{7.4}
\]

After Young's inequality, the source measure is bounded by

\[
 C\bigl(A\,dM_b+B\,dM_a\bigr).
 \tag{7.5}
\]

Equations (5.5), (7.3), and Lemma 4.1 give a cumulative envelope with
exponent \(6r\).  The rows \(K_z=\pm1,\pm3\) obey the universal bound
(3.3), and \(1/2<3r\).  Therefore

\[
 \boxed{
 Y_c(s)+M_c(s)
 \le C_ce^{-6r\Lambda(D-s)}.}
 \tag{7.6}
\]

## 8. Fourth-order exact remainder

For fixed \(0<\delta\le1\), set

\[
 u_{\rm app}=\delta a+\delta^2b+\delta^3c.
 \tag{8.1}
\]

Define the residual with the sign convention

\[
 R_{\rm app}
 =\mathcal L_\Lambda u_{\rm app}
 +\mathcal B(u_{\rm app},u_{\rm app})
 -\partial_du_{\rm app}.
 \tag{8.2}
\]

Substitution into (8.2) gives

\[
 \begin{aligned}
 R_{\rm app}={}&\delta^4[
 \mathcal B(a,c)+\mathcal B(c,a)+\mathcal B(b,b)]\\
 &+\delta^5[
 \mathcal B(b,c)+\mathcal B(c,b)]
 +\delta^6\mathcal B(c,c).
 \end{aligned}
 \tag{8.3}
\]

Let \(u_\Lambda^\delta\) solve (2.2) with (1.5), and put
\(e=u_\Lambda^\delta-u_{\rm app}\).  Since \(b(0)=c(0)=0\), one has
\(e(0)=0\).  The exact error equation is

\[
 \begin{aligned}
 \partial_de={}&\mathcal L_\Lambda e
+\mathcal B(u_{\rm app},e)+\mathcal B(e,u_{\rm app})
+\mathcal B(e,e)+R_{\rm app}.
 \end{aligned}
 \tag{8.4}
\]

Incompressibility gives the exact cancellations

\[
 \langle\mathcal B(u_{\rm app},e),e\rangle=0,
 \qquad
 \langle\mathcal B(e,e),e\rangle=0.
 \tag{8.5}
\]

The remaining transport term satisfies

\[
 |\langle\mathcal B(e,u_{\rm app}),e\rangle|
 \le\frac14\frac{dM_e}{ds}
 +C\|\nabla u_{\rm app}\|_2^2Y_e.
 \tag{8.6}
\]

Moreover, (5.5), (7.3), and (7.6) give

\[
 \int_0^D\|\nabla u_{\rm app}\|_2^2\,ds
 \le C(\delta^2+\delta^4+\delta^6)
 \le C\delta^2.
 \tag{8.7}
\]

Put \(g=\|\nabla u_{\rm app}\|_2^2\) and define the nondecreasing product
measures

\[
 \begin{aligned}
 dN_4&=Y_a\,dM_c+Y_c\,dM_a+Y_b\,dM_b,\\
 dN_5&=Y_b\,dM_c+Y_c\,dM_b,\\
 dN_6&=Y_c\,dM_c.
 \end{aligned}
 \tag{8.8}
\]

Ladyzhenskaya and Young applied to the fourth-, fifth-, and sixth-order
parts of (8.3) give respectively the measures
\(C\delta^8dN_4\), \(C\delta^{10}dN_5\), and
\(C\delta^{12}dN_6\).  Sections 5 and 7 imply

\[
 \begin{aligned}
 N_4(s)&\le C e^{-8r\Lambda(D-s)},\\
 N_5(s)&\le C e^{-10r\Lambda(D-s)},\\
 N_6(s)&\le C e^{-12r\Lambda(D-s)}.
 \end{aligned}
 \tag{8.9}
\]

The complete error inequality is therefore

\[
 \begin{aligned}
 \frac12dY_e+\frac12dM_e
 \le{}&\left(\frac\Lambda2+Cg\right)Y_e\,ds\\
 &+C\left(\delta^8dN_4+
 \delta^{10}dN_5+
 \delta^{12}dN_6\right).
 \end{aligned}
 \tag{8.10}
\]

All rows obey (3.3), and \(1/2<4r\).  After multiplying (8.10) by two,
the exact integrating factor from \(t\) to \(s\) is bounded by

\[
 \exp\left[\Lambda(s-t)+2C\int_t^sg(\tau)\,d\tau\right]
 \le e^{C_0\delta^2}e^{\Lambda(s-t)}
 \tag{8.11}
\]

by (8.7).  Lemma 4.1 applies to each measure in (8.9); its strict condition
for the leading source is \(1<8r\), equivalent to \(1/2<4r\).  It gives

\[
 Y_e(s)
 \le C_ee^{C_0\delta^2}\delta^8
 e^{-8r\Lambda(D-s)}.
 \tag{8.12}
\]

Finally, integrate (8.10).  The term
\(\Lambda\int_0^sY_e\) has the envelope in (8.12),
\(\int_0^sgY_e\le(\sup_{t\le s}Y_e(t))\int_0^sg\) has the same envelope
by (8.7), and the three source measures obey (8.9).  Hence

\[
 \boxed{
 Y_e(s)+M_e(s)
 \le C_ee^{C_0\delta^2}\delta^8
 e^{-8r\Lambda(D-s)}.}
 \tag{8.13}
\]

In particular,

\[
 \boxed{\|e(D)\|_2\le C_R\delta^4,}
 \tag{8.14}
\]

with \(C_R\) independent of sufficiently large \(\Lambda\) and of
\(0<\delta\le1\).

## 9. Target lower bound

At \(d=D\), (2.6), (6.4), (7.6), and (8.14) give

\[
 \begin{aligned}
 \|\Pi_{\{K_z=\pm1\}}u_\Lambda^\delta(D)\|_2
 &\ge\delta
 -\delta^3\|\Pi_{\{K_z=\pm1\}}c(D)\|_2
 -\|e(D)\|_2\\
 &\ge\delta-C_3\delta^3-C_R\delta^4.
 \end{aligned}
 \tag{9.1}
\]

Choose \(0<\delta_0\le1\) so that
\(C_3\delta_0^2+C_R\delta_0^3\le1/2\).  Then (1.6) follows.  Equations
(1.7)--(1.8) follow from the R0.73F gain lower bound and the R0.73G
top-vector Sobolev cost.  This completes the proof.

## 10. Exact boundary

The theorem closes all of the following:

- exact odd/even harmonic selection through cubic order;
- a continuum \(1/3\) numerical-abscissa bound on the doubled row;
- \(L^2\) and cumulative-dissipation localization of the first three
  Taylor coefficients;
- a fourth-order exact remainder controlled without uniform \(H^s\)
  propagation;
- fixed-distance nonlinear departure for the gain-normalized seed;
- global smoothness of every selected orbit.

It does not close any of the following:

- a sharp asymptotic formula or matching exponential action for
  \(G_\Lambda\);
- fixed-distance departure for the prescribed lower-law seed
  \(\delta e^{-r\Lambda D}\);
- one fixed background with a Lyapunov-instability sequence;
- a transverse \(K_x\ne0\) perturbation or nonzero first velocity
  component;
- three-dimensional vortex stretching, finite-time singularity, or the
  Clay alternative.

The fixed-distance result is a genuine nonlinear theorem, but it lies
inside an exactly invariant, globally regular two-dimensional subsystem.
