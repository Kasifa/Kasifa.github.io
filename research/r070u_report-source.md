# R0.70U — A fixed-frame square-root obstruction for the signed covariance remainder

**Status:** internal canonical candidate; not a public theorem chapter

**Release:** R0.70U

**Date:** 2026-08-25

## 1. Decision

R0.70T isolated the signed remainder

\[
 \mathfrak R_{\mathrm{sgn}}
 =-\int_{\mathbb T^3}u_*\cdot\mathcal A_L\,dx
  +\int_{\mathbb T^3}S:H\,dx+\mathfrak E_S.
 \tag{1.1}
\]

The first question for R0.70U is whether the near-rank residual

\[
 r=\operatorname{tr}H
 \tag{1.2}
\]

can control (1.1) at linear, or better than square-root, order while all
ordinary fixed-frequency norms and the top spectral gap stay bounded.

The answer is no.  For the fixed complete Littlewood--Paley frame of R0.70T,
there is a fixed three-frequency family of smooth, real, mean-zero,
divergence-free periodic vorticities \(\omega_\varepsilon\) such that

\[
 \|r_\varepsilon\|_{L^p}
 =\Theta(\varepsilon^2)
 \quad(1\leq p\leq\infty),
 \tag{1.3}
\]

but

\[
 \boxed{
 \mathfrak R_{\mathrm{sgn}}(\omega_\varepsilon)
 =c_0\varepsilon+O(\varepsilon^2),
 \qquad c_0\ne0.}
 \tag{1.4}
\]

The frequencies do not move as \(\varepsilon\to0\).  The family has a
uniform global simple-top gap, and every fixed Sobolev norm of its vorticity,
Biot--Savart velocity, and strain remains bounded.  Consequently, no estimate

\[
 |\mathfrak R_{\mathrm{sgn}}|
 \leq F_\varepsilon\|r\|_{L^p}^{\theta}
 \tag{1.5}
\]

can hold along the family when \(\theta>1/2\) and the prefactor
\(F_\varepsilon\) stays locally bounded.  This includes a linear
residual-only bound and any bounded-weight estimate based on
\(\int W r\).

The exponent \(1/2\) is not excluded.  Nor does this release exclude control
by the projector derivative, a stretching commutator square, the explicit
cross-scale tensor \(\omega\otimes\omega-Q\), or cancellation after time
integration.  The route decision is therefore:

1. stop the linear residual-only signed-closure route;
2. treat square-root order as the sharp algebraic frontier exposed by this
   family;
3. retain the cross-scale tensor or a comparable coherence quantity in the
   next estimate rather than compressing it to \(r\) alone.

This is an obstruction theorem for one proposed estimate.  It is not an
enstrophy closure, a singularity construction, a global-regularity theorem,
or a solution of the Millennium problem.  The family is used at one time;
no long-time Navier--Stokes behavior is inferred.  No DNS or DGX computation
is justified for this exact algebraic gate.  No public-page update or GitHub
publication is authorized by this report.

## 2. Conventions and exact signed compression

Work on the normalized torus

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3,
 \qquad \int_{\mathbb T^3}1\,dx=1.
 \tag{2.1}
\]

Let \(u_*\) be the mean-zero Biot--Savart velocity of a smooth mean-zero
divergence-free vorticity \(\omega\), and write

\[
 B_{ij}=\partial_i u_{*,j},
 \qquad S=\frac12(B+B^{\mathsf T}).
 \tag{2.2}
\]

Use the pinned complete scalar frame

\[
 \mathscr T=\{T_\star=\Pi_0\}\cup\{T_j:j\in\mathbb Z\},
 \qquad
 \widehat{T_jf}(k)=\varphi(2^{-j}k)\widehat f(k)
 \quad(k\ne0),
 \tag{2.3}
\]

where \(\varphi\) is real, even, radial, and smooth, with

\[
 \operatorname{supp}\varphi
 \subset\{\tfrac12<|\xi|<2\},
 \qquad
 \sum_{j\in\mathbb Z}|\varphi(2^{-j}\xi)|^2=1
 \quad(\xi\ne0).
 \tag{2.4}
\]

Put

\[
 \Omega_\alpha=T_\alpha\omega,
 \qquad
 Q=\sum_\alpha\Omega_\alpha\otimes\Omega_\alpha.
 \tag{2.5}
\]

At a simple top eigenvalue, write

\[
 Q=\lambda L+H,
 \qquad L=\ell\otimes\ell,
 \qquad P=I-L,
 \qquad H=PQP,
 \qquad r=\operatorname{tr}H.
 \tag{2.6}
\]

The orientation-free longitudinal defect is

\[
 \mathcal A_L
 =L\bigl(\nabla\lambda+2\lambda\operatorname{div}L\bigr).
 \tag{2.7}
\]

R0.70T proved the complete-frame stretching identity

\[
 \int\omega\cdot S\omega\,dx
 =\int S:Q\,dx+\mathfrak E_S,
 \tag{2.8}
\]

with

\[
 \mathfrak E_S
 =\sum_\alpha
 \langle\Omega_\alpha,[T_\alpha,S]\omega\rangle.
 \tag{2.9}
\]

### Proposition 2.1 — exact compression

Under the preceding hypotheses,

\[
 \boxed{
 \mathfrak E_S
 =\int S:(\omega\otimes\omega-Q)\,dx,}
 \tag{2.10}
\]

and therefore

\[
 \boxed{
 \mathfrak R_{\mathrm{sgn}}
 =-\int u_*\cdot\mathcal A_L\,dx
  +\int S:(\omega\otimes\omega-\lambda L)\,dx.}
 \tag{2.11}
\]

#### Proof

Since \(S\) is symmetric,

\[
 \int\omega\cdot S\omega\,dx
 =\int S:(\omega\otimes\omega)\,dx.
 \tag{2.12}
\]

Subtracting \(\int S:Q\) from (2.8) gives (2.10).  Using
\(Q=\lambda L+H\),

\[
 \int S:H+\mathfrak E_S
 =\int S:\bigl[H+\omega\otimes\omega-Q\bigr]
 =\int S:(\omega\otimes\omega-\lambda L),
 \tag{2.13}
\]

which gives (2.11).  This is an exact compression, not an estimate. \(\square\)

## 3. A fixed Pythagorean triad

Let \(m\ge2\) be an integer and define

\[
 a=m^2-1,
 \qquad b=2m,
 \qquad K=m^2+1.
 \tag{3.1}
\]

Then

\[
 a^2+b^2=K^2.
 \tag{3.2}
\]

Use the frequencies

\[
 k=(a,b,0),
 \qquad p=(a,-b,0),
 \qquad q=k+p=(2a,0,0),
 \tag{3.3}
\]

so \(|k|=|p|=K\) and \(|q|=2a=2K-4\).  Put

\[
 n_k=\frac1K(-b,a,0).
 \tag{3.4}
\]

Fix amplitudes

\[
 A>\delta>0
 \tag{3.5}
\]

and define, with \(\theta=k\cdot x\), \(\phi=p\cdot x\), and
\(\psi=q\cdot x=\theta+\phi\),

\[
 w_1
 =A\bigl[n_k\cos\theta+e_3\sin\theta\bigr],
 \tag{3.6}
\]

\[
 w_2=\delta e_3\cos\phi,
 \qquad
 w=w_1+w_2,
 \qquad
 h=e_2\cos\psi,
 \tag{3.7}
\]

and

\[
 \omega_\varepsilon=w+\varepsilon h.
 \tag{3.8}
\]

All these fields are real, smooth, mean zero, periodic, and divergence free.
Moreover,

\[
 |w_1|=A,
 \qquad
 |w|\ge A-\delta=:g_0>0.
 \tag{3.9}
\]

They are genuine vorticities.  Their mean-zero Biot--Savart velocities are

\[
 u_w
 =-\frac A K
   \bigl[n_k\cos\theta+e_3\sin\theta\bigr]
  +\frac{\delta}{K^2}(b,a,0)\sin\phi,
 \tag{3.10}
\]

\[
 u_h=-\frac1{2a}e_3\sin\psi,
 \qquad
 u_\varepsilon=u_w+\varepsilon u_h.
 \tag{3.11}
\]

Indeed, \(\nabla\times w_1=-Kw_1\), while direct differentiation gives
\(\nabla\times u_w=w\) and \(\nabla\times u_h=h\).  Thus
\(\omega_\varepsilon\) is admissible smooth initial vorticity for the
periodic Navier--Stokes equations.  The release uses only the instantaneous
field and does not assert that this particular finite Fourier form persists.

## 4. The fixed-frame overlap lemma

For \(r>0\), define the radial response vector

\[
 v(r)_j=\varphi(2^{-j}r e_1),
 \qquad j\in\mathbb Z.
 \tag{4.1}
\]

Tightness gives

\[
 \|v(r)\|_{\ell^2}=1.
 \tag{4.2}
\]

The strict annular support implies that \(v(r)\) has at most two nonzero
entries, and any two are adjacent.  The dyadic shift is exact:

\[
 v(2r)_j=v(r)_{j-1}.
 \tag{4.3}
\]

If the two possible entries of \(v(r)\) are \(x,y\), the only possible
overlap with the shifted vector is \(xy\).  Therefore

\[
 \bigl|\langle v(r),v(2r)\rangle\bigr|
 \le |xy|
 \le\frac{x^2+y^2}{2}
 =\frac12.
 \tag{4.4}
\]

For the triad, put

\[
 \gamma_m=\langle v(K),v(2a)\rangle.
 \tag{4.5}
\]

Because \(2a=2K-4\), smoothness and finite annular overlap give

\[
 \|v(2a)-v(2K)\|_{\ell^2}
 \le \frac{C_\varphi}{K}.
 \tag{4.6}
\]

For example, if \(M_\varphi=\|\nabla\varphi\|_\infty\), then for \(K\ge4\)
the mean-value theorem on the union of the two supports gives the sufficient
bound

\[
 \|v(2a)-v(2K)\|_{\ell^2}
 \le\frac{16M_\varphi}{K}.
 \tag{4.7}
\]

Combining (4.2), (4.4), and (4.6),

\[
 |\gamma_m|
 \le\frac12+\frac{C_\varphi}{K}.
 \tag{4.8}
\]

Hence, for every fixed pinned cutoff \(\varphi\), there is
\(m_0=m_0(\varphi)\) such that every integer \(m\ge m_0\) satisfies

\[
 |\gamma_m|\le\frac34.
 \tag{4.9}
\]

Fix one such \(m\) for the remainder of the release and abbreviate

\[
 \gamma=\gamma_m,
 \qquad
 \kappa=1-\gamma^2\ge\frac7{16},
 \qquad
 1-\gamma\ge\frac14.
 \tag{4.10}
\]

This is an analytic existence statement for the fixed cutoff.  Unless an
explicit formula for \(\varphi\) is supplied, neither this report nor the
finite certificate claims that a particular numerical value of \(m\) has
been evaluated.

## 5. Exact covariance and the quadratic residual

Write

\[
 c_j=\varphi(2^{-j}K e_1),
 \qquad
 d_j=\varphi(2^{-j}2a e_1).
 \tag{5.1}
\]

Both modes in \(w\) have radius \(K\), while \(h\) has radius \(2a\).
Therefore

\[
 T_jw=c_jw,
 \qquad
 T_jh=d_jh,
 \tag{5.2}
\]

and the constant block vanishes.  Using

\[
 \sum_jc_j^2=\sum_jd_j^2=1,
 \qquad
 \sum_jc_jd_j=\gamma,
 \tag{5.3}
\]

the covariance of \(\omega_\varepsilon\) is exactly

\[
 Q_\varepsilon
 =w\otimes w
  +\varepsilon\gamma(w\otimes h+h\otimes w)
  +\varepsilon^2h\otimes h.
 \tag{5.4}
\]

Set

\[
 z_\varepsilon=w+\varepsilon\gamma h.
 \tag{5.5}
\]

Then

\[
 \boxed{
 Q_\varepsilon
 =z_\varepsilon\otimes z_\varepsilon
  +\kappa\varepsilon^2h\otimes h.}
 \tag{5.6}
\]

At \(\varepsilon=0\), the covariance is the exact rank-one tensor
\(w\otimes w\), globally separated from zero by (3.9).

For this base state, \(\omega_0=w\) and hence
\(\omega_0\otimes\omega_0-Q_0=0\).  This is a property of the constructed
single-radius base, not a universal consequence of \(\operatorname{rank}Q=1\).
In particular, the stated frame assumptions do not require
\(\varphi\ge0\): algebraically \(\kappa=0\) permits both \(\gamma=1\) and
\(\gamma=-1\), and only the first makes the two physical/frame combinations
coincide.  No exact-rank universal cancellation is used below.

For

\[
 |\varepsilon|\le\frac{g_0}{4},
 \tag{5.7}
\]

one has \(|z_\varepsilon|\ge3g_0/4\).  Weyl's inequalities applied to
(5.6) give

\[
 \lambda_1(Q_\varepsilon)\ge\frac{9g_0^2}{16},
 \qquad
 \lambda_2(Q_\varepsilon)\le\frac{g_0^2}{16},
 \tag{5.8}
\]

and hence the uniform global gap

\[
 \lambda_1-\lambda_2\ge\frac{g_0^2}{2}.
 \tag{5.9}
\]

The tensor has rank at most two, so \(\lambda_3=0\) and
\(r_\varepsilon=\lambda_2\).  The product of its two possibly nonzero largest
eigenvalues is

\[
 \lambda_1\lambda_2
 =\kappa\varepsilon^2|z_\varepsilon\times h|^2
 =\kappa\varepsilon^2|w\times h|^2.
 \tag{5.10}
\]

Let

\[
 P_w=I-\frac{w\otimes w}{|w|^2}.
 \tag{5.11}
\]

The uniform lower bound (3.9) and (5.10) yield the uniform expansion

\[
 \boxed{
 r_\varepsilon
 =\kappa\varepsilon^2|P_wh|^2+O(|\varepsilon|^3).}
 \tag{5.12}
\]

At \(x_0=0\),

\[
 w(x_0)=\left(-\frac{Ab}{K},\frac{Aa}{K},\delta\right),
 \qquad h(x_0)=e_2,
 \tag{5.13}
\]

and

\[
 |w(x_0)\times h(x_0)|^2
 =\delta^2+\frac{A^2b^2}{K^2}>0.
 \tag{5.14}
\]

Thus \(|P_wh|^2\) is not identically zero.  From the uniform convergence in
(5.12), for every \(1\le p\le\infty\),

\[
 \lim_{\varepsilon\to0}
 \left\|\frac{r_\varepsilon}{\varepsilon^2}
       -\kappa|P_wh|^2\right\|_{L^p}=0,
 \tag{5.15}
\]

and therefore

\[
 \boxed{
 \|r_\varepsilon\|_{L^p}=\Theta(\varepsilon^2).}
 \tag{5.16}
\]

This is an \(L^p\) statement, not a positive pointwise lower bound: the
coefficient vanishes where \(h=0\).  Since
\(E_\varepsilon=\operatorname{tr}Q_\varepsilon\) stays uniformly above zero
and below infinity, the same order holds for \(r_\varepsilon/E_\varepsilon\).

## 6. The nonzero signed linear term

The physical covariance defect is exact:

\[
 \boxed{
 \omega_\varepsilon\otimes\omega_\varepsilon-Q_\varepsilon
 =\varepsilon(1-\gamma)
  (w\otimes h+h\otimes w).}
 \tag{6.1}
\]

Let \(S_w\) and \(S_h\) be the strains of (3.10) and (3.11), so

\[
 S_\varepsilon=S_w+\varepsilon S_h.
 \tag{6.2}
\]

The only first-order scalar needed below is

\[
 I=\int_{\mathbb T^3}h\cdot S_ww\,dx.
 \tag{6.3}
\]

### Lemma 6.1 — nonzero resonant coefficient

For the fields in Section 3,

\[
 \boxed{
 I=-\frac{A\delta a^2b}{2K^3}\ne0.}
 \tag{6.4}
\]

#### Proof

Since \(h=e_2\cos\psi\),

\[
 h\cdot S_ww
 =\frac12\cos\psi
 \left[(\partial_2u_w)\cdot w+(w\cdot\nabla)u_{w,2}\right].
 \tag{6.5}
\]

Terms formed from two \(k\)-modes or two \(p\)-modes have no Fourier
frequency \(q=k+p\) and integrate to zero against \(\cos\psi\).  The cross
terms inside the square brackets in (6.5) reduce to

\[
 -\frac{4A\delta a^2b}{K^3}\cos\theta\cos\phi.
 \tag{6.6}
\]

Finally,

\[
 \cos\theta\cos\phi
 =\frac12\bigl[\cos\psi+\cos(2bx_2)\bigr],
 \tag{6.7}
\]

and

\[
 \int_{\mathbb T^3}
 \cos\psi\cos\theta\cos\phi\,dx=\frac14.
\]

Thus (6.5)--(6.7) give (6.4). \(\square\)

From (2.10), (6.1), and (6.2), the only possible second-order term is
\(2\varepsilon^2(1-\gamma)\int h\cdot S_hw\).  Its Fourier frequencies do
not sum to zero, so it vanishes.  Therefore

\[
 \mathfrak E_S(\varepsilon)
 =2\varepsilon(1-\gamma)I
 \tag{6.8}
\]

and hence

\[
 \mathfrak E_S'(0)
 =-\frac{(1-\gamma)A\delta a^2b}{K^3}\ne0.
 \tag{6.9}
\]

It remains to show that the other two terms in (1.1) do not contain an
opposite linear contribution.  Define the exact-rank comparator

\[
 \widetilde Q_\varepsilon
 =z_\varepsilon\otimes z_\varepsilon.
 \tag{6.10}
\]

The field \(z_\varepsilon=w+\varepsilon\gamma h\) is divergence free and,
under (5.7), nowhere zero.  For a rank-one covariance generated by one
nowhere-zero divergence-free block, the R0.70T block identity gives

\[
 \mathcal A_L(\widetilde Q_\varepsilon)=0.
 \tag{6.11}
\]

Moreover,

\[
 \|Q_\varepsilon-\widetilde Q_\varepsilon\|_{C^1}
 =O(\varepsilon^2).
 \tag{6.12}
\]

On the uniformly gapped set (5.9), the maps from \((Q,\nabla Q)\) to the top
eigenvalue, top projector, its first derivative, and \(\mathcal A_L\) are
smooth.  Therefore

\[
 \|\mathcal A_{L_\varepsilon}\|_{C^0}
 =O(\varepsilon^2).
 \tag{6.13}
\]

Likewise, pointwise positivity gives

\[
 |H_\varepsilon|_F\le r_\varepsilon,
 \qquad
 \|H_\varepsilon\|_{C^0}=O(\varepsilon^2).
 \tag{6.14}
\]

The frequencies and amplitudes are fixed, so \(u_\varepsilon\) and
\(S_\varepsilon\) remain uniformly bounded in every fixed smooth norm.
Equations (6.8), (6.13), and (6.14) now give

\[
 \boxed{
 \mathfrak R_{\mathrm{sgn}}(\omega_\varepsilon)
 =-\frac{(1-\gamma)A\delta a^2b}{K^3}\varepsilon
  +O(\varepsilon^2).}
 \tag{6.15}
\]

The coefficient is nonzero by (3.1), (3.5), and (4.10).

## 7. Square-root obstruction theorem

### Theorem 7.1

Fix the frame (2.3)--(2.4), choose \(m\ge m_0(\varphi)\) as in Section 4,
and fix \(A>\delta>0\).  The family (3.8) has the following properties for
all sufficiently small nonzero \(\varepsilon\):

1. it is a smooth real mean-zero divergence-free periodic vorticity;
2. its covariance has a global simple top eigenvalue with the uniform gap
   (5.9);
3. every fixed Sobolev norm of \(\omega_\varepsilon\), \(u_\varepsilon\),
   and \(S_\varepsilon\), as well as every fixed inverse power of the top
   gap, is uniformly bounded;
4. for every \(1\le p\le\infty\),
   \(\|r_\varepsilon\|_{L^p}=\Theta(\varepsilon^2)\);
5. \(\mathfrak R_{\mathrm{sgn}}(\omega_\varepsilon)
   =c_0\varepsilon+O(\varepsilon^2)\) with \(c_0\ne0\).

Consequently, for any \(1\le p\le\infty\), any \(\theta>1/2\), and any
nonnegative prefactor family \(F_\varepsilon\) satisfying

\[
 \sup_{0<|\varepsilon|<\varepsilon_0}F_\varepsilon<\infty,
 \tag{7.1}
\]

the inequality

\[
 |\mathfrak R_{\mathrm{sgn}}(\omega_\varepsilon)|
 \le F_\varepsilon
      \|r_\varepsilon\|_{L^p}^{\theta}
 \tag{7.2}
\]

fails for every sufficiently small nonzero \(\varepsilon\).

#### Proof

Items 1--5 are Sections 3--6.  They give constants \(c,C>0\) such that

\[
 |\mathfrak R_{\mathrm{sgn}}(\omega_\varepsilon)|
 \ge c|\varepsilon|,
 \qquad
 \|r_\varepsilon\|_{L^p}
 \le C\varepsilon^2
 \tag{7.3}
\]

for all sufficiently small nonzero \(\varepsilon\).  A bounded right side in
(7.2) is \(O(|\varepsilon|^{2\theta})=o(|\varepsilon|)\) when
\(2\theta>1\), contradicting (7.3). \(\square\)

### Corollary 7.2 — linear and bounded-weight no-go

Theorem 7.1 rules out, along the same family, every estimate of the forms

\[
 |\mathfrak R_{\mathrm{sgn}}|
 \le F_\varepsilon\|r\|_{L^p},
 \tag{7.4}
\]

and

\[
 |\mathfrak R_{\mathrm{sgn}}|
 \le F_\varepsilon
 \left|\int_{\mathbb T^3}W_\varepsilon r\,dx\right|,
 \tag{7.5}
\]

whenever \(F_\varepsilon\) and \(\|W_\varepsilon\|_\infty\) stay bounded.
The same conclusion holds with \(r/E\) in place of \(r\).

More generally, if \(\Phi:[0,\infty)\to[0,\infty)\) satisfies

\[
 \Phi(s)=o(\sqrt{s})
 \qquad(s\downarrow0),
 \tag{7.6}
\]

then no estimate

\[
 |\mathfrak R_{\mathrm{sgn}}|
 \le F_\varepsilon\Phi(\|r\|_{L^p})
 \tag{7.7}
\]

holds along the family with locally bounded \(F_\varepsilon\).  Indeed,
\(\|r_\varepsilon\|_{L^p}=\Theta(\varepsilon^2)\), so the right side is
\(o(|\varepsilon|)\).

The phrase “locally bounded prefactor” is essential.  This theorem does not
exclude a coefficient that itself diverges at least like a negative power of
the residual, or a quantity that detects the order-\(\varepsilon\)
cross-scale defect.

## 8. What the obstruction means

The mechanism is not high-frequency growth.  Once \(m\) is selected from the
fixed frame, every Fourier frequency is fixed as \(\varepsilon\to0\).  The
mechanism is instead a mismatch between two quadratic objects:

\[
 r_\varepsilon
 \sim\varepsilon^2,
 \qquad
 \omega_\varepsilon\otimes\omega_\varepsilon-Q_\varepsilon
 \sim\varepsilon.
 \tag{8.1}
\]

The residual sees the second eigenvalue of a positive covariance and is
quadratic in the transverse amplitude.  The signed commutator sees a
cross-scale covariance defect and is linear in that amplitude.  Compressing
the latter to \(r\) necessarily loses a square root on this family.

The following routes remain open:

1. a genuinely critical estimate of order \(\|r\|^{1/2}\);
2. a bound retaining \(\omega\otimes\omega-Q\) or an equivalent paraproduct
   defect rather than only its positive spectral residual;
3. a derivative-sensitive estimate involving \(\mathcal J_P^{1/2}\) or the
   complete stretching commutator square \(\mathfrak C_S^{1/2}\);
4. cancellation after time integration, using the Navier--Stokes evolution
   rather than an instantaneous algebraic inequality.

The theorem does not rank these open routes by likelihood.  It only removes
the supercritical residual-only exponents \(\theta>1/2\).

## 9. Prior-art boundary

The closest filtered-stretching precedent located in the bounded primary-
source audit is
[Yu (2026)](https://arxiv.org/abs/2606.27560).  It studies filtered vorticity,
a local filtered enstrophy balance, and a differentiated subgrid stress
generated by a spatial convolution filter.  That stress is not the
multiplication commutator
\([T_j,S]\omega=T_j(S\omega)-ST_j\omega\) over the complete Parseval frame
used here, and the preprint does not introduce the covariance \(Q\), its top
projector, or \(r\).

[Yoneda--Goto--Tsuruhashi](https://arxiv.org/abs/2105.12459) formulate vortex
stretching through Littlewood--Paley shell interactions and triadic scale
transfer, while
[Bradshaw--Grujic](https://arxiv.org/abs/1501.01043) prove frequency-localized
regularity criteria.  These establish the surrounding LP route, but neither
contains the pointwise covariance rank or the residual-exponent obstruction
of Theorem 7.1.

The geometric-depletion line beginning with
[Constantin--Fefferman](https://iumj.org/article/3627/) concerns coherence of
the physical direction \(\omega/|\omega|\).  The critical one-half Holder
condition in
[Beirao da Veiga--Berselli](https://people.dm.unipi.it/beiraodaveiga/pdf/hbv-79.pdf)
is a spatial regularity exponent for that direction; it must not be
identified with the algebraic \(r^{1/2}\) frontier here.  The variable plane
in [Miller](https://arxiv.org/abs/2002.02152) is adjacent projector geometry,
but it is not required to be the top eigenspace of \(Q\), and its theorem does
not derive the transverse-vorticity condition from the present residual.

Helical and narrow-shell precedents provide a second boundary.
[Lei--Lin--Zhou](https://arxiv.org/abs/1505.00142) use helicity and Beltrami
structure for global solutions, and
[Miller](https://arxiv.org/abs/2005.14152) measures proximity to Laplacian
eigenfunctions by a Sobolev interpolation defect.  Neither defect is
\(r=\operatorname{tr}(PQP)\).  Classical triad analysis by
[Waleffe](https://ntrs.nasa.gov/citations/19920038608) does not use the fixed
frame response \(\gamma\), and the finite-mode classification of
[Kishimoto--Yoneda](https://arxiv.org/abs/2110.08039) reinforces an important
scope boundary: the field in Section 3 is an instantaneous smooth initial
datum, not a claimed finite-mode exact Navier--Stokes trajectory.

The Pythagorean Fourier triad, the rank-two eigenvalue expansion, and the
critical exponent comparison in this release are elementary exact
calculations.  They are not presented as a new general harmonic-analysis
principle.  In this bounded primary-source audit, no directly isomorphic
statement involving both
\(Q=\sum_jT_j\omega\otimes T_j\omega\) and a sharp exponent for
\(r=\operatorname{tr}(PQP)\) was identified.  That is a search result, not a
novelty or priority claim.  The route-specific result is the application of
the calculations to the pinned covariance remainder (1.1).  A publishable
PDE advance would still require a positive critical or time-integrated
estimate, or a substantially broader impossibility theorem.

## 10. Next gate

R0.70V should keep the first-order cross-scale object visible.  The immediate
candidate is the exact defect

\[
 \mathcal D_\times
 =\omega\otimes\omega-Q,
 \tag{10.1}
\]

for which

\[
 \mathfrak E_S=\int S:\mathcal D_\times\,dx.
 \tag{10.2}
\]

The next gate is not to reapply Cauchy--Schwarz blindly.  It is to determine
whether \(\mathcal D_\times\) admits an exact paraproduct decomposition whose
dangerous interactions can be paired with viscosity or integrated in time at
critical square-root order.  A useful positive result must expose its norm,
frequency weight, and time exponent explicitly; a useful negative result
must use actual common-vorticity fixed-frame fields and keep all proposed
prefactors bounded.

## 11. Claim boundary

What is proved:

- the exact signed compression (2.10)--(2.11);
- for every fixed pinned cutoff, analytic existence of a fixed triad with
  \(|\gamma|\le3/4\);
- the exact covariance factorization (5.6), a uniform global top gap, and the
  uniform residual expansion (5.12);
- the exact nonzero resonant coefficient (6.4);
- the signed asymptotic (6.15);
- the locally bounded no-go theorem for every \(\theta>1/2\), including
  linear residual-only and bounded-weight residual control.

What is not proved:

- a numerical value of \(m_0(\varphi)\) without an explicit cutoff;
- a pointwise positive lower bound for \(r_\varepsilon/\varepsilon^2\);
- failure of the critical exponent \(\theta=1/2\);
- a universal exact-rank cancellation theorem for sign-indefinite frame
  responses;
- failure of estimates involving \(\mathcal J_P^{1/2}\),
  \(\mathfrak C_S^{1/2}\), \(\mathcal D_\times\), or time cancellation;
- an a priori enstrophy estimate or continuation criterion verified from
  initial data;
- long-time persistence of the three-mode form;
- any finite-time singularity, unconditional global regularity, or solution
  of the Navier--Stokes Millennium problem.

The exact certificate for this release checks the finite Fourier, covariance,
spectral, and exponent algebra.  The arbitrary-cutoff overlap lemma, smooth
eigenprojector perturbation under a uniform gap, and the PDE interpretation
remain analytic arguments in this report.
