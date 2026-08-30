# R0.73G operator derivation: exact nonlinear perturbation and the first bootstrap boundary

**Date:** 2026-08-30  
**Parent input:** R0.73F moving-profile dichotomy  
**Scope:** the exact heat-decaying shear, a real perturbation built from the
\(\gamma=1/2,\ \beta=\xi=0\) row, and one fixed physical-time window  
**Evidence class:** exact Navier--Stokes algebra and Sobolev estimates; no
finite-dimensional diagnostic is used

## 0. Direct decision

I fix a concrete realization of the R0.73F family by taking viscosity
\(\nu=1\), carrier \(R=2\), phase \(\phi_*=0\), and positive
\(\Lambda=\lambda\to\infty\). This loses no feature of the permitted row:
\(K_z=1\) gives \(\gamma=K_z/R=1/2\), while \(K_x=r=0\) gives
\(\xi=\beta=0\).

There are three distinct conclusions.

1. The exact nonlinear perturbation equation and its mode convolution close
   without an additional hypothesis. The real \(K_z=\pm1\) row pair is
   **not** a nonlinear invariant space: its quadratic convolution has
   \(K_z=0,\pm2\) output channels.
2. A deliberately over-small seed

   \[
   \delta_\lambda=e^{-A\lambda}
   \tag{0.1}
   \]

   with a fixed sufficiently large \(A\), shadows the R0.73F growing linear
   orbit on a fixed window. The nonlinear gain ratio is still at least
   \(c e^{\kappa_*\lambda}\), but both the initial and final perturbations tend
   to zero. This is a closed perturbative amplification statement, not an
   order-one nonlinear instability.
3. The natural seed \(\delta_\lambda\asymp e^{-\kappa_*\lambda}\), for which the
   linear endpoint is order one, does not close from the R0.73F inputs. The
   missing item is a harmonic-resolved tame estimate for the mode-convolution
   response. The available all-row upper exponent and the one-row lower
   exponent do not provide that estimate.

There is also an exact negative boundary. The real R0.73F seed belongs to
the invariant subspace

\[
 {\cal X}_{2D}
 =\{(0,u_2(y,z),u_3(y,z)):\partial_yu_2+\partial_zu_3=0\}.
\tag{0.2}
\]

The nonlinear evolution stays in \({\cal X}_{2D}\). Its vorticity stretching
is identically zero, and the resulting solution is a globally regular
two-dimensional Navier--Stokes solution. Direct nonlinearization of this
seed therefore cannot produce a three-dimensional singularity.

## 1. Exact background and fixed window

Put

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
 \qquad W_d=W_{xx}.
\tag{1.1}
\]

On \(\mathbb T^3_{2\pi}\), with coordinates \(X=(x_1,y,z)\), define

\[
 d=4t,\qquad
 U_\lambda^b(t,y)=2\lambda W(4t,2y)e_3.
\tag{1.2}
\]

Because \(\partial_tW(4t,2y)=\partial_y^2W(4t,2y)\), and because the shear
has no \(z\)-dependence, \(U_\lambda^b\) is an exact unforced Navier--Stokes
solution.

Let \(d_0,\alpha,\eta,K_1\) be the constants in R0.73F. I fix

\[
 D_*=\frac{d_0}{2},\qquad
 T_*=\frac{D_*}{4}=\frac{d_0}{8},\qquad
 \kappa_*=(\alpha+\eta)D_*>0.
\tag{1.3}
\]

The dimensional time \(T_*\) and the slow time \(D_*\) are independent of
\(\lambda\). The number \(D_*\) is existential because the inherited
dichotomy constants are existential; it is nevertheless one fixed positive
number after the R0.73F constants have been selected.

The exact profile derivative and its primitive are

\[
 \|W_x(d)\|_\infty=\frac12(e^{-d}+e^{-4d}),
\tag{1.4}
\]

\[
 K(r,d)=\int_r^d\|W_x(\tau)\|_\infty\,d\tau
 =\frac12(e^{-r}-e^{-d})+\frac18(e^{-4r}-e^{-4d}).
\tag{1.5}
\]

## 2. Exact nonlinear perturbation equation

Write a full real solution in physical velocity variables as

\[
 U=U_\lambda^b+v,
 \qquad \nabla\cdot v=0.
\tag{2.1}
\]

Subtracting the equation for the background from the full Navier--Stokes
equation gives

\[
 \boxed{
 \partial_tv+2\lambda W(4t,2y)\partial_zv
 +4\lambda W_x(4t,2y)v_2e_3
 +(v\cdot\nabla)v+\nabla p
 =\Delta v,\qquad \nabla\cdot v=0.}
\tag{2.2}
\]

The two linear coefficients are exact:

\[
 U_\lambda^b\cdot\nabla
 =2\lambda W(4t,2y)\partial_z,\qquad
 v\cdot\nabla U_\lambda^b
 =4\lambda W_x(4t,2y)v_2e_3.
\tag{2.3}
\]

Taking the divergence of (2.2) also fixes the nonlinear pressure:

\[
 \Delta p
 =-8\lambda W_x(4t,2y)\partial_zv_2
 -\partial_i\partial_j(v_iv_j).
\tag{2.4}
\]

Let \(\mathbb P\) be the Leray projection on the full torus. Define

\[
 L_\lambda(t)v
 =\Delta v-\mathbb P\left(
 2\lambda W(4t,2y)\partial_zv
 +4\lambda W_x(4t,2y)v_2e_3\right).
\tag{2.5}
\]

Then the exact equation is

\[
 \boxed{\partial_tv=L_\lambda(t)v-\mathbb P(v\cdot\nabla v).}
\tag{2.6}
\]

For comparison with the R0.73F normalization, put
\(v=2\lambda w\) and \(d=4t\). Equation (2.2) becomes

\[
 \partial_dw+\frac{\lambda}{2}W(d,2y)\partial_zw
 +\lambda W_x(d,2y)w_2e_3
 +\frac{\lambda}{2}(w\cdot\nabla)w+\nabla\Pi
 =\frac14\Delta w.
\tag{2.7}
\]

Thus the \(\lambda/2\) multiplying the relative nonlinear term is only a
change-of-amplitude factor; the physical perturbation equation (2.6) has
the standard coefficient one.

The linear operator in (2.5), restricted to

\[
 {\cal S}_+=\{(K_x,K_y,K_z)=(0,2n,1):n\in\mathbb Z\},
\tag{2.8}
\]

is exactly the positive-sign R0.73F row. Its conjugate restriction to
\({\cal S}_-=-{\cal S}_+\) is the negative-sign row.

## 3. Exact Fourier convolution and row leakage

For \(k\ne0\), let

\[
 \mathbb P_k=I-\frac{k\otimes k}{|k|^2},
\tag{3.1}
\]

and put \(\mathbb P_0=I\). The nonlinear term in (2.6) has the exact
Fourier representation

\[
 \boxed{
 \widehat{{\cal N}(v,v)}(k)
 =-i\mathbb P_k
 \sum_{\ell+m=k}\bigl(\widehat v(\ell)\cdot m\bigr)\widehat v(m).}
\tag{3.2}
\]

The zero-mode sum vanishes for divergence-free data, so the convention for
\(\mathbb P_0\) is harmless.

The background shifts \(K_y\) only by \(\pm2,\pm4\), and preserves
\((K_x,K_z,K_y\bmod2)\). The quadratic term instead adds complete Fourier
labels. For a real seed in \({\cal S}_+\cup{\cal S}_-\),

\[
 {\cal S}_++{\cal S}_+\subset\{K_z=2\},\qquad
 {\cal S}_++{\cal S}_-\subset\{K_z=0\},\qquad
 {\cal S}_-+{\cal S}_-\subset\{K_z=-2\}.
\tag{3.3}
\]

Thus the assertion that the R0.73F row is nonlinearly invariant is false.
No linear direct-sum orthogonality removes (3.2).

This is not only a support possibility. For

\[
 u_f=(0,f(y),if'(y))e^{iz},\qquad
 f(y)=\cos2y+\cos4y,
\tag{3.4}
\]

one has \(\nabla\cdot u_f=0\), all input modes lie in \({\cal S}_+\), and

\[
 (u_f\cdot\nabla)u_f
 =\left(0,0,i\,[ff''-(f')^2]\right)e^{2iz},
\tag{3.5}
\]

\[
 ff''-(f')^2=-20-18\cos2y-2\cos6y.
\tag{3.6}
\]

The nonconstant \(y\)-dependence prevents (3.5) from being a pure gradient,
so its Leray projection is nonzero in the \(K_z=2\) channel. Adding the
complex conjugate makes the input real and supplies the conjugate
\(K_z=-2\) output. The \(K_z=0\) channel is allowed by (3.3), although it
can cancel for special profiles such as this real-valued \(f\).

There is, however, an exact \(K_z\)-parity split. Let \(v_o\) and \(v_e\)
be the sums of the odd and even \(K_z\) modes. Since the linear operator
preserves \(K_z\), (2.6) gives

\[
 \begin{aligned}
 \partial_tv_e={}&L_\lambda v_e-\mathbb P_e\mathbb P
 \bigl(v_o\cdot\nabla v_o+v_e\cdot\nabla v_e\bigr),\\
 \partial_tv_o={}&L_\lambda v_o-\mathbb P_o\mathbb P
 \bigl(v_o\cdot\nabla v_e+v_e\cdot\nabla v_o\bigr).
 \end{aligned}
 \tag{3.7}
\]

Starting from \(v_e(0)=0\), the even response begins at quadratic order,
while the correction to the odd target begins at cubic order. This exact
selection rule identifies the useful nonlinear remainder, but it does not
bound it.

## 4. Concrete Sobolev topology and a smooth growing seed

I use the real, mean-zero, divergence-free space

\[
 {\cal H}^3_\sigma
 =H^3_\sigma(\mathbb T^3_{2\pi};\mathbb R^3).
\tag{4.1}
\]

The choice \(3>5/2\) gives
\(H^3\hookrightarrow W^{1,\infty}\) and the standard estimate

\[
 \big|\langle D^3\mathbb P(v\cdot\nabla v),D^3v\rangle\big|
 \le C_{\rm nl}\|\nabla v\|_\infty\|v\|_{H^3}^2
 \le C_{\rm nl}\|v\|_{H^3}^3.
\tag{4.2}
\]

It remains necessary to show that the R0.73F maximizing direction can be
placed in this topology with controlled cost. Put

\[
 B_\varepsilon(0)=\widetilde A(0)-\varepsilon L,\qquad
 L=-\partial_x^2+\frac14,\qquad \varepsilon=\lambda^{-1}.
\tag{4.3}
\]

Choose an \(L^2_x\)-normalized eigenvector \(h_\varepsilon\) belonging to
the finite-dimensional top spectral subspace. Such an eigenvector exists
even when the top cluster is multiple. Its eigenvalue remains in the fixed
R0.73F contour. Since the finite-Fourier operator \(\widetilde A(0)\) is
bounded on every fixed \(H^r_x\), the eigenvalue equation gives, for
\(r=0,2\),

\[
 \varepsilon\|h_\varepsilon\|_{H^{r+2}_x}
 \le C_r\|h_\varepsilon\|_{H^r_x}.
\tag{4.4}
\]

Consequently, for all sufficiently large \(\lambda\),

\[
 \|h_\varepsilon\|_{H^2_x}\le C\lambda,\qquad
 \|h_\varepsilon\|_{H^4_x}\le C\lambda^2.
\tag{4.5}
\]

The exact kinetic-to-velocity map on the permitted row is

\[
 {\cal E}h
 =\left(0,\frac12L^{-1/2}h,
 i\partial_xL^{-1/2}h\right)(2y)e^{iz}.
\tag{4.6}
\]

It is divergence free, has \(u_1=0\), and is an \(L^2\) isometry. Define
the real vector

\[
 g_\lambda=2^{-1/2}\left({\cal E}h_\varepsilon
 +\overline{{\cal E}h_\varepsilon}\right).
\tag{4.7}
\]

Orthogonality of \(K_z=1\) and \(K_z=-1\), (4.5), and the order-zero
velocity reconstruction give

\[
 \boxed{\|g_\lambda\|_2=1,\qquad
 \|g_\lambda\|_{H^3}\le C_g\lambda^2.}
\tag{4.8}
\]

Let \(S_\lambda(t,s)\) denote the complete physical-time linear evolution
generated by \(L_\lambda(t)\). R0.73F applies to each conjugate half of (4.7),
so

\[
 \boxed{\|S_\lambda(T_*,0)g_\lambda\|_2
 \ge K_1^{-1}e^{\kappa_*\lambda}.}
\tag{4.9}
\]

## 5. A closed over-small nonlinear shadowing theorem

The statement in this section is deliberately weaker than order-one
instability. Its purpose is to mark exactly what already follows from the
R0.73F inputs and standard Sobolev calculus.

Because \(W(d,2y)\) has fixed finite Fourier support, there is a constant
\(a_3<\infty\), independent of \(\lambda\), such that the linear terms in
(2.2) satisfy the \(H^3\) commutator bound \(a_3\lambda\|v\|_{H^3}^2\).
Together with (4.2), there is \(b_3<\infty\), also independent of
\(\lambda\), such that every smooth solution of (2.6) satisfies

\[
 \frac12\frac d{dt}\|v\|_{H^3}^2
 +\|\nabla v\|_{H^3}^2
 \le a_3\lambda\|v\|_{H^3}^2
 +b_3\|v\|_{H^3}^3.
\tag{5.1}
\]

Here \(a_3\) may be taken as a universal \(H^3\) commutator constant
times

\[
 1+\sup_{0\le d\le D_*}\left(
 \|W(d,2\cdot)\|_{W^{4,\infty}}
 +\|W_x(d,2\cdot)\|_{W^{3,\infty}}\right),
\tag{5.2}
\]

which is explicit and finite from (1.1).

Put \(Y(t)=\|v(t)\|_{H^3}\). The standard regularization argument at a
zero of \(Y\) turns (5.1) into

\[
 Y'(t)\le a_3\lambda Y(t)+b_3Y(t)^2.
\tag{5.3}
\]

The complete linear energy estimate inherited from R0.73B is

\[
 \|S_\lambda(t,s)\|_{L^2_\sigma\to L^2_\sigma}
 \le \exp\left(\frac{\lambda}{2}K(4s,4t)\right),
 \qquad 0\le s\le t\le T_*.
\tag{5.4}
\]

For the initial data

\[
 v_\lambda(0)=\delta_\lambda g_\lambda,\qquad
 \delta_\lambda=e^{-A\lambda},
\tag{5.5}
\]

put

\[
 z_\lambda(t)=\delta_\lambda S_\lambda(t,0)g_\lambda,\qquad
 r_\lambda=v_\lambda-z_\lambda.
\tag{5.6}
\]

The exact mode-convolution remainder is

\[
 \boxed{
 r_\lambda(t)=-\int_0^t
 S_\lambda(t,\tau)\mathbb P
 (v_\lambda\cdot\nabla v_\lambda)(\tau)\,d\tau.}
\tag{5.7}
\]

Define the fixed exponent

\[
 M_*=\frac12K(0,D_*)+2a_3T_*.
\tag{5.8}
\]

Solving the scalar Riccati inequality (5.3) shows that

\[
 Y(0)\le\frac{a_3\lambda}{4b_3}e^{-a_3\lambda T_*}
 \quad\Longrightarrow\quad
 Y(t)\le2e^{a_3\lambda t}Y(0)
 \quad(0\le t\le T_*).
\tag{5.9}
\]

Since \(Y(0)\le C_g\lambda^2\delta_\lambda\), (5.9) closes for all
sufficiently large \(\lambda\) whenever \(A>a_3T_*\). The \(H^3\)
continuation criterion then supplies a strong solution through \(T_*\).
Equations (4.8), (5.4), (5.7), and (5.9) give

\[
 \boxed{
 \|r_\lambda(T_*)\|_2
 \le C_*T_*\lambda^4\delta_\lambda^2e^{M_*\lambda}.}
\tag{5.10}
\]

Choose once and for all

\[
 \boxed{
 A>A_*:=\max\left\{
 a_3T_*,\ M_*-\kappa_*,\ \kappa_*
 \right\}+1.}
\tag{5.11}
\]

The polynomial \(\lambda^4\) in (5.10) is absorbed by the strict exponential
margin. Equations (4.9)--(5.10) therefore imply, for every sufficiently
large \(\lambda\),

\[
 \boxed{
 \|v_\lambda(T_*)\|_2
 \ge \frac1{2K_1}\delta_\lambda e^{\kappa_*\lambda}.}
\tag{5.12}
\]

Since \(\|v_\lambda(0)\|_2=\delta_\lambda\), the nonlinear gain ratio
satisfies

\[
 \boxed{
 \frac{\|v_\lambda(T_*)\|_2}{\|v_\lambda(0)\|_2}
 \ge\frac1{2K_1}e^{\kappa_*\lambda}.}
\tag{5.13}
\]

\[
 \|v_\lambda(0)\|_{H^3}
 \le C_g\lambda^2e^{-A\lambda}\to0.
\tag{5.14}
\]

Moreover, (5.9) and \(A>a_3T_*\) show that the whole physical perturbation
orbit tends to zero uniformly in \(H^3\) on \([0,T_*]\). The theorem is
therefore an exponentially amplified shadowing orbit entirely inside a
vanishing neighborhood of the background. It is not an order-one
departure.

## 6. Why the natural bootstrap is still open

The natural linear seed is

\[
 \delta_\lambda^{\rm nat}=\delta e^{-\kappa_*\lambda},\qquad
 0<\delta\ll1.
\tag{6.1}
\]

Its initial \(H^3\) norm still tends to zero, while (4.9) gives an
endpoint of size at least \(\delta/K_1\) for the linearized equation. The
available estimate (5.10), however, becomes

\[
 \|r_\lambda(T_*)\|_2
 \le C_*T_*\lambda^4\delta^2
 \exp\left((M_*-2\kappa_*)\lambda\right).
\tag{6.2}
\]

R0.73F supplies no inequality

\[
 M_*<2\kappa_*.
\tag{6.3}
\]

The constant \(a_3\) in \(M_*\) comes from full Sobolev propagation,
whereas \(\kappa_*\) is a one-row \(L^2\) lower exponent. Neither the
R0.73F moving dichotomy nor the R0.73B upper sentinel compares those two
quantities. Thus (6.2) is not a closed natural-scale bootstrap.

The parity identity (3.7) shows the sharper object that is actually needed.
Let \(\Pi_{\rm tar}\) project onto
\({\cal S}_+\cup{\cal S}_-\). Since the first quadratic response is even,
a sufficient missing estimate is the following targeted cubic bound: there
exist \(\delta_0,C<\infty\), independent of large \(\lambda\), such that the
solution with \(0<\rho\le\delta_0e^{-\kappa_*\lambda}\) exists on
\([0,T_*]\) and obeys

\[
 \boxed{
 \|\Pi_{\rm tar}[v_\rho(T_*)-\rho S_\lambda(T_*,0)g_\lambda]\|_2
 \le C \rho^3e^{3\kappa_*\lambda}.}
\tag{6.4}
\]

Indeed, inserting \(\rho=\delta e^{-\kappa_*\lambda}\) into (6.4) gives a
target error \(C\delta^3\), while the linear target is at least
\(\delta/K_1\). A fixed sufficiently small \(\delta\) would then give an
order-one nonlinear departure.

Estimate (6.4) is not a formal consequence of row orthogonality. Its proof
requires, at minimum, tame fixed-window propagation for the even modes
\(K_z=0,\pm2\) created at second order and for the odd modes returned at
third order. A harmonic-resolved semigroup package with subadditive growth
rates, parabolic derivative recovery, and constants uniform in \(\lambda\)
would suffice. No such package is present in R0.73F. This is the minimal
operator estimate that should be tested next; a finite Fourier convolution
cannot certify it in the continuum.

## 7. Exact two-dimensional invariant boundary

The seed (4.7) satisfies

\[
 \partial_{x_1}g_\lambda=0,\qquad (g_\lambda)_1=0.
\tag{7.1}
\]

The background, pressure equation, viscosity, Leray projection, and
quadratic term all preserve these two identities. Therefore the exact
nonlinear solution generated by (4.7) stays in \({\cal X}_{2D}\), even
though it leaves the original \(K_z=\pm1\) rows.

Its three-dimensional vorticity has the form

\[
 \Omega=(\partial_yu_3-\partial_zu_2,0,0).
\tag{7.2}
\]

Hence

\[
 (\Omega\cdot\nabla)u=\Omega_1\partial_{x_1}u=0.
\tag{7.3}
\]

Equivalently, the perturbation scalar vorticity

\[
 \omega=\partial_yv_3-\partial_zv_2
\tag{7.4}
\]

satisfies the exact two-dimensional equation

\[
 \boxed{
 \partial_t\omega+2\lambda W(4t,2y)\partial_z\omega
 +8\lambda W_{xx}(4t,2y)v_2
 +v\cdot\nabla_{y,z}\omega
 =\Delta_{y,z}\omega.}
\tag{7.5}
\]

The quadratic transport in (7.5) is skew in \(L^2\). Standard
two-dimensional Navier--Stokes regularity gives a global smooth solution for
every smooth seed and every fixed \(\lambda\). Consequently:

- row leakage is real, but it is two-dimensional mode convolution;
- the direct R0.73F seed creates no vortex stretching;
- even a proof of order-one nonlinear instability for this seed would not be
  a blow-up mechanism or a Clay-problem result.

A genuinely three-dimensional next gate must add \(K_x\ne0\) or a nonzero
Squire component and control its coupling to the growing two-dimensional
orbit. That is a different operator problem from (6.4).

## 8. Three consistency verdicts for the main shadowing proof

### 8.1 Physical time and amplitude normalization: PASS

The physical background

\[
 \overline U_\Lambda(t,y)=2\Lambda W(4t,2y)e_3
\tag{8.1}
\]

is consistent with \(\nu=1,\ R=2,\ A_b=2\Lambda\). The R0.73F slow time is
\(d=R^2t=4t\), so its endpoint \(d_D=\min(D,d_0)\) is exactly the physical
time \(T_D=d_D/4\). Its lower exponent
\((\alpha+\eta)d_D\Lambda\) is therefore exactly
\(\kappa_D\Lambda\), with no missing factor four.

For the unscaled physical perturbation
\(v=U-\overline U_\Lambda\), the quadratic coefficient is one, as in
(2.6). For the relative perturbation \(w=v/(2\Lambda)\), the slow-time
coefficient is \(\Lambda/2\), as in (2.7). These are equivalent
normalizations. Mixing the physical perturbation with the relative
quadratic coefficient would be wrong; the main shadowing proof uses the
physical normalization consistently.

### 8.2 The \(H^3\) top-vector cost \(C_{\rm top}\Lambda^2\): PASS

The common R0.73F contour gives a uniform bound on the selected viscous top
eigenvalue. The finite-harmonic order-zero operator
\(\widetilde A(0)\) is bounded on \(H^m\) for fixed \(m\). Therefore

\[
 \varepsilon\|h_\varepsilon\|_{H^{m+2}}
 \le C_m\|h_\varepsilon\|_{H^m},
 \qquad m=0,2,
\tag{8.2}
\]

first gives \(H^2=O(\Lambda)\) and then \(H^4=O(\Lambda^2)\). The exact
kinetic velocity reconstruction (4.6) is order zero, and the fixed lift
\(x=2y,\ K_z=\pm1\) does not introduce a \(\Lambda\)-dependent factor.
Hence an \(L^2\)-unit real top vector satisfies
\(\|\phi_\Lambda\|_{H^3}\le C_{\rm top}\Lambda^2\).
The power two is non-sharp but valid and sufficient.

### 8.3 The stated seed ceiling implies half-gain: PASS

The first term of the main proof's seed ceiling,

\[
 \delta\le
 \frac{a}{4bC_{\rm top}}\Lambda^{-1}e^{-a\Lambda T_D},
\tag{8.3}
\]

and \(\|\phi_\Lambda\|_{H^3}\le C_{\rm top}\Lambda^2\) imply exactly

\[
 \|v(0)\|_{H^3}
 \le \frac{a\Lambda}{4b}e^{-a\Lambda T_D},
\tag{8.4}
\]

so the Riccati bootstrap applies. The second term,

\[
 \delta\le
 \frac{\Lambda^{-4}}{2K_1C_DC_{\rm top}^2}
 e^{-(M_D-\kappa_D)_+\Lambda},
\tag{8.5}
\]

implies

\[
 C_De^{M_D\Lambda}C_{\rm top}^2\Lambda^4\delta^2
 \le\frac1{2K_1}e^{\kappa_D\Lambda}\delta.
\tag{8.6}
\]

If \(M_D<\kappa_D\), use of the positive part in (8.5) is conservative and
still sufficient. Subtracting (8.6) from the R0.73F linear lower bound
\(K_1^{-1}e^{\kappa_D\Lambda}\delta\) gives the claimed half-gain. No
hidden extra factor of \(\Lambda\), \(2\), or \(4\) is needed.

## 9. Claim ledger

    exactNonlinearPerturbationEquationAroundR073FHeatShear=CLOSED
    exactFullFourierModeConvolutionFormula=CLOSED
    r073fGrowingDirectionHasPolynomialH3Cost=CLOSED
    fixedWindowExponentiallyOversmallShadowingBootstrap=CLOSED
    nonlinearGainRatioExpKappaLambdaForOversmallSeed=CLOSED

    singleR073FFourierRowIsNonlinearlyInvariant=FALSE
    directR073FRealSeedGeneratesThreeDimensionalVortexStretching=FALSE
    directR073FRealSeedCanYieldNavierStokesBlowup=FALSE

    naturalSeedOrderOneNonlinearDeparture=OPEN
    targetedCubicModeConvolutionEstimate=OPEN
    harmonicResolvedEvenOddPropagationPackage=OPEN
    genuinelyThreeDimensionalNonlinearInstability=OPEN
    nonlinearNavierStokesBlowup=OPEN
    Clay=OPEN

The first two FALSE entries are exact algebraic statements. The third is
an exact consequence of the invariant two-dimensional subspace and global
2D regularity. The OPEN natural-scale statement is not asserted false;
only its derivation from the present R0.73F inputs is unavailable.
