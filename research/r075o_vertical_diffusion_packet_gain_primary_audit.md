# R0.75O primary analytic audit

## Audit object

- Main note: `research/r075o_vertical_diffusion_packet_gain.md`
- Audit type: exact formula, normalization, scale, and claim-boundary audit
- Verdict: **PASS**
- Mathematical blocker count: **0**
- Release blocker count: **0**

The main-note SHA-256 is to be frozen by the finite certificate after the
text is independently reviewed. This audit is not an independent audit
and does not authorize publication by itself.

## 1. Dependency and model audit

The four frozen dependencies resolve and their stated SHA-256 values
match the repository snapshots:

| dependency | audited role |
|---|---|
| R0.75E | physical `x_1`-averaged off-diagonal flux and `pi` prefactor |
| R0.75G | `R,omega,rho,c_gamma`, required coefficient scale, and `R^(-2)` shear size |
| R0.75M | horizontal packet Schur/heat mechanism and normalization |
| R0.75N | canonical radial-collar row `sum_l ||d_l||_infinity<=C L` |

The equation is restricted to constant `B`. The note does not identify
the actual `x_3`-dependent frozen shear with this benchmark.

## 2. Exact flux and energy audit

With

\[
 H=\int_{\mathbb T_{x_1}}\xi\,dx_1,
 \qquad
 d_\ell=\frac1{2\pi}\int_{\mathbb T_{x_2}}
 \partial_2H\,e^{-i\ell x_2}\,dx_2,
\]

the `x_2` integral in the physical flux is `2*pi*d_(m-n)`; the outer
factor `1/2` therefore leaves exactly `pi*B`. Periodicity gives `d_0=0`,
so the diagonal vanishes before absolute values.

For each horizontal mode,

\[
 f_n(t)=e^{-n^2t}e^{-inBt}e^{t\partial_3^2}f_n^0.
\]

The vertical heat semigroup is an `L^2` contraction. Hence multiplication
by `d_(m-n)` costs `||d_(m-n)||_infinity`, while time integration costs
at most `1/(n^2+m^2)`. Since `|n|,|m|>=K`, both Schur row and column sums
are at most `mathcal W_infty/(2K^2)`.

Horizontal Parseval is

\[
 E_0=\int_{\mathbb T^2}|F_0|^2
 =2\pi\sum_n\|f_n^0\|_{L^2_{x_3}}^2.
\]

Thus

\[
 \pi|B|\frac{\mathcal W_\infty}{2K^2}
 \sum_n\|f_n^0\|_2^2
 =\frac{|B|\mathcal W_\infty}{4K^2}E_0.
\]

No upper vertical-frequency bound is used in this energy estimate.

## 3. Short-time cubic audit

For `n^2+j^2<=4K^2` and `t<=1/(8K^2)`, the squared `L^2` heat factor is
bounded below by `e^(-8K^2t)>=e^(-1)`. The measure of `T^2` is
`(2*pi)^2`, so Holder gives

\[
 \|F(t)\|_3^3\ge(2\pi)^{-1}\|F(t)\|_2^3
 \ge(2\pi)^{-1}e^{-3/2}E_0^{3/2}.
\]

The condition `K^2T>=1` contains the interval of length `1/(8K^2)`.
Therefore

\[
 M_K^{(2)}\ge\frac{e^{-3/2}}{16\pi}K^{-2}E_0^{3/2}.
\]

Raising the inverse inequality to power `2/3` gives

\[
 E_0\le e(16\pi)^{2/3}K^{4/3}(M_K^{(2)})^{2/3}.
\]

Multiplication by the energy coefficient `1/(4K^2)` uses the exact
identity

\[
 \frac{(16\pi)^{2/3}}4=(2\pi)^{2/3},
\]

which confirms O.2.

## 4. Normalization and exponent audit

From

\[
 p_{K,23}^{\rm tor}=R^{-2}\omega M_K^{(2)},
 \qquad
 \mathfrak X_{K,23}^{\rm tor}
 =\frac\omega R[\mathcal T_{K,\eta}^{(2)}]_+,
\]

one obtains

\[
 \frac\omega R(M_K^{(2)})^{2/3}
 =R^{1/3}\omega^{1/3}(p_{K,23}^{\rm tor})^{2/3}.
\]

R0.75N supplies `mathcal W_infty<=C_vartheta L`. If
`K>=R^(-kappa)` and `|B|<=C_BR^(-2)`, the remaining power is
`R^((2kappa-5)/3)`. Using

\[
 R=e^{-\rho L^2/4},\qquad
 \omega=e^{-c_\gamma L^2/4}
\]

gives negative exponential rate exactly when

\[
 \rho(5-2\kappa)<c_\gamma
 \quad\Longleftrightarrow\quad
 \kappa>\frac12\left(5-\frac{c_\gamma}{\rho}\right).
\]

For `rho=9/10000` and `c_gamma=8/3969`, exact rational arithmetic gives

\[
 \frac12\left(5-\frac{c_\gamma}{\rho}\right)
 =\frac{98605}{71442}.
\]

At `kappa=3/2`, the remaining exponent is

\[
 \frac\rho6-\frac{c_\gamma}{12}
 =-\frac{4279}{238140000}<0.
\]

The factor `L` is dominated by this strict exponential decay. At equality
in the threshold it is not dominated, so O.22 correctly uses `>`.

## 5. Quantifier and boundary audit

- The energy row allows arbitrary vertical frequencies but only constant
  shear and a finite horizontal packet.
- The cubic conversion additionally requires the total upper-frequency
  cap; this hypothesis is not hidden in O.1.
- Real admissibility is imposed by `c_(-n,-j)=conj(c_(n,j))` only where
  the finite two-dimensional packet is introduced.
- The result uses full-`T^2` cubic mass. It gives no inequality from that
  mass to the smaller buffered-collar atom.
- No inter-packet, low-difference, nonconstant-shear, or inverse-heat
  estimate is asserted.
- The exact R0.75G target E.24, complete clock, fixed deletion,
  suitable-weak transfer, regularity, and singularity remain open.
- The note makes no completeness, novelty, or priority claim and states
  **NOT CLAY**.

## Audit conclusion

All constants, Fourier factors, semigroup directions, packet hypotheses,
normalizations, rational exponents, and claim boundaries in the draft are
internally consistent. The note is ready for independent mathematical
audit and finite-certificate construction.
