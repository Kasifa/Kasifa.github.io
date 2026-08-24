# R0.70W — A far-shell rank-one obstruction to projected area summation

**Status:** internal canonical candidate; not a public theorem chapter

**Release:** R0.70W

**Date:** 2026-08-25

## 1. Decision

R0.70V reduced the complete-frame stretching defect to

\[
 \mathfrak X_\times
 =\sum_{n\ne0}|n|^{-2}
  |\nu_n\times\widehat{\mathcal D_\times}(n)\nu_n|^2,
 \qquad \nu_n=\frac n{|n|},
 \tag{1.1}
\]

and proved a pairwise Fourier estimate in terms of polarization area. The
open question was whether those estimates survive summation and become a
norm of the physical covariance-area field

\[
 G_Q
 =\left(\sum_{\alpha<\beta}
   |\Omega_\alpha\times\Omega_\beta|^2\right)^{1/2}
 =\bigl(\lambda_1r+\lambda_2\lambda_3\bigr)^{1/2}.
 \tag{1.2}
\]

The answer for \(\mathfrak X_\times\) is no, even after restoring the two
inverse-frequency degrees required by scaling.

On the normalized three-torus, put

\[
 \begin{aligned}
 w(x)&=e_1\cos x_2-e_2\cos x_1,\\
 g(x)&=\cos(4x_3),\\
 h(x)&=g(x)w(x),\\
 \omega_\varepsilon(x)&=w(x)+\varepsilon h(x),
 \qquad \varepsilon\ne0.
 \end{aligned}
 \tag{1.3}
\]

The field \(w\) is supported on the radius-one lattice sphere and \(h\) is
supported on the radius-\(\sqrt{17}\) sphere. Since
\(\sqrt{17}>4\), the strict annular supports of their response vectors are
disjoint. Every complete-frame block is nevertheless pointwise parallel to
the same vector \(w(x)\). Consequently,

\[
 \boxed{
 Q_\varepsilon
 =(1+\varepsilon^2g^2)w\otimes w,
 \qquad
 \Omega_\alpha\times\Omega_\beta\equiv0,
 \qquad
 r\equiv0.}
 \tag{1.4}
\]

The frame defect is not zero:

\[
 \boxed{
 \mathcal D_{\times,\varepsilon}
 =2\varepsilon g\,w\otimes w.}
 \tag{1.5}
\]

Its only nonzero strain-projected outputs are

\[
 n=(\pm1,\pm1,\pm4),
 \tag{1.6}
\]

and exact Fourier summation gives

\[
 \boxed{
 \mathfrak X_{\times,\varepsilon}
 =\frac{2}{729}\varepsilon^2>0.}
 \tag{1.7}
\]

Thus no definite norm of \(G_Q\), of the fields
\(\Omega_\alpha\times\Omega_\beta\), or of any linear inverse-frequency
transform of those fields can control \(\mathfrak X_\times\) on the stated
class. In particular, the scale-correct candidate

\[
 \mathfrak X_\times^{1/2}
 \stackrel{?}{\le}
 C_\varphi\|G_Q\|_{L^{6/5}}
 \tag{1.8}
\]

is false. This is an information-loss obstruction, not a missing shell
weight: the proposed right side is identically zero before any weight is
applied.

There is an equally important boundary. In this sample,

\[
 \boxed{
 \mathfrak E_S(\omega_\varepsilon)
 =\int_{\mathbb T^3}S(\omega_\varepsilon):
   \mathcal D_{\times,\varepsilon}\,dx=0.}
 \tag{1.9}
\]

The Fourier supports of \(S(\omega_\varepsilon)\) and
\(\mathcal D_{\times,\varepsilon}\) are disjoint. Hence the counterexample
stops the route

\[
 \text{physical covariance area}
 \longrightarrow \mathfrak X_\times
 \longrightarrow |\mathfrak E_S|,
 \tag{1.10}
\]

but it does not stop a direct signed trilinear estimate for
\(\mathfrak E_S\). The next gate must retain the third Fourier frequency
and its sign from the start.

This release does not prove an enstrophy estimate, a continuation theorem,
a singularity, global regularity, or a solution of the Millennium problem.
The calculation is finite and exact. It does not justify DNS or a DGX run,
and it produces no formal numerical figure. No public-page update or
GitHub publication is authorized by this report.

## 2. Conventions

Work on

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3,
 \qquad \int_{\mathbb T^3}1\,dx=1,
 \tag{2.1}
\]

with Fourier convention

\[
 \widehat f(n)=\int_{\mathbb T^3}f(x)e^{-in\cdot x}\,dx,
 \qquad
 f(x)=\sum_{n\in\mathbb Z^3}\widehat f(n)e^{in\cdot x}.
 \tag{2.2}
\]

Let \(u\) be the mean-zero Biot--Savart velocity of a smooth, real,
mean-zero, divergence-free vorticity \(\omega\). Write

\[
 S=\frac12\bigl(\nabla u+(\nabla u)^{\mathsf T}\bigr).
 \tag{2.3}
\]

Use the pinned real-even complete scalar frame

\[
 \mathscr T=\{T_\star=\Pi_0\}\cup\{T_j:j\in\mathbb Z\},
 \qquad
 \sum_\alpha T_\alpha^2=I,
 \tag{2.4}
\]

whose nonconstant symbols are

\[
 m_j(n)=\varphi(2^{-j}n),
 \qquad
 \operatorname{supp}\varphi
 \subset\{\tfrac12<|\xi|<2\}.
 \tag{2.5}
\]

The cutoff is smooth, real, even, and radial, and satisfies

\[
 \sum_j|\varphi(2^{-j}\xi)|^2=1
 \qquad(\xi\ne0).
 \tag{2.6}
\]

Set

\[
 \Omega_\alpha=T_\alpha\omega,
 \qquad
 Q=\sum_\alpha\Omega_\alpha\otimes\Omega_\alpha,
 \qquad
 \mathcal D_\times=\omega\otimes\omega-Q.
 \tag{2.7}
\]

Let \(\lambda_1\ge\lambda_2\ge\lambda_3\ge0\) be the eigenvalues of
\(Q\), without requiring simplicity, and put

\[
 r=\lambda_2+\lambda_3.
 \tag{2.8}
\]

The algebraic covariance-area identity is

\[
 \sum_{\alpha<\beta}
 |\Omega_\alpha\times\Omega_\beta|^2
 =\lambda_1\lambda_2+
  \lambda_1\lambda_3+\lambda_2\lambda_3
 =\lambda_1r+\lambda_2\lambda_3.
 \tag{2.9}
\]

For nonzero frequencies, use

\[
 V(n)=(m_\alpha(n))_\alpha,
 \qquad \|V(n)\|_{\ell^2}=1,
 \tag{2.10}
\]

and the R0.70V response kernel

\[
 \Gamma(p,q)=\langle V(p),V(q)\rangle,
 \qquad
 K(p,q)=1-\Gamma(p,q).
 \tag{2.11}
\]

## 3. The exact projected-wedge formula

### Proposition 3.1 — outputwise projected-wedge identity

Let

\[
 n=p+q\ne0,
 \qquad p\cdot a=0,
 \qquad q\cdot b=0.
 \tag{3.1}
\]

Then

\[
 \boxed{
 \nu_n\times
  [(a\otimes b+b\otimes a)\nu_n]
 =-\frac1{|n|}\nu_n\times
  [(q-p)\times(a\times b)].}
 \tag{3.2}
\]

Indeed, the divergence constraints give

\[
 (a\otimes b+b\otimes a)\nu_n
 =\frac{a(b\cdot p)+b(a\cdot q)}{|n|},
 \tag{3.3}
\]

while

\[
 (q-p)\times(a\times b)
 =-a(b\cdot p)-b(a\cdot q).
 \tag{3.4}
\]

This proves (3.2). Symmetrizing the ordered Fourier sum gives the exact
identity

\[
 \boxed{
 \begin{aligned}
 F(n)
 &:=
 \nu_n\times\widehat{\mathcal D_\times}(n)\nu_n\\
 &=-\frac1{2|n|}
 \sum_{p+q=n}K(p,q)\,
 \nu_n\times\left[(q-p)\times
  \bigl(\widehat\omega(p)\times\widehat\omega(q)\bigr)
 \right].
 \end{aligned}}
 \tag{3.5}
\]

Before summation,

\[
 |F_{p,q}(n)|
 \le\frac{K(p,q)(|p|+|q|)}{2|n|}
  |\widehat\omega(p)\times\widehat\omega(q)|.
 \tag{3.6}
\]

The response-distance cancellation makes the scalar coefficient uniformly
bounded. The remaining factor \(q-p\) still changes from pair to pair at a
fixed output.

Define

\[
 \Delta_{\alpha\beta}(p,q)
 =m_\alpha(p)m_\beta(q)-m_\beta(p)m_\alpha(q).
 \tag{3.7}
\]

Then

\[
 \widehat{\Omega_\alpha\times\Omega_\beta}(n)
 =\frac12\sum_{p+q=n}
 \Delta_{\alpha\beta}(p,q)
 \widehat\omega(p)\times\widehat\omega(q).
 \tag{3.8}
\]

Under the anti-correlation guard \(1+\Gamma\ge\sigma>0\),

\[
 K(p,q)
 =\sum_{\alpha<\beta}
  \frac{\Delta_{\alpha\beta}(p,q)^2}{1+\Gamma(p,q)}.
 \tag{3.9}
\]

Substitution into (3.5) leaves the pair-dependent multiplier

\[
 \frac{\Delta_{\alpha\beta}(p,q)}{1+\Gamma(p,q)}
 \frac{q-p}{|p+q|}
 \tag{3.10}
\]

inside the convolution. Formula (3.8) cannot be substituted after this
multiplier has been discarded. The example below shows that the
distinction is exact.

## 4. A separated-radius field with rank-one covariance

For the field in (1.3), direct differentiation gives

\[
 \operatorname{div}w=0,
 \qquad
 \operatorname{div}h
 =g\operatorname{div}w+(\nabla g)\cdot w=0,
 \tag{4.1}
\]

because \(w_3=0\) and \(g\) depends only on \(x_3\). Both fields are real,
smooth, and mean zero. Their Fourier supports are

\[
 \operatorname{supp}\widehat w
 =\{(\pm1,0,0),(0,\pm1,0)\},
 \tag{4.2}
\]

and

\[
 \operatorname{supp}\widehat h
 =\{(\pm1,0,\pm4),(0,\pm1,\pm4)\}.
 \tag{4.3}
\]

If one frame index were active at both radii, the two strict support
inequalities in (2.5) would force their ratio to be strictly less than four.
Since \(\sqrt{17}>4\), no such index exists. Hence

\[
 \Gamma(1,\sqrt{17})=0,
 \qquad K(1,\sqrt{17})=1.
 \tag{4.4}
\]

Write

\[
 a_\alpha=m_\alpha(1),
 \qquad b_\alpha=m_\alpha(\sqrt{17}).
 \tag{4.5}
\]

Then

\[
 \sum_\alpha a_\alpha^2
 =\sum_\alpha b_\alpha^2=1,
 \qquad
 \sum_\alpha a_\alpha b_\alpha=0,
 \tag{4.6}
\]

and

\[
 \boxed{
 \Omega_\alpha
 =T_\alpha\omega_\varepsilon
 =(a_\alpha+\varepsilon g b_\alpha)w.}
 \tag{4.7}
\]

All frame blocks are parallel. Therefore

\[
 Q_\varepsilon
 =\sum_\alpha
   (a_\alpha+\varepsilon g b_\alpha)^2w\otimes w
 =(1+\varepsilon^2g^2)w\otimes w.
 \tag{4.8}
\]

This matrix has rank one wherever \(w\ne0\), and rank zero at the common
zeros of \(w\). In either case,

\[
 \lambda_2=\lambda_3=0,
 \qquad r=0,
 \qquad G_Q=0.
 \tag{4.9}
\]

The sample does not have a uniformly positive top eigenvalue. It therefore
does not refute a theorem whose stated hypothesis includes a positive
global lower bound for \(\lambda_1\). It does refute the unconditional
covariance-area estimates below.

## 5. Exact projected defect

Since

\[
 \omega_\varepsilon\otimes\omega_\varepsilon
 =(1+2\varepsilon g+\varepsilon^2g^2)w\otimes w,
 \tag{5.1}
\]

subtracting (4.8) gives (1.5). Expanding \(w\otimes w\) shows that the
defect support is

\[
 \begin{aligned}
 &(0,0,\pm4),\\
 &(\pm2,0,\pm4),\quad(0,\pm2,\pm4),\\
 &(\pm1,\pm1,\pm4).
 \end{aligned}
 \tag{5.2}
\]

There are eighteen modes. The first ten are diagonal tensors whose active
coordinate is orthogonal to the corresponding horizontal output direction,
so their contribution to (1.1) is zero.

At each of the remaining eight modes,

\[
 |n|^2=18,
 \qquad
 \widehat{\mathcal D_\times}(n)
 =-\frac{\varepsilon}{4}
  (e_1\otimes e_2+e_2\otimes e_1),
 \tag{5.3}
\]

and

\[
 |\nu_n\times
   \widehat{\mathcal D_\times}(n)\nu_n|^2
 =\frac{\varepsilon^2}{162}.
 \tag{5.4}
\]

Each mode contributes \(\varepsilon^2/2916\). Hence

\[
 \mathfrak X_{\times,\varepsilon}
 =8\frac{\varepsilon^2}{2916}
 =\frac{2\varepsilon^2}{729}.
 \tag{5.5}
\]

This is the full sum, not a lower bound.

## 6. Why the physical area cancels and the projection does not

At the representative output \(n=(1,1,4)\), two low--high unordered pairs
contribute:

\[
 \begin{array}{c|c|c}
 \text{low mode}&\text{high mode}&a\times b\\ \hline
 (0,1,0),\ e_1/2&(1,0,4),\ -e_2/4&-e_3/8\\
 (1,0,0),\ -e_2/2&(0,1,4),\ e_1/4&+e_3/8.
 \end{array}
 \tag{6.1}
\]

The cross products cancel exactly. This is one Fourier manifestation of

\[
 w\times h=w\times(gw)=0.
 \tag{6.2}
\]

The symmetric tensor products add:

\[
 \varepsilon\sum_{\text{two pairs}}
 (a\otimes b+b\otimes a)
 =-\frac\varepsilon4
  (e_1\otimes e_2+e_2\otimes e_1).
 \tag{6.3}
\]

Equivalently, the pair-dependent factor \(q-p\) in (3.5) undoes the
cancellation in (6.1).

The example lies entirely in the separated-radius region. It has
\(\Gamma=0\), so the anti-correlation guard holds with \(\sigma=1\), and
there is no delicate high--high-to-low output. The failure is not caused by
a cutoff endpoint, a sign-changing response, or a missing near-shell bound.

## 7. Projected area-summation no-go

### Theorem 7.1

For every pinned frame satisfying (2.4)--(2.6), the field (1.3) is smooth,
real, mean zero, and divergence free, and satisfies

\[
 \Omega_\alpha\times\Omega_\beta\equiv0
 \quad\text{for every }\alpha,\beta,
 \qquad
 \mathfrak X_\times=\frac{2\varepsilon^2}{729}>0.
 \tag{7.1}
\]

Consequently, if \(\mathcal N\) is any definite norm or seminorm satisfying
\(\mathcal N(0)=0\), there is no finite universal constant in

\[
 \mathfrak X_\times^{1/2}
 \le C\,
 \mathcal N\!\left(
  (\Omega_\alpha\times\Omega_\beta)_{\alpha<\beta}
 \right).
 \tag{7.2}
\]

This includes

\[
 \|G_Q\|_{L^{6/5}},
 \qquad
 \left(\sum_{\alpha<\beta}
  \|\Omega_\alpha\times\Omega_\beta\|_{\dot H^{-1}_\#}^2
 \right)^{1/2},
 \tag{7.3}
\]

and every shell-weighted expression obtained by applying linear derivatives
or inverse derivatives after the physical cross-product fields have been
formed.

The sample also rules out

\[
 \mathfrak X_\times
 \le F(\omega,Q)\,\|r\|_Y^\theta,
 \qquad \theta>0,
 \tag{7.4}
\]

whenever \(F\) is finite on the sample. It does not rule out prefactors made
singular at covariance zeros or hypotheses that impose a uniform positive
top gap.

R0.70V showed that the raw integral \(\int G_Q^2\) has two more frequency
degrees than \(\mathfrak X_\times\). The scale-correct replacement
\(\|G_Q\|_{L^{6/5}}^2\) has the right degree, but is still zero here.
Correct scaling is necessary and not sufficient: the order in which pairs
are reweighted and summed must also be retained.

### 7.1 A separated-scale family

The integer four is only the smallest convenient fixed choice. For every
integer \(M\ge4\), replace \(g\) by

\[
 g_M(x)=\cos(Mx_3).
 \tag{7.5}
\]

The two radii are \(1\) and \(\sqrt{M^2+1}>4\), so the same response
orthogonality and rank-one covariance calculation applies. The eight
projected modes are \((\pm1,\pm1,\pm M)\), and the complete sum is

\[
 \boxed{
 \mathfrak X_{\times,\varepsilon,M}
 =\frac{\varepsilon^2M^2}{(M^2+2)^3}.}
 \tag{7.6}
\]

For \(M=4\), this is \(2\varepsilon^2/729\). The asymptotic decay
\(\mathfrak X_{\times,\varepsilon,M}\sim\varepsilon^2M^{-4}\) is consistent
with the two inverse-frequency degrees. It does not repair the comparison:
the physical covariance area is exactly zero for every \(M\).

## 8. The signed-work boundary

The Fourier multiplier defining Biot--Savart strain does not create new
frequencies. Therefore

\[
 \operatorname{supp}\widehat{S(\omega_\varepsilon)}
 =\operatorname{supp}\widehat{\omega_\varepsilon}.
 \tag{8.1}
\]

The support in (4.2)--(4.3) is disjoint from the defect support in (5.2).
Parseval gives

\[
 \mathfrak E_S(\omega_\varepsilon)=0.
 \tag{8.2}
\]

This distinction is essential. The valid R0.70V estimate

\[
 |\mathfrak E_S|
 \le\|\nabla\omega\|_2\mathfrak X_\times^{1/2}
 \tag{8.3}
\]

completes the defect against every compatible test frequency. The actual
signed term samples only the strain generated by the same vorticity. In the
present field, that extra resonance constraint makes the left side zero
while the Hilbert majorant is positive.

Thus \(\mathfrak X_\times\) is an exact ambient majorant but is too coarse
for a residual-only closure. The next estimate must be trilinear rather than
bilinear.

### 8.1 A first resonant perturbation is a negative control

There is a simple way to force the strain to see one of the projected defect
outputs. For \(M\ge4\), let

\[
 n_M=(1,1,M),
 \qquad c=(1,-1,0),
 \qquad
 z_{\eta,M}=\eta c\cos(n_M\cdot x),
 \tag{8.4}
\]

and add \(z_{\eta,M}\) to \(w+\varepsilon g_Mw\). The new mode is divergence
free because \(n_M\cdot c=0\). It has radius \(\sqrt{M^2+2}\), adjacent to
the modulated radius \(\sqrt{M^2+1}\).

The exact finite-mode audit gives

\[
 \mathfrak E_S
 =-\frac{\varepsilon\eta M}
  {2(M^2+1)(M^2+2)}.
 \tag{8.5}
\]

For comparison, define

\[
 \mathcal A_{-1}
 =\sum_{\alpha<\beta}
  \|\Omega_\alpha\times\Omega_\beta\|_{\dot H^{-1}_\#}^2.
 \tag{8.6}
\]

Let

\[
 \kappa_{23}
 =1-\Gamma(\sqrt{M^2+1},\sqrt{M^2+2})^2.
 \tag{8.7}
\]

The same exact audit gives

\[
 \mathcal A_{-1}
 =\eta^2\left(A_{13}+\varepsilon^2\kappa_{23}A_{23}\right),
 \tag{8.8}
\]

where

\[
 A_{13}
 =\frac{M^2+3}{2(M^2+1)(M^2+5)}
 \sim\frac1{2M^2},
 \tag{8.9}
\]

and

\[
 A_{23}
 =\frac{(2M^2+3)(12M^2+5)}
 {20(4M^2+1)(4M^2+5)}
 \longrightarrow\frac3{40}.
 \tag{8.10}
\]

Smooth radial response gives \(\kappa_{23}=O_\varphi(M^{-4})\). The two
nominal \(M^{-1}\) signed contributions cancel, leaving
\(\mathfrak E_S=O(\varepsilon\eta M^{-3})\), while
\(\mathcal A_{-1}^{1/2}\) is at least order \(|\eta|M^{-1}\). Thus
for \(\eta\ne0\),

\[
 \frac{|\mathfrak E_S|}{\mathcal A_{-1}^{1/2}}
 =O_\varphi(|\varepsilon|M^{-2}).
 \tag{8.11}
\]

This perturbation does not produce a frequency loss in the direct signed
route. It is a negative control, not a proof of the estimate proposed
below.

### 8.2 An exact response-area current survives

The failed right sides in Section 7 form the physical cross products before
applying any pair-dependent multiplier. There is a derivative-before-
summation quantity that keeps the missing information. For
\(m=1,2,3\), define the vector

\[
 \mathcal C_m
 =2\left[
  \omega\times\partial_m\omega
  -\sum_\alpha
   \Omega_\alpha\times\partial_m\Omega_\alpha
 \right],
 \tag{8.12}
\]

and let \(\mathcal C\) be the matrix whose \(m\)-th row is
\(\mathcal C_m\). Direct Fourier symmetrization gives

\[
 \boxed{
 \widehat{\mathcal C}(n)
 =i\sum_{p+q=n}K(p,q)(q-p)\otimes
  \bigl(\widehat\omega(p)\times\widehat\omega(q)\bigr).}
 \tag{8.13}
\]

Combining (8.13) with (3.5) yields the exact antisymmetric-current identity

\[
 \boxed{
 F(n)
 =\frac{i}{2|n|}
  [\widehat{\mathcal C}(n)
   -\widehat{\mathcal C}(n)^{\mathsf T}]\nu_n.}
 \tag{8.14}
\]

Consequently,

\[
 \|F\|_2^2
 =\frac14\sum_{n\ne0}|n|^{-2}
  |[\widehat{\mathcal C}(n)
    -\widehat{\mathcal C}(n)^{\mathsf T}]\nu_n|^2
 \le\|\mathcal C\|_{\dot H^{-1}_\#,F}^2,
 \tag{8.15}
\]

and

\[
 \boxed{
 \mathfrak X_\times
 \le\|\mathcal C\|_{\dot H^{-2}_\#,F}^2.}
 \tag{8.16}
\]

The exact pairing in R0.70V also gives an unweighted alternative:

\[
 \boxed{
 |\mathfrak E_S|
 \le\|\omega\|_2\|F\|_2
 \le\|\omega\|_2
  \|\mathcal C\|_{\dot H^{-1}_\#,F}.}
 \tag{8.17}
\]

Equations (8.16)--(8.17) have the correct whole-space scaling. They are
identities and elementary norm consequences, not a closure. The current
\(\mathcal C\) contains a derivative and can remain nonzero when all
pointwise frame blocks are parallel. It is therefore not determined by
\(G_Q\) or by the covariance eigenvalues. A useful positive result would
need a compensated estimate for its antisymmetric part, rather than the
false physical-area comparison in Section 7.

### 8.3 A universal two-inverse-frequency majorant

The failed covariance comparison does not prevent a scale-correct estimate
in a stronger, pre-convolution quantity. For \(p,q\ne0\), set

\[
 R(p,q)=\max\{|p|,|q|\}.
 \tag{8.18}
\]

Define

\[
 \mathcal U_{-2}(\omega)
 =\frac14\sum_{n\ne0}
 \left(
  \sum_{p+q=n}
  \frac{|\widehat\omega(p)\times\widehat\omega(q)|}
       {R(p,q)}
 \right)^2.
 \tag{8.19}
\]

This quantity keeps each Fourier pair until after the response and output
weights have been paid. It is not a function of the pointwise covariance
eigenvalues.

### Proposition 8.1 — exact-order summation

Let

\[
 C_0=\max\{12,3M_\varphi^2\},
 \tag{8.20}
\]

where \(M_\varphi\) is the logarithmic response derivative from R0.70V.
Then

\[
 \boxed{
 \mathfrak X_\times
 \le C_0^2\mathcal U_{-2}(\omega).}
 \tag{8.21}
\]

Indeed, assume \(0<|p|\le|q|=R\) and put \(t=|p+q|>0\). If
\(|p|\le R/2\), then \(t\ge R/2\), \(K\le2\), and

\[
 K(p,q)\frac{|p|+|q|}{t^2}
 \le\frac{12}{R}.
 \tag{8.22}
\]

If \(|p|>R/2\), the high--high-to-low response bound gives

\[
 K(p,q)\le\frac{M_\varphi^2}{2}
 \frac{t^2}{|p|^2},
 \tag{8.23}
\]

and therefore

\[
 K(p,q)\frac{|p|+|q|}{t^2}
 \le\frac{3M_\varphi^2}{R}.
 \tag{8.24}
\]

Combining (3.5) with (8.22)--(8.24) and then taking the output
\(\ell^2\) norm proves (8.21). No anti-correlation guard is used.

There is also a standard Sobolev consequence. Since

\[
 R(p,q)^{-1}\le(|p||q|)^{-1/2},
 \tag{8.25}
\]

define the scalar Fourier sequence

\[
 \widehat b(0)=0,
 \qquad
 \widehat b(k)=|k|^{-1/2}|\widehat\omega(k)|
 \quad(k\ne0).
 \tag{8.26}
\]

Convolution, Parseval, and
\(\dot H^{3/4}(\mathbb T^3)\hookrightarrow L^4(\mathbb T^3)\) give

\[
 \begin{aligned}
 \mathcal U_{-2}^{1/2}
 &\le\frac12\|\widehat b*\widehat b\|_{\ell^2}\\
 &=\frac12\|b\|_{L^4}^2\\
 &\le\frac{C_{S,4}^2}{2}
  \|\omega\|_{\dot H^{1/4}_\#}^2.
 \end{aligned}
 \tag{8.27}
\]

Hence

\[
 \boxed{
 \mathfrak X_\times
 \le\frac{C_0^2C_{S,4}^4}{4}
  \|\omega\|_{\dot H^{1/4}_\#}^4.}
 \tag{8.28}
\]

This estimate has exactly the required two inverse-frequency degrees.
However, interpolation and (8.3) return

\[
 |\mathfrak E_S|
 \le\frac{C_0C_{S,4}^2}{2}
  \|\omega\|_2^{3/2}\|\nabla\omega\|_2^{3/2}.
 \tag{8.29}
\]

Young's inequality produces only

\[
 |\mathfrak E_S|
 \le\frac\nu2\|\nabla\omega\|_2^2
  +C_\varphi\nu^{-3}\|\omega\|_2^6.
 \tag{8.30}
\]

This is the classical cubic-enstrophy scale. It is a valid all-mode bound,
but it is not a large-data a priori closure and does not use near-rank
geometry.

## 9. The surviving direct trilinear gate

For modes satisfying

\[
 n+p+q=0,
 \qquad
 n\cdot c=p\cdot a=q\cdot b=0,
 \tag{9.1}
\]

R0.70V proved

\[
 S_c:(a\otimes b+b\otimes a)
 =\frac{[(q-p)\times(\nu_n\times c)]\cdot(a\times b)}{|n|}.
 \tag{9.2}
\]

The actual commutator work is the signed sum of (9.2), weighted by
\(K(p,q)\). Unlike \(\mathfrak X_\times\), it retains

\[
 c=\widehat\omega(n)
 \tag{9.3}
\]

and the exact resonance \(n+p+q=0\).

A scale-consistent candidate for the next gate is

\[
 \boxed{
 |\mathfrak E_S|
 \stackrel{?}{\le}
 C_{\varphi,\sigma}
 \|\nabla\omega\|_{L^2}
 \|G_Q\|_{L^{6/5}},}
 \tag{9.4}
\]

under a nonnegative cutoff or the response guard
\(1+\Gamma\ge\sigma>0\). Both factors on the right scale like
\(\mu^{3/2}\) under whole-space Navier--Stokes dilation, so their product
has the same degree \(\mu^3\) as \(\mathfrak E_S\). Young's inequality
would give

\[
 |\mathfrak E_S|
 \le\frac\nu2\|\nabla\omega\|_2^2
  +\frac{C_{\varphi,\sigma}^2}{2\nu}
   \|G_Q\|_{L^{6/5}}^2.
 \tag{9.5}
\]

Neither (9.4) nor (9.5) is proved here. The exact-rank sample satisfies
their necessary null test because both \(G_Q\) and
\(\mathfrak E_S\) vanish. The R0.70U family also has matching first order:
\(|\mathfrak E_S|=\Theta(|\varepsilon|)\) and
\(G_Q=\Theta(|\varepsilon|)\). These are consistency checks, not evidence
of boundedness.

If (9.4) fails, a replacement must preserve a resonance-aware
response-wedge quantity before pairwise cancellation. Returning to
\(\mathfrak X_\times\), or to a norm formed only after the physical cross
products have been summed, cannot repair the loss proved in Section 7.
The exact current (8.12) is the first such replacement with a complete
Fourier ledger.

## 10. Prior-art boundary

[Eyink--Aluie (2009)](https://arxiv.org/abs/0909.2386) prove rigorous
scale-locality bounds for coarse-grained energy transfer and distinguish
absolute nonlocal-triad bounds from additional cancellation in signed
spatially averaged transfer. That distinction supports retaining the signed
trilinear sum in Section 9. Their stress, filter family, and energy-transfer
observable are different from (2.7) and (9.4).

[Do--Muscalu--Thiele
(2012)](https://ems.press/journals/rmi/articles/11381) prove variational
estimates for continuous and discrete Littlewood--Paley paraproducts. Those
results control frequency-localized signed paraproduct increments; they do
not imply that a pair-dependent multiplier is controlled by a product norm
after the relevant Fourier pairs have already cancelled.

[Muscalu--Pipher--Tao--Thiele
(2006)](https://ems.press/journals/rmi/articles/4896) establish torus
Coifman--Meyer estimates in their multi-parameter setting. Standard
Coifman--Meyer theory estimates multilinear operators through norms of
separate inputs. It does not supply (7.2), whose right side is a norm of the
already-combined cross product, nor does it remove the high--high-to-low
singularity of (3.10) without a separate symbol analysis.

The R0.70W obstruction is an elementary exact Fourier calculation. The
bounded follow-up search found no primary-source theorem that turns the
physical covariance area (1.2) into the projected defect (1.1) despite the
cancellation in Section 6. This is a bounded search result, not a novelty or
priority claim.

## 11. Claim-to-evidence ledger

| statement | support | status |
|---|---|---|
| projected-wedge identity (3.2) and defect formula (3.5) | divergence constraints and vector triple product | proved analytically and checked symbolically |
| radius-one/radius-\(\sqrt{17}\) response separation | explicit Fourier support and strict annular cutoff | proved analytically |
| covariance formula (4.8), rank at most one, and \(G_Q=0\) | complete-frame Parseval sums and response orthogonality | proved analytically; finite matrix minors checked exactly |
| defect formula (1.5) | subtraction of (4.8) from the physical tensor | proved and checked exactly |
| \(\mathfrak X_\times=2\varepsilon^2/729\) | all eighteen defect modes, with eight nonzero projected contributions | complete exact Fourier sum |
| physical wedge cancellation but tensor addition at \((1,1,4)\) | two explicit low--high pairs | checked exactly |
| \(\mathfrak E_S=0\) | disjoint strain and defect Fourier supports | proved analytically and checked as a finite support statement |
| no physical-area norm controls \(\mathfrak X_\times\) | zero right-side field and strictly positive left side | proved for the stated class |
| response-area current identities (8.13)--(8.17) | Fourier symmetrization, (3.5), and matrix antisymmetrization | proved analytically and checked symbolically |
| universal bound (8.21) and Sobolev consequence (8.28) | near/far scalar split, convolution, Parseval, and torus Sobolev embedding | proved analytically; not a covariance estimate |
| direct signed estimate (9.4) | scaling and exact consistency tests | open; not asserted |

## 12. Next gate

R0.70X should no longer try to control \(\mathfrak X_\times\) by a physical
covariance-area norm. It should test the actual signed trilinear sum.

1. Write \(\mathfrak E_S\) as an ordered, real-valued triadic form with all
   conjugations and factors of two fixed.
2. Split comparable-radius and separated-radius input pairs without
   removing the third coefficient \(\widehat\omega(-p-q)\).
3. Test (9.4) on exact-rank fields first. One exact-rank field with nonzero
   signed work would stop the candidate immediately.
4. Test multi-output coherent packets to determine whether cancellation
   survives uniformly in the number of modes and shells.
5. In a positive branch, prove a vector-valued trilinear multiplier bound
   and record the anti-correlation hypothesis. Do not infer it from a
   pairwise absolute estimate.
6. In parallel, test whether the antisymmetric current in (8.14) has a
   compensated \(\dot H^{-1}\) or \(\dot H^{-2}\) bound that vanishes at
   exact covariance rank one.
7. Only after a uniform spatial estimate exists should time integration and
   viscosity absorption be revisited.

The branch must stop if the signed sum requires an uncontrolled
\(L^\infty\) norm, loses a derivative, or develops a mode-count or
logarithmic factor. A finite-mode experiment is useful only as a
counterexample search or a delimited symbol audit; it cannot certify the
infinite trilinear estimate.

## 13. Closed and open statements

### Closed in R0.70W

- The divergence-free tensor projection has the exact wedge form (3.5).
- Physical covariance area can cancel before the pair-dependent projection
  multiplier is applied.
- A fixed, smooth, separated-radius, rank-at-most-one covariance field has
  \(G_Q\equiv0\) but
  \(\mathfrak X_\times=2\varepsilon^2/729>0\).
- No choice of two inverse-frequency degrees applied after formation of the
  physical cross-product fields can control \(\mathfrak X_\times\).
- The derivative-before-summation current (8.12) gives exact scale-correct
  bounds for both the projected defect and the signed work.
- The pre-convolution majorant \(\mathcal U_{-2}\) sums all modes with the
  correct derivative count, but its Sobolev reduction returns only the
  classical cubic-enstrophy inequality.
- The counterexample has zero actual signed work and isolates the
  overstrength of the Hilbert majorant rather than disproving the direct
  signed route.

### Still open

- the direct signed estimate (9.4), or a scale-correct replacement;
- a compensated covariance estimate for the antisymmetric current
  \(\mathcal C-\mathcal C^{\mathsf T}\);
- whether every exact-rank complete-frame covariance forces
  \(\mathfrak E_S=0\);
- uniform summability of the signed near/far trilinear decomposition;
- an a priori bound for the surviving signed commutator term;
- control of the principal covariance stretching term
  \(\int S:Q\,dx\);
- propagation of any covariance-rank or coherence hypothesis by an actual
  Navier--Stokes solution;
- an enstrophy closure, continuation theorem, singularity construction,
  unconditional global regularity, or the Millennium problem.
