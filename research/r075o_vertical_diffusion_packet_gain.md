# R0.75O -- vertical diffusion preserves the packet flux gain for constant shear

## 0. Result and exact boundary

R0.75M proves a `K^(-2/3)` signed-flux gain for one horizontal dyadic
packet with no vertical variable. R0.75N proves that the physical
`x_1`-averaged radial-collar derivative has an `x_3`-uniform Wiener row of
size `O(L)`. The present note joins those two inputs without suppressing
vertical diffusion.

For constant shear `B`, arbitrary vertical frequencies preserve the
quadratic-energy estimate

\[
 \boxed{
 |\mathcal T_{K,\eta}^{(2)}|
 \le \frac{|B|\mathcal W_\infty}{4K^2}E_0,
 \qquad
 \mathcal W_\infty:=
 \sum_{\ell\in\mathbb Z}\|d_\ell\|_{L^\infty_{x_3}}.}
 \tag{O.1}
\]

If the total initial Fourier support additionally obeys
`n^2+j^2<=4K^2` and `K^2T>=1`, then the full two-dimensional spacetime
cubic mass `M_K^(2)` controls the initial energy and

\[
 \boxed{
 |\mathcal T_{K,\eta}^{(2)}|
 \le e(2\pi)^{2/3}|B|\mathcal W_\infty
 K^{-2/3}(M_K^{(2)})^{2/3}.}
 \tag{O.2}
\]

For the canonical radial collar from R0.75N,
`mathcal W_infty<=C_vartheta L`. At the frozen threshold
`K>=R^(-3/2)` and for a constant plateau shear
`|B|<=C_B R^(-2)`, the normalized coefficient is

\[
 C_{\vartheta,B}L\,\omega^{1/3}R^{-2/3}
 =C_{\vartheta,B}L
 \exp\!\left(-\frac{4279}{238140000}L^2\right),
 \tag{O.3}
\]

and therefore tends to zero. This gives the same two-thirds homogeneity
for the packet's own full-`T^2` diagnostic atom under constant shear.

This does **not** localize the cubic mass to the physical collar, sum
different packets, treat low horizontal differences, or handle the
actual nonconstant `b(t,x_3)`. It is a constant-shear benchmark, not E.24.

## 1. Frozen inputs and two-dimensional packet

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` | exact `x_1`-averaged flux |
| `research/r075g_signed_flux_gain_threshold.md` | `f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41` | calibrated gain and shear size |
| `research/r075m_dyadic_packet_diffusive_flux_gain.md` | `13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7` | one-dimensional packet argument |
| `research/r075n_radial_collar_averaged_wiener_row.md` | `ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318` | canonical collar Wiener row |

Work on `[0,T] times T^2_(x_2,x_3)` with

\[
 \mathcal L_B^{(2)}
 :=\partial_t+B\partial_2-\Delta_{23},
 \qquad B\in\mathbb R.
 \tag{O.4}
\]

For an integer `K>=1`, let the horizontal Fourier support satisfy
`K<=|n|<=2K`. Initially allow

\[
 F_0(x_2,x_3)=\sum_{K\le|n|\le2K}
 f_n^0(x_3)e^{inx_2},
 \qquad f_n^0\in L^2(\mathbb T),
 \tag{O.5}
\]

with finitely many nonzero `n`; smooth finite Fourier data may be used
throughout and the estimate then extends by density. Its exact evolution
is

\[
 f_n(t)=e^{-n^2t}e^{-inBt}e^{t\partial_3^2}f_n^0,
 \qquad
 F(t)=\sum_nf_n(t,x_3)e^{inx_2}.
 \tag{O.6}
\]

Let

\[
 H(x_2,x_3):=\int_{-\pi}^{\pi}
 \xi(x_1,x_2,x_3)\,dx_1,
 \qquad
 d_\ell(x_3):=\frac1{2\pi}\int_{-\pi}^{\pi}
 \partial_2H\,e^{-i\ell x_2}\,dx_2.
 \tag{O.7}
\]

Periodicity gives `d_0=0`. Assume `mathcal W_infty<infinity`, take
`0<=eta<=1`, and define the physical `x_1`-integrated signed flux

\[
 \mathcal T_{K,\eta}^{(2)}
 :=\frac12\int_0^T\!\int_{\mathbb T^3}
 \eta(t)B\partial_2\xi(x)|F(t,x_2,x_3)|^2\,dxdt.
 \tag{O.8}
\]

## 2. Vertical-semigroup Schur estimate

Horizontal Fourier expansion of (O.8) gives the exact identity

\[
 \mathcal T_{K,\eta}^{(2)}
 =\pi B\operatorname {Re}\sum_{n,m}
 \int_0^T\!\eta(t)
 \int_{\mathbb T}d_{m-n}(x_3)
 f_n(t,x_3)\overline{f_m(t,x_3)}\,dx_3dt.
 \tag{O.9}
\]

The diagonal vanishes before absolute values. Put
`a_n=||f_n^0||_(L^2_(x_3))`. The vertical heat semigroup is an `L^2`
contraction, so for every pair

\[
 \begin{aligned}
 &\int_0^T\eta(t)
 \left|\int_{\mathbb T}d_{m-n}f_n\overline{f_m}\,dx_3\right|dt\\
 &\qquad\le
 \|d_{m-n}\|_\infty a_na_m
 \int_0^Te^{-(n^2+m^2)t}\,dt\\
 &\qquad\le
 \frac{\|d_{m-n}\|_\infty}{n^2+m^2}a_na_m.
 \end{aligned}
 \tag{O.10}
\]

The nonnegative matrix

\[
 A_{nm}:=\frac{\|d_{m-n}\|_\infty}{n^2+m^2}
 \tag{O.11}
\]

has both row and column sums at most
`mathcal W_infty/(2K^2)`. Schur's test and horizontal Parseval give

\[
 \begin{aligned}
 |\mathcal T_{K,\eta}^{(2)}|
 &\le\frac{\pi|B|\mathcal W_\infty}{2K^2}
 \sum_n\|f_n^0\|_2^2\\
 &=\frac{|B|\mathcal W_\infty}{4K^2}E_0,
 \qquad
 E_0:=\int_{\mathbb T^2}|F_0|^2.
 \end{aligned}
 \tag{O.12}
\]

This proves (O.1). No upper vertical-frequency bound was used: vertical
diffusion can only reduce the `L^2` factors in the flux estimate. An upper
bound becomes necessary only in the reverse comparison from later cubic
mass back to the entrance energy.

## 3. Total-frequency cap and cubic conversion

Now restrict to the finite real-admissible packet

\[
 \Gamma_K:=\left\{(n,j)\in\mathbb Z^2:
 K\le|n|\le2K,\quad n^2+j^2\le4K^2\right\},
 \tag{O.13}
\]

and take

\[
 F_0(x_2,x_3)=\sum_{(n,j)\in\Gamma_K}
 c_{n,j}e^{i(nx_2+jx_3)},
 \qquad c_{-n,-j}=\overline{c_{n,j}}.
 \tag{O.14}
\]

Set

\[
 M_K^{(2)}:=\int_0^T\!\int_{\mathbb T^2}|F(t)|^3.
 \tag{O.15}
\]

For `0<=t<=1/(8K^2)`, the total upper-frequency cap gives

\[
 \begin{aligned}
 \|F(t)\|_2^2
 &=(2\pi)^2\sum_{(n,j)\in\Gamma_K}
 |c_{n,j}|^2e^{-2(n^2+j^2)t}\\
 &\ge e^{-8K^2t}E_0\ge e^{-1}E_0.
 \end{aligned}
 \tag{O.16}
\]

Holder on the torus of measure `(2pi)^2` yields
`||F(t)||_3^3>=(2pi)^(-1)||F(t)||_2^3`. If `K^2T>=1`, integration on
the same short interval gives

\[
 M_K^{(2)}
 \ge\frac{e^{-3/2}}{16\pi}K^{-2}E_0^{3/2},
 \qquad
 E_0\le e(16\pi)^{2/3}K^{4/3}(M_K^{(2)})^{2/3}.
 \tag{O.17}
\]

Combining (O.12) and (O.17) leaves
`(16pi)^(2/3)/4=(2pi)^(2/3)` and proves (O.2). The vertical packet
cardinality does not occur; it is absorbed by Parseval and the torus
Holder inequality.

## 4. Canonical collar and frozen normalization

For the R0.75N canonical radial cutoff,

\[
 \mathcal W_\infty
 =\sum_\ell\|d_\ell\|_\infty
 \le C_\vartheta a\le C_\vartheta L.
 \tag{O.18}
\]

Define the full-`T^2` diagnostic atom and normalized flux by

\[
 p_{K,23}^{\rm tor}:=R^{-2}\omega M_K^{(2)},
 \qquad
 \mathfrak X_{K,23}^{\rm tor}
 :=\frac\omega R[\mathcal T_{K,\eta}^{(2)}]_+.
 \tag{O.19}
\]

Then (O.2) and (O.18) imply

\[
 \boxed{
 \mathfrak X_{K,23}^{\rm tor}
 \le C_\vartheta |B|L
 R^{1/3}\omega^{1/3}K^{-2/3}
 (p_{K,23}^{\rm tor})^{2/3}.}
 \tag{O.20}
\]

If `K>=R^(-kappa)` and `|B|<=C_BR^(-2)`, its scale coefficient is

\[
 C_{\vartheta,B}L\omega^{1/3}
 R^{(2\kappa-5)/3}.
 \tag{O.21}
\]

Under the frozen calibration
`R=exp(-rho L^2/4)`, `omega=exp(-c_gamma L^2/4)`, this tends to zero
precisely when

\[
 \boxed{
 \kappa>\frac12\left(5-\frac{c_\gamma}{\rho}\right)
 =\frac{98605}{71442}
 \approx1.3802105204.}
 \tag{O.22}
\]

At equality the exponential rate vanishes while the factor `L` grows, so
strict inequality is required. The frozen choice `kappa=3/2` is safely
above threshold and gives

\[
 L\omega^{1/3}R^{-2/3}
 =L\exp\!\left[
 \left(\frac\rho6-\frac{c_\gamma}{12}\right)L^2\right]
 =L\exp\!\left(-\frac{4279}{238140000}L^2\right)
 \longrightarrow0.
 \tag{O.23}
\]

Consequently, for sufficiently large `L`, one full-`T^2` packet obeying
the total-frequency cap and frozen high-frequency threshold satisfies

\[
 \boxed{
 \mathfrak X_{K,23}^{\rm tor}
 \le C_{\vartheta,B}(p_{K,23}^{\rm tor})^{2/3}.}
 \tag{O.24}
\]

This is the first certified row in the current route that simultaneously
retains horizontal interference, vertical diffusion, the physical
radial-collar Fourier row, the calibrated `R^(-2)` shear size, and a
bounded coefficient against its own full-torus two-thirds atom. This is
not yet the Version-M payment; the full-torus and constant-shear
restrictions remain decisive.

## 5. Status boundary

**Proved:** the arbitrary-vertical-frequency energy estimate O.4--O.12;
the total-frequency-capped cubic conversion O.13--O.17; the canonical
radial-collar insertion O.18--O.20; the exact paid-frequency threshold
O.21--O.22; and the frozen `kappa=3/2` closure O.23--O.24.

**Not proved:** a replacement of the full-`T^2` cubic atom by the buffered
physical-collar atom; stability under nonconstant `b(t,x_3)`; inter-packet
summation; low horizontal difference control; removal of the total upper-
frequency cap; E.24; complete-clock extraction; fixed deletion;
suitable-weak transfer; or any regularity or singularity conclusion. No
novelty or priority claim is made. \(\mathbf{NOT\ CLAY}.\)
