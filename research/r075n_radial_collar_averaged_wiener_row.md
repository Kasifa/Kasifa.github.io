# R0.75N -- radial-collar averaged Wiener row without an `R^(-1)` loss

## 0. Result and exact boundary

R0.75M compresses all interference inside one horizontal dyadic packet
into the Wiener norm of the cutoff derivative. The physical R0.75E cutoff
is three-dimensional, radial in the central lift, and averaged in `x_1`
before it meets the horizontal modes. The present note computes the scale
of that averaged Fourier row.

Retain the frozen calibration

\[
 p=\frac{32}{63},\qquad a=pL,\qquad r=aR,
 \qquad 0<R\le1,qquad a\ge a_0.
 \tag{N.1}
\]

For a fixed smooth radial profile supported in an `O(R)` enlargement of
the outer collar, let `d_l(x_3)` be the horizontal Fourier coefficient of
the `x_1`-averaged derivative. Then

\[
 \boxed{
 \sum_{\ell\in\mathbb Z}
 \|d_\ell\|_{L^\infty_{x_3}}
 \le C_\vartheta a\le C_\vartheta L.}
 \tag{N.2}
\]

Thus the pointwise derivative size `O(R^(-1))` does not survive as a
negative power of `R` in the exact cross-mode Wiener row. If the cutoff is
also averaged in `x_3`, the corresponding one-dimensional row satisfies

\[
 \boxed{
 \sum_{\ell\in\mathbb Z}|D_\ell|
 \le C_\vartheta R a^2
 \le C_\vartheta L^2R.}
 \tag{N.3}
\]

The proof is a rescaling plus a low/high Fourier-sample split. It avoids
the crude periodic `H^1` estimate from R0.75M, whose second-derivative term
would lose `R^(-1/2)` after the same rescaling.

This is a geometric coefficient theorem. It does not extend the R0.75M
time kernel to `x_3`-dependent shear or vertical diffusion, localize the
full-torus cubic mass, sum dyadic packets, or prove E.24.

## 1. Frozen inputs and a canonical collar representative

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | admissible outer-collar cutoff |
| `research/r075c_background_shear_packing_false_positive.md` | `1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89` | `r=pLR`, `p=32/63`, and central lift |
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` | `x_1`-averaged difference-frequency coefficient |
| `research/r075m_dyadic_packet_diffusive_flux_gain.md` | `13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7` | dyadic Schur/Wiener reduction |

Fix `delta>0` and a nonnegative
`vartheta in C_c^infinity((-delta,delta))`. It may be chosen equal to one
on the normalized radial set supporting the complementary R0.75B clock
piece. Consequently the periodic lift of

\[
 \xi_{a,R}(x)
 :=\vartheta\!\left(\frac{|x|-r}{R}\right)
 =\vartheta\!\left(\frac{|x|}{R}-a\right)
 \tag{N.4}
\]

is an admissible canonical representative of the outer-collar cover.
Take `a>=max(2delta,1)` and `(a+delta)R<pi/2`. Its Euclidean support then
lies in the central torus chart, so periodization introduces no overlap in
any integral below. Derivatives of order `j` cost at most `C_jR^(-j)`.

For the R0.75E convention, define

\[
 \begin{aligned}
 \Xi_\ell(x_3)
 &:=\int_{-\pi}^{\pi}\frac1{2\pi}
 \int_{-\pi}^{\pi}\xi_{a,R}(x_1,x_2,x_3)
 e^{-i\ell x_2}\,dx_2dx_1,\\
 d_\ell(x_3)
 &:=\frac1{2\pi}\int_{-\pi}^{\pi}
 \partial_2\!\left(\int_{-\pi}^{\pi}\xi_{a,R}\,dx_1\right)
 e^{-i\ell x_2}\,dx_2
 =i\ell\Xi_\ell(x_3).
 \end{aligned}
 \tag{N.5}
\]

In particular `d_0=0` exactly. Formula (N.2) is stronger than
`sup_(x_3) sum_l |d_l(x_3)|<=CL`; the supremum is taken separately for
each Fourier coefficient before summation.

## 2. A scale-correct Fourier sampling lemma

Use the real-line Fourier transform

\[
 \widehat h(\zeta):=\int_{\mathbb R}h(y)e^{-i\zeta y}\,dy.
 \tag{N.6}
\]

If a family `h_z` is compactly supported, belongs to `W^(2,1)(R)`, and

\[
 \sup_z\bigl(\|h_z\|_{L^1}+\|h_z''\|_{L^1}\bigr)\le A,
 \tag{N.7}
\]

then for every `nu>=1` and `0<R<=1`,

\[
 R^\nu\sum_{\ell\in\mathbb Z}
 \sup_z|\widehat h_z(\ell R)|
 \le C R^{\nu-1}A.
 \tag{N.8}
\]

Indeed, for `|ell|<=R^(-1)` use
`|hat h_z(ell R)|<=||h_z||_1`; there are `O(R^(-1))` such integers. For
`|ell|>R^(-1)`, two integrations by parts give

\[
 |\widehat h_z(\ell R)|
 \le\frac{\|h_z''\|_{L^1}}{\ell^2R^2},
 \qquad
 \sum_{|\ell|>R^{-1}}\ell^{-2}\le CR.
 \tag{N.9}
\]

The two ranges both contribute at most `CR^(nu-1)A`. No comparison of a
discrete sum with an unsigned Riemann integral is assumed.

## 3. The `x_1`-averaged row

Write `x_3=Rz`, `x_2=Ry`, and set

\[
 G_{a,z}(y):=\int_{\mathbb R}
 \vartheta\!\left(\sqrt{u^2+y^2+z^2}-a\right)du,
 \qquad h_{a,z}:=G_{a,z}'.
 \tag{N.10}
\]

Central support and the change of variables `x_1=Ru` give

\[
 \int_{-\pi}^{\pi}\xi_{a,R}(x_1,Ry,Rz)\,dx_1
 =R G_{a,z}(y),
 \qquad
 d_\ell(Rz)=\frac{R}{2\pi}
 \widehat h_{a,z}(\ell R).
 \tag{N.11}
\]

If the slice meets the radial support, then `|z|<=a+delta`. Its scaled
two-dimensional support is

\[
 A_{a,z}:=left\{(u,y):
 \left|\sqrt{u^2+y^2+z^2}-a\right|<\delta\right\},
 \qquad |A_{a,z}|\le4\pi a\delta.
 \tag{N.12}
\]

For `|z|<=a-delta`, this is the exact difference of two disk areas. In
the tangency band `a-delta<|z|<=a+delta`, it is bounded by the same outer
disk difference. Since the radial variable on the support is at least
`a-delta>=a/2`, the first and third `y` derivatives of the smooth radial
profile are uniformly bounded. Differentiation under the integral and
Fubini therefore give

\[
 \sup_z\left(
 \|h_{a,z}\|_{L^1_y}
 +\|h_{a,z}''\|_{L^1_y}
 \right)
 \le C_\vartheta a.
 \tag{N.13}
\]

Apply (N.8) with `nu=1` to (N.11). This proves (N.2), including spherical
tangencies and every horizontal Fourier mode.

## 4. The fully averaged row

Define

\[
 \begin{aligned}
 \overline\xi_{a,R}(x_2)
 &:=\int_{\mathbb T_{x_1}}\int_{\mathbb T_{x_3}}
 \xi_{a,R}(x_1,x_2,x_3)\,dx_1dx_3,\\
 D_\ell
 &:=\frac1{2\pi}\int_{-\pi}^{\pi}
 \partial_2\overline\xi_{a,R}(x_2)e^{-i\ell x_2}\,dx_2.
 \end{aligned}
 \tag{N.14}
\]

With

\[
 G_a(y):=\int_{\mathbb R^2}
 \vartheta\!\left(\sqrt{u_1^2+y^2+u_3^2}-a\right)du_1du_3,
 \qquad h_a:=G_a',
 \tag{N.15}
\]

scaling gives

\[
 \overline\xi_{a,R}(Ry)=R^2G_a(y),
 \qquad
 D_\ell=\frac{R^2}{2\pi}\widehat h_a(\ell R).
 \tag{N.16}
\]

The scaled three-dimensional shell has volume at most `C_delta a^2`.
The same derivative and Fubini argument gives
`||h_a||_1+||h_a''||_1<=C_vartheta a^2`. Applying (N.8) with `nu=2`
proves (N.3).

## 5. Frequency diagnostic and remaining analytic gate

At the upper heat threshold isolated in R0.75D,
`K>=R^(-3/2)` implies

\[
 \boxed{
 \left(\sum_\ell\|d_\ell\|_\infty\right)K^{-2/3}
 \le C_\vartheta LR,
 \qquad
 \left(\sum_\ell|D_\ell|\right)K^{-2/3}
 \le C_\vartheta L^2R^2.}
 \tag{N.17}
\]

Hence neither within-packet mode count nor radial-collar Fourier geometry
forces a negative `R` power in the high-frequency coefficient. What
remains is genuinely dynamical and local: extend the R0.75M time-kernel
argument through vertical diffusion and nonconstant `b(t,x_3)`, replace
the full-torus cubic mass by buffered collar atoms without backward heat
amplification, and sum packet interactions including low differences.

## 6. Status boundary

**Proved:** a canonical radial cutoff compatible with the frozen outer
collar; the scale-correct Fourier sampling lemma N.6--N.9; the uniform
`x_1`-averaged coefficient row N.10--N.13; the fully averaged row
N.14--N.16; and the high-frequency coefficient diagnostic N.17.

**Not proved:** that the previously unspecified cutoff must have this
bound without choosing the canonical radial representative; a
two-dimensional or nonconstant-shear version of the R0.75M semigroup
estimate; local cubic payment; inter-packet or low-difference control;
E.24; complete-clock extraction; fixed deletion; suitable-weak transfer;
or any regularity or singularity conclusion. No novelty or priority claim
is made. \(\mathbf{NOT\ CLAY}.\)
