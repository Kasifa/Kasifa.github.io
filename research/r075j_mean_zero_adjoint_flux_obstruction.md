# R0.75J -- mean-zero adjoint obstruction for the signed collar flux

## 0. Result and exact boundary

R0.75H leaves open a Feynman--Kac or resolvent treatment of the signed
diffusive collar flux, and R0.75I shows that one short block is not the
difficulty.  The present note tests the most direct adjoint construction.

Let

\[
 \mathcal L:=\partial_t+b(t,x_3)\partial_2-\Delta_{23},
 \qquad
 \mathcal L^*:=-\partial_t-b(t,x_3)\partial_2-\Delta_{23}.
 \tag{J.1}
\]

For the exact flux source

\[
 a(t,x):=\eta_R(t)b(t,x_3)\partial_2\xi(x),
 \tag{J.2}
\]

consider the zero-terminal adjoint problem

\[
 \mathcal L^*\psi=a,
 \qquad \psi(t_2)=0.
 \tag{J.3}
\]

The source has zero `(x_2,x_3)` mean for every fixed `(t,x_1)`.  Hence so
does `psi`.  Therefore, unless `a` vanishes identically, the exact adjoint
weight cannot be nonnegative:

\[
 \boxed{
 a\not\equiv0
 \quad\Longrightarrow\quad
 \psi\text{ changes sign.}}
 \tag{J.4}
\]

For a real passive solution `mathcal L F=0`, exact duality gives

\[
 \boxed{
 \mathcal T_{\xi,\eta}(F,b)
 =\frac12\int\psi(s)|F(s)|^2
 -\int_s^{t_2}\!\int\psi|\nabla_{23}F|^2.}
 \tag{J.5}
\]

Thus the negative part of `psi` places an uncontrolled positive
dissipation term on the upper-bound side.  Adding a constant to make the
weight nonnegative is not free: the exact global energy identity cancels
that constant when all terms are retained, while dropping the favorable
dissipation creates a boundary surcharge equal to that constant times the
global energy drop.

Consequently an exact zero-terminal adjoint inversion of the signed source
does not by itself improve R0.75F/H.  A viable adjoint argument must instead
construct a **nonnegative majorant** whose initial/source boundary row is
independently paid.  This note proves the obstruction and the required
replacement architecture; it does not construct the paid majorant or close
E.24.

## 1. Frozen setting

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` | passive equation and exact signed flux |
| `research/r075f_modal_phase_integration_identity.md` | `f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440` | algebraic circularity boundary |
| `research/r075h_single_pass_transport_flux_closure.md` | `849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9` | pure-transport endpoint mechanism and diffusive remainder |
| `research/r075i_diffusion_safe_block_participation.md` | `c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7` | diffusion-safe one-block bound and multi-block gate |

Work on `[s,t_2] times T^3`.  The passive field is independent of `x_1`,
the shear `b=b(t,x_3)` is independent of `x_1,x_2`, and all functions are
smooth and periodic.  The cutoff `xi` may depend on all spatial variables.
The signed flux is

\[
 \mathcal T_{\xi,\eta}(F,b)
 :=\frac12\int_s^{t_2}\!\int_{\mathbb T^3}
 a(t,x)|F(t,x_2,x_3)|^2\,dxdt.
 \tag{J.6}
\]

The note is an exact smooth identity.  No backward well-posedness for the
passive equation is assumed: (J.3) is an ordinary backward adjoint problem,
equivalently a forward parabolic problem after reversing time.

## 2. Zero-mean forcing and sign change

For every fixed `(t,x_1)`, periodicity and independence of `b` from `x_2`
give

\[
 \begin{aligned}
 \int_{\mathbb T^2_{23}}a(t,x_1,x_2,x_3)\,dx_2dx_3
 &=\eta_R(t)\int_{\mathbb T_{x_3}}b(t,x_3)
 \left(\int_{\mathbb T_{x_2}}\partial_2\xi\,dx_2\right)dx_3\\
 &=0.
 \end{aligned}
 \tag{J.7}
\]

Integrating (J.3) over `(x_2,x_3)` removes both the periodic Laplacian and
the divergence-free shear drift.  Hence

\[
 -\frac d{dt}\int_{\mathbb T^2_{23}}\psi(t,x)\,dx_2dx_3=0.
 \tag{J.8}
\]

The terminal condition gives

\[
 \boxed{
 \int_{\mathbb T^2_{23}}\psi(t,x_1,x_2,x_3)\,dx_2dx_3=0
 \quad\text{for every }(t,x_1).}
 \tag{J.9}
\]

If `psi>=0`, (J.9) and continuity force `psi=0`.  Equation (J.3) would
then force `a=0`.  This proves (J.4).  More precisely, whenever the exact
adjoint solution is nonzero at a time slice, it has both a positive and a
negative spatial part on that slice.

This conclusion uses the physical derivative source.  Replacing `a` by
`|a|` or `a_+` changes the equation and loses the signed cancellation that
the route was meant to exploit.

## 3. Exact duality and reappearance of dissipation

Set

\[
 g:=|F|^2.
 \tag{J.10}
\]

Since `mathcal L F=0` and `F` is real,

\[
 \mathcal Lg=-2|\nabla_{23}F|^2.
 \tag{J.11}
\]

Periodic integration by parts gives the general duality formula

\[
 \begin{aligned}
 \int_s^{t_2}\!\int g\,\mathcal L^*\phi
 ={}&\int_{\mathbb T^3}\phi(s)g(s)
 -\int_{\mathbb T^3}\phi(t_2)g(t_2)\\
 &+\int_s^{t_2}\!\int\phi\,\mathcal Lg.
 \end{aligned}
 \tag{J.12}
\]

Substituting `phi=psi`, (J.3), (J.6), and (J.11) yields (J.5).  Decomposing
`psi=psi_+-psi_-` gives the valid but nonclosing upper bound

\[
 \mathcal T_{\xi,\eta}
 \le\frac12\int\psi_+(s)|F(s)|^2
 +\int_s^{t_2}\!\int\psi_-|\nabla_{23}F|^2.
 \tag{J.13}
\]

The second row is a positive weighted portion of the passive dissipation.
No Version-M cubic payment for it is proved here.  Thus the exact adjoint
representation has moved, rather than removed, the H.28 obstruction.

## 4. Why a positive constant shift is not free

Let

\[
 E(t):=\int_{\mathbb T^3}|F(t)|^2,
 \qquad
 D:=\int_s^{t_2}\!\int_{\mathbb T^3}|\nabla_{23}F|^2.
 \tag{J.14}
\]

The global passive energy identity is

\[
 E(s)-E(t_2)=2D.
 \tag{J.15}
\]

Choose any constant `C>=||psi_-||_infinity` and set `phi=psi+C>=0`.
Since `mathcal L^*C=0`, the source remains exactly `a`, but the terminal
value becomes `phi(t_2)=C`.  Formula (J.12) now gives

\[
 \begin{aligned}
 \mathcal T_{\xi,\eta}
 ={}&\frac12\int(\psi(s)+C)|F(s)|^2
 -\frac C2E(t_2)\\
 &-\int_s^{t_2}\!\int(\psi+C)|\nabla_{23}F|^2.
 \end{aligned}
 \tag{J.16}
\]

The constant contribution to the exact right-hand side is

\[
 \frac C2\bigl(E(s)-E(t_2)\bigr)-CD=0
 \tag{J.17}
\]

by (J.15).  Thus the shift produces no new exact information.  If one uses
`phi>=0` and discards the last nonpositive row in (J.16), the resulting
upper bound pays the surcharge

\[
 \frac C2\bigl(E(s)-E(t_2)\bigr)=CD.
 \tag{J.18}
\]

That is a global energy-drop/dissipation row.  It is not the desired local
cubic payment and cannot be assumed away.  The same cancellation occurs
for any homogeneous adjoint correction once its own boundary and
dissipation terms are retained.

## 5. The admissible replacement: a paid positive majorant

The obstruction does not rule out every adjoint method.  Suppose one can
construct a nonnegative `Phi` such that

\[
 a\le\mathcal L^*\Phi,
 \qquad \Phi\ge0,
 \qquad \Phi(t_2)\ge0.
 \tag{J.19}
\]

Since `g>=0`, (J.11)--(J.12) imply

\[
 \begin{aligned}
 \mathcal T_{\xi,\eta}
 &\le\frac12\int_s^{t_2}\!\int g\,\mathcal L^*\Phi\\
 &\le\frac12\int_{\mathbb T^3}\Phi(s)|F(s)|^2.
 \end{aligned}
 \tag{J.20}
\]

The terminal and dissipation terms are now favorable.  The price is the
initial occupation/source row on the right.  Taking `Phi` to be the
zero-terminal adjoint solution driven by `a_+` is the canonical
Feynman--Kac majorant; the parabolic maximum principle makes it
nonnegative.  However, no estimate of its initial row by
`C(P_R^M)^(2/3)` with the required positive `R` gain is proved here.

Thus the next valid proposition is precise: build a majorant satisfying
(J.19) whose boundary row in (J.20) is paid by existing Version-M atoms,
including the plateau/transition and periodic-copy geometry.  Exact
inversion of the signed mean-zero source is not a substitute for that
estimate.

## 6. Status boundary

**Proved:** zero mean of the physical flux source J.7; zero mean and forced
sign change of its exact zero-terminal adjoint J.8--J.9; the dual identity
J.12--J.13; exact cancellation and global-energy surcharge under a constant
positivity shift J.14--J.18; and the sufficient positive-majorant
architecture J.19--J.20.

**Not proved:** a paid positive majorant, an occupation estimate with the
required `R^alpha` gain, transition-band control, periodic recrossing,
E.24, complete-clock extraction, fixed deletion, suitable-weak transfer,
or any regularity or singularity conclusion.

This is a structural route-pruning theorem for the frozen smooth passive
problem.  It is not a no-go theorem for all resolvent or Feynman--Kac
methods, uses no simulation or numerical fit, and makes no novelty or
priority claim. \(\mathbf{NOT\ CLAY}.\)
