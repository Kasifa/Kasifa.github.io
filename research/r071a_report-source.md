# R0.71A — A constant-projector no-go and the critical coherence method boundary

**Status:** internal canonical candidate; not a public theorem chapter

**Release:** R0.71A

**Date:** 2026-08-25

## 1. Decision in one page

R0.70Z left two possible repairs for the unresolved covariance route:

1. control the exact principal-projector coefficient
   \(|\nabla P_1|\) on its dimensionally critical mixed-norm line;
2. find a signed or Carleson compensation for the order-one common-response
   channel.

R0.71A resolves the first question only at the level of the current proof
mechanism.  It also sharpens the finite-mode obstruction.

### 1.1 Exact coherence-only covariance-work gate: FAIL

For the fixed real-even radial scalar Parseval frame used in R0.70P--Z,
there are smooth real periodic divergence-free vorticities
\(\omega_{\Lambda,+}\) and \(\omega_{\Lambda,-}\), for every
\(\Lambda>0\), such that

\[
 Q(\omega_{\Lambda,+})(x)
 =Q(\omega_{\Lambda,-})(x)
 \tag{1.1}
\]

at every point and

\[
 P_1(Q)=e_3\otimes e_3,
 \qquad \nabla P_1=0,
 \qquad [T_\alpha,I-P_1]=0
 \tag{1.2}
\]

for every scalar frame block.  Nevertheless,

\[
 \boxed{
 \int_{\mathbb T^3}S(\omega_{\Lambda,\pm}):
 Q(\omega_{\Lambda,\pm})\,dx
 =\pm\frac{3\sqrt2}{40}\Lambda^3.}
 \tag{1.3}
\]

The pointwise principal eigengap also obeys

\[
 \lambda_1-\lambda_2\ge10\Lambda^2,
 \qquad
 \frac{\lambda_1-\lambda_2}{\lambda_1}\ge\frac23,
 \qquad
 \frac{\lambda_1-\lambda_2}{\operatorname{tr}Q}\ge\frac12.
 \tag{1.4}
\]

Thus the best possible projector coherence, even together with a strong
gap and a zero exact scalar-frame commutator, does not determine the sign or
force the vanishing of the covariance work.  This proof target therefore
needs some additional amplitude-sensitive, signed, or dynamical input.  A
quantitative transverse residual and amplitude-weighted alignment are two
concrete candidates, not logically exhaustive requirements.

### 1.2 Critical mixed-norm energy gate: only \(L_t^1\), not \(L_t^2\)

Let \(L\) be any rank-one orthogonal projector and put
\(P=I-L\).  The orientation-free projector identity from R0.70P is

\[
 Z_L(t):=\int\operatorname{tr}(LS^2)\,dx
 =\frac14\|P\omega(t)\|_2^2+I_L(t),
 \tag{1.5}
\]

where

\[
 I_L(t)
 =-\int u_{*,j}\,\partial_k u_i\,\partial_iL_{jk}\,dx.
 \tag{1.6}
\]

For

\[
 3\le p\le\infty,
 \qquad
 \frac2q+\frac3p=1,
 \tag{1.7}
\]

the Leray energy bounds imply the sharp kinematic estimate

\[
 \boxed{
 \|I_L\|_{L_t^1}
 \le C_p
 \|\nabla L\|_{L_t^qL_x^p}
 \|u_*\|_{L_t^\infty L_x^2}^{1-3/p}
 \|\nabla u\|_{L_t^2L_x^2}^{1+3/p}.}
 \tag{1.8}
\]

The R0.70P middle-strain consumer needs \((I_L)_+\in L_t^2\), not
merely \(L_t^1\).  A smooth compactly supported nonzero seed and
Navier--Stokes scaling show that the direct \(L_t^2\) analogue of (1.8)
cannot hold with a scale-uniform constant.  An additional
amplitude-normalized concentrating sequence gives a stronger statement: all
three norms on the right can be held fixed while the \(L_t^s\) error
diverges for every \(s>1\).

This is a **method no-go**.  It does not prove that a continuation theorem
under (1.7) is false.  It proves that such a theorem cannot be obtained by
inserting the critical projector norm into the existing energy-level
Hölder--Gagliardo--Nirenberg version of (1.5).

### 1.3 A positive but conditional finite-\(p\) extension

For \(3\le p\le\infty\), define

\[
 \mathfrak W_{L,p}
 =\int_0^{T_{\max}}
 \|u_*(t)\|_2^2
 \|\nabla L(t)\|_p^2
 \|\nabla u(t)\|_2^{2(1-3/p)}
 \|\nabla^2u(t)\|_2^{6/p}\,dt.
 \tag{1.9}
\]

This quantity is dimensionally critical.  If

\[
 P\omega\in L_t^4L_x^2,
 \qquad
 \mathfrak W_{L,p}<\infty,
 \tag{1.10}
\]

then the periodic \(H^1\) solution extends.  At \(p=\infty\), this is the
R0.70Q weighted direction cost.  The finite-\(p\) family is a direct
interpolation extension, not the sought pure projector-coherence theorem:
it contains the unpropagated higher-order factor \(\nabla^2u\).

### 1.4 Common-response gate: still open

The primary-source audit found established Hardy--BMO and direction-weighted
local-bmo compensation, but no result that automatically closes the exact
R0.70Z response trace from Leray energy and covariance-projector data.  No
new common-channel theorem is claimed in this release.

No DNS or DGX run is justified.  The gate is analytic, and the finite
claims are exactly reproducible with symbolic Fourier arithmetic.

## 2. Setting and notation

All periodic integrals use normalized Haar measure on
\(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\).  For a smooth mean-zero
divergence-free vorticity \(\omega\), let

\[
 u=\nabla\times(-\Delta)^{-1}\omega,
 \qquad
 S=\frac12(\nabla u+\nabla u^{\mathsf T}).
 \tag{2.1}
\]

Use the fixed scalar frame \(T_\alpha\) from R0.70P and define

\[
 \Omega_\alpha=T_\alpha\omega,
 \qquad
 Q(\omega)=\sum_\alpha
 \Omega_\alpha\otimes\Omega_\alpha.
 \tag{2.2}
\]

The frame is real, even, radial, smooth, dyadic, and Parseval.  Its annular
support lies in \(1/2<|\xi|<2\).  In particular, radii separated by a
factor greater than four have orthogonal frame-response vectors.  Equal
radii have the same response.

The covariance work considered below is

\[
 \mathfrak P_Q(\omega)
 =\int_{\mathbb T^3}S(\omega):Q(\omega)\,dx.
 \tag{2.3}
\]

This is distinct from the full vortex-stretching integral
\(\int S:\omega\otimes\omega\).  R0.70Z records their exact response-trace
split.

## 3. An exact constant-principal-projector pair

### 3.1 A planar resonant triad

Set

\[
 \begin{aligned}
 n&=(-1,0,-1),
 &c&=(0,-1,0),\\
 p&=(-3,-3,4),
 &a&=\frac{(1,-1,0)}{\sqrt2},\\
 q&=(4,3,-3),
 &b&=\frac{(-3,4,0)}5.
 \end{aligned}
 \tag{3.1}
\]

Then

\[
 n+p+q=0,
 \qquad
 n\cdot c=p\cdot a=q\cdot b=0,
 \tag{3.2}
\]

and all three polarizations lie in \(e_3^\perp\).  The radii satisfy

\[
 |n|^2=2,
 \qquad
 |p|^2=|q|^2=34,
 \qquad
 34-16\cdot2=2>0.
 \tag{3.3}
\]

Define

\[
 \xi(x)
 =c\cos(n\cdot x)
 +a\cos(p\cdot x)
 +b\cos(q\cdot x).
 \tag{3.4}
\]

The response separation gives

\[
 Q(\xi)
 =\xi_{\mathrm{low}}\otimes\xi_{\mathrm{low}}
 +\xi_{\mathrm{high}}\otimes\xi_{\mathrm{high}}.
 \tag{3.5}
\]

Every value of \(Q(\xi)\) maps into \(e_3^\perp\).  Since the low
polarization has norm one and the high vector is the sum of two unit
polarizations,

\[
 \|Q(\xi)(x)\|_{op}
 \le\operatorname{tr}Q(\xi)(x)
 \le1+4=5.
 \tag{3.6}
\]

The exact six-mode Fourier/Parseval calculation gives

\[
 \boxed{
 \mathfrak P_Q(\xi)=\frac{3\sqrt2}{40}.}
 \tag{3.7}
\]

For comparison,

\[
 \int S(\xi):\xi\otimes\xi
 =\frac{6\sqrt2}{85},
 \qquad
 \int S(\xi):(\xi\otimes\xi-Q(\xi))
 =-\frac{3\sqrt2}{680}.
 \tag{3.8}
\]

The exact split in (3.8) sums to (3.7).

### 3.2 A separated orthogonal filler

Let

\[
 \eta(x)
 =e_3\,[\cos(24x_1)+\sin(97x_1)].
 \tag{3.9}
\]

The squared radii obey

\[
 24^2-16\cdot34=32,
 \qquad
 97^2-16\cdot24^2=193.
 \tag{3.10}
\]

Thus the base, the 24-shell, and the 97-shell have mutually orthogonal
frame responses.  Put

\[
 h(x_1)=\cos^2(24x_1)+\sin^2(97x_1).
 \tag{3.11}
\]

The zero sets of \(\cos(24x)\) and \(\sin(97x)\) cannot meet: after clearing
denominators, equality would identify an odd integer with an even one.  The
quantitative zero-set argument from R0.70Y therefore gives

\[
 \boxed{h(x_1)\ge\frac1{24^2+97^2}=\frac1{9985}.}
 \tag{3.12}
\]

Choose

\[
 C^2=15\cdot9985=149775
 \tag{3.13}
\]

and, for \(\sigma\in\{-1,1\}\), set

\[
 \omega_{\Lambda,\sigma}
 =\Lambda(\sigma\xi+C\eta).
 \tag{3.14}
\]

All cross-response covariances vanish.  Consequently,

\[
 \boxed{
 Q(\omega_{\Lambda,\sigma})
 =\Lambda^2\left[Q(\xi)+C^2h\,e_3\otimes e_3\right].}
 \tag{3.15}
\]

The right side is independent of \(\sigma\).  More importantly, it is
exactly block diagonal with respect to
\(e_3^\perp\oplus\operatorname{span}\{e_3\}\).  From (3.6), (3.12), and
(3.13), the \(e_3\) eigenvalue is at least \(15\Lambda^2\), while the lower
block has operator norm at most \(5\Lambda^2\).  Hence

\[
 \boxed{P_1(Q)=e_3\otimes e_3\quad\hbox{at every point}.}
 \tag{3.16}
\]

This proves (1.2) and (1.4).  The trace-relative estimate follows from

\[
 \frac{\lambda_1-\lambda_2}{\operatorname{tr}Q}
 \ge\frac{\alpha-5}{\alpha+5}\ge\frac12,
 \qquad \alpha=C^2h\ge15.
 \tag{3.17}
\]

### 3.3 Opposite work and exact scope

There is no zero-sum Fourier triple containing a filler mode.  The exact
ten-mode enumeration records this fact.  The filler therefore changes the
covariance and the top eigendirection but contributes no cubic resonance to
the work.  The sign of the base strain is the only surviving change, which
proves (1.3).

The lower-plane residual is not small:

\[
 \boxed{
 \int_{\mathbb T^3}
 \operatorname{tr}((I-P_1)Q)\,dx
 =\frac32\Lambda^2.}
 \tag{3.18}
\]

Equation (3.18) is the precise reason the example does not contradict the
R0.70P frame bridge or its continuation theorem.  It proves the following
narrow result.

### Theorem 3.1 — constant principal-projector no-go

For the fixed frame in Section 2 and every \(\Lambda>0\), the fields in
(3.14) are smooth, real, mean-zero, and divergence-free.  They have the same
pointwise covariance, the same exactly constant simple principal projector,
the gap bounds (1.4), zero commutator with that projector and its complement,
and the opposite nonzero work (1.3).

Therefore none of the following, alone or together, supplies a sign or
vanishing law for \(\mathfrak P_Q\):

1. \(\nabla P_1\), even when it is identically zero;
2. the principal eigengap, even with uniform absolute and relative bounds;
3. the exact scalar-frame commutator \([T_\alpha,I-P_1]\).

The theorem does not rule out a bound containing the transverse residual,
\(P\omega\), a signed response coefficient, a higher norm, or an
amplitude-weighted alignment quantity.

### 3.4 Unweighted finite-\(L^p\) angle is also insufficient

The same construction tests the proposed alignment between \(P_1\) and the
physical vorticity.  Let the filler amplitude be a free number \(A>0\):

\[
 \omega_{A,\sigma}=\sigma\xi+A\eta,
 \qquad
 F(x_1)=\cos(24x_1)+\sin(97x_1).
 \tag{3.19}
\]

For \(A^2>5\cdot9985\), the top projector remains
\(P_1=e_3\otimes e_3\).  Since \(\xi\perp e_3\), the unsigned angle between
\(\omega_{A,\sigma}\) and the principal line satisfies

\[
 \sin\theta_{A,\sigma}(x)
 =\frac{|\xi(x)|}
 {\sqrt{|\xi(x)|^2+A^2F(x_1)^2}}.
 \tag{3.20}
\]

It is independent of \(\sigma\).  The trigonometric polynomial \(F\) is
nonzero and analytic, so its zero set has measure zero.  Dominated
convergence gives

\[
 \boxed{
 \|\sin\theta_{A,\sigma}\|_{L^r(\mathbb T^3)}
 \longrightarrow0
 \quad\text{for every }1\le r<\infty,}
 \tag{3.21}
\]

while

\[
 \mathfrak P_Q(\omega_{A,\sigma})
 =\sigma\frac{3\sqrt2}{40}
 \tag{3.22}
\]

is independent of \(A\).  Thus an unweighted finite-\(L^r\) angle cannot by
itself force covariance-work depletion.  This statement does not reach an
\(L^\infty\) angle bound: at zeros of \(F\), the angle can be large.  It also
does not reach the amplitude-weighted transverse quantity, because

\[
 \|(I-P_1)\omega_{A,\sigma}\|_2=\|\xi\|_2
 \tag{3.23}
\]

does not tend to zero.

## 4. The projector error and the exact consumer requirement

Let

\[
 u\in C([0,T_{\max});H^1_\sigma(\mathbb T^3))
 \cap L^2_{\mathrm{loc}}([0,T_{\max});H^2)
 \tag{4.1}
\]

be a maximal periodic mild/strong solution.  Write
\(u_*=u-\bar u_0\), let \(L\) be a rank-one orthogonal projector, and set
\(P=I-L\).  The exact identities are

\[
 \operatorname{tr}(LS^2)-\frac14|P\omega|^2
 =\partial_i u_j\,\partial_k u_i\,L_{jk}
 \tag{4.2}
\]

and

\[
 I_L
 =-\int_{\mathbb T^3}
 u_{*,j}\,\partial_k u_i\,\partial_iL_{jk}\,dx.
 \tag{4.3}
\]

Since \(Z_L\ge0\), only the positive part of the error is dangerous:

\[
 Z_L
 \le\frac14\|P\omega\|_2^2+(I_L)_+,
 \tag{4.4}
\]

and hence

\[
 Z_L^2
 \le\frac18\|P\omega\|_2^4+2(I_L)_+^2.
 \tag{4.5}
\]

The middle-strain argument closes if

\[
 P\omega\in L_t^4L_x^2,
 \qquad
 (I_L)_+\in L_t^2.
 \tag{4.6}
\]

Replacing \((I_L)_+\) by \(|I_L|\) is sufficient but may discard a future
signed cancellation.

## 5. What the critical projector norm does prove

Fix \(3\le p\le\infty\) and define

\[
 \rho=\frac3p,
 \qquad
 q=\frac2{1-\rho}=\frac{2p}{p-3},
 \tag{5.1}
\]

with \(q=\infty\) at \(p=3\).  Let

\[
 r=\frac{2p}{p-2},
 \qquad
 \frac1r+\frac12+\frac1p=1.
 \tag{5.2}
\]

Spatial Hölder and Gagliardo--Nirenberg give

\[
 \begin{aligned}
 |I_L(t)|
 &\le \|\nabla L(t)\|_p
       \|u_*(t)\|_r\|\nabla u(t)\|_2\\
 &\le C_p\|\nabla L(t)\|_p
       \|u_*(t)\|_2^{1-\rho}
       \|\nabla u(t)\|_2^{1+\rho}.
 \end{aligned}
 \tag{5.3}
\]

The critical relation gives the exact time-exponent identity

\[
 \frac1q+\frac{1+\rho}{2}=1.
 \tag{5.4}
\]

Hölder in time and the energy equality prove (1.8).  There is no unused
time integrability in this calculation: the result lands exactly in
\(L_t^1\).

At the endpoints,

\[
 \begin{array}{c|c|c}
 p&q&\text{pointwise bound}\\ \hline
 3&\infty&|I_L|\le C\|\nabla L\|_3\|\nabla u\|_2^2,\\
 \infty&2&|I_L|\le C\|\nabla L\|_\infty
                    \|u_*\|_2\|\nabla u\|_2.
 \end{array}
 \tag{5.5}
\]

Both rows are only \(L_t^1\) under (1.7) and the energy bound.

## 6. A rigorous kinematic \(L_t^2\) obstruction

### 6.1 A nonzero compact seed

The scaling argument needs a seed for which the trilinear functional is not
zero.  The following construction supplies one without assuming a
Navier--Stokes singularity.

Choose a smooth compactly supported cutoff \(\chi\) equal to one on a ball
and define the vector potential

\[
 \mathcal A
 =\chi\left(-\frac{y^2}{2},0,yz\right),
 \qquad
 U=\nabla\times\mathcal A.
 \tag{6.1}
\]

Then \(U\in C_c^\infty(\mathbb R^3)\) and \(\nabla\cdot U=0\).  In the
region where \(\chi=1\),

\[
 U=(z,0,y).
 \tag{6.2}
\]

Put

\[
 F_i=U_1\partial_2U_i+U_2\partial_1U_i,
 \qquad
 \psi=\nabla\cdot F.
 \tag{6.3}
\]

In the same ball,

\[
 F=(0,0,z),
 \qquad
 \psi=1,
 \tag{6.4}
\]

so \(\psi\) is a nonzero smooth compactly supported function.  Define

\[
 \ell_\varepsilon
 =(\cos(\varepsilon\psi),\sin(\varepsilon\psi),0),
 \qquad
 L_\varepsilon
 =\ell_\varepsilon\otimes\ell_\varepsilon.
 \tag{6.5}
\]

Then \(L_\varepsilon\) is a smooth rank-one projector and is constant off a
compact set.  For

\[
 J(\varepsilon)
 =\int U_j\partial_kU_i\partial_i(L_\varepsilon)_{jk}\,dx,
 \tag{6.6}
\]

differentiation at zero gives

\[
 \boxed{
 J'(0)=\int F\cdot\nabla\psi\,dx
 =-\int|\psi|^2\,dx<0.}
 \tag{6.7}
\]

Thus \(J(\varepsilon)\ne0\) for all sufficiently small nonzero
\(\varepsilon\) of one sign.  Since \(I_L=-J\), taking small positive
\(\varepsilon\) makes \((I_L)_+\) nonzero.  The obstruction therefore
reaches the one-sided quantity actually used by the consumer, not only the
absolute value.  Smooth time cutoffs make both \(u\) and the spatial
variation of \(L\) compactly supported in time.  The same seed can be
embedded in one coordinate chart of the torus.

As a separate finite check, take on \(\mathbb T^3\)

\[
 \ell=(\cos z,\sin z,0),
 \quad
 a(z)=1+\delta\cos(2z),
 \quad
 U=\nabla\times(0,a(z)\cos x,0).
 \tag{6.8}
\]

Direct normalized integration gives

\[
 \int U_j\partial_kU_i\partial_i(\ell_j\ell_k)\,dx
 =\frac\delta2.
 \tag{6.9}
\]

This confirms independently that the trilinear tensor contraction is not an
algebraic zero.

### 6.2 Scaling theorem

For the compact seed, set

\[
 u_\lambda(t,x)=\lambda u(\lambda^2t,\lambda x),
 \qquad
 L_\lambda(t,x)=L(\lambda^2t,\lambda x).
 \tag{6.10}
\]

Then

\[
 I_{L_\lambda}(t)=\lambda I_L(\lambda^2t),
 \tag{6.11}
\]

and hence

\[
 \|I_{L_\lambda}\|_{L_t^1}
 =\lambda^{-1}\|I_L\|_{L_t^1},
 \qquad
 \|I_{L_\lambda}\|_{L_t^2}
 =\|I_L\|_{L_t^2}.
 \tag{6.12}
\]

On the critical line (1.7),

\[
 \begin{aligned}
 \|\nabla L_\lambda\|_{L_t^qL_x^p}
 &=\|\nabla L\|_{L_t^qL_x^p},\\
 \|u_\lambda\|_{L_t^\infty L_x^2}
 &=\lambda^{-1/2}\|u\|_{L_t^\infty L_x^2},\\
 \|\nabla u_\lambda\|_{L_t^2L_x^2}
 &=\lambda^{-1/2}\|\nabla u\|_{L_t^2L_x^2}.
 \end{aligned}
 \tag{6.13}
\]

### Theorem 6.1 — \(L_t^1\) is the best unstructured time space from the three norms

Fix \(3\le p\le\infty\) on (1.7).  There is no finite function
\(\Phi:[0,\infty)^3\to[0,\infty)\) such that every smooth compactly
supported divergence-free \(u\) and every smooth rank-one projector \(L\),
constant outside a compact set, satisfy

\[
 \|I_L\|_{L_t^s}
 \le\Phi\!\left(
 \|u\|_{L_t^\infty L_x^2},
 \|\nabla u\|_{L_t^2L_x^2},
 \|\nabla L\|_{L_t^qL_x^p}
 \right)
 \tag{6.14}
\]

for any fixed \(s>1\).  The same conclusion holds with
\(\|(I_L)_+\|_{L_t^s}\) after choosing the sign of the seed.

In particular, there is no scale-uniform \(C_p\) for the natural estimate

\[
 \begin{aligned}
 \|I_L\|_{L_t^2}
 \le C_p
 &\|\nabla L\|_{L_t^qL_x^p}
 \|u\|_{L_t^\infty L_x^2}^{1-3/p}\\
 &\times
 \|\nabla u\|_{L_t^2L_x^2}^{1+3/p}.
 \end{aligned}
 \tag{6.15}
\]

To prove the stronger form, make the additional amplitude normalization

\[
 \widehat u_\lambda
 =\lambda^{1/2}u_\lambda
 =\lambda^{3/2}u(\lambda^2t,\lambda x).
 \tag{6.16}
\]

The two energy norms of \(\widehat u_\lambda\) and the critical projector
norm of \(L_\lambda\) are all independent of \(\lambda\).  The error is
quadratic in \(u\), so

\[
 \boxed{
 \|I_{L_\lambda}[\widehat u_\lambda]\|_{L_t^s}
 =\lambda^{2-2/s}\|I_L[u]\|_{L_t^s}.}
 \tag{6.17}
\]

It stays fixed for \(s=1\) and diverges for every \(s>1\).  Compact support
lets the same concentrating sequence be placed inside a fixed torus chart,
so this is not a replication artifact.

The theorem rejects every control using only the three displayed norm
values for arbitrary kinematic fields.  It does not reject an estimate that
uses the Navier--Stokes equation, the solution-selected covariance dynamics,
the residual, the exact commutator, signed response cancellation, or an
additional norm.  The amplitude-normalized sequence is not a family of
Navier--Stokes solutions.

## 7. Why one extra dissipation interpolation still does not close

Let

\[
 U=\|u_*\|_2,
 \quad
 Y=\|\nabla u\|_2^2,
 \quad
 D=\|\nabla^2u\|_2^2,
 \quad
 G=\|\nabla L\|_p.
 \tag{7.1}
\]

Interpolating \(\nabla u\) between \(L^2\) and \(L^6\) gives

\[
 \boxed{
 |I_L|
 \le C_p U G
 Y^{(1-3/p)/2}D^{3/(2p)}.}
 \tag{7.2}
\]

For \(3<p<\infty\), Young's inequality yields

\[
 |I_L|^2
 \le\varepsilon D
 +C_p\varepsilon^{-3/(p-3)}
 U^qG^qY,
 \qquad q=\frac{2p}{p-3}.
 \tag{7.3}
\]

This does not follow from energy and (1.7): both \(G^q\) and \(Y\) are only
known to lie in \(L_t^1\), and the product of two \(L^1\) functions need
not be integrable.  The term \(D\) is also the unclosed higher-order
dissipation at a candidate blow-up time.

At \(p=3\), (7.2) becomes

\[
 |I_L|^2\le C U^2G^2D,
 \tag{7.4}
\]

which needs unknown \(D\)-integrability or a separate smallness condition.
At \(p=\infty\), it becomes

\[
 |I_L|^2\le C U^2G^2Y,
 \tag{7.5}
\]

the integrand already isolated in R0.70Q.  Assuming \(G\in L_t^2\) and
knowing \(Y\in L_t^1\) does not control their product.

A more general allocation of up to one derivative produces no hidden
Gronwall case.  If \(0\le\beta\le3/p\), the standard Hölder--GN family has

\[
 |I_L|
 \le C G
 U^{1-3/p+\beta}
 Y^{(1+3/p-2\beta)/2}
 D^{\beta/2}.
 \tag{7.6}
\]

After substitution into the strain inequality and Young absorption of
\(D\), the power of \(Y\) is

\[
 m_\beta
 =\frac{2+3/p-2\beta}{1-\beta}>1.
 \tag{7.7}
\]

Thus this whole interpolation family produces a superlinear ODE term rather
than an integrable coefficient times \(Y\).  This is again a statement about
the method, not about all possible PDE cancellations.

## 8. A finite-\(p\) weighted continuation theorem

### Theorem 8.1 — critical weighted direction cost

Let \(u\) be the maximal periodic solution in (4.1), let \(L\) be a jointly
measurable rank-one orthogonal projector with enough spatial regularity for
(7.2), and put \(P=I-L\).  If for some \(3\le p\le\infty\),

\[
 P\omega\in L^4(0,T_{\max};L^2)
 \tag{8.1}
\]

and the quantity \(\mathfrak W_{L,p}\) in (1.9) is finite, then \(u\)
extends past \(T_{\max}\).

#### Proof

Equation (7.2) gives

\[
 \int_0^{T_{\max}}|I_L(t)|^2\,dt
 \le C_p\mathfrak W_{L,p}<\infty.
 \tag{8.2}
\]

Equations (4.5), (8.1), and (8.2) imply \(Z_L\in L_t^2\).  Since
\((\mu_2^+)^2\le\operatorname{tr}(LS^2)\) pointwise for every rank-one
projector, the periodic middle-strain Gronwall argument from R0.70P bounds
the \(H^1\) norm up to \(T_{\max}\).  The \(H^1\) blow-up alternative gives
the extension.

Under whole-space Navier--Stokes scaling, the time integrand in (1.9) scales
like \(\lambda^2\), so the integral is invariant.  The theorem is therefore
dimensionally critical.  It is nevertheless conditional and does not
propagate its own hypothesis.

If the complete-frame residual \(R\) and exact commutator square
\(\mathfrak C_P\) both lie in \(L_t^2\), the R0.70P bridge supplies (8.1).
This gives a covariance version of Theorem 8.1.  The new unresolved quantity
is still \(\mathfrak W_{L,p}\).

## 9. Literature boundary

The literature audit used primary papers and separated the physical
vorticity direction from the analysis-frame covariance projector.

1. **Fixed planes.**  Chae and Choe proved continuation from two fixed
   vorticity components on the scale-critical vorticity line
   \(2/q_t+3/p_x=2\).  This does not treat a variable projector.

2. **Lipschitz variable planes.**  Evan Miller proved the variable-plane
   criterion
   \(v\times\omega\in L_t^4L_x^2\) with
   \(\nabla v\in L_{\mathrm{loc},t}^\infty L_x^\infty\).
   This is the whole-space oriented source of the R0.70P periodic projector
   consumer.  In Remark 3.3, Miller explicitly notes that even the proposed
   relaxation to \(\nabla v\in L_t^4L_x^\infty\) would require a
   fundamentally different proof because the integration-by-parts argument
   does not move all derivatives off \(u\).

3. **Physical vorticity direction.**  Beir\~ao da Veiga and Berselli proved
   regularity when
   \(\xi=\omega/|\omega|\) obeys
   \(\nabla\xi\in L_t^{q_t}L_x^{p_x}\) with
   \(2/q_t+3/p_x=1/2\).  Their proof uses depletion in the Biot--Savart
   vorticity-direction kernel.  It does not apply to the principal projector
   of a frame covariance.  The line \(1/2\) is also stronger than the
   dimensionally critical projector line \(1\).

4. **Fractional direction regularity.**  Chae's Triebel--Lizorkin criterion
   couples regularity of the physical direction to a separate vorticity
   amplitude norm.  With only the Leray \(L_t^2L_x^2\) amplitude, its index
   condition becomes \(3/p_1+2/r_1\le s-1/2\), not the R0.71A line.

5. **Hardy--BMO compensation.**  The Coifman--Lions--Meyer--Semmes div--curl
   lemma puts \(\omega\cdot\nabla u_j\) in \(\mathcal H^1\), and
   Hardy--BMO duality yields the classical common-channel endpoint.
   Direction-weighted local-bmo variants also exist.  These are sufficient
   mechanisms under additional BMO hypotheses; they do not derive an
   unconditional Carleson closure from the R0.70Z response lift.

The bounded search found no published theorem directly asserting

\[
 \nabla P_1(Q)\in L_t^{q_t}L_x^{p_x},
 \qquad
 \frac2{q_t}+\frac3{p_x}=1,
 \tag{9.1}
\]

as a regularity criterion for the principal projector of an analysis-frame
covariance.  This is not a novelty or priority claim.  It records the scope
of the checked sources.

Primary sources:

- D. Chae and H.-J. Choe, “Regularity of solutions to the Navier--Stokes
  equation,” *Electronic Journal of Differential Equations* 1999(05),
  [authoritative journal PDF](https://www.kurims.kyoto-u.ac.jp/EMIS/journals/EJDE/Volumes/1999/05/chae.pdf).
- E. Miller, “A Locally Anisotropic Regularity Criterion for the
  Navier--Stokes Equation in Terms of Vorticity,” *Proc. Amer. Math. Soc.
  Ser. B* 8 (2021), 60--74,
  [arXiv 2002.02152](https://arxiv.org/abs/2002.02152),
  [DOI 10.1090/bproc/74](https://doi.org/10.1090/bproc/74).
- H. Beir\~ao da Veiga and L. C. Berselli, “On the regularizing effect of
  the vorticity direction in incompressible viscous flows,” *Differential
  and Integral Equations* 15 (2002), 345--356,
  [author PDF](https://people.dm.unipi.it/beiraodaveiga/pdf/hbv-79.pdf),
  [DOI 10.57262/die/1356060864](https://doi.org/10.57262/die/1356060864).
- D. Chae, “Conditional regularity of the Navier--Stokes equations,”
  *Banach Center Publications* 74 (2006), 117--130,
  [publisher PDF](https://www.impan.pl/shop/en/publication/transaction/download/product/86213).
- R. Coifman, P.-L. Lions, Y. Meyer, and S. Semmes, “Compensated
  compactness and Hardy spaces,” *J. Math. Pures Appl.* 72 (1993),
  247--286, [zbMATH record](https://zbmath.org/0864.42009).
- H. Kozono and Y. Taniuchi, “Bilinear estimates in BMO and the
  Navier--Stokes equations,” *Math. Z.* 235 (2000), 173--194,
  [DOI 10.1007/s002090000130](https://doi.org/10.1007/s002090000130).
- Z. Bradshaw and Z. Gruji\'c, “Vorticity in \(L\log L\) in the 3D
  Navier--Stokes equations,” [arXiv 1309.2519](https://arxiv.org/abs/1309.2519).

## 10. Consequences for the route

The exact construction and the exponent audit make three route decisions
unavoidable.

1. **Do not try to infer the covariance-work sign or its vanishing from
   \(\nabla P_1\) alone.**  The constant-projector family already has
   \(\nabla P_1=0\), a strong gap, and zero exact commutator.  The
   lower-plane amplitude omitted by those quantities is visible in (3.18).

2. **Do not replace amplitude-weighted alignment by an unsigned angle.**
   Equation (3.21) tends to zero while the work remains fixed.  The
   transverse residual in (3.23) records what the angle discards.

3. **Do not relabel the \(L_t^1\) estimate as a continuation criterion.**
   The consumer needs \(L_t^2\), and Theorem 6.1 proves that the direct
   energy interpolation cannot supply it.

4. **Preserve signed information.**  Only \((I_L)_+\) is dangerous.  An
   estimate that takes absolute values before the response structure is
   used may discard the only remaining path around the scaling obstruction.

The next justified analytic gate is therefore a coupled one:

\[
 \boxed{
 \text{Can }(I_L)_+\text{ or the exact common-response trace be bounded by}
 \ R,\ \mathfrak C_P,\ \text{and a signed scale-local quantity?}}
 \tag{10.1}
\]

One concrete candidate should explicitly register the lower-plane residual
and show a verifiable improvement as that residual tends to zero.  Other
signed or dynamical candidates remain possible.  Every candidate must
survive the constant-projector pair in Section 3 and avoid simply assuming
the desired \(L_t^2\) conclusion.

## 11. Reproducibility and claim boundary

The exact producer is

`research/r071a_exact_audit.py`.

It verifies:

- the divergence-free resonant triad and all radius separations;
- the exact covariance, full, and defect works;
- the absence of every filler-involving zero-sum Fourier triple;
- equality of the two pointwise covariances at every Fourier output;
- the planar block structure, constant projector, and eigengap arithmetic;
- the critical time-exponent identity and every scaling exponent;
- the local nonzero seed jet and the independent periodic seed integral.

The finite producer does not verify the infinite-dimensional
Gagliardo--Nirenberg inequalities, the middle-strain continuation theorem,
or the literature search.  Those dependencies are stated separately in the
audit files.

R0.71A proves no singularity and no global regularity theorem.  It does not
show that the critical condition (9.1), coupled to an appropriate residual,
is false.  Its strongest result is a sharp classification:

> Projector coherence by itself is insufficient, even in its exact constant
> form; and the existing energy-level projector identity reaches only
> \(L_t^1\) on the dimensionally critical mixed-norm line.  A viable next
> estimate must use residual amplitude, signed response cancellation, or new
> Navier--Stokes dynamics.
