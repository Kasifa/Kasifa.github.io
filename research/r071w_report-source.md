# R0.71W -- An amplitude-doped exact 2.5D sequence defeats the complete first-row Leray ledger

**Date:** 2026-08-26

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, Fourier-shell observables, temporal zero sampling,
and normalized Leray--Lamb budgets

**Status:** release source.  This report proves a data-uniform no-go theorem
for the complete first-row zero-atom ledger left open in R0.71V.  The
construction is a sequence of exact, globally smooth, unforced periodic
three-dimensional Navier--Stokes solutions in a triangular 2.5D invariant
class.  A uniform rescaled implicit-function theorem produces the same two
prescribed simple roots while the seed, shear, and a decoupled background are
amplitude doped.  One fixed-shell atom diverges, the enstrophy ratio remains
bounded, and the complete projected rotational charge tends to zero.  The
price is unbounded initial energy and enstrophy.  Consequently the result
rules out a **data-independent** complete first-row ledger; it does not rule
out estimates whose constants depend sufficiently on the initial data.  It
does not prove a singularity, global regularity, a continuation criterion,
novelty, or priority.

## 0. Direct decision

On a fixed interval \(I=[a,b]\) of length \(\ell\), write

\[
 Y(t)=\|\omega(t)\|_2^2,
 \qquad
 L(t)=\mathbb P(u\times\omega)(t),
 \qquad
 \mathcal R_Y(I)=\frac{\sup_IY}{\inf_IY}.
 \tag{0.1}
\]

The complete first-row Leray ledger left open by R0.71V is

\[
 \Lambda_1(I;u)
 =\mathcal R_Y(I)\left[
 \nu^2+\frac1\ell\int_I
 \frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)}\,dt
 \right].
 \tag{0.2}
\]

It is the quantity obtained by inserting the R0.71U first-time-jet payment
into the zero-sampling theorem and deleting the second-time row.  The fixed
\(\nu^2\) term is essential: the bounded-data diagonal in R0.71V does not
defeat it.

R0.71W gives a different exact diagonal.  Fix one compact annular multiplier
\(T_*\), one target eigenshell, one macroscopic interval \(I\), and two
positive rescaled root times.  For every

\[
 1<\alpha<2
 \tag{0.3}
\]

there is a sequence \(u_q\) of smooth global unforced NSE solutions and a
prescribed \(m=2\) root \(t_{2,q}\in I\) such that, with

\[
 \mathscr A_q=q^\alpha,
 \tag{0.4}
\]

\[
 \boxed{
 J_{*,2,q}\asymp\frac{\mathscr A_q^2}{q^2}
 =q^{2\alpha-2}\longrightarrow\infty,}
 \tag{0.5}
\]

\[
 \boxed{
 1\le\mathcal R_{Y_q}(I)\le C,
 \qquad
 \frac1\ell\int_I
 \frac{\|L_q\|_{\dot H^{-1}}^2}{Y_q}\,dt
 \le C\frac{\mathscr A_q^2}{q^4}
 =Cq^{2\alpha-4}\longrightarrow0.}
 \tag{0.6}
\]

Therefore

\[
 \boxed{
 \frac{J_{*,2,q}}{\Lambda_1(I;u_q)}
 \longrightarrow\infty.}
 \tag{0.7}
\]

There is no constant depending only on the fixed annular geometry,
viscosity, and interval such that the sum of positive fixed-shell atoms of
every smooth unforced solution is bounded by that constant times (0.2).  A
singleton shell and a single separately selected root already fail.

The data are not uniformly bounded:

\[
 \|u_q(\sigma_q)\|_2^2+\|\omega_q(\sigma_q)\|_2^2
 \asymp \mathscr A_q^2q^2=q^{2\alpha+2}.
 \tag{0.8}
\]

Thus (0.7) is a no-go for a data-uniform ledger, not a no-go for every
data-dependent estimate.  In particular, it does not contradict the
bounded-energy/enstrophy statements in R0.71U--V.

## 1. The candidate ledger and why the old diagonal is absorbed

For compact real-even annular multipliers \(T_j\), put

\[
 W_j=T_j\omega,
 \qquad
 C_j=\operatorname{curl}W_j=-\Delta T_ju.
 \tag{1.1}
\]

R0.71U proves

\[
 \sum_j\kappa_j^{-6}\|C_{j,t}\|_2^2
 \le 2C_{\rm ann,T}
 \left(\nu^2Y+\|L\|_{\dot H^{-1}}^2\right).
 \tag{1.2}
\]

After division by \(Y\), integration over \(I\), and the inverse-window
factor from the Hilbert-valued sampling lemma, (1.2) produces (0.2), up to a
fixed annular constant.

At a positive root of one target eigenshell \(|k|=\rho_*\), the exact atom is

\[
 J_*(t_*)
 =\kappa_*^{-2}\rho_*^{-4}
 \frac{\|C_{*,t}(t_*)\|_2^2}{Y(t_*)}.
 \tag{1.3}
\]

R0.71V used a bounded-data diagonal in which the actual implicit-curve shear
amplitude \(s_q\) had to satisfy \(s_qq\to0\).  Its atom is

\[
 J_{*,q}\asymp s_q^2q^{-4}\longrightarrow0.
 \tag{1.4}
\]

The selected first-time row is still smaller, but the absolute global
\(\nu^2\) baseline in (0.2) absorbs (1.4).  A counterexample to (0.2) needs a
ratio tending to infinity, not merely a nonzero selected-row ratio.  The
amplitude-doped regime below retains a small **rescaled** implicit parameter
while allowing the physical shear amplitude to grow.

## 2. Exact triangular NSE class

Work on the normalized three-torus with coordinates \((x,y,z)\).  Let

\[
 u(x,y,z,t)=(f(y,z,t),0,v(y,t)).
 \tag{2.1}
\]

Then

\[
 \operatorname{div}u=0,
 \qquad
 (u\cdot\nabla)u=(vf_z,0,0),
 \tag{2.2}
\]

and the unforced three-dimensional NSE is exactly equivalent, with constant
pressure, to

\[
 \boxed{
 v_t=\nu v_{yy},
 \qquad
 f_t+vf_z=\nu(f_{yy}+f_{zz}).}
 \tag{2.3}
\]

The first equation is a finite Fourier heat flow.  The second is a linear
uniformly parabolic equation with smooth divergence-free drift.  Every
finite Fourier datum below therefore produces a global smooth unforced
three-dimensional NSE solution.  This is an exact invariant subclass, not a
forced passive-scalar surrogate.

The vorticity is

\[
 \omega=(v_y,f_z,-f_y).
 \tag{2.4}
\]

More importantly, projection removes all apparently large background
gradients:

\[
 u\times\omega
 =(-vf_z,vv_y+ff_y,ff_z)
 =(-vf_z,0,0)+\nabla_{y,z}\frac{v^2+f^2}{2}.
 \tag{2.5}
\]

Hence

\[
 \boxed{L=\mathbb P(u\times\omega)=(-vf_z,0,0).}
 \tag{2.6}
\]

Estimating the unprojected \(u\times\omega\) would introduce a spurious large
term from the background used below.  Identity (2.6) is therefore structural,
not cosmetic.

## 3. Fixed target, shrinking root layer, and amplitude doping

Fix integers \(K_y,K_z,Q,d\) with

\[
 K_z\ne0,
 \qquad Q>R_*,
 \qquad d>R_*+|K_y|,
 \tag{3.1}
\]

where \(R_*\) is the largest Fourier radius on which the fixed multiplier
\(T_*\) is nonzero.  The target is

\[
 k_*=(0,K_y,K_z),
 \qquad m_*(k_*)\ne0.
 \tag{3.2}
\]

Fix \(N\ge2\), numbers

\[
 0<A_0<\tau_1<\cdots<\tau_N,
 \tag{3.3}
\]

and pairwise distinct positive integers
\(r_1,\ldots,r_{2N+1}\).  For sufficiently large integer \(q\), set

\[
 n_{l,q}=dr_lq,
 \qquad
 \sigma_q=a-A_0q^{-2},
 \qquad
 t_{m,q}=\sigma_q+\tau_mq^{-2}.
 \tag{3.4}
\]

The root layer lies inside the fixed macroscopic interval \(I=[a,b]\).

Choose an amplitude exponent \(1<\alpha<2\) and put

\[
 \mathscr A_q=q^\alpha,
 \qquad
 \delta_q=\frac{\mathscr A_q}{q^2}=q^{\alpha-2}\longrightarrow0.
 \tag{3.5}
\]

The shear is

\[
 v_q(y,\theta)
 =\mathscr A_q\sum_{l=1}^{2N+1}z_{l,q}
 e^{-\nu n_{l,q}^2\theta}
 \left(e^{in_{l,q}y}+e^{-in_{l,q}y}\right),
 \qquad \theta=t-\sigma_q.
 \tag{3.6}
\]

The active scalar seed is

\[
 f_{q}^{\rm act}(y,z,0)
 =\mathscr A_q\sum_{l=1}^{2N+1}
 \left(A_l e^{i((K_y-n_{l,q})y+K_zz)}
 +\overline{A_l}e^{-i((K_y-n_{l,q})y+K_zz)}\right),
 \tag{3.7}
\]

with the two fixed phase classes

\[
 A_l=i\quad(1\le l\le N+1),
 \qquad
 A_l=1\quad(N+2\le l\le2N+1).
 \tag{3.8}
\]

Finally add the \(z\)-independent background

\[
 f_{b,q}(y,\theta)
 =B_qe^{-\nu Q^2\theta}(e^{iQy}+e^{-iQy}),
 \qquad
 B_q=b_0\mathscr A_qq,
 \qquad b_0>0.
 \tag{3.9}
\]

Because \((f_{b,q})_z=0\), it solves heat independently, is never coupled by
\(v f_z\), never enters the target annulus, and does not enter \(L\).

The active support stays in the two cosets

\[
 (K_y+dq\mathbb Z,K_z),
 \qquad
 (-K_y+dq\mathbb Z,-K_z),
 \tag{3.10}
\]

while the shear lies in \((dq\mathbb Z,0)\) and the background stays at
\((\pm Q,0)\).  For large \(q\), the intersection with the fixed multiplier
support is exactly the conjugate target pair \(\{\pm k_*\}\).  Thus zeroing
the target coefficient zeros the entire declared compact shell.

## 4. Uniform rescaled implicit-function theorem

The old pointwise-in-\(q\) implicit-function theorem is insufficient: it only
gives an unspecified radius for each \(q\).  The correct small parameter is
\(\delta_q=\mathscr A_q/q^2\), not the physical shear amplitude.

### 4.1 Scaled Fourier-lattice evolution

Consider the positive \(K_z\) sector and write

\[
 \widehat f_q^{\rm act}(K_y+dqr,K_z,\theta)
 =\mathscr A_q F_{q,r}(x),
 \qquad
 x=q^2\theta,
 \qquad r\in\mathbb Z.
 \tag{4.1}
\]

On \(H=\ell^2(\mathbb Z)\), \(F_q\) satisfies the exact equation

\[
 \partial_xF_q=D_qF_q+\delta V_z(x)F_q,
 \tag{4.2}
\]

where

\[
 (D_qF)_r
 =-\nu\left[
 \left(dr+\frac{K_y}{q}\right)^2
 +\frac{K_z^2}{q^2}\right]F_r,
 \tag{4.3}
\]

\[
 (V_z(x)F)_r
 =-iK_z\sum_{l=1}^{2N+1}z_l
 e^{-\nu d^2r_l^2x}
 \left(F_{r-r_l}+F_{r+r_l}\right).
 \tag{4.4}
\]

The initial vector has fixed finite support \(r=-r_l\) and coefficients
\(A_l\).  The semigroup \(S_q(x)=e^{xD_q}\) is a contraction, while on every
bounded \(z\)-ball

\[
 \|V_z(x)\|_{H\to H}\le C_R e^{-cx}.
 \tag{4.5}
\]

All \(D_q\) are self-adjoint and nonpositive on the common domain

\[
 \mathcal D=\left\{F\in\ell^2(\mathbb Z):
 \sum_{r\in\mathbb Z}(1+r^4)|F_r|^2<\infty\right\}.
 \tag{4.5a}
\]

The finite-shift operator \(V_z(x)\) is bounded and strongly continuous in
\(x\).  Thus (4.2) has the standard contraction-semigroup mild solution; the
proof below works entirely with that mild form.

### Lemma 4.1 -- uniform analytic evolution and target convergence

Fix \(X<\infty\) and \(R<\infty\).  The mild solution of (4.2) is analytic
in \((\delta,z)\) on

\[
 |\delta|\le\delta_0,
 \qquad |z|\le R,
 \tag{4.6}
\]

with every fixed finite order of parameter derivatives bounded independently
of all sufficiently large \(q\).  The target coefficient
\(P_0F_q(x)=F_{q,0}(x)\), its \(x\)-derivative at positive \(x\), and their
parameter derivatives through the order used below converge uniformly on
compact parameter sets to the corresponding \(q=\infty\) objects.  After
division by its exact factor \(\delta\), the target map used below is
uniformly \(C^2\) in \((\delta,z)\).

#### Proof

Duhamel iteration gives the Dyson series

\[
\begin{aligned}
 F_q(x)={}&S_q(x)F_0\\
 &+\sum_{n\ge1}\delta^n
 \int_{0<s_n<\cdots<s_1<x}
 S_q(x-s_1)V_z(s_1)S_q(s_1-s_2)V_z(s_2)\cdots\\
 &\hspace{8em}\cdots S_q(s_{n-1}-s_n)V_z(s_n)S_q(s_n)F_0\,ds.
\end{aligned}
 \tag{4.7}
\]

Contraction of \(S_q\) and (4.5) bound the \(n\)-th term by

\[
 \frac{(C_R|\delta|)^n}{n!}\|F_0\|_H.
 \tag{4.8}
\]

The same factorial majorant, with only polynomial factors in \(n\), controls
every fixed finite number of parameter derivatives.  This proves uniform
analyticity and the stated bounds without differentiating the unbounded
generators \(D_q\).

Write the integral coefficient of \(\delta^n\) in (4.7) as
\(\mathcal T_{q,n}(x;z)\).  It is a continuous homogeneous polynomial of
degree \(n\) in \(z\).  Since the unperturbed heat flow preserves the
nonzero initial lattice indices,

\[
 P_0S_q(x)F_0=0.
 \tag{4.8a}
\]

Consequently the target has the exact analytic factorization

\[
 P_0F_q(x;\delta,z)
 =\delta\sum_{n\ge1}\delta^{n-1}
 P_0\mathcal T_{q,n}(x;z).
 \tag{4.8b}
\]

After division by \(\delta\), derivatives through order two in
\((\delta,z)\) introduce only polynomial factors in \(n\).  The factorial
majorant (4.8) still converges uniformly, including at \(\delta=0\).  This
proves the asserted uniform \(C^2\) bound for the divided target map and, in
particular, a uniform Lipschitz constant for its \(z\)-Jacobian.

For each fixed lattice index,

\[
 S_q(x)e_r\longrightarrow
 S_\infty(x)e_r,
 \qquad
 (D_\infty F)_r=-\nu d^2r^2F_r,
 \tag{4.9}
\]

uniformly for \(x\in[0,X]\).  A finite-support approximation followed by
contraction gives strong semigroup convergence on \(H\), uniformly on that
compact interval.  Every fixed-order Dyson term starting from \(F_0\) has
finite lattice support after finitely many shifts, so the whole term
converges in \(H\), uniformly on its integration simplex.  First truncate
(4.7) in Dyson order, pass \(q\to\infty\) term by term, and then use (4.8)
to remove the truncation.  Hence \(F_q\to F_\infty\) in
\(C([0,X];H)\).  The same argument applies to parameter derivatives and,
using (4.8b), to derivatives of the divided target map.

No unbounded-generator derivative is needed for the target \(x\)-derivative.
The \(r=0\) component of (4.2) is

\[
 \partial_xF_{q,0}
 =-\nu\frac{K_y^2+K_z^2}{q^2}F_{q,0}
 +\delta P_0V_z(x)F_q.
 \tag{4.10}
\]

The right side contains only bounded projection and shift operations, so the
already established convergence proves the final assertion. \(\square\)

### 4.2 Divided target map

For \(m=1,\ldots,N\), define the real target map

\[
 \mathcal G_q(\delta,z)
 =\delta^{-1}
 \left(\operatorname{Re}F_{q,0}(\tau_m),
 \operatorname{Im}F_{q,0}(\tau_m)\right)_{m=1}^N.
 \tag{4.11}
\]

At \(\delta=0\), use the first Dyson coefficient to define the analytic
extension.  Factorization (4.8b) and Lemma 4.1 show that (4.11) is uniformly
\(C^2\) near \(\delta=0\), with a \(q\)-independent Lipschitz bound for its
\(z\)-Jacobian.

Fix \(z_1=1\).  At \(\delta=0\), the equations

\[
 \mathcal G_q(0,z)=0
 \tag{4.12}
\]

are linear in the remaining \(2N\) real variables.  Their real and imaginary
blocks are the response-evaluation matrices generated by

\[
 q^2e^{-\mu x/q^2}
 \frac{1-e^{-\beta_{l,q}x/q^2}}{\beta_{l,q}},
 \qquad
 \beta_{l,q}=2\nu n_{l,q}(n_{l,q}-K_y).
 \tag{4.13}
\]

They converge to

\[
 \Psi_l(x)=\frac{1-e^{-b_lx}}{b_l},
 \qquad
 b_l=2\nu d^2r_l^2.
 \tag{4.14}
\]

Distinct exponentials form an extended Chebyshev system.  Consequently the
two limiting \(N\)-by-\(N\) phase blocks are invertible.  The unique solutions
\(c_q\) of (4.12) converge to a finite \(c_\infty\), and the inverse Jacobian
norms are uniformly bounded.  The imaginary block is homogeneous, so in the
real-coordinate ordering used here
\((c_q)_{N+2:2N+1}=0\), and the same is true of \(c_\infty\).

### Theorem 4.2 -- uniform exact prescribed roots

There are numbers \(q_0,\delta_0,C>0\), independent of \(q\ge q_0\), and
smooth coefficient curves

\[
 z_q:(-\delta_0,\delta_0)\to\mathbb R^{2N+1},
 \qquad (z_q)_1=1,
 \tag{4.15}
\]

such that

\[
 \mathcal G_q(\delta,z_q(\delta))=0,
 \qquad
 |z_q(\delta)-c_q|\le C|\delta|,
 \qquad
 \sup_{q,|\delta|<\delta_0}|z_q(\delta)|\le C.
 \tag{4.16}
\]

Moreover every prescribed root is simple for all sufficiently large \(q\)
when \(0<|\delta|<\delta_0\).

#### Proof

Lemma 4.1 gives a uniform bound on the \(z\)-Lipschitz variation of
\(D_z\mathcal G_q\).  The Jacobians at \((0,c_q)\) have uniformly bounded
inverses.  Uniform control of \(\partial_\delta\mathcal G_q\) also gives
\(|\mathcal G_q(\delta,c_q)|\le C|\delta|\).  Choose a fixed ball on which the Newton map based at
\((0,c_q)\) is a contraction, uniformly in \(q\).  The parameter-dependent
contraction theorem then gives both the fixed point and
\(|z_q(\delta)-c_q|\le C|\delta|\), hence (4.15)--(4.16).  This is the quantitative
finite-dimensional implicit-function theorem, with constants supplied by
these uniform bounds.

Let

\[
 \Gamma(x)=K_z\sum_{l=1}^{N+1}c_l^\infty
 \frac{1-e^{-b_lx}}{b_l}.
 \tag{4.17}
\]

The Chebyshev zero count shows

\[
 \Gamma(\tau_m)=0,
 \qquad
 \Gamma'(\tau_m)\ne0.
 \tag{4.18}
\]

Taylor expansion of the uniformly analytic target path, evaluated along
\(z=z_q(\delta)\), gives

\[
 F_{q,0}(x)
 =\delta\left[\Gamma(x)+o_{q\to\infty}(1)+O(\delta)\right]
 \tag{4.19}
\]

in \(C_x^1\) near the finite set of prescribed roots.  Thus its \(x\)-slope
at every exact root is nonzero for large \(q\). \(\square\)

For R0.71W take \(\delta=\delta_q\).  The physical shear coefficients are

\[
 p_{l,q}=\mathscr A_q(z_q(\delta_q))_l,
 \qquad |p_{l,q}|\le C\mathscr A_q.
 \tag{4.20}
\]

Unlike the R0.71V diagonal, the physical amplitudes grow.  The scaled
interaction \(p/q^2=O(\delta_q)\) still tends to zero, which is exactly what
the uniform theorem requires.

## 5. Exact root slope and atom lower bound

Let

\[
 a_q(t)=\widehat f_q(K_y,K_z,t).
 \tag{5.1}
\]

At \(t=t_{m,q}\), Theorem 4.2 gives \(a_q=0\).  Equations (4.1), (4.10), and
(4.19) give

\[
\begin{aligned}
 \partial_ta_q(t_{m,q})
 &=\mathscr A_qq^2
 \partial_xF_{q,0}(\tau_m)\\
 &=\mathscr A_qq^2\delta_q
 \left[\Gamma'(\tau_m)+o_{q\to\infty}(1)+O(\delta_q)\right]\\
 &=\mathscr A_q^2
 \left[\Gamma'(\tau_m)+o(1)\right].
\end{aligned}
 \tag{5.2}
\]

Hence

\[
 c\mathscr A_q^2
 \le|\partial_ta_q(t_{m,q})|
 \le C\mathscr A_q^2.
 \tag{5.3}
\]

The modular isolation in (3.10) makes the complete target annulus a single
fixed eigenshell.  At its root, target diffusion vanishes and the filtered
rotational coefficient equals \(a_{q,t}\) up to the fixed nonzero multiplier
and eigenshell factors.  Formula (1.3) therefore gives

\[
 J_{*,m,q}\asymp\frac{\mathscr A_q^4}{Y_q(t_{m,q})}.
 \tag{5.4}
\]

It remains only to determine \(Y_q\).

## 6. Uniform enstrophy ratio without exponential Gronwall loss

The background contribution is

\[
 Y_{b,q}(t)
 =2Q^2B_q^2e^{-2\nu Q^2(t-\sigma_q)}.
 \tag{6.1}
\]

Because \(I\) is fixed and \(B_q=b_0\mathscr A_qq\),

\[
 c\mathscr A_q^2q^2
 \le Y_{b,q}(t)
 \le C\mathscr A_q^2q^2
 \qquad(t\in I).
 \tag{6.2}
\]

This is the lower enstrophy floor.  The upper bound must include every
nonlinear scalar mode, not only the target.

Let \(g=f_q^{\rm act}{}_z\).  Since \(v\) is independent of \(z\),

\[
 g_t+vg_z=\nu\Delta g.
 \tag{6.3}
\]

The divergence-free energy identity yields

\[
 \sup_{t\ge\sigma_q}\|g(t)\|_2
 \le\|g(\sigma_q)\|_2
 \le C\mathscr A_q.
 \tag{6.4}
\]

For \(h=f_q^{\rm act}{}_y\), differentiation gives

\[
 h_t+vh_z+v_yg=\nu\Delta h.
 \tag{6.5}
\]

Taking the \(L^2\) norm, rather than applying a squared-norm Gronwall
estimate, gives

\[
 \|h(t)\|_2
 \le\|h(\sigma_q)\|_2
 +\sup_s\|g(s)\|_2
 \int_{\sigma_q}^t\|v_y(s)\|_\infty\,ds.
 \tag{6.6}
\]

The finite heat-mode shear and (4.20) satisfy

\[
 \int_{\sigma_q}^\infty\|v_y(s)\|_\infty\,ds
 \le C\sum_l\frac{|p_{l,q}|}{n_{l,q}}
 \le C\frac{\mathscr A_q}{q}.
 \tag{6.7}
\]

Since \(\|h(\sigma_q)\|_2\le C\mathscr A_qq\),

\[
 \|h(t)\|_2
 \le C\left(\mathscr A_qq+\frac{\mathscr A_q^2}{q}\right)
 =C\mathscr A_qq(1+\delta_q)
 \le C\mathscr A_qq.
 \tag{6.8}
\]

The shear itself obeys

\[
 \|v_y(t)\|_2\le C\mathscr A_qq.
 \tag{6.9}
\]

The background, active \(K_z\)-sector, and shear are Fourier orthogonal.
Combining (2.4), (6.2), (6.4), (6.8), and (6.9) proves

\[
 \boxed{
 c\mathscr A_q^2q^2
 \le Y_q(t)
 \le C\mathscr A_q^2q^2
 \quad(t\in I),
 \qquad
 \mathcal R_{Y_q}(I)\le C.}
 \tag{6.10}
\]

Substitution into (5.4) gives

\[
 \boxed{
 J_{*,m,q}\asymp\frac{\mathscr A_q^2}{q^2}.}
 \tag{6.11}
\]

Because \(\alpha>1\), every prescribed atom diverges.  One atom is enough
for the no-go theorem; \(N=2\) keeps the recurrence boundary from being
confused with a first-sample artifact.

## 7. Complete projected rotational charge

The exact identity (2.6) and the \(z\)-independence of the background give

\[
 L_q=(-v_qf_{q,z}^{\rm act},0,0).
 \tag{7.1}
\]

Every term in \(v_qf_{q,z}^{\rm act}\) has nonzero \(z\)-frequency \(K_z\),
so it has zero mean and

\[
 \|L_q(t)\|_{\dot H^{-1}}
 \le C_{K_z}\|v_q(t)f_{q,z}^{\rm act}(t)\|_2
 \le C\|v_q(t)\|_\infty
 \|f_{q,z}^{\rm act}(t)\|_2.
 \tag{7.2}
\]

The complete heat-mode shear, including all diagonal and off-diagonal
products, satisfies

\[
 \int_{\sigma_q}^\infty\|v_q(t)\|_\infty^2\,dt
 \le C\frac{\mathscr A_q^2}{q^2}.
 \tag{7.3}
\]

Using (6.4), (6.10), and (7.3),

\[
\begin{aligned}
 \frac1\ell\int_I
 \frac{\|L_q\|_{\dot H^{-1}}^2}{Y_q}\,dt
 &\le
 \frac{C}{\ell\mathscr A_q^2q^2}
 \left(\sup_I\|f_{q,z}^{\rm act}\|_2^2\right)
 \int_I\|v_q\|_\infty^2\,dt\\
 &\le C\frac{\mathscr A_q^2}{q^4}.
\end{aligned}
 \tag{7.4}
\]

This is a full-frequency estimate.  It does not discard target-complement
interactions and does not estimate only a selected shell.  Since
\(\alpha<2\), its right side tends to zero.

## 8. Complete first-row no-go theorem

### Theorem 8.1 -- failure of the data-uniform complete Leray ledger

Fix \(\nu>0\), a compact macroscopic interval \(I\), and a compact real-even
annular multiplier \(T_*\) satisfying the fixed target assumptions above.
For every \(1<\alpha<2\), there is a sequence of exact smooth global unforced
three-dimensional NSE solutions \(u_q\) and two prescribed simple positive
target-shell roots in \(I\) such that

\[
 J_{*,2,q}\asymp q^{2\alpha-2},
 \qquad
 \mathcal R_{Y_q}(I)\le C,
 \qquad
 \frac1\ell\int_I
 \frac{\|L_q\|_{\dot H^{-1}}^2}{Y_q}\,dt
 =O(q^{2\alpha-4}).
 \tag{8.1}
\]

Consequently

\[
 \frac{J_{*,2,q}}
 {\mathcal R_{Y_q}(I)\left[
 \nu^2+\ell^{-1}\int_I\|L_q\|_{\dot H^{-1}}^2/Y_q\,dt
 \right]}
 \longrightarrow\infty.
 \tag{8.2}
\]

There is therefore no data-independent constant \(C_*\) for which every
smooth unforced solution satisfies

\[
 \sum_{t_*\in Z_*^+(I)}J_*(t_*)
 \le C_*\mathcal R_Y(I)\left[
 \nu^2+\frac1\ell\int_I
 \frac{\|L\|_{\dot H^{-1}}^2}{Y}\,dt
 \right].
 \tag{8.3}
\]

#### Proof

Theorem 4.2 produces exact roots and (5.2) their nondegenerate slopes.
Modular isolation makes them complete target-shell roots.  Equations (6.10)
and (6.11) give the atom and enstrophy ratio.  Equation (7.4) gives the full
rotational charge.  The two inequalities in (0.3) make the numerator diverge
and the nonconstant part of the denominator vanish, while \(\nu^2\) stays
fixed.  This proves (8.2).  The left side of (8.3) is at least its second
prescribed atom, so (8.3) cannot hold. \(\square\)

### 8.1 Data dependence that remains possible

The background gives

\[
 D_q:=\|u_q(\sigma_q)\|_2^2+
 \|\omega_q(\sigma_q)\|_2^2
 \asymp q^{2\alpha+2}.
 \tag{8.4}
\]

Along this family,

\[
 J_{*,2,q}\asymp
 D_q^{(\alpha-1)/(\alpha+1)}.
 \tag{8.5}
\]

As \(\alpha\uparrow2\), the exponent approaches \(1/3\) from below.  Thus
the family also defeats any proposed polynomial data prefactor \(D^\beta\)
with a fixed \(\beta<1/3\), after choosing \(\alpha\) sufficiently close to
two.  It does not rule out the endpoint \(D^{1/3}\), a larger data
dependence, or a structurally different payment.

## 9. Why a shrinking observation interval does not replace the background

One might try to remove the large background and observe only a
\(q^{-2}\)-length root layer.  That changes the ledger itself.  The factor
\(\ell^{-1}\) then contributes \(q^2\), so the rotational payment returns to
the same scale as the atom.  The fixed macroscopic window and the decoupled
background are therefore not interchangeable devices.  R0.71W tests the
candidate exactly in the fixed-window form in which it was left open.

## 10. Literature boundary

The surrounding ingredients are standard and were checked against primary
or authoritative sources:

1. [Leray (1934)](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/5537-11511_2006_Article_BF02547354.pdf)
   supplies the foundational weak-energy framework for three-dimensional
   NSE.  It does not state a fixed-zero quadratic trace theorem.
2. [Temam, *Navier--Stokes Equations*](https://doi.org/10.1137/1.9781611970050)
   records the functional and semigroup framework used around the Leray
   energy inequality.  The rescaled Fourier-lattice IFT here is proved
   directly rather than attributed to that source.
3. [Linkmann--Buzzicotti--Biferale
   (2018)](https://doi.org/10.1140/epje/i2018-11612-1) records the standard
   2D3C reduction.  It does not contain the prescribed-root or
   amplitude-doped no-go theorem.
4. [Federer, *Geometric Measure
   Theory*](https://doi.org/10.1007/978-3-642-62010-2),
   [Bertoin--Yor](https://arxiv.org/abs/1307.1288), and
   [\L{}ochowski](https://arxiv.org/abs/1503.01746) support the area,
   occupation, and crossing background used in R0.71V.  Those results are
   level integrated and do not provide the distinguished fixed-zero
   quadratic trace rejected here.

A bounded primary-source search did not locate a deterministic theorem that
converts only the normalized Leray first row into the data-uniform fixed-zero
atom sum in (8.3), nor a published statement of the exact amplitude-doped
triangular countersequence above.  This is a search boundary, not a claim of
novelty, priority, or nonexistence.

## 11. Computational audit

The producer certificate performs two separate checks.

1. It reconstructs the fixed-target Chebyshev interpolation at 90 digits,
   sweeps the seed/background balance, and verifies that the old tangent
   coefficient divided by the \(\mathcal R_Y\nu^2\) baseline is
   \(O(q^{-2})\).  This prevents the old coefficient from being confused with
   the physical amplitude-doped atom.
2. It restores \(\mathscr A_q=q^{3/2}\), includes the heat/tangent shear in
   the enstrophy proxy, and evaluates a deterministic full-frequency
   rotational upper bound.  The fitted powers are

\[
 \delta_q:q^{-1/2},
 \qquad
 J_{\rm proxy}:q^{1},
 \qquad
 \mathcal L_{\rm rot}^{\rm upper}:q^{-1},
 \qquad
 Y_{\rm proxy}:q^5.
 \tag{11.1}
\]

An independent binary64 program rebuilds the response, logarithmic heat
enstrophy, restored shear, rotational bound, and power fits without importing
the producer or its output.  The computation corroborates leading constants
and powers.  The continuum Dyson convergence, quantitative IFT, exact root
slope, and nonlinear enstrophy estimates are proved analytically in Sections
4--7; they are not inferred from finite computation.

## 12. Claim--evidence boundary

### Proved

1. A uniform rescaled Fourier-lattice implicit-function theorem for the
   prescribed roots.
2. Exact target-shell roots and root slopes of order
   \(\mathscr A_q^2\).
3. Full nonlinear enstrophy bounds
   \(Y_q\asymp\mathscr A_q^2q^2\) on the fixed interval.
4. The exact projected identity \(L=(-vf_z,0,0)\) and the full-frequency
   rotational bound \(O(\mathscr A_q^2/q^4)\).
5. Divergence of one fixed-shell atom relative to the complete first-row
   data-uniform Leray ledger.

### Not proved

1. Failure of estimates with arbitrary dependence on initial energy or
   enstrophy.
2. Sharpness of a \(D^{1/3}\) data prefactor.
3. Failure of the R0.71U second-time-jet theorem.
4. A weak-solution zero trace, a localized-cell theorem, or a
   single-trajectory infinite recurrence theorem.
5. A continuation criterion, finite-time singularity, or global regularity.
6. Novelty or priority relative to literature outside the bounded search.

## 13. Research value and next gate

R0.71W closes the exact question left by R0.71V: the fixed global
\(\nu^2\) baseline and the complete projected rotational term do **not**
rescue a data-uniform first-row fixed-zero ledger.  The obstruction is not
an artifact of an abstract time path, a selected-shell omission, pressure,
or an unspecified pointwise-in-\(q\) IFT radius.

The result is a rigorous route-pruning theorem, not progress toward a
singularity by itself.  It says that a successful replacement for the
R0.71U second-time row must contain at least one genuinely new ingredient:

1. explicit initial-data dependence of sufficient strength;
2. a persistence/noncollapse trace condition;
3. a stronger time-regularity charge;
4. or a different observable whose zero trace is not vulnerable to
   amplitude doping.

The next finite gate is R0.71X: test whether the data scale exposed in
(8.4)--(8.5) can be paid by a scale-compatible energy/enstrophy charge, and
determine whether the \(1/3\) boundary is structural or only a feature of
this triangular family.
