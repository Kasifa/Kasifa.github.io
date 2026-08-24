# R0.70X — Cyclic null structure and a rank-at-most-one signed obstruction

**Status:** internal canonical candidate; not a public theorem chapter

**Release:** R0.70X

**Date:** 2026-08-25

## 1. Decision

R0.70W left open the direct signed covariance-area estimate

\[
 |\mathfrak E_S|
 \stackrel{?}{\le}
 C_{\varphi,\sigma}
 \|\nabla\omega\|_{L^2}
 \|G_Q\|_{L^{6/5}},
 \qquad
 G_Q=
 \left(\sum_{\alpha<\beta}
 |\Omega_\alpha\times\Omega_\beta|^2\right)^{1/2}.
 \tag{1.1}
\]

The answer is no on the stated complete-frame class. There is a smooth,
real, mean-zero, divergence-free finite Fourier field for which

\[
 \boxed{
 \operatorname{rank}Q\le1,
 \qquad G_Q\equiv0,
 \qquad \mathfrak E_S<0.}
 \tag{1.2}
\]

Thus rank-at-most-one covariance does not null the signed frame-defect work.
The obstruction remains valid for a nonnegative cutoff, so it is not caused
by response anti-correlation. It rules out (1.1) and every other definite
right side that vanishes whenever the physical frame blocks are pointwise
parallel.

The signed triad calculation also contains a positive result. If

\[
 n+p+q=0,
 \qquad
 n\cdot c=p\cdot a=q\cdot b=0,
 \tag{1.3}
\]

and \(A_n,A_p,A_q\) are the three cyclic strain placements, then

\[
 \boxed{
 |n|^2A_n+|p|^2A_p+|q|^2A_q=0.}
 \tag{1.4}
\]

In a high--high--low triangle, this exact null identity produces a
summable \(t/R\) shell-gap factor after the three strain placements are
combined. An explicit family proves that one power of \(t/R\) is sharp for
the orbitwise estimate.

These two findings identify the boundary of the geometry. The physical
covariance area discards too much response-frequency information, while the
signed trilinear form retains a real cyclic cancellation. That cancellation
gives an orbitwise scale-locality factor, but it does not make the work
vanish at covariance rank at most one and does not improve the classical
cubic vorticity bound by itself.

This release does not prove an enstrophy estimate, a continuation theorem,
a singularity, global regularity, or a solution of the Millennium problem.
The calculation is finite and exact. It does not justify DNS or a DGX run,
and it produces no formal numerical figure. No public-page update or GitHub
publication is authorized by this report.

## 2. Conventions

Work on the normalized torus

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3,
 \qquad \int_{\mathbb T^3}1\,dx=1,
 \tag{2.1}
\]

with Fourier convention

\[
 \widehat f(k)=\int_{\mathbb T^3}f(x)e^{-ik\cdot x}\,dx,
 \qquad
 f(x)=\sum_{k\in\mathbb Z^3}\widehat f(k)e^{ik\cdot x}.
 \tag{2.2}
\]

Let \(u\) be the mean-zero Biot--Savart velocity of a smooth real
mean-zero divergence-free vorticity \(\omega\). Then

\[
 \widehat u(k)=\frac{i\,k\times\widehat\omega(k)}{|k|^2},
 \qquad
 S=\frac12(\nabla u+\nabla u^{\mathsf T}).
 \tag{2.3}
\]

Use the pinned real-even radial complete scalar frame

\[
 \mathscr T=\{T_\star=\Pi_0\}\cup\{T_j:j\in\mathbb Z\},
 \qquad
 \sum_\alpha T_\alpha^2=I,
 \tag{2.4}
\]

where

\[
 m_j(k)=\varphi(2^{-j}k),
 \quad
 \operatorname{supp}\varphi
 \subset\{\tfrac12<|\xi|<2\},
 \quad
 \sum_j|\varphi(2^{-j}\xi)|^2=1
 \quad(\xi\ne0).
 \tag{2.5}
\]

Set

\[
 \Omega_\alpha=T_\alpha\omega,
 \qquad
 Q=\sum_\alpha\Omega_\alpha\otimes\Omega_\alpha,
 \qquad
 \mathcal D_\times=\omega\otimes\omega-Q,
 \tag{2.6}
\]

and

\[
 \mathfrak E_S
 =\int_{\mathbb T^3}S:\mathcal D_\times\,dx.
 \tag{2.7}
\]

For nonzero frequencies, let

\[
 V(k)=(m_\alpha(k))_\alpha,
 \qquad
 \Gamma(p,q)=\langle V(p),V(q)\rangle,
 \qquad
 K(p,q)=1-\Gamma(p,q).
 \tag{2.8}
\]

The Parseval identity gives \(\|V(k)\|_{\ell^2}=1\), hence

\[
 K(p,q)=\frac12\|V(p)-V(q)\|_{\ell^2}^2\ge0.
 \tag{2.9}
\]

## 3. The ordered real-valued triad formula

For a mode \(c=\widehat\omega(n)\), the strain symbol is

\[
 S_c(n)
 =-\frac1{2|n|^2}
 \left[n\otimes(n\times c)+(n\times c)\otimes n\right].
 \tag{3.1}
\]

There is no factor of \(i\) in (3.1): the Biot--Savart factor and the
spatial derivative factor cancel.

Let \(n+p+q=0\), and write

\[
 c=\widehat\omega(n),
 \qquad a=\widehat\omega(p),
 \qquad b=\widehat\omega(q).
 \tag{3.2}
\]

All three frequencies in the displayed sums below are nonzero. Terms with a
zero vorticity coefficient vanish because \(\omega\) is mean-zero.

Define

\[
 \begin{aligned}
 A_n
 &:=S_c(n):(a\otimes b+b\otimes a)\\
 &=\frac{
 [(q-p)\times(n\times c)]\cdot(a\times b)}
 {|n|^2}.
 \end{aligned}
 \tag{3.3}
\]

All products in (3.3) are complex bilinear, not Hermitian. Since the strain
is symmetric, the exact ordered formula is

\[
 \boxed{
 \mathfrak E_S
 =\frac12\sum_{\substack{n+p+q=0\\n,p,q\ne0}}K(p,q)A_n.}
 \tag{3.4}
\]

The factor \(1/2\) comes from replacing \(a\otimes b\) by its symmetric
part. The summand is unchanged under \((p,a)\leftrightarrow(q,b)\).
Reality is also exact:

\[
 \tau(-n,-p,-q)=\overline{\tau(n,p,q)},
 \qquad
 \tau(n,p,q)=\frac12K(p,q)A_n.
 \tag{3.5}
\]

Therefore the full lattice sum is real without adding another real-part
operation or another factor of two.

## 4. The Laplacian-weighted cyclic null identity

Define the other two strain placements by

\[
 \begin{aligned}
 A_p&=S_a(p):(b\otimes c+c\otimes b),\\
 A_q&=S_b(q):(c\otimes a+a\otimes c).
 \end{aligned}
 \tag{4.1}
\]

### Proposition 4.1 — cyclic square-weight identity

For every divergence-free triad (1.3),

\[
 \boxed{
 |n|^2A_n+|p|^2A_p+|q|^2A_q=0.}
 \tag{4.2}
\]

One proof is a direct modewise expansion of (3.3). A more informative proof
comes from physical space. For a smooth periodic divergence-free field
\(v\), let \(S(v)\) be its Biot--Savart strain. Since

\[
 -\Delta u_v=\nabla\times v,
 \qquad
 -\Delta S(v)=\operatorname{sym}\nabla(\nabla\times v),
 \tag{4.3}
\]

integration by parts gives

\[
 \begin{aligned}
 \int(-\Delta S(v)):v\otimes v
 &=\int(v\cdot\nabla)(\nabla\times v)\cdot v\\
 &=-\int(\nabla\times v)\cdot(v\cdot\nabla)v\\
 &=0.
 \end{aligned}
 \tag{4.4}
\]

The last equality uses

\[
 (v\cdot\nabla)v
 =\nabla\frac{|v|^2}{2}-v\times(\nabla\times v),
 \qquad
 \nabla\cdot(\nabla\times v)=0.
 \tag{4.5}
\]

Polarizing the cubic identity (4.4) and selecting one Fourier orbit yields
(4.2).

Let

\[
 B_n=|n|^2A_n,
 \qquad
 \beta_n=\frac{K(p,q)}{|n|^2},
 \tag{4.6}
\]

with cyclic definitions for \(B_p,B_q,\beta_p,\beta_q\). Averaging (3.4)
over the three strain placements gives

\[
 \mathfrak E_S
 =\frac16\sum_{\substack{n+p+q=0\\n,p,q\ne0}}\mathcal G(n,p,q),
 \tag{4.7}
\]

where

\[
 \begin{aligned}
 \mathcal G
 &:=K(p,q)A_n+K(q,n)A_p+K(n,p)A_q\\
 &=\beta_nB_n+\beta_pB_p+\beta_qB_q\\
 &=(\beta_n-\beta_q)B_n+(\beta_p-\beta_q)B_p.
 \end{aligned}
 \tag{4.8}
\]

Only the oscillation of the three response slopes \(\beta_j\) contributes.
A common value cancels. This is the correct signed null structure; it is a
three-leg statement, not a norm bound for one physical cross product.

## 5. A sharp high--high--low gain

Put

\[
 t=|n|,
 \qquad P=|p|,
 \qquad Q=|q|,
 \qquad R=\max(P,Q),
 \tag{5.1}
\]

and assume

\[
 t<\frac14\min(P,Q).
 \tag{5.2}
\]

After exchanging \(p,q\) if necessary, take \(Q=R\). Strict annular
support gives

\[
 K(q,n)=K(n,p)=1,
 \tag{5.3}
\]

while \(|P-Q|\le t\). Eliminating \(A_q\) with (4.2) gives the exact
formula

\[
 \boxed{
 \mathcal G
 =\left[K(p,q)-\frac{t^2}{Q^2}\right]A_n
  {}+\left[1-\frac{P^2}{Q^2}\right]A_p.}
 \tag{5.4}
\]

Let

\[
 M_\varphi
 =\sup_{\rho>0}\left\|\frac{d}{d\log\rho}V(\rho)\right\|_{\ell^2}.
 \tag{5.5}
\]

The response chord identity gives

\[
 K(p,q)
 \le\frac{M_\varphi^2}{2}
 \left|\log\frac PQ\right|^2
 \lesssim_\varphi\frac{t^2}{R^2}.
 \tag{5.6}
\]

Also,

\[
 \left|1-\frac{P^2}{Q^2}\right|
 \lesssim\frac tR,
 \tag{5.7}
\]

and (3.3) gives

\[
 |A_n|
 \le\frac{P+Q}{t}|c|\,|a\times b|,
 \qquad
 |A_p|
 \le\frac{Q+t}{P}|a|\,|b\times c|.
 \tag{5.8}
\]

Combining (5.4)--(5.8) proves the orbitwise estimate

\[
 \boxed{
 |\mathcal G(n,p,q)|
 \le C_\varphi\frac tR
 \left(
 |c|\,|a\times b|
 +|a|\,|b\times c|
 \right).}
 \tag{5.9}
\]

At dyadic radii \(t\simeq2^k\) and \(R\simeq2^j\), the new factor is
\(2^{k-j}\), whose sum over \(j-k\ge3\) is finite. Estimating the three
strain placements separately loses this factor.

### Proposition 5.1 — one power is sharp

For integer \(M\ge3\), take

\[
 \begin{aligned}
 n&=(1,0,0),\\
 p&=(M,M,0),\\
 q&=(-M-1,-M,0),
 \end{aligned}
 \qquad
 \begin{aligned}
 c&=e_2,\\
 a&=e_3,\\
 b&=\frac{(M,-M-1,0)}{Q_M},
 \end{aligned}
 \tag{5.10}
\]

where \(Q_M=(2M^2+2M+1)^{1/2}\). Direct calculation gives

\[
 (A_n,A_p,A_q)
 =\frac1{Q_M}(-M,-M-1,M).
 \tag{5.11}
\]

Let \(\kappa_M=K(p,q)\). The two low--high response factors are one, so

\[
 \boxed{
 \mathcal G_M
 =-\frac{1+M\kappa_M}{Q_M}.}
 \tag{5.12}
\]

Since \(\kappa_M\ge0\),

\[
 |\mathcal G_M|\ge Q_M^{-1}\simeq M^{-1}.
 \tag{5.13}
\]

The three polarizations in (5.10) are unit vectors, with
\(|a\times b|=1\) and \(|b\times c|=M/Q_M\simeq1\). Thus the amplitude on
the right side of (5.9) stays of order one; (5.13) genuinely fixes the
power of \(t/R\).

Response smoothness also gives \(\kappa_M=O_\varphi(M^{-2})\), hence

\[
 \mathcal G_M
 =-\frac1{\sqrt2M}+O_\varphi(M^{-2}).
 \tag{5.14}
\]

Thus \(t/R\) cannot be replaced uniformly by
\((t/R)^{1+\varepsilon}\) without additional structure. This is a
single-orbit statement, not yet a global function-space locality theorem.

## 6. A complete-frame rank-at-most-one field

Let

\[
 \begin{aligned}
 k&=(1,-1,1),\\
 p_0&=(1,1,0),\\
 q_0&=(-1,0,1),\\
 r_0&=p_0+q_0=(0,1,1).
 \end{aligned}
 \tag{6.1}
\]

These vectors satisfy

\[
 |k|^2=3,
 \qquad
 |p_0|^2=|q_0|^2=|r_0|^2=2,
 \qquad
 k\cdot p_0=k\cdot q_0=k\cdot r_0=0.
 \tag{6.2}
\]

Define

\[
 \psi(x)
 =\cos(p_0\cdot x)+\cos(q_0\cdot x)+\cos(r_0\cdot x),
 \qquad
 w=k\times\nabla\psi.
 \tag{6.3}
\]

Then

\[
 \nabla\cdot w=0,
 \qquad k\cdot w=0,
 \qquad -\Delta w=2w,
 \qquad \langle\psi^3\rangle=\frac32.
 \tag{6.4}
\]

Put \(z=k\cdot x\). For integer \(M\ge6\), let \(N=M+1\) and

\[
 \omega
 =\left[a\cos z+b\cos(Mz)+c\sin(Nz)\right]w,
 \qquad abc\ne0.
 \tag{6.5}
\]

Write the three summands as \(f_j(z)w\), for \(j=1,M,N\). Each is a
single Laplacian-shell field:

\[
 -\Delta(f_jw)=L_jf_jw,
 \qquad
 L_j=2+3j^2.
 \tag{6.6}
\]

It follows that every actual frame block has the form

\[
 \Omega_\alpha
 =\left[
 m_\alpha(\sqrt{L_1})f_1
 +m_\alpha(\sqrt{L_M})f_M
 +m_\alpha(\sqrt{L_N})f_N
 \right]w.
 \tag{6.7}
\]

All frame blocks are pointwise parallel to the same vector \(w(x)\).
Therefore

\[
 \boxed{
 \Omega_\alpha\times\Omega_\beta\equiv0,
 \qquad
 \operatorname{rank}Q\le1,
 \qquad
 G_Q\equiv0.}
 \tag{6.8}
\]

This is a covariance produced by the complete radial frame, not an
independently prescribed rank-one matrix. The field \(w\) has zeros, so the
example does not have a uniformly positive top covariance eigenvalue.

## 7. The exact frame defect

For shell labels \(i,j\in\{1,M,N\}\), put

\[
 \Gamma_{ij}
 =\left\langle
 V(\sqrt{L_i}),V(\sqrt{L_j})
 \right\rangle,
 \qquad
 K_{ij}=1-\Gamma_{ij}.
 \tag{7.1}
\]

Since \(M\ge6\),

\[
 \frac{\sqrt{L_M}}{\sqrt{L_1}}>4,
 \qquad
 \frac{\sqrt{L_N}}{\sqrt{L_1}}>4.
 \tag{7.2}
\]

Strict annular support gives

\[
 \Gamma_{1M}=\Gamma_{1N}=0,
 \qquad
 K_{1M}=K_{1N}=1.
 \tag{7.3}
\]

Let

\[
 \kappa=K_{MN}=1-\Gamma_{MN}\ge0.
 \tag{7.4}
\]

Expanding the complete-frame Gram matrix gives

\[
 \boxed{
 \mathcal D_\times
 =2\left(f_1f_M+f_1f_N+\kappa f_Mf_N\right)w\otimes w.}
 \tag{7.5}
\]

For a nonnegative cutoff, \(\Gamma_{MN}\ge0\), so
\(0\le\kappa\le1\). No sign or size information beyond
\(\kappa\ge0\) is needed below.

## 8. Nonzero signed work at covariance rank at most one

For \(\omega_j=f_j(z)w\), (6.6) gives

\[
 u_j=L_j^{-1}\nabla\times(f_jw).
 \tag{8.1}
\]

Using

\[
 \nabla\times w=-2k\psi,
 \qquad
 k\times w=-3\nabla\psi,
 \tag{8.2}
\]

one obtains

\[
 S(\omega_j):w\otimes w
 =\frac{f_j'(z)}{L_j}A(x),
 \tag{8.3}
\]

where

\[
 A
 =-3w\cdot(\nabla^2\psi)w
 =w\cdot\left[k\times(w\cdot\nabla)w\right].
 \tag{8.4}
\]

The three-wave resonance in (6.3) gives the exact mean

\[
 \langle A\rangle=\frac{81}{2}.
 \tag{8.5}
\]

The only axial cubic resonance is \(1+M=N\). Substitution of (7.5) and
(8.3) into (2.7) yields

\[
 \boxed{
 \mathfrak E_S
 =\frac{81abc}{4}
 \left[
 \frac{M+1}{L_{M+1}}
 -\frac{M}{L_M}
 -\frac{\kappa}{L_1}
 \right].}
 \tag{8.6}
\]

The part independent of the adjacent-shell response is already negative:

\[
 \frac{M+1}{L_{M+1}}-\frac{M}{L_M}
 =\frac{2-3M(M+1)}{L_ML_{M+1}}<0.
 \tag{8.7}
\]

Since \(L_1=5\) and \(\kappa\ge0\), (8.6) proves

\[
 \boxed{abc>0\quad\Longrightarrow\quad\mathfrak E_S<0.}
 \tag{8.8}
\]

For the smallest convenient fixed instance

\[
 M=6,
 \qquad N=7,
 \qquad a=b=c=1,
 \tag{8.9}
\]

the three squared radii are

\[
 L_1=5,
 \qquad L_6=110,
 \qquad L_7=149,
 \tag{8.10}
\]

and

\[
 \boxed{
 \mathfrak E_S
 =-\frac{81(62+1639\kappa)}{32780}<0.}
 \tag{8.11}
\]

This proves that (1.1) is false: its right side is identically zero, while
the left side is strictly positive after taking the absolute value.

## 9. How the counterexample survives the cyclic identity

The sample does not evade Proposition 4.1. It isolates exactly why that
identity is insufficient for covariance-area control.

For every resonant plane triad, the three axial strain placements share a
common spatial factor \(C\) and have the form

\[
 A_N=C\frac{N}{L_N},
 \qquad
 A_M=-C\frac{M}{L_M},
 \qquad
 A_1=-C\frac1{L_1}.
 \tag{9.1}
\]

Hence

\[
 L_NA_N+L_MA_M+L_1A_1
 =C(N-M-1)=0.
 \tag{9.2}
\]

The actual frame-defect weights instead give

\[
 \begin{aligned}
 K_{1M}A_N+K_{1N}A_M+K_{MN}A_1
 =C\left[
 \frac{N}{L_N}-\frac{M}{L_M}-\frac\kappa{L_1}
 \right]\ne0.
 \end{aligned}
 \tag{9.3}
\]

Thus the physical wedges vanish, but the three response slopes

\[
 \frac1{L_N},
 \qquad
 \frac1{L_M},
 \qquad
 \frac\kappa{L_1}
 \tag{9.4}
\]

do not agree. Their cyclic oscillation is the surviving information.

## 10. Independent finite Fourier reconstruction

The certificate fixes (8.9) and treats \(\kappa\) as an exact nonnegative
symbol. It expands (6.5) into all thirty-six nonzero Fourier modes. For each
mode, it checks

\[
 k\cdot\widehat\omega(k)=0
 \tag{10.1}
\]

and reconstructs the three shells \(5,110,149\). It then computes

\[
 \widehat u(k)
 =\frac{i\,k\times\widehat\omega(k)}{|k|^2},
 \qquad
 \widehat S(k)
 =\frac i2
 \left(k\otimes\widehat u(k)
 +\widehat u(k)\otimes k\right),
 \tag{10.2}
\]

forms every ordered defect pair with the exact kernel

\[
 K_{ii}=0,
 \qquad
 K_{16}=K_{17}=1,
 \qquad
 K_{67}=\kappa,
 \tag{10.3}
\]

and performs the full Parseval sum

\[
 \sum_k\widehat S(k):\widehat{\mathcal D_\times}(-k).
 \tag{10.4}
\]

The machine result is exactly

\[
 -\frac{81(62+1639\kappa)}{32780},
 \tag{10.5}
\]

with zero residual against the independent physical-space derivation.
There is no floating-point arithmetic, grid quadrature, random search, or
truncated infinite sum in this certificate.

## 11. Consequences for the route tree

The following implication is now false:

\[
 \operatorname{rank}Q\le1
 \quad\Longrightarrow\quad
 \mathfrak E_S=0.
 \tag{11.1}
\]

Consequently, none of the following can control \(\mathfrak E_S\) on the
stated class:

1. a definite norm of \(G_Q\);
2. a definite norm of the physical fields
   \(\Omega_\alpha\times\Omega_\beta\);
3. any operator applied only after those zero physical wedges have been
   formed; or
4. a current norm whose claimed right side vanishes whenever \(G_Q=0\).

The response guard does not repair the failure. For a nonnegative cutoff,
all response correlations are nonnegative and (8.11) remains strictly
negative.

There is a narrower unresolved boundary. The example has no uniformly
positive top covariance eigenvalue. It therefore does not disprove a
theorem that uses both a quantitative top gap and more information than
\(G_Q\) alone. Such a theorem would need to use the gap essentially; a
right side containing only \(G_Q\) would still vanish.

## 12. Ambient bounds and the remaining signed information

Standard Riesz-transform and vector-valued Littlewood--Paley estimates give,
for \(1<p_1,p_2,p_3<\infty\) and
\(p_1^{-1}+p_2^{-1}+p_3^{-1}=1\),

\[
 |\mathfrak E_S|
 \le C_{\varphi,p_1,p_2,p_3}
 \prod_{j=1}^3\|\omega\|_{L^{p_j}}.
 \tag{12.1}
\]

For example,

\[
 |\mathfrak E_S|
 \le C_\varphi
 \|\omega\|_6\|\omega\|_2\|\omega\|_3.
 \tag{12.2}
\]

This is an ordinary separate-input cubic estimate. Sobolev interpolation
returns the classical vorticity scale and does not close the large-data
enstrophy inequality.

The positive content of Sections 4--5 is more specific. A potentially
useful replacement for \(G_Q\) must retain the cyclic response-slope
oscillation before convolution and before taking absolute values. For
example, the pair-frequency object

\[
 Z_\alpha(p,q)
 =[m_\alpha(p)-m_\alpha(q)]
 [\widehat\omega(p)\times\widehat\omega(q)]
 \tag{12.3}
\]

retains one response chord and the ordered Fourier pair. A viable estimate
would still have to combine such objects with the third coefficient and the
three cyclic beta differences. No critical norm or factorization of this
kind is proved here. The counterexample shows more strongly that no
pointwise factorization through the already-formed fields
\(\Omega_\alpha\times\Omega_\beta\) can equal \(\mathfrak E_S\) on the
stated class.

## 13. Prior-art boundary

[Waleffe
(1992)](https://doi.org/10.1063/1.858309) showed that individual helical
triads obey exact energy and helicity conservation and described
opposite-signed cancellations in elongated triads. Accordingly, (4.2) is
not presented as a new general triad-conservation principle. The result
proved here is its exact formulation for the present strain--vorticity
amplitudes and its interaction with unequal radial-frame response weights.

[L'vov--Falkovich
(1992)](https://doi.org/10.1103/PhysRevA.46.4762) obtained an explicit
scale-ratio suppression in a statistical triple-correlation analysis of
nonlocal turbulence interactions. Their observable and assumptions differ
from the deterministic frame-defect block (5.4). Therefore (5.9) is not
claimed as the first cancellation-based locality factor.

[Eyink--Aluie
(2009)](https://arxiv.org/abs/0909.2386) prove conditional scale-locality
bounds for coarse-grained kinetic-energy flux and distinguish absolute
nonlocal-triad estimates from additional cancellation in signed transfer.
That distinction supports the cyclic treatment above, but their theorem
does not imply (5.9) or a vorticity covariance estimate.

Classical Bony--Coifman--Meyer theory is the natural framework for summing
the comparable-scale region and the dyadic factor in (5.9). A flag
paraproduct theorem would be relevant only if a later factorization has
nested singular subspaces. No such global multiplier theorem is claimed in
this release.

The bounded source audit found no primary-source statement matching the
complete-frame example in Sections 6--9. This is not a novelty or priority
claim.

## 14. Claim-to-evidence ledger

| statement | support | status |
|---|---|---|
| ordered formula (3.4), factor \(1/2\), and reality | Biot--Savart symbol, strain symmetry, negative-frequency conjugation | proved analytically |
| cyclic identity (4.2) | polarized physical cubic null identity and generic symbolic mode calculation | proved analytically and checked exactly |
| beta-difference form (4.8) | substitution of (4.2) | proved and checked exactly |
| high--high--low identity (5.4) | strict response separation and cyclic elimination | proved analytically |
| orbitwise \(t/R\) estimate (5.9) | response chord smoothness and triangle bounds | proved analytically |
| sharpness family (5.10)--(5.14) | exact triad amplitudes and nonnegative response distance | proved and checked symbolically |
| field geometry (6.1)--(6.6) | finite trigonometric differentiation | proved and checked exactly |
| complete-frame rank at most one and \(G_Q=0\) | every frame block is a scalar multiple of \(w\) | proved analytically; all matrix minors checked |
| defect formula (7.5) | complete-frame response Gram matrix | proved and checked exactly |
| signed formula (8.6) and strict sign | Biot--Savart strain calculation and axial resonance | proved analytically |
| fixed result (8.11) | independent physical and 36-mode Fourier sums | complete exact agreement |
| failure of (1.1) | zero right side and nonzero left side | proved on the stated class |
| global critical cyclic factorization | no certificate | open; not asserted |

## 15. Next gate

R0.70Y should preserve the cyclic response weights rather than return to a
positive covariance-area norm.

1. Seek an exact response-index factorization of the beta differences in
   (4.8) before the physical frame wedges are summed.
2. Test the factorization on the rank-at-most-one field (6.5). Any candidate that
   vanishes on that field is false.
3. Prove the comparable-scale piece with explicit periodic
   Coifman--Meyer derivative bounds.
4. Sum the high--high--low piece using the sharp \(2^{k-j}\) factor, keeping
   the vector-valued frame indices until the last step.
5. Check whether a uniformly positive top covariance gap supplies genuinely
   new information or only multiplies a quantity that still vanishes.
6. Stop any route that replaces the cyclic form by a norm of the ambient
   current or by \(G_Q\) after physical cancellation.
7. Revisit viscosity absorption only after a scale-critical spatial bound
   survives the rank-at-most-one counterexample.

## 16. Closed and open statements

### Closed in R0.70X

- The signed work has the ordered real-valued formula (3.4).
- Its three strain placements obey the exact Laplacian-weighted cyclic null
  identity (4.2).
- A high--high--low cyclic orbit gains one summable factor \(t/R\), and this
  power is sharp in general.
- There is a smooth finite Fourier field generated by the actual complete
  radial frame with \(\operatorname{rank}Q\le1\) and \(G_Q=0\), but
  \(\mathfrak E_S<0\).
- Rank-at-most-one covariance does not force the signed frame-defect work to
  vanish.
- The direct covariance-area candidate (1.1) is false, including for a
  nonnegative cutoff.
- Separate-input multiplier bounds return only the classical cubic
  vorticity scale.

### Still open

- a critical response-index quantity that retains cyclic beta oscillation;
- a global vector-valued summation theorem exploiting (5.9);
- whether a uniformly positive top covariance gap gives a usable additional
  constraint;
- control of the principal covariance stretching term
  \(\int S:Q\,dx\);
- propagation of any covariance coherence or top-gap hypothesis by an
  actual Navier--Stokes solution;
- an enstrophy closure, continuation theorem, singularity construction,
  unconditional global regularity, or the Millennium problem.
