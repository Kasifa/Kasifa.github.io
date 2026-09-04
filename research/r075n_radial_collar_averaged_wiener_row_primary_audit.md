# Primary mathematical audit of R0.75N

## 0. Frozen object and verdict

Audited file: `research/r075n_radial_collar_averaged_wiener_row.md`.

Frozen SHA-256:
`ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318`.

**Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.**

The note proves that a canonical smooth radial representative of the
frozen outer-collar cover has `x_1`-averaged derivative Fourier row
`sum_l ||d_l||_infinity<=Ca=O(L)`, without any negative power of `R`.
After averaging both transverse variables, the corresponding row is
`O(Ra^2)=O(L^2R)`. It does not prove a local cubic-payment or
nonconstant-shear flux estimate.

The four frozen inputs recompute as

| input | SHA-256 |
|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` |
| `research/r075c_background_shear_packing_false_positive.md` | `1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89` |
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` |
| `research/r075m_dyadic_packet_diffusive_flux_gain.md` | `13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7` |

## 1. Canonical-cutoff compatibility, N.1--N.5

R0.75B leaves freedom to choose the complementary cutoff inside a fixed
enlargement of the radial outer collar. The shell cutoff and the interior
piece can both be chosen radial. Their difference is supported on a fixed
compact set of the normalized coordinate `(|x|-r)/R`. A fixed smooth
nonnegative profile `vartheta`, equal to one on that set, therefore gives
an admissible cover with bounds `|nabla^j xi|<=C_jR^(-j)`.

For the frozen `r=pLR`, scaling gives `a=r/R=pL`. Once `L` is large,
`a>=max(2delta,1)` and `(a+delta)R<pi/2`, so the Euclidean support lies in
one central torus chart. No periodic copy or boundary term is lost.

The R0.75E coefficient is

\[
 \Xi_\ell(x_3)=\int_{x_1}\frac1{2\pi}\int_{x_2}
 \xi(x)e^{-i\ell x_2}\,dx_2dx_1.
\]

Periodic integration by parts gives

\[
 \frac1{2\pi}\int_{x_2}\partial_2
 \left(\int_{x_1}\xi\,dx_1\right)e^{-i\ell x_2}\,dx_2
 =i\ell\Xi_\ell(x_3).
\]

Thus the `d_l` convention, its sign, and `d_0=0` in N.5 are exact.

## 2. Fourier-sample lemma, N.6--N.9

Let `N=floor(R^(-1))`. For the low samples,

\[
 R^\nu\sum_{|\ell|\le R^{-1}}
 \sup_z|\widehat h_z(\ell R)|
 \le CR^{\nu-1}\sup_z\|h_z\|_1.
\]

For nonzero high samples, compact support and `W^(2,1)` regularity justify
two integrations by parts:

\[
 |\widehat h_z(\ell R)|
 \le |\ell R|^{-2}\|h_z''\|_1.
\]

The elementary tail bound
`sum_(|l|>R^(-1))l^(-2)<=CR` then gives another
`CR^(nu-1)sup_z||h_z''||_1`. This proves N.8 with the supremum taken
inside the sum. The proof does not rely on monotonicity of
`|hat h|`, a Riemann-sum approximation, or pointwise Fourier decay beyond
the audited two integrations by parts.

## 3. Slice geometry and scaling, N.10--N.13

With `x_1=Ru`, `x_2=Ry`, and `x_3=Rz`, central support gives

\[
 \int_{x_1}\xi(x_1,Ry,Rz)\,dx_1=RG_{a,z}(y).
\]

One `x_2` derivative cancels that factor `R`, and the Fourier coefficient
then acquires exactly one Jacobian factor:

\[
 d_\ell(Rz)=\frac R{2\pi}\widehat h_{a,z}(\ell R).
\]

For `|z|<=a-delta`, the cross-sectional area of the scaled shell is

\[
 \pi\bigl((a+\delta)^2-z^2\bigr)
 -\pi\bigl((a-\delta)^2-z^2\bigr)=4\pi a\delta.
\]

For `a-delta<|z|<=a+delta`, only the outer disk remains and its area is at
most the same value. Outside that range the slice is empty. This verifies
N.12 uniformly through spherical tangencies.

On the support, the scaled radius is at least `a-delta>=a/2>=1/2`.
The first and third `y` derivatives of the radial composite are therefore
bounded by constants depending only on finitely many derivatives of
`vartheta`. Fubini gives

\[
 \sup_z\bigl(\|G_{a,z}'\|_1+
 \|G_{a,z}'''\|_1\bigr)\le C_\vartheta a.
\]

Since `h=G'` and `h''=G'''`, the family form of N.8 with `nu=1` yields
`sum_l sup_z|d_l(Rz)|<=C_vartheta a`. This is exactly N.2 and is stronger
than a supremum placed outside the Fourier sum.

## 4. Full transverse average, N.14--N.16

Integrating in both `x_1` and `x_3` contributes the scaling factor `R^2`:

\[
 \overline\xi(Ry)=R^2G_a(y),
 \qquad D_\ell=\frac{R^2}{2\pi}\widehat h_a(\ell R).
\]

The scaled shell volume is bounded by

\[
 \frac{4\pi}{3}\bigl((a+\delta)^3-(a-\delta)^3\bigr)
 \le C_\delta a^2
\]

for `a>=max(2delta,1)`. The same first/third derivative argument gives
`||h_a||_1+||h_a''||_1<=C_vartheta a^2`. Applying N.8 with `nu=2`
leaves `R^(2-1)a^2=Ra^2`, proving N.3.

## 5. High-frequency diagnostic, N.17

If `K>=R^(-3/2)` and `0<R<=1`, then `K^(-2/3)<=R`. Multiplying N.2 and
N.3 by that inequality gives exactly

\[
 \left(\sum_\ell\|d_\ell\|_\infty\right)K^{-2/3}
 \le C_\vartheta LR,
 \qquad
 \left(\sum_\ell|D_\ell|\right)K^{-2/3}
 \le C_\vartheta L^2R^2.
\]

This is only a coefficient calculation. The note does not apply the
one-dimensional R0.75M time kernel slice by slice to a vertically
diffusing or nonconstant-shear field, and it does not replace the
full-torus cubic mass by a collar atom.

## 6. Structure and claim-boundary audit

- Equation tags N.1--N.17 are unique and consecutive.
- Every internal N-reference resolves.
- All 17 display-math environments are paired.
- The four frozen input hashes match.
- The main note contains no disallowed control byte.
- The canonical radial profile is an allowed choice, not a theorem about
  every previously unspecified admissible cutoff.
- Spherical tangencies and the sum of coefficientwise `x_3` suprema are
  both included.
- Vertical diffusion, nonconstant shear, local cubic payment, packet
  summation, low differences, E.24, complete clock, fixed deletion,
  suitable-weak transfer, regularity, and singularity remain open.
- No simulation, numerical fit, novelty, priority, or Clay claim is made.

The R0.75N mathematical claims are internally consistent and ready for an
independent finite certificate. **NOT CLAY.**
