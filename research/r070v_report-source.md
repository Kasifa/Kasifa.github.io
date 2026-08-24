# R0.70V — Response-distance decomposition and the strain-projected critical defect

**Status:** internal canonical candidate; not a public theorem chapter

**Release:** R0.70V

**Date:** 2026-08-25

## 1. Decision

R0.70U left the exact complete-frame defect

\[
 \mathcal D_\times
 =\omega\otimes\omega-Q,
 \qquad
 Q=\sum_\alpha T_\alpha\omega\otimes T_\alpha\omega,
 \tag{1.1}
\]

visible in the signed stretching commutator

\[
 \mathfrak E_S
 =\int_{\mathbb T^3}S:\mathcal D_\times\,dx.
 \tag{1.2}
\]

This release identifies the exact harmonic-analysis structure of
\(\mathcal D_\times\) and decides which norm of it is relevant to the
enstrophy ledger.

The main conclusions are as follows.

1. The complete Parseval frame gives an exact carré-du-champ identity and a
   nonnegative Fourier response-distance kernel:

   \[
    \widehat{\mathcal D_\times}(n)
    =\sum_{p+q=n}K(p,q)\widehat\omega(p)\otimes\widehat\omega(q),
    \qquad
    K(p,q)=\frac12\|V(p)-V(q)\|_{\ell^2}^2.
    \tag{1.3}
   \]

2. The kernel vanishes quadratically when the two input radii approach one
   another.  In particular, a vorticity supported in one Laplacian sphere
   has \(\mathcal D_\times\equiv0\), and a logarithmically narrow radial band
   satisfies a mode-count-independent \(L^1\) estimate.

3. The full tensor is nevertheless too large a target.  A fixed-frame,
   two-shell, smooth periodic shear has a globally simple rank-one covariance
   and residual \(r\equiv0\), while

   \[
    \|\mathcal D_\times\|_{\dot H^{-1}_\#,F}>0.
    \tag{1.4}
   \]

   Hence no positive power of \(r\) controls the full tensor in any ordinary
   definite tensor norm, even under exact rank one.

4. That counterexample is invisible to vortex stretching.  The signed term
   sees only the strain-compatible projection

   \[
    \mathfrak X_\times
    =\sum_{n\ne0}|n|^{-2}
      |\nu_n\times\widehat{\mathcal D_\times}(n)\nu_n|^2,
    \qquad \nu_n=\frac n{|n|}.
    \tag{1.5}
   \]

   The exact Fourier ledger is

   \[
    \boxed{
    |\mathfrak E_S|
    \le \|\nabla\omega\|_2\mathfrak X_\times^{1/2}
    \le \frac\nu2\|\nabla\omega\|_2^2
       +\frac1{2\nu}\mathfrak X_\times.}
    \tag{1.6}
   \]

5. The R0.70U three-frequency family saturates the orders in (1.6):

   \[
    \mathfrak X_{\times,\varepsilon}
    =\Theta(\varepsilon^2),
    \qquad
    |\mathfrak E_S(\varepsilon)|=\Theta(|\varepsilon|),
    \qquad
    \|r_\varepsilon\|_{L^p}^{1/2}=\Theta(|\varepsilon|).
    \tag{1.7}
   \]

The route decision is therefore asymmetric.  Control of the full tensor by
\(r\) is stopped.  The strain-projected quantity \(\mathfrak X_\times\), at
square-root order, remains open and becomes the next target.  Formula (1.6)
is a viscosity-absorption ledger, not a closure: no energy-level a priori
bound for \(\int\mathfrak X_\times\,dt\) is proved here, and the principal
term \(\int S:Q\) is not controlled by this release.

This is not an enstrophy estimate, a continuation theorem, a singularity
construction, a global-regularity theorem, or a solution of the Millennium
problem.  No DNS or DGX computation is justified for this finite Fourier and
operator-identity gate.  No formal figure is created because there is no
numerical data to visualize.  No public-page update or GitHub publication is
authorized by this report.

## 2. Conventions and the complete response vector

Work on the normalized torus

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3,
 \qquad \int_{\mathbb T^3}1\,dx=1.
 \tag{2.1}
\]

For a scalar, vector, or tensor field \(f\), use

\[
 \widehat f(n)=\int_{\mathbb T^3}f(x)e^{-in\cdot x}\,dx,
 \qquad
 f(x)=\sum_{n\in\mathbb Z^3}\widehat f(n)e^{in\cdot x}.
 \tag{2.2}
\]

Let \(u\) be a smooth, real, mean-zero, divergence-free periodic velocity,
and put

\[
 \omega=\nabla\times u,
 \qquad
 B_{ij}=\partial_i u_j,
 \qquad
 S=\frac12(B+B^{\mathsf T}).
 \tag{2.3}
\]

Use the pinned real-even complete scalar frame

\[
 \mathscr T=\{T_\star=\Pi_0\}\cup\{T_j:j\in\mathbb Z\},
 \tag{2.4}
\]

with multiplier symbols

\[
 m_\star(n)=\mathbf1_{\{n=0\}},
 \qquad
 m_j(0)=0,
 \qquad
 m_j(n)=\varphi(2^{-j}n)\quad(n\ne0).
 \tag{2.5}
\]

The cutoff \(\varphi\) is real, even, radial, and smooth, and satisfies

\[
 \operatorname{supp}\varphi
 \subset\{\tfrac12<|\xi|<2\},
 \qquad
 \sum_{j\in\mathbb Z}|\varphi(2^{-j}\xi)|^2=1
 \quad(\xi\ne0).
 \tag{2.6}
\]

Thus every \(T_\alpha\) is self-adjoint and

\[
 \sum_{\alpha\in\{\star\}\cup\mathbb Z}T_\alpha^2=I.
 \tag{2.7}
\]

Define the response vector

\[
 V(n)=\bigl(m_\alpha(n)\bigr)_\alpha\in\ell^2,
 \qquad \|V(n)\|_{\ell^2}=1
 \quad(n\in\mathbb Z^3).
 \tag{2.8}
\]

For \(n\ne0\), radiality permits the notation

\[
 v(|n|)=V(n).
 \tag{2.9}
\]

The constant coordinate is essential when the frame is applied to a
product.  Although \(\Pi_0\omega=0\), generally
\(\Pi_0(\omega\otimes\omega)\ne0\).  Omitting \(T_\star\) from a product
identity below would create a false zero-mode defect.

Tensor norms use the full Frobenius convention

\[
 |D|_F^2=\sum_{i,j=1}^3|D_{ij}|^2.
 \tag{2.10}
\]

For a mean-zero tensor field, define the homogeneous periodic norm

\[
 \|D\|_{\dot H^{-1}_\#,F}^2
 =\sum_{n\ne0}|n|^{-2}|\widehat D(n)|_F^2.
 \tag{2.11}
\]

The subscript \(\#\) records the periodic mean-zero convention.  It is not
the inhomogeneous Bessel-potential norm.

Whenever the covariance \(Q\) in (3.1) has a simple top eigenvalue, write

\[
 \lambda_1>\lambda_2\ge\lambda_3\ge0,
 \qquad
 L=\ell\otimes\ell,
 \qquad
 P=I-L,
 \qquad
 r=\operatorname{tr}(PQP)=\lambda_2+\lambda_3.
 \tag{2.12}
\]

All statements involving \(r\), \(L\), or \(P\) use this convention.

## 3. Exact carré-du-champ and response distance

Set

\[
 \Omega_\alpha=T_\alpha\omega,
 \qquad
 Q=\sum_\alpha\Omega_\alpha\otimes\Omega_\alpha,
 \qquad
 \mathcal D_\times=\omega\otimes\omega-Q.
 \tag{3.1}
\]

### Proposition 3.1 — complete-frame carré-du-champ

For smooth \(\omega\),

\[
 \boxed{
 \mathcal D_\times
 =\sum_\alpha
  \left[T_\alpha^2(\omega\otimes\omega)
   -(T_\alpha\omega)\otimes(T_\alpha\omega)\right].}
 \tag{3.2}
\]

It also has the symmetric field-level form

\[
 \boxed{
 \mathcal D_\times
 =\frac12\sum_\alpha
 \left[(T_\alpha^2\omega)\otimes\omega
       +\omega\otimes(T_\alpha^2\omega)
       -2(T_\alpha\omega)\otimes(T_\alpha\omega)\right].}
 \tag{3.3}
\]

For \(\omega\in L^2\), (3.3) is well defined in \(L^1\), with the first
two sums understood through \(L^2\) reconstruction, and

\[
 \boxed{
 \|\mathcal D_\times\|_{L^1(F)}
 \le2\|\omega\|_2^2.}
 \tag{3.4}
\]

#### Proof

Equation (3.2) follows from (2.7) applied to the product and from the
definition of \(Q\).  Equation (3.3) follows from
\(\sum_\alpha T_\alpha^2\omega=\omega\).  Finally,

\[
 \|\omega\otimes\omega\|_{L^1(F)}=\|\omega\|_2^2,
 \qquad
 \sum_\alpha
 \|T_\alpha\omega\otimes T_\alpha\omega\|_{L^1(F)}
 =\sum_\alpha\|T_\alpha\omega\|_2^2
 =\|\omega\|_2^2,
 \tag{3.5}
\]

which proves (3.4).  \(\square\)

### Proposition 3.2 — Fourier Gram-distance kernel

For every output frequency \(n\),

\[
 \boxed{
 \widehat{\mathcal D_\times}(n)
 =\sum_{p+q=n}K(p,q)
   \widehat\omega(p)\otimes\widehat\omega(q),}
 \tag{3.6}
\]

where

\[
 \boxed{
 \begin{aligned}
 K(p,q)
 &=1-\Gamma(p,q),\\
 \Gamma(p,q)
 &=\langle V(p),V(q)\rangle_{\ell^2},\\
 K(p,q)
 &=\frac12\|V(p)-V(q)\|_{\ell^2}^2.
 \end{aligned}}
 \tag{3.7}
\]

Consequently,

\[
 0\le K(p,q)\le2.
 \tag{3.8}
\]

This scalar positivity survives a sign-changing cutoff.  It does not imply
that \(\mathcal D_\times(x)\) is a positive-semidefinite tensor.

#### Proof

The Fourier coefficient of \(Q\) is

\[
 \widehat Q(n)
 =\sum_{p+q=n}\sum_\alpha
   m_\alpha(p)m_\alpha(q)
   \widehat\omega(p)\otimes\widehat\omega(q).
 \tag{3.9}
\]

Subtracting it from the convolution formula for
\(\omega\otimes\omega\) gives the first two lines of (3.7).  Since both
response vectors have norm one,

\[
 \frac12\|V(p)-V(q)\|_{\ell^2}^2
 =1-\langle V(p),V(q)\rangle,
 \tag{3.10}
\]

and (3.8) follows.  \(\square\)

### Corollary 3.3 — exact zero-mode cancellation

Evenness gives \(V(-p)=V(p)\), hence

\[
 K(p,-p)=0,
 \qquad
 \widehat{\mathcal D_\times}(0)=0,
 \qquad
 \int_{\mathbb T^3}\mathcal D_\times\,dx=0.
 \tag{3.11}
\]

This agrees with tensor Parseval:

\[
 \int\omega\otimes\omega\,dx
 =\sum_\alpha\int
   T_\alpha\omega\otimes T_\alpha\omega\,dx.
 \tag{3.12}
\]

## 4. Radial geometry of the kernel

For \(r>0\), set

\[
 v(r)=\bigl(\varphi(2^{-j}re_1)\bigr)_{j\in\mathbb Z},
 \qquad \|v(r)\|_{\ell^2}=1,
 \tag{4.1}
\]

and define the finite logarithmic derivative constant

\[
 M_\varphi
 =\sup_{r>0}
  \left(\sum_j
  |(2^{-j}re_1)\cdot\nabla\varphi(2^{-j}re_1)|^2
  \right)^{1/2}.
 \tag{4.2}
\]

Only finitely many summands are nonzero at each \(r\), uniformly in \(r\).
The fundamental theorem of calculus in \(\ell^2\) gives

\[
 \|v(r)-v(s)\|_{\ell^2}
 \le M_\varphi\left|\log\frac rs\right|.
 \tag{4.3}
\]

Therefore, for nonzero frequencies,

\[
 \boxed{
 K(p,q)
 \le\min\left\{2,
 \frac{M_\varphi^2}{2}
 \left|\log\frac{|p|}{|q|}\right|^2\right\}.}
 \tag{4.4}
\]

### 4.1 Same-radius annihilation

If \(|p|=|q|\), then \(V(p)=V(q)\) and

\[
 K(p,q)=0.
 \tag{4.5}
\]

Hence every mean-zero field whose Fourier support lies in one Laplacian
sphere satisfies

\[
 \boxed{\mathcal D_\times\equiv0.}
 \tag{4.6}
\]

Equation (4.6) concerns only the frame defect.  It does not assert that the
physical vortex-stretching integral vanishes for every such field.

### 4.2 Quadratic local order

Writing \(s=re^h\), smoothness and \(\|v(r)\|_{\ell^2}=1\) give

\[
 \boxed{
 K(re^h,r)
 =\frac{h^2}{2}
  \|\partial_{\log r}v(r)\|_{\ell^2}^2
  +O_\varphi(|h|^3).}
 \tag{4.7}
\]

The derivative cannot vanish for every \(r\).  Otherwise \(v\) would be
constant in \(r\), while

\[
 v(2r)_j=v(r)_{j-1}
 \tag{4.8}
\]

would make that nonzero unit vector shift invariant in \(\ell^2\), which is
impossible.  Thus the quadratic order in (4.7) is attained at some response
phase.  The coefficient is frame dependent.

The response is invariant under a common dyadic scaling, through the index
shift (4.8).  For a general smooth cutoff it is not invariant under an
arbitrary continuous common scaling.  Accordingly, \(\Gamma(p,q)\) must not
be described as a function only of \(|p|/|q|\).

### 4.3 High-high to low compensation

If \(p+q=n\ne0\) and \(\min\{|p|,|q|\}\ge N\), then

\[
 \left|\log\frac{|p|}{|q|}\right|
 \le\frac{\bigl||p|-|q|\bigr|}{\min\{|p|,|q|\}}
 \le\frac{|n|}{N}.
 \tag{4.9}
\]

Thus

\[
 \boxed{
 K(p,q)\le\frac{M_\varphi^2}{2}\frac{|n|^2}{N^2}.}
 \tag{4.10}
\]

This quadratic cancellation neutralizes the explicit \(|n|^{-2}\) weight in
\(\mathfrak X_\times\) for a single high-high-to-low interaction.  It does
not sum the interactions, and therefore is not yet a bilinear estimate.

At the opposite extreme, the strict annular support in (2.6) makes the
response supports at radii \(r\) and \(4r\) disjoint.  Hence

\[
 \Gamma(re_1,4re_1)=0,
 \qquad K(re_1,4re_1)=1.
 \tag{4.11}
\]

Separated-shell interactions survive with full coefficient.

## 5. A positive narrow-radial-band theorem

### Theorem 5.1 — mode-count-independent \(L^1\) control

Suppose

\[
 \operatorname{supp}\widehat\omega
 \subset
 \left\{n\ne0:
 \left|\log\frac{|n|}{\rho}\right|\le\delta\right\}
 \tag{5.1}
\]

for some \(\rho>0\) and \(\delta\ge0\).  Then

\[
 \boxed{
 \|\mathcal D_\times\|_{L^1(F)}
 \le
 \min\{2,2M_\varphi^2\delta^2\}
 \|\omega\|_2^2.}
 \tag{5.2}
\]

#### Proof

Put

\[
 c_\star=0,
 \qquad
 c_j=v(\rho)_j\quad(j\in\mathbb Z),
 \qquad
 e_\alpha=(T_\alpha-c_\alpha I)\omega,
 \qquad
 g=\sum_\alpha c_\alpha e_\alpha.
 \tag{5.3}
\]

The zero constant coordinate reflects \(\rho>0\).  The mean-zero hypothesis
also gives \(e_\star=0\).

Let

\[
 \beta
 =\sup_{n\in\operatorname{supp}\widehat\omega}
  \|V(n)-v(\rho)\|_{\ell^2}
 \le M_\varphi\delta.
 \tag{5.4}
\]

Plancherel gives

\[
 \sum_\alpha\|e_\alpha\|_2^2
 \le\beta^2\|\omega\|_2^2.
 \tag{5.5}
\]

The unit-sphere identity

\[
 \langle v(\rho),V(n)-v(\rho)\rangle
 =-\frac12\|V(n)-v(\rho)\|_{\ell^2}^2
 \tag{5.6}
\]

improves the naive first-order estimate to

\[
 \|g\|_2\le\frac{\beta^2}{2}\|\omega\|_2.
 \tag{5.7}
\]

Expanding \(T_\alpha\omega=c_\alpha\omega+e_\alpha\), using
\(\sum c_\alpha^2=1\), gives

\[
 \mathcal D_\times
 =-\omega\otimes g-g\otimes\omega
  -\sum_\alpha e_\alpha\otimes e_\alpha.
 \tag{5.8}
\]

Cauchy--Schwarz, (5.5), and (5.7) yield

\[
 \|\mathcal D_\times\|_{L^1(F)}
 \le2\|\omega\|_2\|g\|_2
   +\sum_\alpha\|e_\alpha\|_2^2
 \le2\beta^2\|\omega\|_2^2.
 \tag{5.9}
\]

Combining this with (3.4) proves (5.2).  \(\square\)

The gain in (5.2) is quadratic in logarithmic bandwidth and independent of
the number of Fourier modes.  It is not a smallness theorem for a general
solution: Navier--Stokes evolution need not preserve (5.1).

## 6. Exact rank does not control the full tensor

Fix an integer \(N\ge1\) and nonzero real amplitudes \(A,B\).  Define

\[
 \omega(x)
 =e_3\bigl[A\cos(Nx_1)+B\cos(4Nx_1)\bigr].
 \tag{6.1}
\]

This is a smooth, real, mean-zero, divergence-free periodic vorticity.  The
response index sets at radii \(N\) and \(4N\) are disjoint, so their frame
cross term vanishes exactly.  Consequently,

\[
 \boxed{
 Q(x)=e_3\otimes e_3
 \left[A^2\cos^2(Nx_1)+B^2\cos^2(4Nx_1)\right].}
 \tag{6.2}
\]

The two cosines never vanish simultaneously: if \(\cos(Nx_1)=0\), then
\(\cos(4Nx_1)=1\).  Thus (6.2) has a globally simple positive top eigenvalue,
rank exactly one, and

\[
 r=\operatorname{tr}(PQP)\equiv0.
 \tag{6.3}
\]

On the other hand,

\[
 \boxed{
 \begin{aligned}
 \mathcal D_\times
 &=2AB\cos(Nx_1)\cos(4Nx_1)e_3\otimes e_3\\
 &=AB\bigl[\cos(3Nx_1)+\cos(5Nx_1)\bigr]e_3\otimes e_3,
 \end{aligned}}
 \tag{6.4}
\]

and normalized Fourier Parseval gives

\[
 \boxed{
 \|\mathcal D_\times\|_{\dot H^{-1}_\#,F}^2
 =\frac{17A^2B^2}{225N^2}>0.}
 \tag{6.5}
\]

The same tensor is nonzero in every standard definite \(L^p\), Sobolev, or
Besov tensor norm in which it is measured.  Hence an estimate of the form

\[
 \|\mathcal D_\times\|_X
 \le F\|r\|_Y^\theta,
 \qquad \theta>0,
 \tag{6.6}
\]

cannot hold on all smooth fixed-frame vorticities when \(F\) is finite on
this sample and \(X\) is such a definite norm.

This counterexample remains inside the actual common-vorticity frame origin;
it is not an abstract covariance matrix.  Nonnegative frame responses do not
remove it.  The missing information is polarization: both shells are
parallel to \(e_3\), so the covariance remains rank one even though their
response vectors are separated.

The Biot--Savart velocity of (6.1) is an \(e_2\)-directed shear depending
only on \(x_1\).  Its strain has only \(12\) and \(21\) entries, whereas
\(\mathcal D_\times\) has only a \(33\) entry.  Therefore

\[
 S:\mathcal D_\times\equiv0,
 \qquad
 \mathfrak E_S=0.
 \tag{6.7}
\]

The example disproves full-tensor control, not critical control of the
signed stretching work.

## 7. The exact strain-projected viscosity ledger

For a real symmetric mean-zero tensor \(D\), define

\[
 \mathfrak X[D]
 =\sum_{n\ne0}|n|^{-2}
  |\nu_n\times\widehat D(n)\nu_n|^2,
 \qquad \nu_n=\frac n{|n|}.
 \tag{7.1}
\]

Thus \(\mathfrak X_\times=\mathfrak X[\mathcal D_\times]\).  The unit vector
\(\nu_n\), rather than the unnormalized frequency \(n\), is essential for
the derivative count in (7.1).

### Proposition 7.1 — strain projection

For smooth mean-zero divergence-free \(\omega\) and its Biot--Savart strain,

\[
 \boxed{
 \left|\int_{\mathbb T^3}S:D\,dx\right|
 \le\|\nabla\omega\|_2\mathfrak X[D]^{1/2}.}
 \tag{7.2}
\]

If \(D\) is symmetric, then

\[
 \boxed{
 \mathfrak X[D]
 \le\frac12\|D\|_{\dot H^{-1}_\#,F}^2.}
 \tag{7.3}
\]

Both constants are sharp on the ambient class of compatible vorticity modes
paired with arbitrary real symmetric mean-zero tensor modes.  This statement
does not claim that equality is realized when \(D\) is additionally
constrained to equal the frame defect of the same \(\omega\).

#### Proof

Biot--Savart gives, for \(n\ne0\),

\[
 \widehat u(n)=\frac{i\,n\times\widehat\omega(n)}{|n|^2}.
 \tag{7.4}
\]

Under the row-gradient convention in (2.3),

\[
 \widehat S(n)
 =-\frac12\left[
 \nu_n\otimes(\nu_n\times\widehat\omega(n))
 +(\nu_n\times\widehat\omega(n))\otimes\nu_n
 \right].
 \tag{7.5}
\]

Since \(D\) is real and symmetric, Fourier Parseval and the scalar triple
product give

\[
 \begin{aligned}
 \int S:D\,dx
 &=\sum_{n\ne0}\widehat S(n):\overline{\widehat D(n)}\\
 &=\sum_{n\ne0}\widehat\omega(n)\cdot
   \overline{\nu_n\times\widehat D(n)\nu_n}.
 \end{aligned}
 \tag{7.6}
\]

Weighted Cauchy--Schwarz proves (7.2).  For (7.3), rotate
\(\nu_n\) to \(e_1\).  Symmetry gives

\[
 |e_1\times\widehat D(n)e_1|^2
 =|D_{12}|^2+|D_{13}|^2
 \le\frac12|\widehat D(n)|_F^2,
 \tag{7.7}
\]

because the full Frobenius norm counts each of these off-diagonal entries
twice.  Summing with weight \(|n|^{-2}\) proves (7.3).  \(\square\)

Young's inequality now yields, for every viscosity \(\nu>0\),

\[
 \boxed{
 \begin{aligned}
 |\mathfrak E_S|
 &\le\frac\nu2\|\nabla\omega\|_2^2
  +\frac1{2\nu}\mathfrak X_\times\\
 &\le\frac\nu2\|\nabla\omega\|_2^2
  +\frac1{4\nu}
    \|\mathcal D_\times\|_{\dot H^{-1}_\#,F}^2.
 \end{aligned}}
 \tag{7.8}
\]

For example, the ambient choice

\[
 \omega=e_2\cos x_1,
 \qquad
 D=-\cos x_1(e_1\otimes e_3+e_3\otimes e_1)
 \tag{7.9}
\]

attains equality in both Cauchy--Schwarz and (7.3), with

\[
 \left|\int S:D\right|=\frac12,
 \quad
 \|\nabla\omega\|_2^2=\frac12,
 \quad
 \mathfrak X[D]=\frac12,
 \quad
 \|D\|_{\dot H^{-1}_\#,F}^2=1.
 \tag{7.10}
\]

The tensor in the exact-rank shear of Section 6 instead satisfies

\[
 \mathfrak X_\times=0
 \tag{7.11}
\]

despite (6.5).  Equations (7.10)--(7.11) show why the strain projection, not
the full tensor norm, is the minimally faithful signed target.

## 8. Critical saturation and the chord--area boundary

Return to the fixed R0.70U Pythagorean family.  Its two radial responses have
inner product \(\gamma\), with \(|\gamma|\le3/4\), and

\[
 \omega_\varepsilon=w+\varepsilon h.
 \tag{8.1}
\]

Since the modes forming \(w\) share one radius and \(h\) has the second
radius, the frame defect is exactly

\[
 \boxed{
 \mathcal D_{\times,\varepsilon}
 =\varepsilon(1-\gamma)
  (w\otimes h+h\otimes w).}
 \tag{8.2}
\]

Thus

\[
 \mathfrak X_{\times,\varepsilon}
 =\varepsilon^2(1-\gamma)^2X_0(A,\delta,m).
 \tag{8.3}
\]

The output frequencies \(\pm k\) alone contribute

\[
 X_0(A,\delta,m)
 \ge\frac{\delta^2m^2}{2(m^2+1)^4}>0.
 \tag{8.4}
\]

Because the family has finitely many fixed modes, \(X_0<\infty\).  Hence

\[
 \boxed{
 \mathfrak X_{\times,\varepsilon}=\Theta(\varepsilon^2),
 \qquad
 \mathfrak X_{\times,\varepsilon}^{1/2}=\Theta(|\varepsilon|).}
 \tag{8.5}
\]

R0.70U proved

\[
 |\mathfrak E_S(\varepsilon)|=\Theta(|\varepsilon|),
 \qquad
 \|r_\varepsilon\|_{L^p}=\Theta(\varepsilon^2)
 \quad(1\le p\le\infty).
 \tag{8.6}
\]

Therefore this one family saturates the algebraic orders

\[
 |\mathfrak E_S|
 \asymp\mathfrak X_\times^{1/2}
 \asymp\|r\|_{L^p}^{1/2}.
 \tag{8.7}
\]

This does not prove \(\mathfrak X_\times\lesssim\|r\|\), even on the family;
it only shows that such a critical comparison is not contradicted by the
R0.70U obstruction.

For two unit response vectors, set

\[
 d=1-\gamma,
 \qquad
 \kappa=1-\gamma^2.
 \tag{8.8}
\]

Here \(d\) is the squared-chord coefficient in \(\mathcal D_\times\), while
\(\kappa\) is the two-channel covariance Gram-area coefficient.  Exactly,

\[
 \boxed{
 \kappa=d(2-d)=d(1+\gamma)}
 \tag{8.9}
\]

for every \(-1\le\gamma\le1\).  On the open branch
\(-1<\gamma<1\),

\[
 \boxed{
 \frac d{\sqrt\kappa}
 =\sqrt{\frac{1-\gamma}{1+\gamma}}.}
 \tag{8.9a}
\]

At \(\gamma=1\), both \(d\) and \(\kappa\) vanish and the corresponding
frame-defect pair is zero; the ratio in (8.9a) is the undefined expression
\(0/0\).  At \(\gamma=-1\), \(d=2\) while \(\kappa=0\), so covariance area
cannot control the response chord.

Thus any conversion from response chord to covariance area must prevent
anti-correlation:

\[
 1+\gamma\ge\sigma>0.
 \tag{8.10}
\]

A nonnegative cutoff gives \(\gamma\ge0\) pairwise and permits
\(\sigma=1\).  The present real-even assumptions allow sign changes and do
not imply (8.10).  The selected R0.70U pair has \(|\gamma|\le3/4\), so

\[
 d\le4\kappa,
 \qquad
 \frac d{\sqrt\kappa}\le\sqrt7.
 \tag{8.11}
\]

The exact-rank shear in Section 6 shows that even a nonnegative cutoff and
perfect anti-correlation guard cannot control the full tensor by covariance
area.  Parallel physical polarizations make every covariance cross product
zero while the response chord remains nonzero.  Any viable critical theorem
must use the strain projection or an equivalent triadic cancellation.

## 9. The remaining pairwise-area gate

The positive covariance identity is

\[
 \boxed{
 \sum_{\alpha<\beta}
 |\Omega_\alpha\times\Omega_\beta|^2
 =\lambda_1\lambda_2+\lambda_1\lambda_3+\lambda_2\lambda_3
 =\lambda_1r+\lambda_2\lambda_3.}
 \tag{9.1}
\]

It records physical polarization area between frame blocks.  In contrast,
the Fourier formula (3.6) weights pairs by response distance before the
pairs are recombined in physical space.  The two-shell shear proves that
these two pieces of information cannot be compared before the strain
projection is imposed.

The high-high-to-low estimate (4.10) supplies one encouraging mechanism:
the quadratic response-distance zero cancels the low-output singular weight
in (7.1).  The far-shell region has no such small coefficient, but it has
strong scale separation and is the natural domain for paraproduct estimates.

### Proposition 9.1 — exact triad-area reduction

Let

\[
 n+k+l=0,
 \qquad
 n\cdot c=k\cdot a=l\cdot b=0,
 \qquad n,k,l\ne0,
 \tag{9.2}
\]

and let \(S_c\) denote the strain symbol (7.5) at frequency \(n\) with
vorticity coefficient \(c\).  Then

\[
 \boxed{
 S_c:(a\otimes b+b\otimes a)
 =\frac{[(l-k)\times(\nu_n\times c)]\cdot(a\times b)}{|n|}.}
 \tag{9.3}
\]

Consequently,

\[
 \left|S_c:(a\otimes b+b\otimes a)\right|
 \le\frac{|k|+|l|}{|n|}|c|\,|a\times b|.
 \tag{9.4}
\]

#### Proof

Put \(z=\nu_n\times c\).  Direct contraction of
\(S_c=-\tfrac12(\nu_n\otimes z+z\otimes\nu_n)\) gives

\[
 S_c:(a\otimes b+b\otimes a)
 =-[(\nu_n\cdot a)(z\cdot b)
   +(\nu_n\cdot b)(z\cdot a)].
 \tag{9.5}
\]

Using \(n=-k-l\), \(k\cdot a=0\), and \(l\cdot b=0\), the right side is

\[
 \frac{(l\cdot a)(z\cdot b)+(k\cdot b)(z\cdot a)}{|n|}.
 \tag{9.6}
\]

The Lagrange identity for the two cross products in (9.3) gives exactly
(9.6).  The bound follows from
\(|l-k|\le|l|+|k|\) and \(|z|\le|c|\).  The bilinear identity remains valid
for complex Fourier coefficients; the displayed estimate uses their
Hermitian Euclidean moduli.  \(\square\)

The response distance removes the apparent low-output singularity uniformly.
Indeed, with \(\rho_k=|k|\), \(\rho_l=|l|\),
\(h=|\log(\rho_k/\rho_l)|\), and \(t=|k+l|\),

\[
 t\ge|\rho_k-\rho_l|,
 \qquad
 \frac{\rho_k+\rho_l}{t}\le\coth\frac h2\le1+\frac2h
 \quad(\rho_k\ne\rho_l).
 \tag{9.7}
\]

Combining (4.4) with
\(\min\{2,M_\varphi^2h^2/2\}\le M_\varphi h\) gives

\[
 \boxed{
 K(k,l)\frac{|k|+|l|}{|k+l|}
 \le C_\varphi,
 \qquad C_\varphi=2+2M_\varphi.}
 \tag{9.8}
\]

The case \(\rho_k=\rho_l\) is immediate because \(K(k,l)=0\).  Hence every
nonzero triad satisfies the pairwise estimate

\[
 \boxed{
 K(k,l)
 \left|S_c:(a\otimes b+b\otimes a)\right|
 \le C_\varphi|c|\,|a\times b|.}
 \tag{9.9}
\]

There is also an exact response-area coefficient

\[
 \kappa(k,l)
 =1-\Gamma(k,l)^2
 =\sum_{\alpha<\beta}
  |m_\alpha(k)m_\beta(l)-m_\beta(k)m_\alpha(l)|^2.
 \tag{9.10}
\]

If the anti-correlation guard \(1+\Gamma(k,l)\ge\sigma>0\) holds, then the
\(\Gamma=1\) branch is trivial because \(K=\kappa=0\).  On every remaining
branch, the same argument uses
\(K/\sqrt\kappa=\sqrt{K/(1+\Gamma)}\) and gives

\[
 \boxed{
 K(k,l)
 \left|S_c:(a\otimes b+b\otimes a)\right|
 \le C_{\varphi,\sigma}|c|\,
       \sqrt{\kappa(k,l)}\,|a\times b|,}
 \tag{9.11}
\]

where one admissible constant is

\[
 C_{\varphi,\sigma}
 =\frac{\sqrt2(1+M_\varphi)}{\sqrt\sigma}.
 \tag{9.12}
\]

Thus the low-output derivative loss and the two-channel response coefficient
can both be paid pairwise by physical polarization area.  This is a genuine
positive reduction, but it is not yet the required field estimate.

The unresolved mathematical step is a vector-valued bilinear summation that
turns the strain-projected Fourier pairs into a spacetime quantity controlled
by (9.1), palinstrophy, or a critical combination of the two.  A pointwise
comparison of the full tensor has already been disproved.  A pair-by-pair
estimate is also insufficient unless its constants survive summation over
all modes and shells.

No theorem of the form

\[
 \mathfrak X_\times(t)
 \le C\int_{\mathbb T^3}
   \bigl(\lambda_1r+\lambda_2\lambda_3\bigr)(x,t)\,dx
 \tag{9.13}
\]

is asserted here.  In fact, (9.13) is too strong to be a scale-free
whole-space target.  For the homogeneous whole-space analogue of the pinned
frame, a dyadic Navier--Stokes dilation \(\mu=2^s\) shifts only the frame
index and gives

\[
 u_\mu(x,t)=\mu u(\mu x,\mu^2t),
 \qquad
 \omega_\mu(x,t)=\mu^2\omega(\mu x,\mu^2t),
 \tag{9.14}
\]

the defect has amplitude degree four, and therefore

\[
 \mathfrak X_\times[\omega_\mu](t)
 =\mu^3\mathfrak X_\times[\omega](\mu^2t),
 \qquad
 \int_{\mathbb R^3}
  (\lambda_1r+\lambda_2\lambda_3)[\omega_\mu],dx
 =\mu^5
  \int_{\mathbb R^3}
  (\lambda_1r+\lambda_2\lambda_3)[\omega],dx.
 \tag{9.15}
\]

The two sides differ by two frequency degrees.  On a fixed torus, a dyadic
integer dilation gives degrees six and eight instead; the same two-degree
mismatch is hidden by the lowest available frequency.  A dyadic sequence is
already enough to rule out a scale-free whole-space constant.  Thus (9.13)
is recorded as an overstrong comparator and is closed as a critical route.
The viable next gate must retain two inverse-frequency degrees, or an exactly
equivalent scale compensation, while performing the pairwise-area summation.

## 10. Prior-art boundary

The closest current filtered-vorticity comparison in the bounded primary-
source audit is
[Yu (2026)](https://arxiv.org/abs/2606.27560).  That preprint uses one smooth
spatial filter, its filtered vorticity, a localized filtered-enstrophy
balance, and a differentiated subgrid stress controlled by a filter-adapted
increment defect.  Writing \(\chi_\ell\) for that filter's scalar Fourier
multiplier, its quadratic stress has the usual filtered kernel

\[
 \chi_\ell(p+q)-\chi_\ell(p)\chi_\ell(q).
 \tag{10.1}
\]

The object here instead sums a complete band-pass Parseval frame.  The
product side contains \(T_\alpha^2\), the field side contains
\(T_\alpha\), and summing the output multipliers gives one.  The remaining
kernel is the input response distance (3.7).  The two defects therefore
cannot be identified.

[Eyink--Aluie (2009)](https://arxiv.org/abs/0909.2386) develop a multiscale
generalization of the Germano identity for smooth graded filters and prove
scale-locality bounds for energy transfer.  That work is the relevant
coarse-graining precedent for quadratic filter defects and near/far triadic
splitting.  It does not use the complete-frame covariance \(Q\), its
pointwise spectral residual \(r\), or the strain projection (7.1).

Littlewood--Paley vortex-stretching triads are treated by
[Yoneda--Goto--Tsuruhashi](https://arxiv.org/abs/2105.12459), and
frequency-localized regularity criteria by
[Bradshaw--Grujic](https://arxiv.org/abs/1501.01043).  These papers support
the general shell-interaction setting, but they do not supply (9.13).

The carré-du-champ formula, unit-sphere chord identity, and Fourier
Biot--Savart projection are elementary consequences of the pinned frame.
They are not presented as new general harmonic-analysis principles.  The
bounded search did not identify a directly isomorphic theorem coupling the
response-distance defect (3.7), the pointwise covariance area (9.1), and the
strain-projected norm (7.1).  That is a search result, not a novelty or
priority claim.  Independent manuscript-level review would be required
before any public theorem claim.

## 11. Next gate

R0.70W should test the missing summation in Section 9, with signs and the
strain projection retained from the start.

1. Split (3.6) into comparable-radius and separated-radius interactions.
2. In the comparable-radius region, combine the quadratic kernel bound
   (4.10) with the \(\dot H^{-1}\) output weight before applying any triangle
   inequality.
3. In the separated-radius region, derive the exact paraproduct placement of
   the low and high factors and record every derivative.
4. Test whether the resulting square function can be bounded by the
   covariance-area density (9.1) after retaining exactly two inverse-frequency
   degrees.  Reject every candidate that silently collapses to the
   scaling-incompatible comparison (9.13).
5. Use the R0.70U family as a lower-order saturation test and the Section 6
   shear as a mandatory null-projection test.
6. Stop the route if shell summation forces a supercritical derivative or an
   uncontrolled \(L^\infty\) norm.  Continue to a spacetime estimate only if
   the constants are uniform in the number of active modes and shells.

This gate remains analytic.  A numerical experiment would be useful only
after a precise inequality and a finite truncation with a convergence audit
have been specified.

## 12. Claim boundary

What is proved:

- the complete-frame carré-du-champ identities (3.2)--(3.3) and the robust
  \(L^1\) bound (3.4);
- the exact Fourier response-distance kernel (3.6)--(3.7), its zero mode,
  same-sphere annihilation, radial quadratic bound, and high-high-to-low
  factor;
- the mode-count-independent narrow-radial-band theorem (5.2);
- the actual fixed-frame globally simple rank-one counterexample
  (6.1)--(6.5), which rules out control of the full tensor by every positive
  power of \(r\) in ordinary definite tensor norms;
- the exact strain-projected Fourier ledger (7.2), the ambient symmetric-
  tensor comparison (7.3), and the viscosity insertion (7.8);
- critical-order saturation of \(\mathfrak X_\times^{1/2}\) on the R0.70U
  family;
- the chord--area identity and the necessity of an anti-correlation guard for
  a pairwise response-to-area conversion;
- the exact divergence-free triad identity (9.3), the uniform response-
  weighted estimate (9.9), and its guarded response-area form (9.11);
- the two-frequency-degree scaling obstruction to the scale-free whole-space
  analogue of the raw comparator (9.13); on the fixed torus this is a scaling
  warning rather than a standalone impossibility theorem.

What is not proved:

- \(\mathfrak X_\times\lesssim r\), or a scale-corrected substitute controlled
  only by the R0.70Q energy-level inputs;
- sharpness of the constants in (7.2)--(7.3) inside the constrained subclass
  \(D=\mathcal D_\times(\omega)\);
- propagation of narrow radial support, near rank one, a simple top gap, or
  an anti-correlation guard under Navier--Stokes evolution;
- summability of the near/far Fourier interactions at the critical scale;
- an a priori time bound for \(\int\mathfrak X_\times\,dt\);
- control of the principal covariance stretching term \(\int S:Q\);
- an enstrophy closure, continuation criterion verified from initial data,
  finite-time singularity, unconditional global regularity, or a solution of
  the Navier--Stokes Millennium problem.

The exact certificate for this release checks finite Gram, Fourier,
two-shell, strain-projection, and critical-exponent algebra.  Infinite-frame
reconstruction, the arbitrary-cutoff radial estimates, the narrow-band
operator theorem, and every PDE interpretation remain analytic arguments in
this report.
