# R0.75G -- exact gain threshold for the signed collar flux

## 0. Result and exact boundary

R0.75F proves that direct modal phase substitution is circular: it
reconstructs the off-diagonal part of the same localized energy identity.
The next question is therefore quantitative. How much genuinely new
decorrelation or residence-time gain would be sufficient to close the
remaining R0.75E flux?

For the frozen common shear, define the local cubic atoms `p_b,p_F` as in
R0.75D and retain the positive signed flux
`mathfrak X_{xi,R}` from R0.75E. Suppose an independent dynamical argument
were to prove

\[
 \mathfrak X_{\xi,R}(F,b)
 \le C R^\alpha p_b^{1/3}p_F^{2/3}.
 \tag{G.1}
\]

Then the exact sufficient threshold is

\[
 \boxed{
 \alpha>\alpha_*:=1-\frac{c_\gamma}{3\rho}
 =\frac{27163}{107163}
 \approx0.2534736803.}
 \tag{G.2}
\]

In particular, an `R^(1/3)` gain is sufficient, with strict exponential
margin

\[
 \frac{\rho}{6}-\frac{c_\gamma}{12}
 =-\frac{4279}{238140000}<0.
 \tag{G.3}
\]

An `R^(1/4)` gain is not sufficient for this reduction: its coefficient
still has positive exponential rate

\[
 \frac{3\rho}{16}-\frac{c_\gamma}{12}
 =\frac{1489}{1905120000}>0.
 \tag{G.4}
\]

This is a sharp threshold for the particular sufficient estimate (G.1),
not a proof of (G.1), not a necessary condition for every conceivable
proof of E.24, and not a counterexample at or below the threshold.

## 1. Frozen inputs and atoms

The note is bound to the following snapshots.

| input | SHA-256 | role |
|---|---|---|
| `research/r075c_background_shear_packing_false_positive.md` | `1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89` | common-shear size and collar volume |
| `research/r075d_passive_gradient_route_screen.md` | `54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6` | local cubic atoms and absolute Holder bound |
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` | signed off-diagonal flux and target E.24 |
| `research/r075f_modal_phase_integration_identity.md` | `f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440` | phase-substitution and positivity-only no-go |

Retain

\[
 R=\exp\!\left(-\frac\rho4L^2\right),\qquad
 \omega=\exp\!\left(-\frac{c_\gamma}{4}L^2\right),
 \qquad
 \rho=\frac9{10000},\quad c_\gamma=\frac8{3969}.
 \tag{G.5}
\]

On the outer collar cylinder, put

\[
 \begin{aligned}
 p_b&:=R^{-2}\omega
  \int_{I_{2R}}\!\int_{\operatorname {supp}\xi}|b|^3,\\
 p_F&:=R^{-2}\omega
  \int_{I_{2R}}\!\int_{\operatorname {supp}\xi}|F|^3.
 \end{aligned}
 \tag{G.6}
\]

The nonnegative scale-`2R` exterior velocity row gives

\[
 p_b+p_F\le C P_R^M.
 \tag{G.7}
\]

The absolute estimate in R0.75D is the zero-gain case

\[
 \mathfrak X_{\xi,R}
 \le C p_b^{1/3}p_F^{2/3}.
 \tag{G.8}
\]

## 2. Exact size of the frozen background atom

The time interval has length `O(R^2)`, the collar has spatial volume
`O(L^2 R^3)`, and the calibrated shear obeys `|b| <= C R^(-2)`.
Therefore

\[
 \begin{aligned}
 p_b
 &\le C R^{-2}\omega
 (R^2)(L^2R^3)(R^{-6})\\
 &\le C L^2\omega R^{-3}.
 \end{aligned}
 \tag{G.9}
\]

R0.75C supplies the matching lower bound on a fixed positive cap, but only
the upper bound in (G.9) is needed for the sufficient implication below.
Taking a cube root gives

\[
 p_b^{1/3}\le C L^{2/3}\omega^{1/3}R^{-1}.
 \tag{G.10}
\]

## 3. Proof of the threshold

Assume (G.1). By (G.7) and (G.10),

\[
 \begin{aligned}
 \mathfrak X_{\xi,R}
 &\le C R^\alpha p_b^{1/3}p_F^{2/3}\\
 &\le C L^{2/3}\omega^{1/3}R^{\alpha-1}
 (P_R^M)^{2/3}.
 \end{aligned}
 \tag{G.11}
\]

The exponential rate of its coefficient is

\[
 \lim_{L\to\infty}\frac1{L^2}
 \log\!\left(
 L^{2/3}\omega^{1/3}R^{\alpha-1}
 \right)
 =\frac{(1-\alpha)\rho}{4}-\frac{c_\gamma}{12}.
 \tag{G.12}
\]

It is strictly negative exactly when

\[
 3(1-\alpha)\rho<c_\gamma,
 \qquad
 \alpha>1-\frac{c_\gamma}{3\rho}.
 \tag{G.13}
\]

The rational evaluation is

\[
 1-\frac{(8/3969)}{3(9/10000)}
 =1-\frac{80000}{107163}
 =\frac{27163}{107163}.
 \tag{G.14}
\]

At equality, the exponential rate is zero but the displayed factor
`L^(2/3)` still grows, so the strict inequality in (G.2) is essential for
this unrefined estimate. Substitution of `alpha=1/3` and `alpha=1/4`
into (G.12) gives (G.3) and (G.4), respectively.

Combining (G.11) with R0.75E (E.22) proves the conditional implication

\[
 \boxed{
 \text{(G.1) for some }\alpha>\alpha_*
 \quad\Longrightarrow\quad
 D_{k,R}^{{\rm out},F}
 \le C(P_R^M)^{2/3}.}
 \tag{G.15}
\]

## 4. Amplitude scaling cannot create the missing gain

For a fixed shear and any `A>0`, replace `F` by `AF`. Then

\[
 \mathfrak X_{\xi,R}(AF,b)=A^2\mathfrak X_{\xi,R}(F,b),
 \qquad
 p_{AF}^{2/3}=A^2p_F^{2/3}.
 \tag{G.16}
\]

Consequently the dimensionless correlation ratio

\[
 \mathscr C_R(F,b)
 :=\frac{\mathfrak X_{\xi,R}(F,b)}
 {p_b^{1/3}p_F^{2/3}}
 \tag{G.17}
\]

is invariant under passive-field amplitude scaling whenever the
denominator is nonzero. Use `mathscr C_R=0` when the signed numerator is
zero. Thus the missing factor in (G.1) must come from sign, phase,
dynamics, or geometry; it cannot come from renormalizing the passive
amplitude. R0.75E's horizontal zero sector has `mathscr C_R=0` exactly.

## 5. Residence-time interpretation and its exact exponent

Suppose a future argument replaces the full background atom in the
interaction estimate by a nonnegative interaction atom
`p_b^int` satisfying

\[
 \mathfrak X_{\xi,R}
 \le C(p_b^{\rm int})^{1/3}p_F^{2/3},
 \qquad
 p_b^{\rm int}\le C R^\beta p_b.
 \tag{G.18}
\]

Then (G.1) holds with `alpha=beta/3`. The exact threshold becomes

\[
 \boxed{
 \beta>\beta_*:=3\alpha_*
 =\frac{27163}{35721}
 \approx0.7604210408.}
 \tag{G.19}
\]

The calibrated plateau speed is comparable to `R^(-2)`. During one
unwrapped passage, a monotone real lift crossing an interval of width
`O(R)` has the deterministic occupation bound

\[
 |\{t:q(t)\in J_R\}|
 \le\frac{|J_R|}{\inf|q'|}
 \le C R^3.
 \tag{G.20}
\]

Relative to the full `O(R^2)` window, this is a fraction `O(R)`, formally
corresponding to `beta=1` and hence `alpha=1/3`. This kinematic count
explains the favorable margin (G.3), but it does not prove (G.18) for an
arbitrary diffusing and interfering passive field.

## 6. Exact transport benchmark and the diffusion obstruction

For comparison, let `H` solve the one-dimensional pure transport equation

\[
 \partial_tH+b(t)\partial_2H=0
 \tag{G.21}
\]

with spatially constant drift and a fixed smooth cutoff `xi`. Direct
integration gives

\[
 \frac12\frac d{dt}\int\xi|H|^2
 =\frac12\int b(t)\partial_2\xi|H|^2,
 \tag{G.22}
\]

and therefore

\[
 \frac12\int_s^t\!\int b\partial_2\xi|H|^2
 =\frac12\int\xi|H(t)|^2
 -\frac12\int\xi|H(s)|^2.
 \tag{G.23}
\]

The full-window absolute Holder estimate loses this exact crossing
cancellation. With diffusion restored, however, the localized identity
also contains the very dissipation being estimated. Solving that identity
for the flux merely reproduces R0.75F (F.17)--(F.18). Thus (G.23) is a
benchmark for the desired mechanism, not a proof for the passive
advection-diffusion problem.

## 7. Minimum next proposition and falsification gates

The numerically comfortable target is now explicit:

\[
 \boxed{
 \mathfrak X_{\xi,R}(F,b)
 \le C R^{1/3}p_b^{1/3}p_F^{2/3}.}
 \tag{G.24}
\]

A proof may split the plateau and shear-transition regions, but it must
pass all of the following gates.

1. **Dynamic gate.** The gain must hold for the total passive solution,
   not only for one preselected packet or a static trigonometric family.
2. **Diffusion gate.** Brownian/heat recrossing and vertical diffusion must
   be included without moving the unknown dissipation to the other side.
3. **Geometry gate.** The spherical collar, its `x_1` averaging, all
   periodic copies, and the regions where the radial normal is nearly
   transverse to the drift must remain in the estimate.
4. **Transition gate.** The bands where `b` is small or changes sign must
   be paid using their smaller geometry or an independent shear estimate.
5. **Payment gate.** Any interaction atom in (G.18) must be bounded from
   Version-M rows already present; it cannot assume E.24 or the desired
   dissipation bound.

The alternatives are equally informative: either prove (G.24), prove a
weaker (G.1) with any `alpha>alpha_*`, or construct an exact frozen-family
sequence for which `R^(-alpha_*) mathscr C_R` is unbounded. None of those
three outcomes is established here.

## 8. Status boundary

**Proved:** the background upper bound (G.9), the conditional threshold
(G.2), the exact rational margins (G.3)--(G.4), amplitude invariance
(G.16)--(G.17), the residence-exponent conversion (G.18)--(G.19), and the
pure-transport benchmark (G.22)--(G.23).

**Open:** every positive `R^alpha` gain for the arbitrary real frozen
passive family, the interaction atom in (G.18), E.24, complete-clock
extraction, fixed deletion, suitable-weak transfer, and all regularity or
singularity conclusions. No simulation or numerical fit is used.
\(\mathbf{NOT\ CLAY}.\)
