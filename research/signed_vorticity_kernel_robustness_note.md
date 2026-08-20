# R0.69G — The signed vorticity kernel and the magnitude-coupling barrier

## 1. Result

R0.69F shows that an unsigned scalar resolvent cannot improve the classical
endpoint scale.  The next natural question is whether the sign and direction
geometry discarded by that majorant can supply a genuinely stronger estimate.

There is an exact signed representation.  Let

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3,
 \qquad
 \omega=\nabla\times u,
 \qquad
 \xi=\frac{\omega}{|\omega|}
\]

on the set where \(|\omega|>0\).  Write

\[
 S=\frac12\bigl(\nabla u+(\nabla u)^T\bigr),
 \qquad
 \alpha=\xi\cdot S\xi.
\]

If \(G\) is the mean-zero periodic Green function satisfying

\[
 -\Delta G=\delta_0-(2\pi)^{-3},
\]

then

\[
 \boxed{
 \alpha(x)
 =\xi_i(x)\xi_\ell(x)\varepsilon_{ijk}
 \operatorname{p.v.}\!\int_{\mathbb T^3}
 \partial_{\ell j}G(z)\,\omega_k(x+z)\,dz.}
 \tag{1.1}
\]

For a cutoff \(\chi\) supported inside the injectivity radius and equal to
one near the origin, (1.1) becomes

\[
 \boxed{
 \alpha(x)
 =\frac{3}{4\pi}\operatorname{p.v.}\!\int
 \chi(z)
 D\!\left(\widehat z,\xi(x+z),\xi(x)\right)
 \frac{|\omega(x+z)|}{|z|^3}\,dz
 +\mathcal R_\chi\omega(x),}
 \tag{1.2}
\]

where

\[
 D(e_1,e_2,e_3)
 =(e_1\cdot e_3)\bigl(e_1\cdot(e_2\times e_3)\bigr)
 \tag{1.3}
\]

and \(\mathcal R_\chi\) has a smooth periodic kernel.  In particular,

\[
 |\mathcal R_\chi\omega(x)|
 \le C_\chi\|\omega\|_{L^1(\mathbb T^3)}.
 \tag{1.4}
\]

Formula (1.2) is the periodic local form of Constantin's geometric
vortex-stretching representation.  It is not a new formula.

The new route decision comes from a simple robustness theorem.  Fix an
annulus \(A\) not meeting the origin and freeze \(x,t\).  Put

\[
 K_{x,t}(z)
 =\frac{D(\widehat z,\xi(x+z,t),\xi(x,t))}{|z|^3}.
 \tag{1.5}
\]

Then

\[
 \boxed{
 \sup_{\substack{g\ge0\\ \int_Ag=1}}
 \left|\int_AK_{x,t}(z)g(z)\,dz\right|
 =\|K_{x,t}\|_{L^\infty(A)}.}
 \tag{1.6}
\]

Thus sign changes of the angular kernel do not yield a uniform gain when the
nonnegative magnitude is allowed to choose where to concentrate.  A useful
signed criterion must control the actual coupling

\[
 (\xi(x+z,t),|\omega(x+z,t)|),
 \]

not the direction field alone.  This rules out the proposed **direction-only
annular averaging** route.  It does not rule out magnitude-weighted geometric
criteria, filtered commutators, pressure compensation, or constraints imposed
by \(\nabla\cdot\omega=0\).

## 2. Exact periodic representation

Use the Fourier normalization

\[
 G(z)=\frac1{(2\pi)^3}
 \sum_{k\in\mathbb Z^3\setminus\{0\}}
 \frac{e^{ik\cdot z}}{|k|^2}.
 \tag{2.1}
\]

Since \(u=\nabla\times(G*\omega)\),

\[
 u_i=\varepsilon_{ijk}\partial_jG*\omega_k,
 \qquad
 \partial_\ell u_i
 =\varepsilon_{ijk}\partial_{\ell j}G*\omega_k.
 \tag{2.2}
\]

Contracting the symmetric part with \(\xi_i\xi_\ell\) makes its two halves
equal and gives (1.1).  On a ball smaller than the injectivity radius,

\[
 G(z)=\frac1{4\pi|z|}+H(z),
 \tag{2.3}
\]

where \(H\) is smooth.  The Hessian of the singular part is

\[
 \partial_{\ell j}\frac1{4\pi|z|}
 =\frac{3z_\ell z_j-|z|^2\delta_{\ell j}}
 {4\pi|z|^5}.
 \tag{2.4}
\]

The trace term vanishes after contraction:

\[
 \xi_i\xi_j\varepsilon_{ijk}=0.
 \tag{2.5}
\]

The remaining numerator is

\[
 \xi_i\xi_\ell\varepsilon_{ijk}
 z_\ell z_j\omega_k(x+z)
 =|\omega(x+z)|
 (\xi(x)\cdot z)
 \bigl(z\cdot(\xi(x+z)\times\xi(x))\bigr),
 \tag{2.6}
\]

which is exactly (1.3).  The cutoff complement and the Hessian of \(H\)
form the smooth remainder in (1.2).

## 3. What ordinary direction coherence already gives

For unit vectors,

\[
 |D(e_1,e_2,e_3)|
 \le |e_2\times e_3|
 =|\sin\angle(e_2,e_3)|.
 \tag{3.1}
\]

This is the classical depletion mechanism.  Lipschitz coherence of the
vorticity direction in the intense-vorticity region was used by Constantin
and Fefferman to preclude blow-up.  The spatial exponent was later reduced to
one-half Hölder coherence, and the criterion was localized to arbitrarily
small parabolic cylinders.  Consequently, replacing the signed kernel by
\(|D|\) and imposing a pointwise modulus of continuity would only re-enter
known theory.

There is also recent activity very close to the route considered here.  Two
2026 arXiv preprints study, respectively, a logarithmically weighted BMO
commutator formulation and a filtered finite-scale balance with annular
Carleson conditions.  These are preprints, not inputs treated as established
theorems in this note.  Their proximity means that a future claim based on
commutators or annular packing must be compared with them line by line.

## 4. Proof of the magnitude-coupling barrier

Let \(K\in L^\infty(A)\).  For every nonnegative \(g\) of unit mass,

\[
 \left|\int_AKg\right|
 \le\int_A|K|g
 \le\|K\|_\infty.
 \tag{4.1}
\]

Conversely, let \(M=\|K\|_\infty\).  For every \(\varepsilon>0\), either

\[
 E_+=\{K>M-\varepsilon\}
 \quad\hbox{or}\quad
 E_-=\{K<-M+\varepsilon\}
 \tag{4.2}
\]

has positive measure.  Choosing the normalized indicator of that set gives

\[
 \left|\int_AKg\right|>M-\varepsilon.
 \tag{4.3}
\]

Letting \(\varepsilon\downarrow0\) proves (1.6).

The theorem is deliberately narrow.  For a vorticity field, magnitude and
direction must also satisfy

\[
 \nabla\cdot(|\omega|\xi)=0.
 \tag{4.4}
\]

Equation (1.6) does not assert that every selector \(g\) is realizable by a
smooth divergence-free vorticity field, much less by a Navier--Stokes
solution.  It says that a proof which uses only a direction-dependent kernel
and treats the magnitude as an arbitrary positive weight cannot obtain a
uniform cancellation factor from sign oscillation.

## 5. A transparent two-lobe model

Fix

\[
 \xi(x)=e_3,
 \qquad
 \xi(x+z)=(\sin\varphi,0,\cos\varphi).
 \tag{5.1}
\]

On the unit sphere,

\[
 D(\widehat z,\xi(x+z),\xi(x))
 =-\sin\varphi\,\widehat z_2\widehat z_3.
 \tag{5.2}
\]

The uniform angular average vanishes, but the kernel has four sign lobes and

\[
 \|D\|_{L^\infty(\mathbb S^2)}
 =\frac{|\sin\varphi|}{2},
 \qquad
 \frac1{4\pi}\int_{\mathbb S^2}|D|\,d\sigma
 =\frac{2|\sin\varphi|}{3\pi}.
 \tag{5.3}
\]

For the nonnegative magnitude bias

\[
 g_\eta=1+\eta\,\operatorname{sgn}D,
 \qquad 0\le\eta<1,
 \tag{5.4}
\]

one obtains

\[
 \frac{\int_{\mathbb S^2}Dg_\eta\,d\sigma}
 {\int_{\mathbb S^2}g_\eta\,d\sigma}
 =\eta\frac{2|\sin\varphi|}{3\pi}.
 \tag{5.5}
\]

An arbitrarily modest magnitude bias therefore turns an exactly cancelling
direction pattern into positive stretching.  The figure archived with this
note visualizes (5.2)--(5.5).

## 6. Certified checks

The audit

`research/signed_vorticity_kernel_robustness_audit.py`

checks:

1. the Levi--Civita contraction in (2.5)--(2.6) symbolically;
2. the periodic Green-Hessian strain multiplier against the direct Fourier
   gradient on every mode of an explicit non-coplanar butterfly;
3. the nonzero total vortex stretching of that real divergence-free field;
4. the uniform and magnitude-biased spherical averages in (5.3)--(5.5);
5. the finite-selector version of the duality identity (1.6).

The Fourier calculation validates the identity on a finite trigonometric
field.  It is not a discretization proof of the continuum singular integral.
The continuum derivation is the calculation in Sections 2 and 4.

## 7. Decision and next step

R0.69G has a negative but useful conclusion:

\[
 \boxed{
 \text{direction-only signed annular averaging is not robust to vorticity}
 \text{ magnitude concentration}.}
 \tag{7.1}
\]

I am stopping that narrow branch.  The next calculation will retain a
quantity that couples magnitude to geometry automatically.  The first target
is the pressure-Hessian term in the strain equation,

\[
 (\partial_t+u\cdot\nabla-\Delta)S
 +S^2+\Omega^2+\nabla^2p=0,
 \tag{7.2}
\]

and its contraction with the principal stretching direction.  The immediate
question is whether the nonlocal pressure Hessian supplies a signed
compensation that is not equivalent to a known vorticity-direction criterion.

R0.69G does not prove regularity, construct a singular solution, or resolve
the three-dimensional Navier--Stokes Millennium problem.

## 8. Primary references and status

- P. Constantin and C. Fefferman, *Direction of Vorticity and the Problem of
  Global Regularity for the Navier--Stokes Equations*, Indiana Univ. Math. J.
  42 (1993), 775--789.  Published result.
- H. Beirão da Veiga and L. C. Berselli, *On the regularizing effect of the
  vorticity direction in incompressible viscous flows*, Differential and
  Integral Equations 15 (2002), 345--356.  Published result.
- Z. Grujić, *Localization and Geometric Depletion of Vortex-Stretching in
  the 3D NSE*, Comm. Math. Phys. 290 (2009), 861--870,
  doi:10.1007/s00220-008-0726-8.  Published result.
- R. Yu, *Filtered Vortex Stretching and Subgrid Defects for the
  Three-Dimensional Navier--Stokes Equations*, arXiv:2606.27560 (2026).
  Preprint; not independently validated here.
- Z. Grujić, *Logarithmic Depletion of Vortex Stretching and Singularity
  Evasion in the 3D Navier--Stokes Equations*, arXiv:2607.08866 (2026).
  Preprint; not independently validated here.
