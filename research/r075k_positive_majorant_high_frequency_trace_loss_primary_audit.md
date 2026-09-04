# Primary mathematical audit of R0.75K

## 0. Frozen object and verdict

Audited file:
`research/r075k_positive_majorant_high_frequency_trace_loss.md`.

Frozen SHA-256:
`9282fb30eb7517853759fb835579220e0da763974d5543e2fb260ec8ca6daebf`.

**Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.**

The note gives an exact real high-frequency passive family showing that a
fixed nontrivial nonnegative adjoint entrance weight cannot be paid
uniformly by the local spacetime cubic mass alone.  The actual physical
signed flux in the same family is zero.  Therefore the result obstructs a
specific positive-majorant payment route and is not a counterexample to
E.24.

The three frozen inputs recompute as

| input | SHA-256 |
|---|---|
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` |
| `research/r075i_diffusion_safe_block_participation.md` | `c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7` |
| `research/r075j_mean_zero_adjoint_flux_obstruction.md` | `960e3cbc18ac8207253a8802da215b3eac07a714ddbcc7209985f27a00c9ff4d` |

## 1. Operator and positive-majorant audit, K.2--K.7

For constant shear `b=1`, the passive operator and its periodic formal
adjoint are

\[
 \mathcal L=\partial_t+\partial_2-\partial_2^2,
 \qquad
 \mathcal L^*=-\partial_t-\partial_2-\partial_2^2.
\]

With `xi=sin x_2`, the physical source is `a=cos x_2`.  The smooth source
`q=1+cos x_2` obeys both `q>=a` and `q>=0`.  Reversing time in the
zero-terminal problem `L*Phi=q` gives a forward positivity-preserving
drift-diffusion equation, so `Phi>=0`.

Constant coefficients preserve each Fourier frequency.  Since `q` has
only modes `0,+1,-1`, so does `Phi(0)`.  Spatial integration removes the
drift and Laplacian and gives

\[
 -\frac d{dt}\int\Phi=\int q=2\pi.
\]

Together with `Phi(T)=0`, this yields

\[
 \int\Phi(0)=2\pi T>0.
\]

Thus all hypotheses of the R0.75J positive-majorant bound hold, and the
entrance row in K.7 has the correct factor `1/2`.

## 2. Passive-family audit, K.8--K.10

Set `y=x_2-t`.  For

\[
 F_k=Ae^{-k^2t}\cos(ky),
\]

direct differentiation gives

\[
 \partial_tF_k=-k^2F_k+Ak e^{-k^2t}\sin(ky),
\]

\[
 \partial_2F_k=-Ak e^{-k^2t}\sin(ky),
 \qquad
 -\partial_2^2F_k=k^2F_k.
\]

All three rows cancel in `L F_k`, proving K.9.  At `t=0`, the elementary
double-angle identity gives exactly

\[
 F_k(0)^2=\frac{A^2}{2}(1+\cos(2kx_2)).
\]

The field is smooth, real, periodic, and an exact passive solution.

## 3. Boundary-row and cubic-mass audit, K.11--K.14

The product of the `0,+/-1` modes of `Phi(0)` with the nonzero
`+/-2k` modes of `F_k(0)^2` has zero integral for every integer `k>=1`.
Therefore

\[
 \frac12\int\Phi(0)F_k(0)^2
 =\frac{A^2}{4}\int\Phi(0)
 =\frac{A^2\pi T}{2}.
\]

The factor audit is exact: one `1/2` comes from J.20 and one from
`cos^2=(1+cos(2kx))/2`.

Translation does not change the spatial absolute moment, and

\[
 \int_0^{2\pi}|\cos(kx)|^3\,dx=\frac83.
\]

Hence

\[
 \begin{aligned}
 M_k
 &=\frac{8A^3}{3}\int_0^T e^{-3k^2t}\,dt\\
 &=\frac{8A^3}{9k^2}(1-e^{-3k^2T})
 \le\frac{8A^3}{9k^2}.
 \end{aligned}
\]

Raising the last inequality to the two-thirds power and dividing the
fixed boundary row gives

\[
 \frac{B_k}{M_k^{2/3}}
 \ge\frac{\pi T}{2}\left(\frac98\right)^{2/3}k^{4/3}.
\]

The amplitude cancels exactly.  Multiplying `M_k` by the fixed factor
`R^(-2)omega` likewise cannot remove the divergence in `k`.  The claimed
failure of a frequency-uniform local-cubic payment is correct.

## 4. Signed-flux audit, K.15--K.16

For every fixed time, `F_k^2` contains only Fourier frequencies
`0,+2k,-2k`.  The source `a=cos x_2` contains only `+1,-1`.  Since
`2k` is never `1` for an integer `k>=1`, the spatial integral of their
product is zero at every time.  Thus

\[
 \mathcal T_k=0
\]

exactly, not merely asymptotically.  The fixed positive majorant has
introduced a zero mode that is absent from the signed source.  This proves
that the large boundary row measures loss in the argument rather than a
large target flux.

## 5. General fixed-weight audit, K.17--K.18

For a continuous fixed `W>=0` with positive integral,

\[
 \frac12\int WF_k(0)^2
 =\frac{A^2}{4}\int W
  +\frac{A^2}{4}\int W\cos(2kx).
\]

The second term tends to zero by the Riemann--Lebesgue lemma, while the
first is strictly positive.  The same `M_k=O(k^(-2))` calculation therefore
gives the general fixed-weight trace loss.  The quantifiers remain
correctly limited: `W` is fixed independently of `k`; the theorem does not
cover an `F`-dependent or frequency-adapted weight.

## 6. Source and claim-boundary audit

The source report accurately uses Albritton--Dong, Hu--Li, and
Gardner--Liss--Mattingly only as context for passive-drift,
positive-semigroup, and pathwise shear-diffusion methods.  None is
represented as proving K.13, a Version-M boundary payment, or E.24.  The
counterexample itself is derived entirely in the main note.

- Equation tags K.1--K.18 are unique and consecutive.
- Every internal K-reference resolves.
- All 18 display-math environments are paired.
- The three frozen input hashes match.
- The main note and source report contain no disallowed control bytes.
- The result concerns a fixed positive entrance weight and the local
  spacetime cubic atom alone.
- Signed kernels, frequency-adapted tests, and other full Version-M rows
  are not ruled out.
- E.24, transition and periodic geometry, complete clock, fixed deletion,
  suitable-weak transfer, regularity, and singularity remain open.
- No simulation, numerical fit, priority, or Clay claim is made.

The R0.75K mathematical claims are internally consistent and ready for an
independent finite certificate.  **NOT CLAY.**
