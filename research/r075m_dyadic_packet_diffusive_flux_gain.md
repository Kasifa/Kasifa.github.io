# R0.75M -- dyadic-packet diffusive gain with a cutoff Wiener norm

## 0. Result and exact boundary

R0.75L obtains a `k^(-2/3)` physical signed-flux gain for one real
constant-shear harmonic.  The present note proves that the same exponent
survives arbitrary finite interference inside one dyadic horizontal
frequency packet.

Let the initial passive field have Fourier support
`K<=|n|<=2K`, where `K>=1`, and assume `K^2T>=1`.  If

\[
 d_\ell:=\frac1{2\pi}\int_0^{2\pi}
 \partial_2\xi(x_2)e^{-i\ell x_2}\,dx_2,
 \qquad
 \mathcal W_\xi:=\sum_{\ell\in\mathbb Z}|d_\ell|,
 \tag{M.1}
\]

then the physical signed flux obeys

\[
 \boxed{
 |\mathcal T_{K,\eta}|
 \le e(2\pi)^{1/3}|B|\mathcal W_\xi
 K^{-2/3}M_K^{2/3}.}
 \tag{M.2}
\]

Here `M_K` is the full-torus spacetime cubic mass.  The proof has two
independent pieces: a Schur estimate gives `K^(-2)` against the initial
quadratic energy, and a short-time heat lower bound converts that energy
to `K^(4/3)M_K^(2/3)`.  No pair count appears because the absolutely
summable cutoff Fourier coefficients absorb all within-packet
interference.

This is a strict extension of the R0.75L benchmark, but it remains a
constant-shear, full-torus, single-dyadic-packet result.  The scale of
`W_xi`, localization to the spherical collar, interactions between
different dyadic packets, nonconstant `x_3` shear, and E.24 are open.

## 1. Frozen inputs and packet solution

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` | exact difference-frequency flux |
| `research/r075g_signed_flux_gain_threshold.md` | `f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41` | required `R^alpha` gain |
| `research/r075l_single_harmonic_diffusive_signed_flux_gain.md` | `52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5` | one-harmonic heat/cubic conversion |

Work on `[0,T] times T` with

\[
 \mathcal L_B=\partial_t+B\partial_2-\partial_2^2,
 \qquad B\in\mathbb R.
 \tag{M.3}
\]

Let `Lambda_K={n in Z: K<=|n|<=2K}` and take a finite real-admissible
initial packet

\[
 F_0(x_2)=\sum_{n\in\Lambda_K}c_ne^{inx_2},
 \qquad c_{-n}=\overline{c_n}.
 \tag{M.4}
\]

Its exact passive evolution is

\[
 F(t,x_2)=\sum_{n\in\Lambda_K}
 c_ne^{-n^2t}e^{in(x_2-Bt)},
 \qquad \mathcal L_BF=0.
 \tag{M.5}
\]

Let `xi` be smooth and periodic, let `0<=eta<=1`, and define

\[
 \mathcal T_{K,\eta}
 :=\frac12\int_0^T\!\int_0^{2\pi}
 \eta(t)B\partial_2\xi(x_2)|F(t,x_2)|^2\,dx_2dt.
 \tag{M.6}
\]

Smoothness implies `W_xi<infinity`.  Section 4 records a quantitative
Sobolev bound requiring only the first two derivatives of `xi` in `L^2`.

## 2. Exact modal kernel and Schur estimate

Expanding `|F|^2`, using the coefficients in (M.1), and noting `d_0=0`
gives

\[
 \begin{aligned}
 \mathcal T_{K,\eta}
 =\pi B\sum_{n,m\in\Lambda_K}d_{m-n}c_n\overline{c_m}
 \int_0^T\eta(t)e^{-(n^2+m^2)t}
 e^{-i(n-m)Bt}\,dt.
 \end{aligned}
 \tag{M.7}
\]

The diagonal `n=m` vanishes before any absolute value is taken.  For every
remaining pair,

\[
 \left|\int_0^T\eta(t)e^{-(n^2+m^2)t}
 e^{-i(n-m)Bt}\,dt\right|
 \le\frac1{n^2+m^2}
 \le\frac1{2K^2}.
 \tag{M.8}
\]

For the nonnegative matrix

\[
 A_{nm}:=\frac{|d_{m-n}|}{n^2+m^2},
 \qquad n,m\in\Lambda_K,
 \tag{M.9}
\]

both row and column sums are bounded by

\[
 \sup_n\sum_mA_{nm}
 \le\frac{\mathcal W_\xi}{2K^2}.
 \tag{M.10}
\]

Schur's test and Parseval therefore give

\[
 \begin{aligned}
 |\mathcal T_{K,\eta}|
 &\le\frac{\pi|B|\mathcal W_\xi}{2K^2}
 \sum_{n\in\Lambda_K}|c_n|^2\\
 &=\frac{|B|\mathcal W_\xi}{4K^2}E_0,
 \qquad
 E_0:=\int_0^{2\pi}|F_0|^2.
 \end{aligned}
 \tag{M.11}
\]

Thus within-packet mode count does not appear.  If one discards the
Fourier tail and uses only `sup|d_l|`, the corresponding row sum can lose
one power of `K`; absolute summability is the precise anti-aggregation
input here.

## 3. Short-time conversion from energy to cubic mass

Set

\[
 M_K:=\int_0^T\!\int_0^{2\pi}|F(t,x_2)|^3\,dx_2dt.
 \tag{M.12}
\]

For `0<=t<=1/(8K^2)`, the upper packet edge `|n|<=2K` gives

\[
 \begin{aligned}
 \|F(t)\|_2^2
 &=2\pi\sum_{n\in\Lambda_K}|c_n|^2e^{-2n^2t}\\
 &\ge e^{-8K^2t}E_0
 \ge e^{-1}E_0.
 \end{aligned}
 \tag{M.13}
\]

On a circle of measure `2pi`, Holder gives

\[
 \|F(t)\|_3^3
 \ge(2\pi)^{-1/2}\|F(t)\|_2^3
 \ge(2\pi)^{-1/2}e^{-3/2}E_0^{3/2}.
 \tag{M.14}
\]

The assumption `K^2T>=1` ensures that the entire interval
`[0,1/(8K^2)]` lies inside `[0,T]`.  Integration yields

\[
 M_K
 \ge\frac{e^{-3/2}}{8(2\pi)^{1/2}}
 K^{-2}E_0^{3/2}.
 \tag{M.15}
\]

Equivalently,

\[
 E_0
 \le4e(2\pi)^{1/3}K^{4/3}M_K^{2/3}.
 \tag{M.16}
\]

Combining (M.11) and (M.16) proves (M.2).  The passive-amplitude degree is
two on both sides, and no inverse heat flow or entrance-trace estimate is
assumed.

## 4. The cutoff Wiener row

The exact anti-aggregation quantity in (M.2) is the Wiener norm of
`partial_2 xi`, not merely its pointwise derivative bound.  Cauchy--Schwarz
in Fourier space gives

\[
 \begin{aligned}
 \mathcal W_\xi
 &\le\left(\sum_{\ell\in\mathbb Z}(1+\ell^2)|d_\ell|^2\right)^{1/2}
 \left(\sum_{\ell\in\mathbb Z}(1+\ell^2)^{-1}\right)^{1/2}\\
 &\le C\left(
 \|\partial_2\xi\|_{L^2}
 +\|\partial_2^2\xi\|_{L^2}
 \right).
 \end{aligned}
 \tag{M.17}
\]

This shows that no derivative beyond the second is logically required in
the one-dimensional packet theorem.  It does not yet give the calibrated
`R,L` size of the `x_1,x_3`-dependent frozen collar cutoff after averaging,
nor show that the resulting coefficient is affordable.

## 5. Target normalization and remaining split

Define the full-torus diagnostic atom

\[
 p_K^{\rm tor}:=R^{-2}\omega M_K,
 \qquad
 \mathfrak X_K^{\rm tor}:=\frac\omega R
 [\mathcal T_{K,\eta}]_+.
 \tag{M.18}
\]

Then (M.2) gives

\[
 \boxed{
 \mathfrak X_K^{\rm tor}
 \le e(2\pi)^{1/3}|B|\mathcal W_\xi
 R^{1/3}\omega^{1/3}K^{-2/3}
 (p_K^{\rm tor})^{2/3}.}
 \tag{M.19}
\]

The same conditional exponent diagnostic as R0.75L follows: a paid packet
threshold `K>=R^(-kappa)` produces the factor `R^(2kappa/3)`, whose
exponent exceeds the R0.75G requirement only when

\[
 \kappa>\frac{27163}{71442}.
 \tag{M.20}
\]

The unresolved task is no longer interference inside one dyadic packet.
It is to control the sum over packet pairs, quantify the frozen cutoff
Wiener row, localize `M_K` to existing collar atoms, and handle the low
difference-frequency sector and nonconstant shear without circularity.

## 6. Status boundary

**Proved:** the exact finite-packet solution M.3--M.6; modal kernel and
diagonal cancellation M.7; the Schur/Wiener energy bound M.8--M.11; the
short-time cubic lower bound and energy conversion M.12--M.16; the
second-derivative Wiener estimate M.17; and the normalized dyadic-packet
diagnostic M.18--M.20.

**Not proved:** an inter-packet summation, the calibrated frozen-collar
size of `W_xi`, replacement of `p_K^tor` by existing local Version-M
atoms, nonconstant-shear control, the low difference-frequency sector,
E.24, complete-clock extraction, fixed deletion, suitable-weak transfer,
or any regularity or singularity conclusion.  No novelty or priority
claim is made.  \(\mathbf{NOT\ CLAY}.\)
