# R0.70Y — Response-slope factorization, critical Besov summation, and a top-eigenvalue no-go

**Status:** internal canonical candidate; not a public theorem chapter

**Release:** R0.70Y

**Date:** 2026-08-25

## 1. Decision

R0.70Y closes three questions left by the R0.70X cyclic-null calculation.

First, the response-slope coefficient has an exact pre-convolution
factorization.  If

\[
 d_n=\frac{V(p)-V(q)}{|n|},
 \qquad n+p+q=0,
 \tag{1.1}
\]

with cyclic definitions of \(d_p,d_q\), then

\[
 \beta_n=\frac{K(p,q)}{|n|^2}
 =\frac12\|d_n\|_{\ell^2}^2.
 \tag{1.2}
\]

The complete cyclic block is therefore an oscillation of squared response
chord slopes.  It separates exactly into a response difference and an
inverse-square metric difference.  The latter can remain nonzero even when
two radial responses coincide.  An explicit family inside every admissible
radial frame proves that neither the affine area of the three responses nor
their \(3\times3\) Gram determinant can be a universal factor of the cyclic
block.

Second, retaining the complete cyclic multiplier through the shell
decomposition gives the log-free critical estimates

\[
 \boxed{
 |\mathfrak E_S(\omega)|
 \le C_{\varphi,\Delta}
 \sum_{j\ge0}\|\Delta_j\omega\|_{L^3}^3
 =C_{\varphi,\Delta}\|\omega\|_{B^0_{3,3}}^3 }
 \tag{1.3}
\]

and

\[
 \boxed{
 |\mathfrak E_S(\omega)|
 \le C_{\varphi,\Delta}
 \|\omega\|_{B^0_{\infty,\infty}}
 \|\omega\|_{L^2}^2 .}
 \tag{1.4}
\]

The high--high--low multiplier has a full normalized symbol bound of order
\(2^{k-J}\), not merely a pointwise orbit estimate.  Periodizing its compact
inverse kernel and summing the resulting \(\ell^1\) shell convolution proves
(1.3)--(1.4).  A scale-separated packet made from the R0.70X exact field
shows that \(q=3\) is sharp among symmetric estimates of the form

\[
 |\mathfrak E_S|\le C\|\omega\|_{B^0_{3,q}}^3.
 \tag{1.5}
\]

Third, a two-shell shear filler strengthens the negative result for the old
physical covariance-area candidate.  There is a smooth forty-mode family
\(\omega_\Lambda\) such that

\[
 \lambda_1(Q_{\Lambda})\ge\frac1{41210}
 \quad\hbox{at every point and for every }\Lambda>0,
 \tag{1.6}
\]

but

\[
 \frac{|\mathfrak E_S(\omega_\Lambda)|}
 {\|\nabla\omega_\Lambda\|_2\|G_{Q_\Lambda}\|_{6/5}}
 \longrightarrow\infty.
 \tag{1.7}
\]

Thus a uniformly nonvanishing top covariance eigenvalue does not repair the
R0.70X no-go.  This family deliberately does **not** settle the stronger
principal-eigengap branch: for every \(\Lambda\ge1\) it has a point where
\(\lambda_1=\lambda_2>0\).

The positive result is a genuine endpoint estimate for the signed frame
defect.  It does not control the principal term

\[
 \int_{\mathbb T^3}S:Q\,dx,
 \tag{1.8}
\]

does not supply \(L^1_tB^0_{\infty,\infty}\) from the Leray energy class, and
does not prove an enstrophy closure, a continuation theorem, a singularity,
global regularity, or a solution of the Millennium problem.

No DNS or DGX calculation is needed for this release: every numerical-looking
quantity is an exact rational, symbolic, or finite Fourier identity.  No
public-page update or GitHub publication is authorized by this report.

## 2. Conventions

Work on the normalized torus

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3,
 \qquad \int_{\mathbb T^3}1\,dx=1,
 \tag{2.1}
\]

with the R0.70X Fourier and Biot--Savart conventions.  For a smooth, real,
mean-zero, divergence-free vorticity \(\omega\), let \(S\) be the symmetric
strain of its mean-zero velocity.

The fixed scalar frame is real, even, radial, smooth, dyadic, and Parseval:

\[
 \mathscr T=\{T_\star=\Pi_0\}\cup\{T_j:j\in\mathbb Z\},
 \qquad
 \sum_\alpha T_\alpha^2=I,
 \tag{2.2}
\]

\[
 m_j(k)=\varphi(2^{-j}k),
 \quad
 \operatorname{supp}\varphi
 \subset\{\tfrac12<|\xi|<2\}.
 \tag{2.3}
\]

Write

\[
 \Omega_\alpha=T_\alpha\omega,
 \qquad
 Q=\sum_\alpha\Omega_\alpha\otimes\Omega_\alpha,
 \qquad
 \mathcal D_\times=\omega\otimes\omega-Q,
 \tag{2.4}
\]

\[
 \mathfrak E_S=\int_{\mathbb T^3}S:\mathcal D_\times\,dx.
 \tag{2.5}
\]

For \(k\ne0\), define the unit response vector and response distance

\[
 V(k)=(m_\alpha(k))_\alpha,
 \quad
 \Gamma(p,q)=\langle V(p),V(q)\rangle,
 \quad
 K(p,q)=1-\Gamma(p,q)
 =\frac12\|V(p)-V(q)\|_{\ell^2}^2.
 \tag{2.6}
\]

The ordered and cyclic triad formulae from R0.70X are

\[
 \mathfrak E_S
 =\frac12\sum_{n+p+q=0}K(p,q)A_n
 =\frac16\sum_{n+p+q=0}\mathcal G(n,p,q),
 \tag{2.7}
\]

where

\[
 \mathcal G
 =K(p,q)A_n+K(q,n)A_p+K(n,p)A_q.
 \tag{2.8}
\]

Set

\[
 B_n=|n|^2A_n,
 \qquad
 \beta_n=\frac{K(p,q)}{|n|^2},
 \tag{2.9}
\]

cyclically.  The exact square-weighted null identity is

\[
 B_n+B_p+B_q=0,
 \qquad
 \mathcal G=\beta_nB_n+\beta_pB_p+\beta_qB_q.
 \tag{2.10}
\]

Independently of the analysis frame, fix one standard smooth inhomogeneous
Littlewood--Paley decomposition \((\Delta_j)_{j\ge0}\) on \(\mathbb T^3\).
Its finite overlap constants are absorbed into \(C_{\varphi,\Delta}\), and

\[
 \|f\|_{B^0_{p,q}}
 =\big\|(\|\Delta_jf\|_p)_{j\ge0}\big\|_{\ell^q}.
 \tag{2.11}
\]

## 3. Exact response-chord factorization

Let

\[
 X=V(n),\qquad Y=V(p),\qquad Z=V(q),
 \quad
 N=|n|,\ P=|p|,\ R=|q|.
 \tag{3.1}
\]

Define the three response slopes

\[
 d_n=\frac{Y-Z}{N},
 \qquad
 d_p=\frac{Z-X}{P},
 \qquad
 d_q=\frac{X-Y}{R}.
 \tag{3.2}
\]

They obey the vector closure

\[
 Nd_n+Pd_p+Rd_q=0
 \tag{3.3}
\]

and, by (2.6),

\[
 \beta_j=\frac12\|d_j\|_{\ell^2}^2.
 \tag{3.4}
\]

Using \(B_q=-B_n-B_p\) gives the exact two-leg form

\[
 \boxed{
 \mathcal G
 =\frac12(\|d_n\|^2-\|d_q\|^2)B_n
 +\frac12(\|d_p\|^2-\|d_q\|^2)B_p.}
 \tag{3.5}
\]

Componentwise,

\[
 \begin{aligned}
 \mathcal G=\frac12\sum_\alpha\big[&
 (d_{\alpha,n}-d_{\alpha,q})
 (d_{\alpha,n}+d_{\alpha,q})B_n\\
 &+(d_{\alpha,p}-d_{\alpha,q})
 (d_{\alpha,p}+d_{\alpha,q})B_p\big].
 \end{aligned}
 \tag{3.6}
\]

The permutation-symmetric form is

\[
 \boxed{
 \mathcal G
 =\frac16\sum_{\rm cyc}
 \langle d_n-d_p,d_n+d_p\rangle_{\ell^2}
 (B_n-B_p).}
 \tag{3.7}
\]

Because each multiplier is even and \(-q=p+n\), every scalar component is
an actual averaged radial derivative:

\[
 d_{\alpha,n}
 =-\int_0^1
 \widehat n\cdot\nabla m_\alpha(-q-sn)\,ds.
 \tag{3.8}
\]

For an annular frame only finitely many indices are active at any nonzero
frequency.  On each normalized compact frequency region, the same is true
uniformly for every fixed derivative order.  Equation (3.8) is therefore the
analytic bridge from the exact chord identity to multiplier derivative bounds.

## 4. Response variation versus metric variation

Use the cyclic notation

\[
 K_n=1-\langle Y,Z\rangle,
 \quad
 K_p=1-\langle Z,X\rangle,
 \quad
 x_n=N^{-2},
 \quad x_p=P^{-2}.
 \tag{4.1}
\]

Since

\[
 K_n-K_p=\langle Z,X-Y\rangle,
 \tag{4.2}
\]

there is an exact split

\[
 \boxed{
 \beta_n-\beta_p
 =\frac{x_n+x_p}{2}\langle Z,X-Y\rangle
 +\frac{x_n-x_p}{2}(K_n+K_p).}
 \tag{4.3}
\]

The first term measures motion of the response curve.  The second term is a
pure inverse-square radial metric difference.  Substituting (4.3) into the
symmetric difference identity yields

\[
 \begin{aligned}
 \mathcal G=\frac16\sum_{\rm cyc}(B_n-B_p)\big[&
 (x_n+x_p)\langle V(q),V(n)-V(p)\rangle\\
 &+(x_n-x_p)(K_n+K_p)\big].
 \end{aligned}
 \tag{4.4}
\]

This distinction is essential.  Coincident response vectors kill the first
term but need not kill the second.

Under the anti-correlation guard \(1+\Gamma(p,q)\ge\sigma>0\), one may also
define

\[
 W_n=\frac{V(p)\wedge V(q)}
 {N\sqrt{1+\Gamma(p,q)}}.
 \tag{4.5}
\]

Then

\[
 \|W_n\|^2
 =\frac{1-\Gamma(p,q)^2}
 {N^2(1+\Gamma(p,q))}
 =\beta_n.
 \tag{4.6}
\]

Thus the chord and pairwise wedge descriptions are equal in norm.  The wedge
form adds a guard but no stronger zero structure; the one-index chord is the
smaller analytic object.

There is also a useful Gram trace representation.  With

\[
 \Gamma_{XYZ}=
 \begin{pmatrix}
 1&\langle X,Y\rangle&\langle X,Z\rangle\\
 \langle X,Y\rangle&1&\langle Y,Z\rangle\\
 \langle X,Z\rangle&\langle Y,Z\rangle&1
 \end{pmatrix}
 \tag{4.7}
\]

and

\[
 L_A=
 \begin{pmatrix}
 A_p+A_q&-A_q&-A_p\\
 -A_q&A_q+A_n&-A_n\\
 -A_p&-A_n&A_n+A_p
 \end{pmatrix},
 \tag{4.8}
\]

one has

\[
 \boxed{\mathcal G=\frac12\operatorname{tr}(L_A\Gamma_{XYZ}).}
 \tag{4.9}
\]

This is linear in the response Gram matrix; it is not generally divisible by
a Gram determinant.

## 5. A radial-frame obstruction to response-area divisibility

For any integer \(M\ge4\), set

\[
 \begin{aligned}
 n&=(1,1,0),
 &p&=(M,-M-1,0),
 &q&=(-M-1,M,0),\\
 c&=(1,-1,0),
 &a&=e_3,
 &b&=(M,M+1,0).
 \end{aligned}
 \tag{5.1}
\]

These data are resonant and divergence-free.  With

\[
 R^2=|p|^2=|q|^2=2M^2+2M+1,
 \qquad d=2M+1,
 \tag{5.2}
\]

the exact three placements are

\[
 A_n=d,
 \qquad
 A_p=d\left(1-\frac2{R^2}\right),
 \qquad
 A_q=-d,
 \tag{5.3}
\]

and

\[
 2A_n+R^2A_p+R^2A_q=0.
 \tag{5.4}
\]

Radiality gives \(V(p)=V(q)\).  Moreover \(R>4|n|\), so the strict annular
support gives \(V(n)\perp V(p)\).  Hence

\[
 (K_n,K_p,K_q)=(0,1,1).
 \tag{5.5}
\]

The affine response triangle has zero area, and the three-response Gram
determinant is zero, but

\[
 \boxed{
 \mathcal G=A_p+A_q
 =-\frac{2(2M+1)}{2M^2+2M+1}\ne0.}
 \tag{5.6}
\]

This is an obstruction inside the actual fixed radial frame, not an abstract
limit of an unrealized response parameter.  It rules out every purported
universal identity in which either the affine response area or the
three-response Gram determinant is a necessary factor of \(\mathcal G\).

It does not rule out estimates that use the full pair-dependent chord tensor
before convolution.

## 6. The critical Besov theorem

### Theorem 6.1 — cyclic frame-defect summation

For every smooth, real, mean-zero, divergence-free \(\omega\) on
\(\mathbb T^3\), the frame defect (2.5) satisfies (1.3) and (1.4).

The constants depend only on finitely many seminorms and support constants of
the fixed analysis frame and the auxiliary Littlewood--Paley partition.  They
do not depend on the number of active shells of \(\omega\).

### 6.1 Comparable interactions

Localize the three input frequencies to dyadic indices
\(j_1,j_2,j_3\).  If the largest and smallest indices differ by at most a
fixed constant, all normalized nonzero frequencies lie in compact annular
sets.  The response factors are bounded, the Biot--Savart strain symbol is
smooth of order zero, and the localized complete cyclic tensor is a uniform
compact Coifman--Meyer symbol.

Writing

\[
 c_j=\|\Delta_j\omega\|_3,
 \qquad
 c_J^\star=\sum_{|r-J|\le C_0}c_r,
 \tag{6.1}
\]

the comparable contribution obeys

\[
 |\mathfrak E_{\rm comp}|
 \le C\sum_J(c_J^\star)^3.
 \tag{6.2}
\]

### 6.2 High--high--low interactions

Let the low leg be \(n\), and normalize

\[
 n=2^kx,
 \qquad
 p=2^Jy,
 \qquad
 q=-2^J(y+\delta x),
 \qquad
 \delta=2^{k-J},
 \tag{6.3}
\]

where \(k\le J-L\) and \(L\) is fixed large enough for strict response
separation.  Then

\[
 K(q,n)=K(n,p)=1.
 \tag{6.4}
\]

Eliminating \(A_q\) with the weighted cyclic identity gives the exact
factorization

\[
 \boxed{
 \mathcal G
 =\left[K(p,q)-\frac{|n|^2}{|q|^2}\right]A_n
 +\left[1-\frac{|p|^2}{|q|^2}\right]A_p.}
 \tag{6.5}
\]

The dyadic response vector is invariant under a common dyadic scaling up to
an index shift.  On the normalized compact set,

\[
 V(|y+\delta x|)-V(|y|)
 =\delta\,\widetilde V_\delta(x,y),
 \tag{6.6}
\]

where every fixed derivative of \(\widetilde V_\delta\) is bounded uniformly
in \(0\le\delta\le2^{-L}\).  Consequently,

\[
 K(p,q)
 =\frac12\|V(|y+\delta x|)-V(|y|)\|^2
 =\delta^2k_\delta(x,y).
 \tag{6.7}
\]

The two metric factors are exact:

\[
 1-\frac{|p|^2}{|q|^2}
 =\delta\frac{2x\cdot y+\delta|x|^2}{|y+\delta x|^2},
 \qquad
 \frac{|n|^2}{|q|^2}
 =\delta^2\frac{|x|^2}{|y+\delta x|^2}.
 \tag{6.8}
\]

Use the original strain tensor symbol in \(A_n,A_p\), together with the
smooth Leray projections on the three annuli.  These are uniform order-zero
tensors.  Equations (6.5)--(6.8) therefore give

\[
 \boxed{
 \mathcal M_{kJJ}
 =\delta\widetilde{\mathcal M}_\delta,}
 \tag{6.9}
\]

where the \(K(p,q)\) and \(|n|^2/|q|^2\) pieces begin at order
\(\delta^2\), while the remaining metric piece begins at order \(\delta\).
For every fixed pair of multi-indices,

\[
 \sup_{x,y}
 |\partial_x^\alpha\partial_y^\beta
 \mathcal M_{kJJ}(x,y)|
 \le C_{\alpha,\beta,\varphi}\,2^{k-J}.
 \tag{6.10}
\]

Equivalently, before normalization,

\[
 \sup
 |(2^k\partial_n)^\alpha(2^J\partial_p)^\beta
 \mathcal M_{kJJ}(n,p)|
 \le C_{\alpha,\beta,\varphi}\,2^{k-J}.
 \tag{6.10a}
\]

The order of operations matters: the three strain placements are combined
before the response-vector contraction and before an absolute value is
taken.  A one-placement bound does not retain (6.10).

### 6.3 Periodic kernel lemma

Multiply the normalized symbol in (6.9) by the compact LP cutoffs and extend
it smoothly by zero away from a slightly larger compact set.  Taking a fixed
sufficient number of derivatives, for example more than six, and integrating
by parts in its \(\mathbb R^6\)
inverse transform gives

\[
 \|\check{\mathcal M}_{kJJ}\|_{L^1(\mathbb R^6)}
 \le C2^{k-J}.
 \tag{6.11}
\]

Restoring the physical scales preserves this \(L^1\) norm.  Periodize both
kernel variables:

\[
 K^{\mathbb T}_{kJJ}(u,v)
 =\sum_{\ell,m\in\mathbb Z^3}
 K_{kJJ}(u+2\pi\ell,v+2\pi m).
 \tag{6.12}
\]

Then

\[
 \|K^{\mathbb T}_{kJJ}\|_{L^1(\mathbb T^6)}
 \le \|K_{kJJ}\|_{L^1(\mathbb R^6)}
 \le C2^{k-J}.
 \tag{6.13}
\]

Poisson summation identifies its integer-frequency multiplier with the
localized torus symbol.  The physical kernel representation and Hölder give

\[
 |\Lambda_{kJJ}(f,g,h)|
 \le C2^{k-J}
 \|f\|_{p_1}\|g\|_{p_2}\|h\|_{p_3},
 \qquad
 \frac1{p_1}+\frac1{p_2}+\frac1{p_3}=1.
 \tag{6.14}
\]

This includes \((3,3,3)\) and \((\infty,2,2)\).  No singular endpoint
extension of the global Coifman--Meyer theorem is being invoked; the endpoint
here follows directly from the compact localized \(L^1\) kernel.

### 6.4 Shell summation

The triangle relation forces the two highest dyadic indices into a fixed
neighborhood.  Equations (6.2) and (6.14) yield

\[
 |\mathfrak E_S|
 \le C\left[
 \sum_J(c_J^\star)^3
 +\sum_J(c_J^\star)^2
 \sum_{k\le J-L}2^{k-J}c_k
 \right].
 \tag{6.15}
\]

Let

\[
 h_m=2^{-m}\mathbf1_{\{m\ge L\}}.
 \tag{6.16}
\]

Since \(h\in\ell^1\), Hölder in sequence space and Young's convolution
inequality give

\[
 \begin{aligned}
 \sum_J(c_J^\star)^2(h*c)_J
 &\le
 \|(c^\star)^2\|_{\ell^{3/2}}
 \|h*c\|_{\ell^3}\\
 &\le C\|c\|_{\ell^3}^3.
 \end{aligned}
 \tag{6.17}
\]

The finite star convolution also gives

\[
 \sum_J(c_J^\star)^3\le C\sum_jc_j^3.
 \tag{6.18}
\]

This proves (1.3).

For the mixed estimate, set

\[
 a_j=\|\Delta_j\omega\|_2,
 \qquad b_j=\|\Delta_j\omega\|_\infty.
 \tag{6.19}
\]

Use the finite-neighborhood envelopes

\[
 a_J^\star=
 \left(\sum_{|r-J|\le C_0}a_r^2\right)^{1/2},
 \qquad
 b_J^\star=\max_{|r-J|\le C_0}b_r.
 \tag{6.19a}
\]

Choose the low factor in the HHL region for \(L^\infty\), and any one factor
in the comparable region.  The same kernel bounds give

\[
 |\mathfrak E_S|
 \le C\sum_J(a_J^\star)^2
 \left[b_J^\star
 +\sum_{k\le J-L}2^{k-J}b_k\right].
 \tag{6.20}
\]

Finite overlap, \(h\in\ell^1\), and LP almost orthogonality imply

\[
 |\mathfrak E_S|
 \le C\sup_jb_j\sum_ja_j^2
 \le C\|\omega\|_{B^0_{\infty,\infty}}\|\omega\|_2^2,
 \tag{6.21}
\]

which is (1.4).

Finally,

\[
 \begin{aligned}
 \sum_j\|\Delta_j\omega\|_3^3
 &=\int_{\mathbb T^3}\sum_j|\Delta_j\omega|^3\,dx\\
 &\le\int_{\mathbb T^3}
 \left(\sum_j|\Delta_j\omega|^2\right)^{3/2}dx
 \le C\|\omega\|_3^3.
 \end{aligned}
 \tag{6.22}
\]

Thus (1.3) refines the ordinary cubic \(L^3\) estimate by preserving the
cross-scale sequence structure.

## 7. Scaling and what the endpoint does not close

Under the three-dimensional Euclidean scaling

\[
 \omega_\lambda(t,x)
 =\lambda^2\omega(\lambda^2t,\lambda x),
 \tag{7.1}
\]

the defect work and both right sides of (1.3)--(1.4) have spatial degree
\(\lambda^3\).  In particular,

\[
 \|\omega\|_{L^1_tB^0_{\infty,\infty}}
 \tag{7.2}
\]

is dimensionless.  Estimate (1.4) therefore gives a scale-critical time
coefficient for the defect part of the enstrophy identity.

This does not create such a bound from the energy inequality.  More
importantly, the exact splitting is

\[
 \int S:(\omega\otimes\omega)\,dx
 =\int S:Q\,dx+\mathfrak E_S.
 \tag{7.3}
\]

The principal covariance term in (7.3) is not controlled by Theorem 6.1.
Consequently, Grönwall cannot be applied to the full enstrophy using this
release alone.

## 8. Sharpness of the Besov sequence exponent

Let \(W\) be the exact R0.70X field with \(M=6\).  It has thirty-six Fourier
modes, squared radii

\[
 \{5,110,149\},
 \tag{8.1}
\]

and

\[
 \mathfrak E_S(W)
 =-\frac{81(62+1639\kappa)}{32780}<0.
 \tag{8.2}
\]

Choose one fixed \(r_0\) beyond the inhomogeneous low block and, for
\(N\ge1\), define

\[
 W_N(x)=\sum_{r=r_0}^{r_0+N-1}W(64^rx).
 \tag{8.3}
\]

Because \(64=2^6\), each dilation shifts the frame index by six and preserves
every response inner product \(K\).  For the fixed standard LP partition used
here, a six-index gap is wider than twice its finite annular overlap.  For a
different smooth partition with wider fixed overlap, replace \(64\) by a
sufficiently large dyadic \(2^s\); the proof and exponent are unchanged.

There are no mixed-scale resonant triads.  If only one frequency has the
largest macro-scale, cancellation would require

\[
 \sqrt5\,64\le2\sqrt{149},
 \tag{8.4}
\]

which is false.  If two frequencies have the largest macro-scale and their
integer base modes do not cancel, their sum has length at least one, while
the lower macro-scale mode has normalized length at most
\(\sqrt{149}/64<1\).  If the two base modes cancel exactly, the third mode
would have to be zero, which is absent.

Therefore

\[
 \boxed{\mathfrak E_S(W_N)=N\mathfrak E_S(W).}
 \tag{8.5}
\]

The auxiliary LP blocks of different macro-scales have disjoint fixed-width
index neighborhoods, so

\[
 \|W_N\|_{B^0_{3,q}}\asymp N^{1/q},
 \tag{8.6}
\]

with constants independent of \(N\).  If (1.5) held for some \(q>3\), then
(8.5)--(8.6) would imply

\[
 N\le C N^{3/q},
 \tag{8.7}
\]

which fails as \(N\to\infty\).  Hence \(q=3\) is sharp within this symmetric
Besov cubic family.

The same packet has

\[
 \|W_N\|_{B^0_{\infty,\infty}}\asymp1,
 \qquad
 \|W_N\|_2^2=N\|W\|_2^2,
 \tag{8.8}
\]

so the scale counting in (1.4) is also linearly saturated.

## 9. A uniformly positive top-eigenvalue filler

Write the R0.70X rank-at-most-one field as

\[
 \xi(x)=w(x)
 [\cos z+\cos(6z)+\sin(7z)],
 \qquad z=(1,-1,1)\cdot x.
 \tag{9.1}
\]

Its frame covariance has the form

\[
 Q_\xi=\rho(x)w(x)\otimes w(x),
 \qquad \rho\ge0.
 \tag{9.2}
\]

Add the shear

\[
 \eta=e_2[\cos(49x_1)+\sin(197x_1)],
 \qquad
 \omega_\Lambda=\Lambda\xi+\eta.
 \tag{9.3}
\]

The five squared radii are

\[
 5,\ 110,\ 149,\ 49^2,\ 197^2.
 \tag{9.4}
\]

The strict factor-four slacks are

\[
 49^2-16\cdot149=17,
 \qquad
 197^2-16\cdot49^2=393.
 \tag{9.5}
\]

Thus the two filler response vectors are orthogonal to all old responses and
to each other.  Cross-covariances vanish and

\[
 Q_\Lambda
 =\Lambda^2\rho\,w\otimes w
 +h\,e_2\otimes e_2,
 \quad
 h=\cos^2(49x_1)+\sin^2(197x_1).
 \tag{9.6}
\]

### 9.1 Quantitative lower bound for \(h\)

Let \(Z_c\) and \(Z_s\) be the zero sets of \(\cos(49x)\) and
\(\sin(197x)\) on the circle.  For any two such zeros, the normalized
difference has numerator

\[
 197(2r+1)-98s-4\cdot49\cdot197\ell,
 \tag{9.7}
\]

which is odd and hence nonzero.  Their circular distance is at least

\[
 \frac{\pi}{2\cdot49\cdot197}.
 \tag{9.8}
\]

For an arbitrary \(x\), let

\[
 a=49\operatorname{dist}(x,Z_c),
 \qquad
 b=197\operatorname{dist}(x,Z_s).
 \tag{9.9}
\]

Then \(a,b\in[0,\pi/2]\) and

\[
 197a+49b\ge\frac\pi2.
 \tag{9.10}
\]

Using \(\sin y\ge2y/\pi\) on this interval and Cauchy--Schwarz,

\[
 \begin{aligned}
 h&=\sin^2a+\sin^2b\\
 &\ge\frac4{\pi^2}(a^2+b^2)\\
 &\ge\frac4{\pi^2}
 \frac{(197a+49b)^2}{197^2+49^2}\\
 &\ge\frac1{41210}.
 \end{aligned}
 \tag{9.11}
\]

Since \(Q_\Lambda\) is positive semidefinite,

\[
 \lambda_1(Q_\Lambda)
 \ge e_2^{\mathsf T}Q_\Lambda e_2
 \ge h
 \ge\frac1{41210}.
 \tag{9.12}
\]

### 9.2 Exact signed work and failure of the old candidate

No Fourier triad containing a filler mode is resonant with the old support.
With one filler and two old modes, resonance is impossible because
\(49>2\sqrt{149}\).  With two filler modes, their sum is either zero or has
magnitude at least \(98>\sqrt{149}\); the zero sum would force the remaining
old mode to vanish.  With three filler modes, the three signed axial
wavenumbers are odd, so their sum is an odd nonzero integer.  The forty-mode
producer independently enumerates all cases.

It follows, both from support arithmetic and from the independent Fourier
reconstruction, that

\[
 \boxed{
 \mathfrak E_S(\omega_\Lambda)
 =-\frac{81(62+1639\kappa)}{32780}\Lambda^3.}
 \tag{9.13}
\]

Every \(\Lambda^2\), \(\Lambda\), and constant mixed-work coefficient is
exactly zero.  Parseval also gives

\[
 \|\nabla\omega_\Lambda\|_2^2
 =1188\Lambda^2+20605.
 \tag{9.14}
\]

For any positive-semidefinite covariance assembled from frame vectors,

\[
 G_Q^2
 =\frac12[(\operatorname{tr}Q)^2-\operatorname{tr}(Q^2)].
 \tag{9.15}
\]

Applying (9.15) to (9.6) gives

\[
 \boxed{
 G_{Q_\Lambda}^2
 =\Lambda^2\rho h\,|w\times e_2|^2.}
 \tag{9.16}
\]

The coefficient is finite and not identically zero, so

\[
 \|G_{Q_\Lambda}\|_{6/5}
 =\Lambda C_G,
 \qquad 0<C_G<\infty.
 \tag{9.17}
\]

Combining (9.13)--(9.17) proves (1.7).  Therefore the estimate

\[
 |\mathfrak E_S|
 \le C\|\nabla\omega\|_2\|G_Q\|_{6/5}
 \tag{9.18}
\]

cannot be restored merely by adding a uniform lower bound on
\(\lambda_1(Q)\).

## 10. Why this is not a principal-eigengap counterexample

Consider the curve

\[
 x(A)=(A/3,2A/3,A/3).
 \tag{10.1}
\]

Along it,

\[
 z=0,
 \qquad
 w=3\sin A\,(e_1-e_3)\perp e_2,
 \qquad
 \rho=2.
 \tag{10.2}
\]

The two nonzero covariance eigenvalues are therefore exactly

\[
 X(A)=36\Lambda^2\sin^2A,
 \qquad
 Y(A)=h(A/3).
 \tag{10.3}
\]

For every \(\Lambda\ge1\),

\[
 X(0)-Y(0)=-1,
 \qquad
 X(\pi/6)-Y(\pi/6)\ge9\Lambda^2-2>0.
 \tag{10.4}
\]

Continuity supplies \(A_\Lambda\in(0,\pi/6)\) with

\[
 X(A_\Lambda)=Y(A_\Lambda)>0.
 \tag{10.5}
\]

At that point,

\[
 \lambda_1(Q_\Lambda)=\lambda_2(Q_\Lambda),
 \tag{10.6}
\]

so both the absolute and relative principal gaps vanish.  There is also a
fully explicit equality:

\[
 \Lambda=\frac16,
 \qquad
 x=(\pi/6,\pi/3,\pi/6),
 \qquad
 \lambda_1=\lambda_2=1.
 \tag{10.7}
\]

Consequently, R0.70Y rules out the **top-eigenvalue lower-bound** repair but
leaves the genuine uniformly positive principal-eigengap branch open.

If the filler were amplified proportionally to \(\Lambda\), a sufficiently
large fixed coefficient could force a true gap by eigenvalue perturbation,
but then \(G_Q=\Theta(\Lambda^2)\).  The right side of (9.18) would recover
the same cubic homogeneity as the left, and this amplitude argument would no
longer disprove it.

## 11. Literature boundary

The harmonic-analysis mechanisms used here are classical.  Bony introduced
the paradifferential decomposition underlying modern shell-wise nonlinear
estimates [Bony 1981](https://doi.org/10.24033/asens.1404), while
Coifman--Meyer developed bilinear singular-integral estimates
[Coifman--Meyer 1975](https://doi.org/10.1090/S0002-9947-1975-0380244-8).
R0.70Y uses a simpler compact localized inverse-kernel argument at the
\((\infty,2,2)\) endpoint rather than asserting a new endpoint theorem for
the global multiplier class.

Triadic cancellation and scale locality also have a substantial literature.
Waleffe's helical-triad analysis identifies paired, nearly cancelling
nonlocal transfers [Waleffe 1992](https://doi.org/10.1063/1.858309).
Eyink and Aluie prove rigorous nonlocal-triad bounds for kinetic-energy
transfer and distinguish absolute estimates from additional cancellations in
signed spatial averages
[Eyink--Aluie 2009](https://arxiv.org/abs/0909.2386).  Those papers concern
different transfer objects and do not imply the frame-defect identity or
Theorem 6.1.

L'vov and Falkovich obtain an explicit scale-ratio suppression in a
quasi-Lagrangian statistical theory
[L'vov--Falkovich 1992](https://doi.org/10.1103/PhysRevA.46.4762), while the
sharp-filter sequel of Aluie and Eyink emphasizes that large individual
nonlocal triads and their aggregate contribution are different objects
[Aluie--Eyink 2009](https://arxiv.org/abs/0909.2451).  These precedents mean
that neither a generic \(t/R\) locality slogan nor signed triad cancellation
is a novelty claim here.  The specific result is the deterministic
frame-response cyclic symbol and its uniform derivative estimate.

Littlewood--Paley and Besov methods for the vorticity equation are likewise
established.  Manna and Sritharan study local dissipativity and Lyapunov
properties of vorticity norms
[Manna--Sritharan 2008](https://arxiv.org/abs/0802.2898), and Yuan and Zhang
derive continuation criteria in negative-index Besov spaces
[Yuan--Zhang 2007](https://arxiv.org/abs/math/0703883).  Kozono, Ogawa and
Taniuchi establish logarithmic critical Besov inequalities and corresponding
regularity criteria
[Kozono--Ogawa--Taniuchi 2002](https://doi.org/10.1007/s002090100332).
Their hypotheses,
functionals, and conclusions differ from the signed complete-frame defect
estimated here.

For shell summation and sharpness, Cheskidov, Constantin, Friedlander and
Shvydkoy give a Littlewood--Paley energy-flux convolution and a natural
critical-space sharpness mechanism for Euler
[CCFS 2007](https://arxiv.org/abs/0704.0759).  The standard relation between
the Besov sequence index and separated dyadic packets is also part of the
classical LP framework summarized by
[Bahouri--Chemin--Danchin 2011](https://doi.org/10.1007/978-3-642-16830-7).
Accordingly, the \(q=3\) packet is an exact operator-level obstruction for
this defect, not a new general theory of Besov sequence exponents.

A bounded search of these primary sources did not locate the exact
\(B^0_{3,3}\) frame-defect inequality, its \(q=3\) packet obstruction, or the
top-eigenvalue filler family.  That is only a literature boundary, not a
novelty or priority claim.  A paper-level claim would require a broader
specialist search and external expert review.

## 12. Research value and next gate

R0.70Y has three concrete values.

1. It converts the orbitwise \(t/R\) observation into a full multiplier
   derivative estimate and a global, critical, log-free Besov theorem.
2. It proves that the shell sequence exponent cannot be weakened past
   \(q=3\), so further progress cannot come from a more permissive symmetric
   shell summation of the same form.
3. It separates two covariance hypotheses that were previously conflated:
   nonvanishing \(\lambda_1\) is insufficient, while a true
   \(\lambda_1-\lambda_2\) gap remains untested.

The response/metric split and the no-log mixed endpoint (1.4) are the strongest
research components.  Estimate (1.3) is a clean positive theorem but its
sequence mechanism is comparatively standard; the \(q=3\) packet is best
treated as a supporting proposition rather than a headline novelty.

The result is strong enough to serve as a rigorous lemma package in a larger
analysis paper.  On its own, its publication value is limited because the
uncontrolled principal term (1.8) is exactly where the remaining
vortex-stretching difficulty can reside.

The next mathematically justified stage is therefore not another search for a
post-convolution rank-one-null norm.  It is a two-pronged principal-term gate:

- derive an exact eigenprojector decomposition of \(\int S:Q\) under a true
  principal eigengap and identify the scale-critical coefficient it would
  require; and
- test whether a pre-convolution response-index tensor can control the
  principal and defect terms together without vanishing on the R0.70X field.

Only if one branch produces a complete enstrophy inequality should dynamic
propagation or large computation begin.

## 13. Reproduction and exact certificate

Run

```bash
tmp/r068b-venv/bin/python research/r070y_exact_audit.py
```

The producer emits one canonical JSON document and verifies six groups:

1. response-chord, symmetric, metric/response, wedge, and Gram identities;
2. the \(M\ge4\) radial-frame response-area obstruction;
3. scale-packet separation arithmetic;
4. filler covariance and the \(1/41210\) top-eigenvalue lower bound ledger;
5. the explicit and asymptotic principal-eigengap boundary; and
6. a forty-mode Fourier/Parseval reconstruction with 376 defect outputs.

The archived polynomial is

\[
 -\frac{81(62+1639\kappa)}{32780}\Lambda^3,
 \tag{13.1}
\]

with exact zero coefficients at powers \(\Lambda^2,\Lambda,\Lambda^0\).
The producer imports the already archived R0.70X thirty-six-mode field; its
checksum is therefore part of the R0.70Y dependency ledger.

## 14. Claim boundary

R0.70Y proves or supports, with the stated analytic lemmas:

- exact response-chord, metric/response, wedge-norm, and Gram-trace identities;
- a concrete radial-frame obstruction to Gram-area divisibility;
- the critical estimates (1.3)--(1.4);
- sharpness of \(q=3\) within the symmetric \(B^0_{3,q}\) cubic family; and
- failure of the old \(G_Q\) estimate even under a uniform positive lower
  bound on \(\lambda_1(Q)\).

It does not prove:

- a no-go theorem under a true uniform principal eigengap;
- control of \(\int S:Q\);
- propagation of an \(L^1_tB^0_{\infty,\infty}\) coefficient;
- an enstrophy closure or continuation theorem;
- finite-time blow-up or global smoothness; or
- a solution of the Navier--Stokes Millennium problem.
