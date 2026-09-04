# R0.75P -- buffered-collar closure under quantified entrance concentration

## 0. Result and exact boundary

R0.75O controls the full-time signed flux of one constant-shear packet by
its entrance energy, but pays that energy with a full-`T^2` cubic mass.
The present note gives a sufficient condition that replaces that global
mass by a genuine three-dimensional radial-collar atom.

Choose the canonical R0.75N radial profile with a fixed plateau and a
smooth cutoff `phi_0` inside its transverse projection. Let

\[
 E_{\rm in}:=\int_{\mathbb T^2}\phi_0|F_0|^2,
 \qquad
 E_0:=\int_{\mathbb T^2}|F_0|^2,
 \qquad
 E_{\rm in}\ge\mu E_0,\qquad 0<\mu\le1.
 \tag{P.1}
\]

For a real constant-shear packet with

\[
 K\le|n|\le2K,qquad n^2+j^2\le4K^2,qquad
 K\ge R^{-3/2},qquad |B|\le C_BR^{-2},
 \tag{P.2}
\]

the cutoff transported by `B` retains at least half of the entrance
fraction for a time `tau=c_0 mu K^(-2)`. The three-dimensional plateau
fibres then give the local cubic lower bound

\[
 \boxed{
 M_{K,\rm col}
 \ge c_*a^{-1}\mu^{5/2}K^{-2}E_0^{3/2},
 \qquad a=pL.}
 \tag{P.3}
\]

Combining this with R0.75O yields

\[
 \boxed{
 \mathfrak X_{K,\rm col}
 \le C|B|a^{5/3}\mu^{-5/3}
 R^{1/3}\omega^{1/3}K^{-2/3}
 p_{K,\rm col}^{2/3}.}
 \tag{P.4}
\]

Here `p_(K,col)=R^(-2)omega M_(K,col)` is supported inside the actual
radial-collar payment region. At the frozen `B,K` scales, the coefficient
is bounded for large `L` whenever

\[
 \boxed{
 \mu\ge c_\mu R^\sigma,
 \qquad
 0\le\sigma<\sigma_*:=
 \frac15\left(\frac{c_\gamma}{\rho}-2\right)
 =\frac{8558}{178605}
 \approx0.0479157918.}
 \tag{P.5}
\]

Under (P.5), the packet's signed flux is paid by the existing Version-M
row whenever the packet is an actual coordinate component of the same
velocity measured by that row, and the collar is aligned as specified
below. A Fourier projection of a larger component is not covered. This is
a conditional realized-subclass closure, not an arbitrary-packet result.
A spatially spread packet can have an entrance fraction of order
`L^2R^2`, far below (P.5), while its signed flux may still be small by
localization or cancellation. The low-concentration branch therefore
requires a spatially localized signed-kernel estimate; it cannot be
settled by the global entrance energy in R0.75O.

The theorem remains constant-shear, single-packet, and total-frequency
capped. It does not prove E.24 for an arbitrary passive field.

## 1. Frozen inputs and canonical plateau geometry

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | outer-collar payment and scale-`2R` weight |
| `research/r075i_diffusion_safe_block_participation.md` | `c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7` | short-block payment scale and participation boundary |
| `research/r075n_radial_collar_averaged_wiener_row.md` | `ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318` | selectable radial cutoff and Wiener row |
| `research/r075o_vertical_diffusion_packet_gain.md` | `3efb39d2624cf5b5a0e7f348f6cde2ef2416eca900f1aa3ecc90a6ad734849a9` | constant-shear vertical-diffusion packet estimate |

Retain

\[
 p=\frac{32}{63},\qquad a=pL,qquad r=aR,qquad
 R=e^{-\rho L^2/4},\qquad
 \omega=e^{-c_\gamma L^2/4}.
 \tag{P.6}
\]

Translate the time origin to the left endpoint of the full signed-flux
window and assume this window is contained in the frozen scale-`2R`
exterior measurement interval `I_(2R)`. Use the Version-M translated
spatial coordinates, and assume that the canonical plateau shell below is
contained in the selected outer-collar cover. In particular, the short
interval `[0,tau]` constructed below is measured by the same Version-M
cubic row. This is a ledger-alignment hypothesis. It does not assert that
an arbitrary constant-shear packet realizes the frozen inversion-paired
zero-trajectory family.

For the final payment statement P.31, impose the additional
field-realization hypothesis: after the common coordinate translation,
`F` is an actual coordinate component of the same smooth velocity `v_R`
to which `P_R^M` is applied throughout the aligned tube. Thus
`|F|<=|v_R|` pointwise there. In particular, `F` is not a Littlewood--Paley
or Fourier projection of a larger velocity component. Statements
P.3--P.30 do not use this realization hypothesis.

Choose the admissible canonical profile from R0.75N so that, for a fixed
`delta_0>0`,

\[
 \vartheta(s)=1\quad(|s|\le\delta_0),
 \qquad
 \xi_{a,R}(x)=\vartheta(|x|/R-a).
 \tag{P.7}
\]

Assume `a>=4delta_0` and `(a+delta)R<pi/2`, as in the central-chart
construction. Define its plateau shell

\[
 \mathcal S_{a,R}^{\rm plat}
 :=\{x\in\mathbb T^3:
 ||x|/R-a|\le\delta_0\}.
 \tag{P.8}
\]

Let `y=(x_2,x_3)` and choose `phi_0 in C_c^infinity(T^2)` with

\[
 \begin{aligned}
 &0\le\phi_0\le1,\qquad
 \operatorname {supp}\phi_0
 \subset\{|y|\le(a-3\delta_0)R\},\\
 &\|\Delta_y\phi_0\|_\infty\le C_\phi R^{-2},
 \qquad
 V_\phi:=|\operatorname {supp}\phi_0|
 \le\pi a^2R^2.
 \end{aligned}
 \tag{P.9}
\]

For every `|y|<= (a-2delta_0)R`, the `x_1`-fibre of the plateau shell has
length at least `4delta_0R`. Indeed, with `q=|y|/R`, its exact length is

\[
 \ell_{a}(q)=2R\left[
 \sqrt{(a+\delta_0)^2-q^2}
 -\sqrt{(a-\delta_0)^2-q^2}\right]
 \ge4\delta_0R.
 \tag{P.10}
\]

The difference in brackets is increasing in `q` and equals
`2delta_0` at `q=0`. This is a lower fibre estimate on the chosen plateau,
not an upper estimate for the whole shell.

## 2. Packet, moving cutoff, and local persistence

Let

\[
 \Gamma_K=\{(n,j)\in\mathbb Z^2:
 K\le|n|\le2K,\ n^2+j^2\le4K^2\},
 \tag{P.11}
\]

and take the real finite datum

\[
 F_0(y)=\sum_{(n,j)\in\Gamma_K}
 c_{n,j}e^{i(nx_2+jx_3)},
 \qquad c_{-n,-j}=\overline{c_{n,j}}.
 \tag{P.12}
\]

Its constant-shear evolution is

\[
 F(t,y)=\sum_{(n,j)\in\Gamma_K}c_{n,j}
 e^{-(n^2+j^2)t}e^{i(n(x_2-Bt)+jx_3)}.
 \tag{P.13}
\]

Transport the entrance cutoff by the same shear,

\[
 \phi_t(x_2,x_3):=\phi_0(x_2-Bt,x_3),
 \qquad
 \partial_t\phi_t+B\partial_2\phi_t=0,
 \tag{P.14}
\]

and put

\[
 E_\phi(t):=\int_{\mathbb T^2}\phi_t|F(t)|^2.
 \tag{P.15}
\]

The exact local energy identity is

\[
 E_\phi'(t)
 =\int_{\mathbb T^2}\Delta_y\phi_t|F|^2
 -2\int_{\mathbb T^2}\phi_t|\nabla_yF|^2.
 \tag{P.16}
\]

The total-frequency cap is preserved and gives

\[
 \|\nabla_yF(t)\|_2^2
 \le4K^2\|F(t)\|_2^2
 \le4K^2E_0.
 \tag{P.17}
\]

Since `K>=R^(-3/2)` and `R<=1`, one has `R^(-2)<=K^2`. Hence

\[
 E_\phi'(t)\ge-(8+C_\phi)K^2E_0.
 \tag{P.18}
\]

Choose a fixed `c_0>0` satisfying

\[
 c_0\le\min\left\{
 \frac1{2(8+C_\phi)},\frac{\delta_0}{C_B},1\right\},
 \qquad
 \tau:=c_0\mu K^{-2}.
 \tag{P.19}
\]

If the available time window obeys `K^2T>=1`, then `tau<=T`. Moreover,
`|B|tau<=delta_0R`, so `supp phi_t` stays inside
`{|y|<=(a-2delta_0)R}` for `0<=t<=tau`. Integrating (P.18) and using
(P.1) gives

\[
 \boxed{
 E_\phi(t)\ge\frac\mu2E_0
 \quad(0\le t\le\tau).}
 \tag{P.20}
\]

## 3. Physical-collar cubic lower bound

Define the local three-dimensional cubic mass

\[
 M_{K,\rm col}:=
 \int_0^\tau\!\int_{\mathcal S_{a,R}^{\rm plat}}
 |F(t,x_2,x_3)|^3\,dxdt.
 \tag{P.21}
\]

The field is independent of `x_1`. Equations (P.10) and (P.20), followed
by Holder on `supp phi_t`, give for every `0<=t<=tau`

\[
 \begin{aligned}
 \int_{\mathcal S_{a,R}^{\rm plat}}|F(t)|^3
 &\ge4\delta_0R
 \int_{\operatorname {supp}\phi_t}|F(t,y)|^3\,dy\\
 &\ge4\delta_0R\,V_\phi^{-1/2}
 E_\phi(t)^{3/2}\\
 &\ge\frac{4\delta_0}{\sqrt\pi\,a}
 \left(\frac\mu2E_0\right)^{3/2}.
 \end{aligned}
 \tag{P.22}
\]

Integration over `tau=c_0mu K^(-2)` proves (P.3) with the explicit
constant

\[
 c_*:=\frac{\sqrt2\,\delta_0c_0}{\sqrt\pi}.
 \tag{P.23}
\]

Equivalently,

\[
 E_0\le c_*^{-2/3}a^{2/3}\mu^{-5/3}
 K^{4/3}M_{K,\rm col}^{2/3}.
 \tag{P.24}
\]

No backward heat estimate or spectral observability constant is used.
The power `mu^(5/2)` consists of `mu^(3/2)` from the persistent local
energy and one further `mu` from the certified time length.

## 4. Flux closure and exact concentration threshold

Let `mathcal T_(K,eta)^(2)` be the full-window physical signed flux from
R0.75O. Its arbitrary-vertical-frequency energy row and the canonical
R0.75N Wiener estimate give

\[
 |\mathcal T_{K,\eta}^{(2)}|
 \le\frac{|B|\mathcal W_\infty}{4K^2}E_0,
 \qquad
 \mathcal W_\infty\le C_\vartheta a.
 \tag{P.25}
\]

Substitution of (P.24) proves

\[
 |\mathcal T_{K,\eta}^{(2)}|
 \le C|B|a^{5/3}\mu^{-5/3}
 K^{-2/3}M_{K,\rm col}^{2/3}.
 \tag{P.26}
\]

Define

\[
 p_{K,\rm col}:=R^{-2}\omega M_{K,\rm col},
 \qquad
 \mathfrak X_{K,\rm col}
 :=\frac\omega R[\mathcal T_{K,\eta}^{(2)}]_+.
 \tag{P.27}
\]

This gives (P.4). At `|B|<=C_BR^(-2)` and `K>=R^(-3/2)`,

\[
 \mathfrak X_{K,\rm col}
 \le C L^{5/3}\mu^{-5/3}
 R^{-2/3}\omega^{1/3}p_{K,\rm col}^{2/3}.
 \tag{P.28}
\]

If `mu>=c_mu R^sigma`, the exponential rate of the coefficient in
(P.28) is

\[
 \frac\rho6-\frac{c_\gamma}{12}
 +\frac{5\sigma\rho}{12}.
 \tag{P.29}
\]

It is strictly negative exactly for (P.5), because

\[
 \frac15\left(\frac{c_\gamma}{\rho}-2\right)
 =\frac15\left(\frac{80000}{35721}-2\right)
 =\frac{8558}{178605}.
 \tag{P.30}
\]

At equality the exponential rate vanishes and the factor `L^(5/3)` is
unbounded, so the strict endpoint is excluded. Under the ledger-alignment
hypotheses above, the plateau shell lies in the scale-`2R` exterior
measurement region where the frozen weight is at least `omega`. Since
`F` is the actual coordinate component of that same velocity,
`|F|<=|v_R|` pointwise. Nonnegativity of the exterior cubic row therefore
gives

\[
 p_{K,\rm col}\le C P_R^M,
 \qquad
 \boxed{
 \mathfrak X_{K,\rm col}
 \le C(P_R^M)^{2/3}}
 \tag{P.31}
\]

for all sufficiently large `L` under (P.5).

## 5. The remaining low-concentration branch

For a packet whose energy is spatially spread at torus scale, the fraction
captured by `phi_0` can be of order `a^2R^2`, hence of order `L^2R^2`.
This is much smaller than
`R^sigma` for every `sigma<sigma_*`. Such a packet need not have a large
signed collar flux: the same spatial geometry and difference-frequency
cancellation discarded by the global energy `E_0` may make the flux
small.

Therefore failure of (P.5) is not a counterexample. It shows that the
next estimate must localize the signed R0.75O kernel to the moving collar,
or split near and far entrance data while preserving the horizontal
packet cancellation. Replacing `E_0` by a positive fixed entrance
majorant would repeat the R0.75K trace loss.

## 6. Status boundary

**Proved:** canonical plateau fibres P.7--P.10; moving-cutoff local energy
and persistence P.14--P.20; the physical-collar cubic lower bound
P.21--P.24; the conditional signed-flux estimate P.25--P.28; the exact
entrance-concentration threshold P.29--P.30; and conditional Version-M
ledger payment P.31 under the stated space-time alignment hypothesis.

**Not proved:** the entrance concentration P.5 for every packet; the
low-concentration complement; a spatially localized signed heat kernel;
nonconstant shear; inter-packet summation; low differences; removal of the
total upper-frequency cap; arbitrary-field E.24; complete-clock
extraction; fixed deletion; suitable-weak transfer; or any regularity or
singularity conclusion. P.31 is not proved for a Fourier projection of a
larger velocity component. No arbitrary constant-shear packet is claimed
to realize the frozen inversion-paired zero-trajectory family. No novelty
or priority claim is made.
\(\mathbf{NOT\ CLAY}.\)
