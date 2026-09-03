# R0.75I -- diffusion-safe block flux and the participation threshold

## 0. Result and exact boundary

R0.75H obtains the required `R^(1/3)` gain for one pure-transport
passage by reducing the full signed flux to a terminal endpoint.  The
present note separates two issues that must not be conflated:

1. payment of the flux on one `O(R^3)` block; and
2. aggregation over the `O(R^(-1))` blocks in the full `O(R^2)` clock.

The first issue is completely insensitive to diffusion.  On every short
block `J_j`, the frozen pointwise bounds and spacetime Holder give

\[
 \boxed{
  \mathfrak X_j
  \le C L^{2/3}\omega^{1/3}R^{-2/3}p_j^{2/3}.}
 \tag{I.1}
\]

No equation for the passive field is used in this estimate.  It therefore
holds, in particular, for every smooth solution of the frozen
advection--diffusion equation.

For a collection of blocks, define the cubic participation count

\[
 N_{\rm eff}
 :=\frac{\left(\sum_jp_j^{2/3}\right)^3}
          {\left(\sum_jp_j\right)^2}.
 \tag{I.2}
\]

Then the exact aggregation loss is `N_eff^(1/3)`.  If

\[
 N_{\rm eff}\le C R^{-\theta},
 \qquad
 \theta<\theta_*:=\frac{8558}{35721}
 \approx0.2395789592,
 \tag{I.3}
\]

the selected-block flux is paid at the target `P^(2/3)` scale for all
sufficiently large `L`.  In contrast, uniform payment across all
`N asymp R^(-1)` blocks has a strictly adverse exponential rate.  Thus
R0.75I reduces the **absolute block-summation route** from "diffusion on
one passage" to a precise occupation/recrossing statement: prove (I.3), or
obtain signed cancellation that is at least as strong.  Small participation
is sufficient, not necessary; a zero-flux sector can have maximal
participation.

This note does **not** prove (I.3) for the frozen passive solution, does not
close E.24, and proves no complete-clock or regularity statement.

## 1. Frozen short-block geometry

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | clock, collar support, cutoff and shear bounds |
| `research/r075c_background_shear_packing_false_positive.md` | `1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89` | total-cubic participation false-positive boundary |
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` | signed flux and Version-M cubic atom |
| `research/r075g_signed_flux_gain_threshold.md` | `f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41` | required gain and residence threshold |
| `research/r075h_single_pass_transport_flux_closure.md` | `849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9` | one-passage benchmark and diffusion boundary |

Retain

\[
 R=\exp\!\left(-\frac\rho4L^2\right),\qquad
 \omega=\exp\!\left(-\frac{c_\gamma}{4}L^2\right),
 \qquad
 \rho=\frac9{10000},\quad c_\gamma=\frac8{3969}.
 \tag{I.4}
\]

The smooth frozen collar cutoff and common shear obey

\[
 |\partial_2\xi|\le C_\xi R^{-1},\qquad
 |\operatorname {supp}\partial_2\xi|
 \le C_\Omega L^2R^3,qquad
 |b|\le C_bR^{-2},
 \tag{I.5}
\]

and `0<=eta_R<=1`.  Let `J_1,...,J_N` be pairwise disjoint time
intervals with

\[
 |J_j|\le C_JR^3.
 \tag{I.6}
\]

Write

\[
 \Omega_\partial:=\operatorname {supp}\partial_2\xi,
 \qquad Q_j:=J_j\times\Omega_\partial.
 \tag{I.7}
\]

Equations (I.5)--(I.6) imply

\[
 |Q_j|\le C L^2R^6.
 \tag{I.8}
\]

The result below only needs these measure and pointwise bounds.  In
particular, it does not use characteristics, a heat kernel, a frequency
cutoff, or a sign for `b`.

## 2. One-block estimate

For an arbitrary real measurable field `F` with finite cubic integral, set

\[
 \begin{aligned}
  \mathcal T_j(F,b)
  &:=\frac12\int_{J_j}\!\int
       \eta_R b\,\partial_2\xi\,|F|^2,\\
  \mathfrak X_j(F,b)
  &:=\frac\omega R[\mathcal T_j(F,b)]_+,\\
  p_j(F)&:=R^{-2}\omega\int_{Q_j}|F|^3.
 \end{aligned}
 \tag{I.9}
\]

The pointwise bounds give

\[
 |\mathcal T_j|
 \le C R^{-3}\int_{Q_j}|F|^2.
 \tag{I.10}
\]

Spacetime Holder on `Q_j`, followed by (I.8), yields

\[
 \int_{Q_j}|F|^2
 \le |Q_j|^{1/3}
       \left(\int_{Q_j}|F|^3\right)^{2/3}
 \le C L^{2/3}R^2
       \left(\int_{Q_j}|F|^3\right)^{2/3}.
 \tag{I.11}
\]

Substitution of

\[
 \int_{Q_j}|F|^3=R^2\omega^{-1}p_j
 \tag{I.12}
\]

into (I.10)--(I.11), followed by multiplication by `omega/R`, gives

\[
 \begin{aligned}
 \mathfrak X_j
 &\le C\frac\omega R R^{-3}
       L^{2/3}R^2
       (R^2\omega^{-1}p_j)^{2/3}\\
 &=C L^{2/3}\omega^{1/3}R^{-2/3}p_j^{2/3}.
 \end{aligned}
 \tag{I.13}
\]

This proves (I.1).  The coefficient has the strict rate

\[
 \lim_{L\to\infty}\frac1{L^2}
 \log\!\left(L^{2/3}\omega^{1/3}R^{-2/3}\right)
 =\frac\rho6-\frac{c_\gamma}{12}
 =-\frac{4279}{238140000}<0.
 \tag{I.14}
\]

Consequently one short exterior block is paid uniformly for large `L`
after using the domination `p_j<=p_F<=C P_R^M` in (I.18).  Since no PDE
identity entered (I.10)--(I.13), physical diffusion cannot invalidate this
conclusion.

## 3. Exact participation count

Let `A` be any finite collection of the disjoint blocks and define

\[
 p_A:=\sum_{j\in A}p_j,
 \qquad
 \mathfrak X_A
 :=\frac\omega R
   \left[\sum_{j\in A}\mathcal T_j\right]_+.
 \tag{I.15}
\]

If `p_A>0`, define `N_eff(A)` by (I.2), with the sums restricted to
`A`; set `N_eff(A)=0` when `p_A=0`.  Positivity and Holder for finite
sums give

\[
 1\le N_{\rm eff}(A)\le |A|
 \quad(p_A>0).
 \tag{I.16}
\]

The lower equality occurs when only one block carries payment.  The upper
equality occurs when all `p_j`, `j in A`, are equal and positive.  This
definition records the actual cubic distribution and is sharper than simply
counting every block intersecting the clock.

Using `[sum_j a_j]_+<=sum_j|a_j|`, (I.13), and (I.2),

\[
 \boxed{
 \mathfrak X_A
 \le C L^{2/3}\omega^{1/3}R^{-2/3}
 N_{\rm eff}(A)^{1/3}p_A^{2/3}.}
 \tag{I.17}
\]

For blocks inside the frozen exterior cylinder, disjointness and the
Version-M cubic row imply

\[
 p_A\le p_F\le C P_R^M.
 \tag{I.18}
\]

Thus a dynamical estimate

\[
 N_{\rm eff}(A)\le C_NR^{-\theta}
 \tag{I.19}
\]

would give

\[
 \mathfrak X_A
 \le C L^{2/3}\omega^{1/3}
 R^{-(2+\theta)/3}(P_R^M)^{2/3}.
 \tag{I.20}
\]

The exponential rate of the coefficient in (I.20) is

\[
 \frac{\rho(2+\theta)-c_\gamma}{12}.
 \tag{I.21}
\]

It is strictly negative exactly when

\[
 \boxed{
 \theta<\frac{c_\gamma}{\rho}-2
 =\frac{8558}{35721}=\theta_*.}
 \tag{I.22}
\]

The inequality must be strict: at equality the exponential rate is zero
and the remaining factor `L^(2/3)` is unbounded.  Equivalently, if the
active time fraction is written `R^beta` so that `theta=1-beta`, then

\[
 \beta>1-\theta_*
 =\frac{27163}{35721}\approx0.7604210408,
 \tag{I.23}
\]

which agrees exactly with the residence threshold in R0.75G.

## 4. The full-block obstruction

The frozen clock has length `O(R^2)`.  A partition into `O(R^3)` blocks
contains

\[
 N\asymp R^{-1}
 \tag{I.24}
\]

blocks.  Uniformly spread cubic payment has `N_eff=N`, hence `theta=1`.
The coefficient in (I.20) then becomes

\[
 L^{2/3}\omega^{1/3}R^{-1},
 \tag{I.25}
\]

whose exponential rate is

\[
 \frac\rho4-\frac{c_\gamma}{12}
 =\frac{27163}{476280000}>0.
 \tag{I.26}
\]

Therefore independent absolute estimates on all blocks reproduce the
known adverse block-count loss.  The favorable one-block estimate cannot
be summed naively over the whole clock.

### A high-participation zero-flux diagnostic

The participation count is not itself an obstruction to E.24.  Let
`F=f_0(t,x_3)` be independent of `x_2`.  Since `b` and `F` are also
independent of `x_2`, periodic integration gives, on every block,

\[
 \mathcal T_j
 =\frac12\int_{J_j}\!\int_{\mathbb T_{x_1}\times\mathbb T_{x_3}}
 \eta_R b|f_0|^2
 \left(\int_{\mathbb T_{x_2}}\partial_2\xi\,dx_2\right)
 dx_1dx_3dt
 =0.
 \tag{I.27}
\]

A temporally persistent nonzero zero mode can nevertheless have comparable
positive `p_j` on all blocks, hence `N_eff asymp R^(-1)`.  Thus a large
passive-cubic participation count can be a false positive for the absolute
route, just as R0.75C found for the background cubic count.  Equation
(I.19) is only a sufficient route.  Failure of (I.19) neither disproves
E.24 nor removes the signed cross-mode alternative.

## 5. What remains dynamical

The algebraic theorem reduces the next step to a falsifiable dichotomy.

1. Prove the sufficient participation estimate (I.19) with some
   `theta<theta_*` from shear transport, diffusion, collar geometry, and
   Version-M rows already present; or
2. prove signed inter-block cancellation that dominates the right side of
   (I.17); or
3. construct an admissible frozen passive sequence with
   `N_eff >= R^(-theta_*+o(1))` and uncompensated positive flux.

Diffusion enters only at this stage, through occupation and recrossing
across many blocks.  It is not an obstruction to (I.1).  A future
Feynman--Kac, Davies--Gaffney, or resolvent argument is useful only if it
controls the multi-block participation or signed aggregation; a one-block
localization estimate alone would not close E.24.

## 6. Status boundary

**Proved:** the arbitrary-field one-block estimate I.10--I.14, the exact
participation identity and bounds I.15--I.17, the conditional threshold
I.19--I.23, the adverse full-uniform-block rate I.24--I.26, and the
high-participation zero-flux diagnostic I.27.

**Not used:** the passive PDE, characteristics, heat-kernel estimates,
frequency localization, or numerical simulation.

**Open:** the required bound on `N_eff` or an equivalent signed
cancellation for the frozen diffusing field; shear-transition bands;
periodic recrossing; E.24; complete-clock extraction; fixed deletion;
suitable-weak transfer; and every regularity or singularity conclusion.
\(\mathbf{NOT\ CLAY}.\)
