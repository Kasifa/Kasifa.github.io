# R0.70A draft — Moving physical annuli and the missing normal form

## 1. Status and the first structural distinction

This note is a derivation draft.  It records identities for smooth decaying
three-dimensional Navier--Stokes solutions.  It does not give a regularity
criterion, a depletion theorem, or a solution of the Millennium Problem.
The differentiation method belongs to the mature family of exact two-point
and coarse-grained balances represented by
[Hill's exact structure-function equations](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/exact-secondorder-structurefunction-relationships/C48D3847FDAE125F92032A412AB674A7),
[Eyink--Aluie smooth coarse-graining](https://arxiv.org/html/0909.2386), and
[Yu's filtered vorticity-energy balance](https://arxiv.org/html/2606.27560v1).
I do not claim novelty for the act of differentiating a two-point kernel or a
moving localized energy.  Any contribution would have to come from a new
signed estimate or a rigorous obstruction for a specified class.

Let

\[
 \partial_tu+u\cdot\nabla u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0,
 \qquad \omega=\nabla\times u,
 \tag{1.1}
\]

on \(\mathbb R^3\), with enough decay that all integrations below are
justified.  Write

\[
 A=\nabla u,\qquad
 S=\frac12(A+A^{\mathsf T}),\qquad
 \Omega=\frac12(A-A^{\mathsf T}),\qquad
 H=\nabla^2p.
 \tag{1.2}
\]

There are two different operations that must not be conflated.

1. At each fixed time, one may insert an arbitrary scale \(r(t)>0\) into the
   algebraic physical-annulus partition of vortex stretching.  This merely
   relabels the instantaneous terms.  No \(\dot r\) term appears in the
   enstrophy identity.
2. One may instead differentiate a specifically defined band functional, or
   a one-point energy carrying a moving spatial cutoff.  Then the chain rule
   produces a \(\dot r\) boundary term.  That term is a scale-label flux.  It
   is not automatically vortex stretching and has no fixed sign.  "Scale-label
   flux" here means only the kinematic derivative of a freely moving label; it
   is not the physical inter-scale energy flux of coarse-graining theory.

R0.69T anticipated a moving boundary but did not construct a quadratic
two-point energy whose derivative produces the desired annular stretching.
The missing construction is the main obstruction identified here.  I do not
use the phrase "moving annular budget" unless such an energy or normal form is
specified.

This time-dependent separation label is also distinct from the "moving shell"
in Yu Section 8.3, where a spatial shell follows a core point inside an
absolute-value estimate.

## 2. A continuous physical annulus

Choose a nonincreasing radial profile \(\chi\in C^\infty([0,\infty))\) with

\[
 \chi(s)=1\quad(0\le s\le1),\qquad
 \chi(s)=0\quad(s\ge2),\qquad 0\le\chi\le1.
 \tag{2.1}
\]

For \(z=y-x\ne0\), put

\[
 e=\frac z{|z|},\qquad
 \delta\omega=\omega(y)-\omega(x),
 \tag{2.2}
\]

and define the signed two-increment numerator

\[
 N[\omega](x,y)
 =\bigl(e\cdot\delta\omega\bigr)
  \bigl(e\cdot(\omega(x)\times\delta\omega)\bigr).
 \tag{2.3}
\]

Fix a ratio \(\Lambda>1\).  The continuous annular window is

\[
 \eta_{r,\Lambda}(z)
 =\chi\!\left(\frac{|z|}{\Lambda r}\right)
  -\chi\!\left(\frac{|z|}{r}\right),
 \qquad r>0,
 \tag{2.4}
\]

and the corresponding signed production is

\[
 \boxed{
 \mathcal A_{r,\Lambda}(u)
 =\frac{3}{8\pi}\iint
 \eta_{r,\Lambda}(y-x)
 \frac{N[\omega](x,y)}{|x-y|^3}\,dy\,dx.}
 \tag{2.5}
\]

For \(\Lambda=2\) and \(r=2^j\), this is the R0.69T functional
\(\mathcal A_j\).  Define also the signed near and far pieces

\[
 \begin{aligned}
 \mathcal N_r(u)
 &=\frac{3}{8\pi}\iint
   \chi\!\left(\frac{|z|}{r}\right)
   \frac{N[\omega](x,y)}{|z|^3}\,dy\,dx,\\
 \mathcal F_{\Lambda r}(u)
 &=\frac{3}{8\pi}\iint
   \left[1-\chi\!\left(\frac{|z|}{\Lambda r}\right)\right]
   \frac{N[\omega](x,y)}{|z|^3}\,dy\,dx.
 \end{aligned}
 \tag{2.6}
\]

The three weights sum to one.  Therefore, for every \(r>0\),

\[
 \boxed{
 \mathcal V(u):=\int\omega\cdot S\omega\,dx
 =\mathcal N_r(u)+\mathcal A_{r,\Lambda}(u)
  +\mathcal F_{\Lambda r}(u).}
 \tag{2.7}
\]

The identity remains true after replacing \(r\) by any positive function
\(r(t)\).  It is still a fixed-time algebraic identity.

The global enstrophy balance is

\[
 \frac12\frac d{dt}\|\omega(t)\|_2^2
 +\nu\|\nabla\omega(t)\|_2^2
 =\mathcal V(u(t)).
 \tag{2.8}
\]

Combining (2.7) and (2.8) gives

\[
 \frac12\frac d{dt}\|\omega\|_2^2
 +\nu\|\nabla\omega\|_2^2
 =\mathcal N_{r(t)}(u)
  +\mathcal A_{r(t),\Lambda}(u)
  +\mathcal F_{\Lambda r(t)}(u).
 \tag{2.9}
\]

There is no \(\dot r\) in (2.9).  Integrating (2.9) in time also introduces
no \(\dot r\); it only integrates the three instantaneous pieces.  A
\(\dot r\) term belongs to the derivative of one selected piece, which is a
different calculation.

## 3. Exact derivative of a selected moving band

Set

\[
 \vartheta(s)=-s\chi'(s)\ge0.
 \tag{3.1}
\]

For a differentiable positive scale \(r(t)\),

\[
 \partial_t\eta_{r(t),\Lambda}(z)
 =\frac{\dot r(t)}{r(t)}
 \left[
  \vartheta\!\left(\frac{|z|}{\Lambda r(t)}\right)
  -\vartheta\!\left(\frac{|z|}{r(t)}\right)
 \right].
 \tag{3.2}
\]

For a vorticity variation \(h\), the exact first variation of (2.3) is

\[
\begin{aligned}
 DN_\omega[h]
={}&(e\cdot\delta h)
     (e\cdot(\omega(x)\times\delta\omega))\\
 &+(e\cdot\delta\omega)
   \left[e\cdot\bigl(h(x)\times\delta\omega
                      +\omega(x)\times\delta h\bigr)\right],
\end{aligned}
 \tag{3.3}
\]

where \(\delta h=h(y)-h(x)\).  Define

\[
 \mathfrak L_{r,\Lambda}[h]
 =\frac{3}{8\pi}\iint
  \eta_{r,\Lambda}(z)\frac{DN_\omega[h]}{|z|^3}\,dy\,dx
 \tag{3.4}
\]

and

\[
 \mathfrak B_{r,\Lambda}[\omega]
 =\frac{3}{8\pi}\iint
 \left[
  \vartheta\!\left(\frac{|z|}{\Lambda r}\right)
  -\vartheta\!\left(\frac{|z|}{r}\right)
 \right]
 \frac{N[\omega](x,y)}{|z|^3}\,dy\,dx.
 \tag{3.5}
\]

The vorticity equation is

\[
 \partial_t\omega=-u\cdot\nabla\omega+S\omega+\nu\Delta\omega.
 \tag{3.6}
\]

The exact differentiated identity is therefore

\[
\boxed{
\begin{aligned}
 \frac d{dt}\mathcal A_{r(t),\Lambda}(u(t))
 ={}&\frac{\dot r}{r}\mathfrak B_{r,\Lambda}[\omega]
   +\mathfrak T_{r,\Lambda}[u,\omega]
   +\mathfrak S_{r,\Lambda}[u,\omega]
   +\mathfrak D_{r,\Lambda}[\omega],\\
 \mathfrak T_{r,\Lambda}
 :={}&\mathfrak L_{r,\Lambda}[-u\cdot\nabla\omega],\\
 \mathfrak S_{r,\Lambda}
 :={}&\mathfrak L_{r,\Lambda}[S\omega],\\
 \mathfrak D_{r,\Lambda}
 :={}&\nu\mathfrak L_{r,\Lambda}[\Delta\omega].
\end{aligned}}
 \tag{3.7}
\]

All four terms in (3.7) are retained.  In particular, the viscous derivative
of this cubic functional is not an enstrophy dissipation and has no evident
sign.

The transport term has an equivalent relative-velocity form.  If
\(\delta u=u(y)-u(x)\), integration by parts in \(x\) and \(y\), using
\(\nabla\cdot u=0\), gives

\[
 \boxed{
 \mathfrak T_{r,\Lambda}
 =\frac{3}{8\pi}\iint
 \delta u\cdot\nabla_z
 \left[
  \eta_{r,\Lambda}(z)
  \frac{N[\omega](x,y)}{|z|^3}
 \right]_{\omega(x),\omega(y)\ \text{ fixed}}dy\,dx.}
 \tag{3.8}
\]

The gradient in (3.8) differentiates the explicit separation vector,
including \(e=z/|z|\), but holds the two vorticity values fixed.  Thus
ordinary advection produces another boundary and angular flux.  It does not
vanish merely because the window is radial.

For the three-piece partition (2.7), the explicit scale derivatives are
proportional to

\[
 \vartheta\!\left(\frac{|z|}{r}\right),\qquad
 \vartheta\!\left(\frac{|z|}{\Lambda r}\right)
 -\vartheta\!\left(\frac{|z|}{r}\right),\qquad
 -\vartheta\!\left(\frac{|z|}{\Lambda r}\right),
 \tag{3.9}
\]

for the near, band, and far pieces, respectively.  Their sum is zero.  This
is the exact statement that the \(\dot r\) terms only redistribute a fixed
instantaneous production among moving labels.

## 4. Initial trace and what (3.7) does not provide

Integrating (3.7) from \(t_0\) to \(t_1\) gives

\[
\boxed{
\begin{aligned}
 \mathcal A_{r(t_1),\Lambda}(u(t_1))
 ={}&\mathcal A_{r(t_0),\Lambda}(u(t_0))\\
 &+\int_{t_0}^{t_1}
 \left(
  \frac{\dot r}{r}\mathfrak B_{r,\Lambda}
  +\mathfrak T_{r,\Lambda}
  +\mathfrak S_{r,\Lambda}
  +\mathfrak D_{r,\Lambda}
 \right)dt.
\end{aligned}}
 \tag{4.1}
\]

The first term on the right is an unavoidable cubic initial trace.  Equation
(4.1) controls the change of an annular production.  It does **not** rewrite

\[
 \int_{t_0}^{t_1}\mathcal A_{r(t),\Lambda}(u(t))\,dt
 \tag{4.2}
\]

as a boundary term.  The right side of (3.7) is cubic under the linear heat
part and quartic under the nonlinear stretching and transport parts.  It is
not the cubic integrand (4.2).  Therefore choosing \(r(t)\) does not by itself
close the enstrophy balance.

## 5. Where nonlocal strain and pressure enter

The term \(S\omega\) in (3.6) is already nonlocal because \(S\) is a
Calderon--Zygmund transform of \(\omega\).  Pressure is absent from the curl
equation.  It must not be declared zero in the corresponding strain
dynamics.

For the full, untruncated production

\[
 \mathcal V(t)=\int\omega\cdot S\omega\,dx,
 \tag{5.1}
\]

the strain equation

\[
 (\partial_t+u\cdot\nabla-\nu\Delta)S
 +S^2+\Omega^2+H=0
 \tag{5.2}
\]

and the vorticity equation give

\[
\boxed{
\begin{aligned}
 \frac d{dt}\mathcal V
 ={}&\int|S\omega|^2\,dx-\int\omega\cdot H\omega\,dx\\
 &+\nu\left[
  2\int\Delta\omega\cdot S\omega\,dx
  +\int\omega\cdot(\Delta S)\omega\,dx
 \right].
\end{aligned}}
 \tag{5.3}
\]

Here \(\Omega\omega=0\), and
\(\omega\cdot S^2\omega=|S\omega|^2\), which gives the first line.
The viscous bracket may also be written as

\[
 -4\int(\partial_k\omega_i)(\partial_kS_{ij})\omega_j\,dx
 -2\int S_{ij}(\partial_k\omega_i)(\partial_k\omega_j)\,dx.
 \tag{5.4}
\]

Neither (5.3) nor (5.4) has a fixed sign.  In particular, the pressure-Hessian
term is present and nonlocal.

If the derivatives of the near, band, and far pieces in (2.7) are added,
their \(\dot r\) terms cancel and the remaining terms reconstruct (5.3).
In a vorticity-only calculation the pressure Hessian is encoded in the full
Leray/Biot--Savart relation.  Assigning a separate pressure contribution to
one annulus requires an additional choice of truncated projection and its
commutator.  There is no canonical pressure-shell term supplied by R0.69T.

## 6. A standard moving one-point localized enstrophy balance

A \(\dot r\) term does occur in an energy identity when the energy itself
carries a moving spatial cutoff.  This is different from the pair-separation
window in Section 2.

Let \(\phi_0\in C_c^\infty(\mathbb R^3)\), let \(R(t)>0\), and optionally
let the center \(X(t)\) move.  Set

\[
 \phi(x,t)=\phi_0\!\left(\frac{x-X(t)}{R(t)}\right).
 \tag{6.1}
\]

Then

\[
 \partial_t\phi
 =-\dot X\cdot\nabla\phi
  -\frac{\dot R}{R}(x-X)\cdot\nabla\phi.
 \tag{6.2}
\]

With \(e_\omega=|\omega|^2/2\), the exact localized enstrophy identity is

\[
\boxed{
\begin{aligned}
 \frac d{dt}\int\phi e_\omega\,dx
 +\nu\int\phi|\nabla\omega|^2\,dx
 ={}&\int\phi\,\omega\cdot S\omega\,dx\\
 &+\int e_\omega
 \left[
  (u-\dot X)\cdot\nabla\phi
  -\frac{\dot R}{R}(x-X)\cdot\nabla\phi
  +\nu\Delta\phi
 \right]dx.
\end{aligned}}
 \tag{6.3}
\]

After integration in time, (6.3) contains the initial trace

\[
 \int\phi(x,t_0)e_\omega(x,t_0)\,dx.
 \tag{6.4}
\]

The three boundary terms in (6.3) are, respectively, relative transport,
motion of the spatial scale, and viscous leakage.  Their signs depend on the
solution and on the prescribed motion.  The \(\dot R\) term cannot be counted
as dissipation.

### 6.1 Weighted pair decomposition of the localized stretching

Spatial localization also changes the two-increment identity.  For an even
separation weight \(\eta(z)\), define the unsymmetrized piece

\[
 \mathcal V_{\phi,\eta}
 =\frac{3}{4\pi}\iint
 \phi(x)\eta(y-x)
 \frac{J(x,y)}{|x-y|^3}\,dy\,dx,
 \tag{6.5}
\]

where \(J\) is the R0.69T unsymmetrized numerator.  Put

\[
 \bar\phi=\frac{\phi(x)+\phi(y)}2,
 \qquad \delta\phi=\phi(y)-\phi(x).
 \tag{6.6}
\]

Pair exchange gives the exact weighted identity

\[
\boxed{
\begin{aligned}
 \mathcal V_{\phi,\eta}
 =\frac{3}{8\pi}\iint\frac{\eta(z)}{|z|^3}
 \Bigg[{}&\bar\phi
  (e\cdot\delta\omega)
  (e\cdot(\omega(x)\times\delta\omega))\\
 &+\frac{\delta\phi}{2}
  (e\cdot(\omega(x)+\omega(y)))
  (e\cdot(\omega(x)\times\delta\omega))
 \Bigg]dy\,dx.
\end{aligned}}
 \tag{6.7}
\]

For \(\phi=1\), the second line vanishes and (6.7) reduces to R0.69T.  For a
moving local energy it is an unavoidable weight commutator.  A partition of
unity in \(\eta\) reconstructs the localized stretching in (6.3), but every
annulus carries both lines of (6.7).  Keeping only the first line would omit a
boundary-crossing interaction of the same scaling degree.

## 7. The corresponding moving strain balance and pressure terms

The vorticity identity (6.3) contains nonlocal strain but no explicit
pressure.  The moving localized strain identity displays the pressure terms.
Let

\[
 q=\operatorname{tr}(A^2)=-\Delta p.
 \tag{7.1}
\]

The exact weighted identities from R0.69I are

\[
 \int\phi S:H\,dx
 =\int(\Delta p)u\cdot\nabla\phi\,dx
  +\int u_i(\partial_jp)(\partial_{ij}\phi)\,dx
 \tag{7.2}
\]

and

\[
 \int\phi\operatorname{tr}(A^3)\,dx
 =\int\left(\frac12qu-A^2u\right)\cdot\nabla\phi\,dx.
 \tag{7.3}
\]

Using (6.2), the full moving localized strain balance is

\[
\boxed{
\begin{aligned}
 &\frac12\frac d{dt}\int\phi|S|^2\,dx
 +\nu\int\phi|\nabla S|^2\,dx
 +2\int\phi\det S\,dx\\
 ={}&\frac12\int
 \left[
  (u-\dot X)\cdot\nabla\phi
  -\frac{\dot R}{R}(x-X)\cdot\nabla\phi
  +\nu\Delta\phi
 \right]|S|^2\,dx\\
 &-\frac13\int
  \left(\frac12qu-A^2u\right)\cdot\nabla\phi\,dx\\
 &-\int(\Delta p)u\cdot\nabla\phi\,dx
  -\int u_i(\partial_jp)(\partial_{ij}\phi)\,dx.
\end{aligned}}
 \tag{7.4}
\]

Integrating (7.4) retains the initial strain trace

\[
 \frac12\int\phi(x,t_0)|S(x,t_0)|^2\,dx.
 \tag{7.5}
\]

Equation (7.4) contains the moving-scale, transport, viscous, Betchov, and
pressure boundary terms separately.  R0.69O supplies a possible estimate for
part of the pressure commutator at the smooth level, but it does not turn the
annular stretching in (6.7) into a time derivative.

## 8. Scaling audit

Under the Navier--Stokes scaling

\[
 u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t),
 \qquad
 p_\lambda(x,t)=\lambda^2p(\lambda x,\lambda^2t),
 \tag{8.1}
\]

set

\[
 \widetilde r(t)=\lambda^{-1}r(\lambda^2t),
 \qquad
 \widetilde R(t)=\lambda^{-1}R(\lambda^2t),
 \qquad
 \widetilde X(t)=\lambda^{-1}X(\lambda^2t).
 \tag{8.2}
\]

Then

\[
 \mathcal A_{\widetilde r(t),\Lambda}(u_\lambda(t))
 =\lambda^3
  \mathcal A_{r(\lambda^2t),\Lambda}(u(\lambda^2t)),
 \tag{8.3}
\]

and every term in (3.7) scales as \(\lambda^5\).  In particular,

\[
 \frac{\dot{\widetilde r}}{\widetilde r}
 =\lambda^2\frac{\dot r}{r}
 \tag{8.4}
\]

at the corresponding time, so the moving-boundary term has no subcritical
gain.

The localized enstrophy and strain energies in (6.3) and (7.4) scale as
\(\lambda\).  Their instantaneous rates, including all transport, moving,
viscous, cubic, and pressure terms, scale as \(\lambda^3\).  Their time
integrals again scale as \(\lambda\).  Consequently,

\[
 r\int_{t_0}^{t_0+cr^2}\mathcal A_{r,\Lambda}(u(t))\,dt
 \tag{8.5}
\]

is dimensionless, but dimensional consistency alone gives no estimate or
sign.

## 9. Sign audit

The exact identities give the following sign table.

| term | available sign | reason |
|---|---:|---|
| \((\dot r/r)\mathfrak B_{r,\Lambda}\) | none | \(N[\omega]\) is signed and the two boundary shells enter with opposite signs |
| \(\mathfrak T_{r,\Lambda}\) | none | relative transport differentiates the radial and angular kernel |
| \(\mathfrak S_{r,\Lambda}\) | none | it is quartic and contains the nonlocal strain |
| \(\mathfrak D_{r,\Lambda}\) | none | a cubic functional has no positive quadratic viscous form |
| \(-\int\omega\cdot H\omega\) | none | the pressure Hessian is nonlocal and has pointwise sign counterexamples |
| moving spatial-cutoff term in (6.3) | none | its sign can be changed by the prescribed \(\dot R\) |
| initial traces in (4.1), (6.4), (7.5) | none | they are data, not dissipation |

Thus no term obtained merely by differentiating the moving annulus is a
candidate universal deficit.

## 10. Affine-core and single-scale pressure tests

### 10.1 Affine core

Let \(v_A\) be the compactly supported divergence-free field from R0.69P,
equal to \(Ax\) on a ball.  In a smaller core ball,

\[
 \omega=\omega_0,\qquad S=S_0,qquad
 \nabla\omega=0,qquad
 \omega_0\cdot S_0\omega_0>0.
 \tag{10.1}
\]

For every pair lying wholly in the affine core,

\[
 \delta\omega=0,qquad N[\omega](x,y)=0.
 \tag{10.2}
\]

Hence a quadratic or cubic candidate built only from sufficiently short
internal vorticity increments cannot generate the positive core stretching.
It must retain boundary-crossing pairs or an initial trace.

Choose the spatial cutoff \(\phi\) in (6.3) with its full support inside the
affine region and take \(\dot X=\dot R=0\) at the initial time.  Since
\(\omega\) is constant there,

\[
 \int\phi|\nabla\omega|^2=0,
 \qquad
 \int e_\omega(u\cdot\nabla\phi+\nu\Delta\phi)=0,
 \tag{10.3}
\]

while

\[
 \int\phi\,\omega\cdot S\omega>0.
 \tag{10.4}
\]

The transport integral in (10.3) vanishes by incompressibility and constant
\(e_\omega\); the Laplacian integral vanishes by compact support.  This is an
exact initial-time test.  Allowing an arbitrary \(\dot R\) only adds a
chosen label-volume derivative and does not turn (10.4) into dissipation.

### 10.2 Single-scale dilation

For the R0.69U self-similar family

\[
 U_R(x)=R\,U_1(x/R),
 \tag{10.5}
\]

the full physical annular pieces obey

\[
 \mathcal A_{Rr,\Lambda}(U_R)
 =R^3\mathcal A_{r,\Lambda}(U_1).
 \tag{10.6}
\]

Therefore matching a moving window to a single geometric scale does not
create a smaller remainder.  The window flux remains at the same scaling
degree as the stretching.  Any proposed estimate that gains a factor tending
to zero solely because \(r(t)\) follows this scale fails (10.6).

The schedule test is also strict: the same smooth solution may be inspected
with two different positive functions \(r_1(t)\) and \(r_2(t)\).  Their
fixed-time reconstructions (2.7) agree, while their individual
\(\dot r\)-fluxes differ.  A physical conclusion cannot depend on the sign of
that freely prescribed flux unless the scale law is part of a proved
solution-dependent construction and its initial trace is retained.

### 10.3 Pressure nonlocality

R0.69H supplies two smooth divergence-free initial data with the same local
pair \((S,\omega)\) but opposite signs of one principal pressure-Hessian
component.  Therefore a normal form depending only on local \((S,\omega)\)
cannot assign a favorable pressure sign.  It must contain the nonlocal
pressure projection or an integrated pressure commutator such as (7.2).

## 11. The project-specific bridge lemma that is still missing

For this project's next candidate, the useful target is not
\(d\mathcal A_{r(t),\Lambda}/dt\).  It is a quadratic two-point energy or
normal form \(Q_r\) whose **nonlinear** time derivative contains
\(\mathcal A_{r,\Lambda}\).  This is a route choice, not a claim that exact
structure functions, coarse-grained energies, or filtered enstrophy provide no
other dynamic organization.

A minimal translation-invariant candidate would have the form

\[
 Q_r(\omega)=\frac12\langle\omega,M_r\omega\rangle,
 \tag{11.1}
\]

where \(M_r\) is self-adjoint and localized to physical scale \(r\).  Along
the vorticity equation,

\[
\begin{aligned}
 \frac d{dt}Q_{r(t)}(\omega)
 ={}&\langle M_r\omega,S\omega-u\cdot\nabla\omega\rangle
 -\nu\langle\nabla\omega,M_r\nabla\omega\rangle\\
 &+\frac{\dot r}{2}\langle\omega,(\partial_rM_r)\omega\rangle,
\end{aligned}
 \tag{11.2}
\]

when \(M_r\) commutes with spatial derivatives; otherwise the corresponding
commutators must be added.  The unresolved bridge lemma is to find \(M_r\),
or a more general two-point \(Q_r\), such that

\[
 \boxed{
 \langle M_r\omega,S\omega-u\cdot\nabla\omega\rangle
 =\mathcal A_{r,\Lambda}(u)+\mathcal R_r(u),}
 \tag{11.3}
\]

with all of the following properties:

1. \(Q_r\) and its initial trace are controlled by a scale-critical energy;
2. the viscous term is nonnegative or absorbable;
3. \(r\int\mathcal R_r\,dt\) is summable, telescoping, or strictly smaller
   than the target production;
4. the moving-boundary term is controlled for a scale law determined by the
   solution, not chosen after seeing the sign;
5. spatial localization retains the weight commutator in (6.7) and the
   pressure terms in (7.4).

For \(M_r=I\), transport cancels and (11.3) holds only after summing all
separations: this is the ordinary enstrophy identity.  For a nonconstant
scale selector, the transport commutator reappears.  No operator satisfying
all five requirements has been constructed in this note.

## 12. Falsification gates for the next calculation

Before any large simulation, the bridge lemma should pass four exact tests.

1. **Triad-symbol test.**  For a translation-invariant multiplier \(M_r\),
   compare the full Fourier triad symbol on the left of (11.3) with the symbol
   of \(\mathcal A_{r,\Lambda}\).  An exact resonant triad on which the target
   is nonzero but every admissible coboundary vanishes rules out this class of
   normal forms.
2. **Affine-core test.**  A candidate supported only on internal short
   increments fails unless it reproduces the boundary carrier and the
   initial trace from Section 10.1.
3. **Single-scale test.**  Every remainder must respect (10.6); a claimed
   scale-decaying factor produced only by moving the label is false.
4. **Pressure-twin test.**  A local closure must give the same value on the
   R0.69H pressure twins, while the exact pressure response has opposite
   signs.  Such a closure must be rejected or enlarged by a nonlocal term.

The branch should stop if the triad-symbol equation is inconsistent, if the
affine core leaves a same-order uncancelled carrier, or if closing
\(\mathcal R_r\) requires assuming an existing critical regularity criterion.
Each failure has a deliberately narrow scope: the triad test can rule out the
tested translation-invariant multiplier class; the affine-core test can rule
out a pure short-increment form; the single-scale test can rule out smallness
created only by moving the label; and the pressure twins can rule out a closure
depending only on local \((S,\omega)\).  None rules out every possible normal
form or every annular route.  A failure is an obstruction only for its stated
class, and it is not a reason to replace the missing estimate by numerical
evidence.

## 13. Claim boundary

The completed part of this draft consists of:

- the fixed-time near/band/far identity with an arbitrary moving label;
- the exact derivative (3.7), including \(\dot r\), transport, stretching,
  and viscosity;
- the cubic initial trace (4.1);
- the full pressure-Hessian consistency identity (5.3);
- the moving localized enstrophy and strain balances (6.3) and (7.4);
- the weighted pair commutator (6.7);
- the scaling and sign audits.

The unproved part is decisive: no controlled \(Q_r\) satisfying (11.3) has
been found.  Without that normal form, the moving scale does not convert
annular vortex stretching into a favorable time boundary or a critical-norm
estimate.  R0.70A is therefore an unclosed derivation and route test, not a
Navier--Stokes regularity result.
