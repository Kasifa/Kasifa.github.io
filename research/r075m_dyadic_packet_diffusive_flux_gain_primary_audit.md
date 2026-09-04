# Primary mathematical audit of R0.75M

## 0. Frozen object and verdict

Audited file:
`research/r075m_dyadic_packet_diffusive_flux_gain.md`.

Frozen SHA-256:
`13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7`.

**Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.**

The note extends the R0.75L one-harmonic calculation to every finite real
packet supported on `K<=|n|<=2K`.  It proves a mode-count-free
`K^(-2/3)` estimate for the physical signed cutoff flux, with the cutoff
derivative paid in its one-dimensional Wiener norm.  It does not sum
different dyadic packets, calibrate that Wiener norm in the frozen
spherical collar, replace the full-torus cubic mass by a Version-M atom,
or prove E.24.

The three frozen inputs recompute as

| input | SHA-256 |
|---|---|
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` |
| `research/r075g_signed_flux_gain_threshold.md` | `f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41` |
| `research/r075l_single_harmonic_diffusive_signed_flux_gain.md` | `52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5` |

## 1. Fourier convention and exact kernel, M.1--M.7

With

\[
 d_\ell=\frac1{2\pi}\int_0^{2\pi}\partial_2\xi(x_2)
 e^{-i\ell x_2}\,dx_2,
\]

the Fourier reconstruction is
`partial_2 xi=sum_l d_l exp(ilx_2)`.  Periodicity gives `d_0=0`.
For

\[
 F(t,x_2)=\sum_n c_ne^{-n^2t}e^{in(x_2-Bt)},
\]

one has

\[
 |F|^2=\sum_{n,m}c_n\overline{c_m}e^{-(n^2+m^2)t}
 e^{i(n-m)x_2}e^{-i(n-m)Bt}.
\]

The spatial integral against `partial_2 xi` is
`2pi d_(m-n)`.  Multiplication by the defining factor `B/2` therefore
gives exactly the coefficient `pi B` and the phase displayed in M.7.
The diagonal `n=m` is zero before absolute values are introduced.  The
reality condition `c_(-n)=conjugate(c_n)` is sufficient for a real
physical field but is not otherwise used in the estimate.

## 2. Time kernel, Schur row, and Parseval constant, M.8--M.11

Since `0<=eta<=1`,

\[
 \left|\int_0^T\eta(t)e^{-(n^2+m^2)t}
 e^{-i(n-m)Bt}\,dt\right|
 \le \int_0^\infty e^{-(n^2+m^2)t}\,dt
 =\frac1{n^2+m^2}.
\]

Every packet mode satisfies `|n|,|m|>=K`, hence
`n^2+m^2>=2K^2`.  For the nonnegative matrix in M.9, extending a finite
row from `m in Lambda_K` to all integer differences gives

\[
 \sum_m A_{nm}\le\frac1{2K^2}\sum_{\ell\in\mathbb Z}|d_\ell|
 =\frac{\mathcal W_\xi}{2K^2},
\]

and the same bound holds for columns.  Schur's test therefore controls
the absolute coefficient quadratic form by
`W_xi/(2K^2) sum_n |c_n|^2`.  Because the Fourier normalization gives

\[
 E_0=\int_0^{2\pi}|F_0|^2=2\pi\sum_n|c_n|^2,
\]

the outer factor `pi|B|` becomes

\[
 \frac{\pi|B|\mathcal W_\xi}{2K^2}\sum_n|c_n|^2
 =\frac{|B|\mathcal W_\xi}{4K^2}E_0.
\]

Thus the coefficient `1/4` in M.11 is exact for the stated convention.
No packet cardinality is hidden in the estimate.

## 3. Short-time cubic lower bound and inversion, M.12--M.16

For `|n|<=2K` and `0<=t<=1/(8K^2)`,
`exp(-2n^2t)>=exp(-8K^2t)>=exp(-1)`.  Parseval gives M.13.
On a circle of measure `2pi`, Holder gives

\[
 \|F(t)\|_3^3\ge(2\pi)^{-1/2}\|F(t)\|_2^3.
\]

The assumption `K^2T>=1` contains the whole interval of length
`1/(8K^2)`, so

\[
 M_K\ge c_0K^{-2}E_0^{3/2},
 \qquad c_0=\frac{e^{-3/2}}{8(2\pi)^{1/2}}.
\]

Raising `c_0^(-1)K^2M_K` to the power `2/3` yields

\[
 c_0^{-2/3}=4e(2\pi)^{1/3},
 \qquad
 E_0\le4e(2\pi)^{1/3}K^{4/3}M_K^{2/3}.
\]

Combining this row with M.11 cancels the factors `4` and leaves exactly
`e(2pi)^(1/3)|B|W_xi K^(-2/3)M_K^(2/3)`.  The passive-amplitude degree
is two on both sides.

## 4. Wiener/Sobolev row, M.17

Cauchy--Schwarz gives

\[
 \sum_\ell|d_\ell|
 \le\left(\sum_\ell(1+\ell^2)|d_\ell|^2\right)^{1/2}
 \left(\sum_\ell(1+\ell^2)^{-1}\right)^{1/2}.
\]

Parseval identifies the first factor, up to the fixed normalization
`(2pi)^(-1/2)`, with

\[
 \left(\|\partial_2\xi\|_2^2+
 \|\partial_2^2\xi\|_2^2\right)^{1/2}.
\]

The generic constant in M.17 therefore absorbs all normalization, and no
derivative above order two is used.  This is only a one-dimensional
regularity statement; it does not determine the frozen collar's
`R,L`-scaling.

## 5. Normalization and strict exponent threshold, M.18--M.20

From `p_K^tor=R^(-2)omega M_K`,

\[
 M_K^{2/3}=R^{4/3}\omega^{-2/3}
 (p_K^{\rm tor})^{2/3}.
\]

Multiplication by `omega/R` produces precisely
`R^(1/3)omega^(1/3)`, as in M.19.  If `0<R<1` and
`K>=R^(-kappa)`, then

\[
 K^{-2/3}\le R^{2\kappa/3}.
\]

The exponent strictly improves the frozen R0.75G requirement exactly
when

\[
 \frac{2\kappa}{3}>\frac{27163}{107163}
 \quad\Longleftrightarrow\quad
 \kappa>\frac{27163}{71442}
 \approx0.3802105204.
\]

Equality is not sufficient for a strict gain.  For `0<R<1`, increasing
the exponent makes the numerical power of `R` smaller; M.20 is an
exponent comparison, not a claim that the numerical factor itself is
larger.

## 6. Source, structure, and claim-boundary audit

The cited primary literature is used only for neighboring mechanism
classes: mode-by-mode passive-shear analysis, pathwise nonconstant-shear
control, and exact modal periodic-shear representations.  None is
represented as proving M.2, frozen-collar Wiener payment, Version-M
localization, or E.24.

- Equation tags M.1--M.20 are unique and consecutive.
- Every internal M-reference resolves.
- All 20 display-math environments are paired.
- The three frozen input hashes match.
- The main note and source report contain no disallowed control bytes.
- The theorem covers arbitrary finite interference inside one real
  dyadic packet only.
- Inter-packet summation, calibrated cutoff scaling, collar localization,
  low difference frequencies, nonconstant shear, E.24, complete clock,
  fixed deletion, suitable-weak transfer, regularity, and singularity
  remain open.
- No simulation, numerical fit, novelty, priority, or Clay claim is made.

The R0.75M mathematical claims are internally consistent and ready for an
independent finite certificate.  **NOT CLAY.**
