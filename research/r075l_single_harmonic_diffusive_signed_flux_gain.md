# R0.75L -- diffusive high-frequency gain for one real shear harmonic

## 0. Result and exact boundary

R0.75K shows that a fixed positive adjoint entrance weight loses the
high-frequency cancellation of the signed collar source.  The present note
returns to the physical signed flux and asks whether diffusion itself
creates a measurable gain before any positive majorant is introduced.

For a constant shear and one real horizontal harmonic of frequency `k`,
the answer is yes.  If `k^2 T>=1`, then

\[
 \boxed{
 |\mathcal T_{k,\eta}|
 \le C_*|B|V_\xi k^{-2/3}M_k^{2/3},}
 \tag{L.1}
\]

where `B` is the constant shear, `V_xi=int|partial_2 xi|`, and `M_k` is
the full spacetime cubic mass of the passive harmonic.  The exponent
`k^(-2/3)` is exact for the elementary conversion used here: the flux has
a `k^(-2)` diffusive time integral, whereas `M_k^(2/3)` has size
`k^(-4/3)`.

This is a genuine bound for the physical signed source, unlike the
positive-majorant boundary row in R0.75K.  It is nevertheless only a
constant-shear, single-real-harmonic benchmark with a full-torus cubic
mass.  It does not sum arbitrary cross modes, localize the cubic mass to
the frozen spherical collar, treat `x_3`-dependent shear, or prove E.24.

## 1. Frozen inputs and exact subfamily

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` | signed difference-frequency flux and E.24 |
| `research/r075g_signed_flux_gain_threshold.md` | `f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41` | exact `R^alpha` threshold |
| `research/r075k_positive_majorant_high_frequency_trace_loss.md` | `9282fb30eb7517853759fb835579220e0da763974d5543e2fb260ec8ca6daebf` | fixed-positive-weight high-frequency loss |

Work on `[0,T] times T`, with the circle represented by `[0,2pi]`.  Let
`B` be a real constant and set

\[
 \mathcal L_B:=\partial_t+B\partial_2-\partial_2^2.
 \tag{L.2}
\]

Let `xi` be any smooth periodic real cutoff and let `eta` be any measurable
time weight satisfying `0<=eta<=1`.  Define

\[
 V_\xi:=\int_0^{2\pi}|\partial_2\xi(x_2)|\,dx_2.
 \tag{L.3}
\]

For an integer `k>=1` and amplitude `A>0`, put

\[
 F_k(t,x_2)
 :=A e^{-k^2t}\cos\bigl(k(x_2-Bt)\bigr).
 \tag{L.4}
\]

The phase and amplitude cancellations give

\[
 \boxed{\mathcal L_BF_k=0.}
 \tag{L.5}
\]

This is a smooth real passive solution.  The unused variables can be
restored as normalized constant factors, but the result is not asserted
for a nonconstant `x_3` shear.

## 2. Exact diagonal cancellation and diffusive flux bound

The physical signed cutoff flux is

\[
 \mathcal T_{k,\eta}
 :=\frac12\int_0^T\!\int_0^{2\pi}
 \eta(t)B\partial_2\xi(x_2)|F_k(t,x_2)|^2\,dx_2dt.
 \tag{L.6}
\]

Using

\[
 |F_k|^2
 =\frac{A^2e^{-2k^2t}}2
 \left[1+\cos\bigl(2k(x_2-Bt)\bigr)\right],
 \tag{L.7}
\]

the constant horizontal mode makes no contribution because
`int partial_2 xi=0`.  Hence

\[
 \mathcal T_{k,\eta}
 =\frac{A^2B}{4}\int_0^T\eta(t)e^{-2k^2t}
 \left(\int_0^{2\pi}\partial_2\xi(x_2)
 \cos\bigl(2k(x_2-Bt)\bigr)\,dx_2\right)dt.
 \tag{L.8}
\]

Taking the absolute value only after this exact diagonal cancellation gives

\[
 \begin{aligned}
 |\mathcal T_{k,\eta}|
 &\le\frac{A^2|B|V_\xi}{4}
       \int_0^T e^{-2k^2t}\,dt\\
 &=\frac{A^2|B|V_\xi}{8k^2}
   \bigl(1-e^{-2k^2T}\bigr)\\
 &\le\frac{A^2|B|V_\xi}{8k^2}.
 \end{aligned}
 \tag{L.9}
\]

The `k^(-2)` factor is the ordinary horizontal heat decay of this exact
mode.  No enhanced-dissipation theorem, resolvent estimate, or stochastic
representation is used.

## 3. Conversion to the spacetime cubic payment

The exact full-torus cubic mass is

\[
 \begin{aligned}
 M_k
 &:=\int_0^T\!\int_0^{2\pi}|F_k|^3\,dx_2dt\\
 &=\frac{8A^3}{9k^2}\bigl(1-e^{-3k^2T}\bigr).
 \end{aligned}
 \tag{L.10}
\]

Assume

\[
 k^2T\ge1.
 \tag{L.11}
\]

Then `1-e^(-3k^2T)>=1-e^(-3)`, and (L.10) gives

\[
 A^2
 \le\left(\frac9{8(1-e^{-3})}\right)^{2/3}
 k^{4/3}M_k^{2/3}.
 \tag{L.12}
\]

Substituting (L.12) into (L.9) proves (L.1), with

\[
 C_*:=\frac18
 \left(\frac9{8(1-e^{-3})}\right)^{2/3}.
 \tag{L.13}
\]

Both sides scale like `A^2`; the gain cannot be created by passive-amplitude
normalization.  It comes from comparing the heat time integral with the
two-thirds power of the cubic time integral.

## 4. Target normalization and exponent diagnostic

For fixed positive `R,omega`, define the full-torus diagnostic atom and
normalized flux

\[
 p_k^{\rm tor}:=R^{-2}\omega M_k,
 \qquad
 \mathfrak X_k^{\rm tor}:=\frac\omega R
 [\mathcal T_{k,\eta}]_+.
 \tag{L.14}
\]

Equation (L.1) becomes

\[
 \boxed{
 \mathfrak X_k^{\rm tor}
 \le C_*|B|V_\xi
 R^{1/3}\omega^{1/3}k^{-2/3}
 (p_k^{\rm tor})^{2/3}.}
 \tag{L.15}
\]

This is not yet the frozen Version-M estimate: `p_k^tor` uses the whole
circle, and `|B|V_xi` has not been converted into the frozen background
atom.  It does isolate the exact frequency factor that survives the target
normalization.

If a future paid high-frequency decomposition has `k>=R^(-kappa)`, then

\[
 k^{-2/3}\le R^{2\kappa/3}.
 \tag{L.16}
\]

Purely at the exponent-diagnostic level, this factor exceeds the R0.75G
threshold `R^(alpha_*)` when

\[
 \boxed{
 \kappa>\frac32\alpha_*
 =\frac{27163}{71442}
 \approx0.3802105204.}
 \tag{L.17}
\]

This implication is conditional on paying every other coefficient and on
replacing the full-torus cubic mass by frozen local atoms.  It is not a
proof of G.1.

## 5. What fails beyond one harmonic

The proof uses three properties simultaneously:

1. one real `+/-k` pair produces only the diagonal zero mode and the
   difference frequencies `+/-2k` in `|F_k|^2`;
2. periodicity kills the zero mode before an absolute value is taken; and
3. both members of the pair have the same exact heat factor
   `e^(-k^2t)`.

For a general real passive field, `|F|^2` contains all differences `m-n`.
Even for constant shear, summing pairwise time-decay factors against the
local cubic payment requires a nontrivial convolution estimate.  For the
frozen `b(t,x_3)`, vertical diffusion and `x_3`-dependent modal phases add
another layer.  Localizing the full-torus cubic mass to the spherical
collar can also reintroduce frequency leakage.

The next valid target is therefore a paid high/low difference-frequency
split: use diffusive time decay and cutoff Fourier tails on the high part,
and reserve pathwise/resolvent or geometric information for the low part.
No such summation or low-frequency estimate is proved here.

## 6. Status boundary

**Proved:** the exact constant-shear passive family L.2--L.5; diagonal
cancellation before absolute values L.6--L.8; the `k^(-2)` flux bound L.9;
the exact cubic mass and `k^(-2/3)` payment gain L.10--L.13; the normalized
diagnostic L.14--L.15; and the conditional frequency threshold
L.16--L.17.

**Not proved:** a multimode convolution bound, localization of
`p_k^tor` to the frozen collar, payment of `|B|V_xi` by Version-M,
nonconstant-shear enhanced dissipation, the low difference-frequency
sector, E.24, complete-clock extraction, fixed deletion, suitable-weak
transfer, or any regularity or singularity conclusion.  No novelty or
priority claim is made.  \(\mathbf{NOT\ CLAY}.\)
