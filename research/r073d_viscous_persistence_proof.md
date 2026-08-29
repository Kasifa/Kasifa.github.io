# R0.73D proof: static vanishing-viscosity persistence of the certified Rayleigh eigenvalue

**Date:** 2026-08-30  
**Scope:** the frozen periodic row \(\gamma=1/2\), \(d=0\), and the sign
\(s=+1\)  
**Evidence class:** exact operator theorem, conditional only on the already
certified R0.73C inviscid eigenvalue

## 1. Theorem

On \(\mathbb T_{2\pi}\), set

\[
 W_0(x)=-\frac12\sin x+\frac14\sin2x,
 \qquad L=L_{1/4}=-\partial_x^2+\frac14,
\]

and let \(X=X_{1/4}\) be the completion of \(L^2\) in the norm

\[
 \|q\|_X^2=4\langle L^{-1}q,q\rangle_{L^2}.
\]

The displayed \(L^2\) formula is initially evaluated on \(L^2\) and then
extended by completion; equivalently, it is the \(H^1\)--\(H^{-1}\) dual
pairing.

The inviscid and viscous frozen generators are

\[
 A=-\frac i2\bigl(M_{W_0}+M_{W_0''}L^{-1}\bigr)\in\mathcal B(X),
 \qquad
 B_\varepsilon=A-\varepsilon L,
 \qquad D_X(B_\varepsilon)=H^1_{\rm per}.
 \tag{1.1}
\]

Let \(\sigma_*\in(0.17035,0.17050)\) be any eigenvalue supplied by the
R0.73C interval-monodromy theorem.  Its Rayleigh eigenfunction is smooth
because \(W_0-i\eta_*\) never vanishes, so the certified vorticity
eigenvector belongs to \(X\).  Then \(\sigma_*\) is an isolated
eigenvalue of \(A\) with finite algebraic multiplicity \(m_*\ge1\).  There
are \(r_*>0\) and \(\varepsilon_*>0\) such that, for the fixed circle

\[
 \Gamma_*:=\{z:|z-\sigma_*|=r_*\}
 \subset\{\operatorname{Re}z>0\},
 \tag{1.2}
\]

the following hold for \(0<\varepsilon<\varepsilon_*\):

1. \(\Gamma_*\subset\rho(B_\varepsilon)\), and the resolvents are uniformly
   bounded on this contour;
2. the Riesz projections

   \[
    P_\varepsilon=\frac1{2\pi i}\int_{\Gamma_*}
      (z-B_\varepsilon)^{-1}\,dz
   \]

   satisfy

   \[
    \|P_\varepsilon-P_0\|_{\mathcal B(X)}\longrightarrow0;
    \tag{1.3}
   \]

3. \(\operatorname{rank}P_\varepsilon=m_*\), so the viscous spectrum inside
   \(\Gamma_*\) is nonempty and has total algebraic multiplicity \(m_*\);
4. every eigenvalue in this viscous cluster converges to \(\sigma_*\) as
   \(\varepsilon\downarrow0\).  In particular, one may select
   \(\lambda_\varepsilon\in\sigma_p(B_\varepsilon)\) with

   \[
    \lambda_\varepsilon\longrightarrow\sigma_*.
    \tag{1.4}
   \]

This is a static frozen-profile theorem.  It does not give a contour uniform
in the moving profile parameter \(d\), a complementary dichotomy, graph-domain
Kato transport, a logarithmic fast-time lower bound, or a nonlinear
Navier--Stokes conclusion.

## 2. The kinetic-space unitary transform

For the proof it is useful to retain a general fixed \(\mu>0\).  Define

\[
 U_\mu=\mu^{-1/2}L_\mu^{-1/2}:X_\mu\longrightarrow L^2(\mathbb T_{2\pi}).
 \tag{2.1}
\]

Then \(U_\mu\) is unitary because

\[
 \|U_\mu q\|_2^2
 =\mu^{-1}\langle L_\mu^{-1}q,q\rangle_2
 =\|q\|_{X_\mu}^2.
\]

Fourier coefficients also show

\[
 U_\mu L_\mu U_\mu^{-1}=L_\mu,
 \qquad
 U_\mu D_{X_\mu}(L_\mu)=H^2_{\rm per}.
 \tag{2.2}
\]

Thus the statement \(D_{X_\mu}(L_\mu)=H^1_{\rm per}\) in the original
vorticity variable becomes the usual \(H^2\) domain after conjugation.

For real smooth \(W\), first compute on trigonometric polynomials:

\[
 U_\mu A_\gamma U_\mu^{-1}=M+K,
 \qquad M=-i\gamma M_W,
 \tag{2.3}
\]

where

\[
 K=-i\gamma\left(
 L_\mu^{-1/2}[M_W,L_\mu^{1/2}]
 +L_\mu^{-1/2}M_{W''}L_\mu^{-1/2}
 \right).
 \tag{2.4}
\]

The right side extends boundedly to all of \(L^2\), and therefore (2.3)
extends by density.

## 3. Compactness of the Rayleigh correction

Write \(\omega_n=(n^2+\mu)^{1/2}\) and
\(W(x)=\sum_kW_ke^{ikx}\).  The Fourier matrix of the commutator in (2.4)
has entries

\[
 W_{n-m}(\omega_m-\omega_n).
\]

Since

\[
 |\omega_m-\omega_n|\le |m-n|,
\]

Young's convolution inequality gives

\[
 \|[M_W,L_\mu^{1/2}]\|_{2\to2}
 \le \sum_k |k|\,|W_k|.
 \tag{3.1}
\]

For \(W_0\), the last sum equals

\[
 2\left(1\cdot\frac14\right)
 +2\left(2\cdot\frac18\right)=1.
 \tag{3.2}
\]

The diagonal multiplier \(L_\mu^{-1/2}\) is compact on the periodic
\(L^2\) space.  Hence both terms in (2.4) are compact, and so is \(K\).
For the frozen row \(\mu=1/4\), \(\gamma=1/2\), the rough check

\[
 \|K\|\le\frac12\left(
 2\cdot1+4\|W_0''\|_\infty\right)\le4
 \tag{3.3}
\]

uses \(\|L^{-1/2}\|=2\) and \(\|W_0''\|_\infty\le3/2\).  No sharp
constant is needed below.

Since \(M\) is multiplication by the purely imaginary function
\(-i\gamma W\), its spectrum is contained in the imaginary axis.  The
operator \(M+K\) is a compact perturbation of \(M\).  Analytic Fredholm
theory therefore makes every spectral point of \(M+K\) in the open right
half-plane an isolated eigenvalue of finite algebraic multiplicity.  This
applies to the certified positive eigenvalue \(\sigma_*\).

## 4. The dissipative base resolvents

After the unitary transform, put

\[
 H_\varepsilon=M-\varepsilon L_\mu,
 \qquad D(H_\varepsilon)=H^2_{\rm per}\quad(\varepsilon>0),
 \qquad D(H_0)=L^2,
 \qquad
 R_\varepsilon(z)=(z-H_\varepsilon)^{-1}.
 \tag{4.1}
\]

The domain jump at \(\varepsilon=0\) is essential: \(H_0=M\) is a bounded
operator on all of \(L^2\), whereas \(H_\varepsilon\) has the elliptic
domain \(H^2\) for every \(\varepsilon>0\).  For
\(\operatorname{Re}z>0\) and \(u\in H^2_{\rm per}\),

\[
 \operatorname{Re}\langle(z-H_\varepsilon)u,u\rangle
 =\operatorname{Re}z\,\|u\|_2^2
  +\varepsilon\langle L_\mu u,u\rangle
 \ge\operatorname{Re}z\,\|u\|_2^2.
 \tag{4.2}
\]

The same estimate holds for the adjoint
\(H_\varepsilon^*=-M-\varepsilon L_\mu\).  Thus
\(z-H_\varepsilon\) has closed dense range and trivial cokernel; it is onto.
Consequently

\[
 \|R_\varepsilon(z)\|\le(\operatorname{Re}z)^{-1}
 \qquad(\varepsilon\ge0).
 \tag{4.3}
\]

For \(u\in H^2_{\rm per}\) and \(f=(z-M)u\), the exact identity

\[
 R_\varepsilon(z)f-u
 =-\varepsilon R_\varepsilon(z)L_\mu u
 \tag{4.4}
\]

shows convergence on the dense set \((z-M)H^2_{\rm per}\).  The uniform
bound (4.3) then gives

\[
 R_\varepsilon(z)\longrightarrow R_0(z)
 \quad\hbox{strongly for every }\operatorname{Re}z>0.
 \tag{4.5}
\]

The resolvent identity makes the family equicontinuous on every compact
subset of the right half-plane.  A finite-net argument upgrades (4.5) to
strong convergence uniform in \(z\) on such compact sets.  Applying the same
argument to \(H_\varepsilon^*\) gives uniform strong convergence of the
adjoint resolvents as well.

Two standard compactness consequences will be used repeatedly.  If
\(C\) is compact and \(\mathcal Z\) is a compact subset of
\(\{\operatorname{Re}z>0\}\), then

\[
 \sup_{z\in\mathcal Z}
 \|(R_\varepsilon(z)-R_0(z))C\|\longrightarrow0,
 \tag{4.6}
\]

and, using the adjoint convergence,

\[
 \sup_{z\in\mathcal Z}
 \|C(R_\varepsilon(z)-R_0(z))\|\longrightarrow0.
 \tag{4.7}
\]

Both statements follow by approximating the compact image of the unit ball
by a finite net.

## 5. Compact-Fredholm convergence on a fixed contour

In the transformed space the full generator is

\[
 \widetilde B_\varepsilon=H_\varepsilon+K.
\]

For \(\operatorname{Re}z>0\), factor on \(H^2_{\rm per}\):

\[
 z-\widetilde B_\varepsilon
 =(z-H_\varepsilon)(I-R_\varepsilon(z)K).
 \tag{5.1}
\]

Let

\[
 F_\varepsilon(z)=I-R_\varepsilon(z)K.
\]

Equation (4.6) gives

\[
 \sup_{z\in\Gamma_*}
 \|F_\varepsilon(z)-F_0(z)\|\longrightarrow0.
 \tag{5.2}
\]

Choose \(r_*\) so that the closed disk bounded by \(\Gamma_*\) lies in the
right half-plane and contains no spectral point of \(M+K\) other than
\(\sigma_*\).  Then \(F_0(z)\) is invertible on \(\Gamma_*\).  Compactness
of the contour and (5.2) imply that \(F_\varepsilon(z)\) is invertible there
for every sufficiently small \(\varepsilon\), with a uniform inverse bound.
Thus

\[
 G_\varepsilon(z):=(z-\widetilde B_\varepsilon)^{-1}
 =F_\varepsilon(z)^{-1}R_\varepsilon(z)
 \tag{5.3}
\]

is uniformly bounded on \(\Gamma_*\), and

\[
 G_\varepsilon(z)\longrightarrow G_0(z)
\]

strongly and uniformly there.  The same argument for the adjoints supplies
uniform strong convergence of \(G_\varepsilon(z)^*\).

## 6. Why the Riesz projections converge in norm

Strong resolvent convergence alone would not imply (1.3).  The missing step
comes from two facts specific to this factorization: the perturbation \(K\)
is compact, and the dissipative base resolvent has no spectrum anywhere in
the disk bounded by \(\Gamma_*\).

Indeed, the resolvent identity gives

\[
 G_\varepsilon-R_\varepsilon
 =G_\varepsilon K R_\varepsilon.
 \tag{6.1}
\]

Uniform strong convergence, compactness of \(K\), and (4.7) imply

\[
 \sup_{z\in\Gamma_*}
 \|G_\varepsilon(z)K R_\varepsilon(z)
   -G_0(z)K R_0(z)\|\longrightarrow0.
 \tag{6.2}
\]

For completeness, split the difference as

\[
 (G_\varepsilon K-G_0K)R_\varepsilon
 +G_0(KR_\varepsilon-KR_0).
\]

The first term tends to zero in norm because \(K\) is compact; the second
does so by (4.7).  All convergence is uniform on the contour.  Equivalently,
the norm-continuous family \(z\mapsto G_0(z)K\) is an operator-norm compact
family on \(\Gamma_*\), so the same conclusion follows from a uniform finite
net.

Every \(H_\varepsilon\) has spectrum in the closed left half-plane.  Hence
\(R_\varepsilon\) is analytic throughout the disk bounded by
\(\Gamma_*\), and

\[
 \int_{\Gamma_*}R_\varepsilon(z)\,dz=0.
 \tag{6.3}
\]

Combining (6.1)--(6.3),

\[
 \begin{aligned}
 \|P_\varepsilon-P_0\|
 &\le \frac{|\Gamma_*|}{2\pi}
 \sup_{z\in\Gamma_*}
 \|G_\varepsilon(z)K R_\varepsilon(z)
   -G_0(z)K R_0(z)\|\\
 &\longrightarrow0.
 \end{aligned}
 \tag{6.4}
\]

Unitary conjugation transfers this operator-norm statement back to \(X\).

## 7. Multiplicity and eigenvalue convergence

The operator \(-\varepsilon L_\mu\) has compact resolvent for
\(\varepsilon>0\); adding the bounded operator \(M+K\) preserves compact
resolvent.  Thus \(P_\varepsilon\) has finite rank equal to the total
algebraic multiplicity of the enclosed viscous eigenvalues.

Once \(\|P_\varepsilon-P_0\|<1\), the restrictions of one projection to the
range of the other are injective.  Therefore

\[
 \operatorname{rank}P_\varepsilon
 =\operatorname{rank}P_0=m_*.
 \tag{7.1}
\]

Finally, repeat the same fixed-contour proof on every smaller circle
\(|z-\sigma_*|=r\), \(0<r<r_*\).  For each such \(r\), all \(m_*\)
viscous eigenvalues counted with algebraic multiplicity eventually lie in
\(|z-\sigma_*|<r\).  Hence the whole cluster converges to \(\sigma_*\),
which proves (1.4).  \(\square\)

## 8. Exact boundary of the result

Relative to the earlier project-internal H1 in the R0.73C conditional
transfer lemma, the proof strengthens the requested projection statement
from uniform boundedness to operator-norm convergence of the fixed-cluster
Riesz projection.  No priority or strict-strengthening claim relative to the
general theorem of Shvydkoy--Friedlander is made.  The proof does not close:

- root uniqueness or algebraic simplicity of the inviscid monodromy root;
- a contour uniform in \(d\) for \(B_\varepsilon(d)\);
- a uniform complementary resolvent or semigroup dichotomy;
- graph-domain bounds for \(\partial_dP_\varepsilon(d)\);
- Kato transport on \(M\log(1/\varepsilon)\) fast time;
- the complete Orr--Sommerfeld--Squire direct sum;
- nonlinear Navier--Stokes control or the Clay problem.
