# R0.70E — Yu object repair and a single-shell parity--transversality theorem

**Status:** internal canonical research report; not a public theorem chapter
**Date:** 2026-08-24
**Primary source:** Runlong Yu, *Filtered Vortex Stretching and Subgrid Defects for the Three-Dimensional Navier--Stokes Equations*, arXiv:2606.27560v1
**Purpose:** replace an ill-posed “exact Yu signed shell” target by two precisely separated objects, then close the parity--transversality gate for both the paper-defined signed remainder work and one project-defined contraction of Yu's moving-shell strain field

The labels are **[F]** for a primary-source fact, **[P]** for a proof completed
here, **[O]** for the resulting rigorous obstruction, and **[U]** for an
unresolved statement.  Every label is restricted to the displayed object and
quantifiers.

## 1. Result in one page

R0.70E reaches a real PDE-specific result, but it begins with a correction.

1. **[F] Source correction.**  Yu v1 defines the signed remainder work
   \(\mathcal V_\chi^{\mathrm{rem}}\) in (6.9), its positive part in
   (6.13), and the moving-shell strain tensors \(\mathbb S_{k,m}\) in
   Section 8.1.  It does **not** define a scalar
   \(F_{j,k}^{\mathrm{Yu}}\), a smooth Yu shell window \(\eta_j\), or a
   signed equality behind Proposition 8.6.  The latter is an
   absolute-value/reservoir upper bound.

2. **[P] Exact-paper object.**  For a Yu-admissible radial mollifier, a
   project-chosen inversion-even cutoff, and one dyadic cylinder, there are
   compactly supported smooth divergence-free initial data generating global
   small-data smooth Navier--Stokes solutions for which

   \[
   \boxed{
   \mathcal V_\chi^{\mathrm{rem}}=0,
   \qquad
   \mathcal A_\chi^{\mathrm{rem}}>0,
   \qquad
   \mathcal V_\chi^{+,\mathrm{rem}}
     =\tfrac12\mathcal A_\chi^{\mathrm{rem}}>0.}
   \tag{1.1}
   \]

   Here \(\mathcal A_\chi^{\mathrm{rem}}\) is the same-kernel,
   same-filter, same-cutoff absolute companion defined below.  Thus the exact
   signed work in Yu's balance cannot replace its positive remainder term by
   a deterministic reverse estimate, even inside the global smooth
   small-data class.

3. **[P] Yu-kernel project object.**  Define, rather than attribute to Yu,

   \[
   \mathcal W_{k,m}^{\mathrm{mov}}[u]
   :=r_k\int_{I_k}\!\int\chi_k
   (\mathbb S_{k,m}\Omega_k)\cdot\Omega_k\,dx\,dt .
   \tag{1.2}
   \]

   For one sufficiently separated pair \(m=k-j\ge1\), the same construction
   gives a global smooth small-data solution with

   \[
   \boxed{
   \mathcal W_{k,m}^{\mathrm{mov}}=0,
   \qquad
   \mathcal P_{k,m}^{\mathrm{mov}}>0.}
   \tag{1.3}
   \]

   This is a theorem about the project-defined signed contraction (1.2), not
   a theorem about Yu's \(\mu_k^{\mathrm{far,ann}}\).

4. **[P] All four cubic terms are retained.**  For the reflection parameter
   \(\lambda\), the heat-layer signed functional has the exact form

   \[
   H(\lambda)
   =c_0+c_1\lambda-c_1\lambda^2-c_0\lambda^3,
   \qquad H(1)=0,
   \tag{1.4}
   \]

   and the explicit construction makes \(H'(1)\ne0\).  No cross-pair is
   silently deleted.

5. **[O] Route consequence.**  Signed cancellation is now ruled out as a
   stand-alone substitute for Yu's positive remainder or annular magnitude
   budgets.  The next useful positive route must control a genuinely
   nonnegative quantity or impose a quantitative symmetry-breaking/affine-jet
   condition.  R0.70E does not prove regularity, control the commutator or
   localization budgets, or approach a singular solution.

The proof below is an existence proof.  The symbolic certificate checks the
finite algebra and the shell multiplier's leading moment.  The compact
localization, heat-tail limit, Kato solution map, and implicit-function step
are analytic arguments, not numerical evidence.

## 2. What Yu v1 actually defines

Set \(z_0=(x_0,t_0)\),

\[
B_r=B_r(x_0),\qquad I_r=(t_0-r^2,t_0),\qquad Q_r=B_r\times I_r.
\tag{2.1}
\]

Yu's (2.2) assumes only

\[
\varphi\in C_c^\infty(B_1),\qquad
\varphi\ge0,\qquad \int\varphi=1.
\tag{2.2}
\]

It does not require \(\varphi\) to be even or radial.  The radial object is
the separate near-field cutoff \(\vartheta\) in (2.7).  R0.70E selects a
radial \(\varphi\) from the admissible class; this is an additional project
choice, not a hypothesis quoted from Yu.

For \(\ell_k=\sigma r_k\), let

\[
U_k=\varphi_{\ell_k}*u,qquad
\Omega_k=\nabla\times U_k,qquad
\mathbb S_k=\tfrac12(\nabla U_k+\nabla U_k^T).
\tag{2.3}
\]

Yu's exact signed remainder work, equation (6.9), is

\[
\mathcal V_\chi^{\mathrm{rem}}[u]
=r\int_{s_0}^{s_1}\!\int
 \chi\,(\mathbb S_\ell^{\mathrm{rem}}\Omega_\ell)
 \cdot\Omega_\ell\,dx\,dt,
\tag{2.4}
\]

and its positive companion, equation (6.13), is

\[
\mathcal V_\chi^{+,\mathrm{rem}}[u]
=r\int_{s_0}^{s_1}\!\int
 \chi\,\bigl((\mathbb S_\ell^{\mathrm{rem}}\Omega_\ell)
 \cdot\Omega_\ell\bigr)_+\,dx\,dt.
\tag{2.5}
\]

Define the project notation

\[
\mathcal A_\chi^{\mathrm{rem}}[u]
:=r\int_{s_0}^{s_1}\!\int
 \chi\,\left|(\mathbb S_\ell^{\mathrm{rem}}\Omega_\ell)
 \cdot\Omega_\ell\right|\,dx\,dt.
\tag{2.6}
\]

Because all three quantities use exactly the same integrand and
\(\chi\ge0\),

\[
\mathcal V_\chi^{+,\mathrm{rem}}
=\frac{\mathcal A_\chi^{\mathrm{rem}}
       +\mathcal V_\chi^{\mathrm{rem}}}{2}.
\tag{2.7R}
\]

At dyadic scale \(r_k=2^{-k}\), Yu's Section 8.1 instead defines the tensor

\[
\mathbb S_{k,m}(x,t)
=\int_{A_{k,m}(x)}K(x-y)\Omega_k(y,t)\,dy,
\tag{2.8}
\]

where

\[
A_{k,m}(x)
=\{y:\Gamma2^m r_k<|x-y|\le2\Gamma2^m r_k\},
\qquad \Gamma>1.
\tag{2.9}
\]

The phrase defining \(\mu_k^{\mathrm{far,ann}}\) says only “the contribution
of the shells” to a positive far-field quantity.  It does not specify whether
one sums shells before or after taking a positive part.  Equation (8.4) then
uses an absolute kernel estimate and Cauchy--Schwarz; Section 8.3 explicitly
calls the moving-shell decomposition an “absolute-value device.”  Therefore
(1.2) is legitimate project notation built from (2.8), but it is not renamed
as a Yu-defined signed scalar.

There is a second source boundary.  In Yu's (2.10),
\(1-\vartheta(z/(\rho r_k))\) vanishes for
\(|z|\le\rho r_k/2\), varies on the transition annulus, and equals one for
\(|z|\ge\rho r_k\).  By contrast, (2.9) begins at
\(\Gamma r_k\) with \(\Gamma>1\).  Yu v1 does not display an identity bridging
the intermediate region.  R0.70E never identifies (2.4) with a sum of (1.2).

## 3. Reflection covariance

Translate coordinates so that \(x_0=0\), and define the Navier--Stokes
inversion action

\[
(\mathcal Ru)(x,t):=-u(-x,t).
\tag{3.1}
\]

The minus sign is the polar-vector transformation under the orientation-
reversing map \(x\mapsto-x\).  Its curl is an axial vector:

\[
\Omega[\mathcal Ru](x,t)=\Omega[u](-x,t),
\qquad
\mathbb S[\mathcal Ru](x,t)=\mathbb S[u](-x,t).
\tag{3.2}
\]

The moving shell is exactly covariant because

\[
-A_{k,m}(x)=A_{k,m}(-x),
\tag{3.3}
\]

or, in relative coordinates, because (2.8) is convolution by the integrable
kernel

\[
K(z)\mathbf1_{\{\Gamma2^m r_k<|z|\le2\Gamma2^m r_k\}}.
\tag{3.4}
\]

The strain kernel is even: \(K(-z)=K(z)\).  If the selected mollifier is even,
filtering commutes with \(\mathcal R\).  If also

\[
\chi_k(-x,t)=\chi_k(x,t),
\tag{3.5}
\]

then both (2.4) and (1.2), denoted generically by \(\mathcal F\), satisfy

\[
\mathcal F[\mathcal Ru]=\mathcal F[u].
\tag{3.6}
\]

They are cubic:

\[
\mathcal F[a u]=a^3\mathcal F[u].
\tag{3.7}
\]

The heat kernel is radial, so

\[
e^{\nu t\Delta}\mathcal R
=\mathcal R e^{\nu t\Delta}.
\tag{3.8}
\]

Consequently, for \(q_\lambda=v-\lambda\mathcal Rv\),

\[
H(\lambda):=\mathcal F[e^{\nu(t-t_-)\Delta}q_\lambda]
=-\lambda^3H(1/\lambda).
\tag{3.9}
\]

Every such cubic is anti-palindromic:

\[
H(\lambda)=a+b\lambda-b\lambda^2-a\lambda^3.
\tag{3.10}
\]

Parity gives \(H(1)=0\), but it does not give a simple root.  The missing
gate is a nonzero even--even--odd mixed polarization.  Sections 4--7 construct
it explicitly.

For a non-even admissible \(\varphi\) or \(\chi\), the correct identity pairs
the reflected filter/cutoff with the original one.  Thus R0.70E proves an
existence theorem in an admissible even subclass, not a theorem for every
Yu-admissible profile.

## 4. An explicit even--odd Fourier pair

In dimensionless variables define

\[
E(x,y,z)=(\cos y,\cos z,\cos x),
\qquad
O(x,y,z)=(\sin y,\sin z,\sin x).
\tag{4.1}
\]

Both are divergence free and satisfy

\[
\Delta E=-E,qquad \Delta O=-O,qquad
\mathcal RE=-E,qquad \mathcal RO=O.
\tag{4.2}
\]

They have vector potentials

\[
A_E=(\sin z,\sin x,\sin y),
\qquad
A_O=\nabla\times O=(-\cos z,-\cos x,-\cos y),
\tag{4.3}
\]

with \(\nabla\times A_E=E\) and
\(\nabla\times A_O=O\).

Let

\[
G_s=(\nabla\times(E+sO))\cdot
S[E+sO](\nabla\times(E+sO)).
\tag{4.4}
\]

Exact expansion gives

\[
G_s=C_0+sC_1+s^2C_2+s^3C_3,
\tag{4.5}
\]

where

\[
\begin{aligned}
C_0={}&-3\sin x\sin y\sin z,\\
C_1={}&3(\sin x\sin y\cos z
          +\sin x\sin z\cos y
          +\sin y\sin z\cos x),\\
C_2={}&-3(\sin x\cos y\cos z
          +\sin y\cos x\cos z
          +\sin z\cos x\cos y),\\
C_3={}&3\cos x\cos y\cos z.
\end{aligned}
\tag{4.6}
\]

The parities of \((C_0,C_1,C_2,C_3)\) under full inversion are respectively
odd, even, odd, even.  At

\[
p_*=(\pi/4,\pi/4,\pi/4)
\tag{4.7}
\]

their exact values are

\[
\left(-\frac{3\sqrt2}{4},
       \frac{9\sqrt2}{4},
      -\frac{9\sqrt2}{4},
       \frac{3\sqrt2}{4}\right).
\tag{4.8}
\]

For equal small phases \(x=y=z=\delta\), the two coefficients needed below
are

\[
C_0=-3\sin^3\delta\ne0,
\qquad
C_1=\frac94(\cos\delta-\cos3\delta)>0
\quad(0<\delta<\pi/2).
\tag{4.9}
\]

Thus a pair of small equal cutoff lobes around \(p\) and \(-p\) cancels
\(C_0\) exactly, retains positive absolute \(C_0\)-activity, and adds the
two positive \(C_1\) contributions.

## 5. The hard-annulus multiplier is nonzero

Let

\[
K_{a,b}(z)=K(z)\mathbf1_{\{a<|z|\le b\}},
\qquad 0<a<b<\infty.
\tag{5.1}
\]

This is an \(L^1\) kernel.  Its angular factor is the pure trace-free
degree-two spherical-harmonic tensor carried by the strain kernel.  Radial
truncation preserves that representation, so rotational covariance and
equivariant uniqueness show that, on every divergence-free plane wave of
wave number \(q\), convolution by \(K_{a,b}\) is a scalar multiple
\(\alpha_{a,b}(q)\) of the full strain.  The scalar is the same for every
rotated member of (4.1).

It remains to show that this scalar is not zero.  Take a wave vector along
\(e_1\), vorticity along \(e_2\), and inspect the \((1,3)\) strain component.
Yu's kernel (3.2) gives

\[
K_{132}(z)=\frac{3}{8\pi|z|^5}(z_1^2-z_3^2).
\tag{5.2}
\]

The constant and odd terms in \(e^{-iqz_1}\) integrate to zero.  Since

\[
\int_{S^2}(n_1^4-n_1^2n_3^2)\,dS
=4\pi\left(\frac15-\frac1{15}\right)
=\frac{8\pi}{15},
\tag{5.3}
\]

Taylor expansion at \(q=0\) yields

\[
\widehat K_{132}^{\,a,b}(qe_1)
=-\frac{q^2(b^2-a^2)}{20}+O(q^4b^4).
\tag{5.4}
\]

With Yu's kernel convention and \(\Omega=\nabla\times U\), the full
\(S_{13}/\Omega_2\) multiplier is \(-1/2\).  Therefore

\[
\boxed{
\alpha_{a,b}(q)
=\frac{q^2(b^2-a^2)}{10}+O(q^4b^4).}
\tag{5.5}
\]

Equivalently, with \(j_\ell\) denoting the spherical Bessel functions, the
exact scalar multiplier is

\[
\alpha_{a,b}(q)
=3\int_{qa}^{qb}\frac{j_2(s)}s\,ds
=3\left(\frac{j_1(qa)}{qa}-\frac{j_1(qb)}{qb}\right).
\tag{5.5a}
\]

For the Yu shell belonging to \(j=k-m\),

\[
a=\Gamma r_j,qquad b=2\Gamma r_j.
\tag{5.6}
\]

Choose \(q=\kappa/r_j\) with \(0<\kappa\ll_\Gamma1\).  Then

\[
\alpha_{a,b}(q)
=\frac{3\Gamma^2}{10}\kappa^2+O_\Gamma(\kappa^4)\ne0.
\tag{5.7}
\]

This is the key replacement for the idealized point-vorticity picture.  It
includes the complete spherical shell and every angular contribution; no
selected pair is discarded.

For an admissible radial mollifier,
\(\varphi_{\ell_k}*E(q\cdot)\) and
\(\varphi_{\ell_k}*O(q\cdot)\) acquire the same real multiplier

\[
c_\varphi(q\ell_k)=1+O((q\ell_k)^2).
\tag{5.8}
\]

Accordingly, the filtered shell density for the scaled periodic pair is

\[
q^3c_\varphi(q\ell_k)^3\alpha_{a,b}(q)
\bigl(C_0+sC_1+s^2C_2+s^3C_3\bigr)(qx),
\tag{5.8a}
\]

and the remainder version replaces \(\alpha_{a,b}\) by
\(1-\alpha_{\mathrm{near}}\).  These common factors are nonzero in the
parameter range selected below.

With \(m=k-j\),

\[
q r_k=\kappa2^{-m},qquad
q\ell_k=\sigma\kappa2^{-m}.
\tag{5.9}
\]

Thus the selected strictly separated shell preserves the nonzero multiplier
and makes filter distortion and heat decay at the core scale small.

The exact remainder operator has the same plane-wave covariance.  Its
near-field multiplier obeys

\[
\alpha_{\mathrm{near}}(q\rho r_k)
=O((q\rho r_k)^2),
\tag{5.10}
\]

so

\[
\mathbb S_\ell^{\mathrm{rem}}
=(1-\alpha_{\mathrm{near}})\mathbb S_\ell
\tag{5.11}
\]

on this single-frequency family, with a nonzero factor for sufficiently large
separation.  Equations (5.7) and (5.11) therefore multiply every coefficient
in (4.6) by a common nonzero scalar.

## 6. Compact divergence-free localization and the return field

The periodic pair is only a local model.  It is now localized at the velocity
level without altering its divergence.

Let \(\zeta_L\) be a smooth radial even cutoff, equal to one on
\(B_{Lr_j}\) and zero outside \(B_{2Lr_j}\).  Define the scaled potentials

\[
A_{E,q}(x)=q^{-1}A_E(qx),
\qquad
A_{O,q}(x)=q^{-1}A_O(qx),
\tag{6.1}
\]

and the compact fields

\[
E_L=\nabla\times(\zeta_L A_{E,q}),
\qquad
O_L=\nabla\times(\zeta_L A_{O,q}).
\tag{6.2}
\]

Then

\[
E_L,O_L\in C_{c,\sigma}^\infty(\mathbb R^3),
\qquad
\mathcal R E_L=-E_L,
\qquad
\mathcal R O_L=O_L.
\tag{6.3}
\]

On the plateau they equal \(E(qx)\) and \(O(qx)\).  For the hard moving-shell
functional, all transition and return vorticity created by
\(\nabla\zeta_L\) lies outside the finite
core-plus-shell-plus-filter dependency region once \(L>2\Gamma+2\).  Thus
the transition is exactly absent from that functional at \(t=0\).

The remainder functional requires a different argument: its Biot--Savart
interpretation extends to infinity, so its return field is **not** declared
geometrically invisible.  Instead use Yu's defining identity

\[
\mathbb S_\ell^{\mathrm{rem}}
=\mathbb S(\varphi_\ell*u)-\mathbb S_\ell^{\mathrm{near}}.
\tag{6.3a}
\]

The first term is the local symmetric gradient of the filtered velocity and
the second depends only on the finite near-field neighborhood.  Plateau
equality on the corresponding filter-buffered neighborhood therefore makes
both terms, and hence their difference, exactly equal to the periodic
comparator at \(t=0\).  In a global Biot--Savart reconstruction the return
field contributes to the cancellation that recovers this local gradient; it
must not be dropped term by term.

This construction does not assert that a compact curl has nonzero total
vorticity.  Its necessary return field is present, explicitly, in the cutoff
transition and is handled by the two arguments above.

At positive times the heat kernel has infinite propagation, so geometric
separation alone is not called exact.  Put

\[
d_L=(L-2\Gamma-2)r_j>0.
\tag{6.3b}
\]

On either finite local dependency region \(D\), the initial difference from
the periodic comparator vanishes throughout the \(d_L\)-neighborhood of
\(D\) and has bounded derivatives of every fixed order.  Standard Gaussian
derivative bounds give, for \(0<t\le T\le r_k^2\),

\[
\|\nabla^a e^{\nu t\Delta}(E_L-E(q\cdot))\|_{L^\infty(D)}
\le C_a t^{-a/2}\exp\!\left(-\frac{d_L^2}{C_a\nu t}\right),
\tag{6.3c}
\]

and analogously for \(O_L\).  Since
\(\sup_{0<t\le T}t^{-a/2}e^{-d_L^2/(C\nu t)}\) is bounded by a polynomial in
\(d_L^{-1}\) times \(e^{-d_L^2/(C'\nu T)}\), this implies, for each fixed
derivative order \(a\),

\[
\sup_{0\le t\le r_k^2}
\|\nabla^a(e^{\nu t\Delta}E_L-e^{-\nu q^2t}E(q\cdot))\|_{L^\infty(D)}
\longrightarrow0
\quad(L\to\infty),
\tag{6.4}
\]

and the same holds for \(O_L\).  More quantitatively, away from the transition
the error is bounded by a polynomial derivative factor times

\[
\exp\!\left[-c_\nu(L-2\Gamma-2)^2
                 \left(\frac{r_j}{r_k}\right)^2\right].
\tag{6.5}
\]

The hard-shell kernel (5.1) is \(L^1\).  For the remainder, take at least one
derivative to control the full symmetric gradient and a local
\(C^{1,\alpha}\) norm for the near term.  Both filtered cubic densities are
therefore continuous in the displayed local smooth convergence.  Hence the
heat-averaged cubic coefficients for \((E_L,O_L)\) converge to the periodic
coefficients.
Choose one finite \(L\) after the nonzero periodic margins have been fixed.
This retains both the nonzero mixed coefficient and positive absolute
activity.  No limiting, non-energy datum enters the final theorem.

## 7. The cutoff lobes and the four exact coefficients

Choose one sufficiently large integer \(m\ge1\), then \(k\ge m\), put
\(j=k-m\), and take \(q=\kappa/r_j\) as in Section 5.  Select
\(0<\delta<\pi/2\) small enough that

\[
d_*:=q^{-1}(\delta,\delta,\delta)\in B_{r_k}.
\tag{7.1}
\]

This is possible because \(\delta\) may be chosen below
\(q r_k/\sqrt3=\kappa2^{-m}/\sqrt3\).  Let the spatial cutoff be the sum of
two identical nonnegative smooth bumps around \(d_*\) and \(-d_*\), small
enough that their closures are disjoint, lie in \(B_{r_k}\), and remain
inside the strict-sign neighborhoods in (4.9).  Normalize their heights and
the time factor so that \(0\le\chi_k\le1\).  Multiply by a nonzero
nonnegative smooth time profile compactly supported in \(I_k\).  The resulting
\(\chi_k\) is inversion even and is the parabolic rescaling of a fixed
profile after the pair \((k,m)\) is fixed.

For either the exact remainder functional or the project moving-shell
functional, write the linear heat-layer cubic as

\[
\mathcal F_0(E_L+sO_L)=A_0+A_1s+A_2s^2+A_3s^3.
\tag{7.2}
\]

Exact reflection parity gives

\[
A_0=A_2=0.
\tag{7.3}
\]

For the periodic comparator, heat evolution multiplies both \(E(q\cdot)\)
and \(O(q\cdot)\) by \(e^{-\nu q^2(t-t_-)}\); the radial filter and the
selected shell or remainder operator contribute the common nonzero factors
from Section 5.  Hence the mixed density keeps one strict sign on both lobes
throughout the support of the nonnegative time cutoff.  The periodic
calculation (4.9) and the localization convergence (6.4) then give, for the
selected finite \(L\),

\[
A_1\ne0.
\tag{7.4}
\]

The base density at \(s=0\) has opposite nonzero signs on the two cutoff
lobes.  Therefore

\[
\mathcal F_0(E_L)=0,
\qquad
\mathcal P_0(E_L)>0,
\tag{7.5}
\]

where \(\mathcal P_0\) denotes the same-kernel absolute companion.
The second inequality transfers from the periodic comparator because
\(\bigl||g_L|-|g_{\rm per}|\bigr|\le|g_L-g_{\rm per}|\); the first equality
is exact reflection parity and is not an approximation statement.

Now set

\[
v=\frac{E_L+O_L}{2},
\qquad
q_\lambda=v-\lambda\mathcal Rv
=\frac{1+\lambda}{2}E_L
 +\frac{1-\lambda}{2}O_L.
\tag{7.6}
\]

Substituting (7.2)--(7.3) gives every coefficient, without a pair-isolation
assumption:

\[
\begin{aligned}
H_0(\lambda)
={}&\frac18\left[
A_1(1+\lambda)^2(1-\lambda)
+A_3(1-\lambda)^3\right]\\
={}&\frac{A_1+A_3}{8}
+\frac{A_1-3A_3}{8}\lambda
+\frac{-A_1+3A_3}{8}\lambda^2
+\frac{-A_1-A_3}{8}\lambda^3.
\end{aligned}
\tag{7.7}
\]

Thus

\[
H_0(1)=0,
\qquad
H_0'(1)=-\frac{A_1}{2}\ne0.
\tag{7.8}
\]

This is the exact heat-averaged parity--transversality gate requested after
R0.70D.  The earlier ideal polynomial
\(K(\lambda-1)(\lambda+1)^2\) is not used; parity only forces the
anti-palindromic structure, while (7.4) supplies the simple root.

## 8. Small-data Navier--Stokes and exact nonlinear tuning

Let \(u^{\varepsilon,\lambda}\) be the whole-space Navier--Stokes solution
with initial datum

\[
u_0^{\varepsilon,\lambda}=\varepsilon q_\lambda.
\tag{8.1}
\]

Because \(q_\lambda\in C_{c,\sigma}^\infty\) and depends smoothly on
\(\lambda\), Kato small-data theory gives a unique global smooth solution for
all sufficiently small \(|\varepsilon|\), uniformly for \(\lambda\) near
one.  Put

\[
a^{\varepsilon,\lambda}
=u^{\varepsilon,\lambda}/\varepsilon
\quad(\varepsilon\ne0).
\tag{8.2}
\]

The normalized mild equation is

\[
a^{\varepsilon,\lambda}(t)
=e^{\nu t\Delta}q_\lambda
-\varepsilon\int_0^t e^{\nu(t-s)\Delta}
 \mathbb P\nabla\!\cdot
 (a^{\varepsilon,\lambda}\otimes a^{\varepsilon,\lambda})(s)\,ds.
\tag{8.3}
\]

Fix \(s>7/2\) and

\[
X_T=C([0,T];H^s(\mathbb R^3))
\cap L^2(0,T;H^{s+1}(\mathbb R^3)).
\tag{8.3a}
\]

Smallness in a critical Kato norm supplies global persistence, while the
local \(H^s\) mild map on the fixed interval is \(C^1\).  The contraction map
and its differentiated fixed-point equation therefore make
\(a^{\varepsilon,\lambda}\) a \(C^1\) function of
\((\varepsilon,\lambda)\) through

\[
a^{0,\lambda}=e^{\nu t\Delta}q_\lambda
\tag{8.4}
\]

in \(X_T\), which embeds into the local smooth norms required by both cubic
functionals.  Define

\[
\mathscr H(\varepsilon,\lambda)
=\begin{cases}
 \varepsilon^{-3}\mathcal F[u^{\varepsilon,\lambda}],
     &\varepsilon\ne0,\\
 \mathcal F[e^{\nu t\Delta}q_\lambda],&\varepsilon=0.
 \end{cases}
\tag{8.5}
\]

Exact cubic homogeneity and trilinear continuity make \(\mathscr H\) a
\(C^1\) function.  Equations (7.8) give

\[
\mathscr H(0,1)=0,
\qquad
\partial_\lambda\mathscr H(0,1)=-A_1/2\ne0.
\tag{8.6}
\]

The implicit-function theorem produces \(\lambda(\varepsilon)\), with

\[
\lambda(0)=1,
\qquad
\lambda(\varepsilon)=1+O(\varepsilon),
\tag{8.7}
\]

such that

\[
\mathcal F[u^{\varepsilon,\lambda(\varepsilon)}]=0.
\tag{8.8}
\]

By (7.5), continuity of the absolute companion, and exact cubic scaling,

\[
\mathcal P[u^{\varepsilon,\lambda(\varepsilon)}]
=\varepsilon^3\mathcal P_0(E_L)+o(\varepsilon^3)>0
\tag{8.9}
\]

for all sufficiently small positive \(\varepsilon\).  Applied to (2.4),
(8.8)--(8.9) prove (1.1) using the algebraic identity (2.7R).  Applied to
(1.2), they prove (1.3).

The full nonlinear solution does not preserve the linear parity at
\(\lambda=1\).  The exact nonlinear zero is supplied by the tuned
\(\lambda(\varepsilon)\), not by an incorrect symmetry assertion.

## 9. Formal theorem statements

### Theorem 9.1 — exact Yu remainder sign defect [P]

There exist parameters \(r>0\), \(0<\rho\le1/4\),
\(0<\ell\le\rho r\), a radial
Yu-admissible mollifier \(\varphi\), a radial Yu near cutoff \(\vartheta\),
an inversion-even \(0\le\chi\le1\) in \(C_c^\infty(Q_r)\), and a one-parameter
family of data in \(C_{c,\sigma}^\infty(\mathbb R^3)\) such that, for every
sufficiently small \(\varepsilon>0\), a member of the family generates a
unique global smooth Navier--Stokes solution satisfying (1.1) on the selected
time interval.

The functional \(\mathcal V_\chi^{\mathrm{rem}}\) and its positive part are
exactly Yu's (6.9) and (6.13).  The cutoff is project-chosen from Yu's
admissible class and is not the solution-adapted adjoint cutoff of Proposition
6.4.

### Theorem 9.2 — one strict Yu-kernel moving shell [P]

There exist integers \(k\ge m\ge1\), \(j=k-m\), an inversion-even
Yu-admissible \(0\le\chi_k\le1\), a radial admissible mollifier, and a
one-parameter family \(q_\lambda\in C_{c,\sigma}^\infty\) such that, for every
sufficiently small \(\varepsilon>0\), the datum
\(\varepsilon q_{\lambda(\varepsilon)}\) generates a global smooth
Navier--Stokes solution satisfying (1.3), with

\[
\mathcal P_{k,m}^{\mathrm{mov}}[u]
:=r_k\int_{I_k}\!\int\chi_k
\left|(\mathbb S_{k,m}\Omega_k)\cdot\Omega_k\right|dx\,dt.
\tag{9.1}
\]

Moreover the positive and negative parts of the same project density are
both \(\mathcal P_{k,m}^{\mathrm{mov}}/2\).

This theorem uses Yu's exact moving-shell strain tensor, hard shell, filter,
and dyadic time interval.  The scalar contraction, its absolute companion,
and the claim are new project objects.  They do not identify or estimate
\(\mu_k^{\mathrm{far,ann}}\), \(\mathfrak A_{j,k}\), or
\(\mathcal Q_k\).

## 10. Correction ledger for R0.70D

R0.70D's abstract fixed-scale cover obstruction remains valid.  Only its
description of the proposed next transfer target needs correction.

| R0.70D shorthand | R0.70E correction |
|---|---|
| “Yu filtered annular density” | Yu v1 defines no such signed scalar |
| “Yu shell window \(\eta_j\)” | Section 8.1 uses the hard moving domain \(A_{k,m}(x)\); a smooth fixed \(\eta_j\) is project-defined |
| “inversion-even Yu cutoff/filter” | Evenness is a project choice inside Yu's admissible classes, not a paper requirement |
| \(F_{j,k}^{\mathrm{Yu}}\) | Replace by the paper-defined \(\mathcal V_\chi^{\mathrm{rem}}\) or the explicitly project-defined \(\mathcal W_{k,m}^{\mathrm{mov}}\) |
| “one exact Yu matching shell” | “one project-defined signed contraction of Yu's moving-shell strain field” |
| \(\chi_k\eta_j=0\) return-field condition | Not the moving-shell geometry; use vector-potential localization plus the complete dependency region and heat-tail limit |

No result in R0.70A--D is retroactively promoted.  The correction prevents a
future manuscript from attributing a project definition to the primary
source.

## 11. What this changes, and what it does not

### Closed

- **Exact source-defined signed remainder:** realized by global smooth NSE
  with zero signed work and strictly positive positive-part work.
- **One real hard moving shell:** at the linear heat layer, the project signed
  contraction has an exact simple reflection root after all cubic terms are
  retained; the nonlinear root is the tuned \(\lambda(\varepsilon)\).
- **Return-field objection:** resolved by compactly localizing vector
  potentials.  The hard shell excludes the transition at \(t=0\); the exact
  remainder uses \(\mathbb S_\ell^{\rm rem}=\mathbb S_\ell-
  \mathbb S_\ell^{\rm near}\) and retains the global Biot--Savart
  cancellation rather than discarding the return field.
- **Heat interval:** the full Yu interval \(|I_k|=r_k^2\) is retained; strict
  scale separation makes the periodic heat model stable and the finite
  localization error arbitrarily small.
- **Nonlinear remainder:** exact signed cancellation is restored by a genuine
  one-parameter implicit-function argument.

### Not closed

- The theorem is existential for a selected even admissible
  \(\varphi,\chi_k\); it is not uniform over every admissible profile.
- It treats one shell pair, not all \(j\le k\), and it does not sum over
  scales.
- It gives no Carleson estimate for \(\mathfrak A_j\) and no affine-jet
  cancellation theorem.
- It does not control Yu's commutator defect or localization budgets.
- It concerns deliberately small global smooth solutions, not a
  near-singular or large-data regime.
- It is a no-go theorem for a proposed signed replacement, not a proof of
  regularity or blow-up.

## 12. Research value and next gate

The mathematical value is **route-elimination plus an exact transfer**.
R0.70C showed a parity obstruction for a generic smooth annular functional.
R0.70E transfers that obstruction to Yu's actual filtered remainder work and
to a genuine hard moving-shell kernel.  This removes the plausible objection
that the earlier cancellation was an artifact of the project's smooth shell
window, a short arbitrary time interval, or an unphysical compact-vorticity
ansatz.

The result also shows why Yu's balance must keep a positive part and
illustrates why magnitude-based annular estimates are natural: a signed
scalar can vanish at the same scale and on the same smooth solution where the
positive work is strictly nonzero.  It does not identify that scalar with
\(\mu_k^{\mathrm{far,ann}}\).

Its value toward the Millennium problem is indirect.  It prevents us from
spending further effort on a false deterministic closure mechanism.  The
next positive gate should be:

> **R0.70F:** test whether the low-order external affine strain jet admits a
> scale-summable cancellation or rigidity law under the exact filtered
> enstrophy evolution, with the positive remainder, commutator, and
> localization budgets kept explicit.

Any R0.70F statement must survive the R0.70E even--odd family.  In
particular, a proposed symmetry-breaking quantity must see the mixed
even--even--odd coefficient \(A_1\); a signed annular mean alone cannot.

## 13. Certificate and publication boundary

The exact algebra is reproduced by
`research/r070e_yu_parity_transversality_audit.py`.  It checks

1. divergence, potentials, heat eigenvalues, and reflection eigenvalues;
2. all four coefficients in (4.6) and their values at (4.7);
3. all four \(\lambda\)-coefficients in (7.7), the root, and its derivative;
4. the spherical moment (5.3) and leading shell multiplier (5.5).

The certificate does not numerically prove Gaussian heat-tail convergence,
Kato theory, or the implicit-function theorem.  The explanatory figure is an
analytic diagram generated from exact formulas, not DNS, trajectory data, or
an interval proof.

**DGX:** not justified.  The gate is analytic and symbolic; brute-force DNS
would not certify the simple root or the source-definition boundary.

**Independent review:** three read-only audits covering the primary source,
the reflection/kernel algebra, and the PDE localization/IFT chain passed
after the recorded corrections; see `research/r070e_independent_audit.md`.

**Publication:** the independent review gate has passed.  Keep R0.70E local.
Do not push, merge, or present Theorems 9.1--9.2 as public results without a
separate publication approval.

## 14. Primary-source map

| Claim used | Primary source | Boundary retained |
|---|---|---|
| Mollifier assumptions and near cutoff | [Yu v1, §2](https://arxiv.org/html/2606.27560v1#S2) | \(\varphi\) is not required to be even/radial; \(\vartheta\) is radial |
| Signed remainder work and positive remainder | [Yu v1, (6.9), (6.13)](https://arxiv.org/html/2606.27560v1#S6) | Exact paper-defined objects |
| Dyadic scales, filter, cutoff profile | [Yu v1, §7](https://arxiv.org/html/2606.27560v1#S7) | Even cutoff is an admissible project specialization |
| Moving-shell strain tensor and reservoirs | [Yu v1, §8.1](https://arxiv.org/html/2606.27560v1#S8.SS1) | Tensor is defined; project signed scalar is not |
| Moving shells are an absolute-value device | [Yu v1, §8.3](https://arxiv.org/html/2606.27560v1#S8.SS3) | No identification with a fixed smooth signed partition |
| Small-data global mild solution and normalized IFT framework | Kato theory as used already in R0.70C | Standard analytic input; not re-proved by the symbolic certificate |
