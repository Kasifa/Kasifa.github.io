# R0.74S Step 16 — independent audit of the moving-frame Taylor-vortex obstruction

## Status and audited object

This is an independent analytic audit of
`research/r074s_moving_frame_taylor_vortex_obstruction.md` as read at

```text
SHA256 de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0
```

The audit checks the frozen Version-M definitions, every displayed equation
(S.417)--(S.444), all signs and powers of \(R\), the complete payment rather
than a selected row, the negation of the quantifiers in (S.342), and the
primary-source boundary.  It makes no numerical or computer-assisted claim.

The main verdict is:

> **ANALYTIC PASS.**  The Taylor-vortex family is a smooth periodic exact
> solution and gives a genuine counterexample to (S.342) for every fixed
> \(p>1\) and every finite deletion budget.  The counterexample is caused by
> the Version-M moving-cutoff drift.  The fixed-frame kinetic and pressure
> fluxes cancel exactly.  No omitted payment row repairs the divergence.

The current frozen draft explicitly restricts the auxiliary payment exponent
in (S.438a) to \(\beta\ge0\), and its endpoint \(p=1\) lower law follows
directly by integrating the same positive terminal block.  No equation-level
correction remains.

## 1. Frozen definitions used in the audit

The audit uses the Version-M trajectory and flux exactly as frozen earlier:

\[
 \dot X_R=u_R(t,X_R),\qquad
 v_R(t,y)=u(t,y+X_R(t)),\qquad a_R=\dot X_R,
\]

and

\[
 \dot F_{k,R}(t)
 ={\gamma_k\over R}\eta_R(t)
 \int_{\mathbb T^3}
 \left[{1\over2}|v_R|^2(v_R-a_R)
       +(\pi_R-c_R)v_R\right]\cdot\nabla\Psi_k^R\,dy.
\]

The dimensionless density and common-deletion tail are

\[
 h_{k,R}(\sigma)=R^2
 |\dot F_{k,R}(s_R+R^2\sigma)|,
\]

\[
 \mathfrak H^F_{p,N,R}
 =\inf_{\#S\le N}\sum_{k\notin S}
   \|h_{k,R}\|_{L^p(0,4)}.
\]

The complete payment is

\[
 P_R^M
 =\mathcal E^{M,R}(z_0,8R)^{3/2}
  +\mathcal G_{v_R,\pi_R}^{M,R}(z_0,2R;1)
  +\mathcal H_{v_R}^{M,R}(z_0,2R).
\]

Thus a valid counterexample must survive the physical pressure, the
trajectory drift, all periodized copies, one deletion set chosen before the
time norm, and every nonnegative row in \(P_R^M\).  The main note does so.

## 2. Equation-by-equation audit

### 2.1 Equations (S.417)--(S.420): exact Navier--Stokes solution

For

\[
 W=(\sin x_1\cos x_2,-\cos x_1\sin x_2,0),
 \qquad
 p_W={\cos2x_1+\cos2x_2\over4},
\]

direct differentiation gives

\[
 \partial_1W_1+\partial_2W_2
 =\cos x_1\cos x_2-\cos x_1\cos x_2=0,
\]

and every nonzero Fourier mode has \(|n|^2=2\), hence

\[
 \Delta W=-2W.
\]

The two nonzero components of the convection are

\[
 (W\cdot\nabla)W_1=\sin x_1\cos x_1,
 \qquad
 (W\cdot\nabla)W_2=\sin x_2\cos x_2.
\]

On the other hand,

\[
 \nabla p_W=(-\sin x_1\cos x_1,-\sin x_2\cos x_2,0).
\]

This proves (S.418), including its sign.  With

\[
 b_A=Ae^{-2(t-t_0)},\qquad b_A'=-2b_A,
\]

one has

\[
 \partial_t(b_AW)-\Delta(b_AW)
 =(-2b_A+2b_A)W=0,
\]

while

\[
 (b_AW\cdot\nabla)(b_AW)+\nabla(b_A^2p_W)
 =b_A^2[(W\cdot\nabla)W+\nabla p_W]=0.
\]

Therefore (S.419)--(S.420) are exact.  The solution is smooth on every
finite time interval, has zero spatial mean, is unforced, and belongs to the
periodic suitable-weak/Leray class.  No amplitude-symmetry claim for a
general Navier--Stokes solution is used.

**Verdict for (S.417)--(S.420): PASS.**

### 2.2 Equations (S.421)--(S.423): mollifier and terminal trajectory

The field \(W\) is a linear combination of torus modes

\[
 n=(\pm1,\pm1,0),\qquad |n|=\sqrt2.
\]

For the fixed even radial mollifier,

\[
 \int_{\mathbb R^3}\varphi(z)e^{-iRn\cdot z}\,dz
 =\int_{\mathbb R^3}\varphi(z)
       \cos(Rn\cdot z)\,dz.
\]

Radiality makes this multiplier identical for all four modes.  The
normalization-free definition in (S.421), with \(n=(1,1,0)\), is therefore
correct.  Nonnegativity and unit mass give \(|\mu_R|\le1\), and dominated
convergence gives \(\mu_R\to1\).  Hence \(\mu_R\in[1/2,1]\) can be imposed by
choosing \(R\) sufficiently small.

At the terminal point \((\pi/4,0,0)\), uniqueness in the second equation

\[
 \dot\xi_2=-\mu_Rb_A\cos\xi_1\sin\xi_2
\]

and the identically zero third equation preserve \(\xi_2=\xi_3=0\).  The
remaining scalar ODE is

\[
 \dot\xi_1=\mu_Rb_A\sin\xi_1.
\]

Since

\[
 {d\over dx}\log\tan{x\over2}={1\over\sin x},
\]

integration from \(t\) to \(t_0\) gives exactly

\[
 \log\tan{\pi\over8}-\log\tan{\xi_1(t)\over2}
 =\mu_R\int_t^{t_0}b_A(s)\,ds,
\]

which is (S.423).  It also proves \(0<\xi_1(t)\le\pi/4\), so the asserted
continuous lift does not wind.

**Verdict for (S.421)--(S.423): PASS.**

### 2.3 Equations (S.424)--(S.425): Bernoulli cancellation and drift sign

The Bernoulli scalar can be simplified to

\[
 B_W={1\over2}|W|^2+p_W
 ={1\over2}-\sin^2x_1\sin^2x_2.
\]

A direct calculation gives \(W\cdot\nabla B_W=0\).  Since
\(\nabla\cdot W=0\),

\[
 \nabla\cdot(B_WW)=0.
\]

Consequently, for every smooth periodic shell cutoff,

\[
 \int_{\mathbb T^3}B_W(y+\xi)W(y+\xi)
       \cdot\nabla\Psi_k^R(y)\,dy=0.
\]

This is an integral cancellation; a pointwise cancellation is neither
claimed nor needed.  A time-dependent pressure gauge also contributes zero:

\[
 \int_{\mathbb T^3}c_R(t)v_R\cdot\nabla\Psi_k^R\,dy
 =-c_R(t)\int_{\mathbb T^3}\Psi_k^R\nabla\cdot v_R\,dy=0.
\]

The only surviving term is therefore

\[
 -{\gamma_k\eta_R\over2R}b_A^2a_R\cdot
   \int|W(y+\xi)|^2\nabla\Psi_k^R(y)\,dy,
\]

where \(a_R=\mu_Rb_AW(\xi)\).  Periodic integration by parts gives

\[
 \int|W(y+\xi)|^2\nabla\Psi_k^R(y)\,dy
 =-\int\Psi_k^R(y)\nabla|W(y+\xi)|^2\,dy
 =-\nabla_\xi J_{k,R}(\xi).
\]

The two minus signs cancel.  Thus the positive sign and the prefactor
\(\gamma_k\mu_R\eta_Rb_A^3/(2R)\) in (S.425) are correct.

**Verdict for (S.424)--(S.425): PASS.**

### 2.4 Equations (S.426)--(S.432): Fourier normalization, shell positivity, and residence

The identity

\[
 |W|^2={1-\cos2x_1\cos2x_2\over2}
\]

is correct.  With \(q_+=(2,2,0)\) and \(q_-=(2,-2,0)\), it is equivalently

\[
 |W(x)|^2={1\over2}
 -{1\over4}\left[\cos(q_+\cdot x)+\cos(q_-\cdot x)\right].
\]

Unfolding is legitimate because \(|W|^2\) is periodic:

\[
 \int_{\mathbb T^3}\Psi_k^R(y)|W(y+\xi)|^2\,dy
 =\int_{\mathbb R^3}\psi_k^R(y)|W(y+\xi)|^2\,dy.
\]

Evenness kills the sine coefficients, and radiality makes the coefficients
at \(q_+\) and \(q_-\) equal to the same unnormalized cosine integral
\(c_{k,R}\).  Hence

\[
 J_{k,R}(\xi)
 ={m_{k,R}\over2}
 -{c_{k,R}\over4}
  [\cos(q_+\cdot\xi)+\cos(q_-\cdot\xi)].
\]

Because

\[
 |W(\xi)|^2-{1\over2}
 =-{1\over4}
  [\cos(q_+\cdot\xi)+\cos(q_-\cdot\xi)],
\]

this is exactly (S.428).  There is no missing factor \(1/2\), \(1/4\), or
Fourier normalization.

For \(M=N+1\), the support bound and \(|q_+|=2\sqrt2\) give, for
\(k\le M\),

\[
 |q_+\cdot y|
 \le2\sqrt2(2^{M+1}+1/8)R<\pi/3.
\]

Therefore \(\cos(q_+\cdot y)\ge1/2\) throughout the support.  Since
\(\psi_k^R\ge0\) and is not identically zero,

\[
 c_{k,R}\ge{1\over2}m_{k,R}>0.
\]

This proves positivity on \(N+1\) actual physical shells.  It does not
replace a physical-shell index by a Fourier-shell index.

For the residence estimate, if \(0\le t_0-t\le\delta/A\), then

\[
 \int_t^{t_0}b_A(s)\,ds
 ={A\over2}(e^{2(t_0-t)}-1)
 \le{e^{2\delta}-1\over2}.
\]

The last inequality follows from convexity of \(e^x-1\), using \(A\ge1\).
Together with \(\mu_R\le1\), the chosen \(\delta\) and (S.423) imply
\(\xi_1\ge\pi/8\).  The already proved upper bound is \(\xi_1\le\pi/4\).
After \(A>\delta/R^2\), this interval lies in \(I_R\), where \(\eta_R=1\).

On \([\pi/8,\pi/4]\),

\[
 W(\xi)\cdot\nabla|W(\xi)|^2
 =\sin\xi_1\sin2\xi_1
 \ge\sin(\pi/8)\sin(\pi/4)=g_0.
\]

Since \(b_A(t)\ge A\) for \(t\le t_0\), (S.432), including its sign, follows.

**Verdict for (S.426)--(S.432): PASS.**

### 2.5 Equations (S.433)--(S.438): all \(R\)-powers and the common deletion

Under \(t=s_R+R^2\sigma\), one has \(d\sigma=dt/R^2\).  On the terminal
block,

\[
 h_{k,R}\ge
 {\gamma_k\mu_Rc_{k,R}g_0\over2}RA^3,
\]

and the block has dimensionless length

\[
 {\delta/A\over R^2}={\delta\over AR^2}.
\]

Thus, for finite \(p\),

\[
 \|h_{k,R}\|_p
 \ge {\gamma_k\mu_Rc_{k,R}g_0\over2}
 R A^3\left({\delta\over AR^2}\right)^{1/p},
\]

which is exactly

\[
 {\gamma_k\mu_Rc_{k,R}g_0\over2}
 \delta^{1/p}R^{1-2/p}A^{3-1/p}.
\]

For \(p=\infty\), the time-length factor disappears and the remaining
factor is \(RA^3\).  Hence (S.433)--(S.434) have the correct powers of
\(R\) and \(A\).

For every \(S\subset\mathbb N\) with \(\#S\le N=M-1\), at least one index
in \(\{1,\ldots,M\}\) is not in \(S\).  Therefore

\[
 \sum_{k\notin S}\|h_{k,R}\|_p
 \ge\min_{1\le k\le M}\|h_{k,R}\|_p,
\]

and the minimum has a strictly positive constant after \(N,R,p\) are fixed.
This proves (S.435) with the deletion set in the correct order.

Section 3 below independently checks \(P_R^M\le C_RA^3\).  Consequently,

\[
 {\mathfrak H^F_{p,N,R}\over(P_R^M)^{2/3}}
 \ge c_{p,N,R}A^{3-1/p-2}
 =c_{p,N,R}A^{1-1/p}\to\infty
\]

for every \(p>1\).  This is (S.437).

The proposed statement (S.342) has the logical form

\[
 \exists p>1\ \exists N\in\mathbb N_0\ \exists C>0\quad
 \forall(u,\pi)\ \forall R\ \forall z_0\ \forall\text{ terminal settings}:
 \mathfrak H^F_{p,N,R}\le C(P_R^M)^{2/3}.
\]

Its negation is exactly (S.438): after arbitrary \(p,N,C\) are fixed, choose
\(R\) satisfying (S.429), and then choose \(A\) sufficiently large.  The
scale is allowed to depend on the proposed universal \(N\); it is fixed
before the amplitude is sent to infinity.

**Verdict for (S.433)--(S.438): PASS.**

### 2.6 Equations (S.438a)--(S.438b): stronger exponent boundary

For the stated domain \(\beta\ge0\), the terminal-block calculation behind
(S.435), including its identical \(p=1\) integration, and the payment upper
bound give

\[
 {\mathfrak H^F_{p,N,R}\over(P_R^M)^\beta}
 \gtrsim_{p,N,R}A^{3-1/p-3\beta}.
\]

A universal upper bound can therefore hold only if

\[
 \beta\ge1-{1\over3p}.
\]

This proves (S.438a) for \(p>1\) directly.  At \(p=1\), integrating (S.432)
over its physical interval of length \(\delta/A\), applying the same
\(N+1\)-shell pigeonhole, and using (S.436) gives the same exponent
\(3-1/p=2\) without invoking a later result.  This calculation is recorded
again as (S.441).  Thus the current \(p\in[1,\infty]\), \(\beta\ge0\)
statement has no forward-reference gap.

On the dimensionless terminal interval \(I\) corresponding to
\([t_0-\delta/A,t_0)\), fixed \(N,R\) give

\[
 |I|={\delta\over AR^2}\asymp_R A^{-1},
 \qquad
 \int_Ih_{k,R}\,d\sigma\asymp_{k,R}A^2
\]

for each of the activated shells.  Hence

\[
 A^2\lesssim A^{3\beta-\alpha}
\]

is necessary for a bound of the form displayed before (S.438b).  This is
equivalent to \(3\beta-\alpha\ge2\).  If the window estimate is formulated
after a deletion of \(N\) shells, the same conclusion follows by using the
\(N+1\) activated shells and retaining one survivor.

**Verdict for (S.438a)--(S.438b): PASS.**

### 2.7 Equations (S.439)--(S.444): the \(p=1\) endpoint

For all \(k\), radial evenness gives \(|c_{k,R}|\le m_{k,R}\).  Along the
trajectory,

\[
 d\xi_1=\mu_Rb_A\sin\xi_1\,dt.
\]

Using (S.425), (S.431), \(0\le\eta_R\le1\), and
\(\sin2x=2\sin x\cos x\), the multiplier \(\mu_R\) cancels exactly:

\[
\begin{aligned}
 \int_{s_R}^{t_0}|\dot F_{k,R}|\,dt
 &\le {\gamma_k|c_{k,R}|\over2R}
       \sup_{I_{2R}}b_A^2
       \int_0^{\pi/4}\sin2x\,dx\\
 &= {\gamma_k|c_{k,R}|\over R}
       \sup_{I_{2R}}b_A^2
       \int_0^{\pi/4}\sin x\cos x\,dx.
\end{aligned}
\]

This is (S.439).  Since

\[
 \|h_{k,R}\|_{L^1(0,4)}
 =\int_{s_R}^{t_0}|\dot F_{k,R}(t)|\,dt,
\]

and

\[
 m_{k,R}\le C2^{3k}R^3,
 \qquad
 \sum_{k\ge1}2^{3k}\gamma_k<\infty,
\]

summing over all shells proves (S.440).  Integrating (S.432) over a physical
interval of length \(\delta/A\), then applying the same \(N+1\)-shell
pigeonhole, proves (S.441).

For the payment lower bound, smoothness permits good times \(t_j\uparrow t_0\)
and

\[
 v_R(t_j,y)\to AW(y+x_*).
\]

The continuous field on the right is nonzero on a positive-volume subset of
\(B_{8R}\), so

\[
 \mathcal E^{M,R}(z_0,8R)
 \ge {A^2\over8R}
       \int_{B_{8R}}|W(y+x_*)|^2\,dy
 =c_RA^2.
\]

Taking the \(3/2\) power proves (S.442).  Combining the upper and lower
bounds proves all three comparisons in (S.443), with constants depending on
\(N,R\) exactly as stated.  This is amplitude-exponent saturation at fixed
\((N,R)\), not a claim of a uniform sharp constant.

The quantifiers in the corrected (S.444) are complete: \(N_1,C\) are fixed
universally before the solution, admissible scale, and terminal point.  The
Taylor family neither proves nor disproves this statement.  Since the Step
15 variation-to-terminal argument is valid at \(p=1\), (S.444) remains a
sufficient, but open, route to the hybrid terminal residual.

**Verdict for (S.439)--(S.444): PASS.**

## 3. Independent completeness check for the payment (S.436)

The payment comparison must include all rows over the full frozen time
interval.  On \(\overline I_{8R}\),

\[
 A\le b_A(t)\le Ae^{128R^2}.
\]

For fixed \(R\), compactness of the torus gives

\[
 |v_R|+|\nabla v_R|\le C_RA,
 \qquad
 |\pi_R|\le C_RA^2,
\]

uniformly in the \(A\)-dependent translated phase.

### 3.1 Buffered local energy

The essential-supremum part satisfies

\[
 (8R)^{-1}\mathop{\rm ess\,sup}_{I_{8R}}
 \int_{B_{8R}}|v_R|^2\le C_RA^2.
\]

The dissipation part satisfies

\[
 (8R)^{-1}\int_{I_{8R}}\int_{B_{8R}}|\nabla v_R|^2
 \le C_RA^2.
\]

Hence

\[
 \mathcal E^{M,R}(z_0,8R)^{3/2}\le C_RA^3.
\]

### 3.2 Exterior velocity and pressure row

At the fixed radius \(\rho=2R\), the localized Riesz transform, harmonic
remainder, and fixed gauge are quadratic in \(b_A\).  Their spatial profiles
depend on the translated phase, but that phase ranges in the compact torus;
the resulting family is uniformly bounded for fixed \(R\).  Therefore

\[
 |v_R|^3+|\pi_R-c_{2R}^{M,R}|^{3/2}\le C_RA^3.
\]

Since

\[
 \sum_{j\ge1}\gamma_j|A_j(2R)|
 \le C R^3\sum_{j\ge1}2^{3j}\gamma_j<\infty,
\]

and \(|I_{2R}|=4R^2\), the normalization in
\(\mathcal G^{M,R}\) gives

\[
 \mathcal G_{v_R,\pi_R}^{M,R}(z_0,2R;1)\le C_RA^3.
\]

This includes the actual frozen pressure gauge; it is not a bound for a
more favorable substitute gauge.

### 3.3 Algebraic harmonic row

Pointwise boundedness gives

\[
\begin{aligned}
 \Lambda_{2R}^{M,R}(t)
 &=(2R)\sum_{j\ge1}(2^j\,2R)^{-4}
   \int_{A_j(2R)}|\widetilde v_R|^2\\
 &\le C A^2(2R)\sum_{j\ge1}
       (2^j\,2R)^{-4}(2^j\,2R)^3\\
 &\le CA^2\sum_{j\ge1}2^{-j}\le CA^2.
\end{aligned}
\]

Thus

\[
 \mathcal H_{v_R}^{M,R}(z_0,2R)
 =(2R)\int_{I_{2R}}(\Lambda_{2R}^{M,R})^{3/2}\,dt
 \le C_RA^3.
\]

The convergence mechanisms should be distinguished: the exterior cubic and
pressure row uses the super-Gaussian \(\gamma_j\), whereas the harmonic row
uses the algebraic order-\(-4\) kernel and the summable factor \(2^{-j}\).
The frozen sentence after (S.436) now records these two convergence
mechanisms separately.

Combining Sections 3.1--3.3 proves

\[
 P_R^M\le C_RA^3.
\]

There is no acceleration payment in Version M.  The moving-cutoff drift is
part of \(F_{k,R}\), not an omitted row of \(P_R^M\).  Thus the payment audit
is complete.

**Verdict for (S.436): PASS, with the stated wording distinction between
the two all-copy convergence mechanisms.**

## 4. Quantifier and scope verdict

The disproof fixes the quantifiers in the required order:

1. an adversary proposes \(p>1\), \(N<\infty\), and a universal \(C\);
2. choose \(M=N+1\);
3. choose one admissible \(R\) so that the first \(M\) shell coefficients
   and the velocity-mollifier coefficient are positive;
4. keep that \(R\) fixed and send \(A\to\infty\).

The resulting solution is smooth, so it lies inside every suitable-weak or
Leray class used by the project.  Therefore a failure on this family is a
failure on the larger bare class.  Dependence of the lower-bound constant on
\(p,N,R\) is harmless because the divergence occurs after those parameters
are fixed.  Dependence of the chosen \(R\) on \(N\) is also harmless because
(S.342) asserted one \(N\) uniformly over all admissible scales.

What is disproved is precisely

\[
 \mathfrak H^F_{p,N,R}\lesssim(P_R^M)^{2/3}
 \quad\text{for a fixed }p>1\text{ and finite }N.
\]

The calculation does not disprove:

- a \(p>1\) estimate with a sufficiently larger payment power;
- an estimate containing an additional energy, scale, or regularity factor;
- the critical \(p=1\) candidate (S.444);
- a signed terminal increment estimate which does not pay full absolute
  temporal variation;
- the hybrid terminal gate, Q.12, Q.1, scale contraction, or regularity.

The title and scope language in the corrected main note respect this
boundary.

## 5. ABC cross-check

For

\[
 U=(\sin x_3+\cos x_2,\ \sin x_1+\cos x_3,\
       \sin x_2+\cos x_1),
\]

direct differentiation gives

\[
 \nabla\times U=U,\qquad \Delta U=-U.
\]

The vector identity

\[
 (U\cdot\nabla)U
 =\nabla{|U|^2\over2}-U\times(\nabla\times U)
 =\nabla{|U|^2\over2}
\]

shows that \(Ae^{-(t-t_0)}U\), with pressure \(-|u|^2/2\), is exact.  At the
origin, \(U=(1,1,1)\) and

\[
 \nabla|U|^2=(2,2,2),\qquad
 U\cdot\nabla|U|^2=6.
\]

The velocity modes have frequency length \(1\).  In the sum of the three
squared components, the axial frequency-two pieces cancel in pairs, leaving
only nonconstant modes of length \(\sqrt2\).  Hence the radial-multiplier
description is correct.

The main Taylor proof does not depend on this screen.  If the ABC paragraph
were later promoted to a second fully stated theorem, it should display its
own short-time trajectory-residence and simultaneous-mode positivity
argument.  As presently labeled an independent algebraic screen and omitted
from the proved-claim ledger, its scope is appropriate.

## 6. Primary-source boundary

The direct substitution above proves the counterexample; no literature
non-hit is used as a premise.  The historical citations have the following
limited roles.

| Primary source | What it supports | What it does not support |
|---|---|---|
| G. I. Taylor, [*On the decay of vortices in a viscous fluid*](https://doi.org/10.1080/14786442308634295) (1923) | Classical viscous periodic-vortex provenance | The project-specific moving terminal trajectory, common deletion, or payment \(P_R^M\) |
| G. I. Taylor and A. E. Green, [*Mechanism of the production of small eddies from large ones*](https://doi.org/10.1098/rspa.1937.0036) (1937) | Historical Taylor--Green context | The exact Version-M obstruction or its quantifiers |
| J. Chai, T. Wu, and L. Fang, [*Single-scale two-dimensional-three-component generalized-Beltrami-flow solutions of incompressible Navier--Stokes equations*](https://doi.org/10.1016/j.physleta.2020.126857) (2020) | Modern generalized-Beltrami exact-flow context | A temporal shell-tail counterexample |
| M. Antuono, [*Tri-periodic fully three-dimensional analytic solutions for the Navier--Stokes equations*](https://doi.org/10.1017/jfm.2020.126) (2020) | Tri-periodic Beltrami solutions and explicit acknowledgement of Taylor's bi-periodic viscous vortex | The frozen mollified path, physical-annulus deletion, or \(P_R^M\) comparison |
| Caffarelli--Kohn--Nirenberg, [*Partial regularity of suitable weak solutions of the Navier--Stokes equations*](https://doi.org/10.1002/cpa.3160350604) (1982) | Suitable-weak and local-energy framework | Any \(L_t^p\) common-deletion flux estimate |
| J. Wolf, [*On the local pressure of the Navier--Stokes equations and related systems*](https://arxiv.org/abs/1611.01482) (2016/2017) | Local/harmonic pressure provenance | The temporal-tail power or fixed shell deletion |
| R. Dascaliuc and Z. Grujić, [*Energy cascades and flux locality in physical scales of the 3D Navier--Stokes equations*](https://arxiv.org/abs/1101.2193) (2011) | Rigorous physical-space flux estimates after time/ensemble averaging | Full absolute time variation along a terminal mollified trajectory |
| H. Koch and D. Tataru, [*Well-posedness for the Navier--Stokes equations*](https://math.berkeley.edu/~tataru/papers/nas.pdf) (2001) | A Carleson-type norm in a critical small-\(BMO^{-1}\) solution class | A Carleson or Morrey gain derived from the bare Leray energy class |
| J. Yang, [*Construction of maximal functions associated with skewed cylinders generated by incompressible flows and applications*](https://doi.org/10.4171/AIHPC/20) (2022) | Weak-\((1,1)\)/strong-\((p,p)\) maximal bounds for mollified-flow cylinders | The shellwise flux observable, one common deletion, or \((P_R^M)^{2/3}\) |
| A. Vasseur and J. Yang, [*Second derivatives estimate of suitable solutions to the 3D Navier--Stokes equations*](https://arxiv.org/abs/2009.14291) (2021) | A spacetime Lorentz improvement for \(\nabla^2u\) | An \(\ell^1(L_t^p)\) moving-shell flux tail |

The checked literature supplies the classical ingredients and nearby
analytic architectures.  It does not supply (S.342), its counterexample, or
an equivalent weak-\(L^p\)/Carleson statement with the same quantifiers.  This
is a bounded collision statement, not a novelty or priority theorem.

## 7. Issue ledger

| Item | Status | Audit conclusion |
|---|---|---|
| Exact NSE field and pressure sign | **PASS** | (S.417)--(S.420) cancel componentwise |
| Mollifier normalization | **PASS** | (S.421) is convention-free and common to all \(|n|=\sqrt2\) modes |
| Backward terminal trajectory | **PASS** | (S.423) has the correct sign and no winding |
| Bernoulli cancellation | **PASS** | Integral cancellation is exact for every periodic shell |
| Moving-drift sign | **PASS** | Two minus signs give the positive second line of (S.425) |
| Fourier coefficient in (S.428) | **PASS** | Product-to-sum gives the displayed coefficient with no missing factor |
| \(N+1\)-shell positivity | **PASS** | (S.429) implies \(\cos(q_+\cdot y)\ge1/2\) on every selected support |
| Terminal residence | **PASS** | A physical window of length \(\delta/A\) lies in \(\eta_R=1\) for large \(A\) |
| \(R\)-powers in \(L^p\) | **PASS** | \(R^{1-2/p}A^{3-1/p}\), and \(RA^3\) for \(p=\infty\), are correct |
| Common deletion | **PASS** | One of the first \(N+1\) shells survives every deletion of size \(N\) |
| Complete payment | **PASS** | Local energy, exterior cubic/pressure, fixed gauge, and algebraic harmonic rows are all \(O_R(A^3)\) |
| Quantifier negation | **PASS** | (S.438) is the exact negation of (S.342) |
| General \(\beta\)-boundary | **PASS** | The current draft states \(\beta\ge0\); the \(p=1\) case follows directly from the same terminal-block integration and is recorded as (S.441) |
| \(p=1\) amplitude law | **PASS** | Both \(\mathfrak H^F_{1,N,R}\asymp_{N,R}A^2\) and \(P_R^M\asymp_RA^3\) hold |
| Critical candidate (S.444) | **OPEN, CORRECTLY SCOPED** | The exact family neither proves nor refutes it |
| ABC paragraph | **ALGEBRAIC PASS** | Correct independent screen; not needed for the theorem |
| Literature boundary | **PASS** | Provenance only; no absence-based proof or priority claim |

## 8. Final audit conclusion

The main result is rigorous:

\[
 \boxed{
 \forall p\in(1,\infty]\ \forall N\in\mathbb N_0\ \forall C>0\
 \exists\text{ a smooth periodic Version-M example and admissible }R,z_0:
 \quad
 \mathfrak H^F_{p,N,R}>C(P_R^M)^{2/3}.}
\]

Accordingly, (S.342) must be marked **FALSE**, not merely open.  The result
does not solve or negatively resolve any regularity gate.  It removes one
overstrong sufficient route and leaves the critical \(L_t^1\) and signed
terminal routes open.  **NOT CLAY.**
