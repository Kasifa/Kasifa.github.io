# R0.71V -- Leray-paid amplitude excursions and a genuine NSE obstruction to first-row-only zero sampling

**Date:** 2026-08-26

**Status:** release source. This report proves a scale-zero amplitude-excursion
packing law for compact Fourier shells at the Leray--Hopf level. It also
constructs a fixed-target, fixed-window sequence of globally smooth unforced
2.5D NSE solutions for which a prescribed second zero atom divided by the
first-time-jet row grows like \(q^2\). The R0.71U second-time-jet row still
pays that event. The same sequence makes the exact excursion-to-atom
noncollapse factor decay like \(q^{-4}\). A weighted one-dimensional area
formula explains the boundary: Leray pays a level-integrated linear-slope
density, while a quadratic zero-slope density requires cubic time occupation
or an additional endpoint trace. No weak zero-jet definition, continuation
criterion, singularity, global regularity, novelty, or priority claim is made.

## 0. Direct decision

Let \(K=[a,b]\), \(\ell=b-a\), and retain the R0.71U global-shell notation

\[
 r_j(t)=\|C_j(t)\|_2,\qquad
 B_1(K)=\int_K\frac1Y\sum_j\kappa_j^{-6}\|C_{j,t}\|_2^2\,dt.
 \tag{0.1}
\]

For every right-rooted connected component \(E\) of
\(\{t\in K:r_j(t)>0\}\), put

\[
 h_E=\sup_Er_j,\qquad
 Y_E=\int_EY(t)\,dt,\qquad
 H_E^2=\frac{\kappa_j^{-6}h_E^2}{\ell Y_E}.
 \tag{0.2}
\]

The first result is

\[
 \boxed{
 \sum_{j,E}H_E^2
 \le \frac{B_1(K)}\ell
 \le 2C_{\rm ann,T}\left[
 \nu^2+\frac1\ell\int_K
 \frac{\|L\|_{\dot H^{-1}}^2}{Y}\,dt\right].}
 \tag{0.3}
\]

Here \(L=\mathbb P(u\times\omega)\) is the projected rotational
nonlinearity. The last integral is finite from Leray energy. Compact
Fourier-shell coefficients have absolutely continuous representatives for a
Leray--Hopf solution, so (0.3) is not restricted to a classical interval.
It gives

\[
 \#\{(j,E):H_E\ge\delta\}
 \le \delta^{-2}\frac{B_1(K)}\ell.
 \tag{0.4}
\]

The theorem pays normalized excursion height, not the root slope. At a
classical simple root \(t_E\), define

\[
 s_E=\|C_{j,t}(t_E)\|_2,\qquad
 D_E=\frac{h_E^2Y(t_E)}{\ell Y_Es_E^2}.
 \tag{0.5}
\]

Then

\[
 H_E^2=D_E\kappa_j^{-6}\frac{s_E^2}{Y(t_E)}.
 \tag{0.6}
\]

A uniform \(D_E\ge d_0>0\) would replace the second-time-jet tax by the
Leray-paid right side of (0.3). R0.71V shows that this hypothesis is not a
consequence of smooth unforced NSE dynamics plus bounded initial energy and
enstrophy.

There is a sequence of exact 2.5D solutions, one fixed compact target
multiplier, and one fixed macroscopic interval \(K\), such that a prescribed
second root satisfies the following ratios against the first- and second-time
rows of that selected singleton target shell. The quantities in (0.7) are
evaluated on the exact diagonal solutions; their ratios inherit the tangent
limits constructed below:

\[
 \boxed{
 \frac{J_{2,q}}{(2/\ell)B_{1,q}^{(*)}}\asymp q^2,\qquad
 \frac{J_{2,q}}{(7\ell/3)B_{2,q}^{(*)}}\asymp q^{-2}.}
 \tag{0.7}
\]

For the last outgoing component,

\[
 \boxed{D_{E,q}\asymp q^{-4}.}
 \tag{0.8}
\]

The first prescribed atom can be paid separately and the second still has
the \(q^2\) ratio. Thus this is a recurrence obstruction, not only the first
sample in a point-trace estimate. The result does not prove that the
coefficient \(7\ell/3\) is sharp; this family makes the second row overpay.
It also does not reject a different estimate containing the global
\(\nu^2\) baseline, an explicit root trace, or another dynamical charge.

## 1. Global-shell payment setting

Work on the normalized three-torus. Let

\[
 \omega=\operatorname{curl}u,\qquad
 Y=\|\omega\|_2^2,\qquad
 L=\mathbb P(u\times\omega),
 \tag{1.1}
\]

With the common convention
\(D_{\rm Lamb}=\omega\times u\), this report uses
\[
 L=-\mathbb P D_{\rm Lamb}.
 \tag{1.1a}
\]
Thus \(L\) is called the projected rotational nonlinearity; its sign is
chosen so that the unforced projected equation is
\(u_t=\nu\Delta u+L\).

Let \(T_j\) be compactly supported, real-even annular Fourier
multipliers. Set

\[
 W_j=T_j\omega,\qquad
 F_j=T_jL,\qquad
 C_j=\operatorname{curl}W_j=-\Delta T_ju.
 \tag{1.2}
\]

The nonzero support satisfies
\(c_0\kappa_j\le |k|\le c_1\kappa_j\), and the frame has the R0.71U upper
square-function bound. At a positive global-shell root,

\[
 J_E\le c_0^{-4}\kappa_j^{-6}
 \frac{\|C_{j,t}(t_E)\|_2^2}{Y(t_E)}.
 \tag{1.3}
\]

On one Laplace eigenshell \(|k|=\rho_j\),

\[
 J_E=\frac{\kappa_j^4}{\rho_j^4}
 \kappa_j^{-6}\frac{\|C_{j,t}(t_E)\|_2^2}{Y(t_E)}.
 \tag{1.4}
\]

The first-time row obeys

\[
 B_1(K)\le 2C_{\rm ann,T}\left[
 \nu^2\ell+\int_K\frac{\|L\|_{\dot H^{-1}}^2}{Y}\,dt\right].
 \tag{1.5}
\]

Every normalized quotient in (0.1), (0.3), and (1.5) is assigned the value
zero on \(\{Y=0\}\). At almost every such time the mean-zero part of \(u\)
vanishes, hence \(L=0\) and all compact-shell derivatives in the numerator
vanish as well. This convention only removes the indeterminate notation
\(0/0\); it adds no positive charge.

Indeed,
\(\|L\|_{\dot H^{-1}}^2/Y\lesssim\|u\|_2Y^{1/2}\), and the Leray energy
inequality makes the right side finite on every finite interval.

## 2. Weak shell traces are enough for excursions

A compact torus annulus contains finitely many lattice modes. Testing the
Leray--Hopf equation against the associated divergence-free Fourier basis
vectors shows that every coefficient is in \(W^{1,1}(K)\). Hence \(C_j\)
and \(r_j=\|C_j\|_2\) have absolutely continuous representatives, with

\[
 |r_{j,t}|\le\|C_{j,t}\|_2
 \quad\text{for almost every }t.
 \tag{2.1}
\]

The open set \(\{r_j>0\}\) has at most countably many components. Call a
component \(E\) right rooted if its left endpoint \(t_E\) is a zero, with
the one-sided convention at \(a\). Thus a component meeting \(a\) is included
only when \(r_j(a)=0\). A component already positive at \(a\) requires a
separate initial trace and is not charged by Theorem 3.1.

If \(h_E>0\), then \(Y_E>0\). Continuity makes \(r_j\) positive on a
smaller open interval, while annular Bernstein gives

\[
 r_j(t)\lesssim\kappa_jY(t)^{1/2}
 \tag{2.2}
\]

almost everywhere.

## 3. Leray-paid amplitude-excursion theorem

### Theorem 3.1 -- scale-zero excursion-height packing

For every finite compact-shell family and finite selection of right-rooted
components,

\[
 \boxed{
 \sum_{j,E}\frac{\kappa_j^{-6}h_E^2}{Y_E}
 \le B_1(K).}
 \tag{3.1}
\]

The statement extends to countable shells and all right-rooted components by
Tonelli and monotone convergence.

For one component,

\[
 h_E\le\int_E(r_{j,t})_+\,dt
 \le Y_E^{1/2}
 \left(\int_E\frac{(r_{j,t})_+^2}{Y}\,dt\right)^{1/2}.
 \tag{3.2}
\]

The components of one shell are disjoint. Squaring (3.2), multiplying by
\(\kappa_j^{-6}\), and summing proves (3.1). Division by \(\ell\) and
(1.5) prove (0.3); Chebyshev's inequality proves (0.4).

The scaling is exact:

\[
 h_E:+3,\qquad Y_E:+2,\qquad
 \ell:-2,\qquad\kappa_j^{-6}:-6.
 \tag{3.3}
\]

Thus \(H_E^2\) and \(B_1(K)/\ell\) both have scale exponent zero.

## 4. Exact excursion-to-atom conversion

For a classical simple positive root, (0.6) is an algebraic identity. If
\(D_E\ge d_0>0\) over the selected events, then (1.3) and Theorem 3.1 give

\[
 \boxed{
 \sum_EJ_E
 \le 2c_0^{-4}d_0^{-1}C_{\rm ann,T}
 \left[\nu^2+\frac1\ell\int_K
 \frac{\|L\|_{\dot H^{-1}}^2}{Y}\,dt\right].}
 \tag{4.1}
\]

For one fixed classical trajectory with finitely many simple roots and
nonzero right excursions, every \(D_E\) is positive. Uniformity across data,
frequencies, and recurrence patterns is the missing step. The factor measures
whether the root slope persists long enough to create a normalized height.

## 5. Weighted area formula and the missing slope

Let \(r\in W^{1,1}(I)\), let \(w\ge0\), and let
\(B\subset(0,\infty)\) be Borel. The one-dimensional weighted area formula is

\[
 \boxed{
 \int_{\{r\in B\}}w(t)(r_t)_+\,dt
 =\int_B\sum_{\substack{t:r(t)=z\\r_t(t)>0}}w(t)\,dz.}
 \tag{5.1}
\]

Critical points do not contribute. At Leray regularity, the following root
sums define almost-everywhere-in-\(z\) equivalence classes; their values on the
exceptional set of levels may be chosen arbitrarily, and the sums may equal
\(+\infty\):

\[
 \mathcal M(z)=
 \sum_j\sum_{\substack{t:r_j(t)=z\\r_{j,t}>0}}
 \kappa_j^{-6}\frac{r_{j,t}(t)}{Y(t)}
 \tag{5.2}
\]

and

\[
 \mathcal Q(z)=
 \sum_j\sum_{\substack{t:r_j(t)=z\\r_{j,t}>0}}
 \kappa_j^{-6}\frac{r_{j,t}(t)^2}{Y(t)}.
 \tag{5.3}
\]

Then

\[
 \boxed{
 \int_B\mathcal M(z)\,dz
 =\int_K\sum_j\mathbf 1_{\{r_j(t)\in B\}}
 \kappa_j^{-6}\frac{(r_{j,t})_+^2}{Y}\,dt
 \le B_1(K),}
 \tag{5.4}
\]

whereas

\[
 \boxed{
 \int_B\mathcal Q(z)\,dz
 =\int_K\sum_j\mathbf 1_{\{r_j(t)\in B\}}
 \kappa_j^{-6}\frac{(r_{j,t})_+^3}{Y}\,dt.}
 \tag{5.5}
\]

Only in the classical finite-shell situation with finitely many isolated
simple roots and nonzero endpoints do we use the pointwise boundary formula

\[
 \lim_{z\downarrow0}\mathcal Q(z)
 =\sum_{j,E}\kappa_j^{-6}
 \frac{\|C_{j,t}(t_E)\|_2^2}{Y(t_E)}.
 \tag{5.6}
\]

Leray's \(L_t^2\) row therefore pays a level-integrated density with one
slope. Keeping the quadratic zero-slope mass under level averaging raises
the time power to three. An \(L^1(dz)\) bound does not determine the
distinguished boundary value at \(z=0\). A sufficient missing estimate would
be a uniform reverse average

\[
 \mathcal Q(0+)\le\frac C{h_0}\int_0^{h_0}\mathcal Q(z)\,dz.
 \tag{5.7}
\]

Ordinary coarea and Leray energy do not supply (5.7).

## 6. Exact sine stress test

On the time circle of length \(2\pi\), take

\[
 C_N(t)=N^{-1}\sin(Nt)e,\qquad Y=\kappa=1.
 \tag{6.1}
\]

There are \(2N\) simple roots and excursions. Each has

\[
 s_E=1,\qquad h_E=N^{-1},\qquad Y_E=\pi/N.
 \tag{6.2}
\]

Consequently

\[
 D_E=H_E^2=\frac1{2\pi^2N},\qquad
 \sum_EH_E^2=\frac1{\pi^2},
 \tag{6.3}
\]

while

\[
 B_1=\pi,\qquad B_1/\ell=\frac12,\qquad
 \sum_Es_E^2=2N,\qquad
 \int\|C_{N,tt}\|_2^2dt=\pi N^2.
 \tag{6.4}
\]

For \(0<z<1/N\),

\[
 \mathcal Q_N(z)=2N(1-N^2z^2),\qquad
 \mathcal M_N(z)=2N\sqrt{1-N^2z^2}.
 \tag{6.5}
\]

Yet

\[
 \int_0^\infty\mathcal Q_N(z)\,dz=\frac43,\qquad
 \int_0^\infty\mathcal M_N(z)\,dz=\frac\pi2,
 \tag{6.6}
\]

while both zero-level traces equal \(2N\). This is a shell-path method test,
not an NSE trajectory.

## 7. Tangent ledger for the exact 2.5D recurrence family

Use the exact invariant class

\[
 u=(f(y,z,t),0,v(y,t)),\qquad
 v_t=\nu v_{yy},\qquad
 f_t+vf_z=\nu(f_{yy}+f_{zz}).
 \tag{7.1}
\]

Fix \(k_*=(0,K_y,K_z)\), writing \(K_y,K_z\) for the target spatial
frequencies to avoid collision with the time interval \(K\) and the
projected rotational nonlinearity \(L\). Put

\[
 \rho^2=K_y^2+K_z^2,\quad \mu=\nu\rho^2,\quad
 \alpha_l=(K_y-n_l)^2+K_z^2,\quad
 \beta_l=2\nu n_l(n_l-K_y),
 \tag{7.2}
\]

\[
 \psi_l(t)=\frac{1-e^{-\beta_lt}}{\beta_l}.
 \tag{7.3}
\]

For \(N\) prescribed roots, normalize \(c_1=1\) and choose the other real
tangent coefficients so that

\[
 h(t)=\sum_{l=1}^{N+1}c_l\psi_l(t),\qquad h(t_m)=0.
 \tag{7.4}
\]

The Chebyshev-system determinant makes the coefficients unique and every
\(h'(t_m)\) nonzero. If all scalar seeds are multiplied by \(\varepsilon\),
the exact implicit curve satisfies

\[
 a_{p(s)}(t)=\varepsilon K_zs e^{-\mu t}h(t)
 +O_{C^2}(\varepsilon s^2).
 \tag{7.5}
\]

Let \(Y_0\) be the enstrophy at \(s=0\), including any decoupled background.
Then

\[
 \sum_mJ_m(s)=s^2M_2+O(s^3),
 \tag{7.6}
\]

\[
 M_2=2|m_*|^2\kappa_*^{-2}\varepsilon^2K_z^2
 \sum_m\frac{e^{-2\mu t_m}|h'(t_m)|^2}{Y_0(t_m)}.
 \tag{7.7}
\]

The two R0.71U rows are

\[
 B_1(s)=s^2B_{1,2}+O(s^3),
 \tag{7.8}
\]

\[
 B_{1,2}=2\rho^4|m_*|^2\kappa_*^{-6}\varepsilon^2K_z^2
 \int_K\frac{e^{-2\mu t}|h'-\mu h|^2}{Y_0}\,dt,
 \tag{7.9}
\]

and

\[
 B_2(s)=s^2B_{2,2}+O(s^3),
 \tag{7.10}
\]

\[
 B_{2,2}=2\rho^4|m_*|^2\kappa_*^{-6}\varepsilon^2K_z^2
 \int_K\frac{e^{-2\mu t}|h''-2\mu h'+\mu^2h|^2}{Y_0}\,dt.
 \tag{7.11}
\]

Without a background,

\[
 Y_0(t)=2\varepsilon^2
 \sum_{l=1}^{2N+1}\alpha_l e^{-2\nu\alpha_lt}.
 \tag{7.12}
\]

Thus \(\varepsilon\) cancels from the leading normalized fixed-data
coefficients. Passive amplitude alone is not the source of leading atom
collapse.

For fixed response rates and roots clustered with spacing \(\Delta\) around
\(t_0>0\), the determinant factorization gives

\[
 h'(t_m)=O(\Delta^{N-1}),\qquad
 J_m=O(s^2\Delta^{2N-2}).
 \tag{7.13}
\]

Clustering at the launch time adds the common zero \(\psi_l(0)=0\):

\[
 h'(t_m)=O(\Delta^N),\qquad
 J_m=O(s^2\Delta^{2N}).
 \tag{7.14}
\]

## 8. Fixed-target high-frequency repeated-root family

This construction is not a covariant parabolic dilation. The target
multiplier, nominal scale, and observation window remain fixed while only
auxiliary shear frequencies increase.

Fix

\[
 0<A<\tau_1<\cdots<\tau_N,\qquad
 K=[a,b],\qquad \ell=b-a>0,
 \tag{8.1}
\]

pairwise distinct positive integers \(r_1,\ldots,r_{2N+1}\) with greatest
common divisor one. The torus frequencies \(K_y,K_z,Q,d\) are fixed
integers with \(K_z\ne0\), while \(B\ne0\), \(Q>R_*\), and
\(d>R_*+|K_y|\). Choose \(q_0\) so that all times in (8.3) lie in \(K\).
For each integer \(q\ge q_0\), launch the exact solution at

\[
 \sigma_q=a-Aq^{-2}.
 \tag{8.2}
\]

With relative time \(\theta=t-\sigma_q\), set

\[
 n_{l,q}=dr_lq,\qquad
 \varepsilon_q=q^{-2},\qquad
 t_{m,q}=a+(\tau_m-A)q^{-2}.
 \tag{8.3}
\]

Add the decoupled background

\[
 f_b(y,\theta)=B e^{-\nu Q^2\theta}
 (e^{iQy}+e^{-iQy}),\qquad Q>R_*.
 \tag{8.4}
\]

It has \(z\)-frequency zero, so \(v(f_b)_z=0\). It evolves by heat, never
enters the target annulus, and supplies a uniform positive enstrophy floor.

For the \(N+1\) real tangent columns, let

\[
 \phi_{l,q}(\theta)=e^{-\mu\theta}
 \frac{1-e^{-\beta_{l,q}\theta}}{\beta_{l,q}},
 \tag{8.5}
\]

and choose \(c_{1,q}=1,c_{2,q},\ldots,c_{N+1,q}\) so that

\[
 \gamma_q(\theta)=K_z\sum_{l=1}^{N+1}c_{l,q}\phi_{l,q}(\theta),
 \qquad
 \gamma_q(\tau_mq^{-2})=0.
 \tag{8.6}
\]

The remaining \(N\) parameters supply the imaginary Jacobian block. The real
implicit-function matrix is invertible. More explicitly, modular separation
makes the generated modes inside the fixed compact target support equal to
the single conjugate pair \(\pm k_*\). Let \(E_*\) be its two-dimensional
real target space and define the exact triangular-flow target map

\[
 \Phi_q(s,z)=
 \bigl(T_*\omega_{s,z}(t_{1,q}),\ldots,
 T_*\omega_{s,z}(t_{N,q})\bigr)
 \in E_*^N\simeq\mathbb R^{2N}.
 \tag{8.6a}
\]

Here \(s\) is the free real shear amplitude and
\(z\in\mathbb R^{2N}\) contains the other \(2N\) real shear amplitudes from
the R0.71U exact 2.5D construction. The seed coefficients have the fixed
phases \(i\) and \(1\); they are not variables. At \((s,z)=(0,0)\), the
columns attached to those two fixed phase classes form the real and imaginary
evaluation blocks, and \(D_z\Phi_q(0,0)\) is invertible. The
finite-dimensional implicit-function theorem therefore gives
\(z=z_q(s)\), or equivalently a full shear-amplitude curve \(p_q(s)\), with

\[
 \Phi_q(s,z_q(s))=0,\qquad
 s^{-1}a_{p_q(s)}(t)\longrightarrow
 \varepsilon_q\gamma_q(t-\sigma_q)
 \quad\text{in }C^2(K)\quad(s\to0)
 \tag{8.6b}
\]

for each fixed \(q\). The background has \(z\)-frequency zero and changes
neither \(\Phi_q\) nor this derivative. On the isolated nonzero pair
\(\pm k_*\), curl is an invertible linear map on the divergence-free real
mode space; hence \(\Phi_q=0\) is equivalent to vanishing of the target
velocity coefficient used in the response formula.

Put

\[
 b_l=2\nu d^2r_l^2,\qquad
 \Psi_l(x)=\frac{1-e^{-b_lx}}{b_l}.
 \tag{8.7}
\]

The limiting interpolation coefficients \(c_l^\infty\) solve

\[
 \Gamma(x)=K_z\sum_{l=1}^{N+1}c_l^\infty\Psi_l(x),
 \qquad
 \Gamma(\tau_m)=0.
 \tag{8.8}
\]

The limiting functions remain a Chebyshev system, so

\[
 \sigma_m^\infty=|\Gamma'(\tau_m)|>0.
 \tag{8.9}
\]

The same zero count gives more than simplicity. Both \(\gamma_q\) and
\(\Gamma\) have their common launch zero and exactly the \(N\) prescribed
positive zeros, with no additional positive zero. Moreover
\(\Gamma_\infty=K_z\sum_lc_l^\infty/b_l\ne0\): if this constant vanished,
\(\Gamma\) would reduce to a nontrivial combination of \(N+1\) decaying
exponentials vanishing at the \(N+1\) distinct points
\(0,\tau_1,\ldots,\tau_N\), contradicting their Chebyshev zero count. Each
internal limiting lobe therefore has a nonzero extremal height, and the final
branch has a nonzero limiting tail.

## 9. Boundary-layer asymptotics and exact NSE obstruction

Uniformly on compact \(x\)-intervals,

\[
 q^2\gamma_q(xq^{-2})\to\Gamma(x),\qquad
 \gamma_q'(xq^{-2})\to\Gamma'(x),\qquad
 q^{-2}\gamma_q''(xq^{-2})\to\Gamma''(x).
 \tag{9.1}
\]

The background makes \(Y_{0,q}(xq^{-2})\to Y_b(0)>0\). The high-frequency
seed enstrophy is \(O(q^{-2})\). For fixed \(q\), define the tangent
coefficients

\[
 M_{m,q}=\lim_{s\to0}s^{-2}J_{m,q}(s),\qquad
 \mathcal B_{r,q}^{(*)}=\lim_{s\to0}s^{-2}B_{r,q}^{(*)}(s),\quad r=1,2.
 \tag{9.2}
\]

Also define

\[
 I_1=\int_A^\infty|\Gamma'(x)|^2\,dx>0,\qquad
 I_2=\int_A^\infty|\Gamma''(x)|^2\,dx>0.
 \tag{9.3}
\]

Split each integral at a fixed rescaled time, use rescaled dominated
convergence on the compact part, and then use the uniform fast/slow
exponential tail bounds. This gives, for every prescribed atom,

\[
 M_{m,q}\asymp\varepsilon_q^2=q^{-4},
 \tag{9.4}
\]

and for the selected singleton target shell,

\[
 \mathcal B_{1,q}^{(*)}\asymp\varepsilon_q^2q^{-2}=q^{-6},\qquad
 \mathcal B_{2,q}^{(*)}\asymp\varepsilon_q^2q^2=q^{-2}.
 \tag{9.5}
\]

After restoring the fixed eigenshell constants,

\[
 \frac{M_{m,q}}{(2/\ell)\mathcal B_{1,q}^{(*)}}\asymp q^2,\qquad
 \frac{M_{m,q}}{(7\ell/3)\mathcal B_{2,q}^{(*)}}\asymp q^{-2}.
 \tag{9.6}
\]

### Theorem 9.1 -- genuine repeated-root failure of first-row-only sampling

For \(N\ge2\), there is a sequence \(u_q\) of smooth global unforced
solutions for which

\[
 \sup_q\left[
 \|u_q(\sigma_q)\|_2^2+\|\omega_q(\sigma_q)\|_2^2
 +\frac{\sup_KY_q}{\inf_KY_q}\right]<\infty,
 \qquad
 \frac{J_{2,q}}{\ell^{-1}B_{1,q}^{(*)}}\longrightarrow\infty.
 \tag{9.6a}
\]

Here \(\sigma_q\) is the launch time in (8.2), and \(J_{2,q}\) is the atom
at the second prescribed root. Consequently there is no constant depending
only on the fixed annular data and the three displayed uniform bounds such
that every smooth unforced solution
satisfies the R0.71U zero-atom estimate for every permissible finite shell
selection after deleting \(B_2\) and retaining only the same selected
\(\ell^{-1}B_1\) row. The singleton selection containing only the target
shell already fails. The failure remains if the first prescribed root in that
shell is separately paid, because the second root already has (9.6).

For each fixed \(q\), (8.6b) gives an exact curve with all prescribed roots.
Write \(c_q=p_q'(0)\). Convergence of the interpolation matrices gives
\(c_q\to c_\infty\), so \(\sup_q|c_q|<\infty\). First take \(s\to0\) at
fixed \(q\). Then choose \(s_q\ne0\) inside the IFT radius so that its
\(C^2\) target tangent error is small relative to every prescribed root
slope, every internal limiting lobe height, and the nonzero terminal tail,
and so that

\[
 \left|\frac{p_q(s_q)}{s_q}-p_q'(0)\right|\le1,
 \qquad |p_q(s_q)|\le C|s_q|.
 \tag{9.7}
\]

Simultaneously require

\[
 s_qq\to0.
 \tag{9.8}
\]

This diagonal choice is possible because only finitely many positive
quantities occur for each fixed \(q\). It preserves simplicity of the exact
prescribed roots, the sign of each intervening lobe, and the absence of an
additional terminal root. Hence the tangent ratios in (9.6) pass to the exact
solutions.

At the launch time \(\sigma_q\), seed enstrophy is \(O(q^{-2})\), shear
enstrophy is \(O(s_q^2q^2)\) by (9.7), and the background is fixed. Launch
energy and enstrophy are therefore uniformly bounded. For the passive scalar
part, the exact energy estimate

\[
 \frac d{dt}\|\nabla f\|_2^2
 \le2\|v_y\|_\infty\|\nabla f\|_2^2,
 \qquad
 \int_{\sigma_q}^{b}\|v_y\|_\infty\,dt
 \le C\sum_l\frac{|p_{l,q}(s_q)|}{n_{l,q}}
 =O(|s_q|/q)
 \tag{9.9}
\]

gives a uniform upper bound throughout \(K\). On the relative-time interval
corresponding to \(K\),
the background contribution
\(Y_b(\theta)=2Q^2B^2e^{-2\nu Q^2\theta}\) stays between two fixed positive
constants and is spectrally disjoint from the seed, so it also gives the
uniform lower bound. Hence \(\sup_KY/\inf_KY\) is uniformly bounded. The
diagonal sequence therefore consists of exact globally smooth unforced NSE
solutions, satisfies (9.6a), and proves the theorem.

This does not exclude a variant with an explicit trace payment for every
root, a uniform interior-persistence condition, or the complete fixed-frame
ledger in which the decoupled background contributes through other shells
and through the global \(\nu^2\) baseline.

## 10. The same NSE family collapses excursion nondegeneracy

For an internal component between two prescribed roots, the simple limiting
slopes and nonzero lobe height just established give two-sided bounds

\[
 h_{E,q}\asymp |s_q|\varepsilon_qq^{-2},\qquad
 Y_E\asymp q^{-2},\qquad
 s_E\asymp |s_q|\varepsilon_q,qquad Y(t_E)\asymp1,
 \tag{10.1}
\]

so

\[
 D_{E,q}\asymp q^{-2}.
 \tag{10.2}
\]

For the last component, the nonzero limiting tail and the diagonal sign
control make the component extend to \(b\). Thus

\[
 h_{E,q}\asymp |s_q|\varepsilon_qq^{-2},\qquad
 Y_E\asymp1,\qquad s_E\asymp |s_q|\varepsilon_q,qquad
 D_{E,q}\asymp q^{-4}.
 \tag{10.3}
\]

On one target eigenshell,

\[
 J_{E,q}=\frac{\kappa_*^4}{\rho^4}
 D_{E,q}^{-1}H_{E,q}^2.
 \tag{10.4}
\]

In particular, for the last component,

\[
 H_{E,q}^2\asymp s_q^2q^{-8},\qquad
 J_{E,q}\asymp s_q^2q^{-4}.
 \tag{10.5}
\]

Thus bounded smooth NSE dynamics does not supply a uniform \(D_E\) lower
bound.

## 11. Mollifier boundary and noncommuting limits

Let \(\rho\in C_c^\infty((0,1))\), \(\rho\ge0\), \(\int\rho=1\), and use
the R0.71T outgoing occupation mollifier. Along a fixed recurrence curve,

\[
 r_s=|s|R_g+O(s^2),\qquad q_s=s^2Q_g+O(s^3).
 \tag{11.1}
\]

Three regimes differ:

1. \(\delta/|s|\to\infty\): the positive band eventually lies above the
   entire excursion and the occupation is zero.
2. \(\delta=\eta|s|\): the occupation is
   \(s^2\mathcal B_g(\eta)+O(s^3)\).
3. \(\delta/|s|\to0\): the simple-root boundary trace recovers the
   \(s^2\) atom coefficient.

Hence

\[
 \lim_{\delta\downarrow0}\lim_{s\to0}s^{-2}\mathcal B_\delta(s)=0,\qquad
 \lim_{s\to0}s^{-2}\lim_{\delta\downarrow0}\mathcal B_\delta(s)=M_2>0.
 \tag{11.2}
\]

The limits do not commute. In the high-\(q\) family, the leading excursion
height is \(O(|s|q^{-4})\); even a band of size \(\eta|s|\) with fixed
\(\eta>0\) eventually misses it.

## 12. Primary-literature boundary

The checked sources support the surrounding interfaces, not the complete
R0.71V theorem.

1. [Federer, *Geometric Measure Theory*, §3.2.3,
   p.243](https://doi.org/10.1007/978-3-642-62010-2) gives the weighted
   Lipschitz area formula with multiplicity. In one dimension the
   \(W^{1,1}=AC\) version in Section 5 follows by the standard
   absolutely-continuous/finite-variation extension; it is not §3.2.3
   applied verbatim outside its Lipschitz hypotheses. Both versions are
   integrated over the level and do not supply a prescribed boundary trace.
2. [Banach (1925), p.228, Théorème
   2](https://doi.org/10.4064/fm-7-1-225-236) identifies total variation
   with the level integral of the indicatrix.
3. [Bertoin--Yor (2014), Theorem 1, journal
   p.555](https://doi.org/10.1112/blms/bdu014) gives occupation densities
   for finite-variation paths as \(L^1\) level objects. The recent
   [Hove--Mhlanga--Łochowski--Zondi, Theorem
   2.8](https://doi.org/10.4064/cm9372-11-2025) retains the same
   level-integrated boundary.
4. [Łochowski (2017), Theorem 1, journal
   pp.304--305](https://doi.org/10.4064/cm6583-3-2017) represents upward,
   downward, and truncated variation through positive-band crossings.
5. [Biferale--Buzzicotti--Linkmann (2017), §II, equations (1)--(2),
   manuscript p.2](https://doi.org/10.1063/1.4990082) records the exact
   2D3C reduction, not the triangular prescribed-recurrence construction.
6. [Karlin--Studden, *Tchebycheff
   Systems*](https://books.google.com/books?id=P7Y-AAAAIAAJ), Chapters I
   and XI, supplies the standard T-system determinant and zero-count
   machinery, not the particular NSE response family or its asymptotics.
7. [Leray (1934), p.235, equation (5.9), and
   p.241](https://doi.org/10.1007/BF02547354), together with
   [Temam, equation (3.2), p.17, Theorem 3.1, p.21, and Remark 3.2,
   p.22](https://doi.org/10.1137/1.9781611970050), supplies the weak energy
   framework, not \(C_{tt}\), \(\omega_t\), or \(L_t\) control.
8. [Doering--Gibbon, p.129, equations (6.5.1)--(6.5.3), and p.131,
   equation (6.5.13)](https://doi.org/10.1017/CBO9780511608803) records the
   rotational, energy, and enstrophy identities.
   [Gibbon--Holm, equation (1.3)](https://arxiv.org/abs/1012.3597) uses the
   common Lamb-vector convention \(D_{\rm Lamb}=\omega\times u\).
   Consequently the report's
   \(L=\mathbb P(u\times\omega)=-\mathbb P D_{\rm Lamb}\) is the projected
   rotational nonlinearity appearing with a plus sign in
   \(u_t=\nu\Delta u+L\).

The bounded search found no theorem promoting the cited level-integrated
control to a fixed zero-level quadratic trace without a reverse-average,
uniform modulus, or persistence hypothesis. This is a scoped literature
finding, not an originality, priority, or nonexistence claim.

## 13. Computational corroboration boundary

The formal figure evaluates the closed response sums for

\[
 \nu=0.02,\quad K_y=K_z=1,\quad d=8,\quad
 (r_1,\ldots,r_5)=(1,\ldots,5),
 \tag{13.1}
\]

with two scaled roots. Rescaled quadrature checks the predicted powers
\(q^{-4},q^{-6},q^{-2},q^{-2},q^{-4}\), and \(q^{-8}\) for the atom,
first row, second row, internal \(D_E\), terminal \(D_E\), and terminal
excursion charge. An independent implementation reconstructs the response
solve, branch maxima, and regression exponents.

The computation uses finite sums and one-dimensional quadrature. It does not
time-step NSE, prove the IFT, control the nonlinear remainder uniformly in
\(q\), or establish global regularity. The analytic diagonal argument
supplies the exact smooth trajectories.

## 14. Exact result boundary

### Proved in R0.71V

1. compact global-shell coefficients have absolutely continuous
   representatives at the Leray--Hopf level;
2. the scale-zero excursion-height packing theorem, its Leray payment, and
   its threshold count;
3. the exact classical factor \(D_E\) converting excursion height to the
   root-slope jet;
4. the area-formula hierarchy: linear slope is \(L_t^2\)-paid, while
   quadratic slope carries a cubic occupation Jacobian;
5. the exact sine fixed-level obstruction;
6. fixed-\(N\) tangent coefficients for the atom and both time-jet rows;
7. cancellation of passive scalar amplitude from fixed-data leading
   normalized coefficients when no background is present;
8. a fixed-target, fixed-window, smooth unforced 2.5D NSE sequence that
   defeats first-row-only sampling even after the first root is paid;
9. uniform initial energy, enstrophy, and enstrophy-ratio bounds for that
   sequence;
10. \(D_E\asymp q^{-2}\) on internal shrinking components and
    \(D_E\asymp q^{-4}\) on the terminal component;
11. noncommutation of zero-level and collapsing-amplitude limits.

### Not proved

1. sharpness of the R0.71U second-time coefficient or exact row;
2. impossibility of every alternative Leray-paid zero-atom estimate,
   especially one retaining the global \(\nu^2\) baseline;
3. control of \(C_{tt}\), \(\omega_t\), or \(L_t\) by ordinary Leray energy;
4. a zero-jet definition at arbitrary weak zero times;
5. a localized-cell theorem with cutoff commutators;
6. a single fixed trajectory with infinite prescribed recurrence;
7. a continuation criterion, finite-time singularity, or global regularity.

## 15. Route verdict and next finite gate

R0.71V separates three objects that cannot be exchanged silently.

1. Normalized excursion height has an unconditional, scale-zero,
   Leray--Hopf packing law.
2. The quadratic zero-slope atom is a boundary trace. Ordinary level
   integration either loses one slope or demands cubic time occupation.
3. A genuine repeated-root NSE boundary layer makes root slopes much larger
   than the height they produce. It defeats first-row-only sampling and a
   uniform excursion-to-atom noncollapse hypothesis.

R0.71W should test whether the complete global \(\nu^2\) baseline and the
projected rotational term can pay the fixed-target high-frequency events
after the decoupled background is removed or balanced. A negative result must
keep atom mass noncollapsing relative to that complete Leray ledger. A
positive result needs a new dynamical inequality, not a fixed-level trace
inferred from \(L^1\) occupation alone.
