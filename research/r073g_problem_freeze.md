# R0.73G problem freeze: nonlinear shadowing of one-row amplification

**Frozen:** 2026-08-30  
**Parent release:** R0.73F  
**Physical realization:** viscosity one, shear frequency $R=2$, horizontal
row $K_1=0$, $K_3=1$, Bloch residue zero  
**Evidence target:** a finite-time nonlinear perturbation theorem with an
explicit topology, seed threshold, lifespan, and quadratic remainder; no
finite calculation may carry the proof

## 1. Exact background and inherited linear input

Let

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
 \qquad W_d=W_{xx},
 \tag{1.1}
\]

and work on the standard three-torus.  For every $\Lambda\ge1$,

\[
 \overline U_\Lambda(t,y)
 =\bigl(0,0,2\Lambda W(4t,2y)\bigr)
 \tag{1.2}
\]

is an exact smooth unforced Navier--Stokes solution with viscosity one.  The
choice $R=2$, $K_3=1$ realizes the R0.73F row

\[
 \gamma=\frac{K_3}{R}=\frac12,
 \qquad \beta=\xi=0,
 \qquad \varepsilon=\Lambda^{-1}.
 \tag{1.3}
\]

Let $d_0,K_{\rm F},\alpha,\eta$ be the constants in R0.73F, with
$K_{\rm F}$ denoting its dichotomy prefactor.  For a fixed
dimensionless observation window $D>0$, put

\[
 d_D=\min\{D,d_0\},
 \qquad T_D=\frac{d_D}{4},
 \qquad \kappa_D=(\alpha+\eta)d_D.
 \tag{1.4}
\]

The exact linearized evolution on the conjugate pair of rows
$(K_1,K_3)=(0,\pm1)$ has a smooth real unit vector
$\phi_\Lambda$ satisfying

\[
 \|\mathcal U_\Lambda(T_D,0)\phi_\Lambda\|_{L^2}
 \ge K_{\rm F}^{-1}e^{\kappa_D\Lambda}.
 \tag{1.5}
\]

The vector may depend on $\Lambda$.  R0.73G must quantify enough of its
Sobolev cost to use it as nonlinear initial data.

## 2. Exact perturbation equation

Write an exact solution as

\[
 U=\overline U_\Lambda+w,
 \qquad \nabla\cdot w=0.
 \tag{2.1}
\]

After applying the Leray projector, the perturbation equation is

\[
 \boxed{
 \partial_t w
 =\Delta w
 -\mathbb P\bigl(
 \overline U_\Lambda\cdot\nabla w
 +w\cdot\nabla\overline U_\Lambda
 \bigr)
 -\mathbb P\nabla\cdot(w\otimes w).}
 \tag{2.2}
\]

The first two terms after the Laplacian define the exact full linearized
operator $L_\Lambda(t)$.  The last term couples different Fourier rows and
is not present in R0.73F.

## 3. Contract G1: a polynomial Sobolev cost for a top vector

Let

\[
 \widetilde B_\varepsilon(0)
 =\widetilde A(0)-\varepsilon
 \left(-\partial_x^2+\frac14\right)
 \tag{3.1}
\]

be the frozen kinetic-space generator.  Select an eigenvector in its nonzero
finite-dimensional top cluster and normalize it in kinetic $L^2$.  The
fixed-contour bound from R0.73F and the order-zero structure of
$\widetilde A(0)$ must be used to prove

\[
 \boxed{\|\phi_\Lambda\|_{H^3(\mathbb T^3)}
 \le C_{\rm top}\Lambda^2.}
 \tag{3.2}
\]

The power two is deliberately non-sharp.  A polynomial bound is enough
because (1.5) is exponential.  This contract concerns one selected smooth
top eigenvector, not a uniform $L^2\to H^3$ bound for the whole moving
projection.

## 4. Contract G2: a closed $H^3$ bootstrap on the fixed window

For $Y(t)=\|w(t)\|_{H^3}$, standard commutator and product estimates on the
torus must give constants $a,b>0$, independent of $\Lambda$, such that

\[
 Y'(t)\le a\Lambda Y(t)+bY(t)^2
 \tag{4.1}
\]

for every smooth solution on $0\le t\le T_D$.  Define

\[
 \rho_\Lambda
 =\frac{a\Lambda}{4b}e^{-a\Lambda T_D}.
 \tag{4.2}
\]

If $Y(0)\le\rho_\Lambda$, the bootstrap must close as

\[
 \boxed{Y(t)\le2e^{a\Lambda t}Y(0),
 \qquad 0\le t\le T_D.}
 \tag{4.3}
\]

In particular, the strong solution exists at least through $T_D$.  This is
a finite-time small-perturbation statement around a globally smooth exact
background; it is not a global theorem for arbitrary three-dimensional
data.

## 5. Contract G3: the nonlinear remainder and seed threshold

Let $z$ solve the exact linearized equation

\[
 z_t=L_\Lambda(t)z,
 \qquad z(0)=w(0),
 \tag{5.1}
\]

and put $r=w-z$.  The exact remainder equation is

\[
 r_t=L_\Lambda(t)r
 -\mathbb P\nabla\cdot(w\otimes w),
 \qquad r(0)=0.
 \tag{5.2}
\]

The section must prove constants $C_D,M_D>0$, independent of
$\Lambda$, such that under (4.3)

\[
 \boxed{
 \|r(T_D)\|_2
 \le C_D e^{M_D\Lambda}
 \|w(0)\|_{H^3}^2.}
 \tag{5.3}
\]

Combining (3.2) and (5.3), define the sufficient seed ceiling

\[
 \begin{aligned}
 \delta_\Lambda^{\max}:=\min\Bigg\{&
 \frac{a}{4bC_{\rm top}}\Lambda^{-1}e^{-a\Lambda T_D},\\
 &\frac{1}{2K_{\rm F}C_DC_{\rm top}^2}
 \Lambda^{-4}
 e^{-(M_D-\kappa_D)_+\Lambda}
 \Bigg\}.
 \end{aligned}
 \tag{5.4}
\]

For $0<\delta\le\delta_\Lambda^{\max}$, take

\[
 w(0)=\delta\phi_\Lambda.
 \tag{5.5}
\]

Then the exact nonlinear perturbation must satisfy

\[
 \boxed{
 \|w(T_D)\|_2
 \ge \frac1{2K_{\rm F}}e^{\kappa_D\Lambda}
 \|w(0)\|_2.}
 \tag{5.6}
\]

Equation (5.6) is a family-level nonlinear **relative amplification**
theorem.  The allowed seed is exponentially small and the proof does not
show that the final perturbation is order one.

## 6. Contract G4: the exact two-dimensional barrier and row leakage

Define the planar divergence-free subspace

\[
 \mathcal S_{2D}
 =\left\{
 (0,w_2(y,z),w_3(y,z)):
 \partial_yw_2+\partial_zw_3=0
 \right\}.
 \tag{6.1}
\]

The background (1.2), the R0.73F OS top vector, and its real conjugate pair
all belong to $\mathcal S_{2D}$.  The section must prove that this subspace is
invariant under the full nonlinear three-dimensional Navier--Stokes
equation.  Restricted to $\mathcal S_{2D}$, the equation is exactly the
two-dimensional incompressible Navier--Stokes equation in $(y,z)$.
Consequently, every smooth nonlinear orbit constructed in G3 is global and
smooth.  The selected row can support nonlinear transient amplification, but
it cannot by itself support three-dimensional vortex stretching or a
finite-time singularity.

For the positive physical row, write $x=2y$ and reconstruct the velocity
from a normalized wall-normal profile $v(x)$ as

\[
 u_v(y,z)
 =\left(0,v(2y),2iv'(2y)\right)e^{iz}.
 \tag{6.2}
\]

Direct calculation gives

\[
 (u_v\cdot\nabla)u_v
 =\left(0,0,
 4i\bigl(vv''-(v')^2\bigr)(2y)
 \right)e^{2iz}.
 \tag{6.3}
\]

For real data, the conjugate pair also generates the horizontal mean.  The
section must prove:

1. the one-row linear subspace is not invariant under the quadratic
   Navier--Stokes nonlinearity, although $\mathcal S_{2D}$ is invariant;
2. a frozen top eigenvector cannot be one of the exceptional two-frequency
   profiles for which the projected expression in (6.3) vanishes;
3. the generated physical $K_z=0,\pm2$ rows enter at order
   $\delta^2$, while feedback into the original row starts no earlier than
   cubic order.

This leakage does not contradict (5.6), because (5.3) controls all generated
modes together.  It does rule out an exact nonlinear reduction to the single
R0.73F row.

## 7. Mandatory false shortcuts

The final proof must reject each statement below.

1. **One unstable linear row is a nonlinear invariant subsystem.**  False by
   (6.3) and the conjugate-pair convolution.
2. **An exponentially large relative gain yields order-one departure for the
   seed allowed by the crude $H^3$ bootstrap.**  False as an inference:
   the sufficient seed ceiling may decay faster than
   $e^{-\kappa_D\Lambda}$.
3. **Family-level nonlinear relative amplification proves finite-time
   singularity.**  False: every solution constructed here is smooth on the
   stated window, and the exact planar invariant class is globally regular.

## 8. Claim boundary and next gate

Even if G1--G4 close, R0.73G will not prove:

- a $\Lambda$-uniform, order-one nonlinear departure from the decaying
  shear;
- a sharp bilinear evolution estimate tied to the R0.73F exponent;
- closure of all OS--Squire rows or a cascade through repeated triads;
- one fixed initial datum or one fixed background whose orbit becomes
  singular;
- failure of global regularity or the Clay problem.

The next gate must add a genuinely transverse perturbation with
$K_1\ne0$ or nonzero first velocity component and then replace the crude
$H^3$ energy envelope by a frequency-resolved bilinear evolution estimate.
Only that combination can test whether the unstable signal reaches an
order-one three-dimensional departure before nonlinear mode coupling changes
the mechanism.
