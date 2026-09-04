# R0.75Q -- physical-collar payment for one spatially spread shear harmonic

## 0. Result and exact boundary

R0.75L proves a favorable diffusive factor for one real constant-shear
harmonic but pays it with a full-circle cubic mass. R0.75P replaces the
full-torus mass by a physical radial-collar atom when a quantified fraction
of the entrance energy lies in a central transverse disk. The present note
closes the complementary benchmark in which the field is one harmonic and
is independent of `x_1,x_3`.

Let

\[
 F_k(t,x_2)=A e^{-k^2t}\cos(k(x_2-Bt)),
 \qquad A>0,\quad k\in\mathbb N,
 \tag{Q.1}
\]

and use the canonical radial plateau shell of radius `aR` and fixed
thickness. If

\[
 k^2T\ge1,\qquad kaR\ge2\pi,\qquad
 k\ge R^{-3/2},\qquad |B|\le C_BR^{-2},\qquad
 a\ge4\delta_0,\qquad (a+\delta)R<\frac\pi2,
 \tag{Q.2}
\]

then its physical-collar cubic mass satisfies

\[
 \boxed{
 M_{k,\rm col}
 \ge c_{\rm box}\delta_0a^2R^3k^{-2}A^3,
 \qquad
 c_{\rm box}:=\frac{2(1-e^{-3})}{9\pi}.}
 \tag{Q.3}
\]

For every measurable time weight `0<=eta<=1`, the signed physical cutoff
flux defined below is consequently bounded by

\[
 \boxed{
 |\mathcal T_{k,\eta}^{(3)}|
 \le C_\vartheta\delta_0^{-2/3}|B|a^{2/3}k^{-2/3}
 M_{k,\rm col}^{2/3}.}
 \tag{Q.4}
\]

After the frozen normalization this gives

\[
 \boxed{
 \mathfrak X_{k,\rm col}
 \le C L^{2/3}R^{-2/3}\omega^{1/3}
 p_{k,\rm col}^{2/3}
 \le C p_{k,\rm col}^{2/3}}
 \tag{Q.5}
\]

for all sufficiently large `L`. The coefficient tends to zero at the exact
rate

\[
 L^{2/3}\exp\!\left(-\frac{4279}{238140000}L^2\right).
 \tag{Q.6}
\]

No entrance-concentration hypothesis is used. Indeed, the entrance
fraction for this spatially spread harmonic can be at most of order
`a^2R^2`, far below the R0.75P threshold. This closes the physical-collar
localization left open by R0.75L for this one subfamily.

The theorem remains one real harmonic, constant shear, independent of
`x_1,x_3`, and total-field rather than packet-projection based. It does not
handle arbitrary low-concentration packets, vertical structure,
interference, nonconstant shear, or E.24.

## 1. Frozen inputs and radial geometry

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | outer-collar weight and frozen scales |
| `research/r075l_single_harmonic_diffusive_signed_flux_gain.md` | `52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5` | exact real harmonic and diagonal cancellation |
| `research/r075n_radial_collar_averaged_wiener_row.md` | `ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318` | canonical radial cutoff |
| `research/r075p_buffered_collar_entrance_concentration.md` | `8df38e54514d82102cd3e568e89ec1db93913da3ceac52f1371d77fd79c1b7a6` | plateau fibres and actual-component ledger boundary |

Retain

\[
 a=pL,\qquad p=\frac{32}{63},\qquad
 R=e^{-\rho L^2/4},\qquad
 \omega=e^{-c_\gamma L^2/4},\qquad
 \rho=\frac9{10000},\quad c_\gamma=\frac8{3969}.
 \tag{Q.7}
\]

Choose `0<delta_0<delta` and `0<=vartheta<=1`, and let the central-chart
formula below denote its periodic lift:

\[
 \xi_{a,R}(x)=\vartheta(|x|/R-a),\qquad
 \vartheta=1\quad\hbox{on }[-\delta_0,\delta_0],\qquad
 \operatorname {supp}\vartheta\subset(-\delta,\delta).
 \tag{Q.8}
\]

Assume `a>=4delta_0` and `(a+delta)R<pi/2`. Its plateau shell is

\[
 \mathcal S_{a,R}^{\rm plat}
 :=\{x\in\mathbb T^3:||x|/R-a|\le\delta_0\}.
 \tag{Q.9}
\]

The derivative is supported in a shell of volume at most
`C_delta a^2R^3`, while `|partial_2 xi|<=C_vartheta R^(-1)`. Therefore

\[
 V_{\xi,3}:=\int_{\mathbb T^3}|\partial_2\xi_{a,R}|\,dx
 \le C_\vartheta a^2R^2.
 \tag{Q.10}
\]

This direct `L^1` row is sufficient for one harmonic. No Wiener summation
is needed.

## 2. Exact signed-flux bound

The field Q.1 obeys

\[
 (\partial_t+B\partial_2-\partial_2^2)F_k=0.
 \tag{Q.11}
\]

For any measurable `0<=eta<=1`, define the three-dimensional physical
flux

\[
 \mathcal T_{k,\eta}^{(3)}
 :=\frac12\int_0^T\!\int_{\mathbb T^3}
 \eta(t)B\partial_2\xi_{a,R}(x)|F_k(t,x_2)|^2\,dxdt.
 \tag{Q.12}
\]

The square identity is

\[
 |F_k|^2=\frac{A^2e^{-2k^2t}}2
 \left[1+\cos(2k(x_2-Bt))\right].
 \tag{Q.13}
\]

The constant row vanishes because the integral of `partial_2 xi` over the
torus is zero. Taking absolute values only after that cancellation and
using Q.10 gives

\[
 \begin{aligned}
 |\mathcal T_{k,\eta}^{(3)}|
 &\le\frac{A^2|B|V_{\xi,3}}4
       \int_0^T e^{-2k^2t}\,dt\\
 &\le\frac{A^2|B|V_{\xi,3}}{8k^2}
 \le C_\vartheta A^2|B|a^2R^2k^{-2}.
 \end{aligned}
 \tag{Q.14}
\]

The bound uses ordinary heat decay and the exact zero row. It is not an
enhanced-dissipation estimate.

## 3. A phase-uniform physical-collar lower bound

For

\[
 \mathcal R_{a,R}:=\{(x_2,x_3):
 |x_2|\le aR/4,\ |x_3|\le aR/4\},
 \tag{Q.15}
\]

one has `|(x_2,x_3)|<=aR/(2sqrt(2))<=(a-2delta_0)R`. R0.75P's exact
fibre formula therefore gives

\[
 \left|\{x_1:(x_1,x_2,x_3)\in
 \mathcal S_{a,R}^{\rm plat}\}\right|
 \ge4\delta_0R
 \quad((x_2,x_3)\in\mathcal R_{a,R}).
 \tag{Q.16}
\]

The function `|cos z|^3` has period `pi` and

\[
 \int_0^\pi|\cos z|^3\,dz=\frac43.
 \tag{Q.17}
\]

An interval of length `ell` contains `floor(k ell/pi)` complete periods of
`|cos(kx-phi)|^3`, starting from its own left endpoint. If
`k ell/pi>=1`, then `floor(k ell/pi)>=(k ell/pi)/2`. With
`ell=aR/2` and Q.2, this gives, uniformly in the phase `phi`,

\[
 \int_{-aR/4}^{aR/4}|\cos(kx_2-\phi)|^3\,dx_2
 \ge\frac{aR}{3\pi}.
 \tag{Q.18}
\]

Combining Q.16, Q.18, and the `x_3` interval of length `aR/2` yields

\[
 \int_{\mathcal S_{a,R}^{\rm plat}}
 |\cos(k(x_2-Bt))|^3\,dx
 \ge\frac{2\delta_0a^2}{3\pi}R^3
 \tag{Q.19}
\]

for every time, with no restriction on the translated phase.

Define

\[
 M_{k,\rm col}:=
 \int_0^T\!\int_{\mathcal S_{a,R}^{\rm plat}}|F_k|^3\,dxdt.
 \tag{Q.20}
\]

Since `k^2T>=1`, Q.19 gives

\[
 \begin{aligned}
 M_{k,\rm col}
 &\ge\frac{2\delta_0a^2R^3}{3\pi}A^3\int_0^T e^{-3k^2t}\,dt\\
 &\ge\frac{2(1-e^{-3})}{9\pi}
       \delta_0a^2R^3k^{-2}A^3.
 \end{aligned}
 \tag{Q.21}
\]

This proves Q.3 and implies

\[
 A^2\le c_{\rm box}^{-2/3}\delta_0^{-2/3}
 a^{-4/3}R^{-2}k^{4/3}M_{k,\rm col}^{2/3}.
 \tag{Q.22}
\]

Substitution in Q.14 cancels the full `R^2` and proves Q.4.

## 4. Frozen normalization and Version-M inclusion

Set

\[
 p_{k,\rm col}:=R^{-2}\omega M_{k,\rm col},
 \qquad
 \mathfrak X_{k,\rm col}:=
 \frac\omega R[\mathcal T_{k,\eta}^{(3)}]_+.
 \tag{Q.23}
\]

Equation Q.4 becomes

\[
 \mathfrak X_{k,\rm col}
 \le C|B|a^{2/3}R^{1/3}\omega^{1/3}k^{-2/3}
 p_{k,\rm col}^{2/3}.
 \tag{Q.24}
\]

At the frozen `B,k` bounds this coefficient is at most

\[
 C L^{2/3}R^{-2/3}\omega^{1/3}
 =C L^{2/3}
 \exp\!\left(-\frac{4279}{238140000}L^2\right)
 \longrightarrow0.
 \tag{Q.25}
\]

This proves Q.5--Q.6 against the harmonic's own physical-collar atom.

For the final Version-M payment only, impose the same ledger-alignment and
realized-subclass conditions as R0.75P. Translate the time origin to the
left endpoint of the flux window, require `[0,T]` to lie in the same
scale-`2R` exterior measurement interval, and require the plateau tube to
lie in an exterior row whose weight is at least `omega`. After the common
coordinate translation, require `F_k` to be an actual coordinate component
of the same smooth velocity `v_R` measured by `P_R^M` throughout that
tube. Then `|F_k|<=|v_R|` pointwise and nonnegativity of the exterior cubic
row gives

\[
 p_{k,\rm col}\le C P_R^M,
 \qquad
 \boxed{
 \mathfrak X_{k,\rm col}\le C(P_R^M)^{2/3}}
 \tag{Q.26}
\]

for sufficiently large `L`. This is not asserted for a harmonic projection
of a larger velocity component, and it does not assert arbitrary
zero-trajectory realization.

## 5. Why this result belongs to the low-entrance branch

Let `phi_0` be any R0.75P entrance cutoff. At `t=0`,

\[
 E_0=2\pi^2A^2,
 \qquad
 E_{\rm in}\le A^2|\operatorname {supp}\phi_0|
 \le\pi a^2R^2A^2,
 \qquad
 \frac{E_{\rm in}}{E_0}\le\frac{a^2R^2}{2\pi}.
 \tag{Q.27}
\]

For every fixed `0<=sigma<2`,

\[
 \frac{a^2R^2}{R^\sigma}
 =p^2L^2R^{2-\sigma}\longrightarrow0.
 \tag{Q.28}
\]

In particular this can lie far below the P threshold
`sigma_*=8558/178605`. Q.26 is therefore an independent cancellation and
spatial-spreading mechanism, not a hidden use of P's entrance hypothesis.

## 6. Status boundary

**Proved:** the radial derivative `L^1` row Q.8--Q.10; exact diagonal
cancellation and flux bound Q.11--Q.14; the phase-uniform rectangular
subcollar estimate Q.15--Q.21; the physical-collar cubic conversion
Q.22--Q.25; conditional actual-component Version-M payment Q.26; and the
low-entrance diagnostic Q.27--Q.28.

**Not proved:** the same result for a Fourier or Littlewood--Paley
projection of a larger field; two or more horizontal harmonics; arbitrary
vertical structure; a general low-entrance packet; nonconstant shear;
inter-packet or low-difference summation; removal of the total upper-
frequency cap in the broader route; arbitrary-field E.24; complete-clock
extraction; fixed deletion; suitable-weak transfer; or any regularity or
singularity conclusion. No novelty or priority claim is made.
\(\mathbf{NOT\ CLAY}.\)
