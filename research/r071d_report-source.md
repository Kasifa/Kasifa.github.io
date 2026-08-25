# R0.71D — Complete material heat tents and the critical viscous refinement obstruction

**Date:** 2026-08-25

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, Littlewood--Paley localization, local energy
budgets, and flow-adapted parabolic geometry

**Status:** exact material heat-tent identity, exact smooth NSE obstruction,
and two independent finite certificates; no unconditional regularity theorem,
no singularity construction, and no Millennium-problem claim

## 1. Direct decision

R0.71C left one admissible way to rescue signed-before-square localization:
replace static boxes by material parabolic tents and keep every additive flux.
The hope was that transport, cutoff, pressure, and heat flux might telescope
before the positive part is squared.

R0.71D closes that specific hope in its geometry-only form.

1. A complete heat-extension tent identity does exist.  It retains the
   stretching source, transport--filter commutator, cutoff motion, physical
   time faces, and vertical heat faces with exact signs.
2. Moving a cutoff with a low-frequency flow only replaces the horizontal
   transport by the relative velocity.  It does not remove that flux.
3. Even when the cutoff is an exact material partition, an exact smooth NSE
   shear solution has zero signed parent production and a strictly positive
   refined heat ledger.
4. On a parabolic time interval, this refined ledger is scale critical and
   exactly saturates the R0.71C time-box Cauchy inequality.  There is no
   factor \(k^{-\varepsilon}\) to harvest from the tent geometry.
5. A backward-adjoint cutoff can cancel the heat term, but a nonzero compact
   tent cannot remain compact under the backward parabolic equation.

The conclusion is narrow.  It rules out a universal subcritical gain coming
from material-tent bookkeeping or viscous heat transport alone.  It does not
rule out a special cancellation between the genuinely three-dimensional
stretching, transport--filter, and pressure sectors.

## 2. Heat-extension shell equation

Work on the normalized three-torus.  Let

\[
 \partial_t\omega+u\cdot\nabla\omega-\nu\Delta\omega=S\omega,
 \qquad \nabla\cdot u=0.
 \tag{2.1}
\]

For a real-even Littlewood--Paley block \(T_j\), introduce the heat variable
\(s\ge0\) and define

\[
 A_{j,s}=e^{s\Delta}T_j,
 \qquad W_j(s,t)=A_{j,s}\omega(t),
 \qquad e_j=\frac12|W_j|^2.
 \tag{2.2}
\]

Since \(\partial_sW_j=\Delta W_j\), direct commutation gives

\[
 \boxed{
 (\partial_t+u\cdot\nabla-\nu\partial_s)W_j
 =A_{j,s}(S\omega)+[u\cdot\nabla,A_{j,s}]\omega
 =:G_j.}
 \tag{2.3}
\]

Thus

\[
 \boxed{
 (\partial_t+u\cdot\nabla-\nu\partial_s)e_j=W_j\cdot G_j.}
 \tag{2.4}
\]

The commutator in (2.3) is part of the equation.  Dropping it would replace
NSE by a different filtered dynamics.

## 3. The complete material heat-tent ledger

Let \(I=[t_0,t_1]\), \(0<s<h\), and let
\(\phi(t,x,s)\ge0\) be smooth.  Put

\[
 E_\phi(t,s)=\int_{\mathbb T^3}\phi e_j\,dx.
 \tag{3.1}
\]

Integrating (2.4) by parts in \(t,x,s\) gives the exact identity

\[
 \boxed{
 \begin{aligned}
 &\int_0^h\left[E_\phi(t_1,s)-E_\phi(t_0,s)\right]ds\\
 &\quad+\nu\int_I\left[E_\phi(t,0)-E_\phi(t,h)\right]dt\\
 &=\int_{I\times(0,h)\times\mathbb T^3}
 \left\{
 \phi W_j\cdot G_j
 +e_j(\partial_t+u\cdot\nabla-\nu\partial_s)\phi
 \right\}\,dx\,ds\,dt .
 \end{aligned}}
 \tag{3.2}
\]

The first line records the physical-time faces.  The second line is the
vertical heat flux.  The right side contains the stretching source, the
transport--filter commutator, and every cutoff-motion or sloping-face term.

If a cutoff moves with a smooth low-frequency velocity \(U_j\), write

\[
 (\partial_t+U_j\cdot\nabla-\nu\partial_s)\phi=R_{\rm shape}.
 \tag{3.3}
\]

Then the remaining cutoff term is exactly

\[
 (\partial_t+u\cdot\nabla-\nu\partial_s)\phi
 =(u-U_j)\cdot\nabla\phi+R_{\rm shape}.
 \tag{3.4}
\]

Flow adaptation has therefore reduced the horizontal flux to a relative
velocity.  It has not made that flux zero.

The vertical face has its own exact decomposition:

\[
 \boxed{
 E_\phi(t,0)-E_\phi(t,h)
 =\int_0^h\!\int
 \left(
 \phi|\nabla W_j|^2-e_j\Delta\phi-e_j\partial_s\phi
 \right)dx\,ds.}
 \tag{3.5}
\]

Thus the vertical heat flux is not a new independent positive quantity.  It
contains palinstrophy together with spatial and sloping-boundary leakage.

## 4. Sharp moving-domain and cutoff costs

For a moving physical domain \(D(t)\) with boundary velocity \(V_b\), the
fixed-\(s\) form of (2.4) is

\[
 \begin{aligned}
 \frac d{dt}\int_{D(t)}e_j
\nu\int_{D(t)}|\nabla W_j|^2
={}&\int_{D(t)}W_j\cdot G_j\\
&-\int_{\partial D(t)}e_j(u-V_b)\cdot n
+\nu\int_{\partial D(t)}\partial_ne_j.
 \end{aligned}
 \tag{4.1}
\]

Taking \(V_b=u\) removes the advective boundary flux but leaves the viscous
heat flux.  Meanwhile a material cutoff satisfies

\[
 (\partial_t+u\cdot\nabla)\nabla\phi
 =-(\nabla u)^T\nabla\phi.
 \tag{4.2}
\]

A direct pointwise geometry estimate therefore costs

\[
 \|\nabla\phi(t)\|_\infty
 \le \|\nabla\phi(0)\|_\infty
 \exp\!\left(\int_0^t\|\nabla u(\tau)\|_\infty d\tau\right).
 \tag{4.3}
\]

This is already a Lipschitz/BKM-level control.  Generating the geometry with
a mollified velocity avoids using a rough material indicator, but introduces
the relative-velocity term in (3.4) and requires a skewed-cylinder covering
theorem.

## 5. Bottom cutoff and filter do not commute

If localization is performed before filtering, set

\[
 Z_j=A_{j,s}(\chi\omega).
 \tag{5.1}
\]

Then

\[
 \begin{aligned}
 (\partial_t+u\cdot\nabla-\nu\partial_s)Z_j
={}&A_{j,s}(\chi S\omega)
 +[u\cdot\nabla,A_{j,s}](\chi\omega)\\
&+A_{j,s}\left[
 (D_t\chi-\nu\Delta\chi)\omega
 -2\nu\nabla\chi\cdot\nabla\omega
 \right].
 \end{aligned}
 \tag{5.2}
\]

At \(s=0\),

\[
 Z_j(0)=T_j(\chi\omega)
 =\chi T_j\omega+[T_j,\chi]\omega.
 \tag{5.3}
\]

The exact certificate uses \(f=2a\cos(kx_1)\) and
\(\chi=(1+\rho\cos(2kx_1))/2\).  If the radial multiplier satisfies
\(m_j(k)=m\) and \(m_j(3k)=0\), the \(+3k\) coefficient of
\([T_j,\chi]f\) is

\[
 \boxed{-\frac{\rho ma}{4}.}
 \tag{5.4}
\]

There is no scale-small factor.  For the same reason a localized Bernstein
estimate must use a stabilized dissipation such as

\[
 \widetilde D_{j,\phi}
 =\int\phi|\nabla W_j|^2
 +Cr^{-2}\int_{\operatorname{supp}\nabla\phi}|W_j|^2,
 \tag{5.5}
\]

instead of assuming \(D_{j,\phi}\gtrsim2^{2j}Y_{j,\phi}\) without a boundary
term.

## 6. Exact smooth NSE material witness

For any integer \(k\ge1\), take

\[
 u_k(t,x)
 =\left(0,\frac{A}{k}e^{-\nu k^2t}\sin(kx_1),0\right),
 \tag{6.1}
\]

\[
 \omega_k(t,x)
 =\left(0,0,Ae^{-\nu k^2t}\cos(kx_1)\right).
 \tag{6.2}
\]

This is a smooth exact three-dimensional NSE solution with constant pressure:

\[
 \nabla\cdot u_k=0,
 \quad u_k\cdot\nabla u_k=0,
 \quad u_k\cdot\nabla\omega_k=0,
 \quad S_k\omega_k=0.
 \tag{6.3}
\]

Use the smooth partition

\[
 \phi_\pm=\frac12\left(1\pm\rho\cos(2kx_1)\right),
 \qquad0<\rho<1.
 \tag{6.4}
\]

Because \((u_k)_1=0\), both weights are exactly material:

\[
 (\partial_t+u_k\cdot\nabla)\phi_\pm=0.
 \tag{6.5}
\]

With normalized spatial average, define

\[
 Y_\pm=\int\phi_\pm|\omega_k|^2,
 \qquad
 D_\pm=\int\phi_\pm|\nabla\omega_k|^2,
 \tag{6.6}
\]

\[
 \beta_\pm=\frac12Y_\pm'+\nu D_\pm.
 \tag{6.7}
\]

Exact Fourier averaging gives

\[
 Y_+=\frac{A^2(2+\rho)}8e^{-2\nu k^2t},
 \qquad
 Y_-=\frac{A^2(2-\rho)}8e^{-2\nu k^2t},
 \tag{6.8}
\]

\[
 D_+=\frac{A^2k^2(2-\rho)}8e^{-2\nu k^2t},
 \qquad
 D_-=\frac{A^2k^2(2+\rho)}8e^{-2\nu k^2t},
 \tag{6.9}
\]

\[
 \boxed{
 \beta_+=-\frac{\nu A^2k^2\rho}{4}e^{-2\nu k^2t},
 \qquad
 \beta_- =\frac{\nu A^2k^2\rho}{4}e^{-2\nu k^2t}.}
 \tag{6.10}
\]

For this solution the whole child injection is the viscous cutoff flux:

\[
 \beta_\pm
 =\frac\nu2\int(\Delta\phi_\pm)|\omega_k|^2.
 \tag{6.11}
\]

The stretching, nonlinear transport, pressure, and transport--filter
commutator all vanish.  No uncontrolled term is being hidden.

## 7. Zero parent, positive refinement, critical scaling

The signed parent ledger is exactly zero:

\[
 \beta_++\beta_-=0.
 \tag{7.1}
\]

The refined positive-square ledger is not zero:

\[
 \boxed{
 \delta_k
 =\frac{(\beta_-^+)^2}{D_-}
 =\frac{\nu^2A^2k^2\rho^2}{2(2+\rho)}e^{-2\nu k^2t}>0.}
 \tag{7.2}
\]

Since the parent enstrophy is

\[
 Y=Y_++Y_-=\frac{A^2}{2}e^{-2\nu k^2t},
 \tag{7.3}
\]

the normalized defect is

\[
 \boxed{
 \frac{\delta_k}{Y}
 =\frac{\nu^2\rho^2}{2+\rho}k^2.}
 \tag{7.4}
\]

For every \(\varepsilon>0\), no uniform estimate of the form

\[
 \delta_k\le C\nu^2k^{2-\varepsilon}Y
 \tag{7.5}
\]

can hold on this exact solution family.  Material geometry and viscous heat
exchange therefore supply the critical \(k^2\) cost, not a subcritical gain.

## 8. The parabolic box saturates R0.71C

Take

\[
 \tau_k=\frac\theta{\nu k^2}.
 \tag{8.1}
\]

Writing \(q_\theta=1-e^{-2\theta}\), exact integration yields

\[
 B_-:=\int_0^{\tau_k}\beta_-dt
 =\frac{A^2\rho}{8}q_\theta,
 \tag{8.2}
\]

\[
 \overline D_-:=\int_0^{\tau_k}D_-dt
 =\frac{A^2(2+\rho)}{16\nu}q_\theta.
 \tag{8.3}
\]

Moreover,

\[
 \boxed{
 \frac{B_-^2}{\overline D_-}
 =\int_0^{\tau_k}\frac{(\beta_-^+)^2}{D_-}\,dt
 =\frac{\nu A^2\rho^2}{4(2+\rho)}q_\theta.}
 \tag{8.4}
\]

Equality holds because \(\beta_-/D_-=2\nu\rho/(2+\rho)\) is constant in
time.  The time-box inequality from R0.71C is therefore sharp in exactly the
wrong direction.  Dividing (8.4) by \(\nu Y(0)\) gives

\[
 \boxed{
 \frac{B_-^2}{\nu\overline D_-Y(0)}
 =\frac{\rho^2}{2(2+\rho)}(1-e^{-2\theta}),}
 \tag{8.5}
\]

which is independent of \(k\) and \(\nu\).

## 9. The vertical heat face is exact, not optional

For the witness in Section 6,

\[
 W_j(s,t)=e^{-k^2s}T_j\omega_k(t).
 \tag{9.1}
\]

When \(\phi\) is independent of \(s\), the physical-time loss integrated
over \(0<s<h\) and the vertical boundary flux satisfy

\[
 \int_0^h[E_\phi(\tau_k,s)-E_\phi(0,s)]ds
 +\nu\int_0^{\tau_k}[E_\phi(t,0)-E_\phi(t,h)]dt=0.
 \tag{9.2}
\]

The producer verifies (9.2) symbolically for arbitrary positive
\(A,\nu,k,h,\theta\).  Omitting the vertical face would leave a false
positive budget.

An explicit backward-adjoint Fourier weight,

\[
 \phi(t,x)=\frac12\left[
 1+\rho_Te^{-4\nu k^2(T-t)}\cos(2kx_1)
 \right],
 \tag{9.3}
\]

satisfies

\[
 (\partial_t+\nu\Delta)\phi=0.
 \tag{9.4}
\]

It cancels the heat-cutoff term algebraically.  But a nonzero nonnegative
compact terminal profile becomes strictly positive everywhere at earlier
times by the strong maximum principle.  Exact backward heat balance and
compact tent support cannot both be imposed without another error term.

## 10. Pressure remains a boundary ledger

Pressure is absent from the vorticity equation.  If a localized strain
ledger is used instead, let

\[
 \Sigma_j=A_{j,s}S,
 \qquad U_j=A_{j,s}u,
 \qquad p_j=A_{j,s}p.
 \tag{10.1}
\]

The pressure Hessian contribution localizes as

\[
 \boxed{
 \int\phi\,\Sigma_j:\nabla^2p_j
 =\int(\Delta p_j)U_j\cdot\nabla\phi
 +\int (U_j)_i(\partial_kp_j)(\partial_{ik}\phi).}
 \tag{10.2}
\]

Global pressure orthogonality has become a same-scale boundary term.  The
dissipation-assisted estimates from R0.69N--R0.69O may absorb this sector
under their hypotheses, but they do not cancel the heat obstruction in
(7.2).

## 11. Exact theorem and boundary

### Theorem 11.1 — material heat-tent critical obstruction

For every \(\nu>0\), every integer \(k\ge1\), and every
\(0<\rho<1\), the smooth NSE solution (6.1)--(6.2) and material partition
(6.4) satisfy:

1. the complete ledger (3.2), including its vertical face;
2. zero parent signed injection (7.1);
3. strictly positive refined ledger (7.2);
4. critical normalized scaling (7.4);
5. exact parabolic time-box equality (8.4).

Consequently, no universal estimate that depends only on material-tent
geometry and viscous heat transport can improve the critical factor \(k^2\)
by \(k^{-\varepsilon}\), for any \(\varepsilon>0\).

**Proof.**  Equations (2.3), (3.2), and (3.5) follow by exact commutation and
integration by parts.  Equations (6.8)--(6.11) follow from the Fourier
averages of \(\cos^2(kx_1)\), \(\sin^2(kx_1)\), and
\(\cos(2kx_1)\cos^2(kx_1)\).  Substitution gives (7.1)--(7.4).  Direct time
integration on (8.1) gives (8.2)--(8.4).  The independent checker reconstructs
the averages and also compares them with numerical quadrature.  \(\square\)

The theorem does **not** show that every adaptive tent defect diverges.  It
does not make a singular NSE solution, prove that a useful nonlinear
compensation is impossible, or obtain an unconditional continuation bound.
It rejects only the geometry-only mechanism stated above.

## 12. Literature boundary and research value

The primary-source matrix in `r071d_literature_audit.md` gives the detailed
claim ledger.  The nearest overlap found is Yu's 2026 conditional
moving-window defect-cascade preprint.  It already combines pressure, flux,
energy, trace, and Carleson packing, but leaves the genuine NSE depletion and
moving-window closure as assumptions.  Tao supplies large-data moving local
energy/enstrophy estimates; Yang and Vasseur--Yang supply skewed-cylinder
geometry; Caffarelli--Kohn--Nirenberg supplies the suitable local energy
framework; Koch--Tataru supplies a heat-tent Carleson precedent.

I found no primary source proving the simultaneous closure needed here:
complete transport, Littlewood--Paley commutator, pressure and viscous heat
flux on flow-adapted tents, followed by a vanishing or summable estimate for
the R0.71C signed refinement defect.  That is a bounded negative search
finding, not a novelty or priority proof.

The value of R0.71D is a rigorous route elimination.  It prevents a false
claim that moving geometry or vertical heat balance automatically converts
signed cancellation into a subcritical estimate.  It also leaves a cleaner
open target: any successful next theorem must use a specifically NSE
correlation, not additive tent bookkeeping.

## 13. Next justified gate: R0.71E

R0.71E should isolate the sectors that vanish on the shear witness but are
present in a genuinely three-dimensional flow:

\[
 [u\cdot\nabla,A_{j,s}]\omega,
 \qquad A_{j,s}(S\omega),
 \qquad \text{localized pressure boundary terms}.
 \tag{13.1}
\]

The geometry should be generated by a mollified low-frequency flow and
audited against Yang-type skewed-cylinder covering.  An acceptable positive
result must produce a vanishing or summable defect estimate strictly below
known Serrin, BMO/Besov, or dissipation-wavenumber criteria.  If every bound
returns to those hypotheses, the route should be recorded as another exact
no-go rather than promoted as progress toward global regularity.

## 14. Reproduction

Producer:

```bash
PYTHONDONTWRITEBYTECODE=1 tmp/r068b-venv/bin/python research/r071d_exact_audit.py
```

Independent checker:

```bash
PYTHONDONTWRITEBYTECODE=1 tmp/r068b-venv/bin/python research/r071d_independent_audit.py
```

The archived JSON outputs, commands, environment, source hashes, and formal
figure package are stored under `research/certificates/r071d/` and
`figures/r071d-material-heat-tent/`.
