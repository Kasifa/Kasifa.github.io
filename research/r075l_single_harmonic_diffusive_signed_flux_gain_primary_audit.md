# Primary mathematical audit of R0.75L

## 0. Frozen object and verdict

Audited file:
`research/r075l_single_harmonic_diffusive_signed_flux_gain.md`.

Frozen SHA-256:
`52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5`.

**Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.**

The note proves a `k^(-2/3)` high-frequency factor for the physical signed
cutoff flux of one exact real constant-shear harmonic, measured against its
full-torus spacetime cubic mass.  It does not prove a multimode estimate,
collar-localized payment, or E.24.

The three frozen inputs recompute as

| input | SHA-256 |
|---|---|
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` |
| `research/r075g_signed_flux_gain_threshold.md` | `f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41` |
| `research/r075k_positive_majorant_high_frequency_trace_loss.md` | `9282fb30eb7517853759fb835579220e0da763974d5543e2fb260ec8ca6daebf` |

## 1. Passive solution audit, L.2--L.5

For `y=x_2-Bt` and

\[
 F_k=Ae^{-k^2t}\cos(ky),
\]

direct differentiation gives

\[
 \partial_tF_k=-k^2F_k+ABk e^{-k^2t}\sin(ky),
\]

\[
 B\partial_2F_k=-ABk e^{-k^2t}\sin(ky),
 \qquad
 -\partial_2^2F_k=k^2F_k.
\]

The amplitude, phase, and diffusion rows cancel exactly, so
`L_B F_k=0` for every real constant `B` and integer `k>=1`.  No property
of a nonconstant shear is assumed.

## 2. Signed-flux and diagonal-cancellation audit, L.6--L.9

The identity

\[
 F_k^2=\frac{A^2e^{-2k^2t}}2
 \left(1+\cos(2k(x_2-Bt))\right)
\]

has a zero-frequency row and the difference frequencies `+/-2k`.
Periodicity gives `int partial_2 xi=0`, so the zero mode is removed before
taking an absolute value.  The surviving term carries the factor
`A^2 B/4`, exactly as in L.8.

Since `0<=eta<=1`,

\[
 \left|\int\partial_2\xi
 \cos(2k(x_2-Bt))\,dx_2\right|
 \le V_\xi.
\]

The remaining time integral is

\[
 \int_0^T e^{-2k^2t}\,dt
 =\frac{1-e^{-2k^2T}}{2k^2}.
\]

Thus

\[
 |\mathcal T_{k,\eta}|
 \le\frac{A^2|B|V_\xi}{8k^2}
 (1-e^{-2k^2T})
 \le\frac{A^2|B|V_\xi}{8k^2}.
\]

Every factor and inequality direction in L.9 is correct.  The estimate is
for the physical signed source; it does not introduce a positive source
majorant.

## 3. Cubic-mass conversion audit, L.10--L.13

Translation preserves the spatial absolute moment, and

\[
 \int_0^{2\pi}|\cos(kx)|^3\,dx=\frac83.
\]

Therefore

\[
 M_k=\frac{8A^3}{3}\int_0^T e^{-3k^2t}\,dt
 =\frac{8A^3}{9k^2}(1-e^{-3k^2T}).
\]

If `k^2T>=1`, monotonicity of the exponential gives

\[
 1-e^{-3k^2T}\ge1-e^{-3}>0.
\]

Solving the exact mass relation for `A^2` then yields

\[
 A^2\le
 \left(\frac9{8(1-e^{-3})}\right)^{2/3}
 k^{4/3}M_k^{2/3}.
\]

Multiplication by the flux factor `k^(-2)/8` leaves `k^(-2/3)` and gives
exactly the constant `C_*` in L.13.  Both sides have passive-amplitude
degree two, so the gain is not an amplitude-normalization artifact.

## 4. Target-normalization and threshold audit, L.14--L.17

From `p_k^tor=R^(-2)omega M_k`,

\[
 M_k^{2/3}=R^{4/3}\omega^{-2/3}
 (p_k^{\rm tor})^{2/3}.
\]

Multiplication by `omega/R` produces precisely
`R^(1/3)omega^(1/3)`, confirming L.15.

If `k>=R^(-kappa)` with `0<R<1`, then

\[
 k^{-2/3}\le R^{2\kappa/3}.
\]

The inequality `2 kappa/3>alpha_*` is equivalent to

\[
 \kappa>\frac32\frac{27163}{107163}
 =\frac{27163}{71442}
 \approx0.3802105204.
\]

The main note correctly labels this only an exponent diagnostic.  The
full-torus atom and the unconverted `|B|V_xi` coefficient prevent it from
being a proof of G.1 or E.24.

## 5. Scope, source, and structural audit

The three literature sources are used only to establish neighboring
mechanism classes:

- He performs horizontal mode-by-mode enhanced-dissipation estimates and
  then sums modes under the paper's assumptions;
- Gardner--Liss--Mattingly use pathwise control for passive shear
  diffusion and obtain local streamline information;
- Jimenez-Urias--Haine give exact modal/Mathieu representations for
  periodic shear dispersion.

None is represented as proving L.1, the collar-localized conversion, or
E.24.  The local theorem uses ordinary heat decay, not an imported
enhanced-dissipation estimate.

- Equation tags L.1--L.17 are unique and consecutive.
- Every internal L-reference resolves.
- All 17 display-math environments are paired.
- The three frozen input hashes match.
- The main note and source report contain no disallowed control bytes.
- The result is limited to one real constant-shear harmonic and a
  full-torus cubic mass.
- Multimode convolution, collar localization, background payment,
  nonconstant shear, low difference frequencies, E.24, complete clock,
  fixed deletion, suitable-weak transfer, regularity, and singularity
  remain open.
- No simulation, numerical fit, priority, or Clay claim is made.

The R0.75L mathematical claims are internally consistent and ready for an
independent finite certificate.  **NOT CLAY.**
