# R0.70J — Deviatoric diagonal correlation: exact helical symbol and compact positive realization

**Status:** internal canonical research report; not a public theorem chapter
**Release:** R0.70J
**Date:** 2026-08-24
**Scope:** degree-zero exterior harmonic strain against the deviatoric
high--high vorticity tensor, with incompressibility, helical polarization,
angular averaging, physical cutoff, compact source/core realization, and the
R0.70G--R0.70I critical coordinates all kept explicit

---

## 1. Result in one page

R0.70I left one algebraic possibility open: perhaps the trace-free exterior
strain and the diagonal high--high vorticity tensor have a signed null
structure stronger than separate Hölder estimates. R0.70J computes the exact
symbol and closes that possibility in the negative.

Let

\[
 S=S^{\mathsf T},\qquad \operatorname{tr}S=0,
 \qquad
 \mathring Q(w)=w\otimes w-\frac{|w|^2}{3}I.
 \tag{1.1}
\]

The tensor contraction is exactly

\[
 \boxed{S:\mathring Q(w)=w^{\mathsf T}Sw.}
 \tag{1.2}
\]

Thus the deviatoric projection supplies no second cancellation: it only
records the isotropic cancellation already proved in R0.70I.

For a real pure-helicity vorticity wave of direction \(\xi\in S^2\),
helicity \(\sigma\in\{\pm1\}\), amplitude \(\rho\), and phase \(\theta\),
the phase-averaged symbol is

\[
 \boxed{
 K_S(\xi)
 :=\rho^{-2}\left\langle
 S:\mathring Q(\omega_{\sigma,\rho})
 \right\rangle_\theta
 =-\xi^{\mathsf T}S\xi.}
 \tag{1.3}
\]

It is independent of the helicity sign and even under
\(\xi\mapsto-\xi\). Hence opposite frequencies and homochiral projection do
not cancel it.

There is an exact pointwise counterexample. Put

\[
 S_0=\operatorname{diag}\left(\frac12,\frac12,-1\right),
 \qquad
 \omega_\sigma
 =\sqrt2\bigl(e_1\cos\theta-\sigma e_2\sin\theta\bigr).
 \tag{1.4}
\]

Then \(\omega_\sigma\) is a Beltrami wave and

\[
 \boxed{
 S_0:\mathring Q(\omega_\sigma)
 =\omega_\sigma^{\mathsf T}S_0\omega_\sigma
 \equiv1.}
 \tag{1.5}
\]

Consequently every nonzero nonnegative physical cutoff retains strict
positivity:

\[
 \int\chi\,S_0:\mathring Q(\omega_\sigma)\,dx
 =\int\chi\,dx>0.
 \tag{1.6}
\]

Full directional isotropy does give a signed cancellation because
\(\langle\xi\otimes\xi\rangle_{S^2}=I/3\). It does not survive a positive
part. For \(S_0\),

\[
 K_{S_0}(\xi)=\frac{3\xi_3^2-1}{2},\qquad
 \langle K_{S_0}\rangle_{S^2}=0,
 \qquad
 \boxed{\langle(K_{S_0})_+\rangle_{S^2}=\frac{\sqrt{3}}{9}>0.}
 \tag{1.7}
\]

The Fourier witness and the physical witness can both be made exact, but
not in the same impossible compact-and-bandlimited object. A periodic
Beltrami wave is an exact one-shell Fourier object. Separately, compact
homotopy localization gives a smooth divergence-free exterior vorticity
source whose strain is exactly \(S_0\) throughout a core, together with a
compact divergence-free carrier whose core vorticity is exactly the wave in
(1.4). All return vorticity is retained and the source/core supports are
strictly separated.

At the R0.70G--R0.70I degree-zero coordinates, with outer scale
\(R=\Lambda r\), amplitude \(a\), and a parabolic window of length \(r^2\),

\[
 c_r=a\Lambda^{-2}S_0,\qquad
 m_r=a^2Q_0,\qquad
 \mathcal N_r=r^{-2}m_r.
 \tag{1.8}
\]

The exact scale ledger is

\[
 \begin{aligned}
 \int r^{-1}|c_r|^2dt&\sim a^2r\Lambda^{-4},\\
 \int r|\mathcal N_r|^2dt&\sim a^4r^{-1},\\
 \int c_r:\mathcal N_r\,dt&\sim a^3\Lambda^{-2}>0.
 \end{aligned}
 \tag{1.9}
\]

Thus the direct source/core Cauchy product is scale-sharp. Choosing
\(a=r^{-1/2}\) also upgrades the abstract R0.70I degree-zero comparator to a
single compact smooth source/core profile with bounded velocity energy and
window dissipation. That family is a function-space comparator, not an NSE
trajectory.

The R0.70J conclusion is therefore precise:

> **Trace freedom removes only the isotropic tensor. Incompressibility,
> fixed helicity, phase averaging, a finite same-shell set, and physical
> cutoff do not remove the deviatoric diagonal. Full second-order isotropy
> gives only a signed pre-positive-part cancellation. Any successful direct
> route must use a quantitative anisotropy defect, a source-aware
> equation-specific correlation, or a different spacetime mechanism.**

Nothing here proves global regularity, constructs a singularity, or solves
the Millennium problem.

## 2. Exact tensor sector

### 2.1 What trace freedom actually kills

For every \(S\in\operatorname{Sym}_0(3)\),

\[
 S:\left(\frac{|w|^2}{3}I\right)=0.
 \tag{2.1}
\]

Subtracting (2.1) from \(S:(w\otimes w)=w^{\mathsf T}Sw\) proves (1.2).
The response \(\mathring Q(w)\) and the source \(S\) are both elements of
the same five-dimensional space \(\operatorname{Sym}_0(3)\). In spherical
harmonic language, both lie in the \(\ell=2\) representation. Orthogonality
to the scalar \(\ell=0\) sector therefore gives no reason for two
\(\ell=2\) tensors to be orthogonal to each other.

If \(S\ne0\), it has both a positive and a negative eigenvalue. Taking \(w\)
in a positive eigendirection gives \(w^{\mathsf T}Sw>0\). This elementary
observation already rules out a pointwise null structure for arbitrary
vectors. The remaining questions are whether incompressibility or the
helical/Fourier geometry removes those directions. They do not.

### 2.2 Incompressibility at one frequency

For a velocity mode \(u=a e^{ik\cdot x}\), incompressibility gives
\(k\cdot a=0\), and its vorticity amplitude is

\[
 b=ik\times a,\qquad k\cdot b=0.
 \tag{2.2}
\]

Conversely, every \(b\perp k\) is realized by

\[
 a=\frac{i\,k\times b}{|k|^2}.
 \tag{2.3}
\]

Thus incompressibility restricts the vorticity to the plane \(k^\perp\).
For a fixed direction \(\xi=k/|k|\), the contraction vanishes for every
admissible polarization if and only if

\[
 P_\xi S P_\xi=0,
 \qquad P_\xi=I-\xi\otimes\xi.
 \tag{2.4}
\]

Condition (2.4) is an exceptional compatibility between \(S\) and \(\xi\),
not a consequence of \(\operatorname{tr}S=0\).

## 3. The physical-cutoff Fourier identity

Fix the Fourier convention

\[
 \widehat f(\xi)=\int_{\mathbb R^3}e^{-ix\cdot\xi}f(x)\,dx.
 \tag{3.1}
\]

For a real field \(W\), a constant source tensor \(S\), and a physical
cutoff \(\chi\), the exact bilinear form is

\[
 \boxed{
 \int\chi(x)W(x)^{\mathsf T}SW(x)\,dx
 =\frac1{(2\pi)^6}
 \iint
 \widehat\chi(-\xi-\eta)
 \widehat W(\xi)^{\mathsf T}S\widehat W(\eta)
 \,d\xi d\eta.}
 \tag{3.2}
\]

When \(\chi\equiv1\), the delta distribution enforces
\(\eta=-\xi\), and reality converts the form to the diagonal covariance

\[
 \frac1{(2\pi)^3}\int
 \widehat W(\xi)^*S\widehat W(\xi)\,d\xi.
 \tag{3.3}
\]

For nonconstant \(\chi\), (3.2) contains coherent cross terms. A physical
cutoff is multiplication, not a Fourier projection, and it does not preserve
the global orthogonality of distinct output frequencies.

This prevents a common false argument. The positive-frequency complex
self-product of \(b e^{ik\cdot x}\) has output frequency \(2k\), so its
global periodic average is zero. A real mode also contains the conjugate
frequency. Its zero-frequency term is

\[
 2b^*Sb,
 \tag{3.4}
\]

which is generally nonzero. Dropping the \(k+(-k)=0\) term manufactures a
spurious cancellation.

## 4. Exact helical symbol

Choose a right-handed orthonormal frame \((e_1,e_2,\xi)\) and define

\[
 h_\sigma(\xi)=\frac{e_1+i\sigma e_2}{\sqrt2},
 \qquad \sigma\in\{\pm1\}.
 \tag{4.1}
\]

Then

\[
 i\xi\times h_\sigma=\sigma h_\sigma.
 \tag{4.2}
\]

The Hermitian rank-one projector is

\[
 h_\sigma h_\sigma^*
 =\frac12\bigl(P_\xi+i\sigma R_\xi\bigr),
 \qquad R_\xi v=\xi\times v.
 \tag{4.3}
\]

Because \(S\) is symmetric, it is orthogonal to the antisymmetric part
\(R_\xi\). Therefore

\[
 h_\sigma^*Sh_\sigma
 =\frac12\operatorname{tr}(P_\xi S)
 =-\frac12\xi^{\mathsf T}S\xi.
 \tag{4.4}
\]

Helicity removes only the antisymmetric projector. The symmetric transverse
projector survives and is independent of \(\sigma\).

Let \(B=\rho e^{i\phi}\) and form the real conjugate pair

\[
 \omega_{\sigma,B}
 =Bh_\sigma e^{i\kappa\xi\cdot x}
  +\overline B\,\overline h_\sigma e^{-i\kappa\xi\cdot x}
 =\sqrt2\rho
 \bigl(e_1\cos\theta-\sigma e_2\sin\theta\bigr),
 \tag{4.5}
\]

where \(\theta=\kappa\xi\cdot x+\phi\). Writing
\(S_{\alpha\beta}=e_\alpha^{\mathsf T}Se_\beta\), direct expansion gives

\[
 \boxed{
 \omega_{\sigma,B}^{\mathsf T}S\omega_{\sigma,B}
 =\rho^2\left[
 -S_{\xi\xi}
 +(S_{11}-S_{22})\cos2\theta
 -2\sigma S_{12}\sin2\theta
 \right].}
 \tag{4.6}
\]

The oscillatory spin-two component depends on helicity. The phase-averaged
diagonal component does not:

\[
 \left\langle
 \omega_{\sigma,B}^{\mathsf T}S\omega_{\sigma,B}
 \right\rangle_\theta
 =-\rho^2\xi^{\mathsf T}S\xi.
 \tag{4.7}
\]

This proves (1.3).

## 5. Exactly when angular averaging cancels

Let \(\{\xi_j\}\subset S^2\) carry nonnegative weights \(w_j\). The signed
phase-averaged helical sum is

\[
 -S:\sum_jw_j\xi_j\otimes\xi_j.
 \tag{5.1}
\]

It vanishes for every \(S\in\operatorname{Sym}_0(3)\) if and only if

\[
 \boxed{
 \sum_jw_j\xi_j\otimes\xi_j
 =\frac{\sum_jw_j}{3}I.}
 \tag{5.2}
\]

Indeed, the orthogonal complement of \(\operatorname{Sym}_0(3)\) inside the
symmetric matrices is precisely the scalar line. Condition (5.2) is exact
second-order isotropy, equivalently a weighted spherical 2-design at the
quadratic level.

### 5.1 Full sphere

Normalized surface measure satisfies

\[
 \left\langle\xi\otimes\xi\right\rangle_{S^2}=\frac13I,
 \tag{5.3}
\]

so the signed mean vanishes. For \(S_0\) in (1.4), with
\(z=\xi_3\),

\[
 K_{S_0}=\frac{3z^2-1}{2}.
 \tag{5.4}
\]

The normalized signed and positive-part means are

\[
 \frac12\int_{-1}^{1}\frac{3z^2-1}{2}\,dz=0,
 \tag{5.5}
\]

\[
 \int_{1/\sqrt{3}}^{1}\frac{3z^2-1}{2}\,dz
 =\frac1{3\sqrt{3}}=\frac{\sqrt{3}}{9}>0.
 \tag{5.6}
\]

Thus isotropy cancels before applying \(|\cdot|\) or \((\cdot)_+\), not
afterwards.

### 5.2 A great circle is not a sphere

If \(\xi\) is uniform on the great circle with normal \(n\), then

\[
 \left\langle\xi\otimes\xi\right\rangle_{\rm ring}
 =\frac12(I-n\otimes n),
 \qquad
 \left\langle K_S\right\rangle_{\rm ring}
 =\frac12n^{\mathsf T}Sn.
 \tag{5.7}
\]

This is generally nonzero. For \(S_0\) and \(n=e_3\), it equals \(-1/2\).

### 5.3 A finite same-shell witness

On one frequency sphere take

\[
 \xi_1=(0,0,1),\qquad
 \xi_2=\left(\frac35,0,\frac45\right).
 \tag{5.8}
\]

For equal amplitudes and equal helicity,

\[
 \xi_1^{\mathsf T}S_0\xi_1=-1,\qquad
 \xi_2^{\mathsf T}S_0\xi_2=-\frac{23}{50},
 \tag{5.9}
\]

so the global spatial mean is

\[
 \boxed{-\sum_{j=1}^{2}\xi_j^{\mathsf T}S_0\xi_j
 =\frac{73}{50}>0.}
 \tag{5.10}
\]

Two modes, one shell, and one helicity sign are still insufficient. Three
equal coordinate axes do satisfy (5.2), but their signed symbols
\((-1/2,-1/2,1)\) have positive-part sum \(1\).

## 6. The strongest single-mode witness

For the field in (1.4), with \(\theta=\kappa x_3\), direct differentiation
gives

\[
 \nabla\cdot\omega_\sigma=0,
 \qquad
 \nabla\times\omega_\sigma=\sigma\kappa\omega_\sigma.
 \tag{6.1}
\]

Hence

\[
 u_\sigma=(\sigma\kappa)^{-1}\omega_\sigma
 \tag{6.2}
\]

is divergence-free and has vorticity \(\omega_\sigma\). Its self-strain has
only entries mixing the transverse plane with \(e_3\), and therefore

\[
 \omega_\sigma^{\mathsf T}
 (\operatorname{sym}\nabla u_\sigma)
 \omega_\sigma=0.
 \tag{6.3}
\]

Equation (6.3) is compatible with (1.5): the positive tensor \(S_0\) is an
external harmonic strain, not the wave's own strain.

There is also a genuine periodic NSE witness for the statement that pure
helicity does not make the dynamics invalid. On \(\mathbb T^3\), put

\[
 u(t,x)=e^{-\nu t}(\sin x_3,\cos x_3,0).
 \tag{6.4}
\]

Then

\[
 \nabla\cdot u=0,\qquad
 \nabla\times u=u,\qquad
 (u\cdot\nabla)u=0,\qquad
 \Delta u=-u.
 \tag{6.5}
\]

It solves NSE with constant pressure. The contraction with \(S_0\) is
\(e^{-2\nu t}/2>0\) pointwise. This rules out an algebraic implication from
“Beltrami NSE mode” to “arbitrary external STF contraction equals zero.” It
does not identify \(S_0\) with the mode's self-generated pressure Hessian or
strain.

## 7. Exact compact source/core realization

The periodic witness is not finite-energy on \(\mathbb R^3\). This section
constructs a separate compact physical realization and retains every return
field.

### 7.1 Any STF tensor as an exterior strain

Let \(S\in\operatorname{Sym}_0(3)\). Choose a radial
\(\zeta_{\rm ext}\in C_c^\infty(B_5)\) equal to one on \(B_4\), and define

\[
 P_S(x)=Sx,
 \qquad
 G_S=\nabla\times\left[-\frac13\zeta_{\rm ext}(x)
 x\times P_S(x)\right].
 \tag{7.1}
\]

The vector identity

\[
 \nabla\times(x\times P_S)=-3P_S
 \tag{7.2}
\]

uses homogeneity of degree one and \(\nabla\cdot P_S=0\). Thus

\[
 G_S=Sx,\qquad
 \operatorname{sym}\nabla G_S=S
 \quad\text{on }B_4.
 \tag{7.3}
\]

Moreover,

\[
 G_S\in C_{c,\sigma}^\infty(B_5),
 \qquad
 \Gamma_S:=\nabla\times G_S,
 \qquad
 \operatorname{supp}\Gamma_S\subset B_5\setminus B_4.
 \tag{7.4}
\]

Because \(G_S\) is compact, divergence-free, and decays at infinity, the
Helmholtz reconstruction is exact:

\[
 G_S=\nabla\times(-\Delta)^{-1}\Gamma_S.
 \tag{7.5}
\]

Therefore the exterior vorticity source \(\Gamma_S\) produces strain exactly
equal to \(S\) throughout the open core. This is stronger than realizing only
the center Taylor coefficient.

### 7.2 Compact core carriers

For a constant-vorticity carrier, choose a unit vector \(e\), a radial
\(\zeta_{\rm core}\in C_c^\infty(B_2)\) equal to one on \(B_1\), and put

\[
 P_e(x)=\frac12e\times x,
 \qquad
 V_e=\nabla\times\left[-\frac13\zeta_{\rm core}(x)
 x\times P_e(x)\right].
 \tag{7.6}
\]

Then

\[
 V_e\in C_{c,\sigma}^\infty(B_2),
 \qquad
 \nabla\times V_e=e,
 \qquad
 \operatorname{sym}\nabla V_e=0
 \quad\text{on }B_1.
 \tag{7.7}
\]

If \(e\) is a positive eigendirection of \(S\), then every nonzero
\(0\le\chi\in C_c^\infty(B_1)\) gives

\[
 \int\chi\,S:\mathring Q(\nabla\times V_e)\,dx
 =\lambda_e\int\chi\,dx>0.
 \tag{7.8}
\]

For a locally helical carrier, let \(W_{\sigma,\kappa}\) be (1.4), let

\[
 U_{\sigma,\kappa}=(\sigma\kappa)^{-1}W_{\sigma,\kappa},
 \qquad
 A_{\sigma,\kappa}=\kappa^{-2}W_{\sigma,\kappa},
 \tag{7.9}
\]

and set

\[
 V_{\sigma,\kappa}
 =\nabla\times(\zeta_{\rm core}A_{\sigma,\kappa}).
 \tag{7.10}
\]

Since \(\nabla\times A_{\sigma,\kappa}=U_{\sigma,\kappa}\),

\[
 V_{\sigma,\kappa}=U_{\sigma,\kappa},
 \qquad
 \nabla\times V_{\sigma,\kappa}=W_{\sigma,\kappa}
 \quad\text{on }B_1.
 \tag{7.11}
\]

The return vorticity in \(B_2\setminus B_1\) is part of the field and is not
discarded.

### 7.3 Strict support separation and physical filtering

Scale the exterior generator at \(R=\Lambda r\) and the carrier at \(r\),
with \(\Lambda>2\). The exterior source vorticity lies in

\[
 B_{5R}\setminus B_{4R},
 \tag{7.12}
\]

whereas the complete carrier vorticity lies in \(B_{2r}\). The strain from
the selected exterior source is \(R^{-2}S\) throughout \(B_{4R}\), hence on
the complete carrier support.

Let \(\chi_r(x)=\chi(x/r)\) with
\(\operatorname{supp}\chi\Subset B_1\). For the helical carrier and
\(S=S_0\),

\[
 \int\chi_r
 (R^{-2}S_0):
 \mathring Q\!\left(r^{-2}W_{\sigma,\kappa}(x/r)\right)dx
 =R^{-2}r^{-1}\int\chi>0.
 \tag{7.13}
\]

A compactly supported even convolution filter can also be retained exactly.
Fix its radius \(\ell=\sigma_0r\), choose \(\Lambda\) large relative to
\(\sigma_0\), and choose one fixed radial annular selector \(\psi_R\) whose
plateau contains the \(\ell\)-expanded support of the exterior source
\(\Gamma_{S,R}\), while its inner hole contains the \(\ell\)-expanded support
of the entire carrier. Then

\[
 \psi_R\bigl(\varphi_\ell*
   (\Gamma_{S,R}+\nabla\times V_r)\bigr)
 =\varphi_\ell*\Gamma_{S,R}.
 \tag{7.14}
\]

The Biot--Savart strain operator commutes with convolution. An even unit-mass
filter fixes affine functions, so the selected exterior strain remains
exactly \(R^{-2}S\) on the buffered core. If the filter support also stays
inside the buffer from \(\operatorname{supp}\chi_r\) to \(\partial B_r\),
write

\[
 \Omega_{V,r}(x)
 =r^{-2}(\nabla\times V_{\sigma,\kappa})(x/r).
\]

Then on \(\operatorname{supp}\chi_r\),

\[
 \varphi_{\sigma_0r}*\Omega_{V,r}
 =\mu_{\sigma_0,\kappa}r^{-2}
 W_{\sigma,\kappa}(x/r).
 \tag{7.15}
\]

Here
\(\mu_{\sigma_0,\kappa}
=\widehat\varphi(\sigma_0\kappa e_3)\).
Choosing \(\sigma_0\) so that this scalar is nonzero preserves strict
positivity, multiplied by \(\mu_{\sigma_0,\kappa}^2\).

There is an unavoidable uncertainty-principle boundary. A nonzero compact
smooth carrier cannot also have compact Fourier support. The periodic mode is
an exact annular/single-shell witness; the compact construction is an exact
physical-space witness. A strict Littlewood--Paley block of the compact
packet requires a separate high-frequency pseudolocal error estimate. R0.70J
does not silently identify these two objects.

## 8. Critical source/core weights

This section connects the compact witness to the exact coordinates derived in
R0.70G--R0.70I.

Let \(F_{\Lambda}=\Lambda^{-1}G_S(\cdot/\Lambda)+V\), where \(V\) is either
compact core carrier above. For an amplitude \(a>0\), define the co-scaled
profile

\[
 u_{a,r}(x)=a r^{-1}F_{\Lambda}(x/r).
 \tag{8.1}
\]

Equivalently, its source and carrier pieces have the natural velocity
scalings \(aR^{-1}G_S(x/R)\) and \(ar^{-1}V(x/r)\). On the physical core, let
\(W^\varphi=W\) in the unfiltered convention and
\(W^\varphi=\mu_{\sigma_0,\kappa}W\) for the exact compact convolution filter
in (7.15). Then the selected source coefficient and selected core vorticity
are

\[
 P_r^{(0)}=aR^{-2}S,
 \qquad
 \Omega_r=ar^{-2}W^\varphi(x/r).
 \tag{8.2}
\]

Write

\[
 Q_0=\int\chi(z)
 W^\varphi(z)\otimes W^\varphi(z)\,dz.
 \tag{8.3}
\]

Then

\[
 M_r^{(0)}=a^2r^{-1}Q_0,
 \qquad
 m_r^{(0)}=rM_r^{(0)}=a^2Q_0,
 \tag{8.4}
\]

and the source coordinate is

\[
 c_r=r^2P_r^{(0)}=a\Lambda^{-2}S.
 \tag{8.5}
\]

The exact work covariance is

\[
 \boxed{
 r^3P_r^{(0)}:M_r^{(0)}
 =c_r:m_r^{(0)}
 =a^3\Lambda^{-2}S:Q_0>0.}
 \tag{8.6}
\]

### 8.1 Parabolic duality ledger

Choose \(0\leq\theta\in C_c^\infty((-1,0))\) with \(\theta\not\equiv0\), let
\(\theta_r(t)=\theta((t-t_0)/r^2)\), and multiply the full profile by
\(\theta_r\). Thus \(\int\theta^3>0\). This produces a norm comparator; it is
not asserted to solve NSE. The source is linear in \(\theta_r\), the core
moment is quadratic, and

\[
 \mathcal N_r^{(0)}=r^{-2}m_r^{(0)}.
 \tag{8.7}
\]

Direct change of variables yields

\[
 \int r^{-1}|c_r(t)|^2dt
 =a^2r\Lambda^{-4}|S|^2
 \int\theta^2,
 \tag{8.8}
\]

\[
 \int r|\mathcal N_r^{(0)}(t)|^2dt
 =a^4r^{-1}|Q_0|^2
 \int\theta^4,
 \tag{8.9}
\]

and

\[
 \boxed{
 \int c_r:\mathcal N_r^{(0)}dt
 =a^3\Lambda^{-2}(S:Q_0)
 \int\theta^3>0.}
 \tag{8.10}
\]

The product of the square roots in (8.8)--(8.9) has scale
\(a^3\Lambda^{-2}\), exactly the scale of (8.10). Thus the missing direct
Cauchy step is saturated, not improved, by the compact geometry.

### 8.2 Two amplitudes and two different claims

For the NSE-invariant spatial amplitude \(a=1\),

\[
 \|u_{1,r}\|_2^2\asymp r,
 \qquad
 \int_{t_0-r^2}^{t_0}\|\nabla u_{1,r}\|_2^2dt\asymp r.
 \tag{8.11}
\]

The source norm squared in (8.8) is \(O(r)\), the core dual norm squared in
(8.9) is \(O(r^{-1})\), and the pairing remains \(O(1)\).

For the Leray-normalized comparator amplitude

\[
 a=r^{-1/2},
 \tag{8.12}
\]

both quantities in (8.11) are \(O(1)\), while

\[
 \int r^{-1}|c_r|^2dt\asymp1,
 \qquad
 \int r|\mathcal N_r^{(0)}|^2dt\asymp r^{-3},
 \qquad
 \int c_r:\mathcal N_r^{(0)}dt\asymp r^{-3/2}.
 \tag{8.13}
\]

This realizes, with one compact smooth divergence-free source/core profile,
the abstract degree-zero norm comparator in R0.70I Section 9. It is a
function-space non-implication: the displayed energy, dissipation, and source
square norms alone do not bound the direct pairing uniformly. The arbitrary
time envelope prevents (8.13) from being reported as an NSE trajectory.

### 8.3 Initial-face NSE compatibility

Fix once and for all \(\Lambda\), both cutoff profiles, the compact convolution
filter \(\varphi\), and the annular selector \(\psi\) satisfying Section 7.3.
At unit scale define

\[
 \Omega_\varphi[u]=\varphi*(\nabla\times u),
 \qquad
 \mathcal S_{\psi,\varphi}[u]
 =\operatorname{sym}\nabla\nabla\times(-\Delta)^{-1}
   \bigl[\psi\,\Omega_\varphi[u]\bigr],
 \tag{8.14}
\]

\[
 \mathcal J_\Lambda[u]
 =\int\chi\,
 \mathcal S_{\psi,\varphi}[u]:
 \operatorname{dev}\bigl(
   \Omega_\varphi[u]\otimes\Omega_\varphi[u]\bigr)\,dx.
 \tag{8.15}
\]

The exact initial geometry gives
\(\mathcal J_\Lambda[F_\Lambda]>0\), and homogeneity gives

\[
 \mathcal J_\Lambda[\varepsilon F_\Lambda]
 =\varepsilon^3\mathcal J_\Lambda[F_\Lambda]>0.
 \tag{8.16}
\]

Because \(F_\Lambda\in C_c^\infty\), choose \(\varepsilon\) sufficiently
small for the standard small-\(L^3(\mathbb R^3)\) global mild-solution
theorem. Its smooth NSE solution \(U\) is continuous in a high Sobolev
topology; the fixed finite-scale functional (8.15) is continuous there.
Hence \(\mathcal J_\Lambda[U(\tau)]>0\) for
\(0\le\tau\le\tau_*(\varepsilon,\Lambda)\).

Now scale the solution, the core cutoff, the convolution scale, the source
annulus, and its selector together:

\[
 u_r(x,t)=r^{-1}U(x/r,t/r^2).
 \tag{8.17}
\]

The scale-covariant functional therefore has the same sign for
\(0\le t\le\tau_*(\varepsilon,\Lambda)r^2\).

This only proves compatibility near the initial face. The intervals shrink
to zero, the solutions are rescaled copies, and no concentration along one
solution history at a fixed positive terminal time is obtained.

## 9. Pressure-Hessian boundary

The source in Sections 2--8 is an exterior **strain** coefficient. The
same matrix \(S_0\) is also the Hessian of the harmonic quadratic

\[
 \Phi_0(x)=\frac14x_1^2+\frac14x_2^2-\frac12x_3^2,
 \qquad
 \Delta\Phi_0=0,\qquad
 \nabla^2\Phi_0=S_0.
 \tag{9.1}
\]

This scalar identity does not make \(S_0\) the pressure Hessian generated by
the same Beltrami core.

There is a separate center-coefficient realization. R0.69K constructed a
compact divergence-free exterior packet \(u_*\) with nonzero center pressure
Hessian

\[
 Q_*=
 \nabla^2(-\Delta)^{-1}
 \partial_i\partial_j(u_{*,i}u_{*,j})(0)
 \in\operatorname{Sym}_0(3).
 \tag{9.2}
\]

Rotations, dilations, and amplitudes transform it by

\[
 Q[aO u_*(O^{\mathsf T}\cdot/\lambda)]
 =a^2\lambda^{-2}OQ_*O^{\mathsf T}.
 \tag{9.3}
\]

The \(SO(3)\) orbit of any nonzero \(Q_*\in\operatorname{Sym}_0(3)\) spans
all of \(\operatorname{Sym}_0(3)\). Here is a direct proof. Choose an
eigenvector \(e\) whose eigenvalue \(q_e\) is nonzero and average \(Q_*\)
over rotations about \(e\). The result is

\[
 \frac32q_e\,\operatorname{dev}(e\otimes e)\ne0.
 \tag{9.4}
\]

Rotating this tensor shows that the orbit span contains
\(\operatorname{dev}(v\otimes v)\) for every \(v\in S^2\). These tensors span
the STF space: if
\(S=\sum_{j=1}^3\lambda_je_j\otimes e_j\) is a spectral decomposition with
\(\sum_j\lambda_j=0\), then

\[
 S=\sum_{j=1}^3\lambda_j
   \operatorname{dev}(e_j\otimes e_j).
 \tag{9.5}
\]

The orbit's Haar average is zero. If zero were a boundary point of its convex
hull, a nonzero separating functional would be nonnegative on the orbit and
have zero Haar average; it would then vanish on the orbit and hence on its
span, a contradiction. Therefore the positive cone of the orbit is the whole
STF space.

Any desired \(S\) is consequently a finite positive sum

\[
 S=\sum_{\ell=1}^m w_\ell O_\ell Q_*O_\ell^{\mathsf T},
 \qquad w_\ell>0.
 \tag{9.6}
\]

Choose finitely many widely separated radial dilations \(\lambda_\ell\) so
that the packet supports are disjoint and remain outside the observation
core, and set

\[
 a_\ell=\lambda_\ell\sqrt{w_\ell}.
 \tag{9.7}
\]

Equation (9.3) then makes the \(\ell\)-th center Hessian exactly
\(w_\ell O_\ell Q_*O_\ell^{\mathsf T}\). Disjoint supports remove all
pointwise quadratic cross terms, so the center pressure Hessians add exactly.
This realizes

\[
 \nabla^2p(0)=S
 \tag{9.8}
\]

from a compact divergence-free exterior velocity.

The claim stops at the center coefficient. R0.70J does not prove that a
velocity-generated pressure satisfies \(\nabla^2p(x)\equiv S\) throughout an
open core. An arbitrary scalar source can achieve that, but it need not be a
double divergence of \(u\otimes u\).

## 10. What truly vanishes and what does not

| Mechanism | Exact conclusion | Survives cutoff? | Survives positive part? |
|---|---|---:|---:|
| isotropic response \((|w|^2/3)I\) | \(S:(|w|^2I/3)=0\) pointwise | yes | yes |
| antisymmetric helical projector | \(S:A=0\) for \(A^{\mathsf T}=-A\) | algebraic | yes |
| one positive complex frequency | its \(2k\) output has zero global average | generally no | no |
| real conjugate pair | zero-frequency term \(2b^*Sb\) remains | yes in the witness | yes in the witness |
| fixed helical direction | phase mean is \(-\rho^2\xi^{\mathsf T}S\xi\) | yes in the witness | yes in the witness |
| full second-order isotropy | signed directional mean is zero | not for coherent general cutoff terms | no |
| Biot--Savart direction coherence | conditional angular depletion for the self-consistent field | theorem-dependent | theorem-dependent |

The first row is the only unconditional pointwise symmetric-tensor null
structure available from trace freedom alone.

## 11. Focused primary-literature conclusion

The bounded ten-source audit is archived in
`research/r070j_literature_audit.md`. Its main separation is:

- STF/spherical-harmonic theory places source and response in the same
  \(\ell=2\) sector;
- helical triad theory supplies conservation and polarization identities but
  not an arbitrary-source zero;
- the cited vorticity-direction criteria obtain conditional depletion under
  quantitative coherence of the vorticity that generates the strain;
- DNS evidence on nonlocal strain is contextual, not an a priori estimate.

No audited primary source supplies a Leray-level cancellation for an
arbitrary external harmonic STF source against the deviatoric high--high
tensor. This is a bounded search result, not a universal literature
nonexistence theorem.

## 12. Closed claims, open claims, and route decision

### Closed in R0.70J

- The exact STF/deviatoric identity (1.2).
- The real pure-helicity tensor symbol (4.6) and phase-average kernel (4.7).
- Independence of the diagonal symbol from helicity and its evenness in
  frequency direction.
- The necessary and sufficient second-order isotropy condition (5.2) for the
  signed phase-averaged sum to vanish for every external
  \(S\in\operatorname{Sym}_0(3)\).
- Failure of full isotropy after a positive part, including the exact value
  \(\sqrt{3}/9\) for \(S_0\).
- A pointwise-positive Beltrami core that survives every nonnegative physical
  cutoff.
- Exact compact smooth, support-separated realization of an arbitrary
  exterior STF strain and a positive core vorticity tensor, with all return
  fields retained.
- Exact saturation of the degree-zero critical source/core scale ledger.
- Compact realization of the previously abstract R0.70I norm comparator.
- Realization of any prescribed STF center pressure Hessian by one
  instantaneous smooth compact divergence-free exterior velocity; neither
  open-core constancy nor persistence along an NSE trajectory is claimed.

### Still open

- A strict annular Littlewood--Paley realization of the compact packet with a
  fully quantified pseudolocal error.
- A source-aware cancellation imposed by one self-consistent NSE history.
- Control of the anisotropy defect from the Leray energy inequality.
- A cancellation that survives scale-by-scale positive parts.
- The moving-low \(B^{3/2}_{2,1}\)-type accumulation left by R0.70I.
- The degree-one compatible STF moment.
- A common fixed positive terminal time and one-solution cascade.

### Route decision

The universal algebraic-null branch based only on trace freedom,
incompressibility, fixed helicity, phase/angular averaging, and physical
cutoff is closed. More Fourier sampling, more helicity labels, or a larger
angular quadrature cannot change the exact counterexample (1.5). The next
useful object is the normalized anisotropy tensor

\[
 \mathcal A_k(t)
 =\operatorname{dev}\int\chi_k
 W_k(t,x)\otimes W_k(t,x)\,dx.
 \tag{12.1}
\]

R0.70K should derive its exact filtered evolution, including transport,
viscous, cutoff, commutator, and strain-production terms, and then test a
source-aware signed correlation across adjacent scales. A positive result
would require an energy-controlled anisotropy defect or compensated
source/core sum. A negative result should construct a compact evolution or
finite exact model retaining the same-sign STF correlation. Neither outcome
may be reported as a Millennium solution without the fixed-positive-time
NSE bridge.

## 13. Reproduction and claim boundary

The exact producer is
`research/r070j_deviatoric_helical_audit.py`. It verifies with exact SymPy
arithmetic:

1. the STF/deviatoric identity;
2. the two helical eigenvectors, projectors, and spin-two terms;
3. the full real-mode formula for both helicities;
4. the pointwise-positive Beltrami contraction and zero self-stretching;
5. the signed sphere, positive-part sphere, great-circle, finite same-shell,
   and three-axis ledgers;
6. the harmonic quadratic and the core polynomial homotopy identities before
   cutoff differentiation;
7. the exact periodic NSE Beltrami mode;
8. the critical source/core monomial ledger.

The producer does not computer-prove smooth support buffers, strict annular
LP localization of a compact packet, small-data theory, persistence of
source/core geometry, the pressure-orbit convexity argument, literature
completeness, or a fixed-positive-time cascade. Those are analytic arguments
or explicit boundaries in this report.

The journal-style figure package is archived under
`figures/r070j-deviatoric-helical/fig-r070j-deviatoric-helical/`. Every panel
plots closed formulas or exact construction geometry. It is not a DNS run,
not a sampled singular trajectory, and not numerical evidence for blow-up or
regularity.

**DGX:** not justified for this gate. The decisive statements are exact
finite algebra, harmonic localization, and scale covariance. Floating-point
throughput cannot strengthen them.

**Publication boundary:** R0.70J remains local and unpublished until the
independent audit, full regression suite, and explicit user approval to push
the GitHub batch are all present.
