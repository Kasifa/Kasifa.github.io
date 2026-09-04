# R0.75K -- high-frequency trace loss for a fixed positive adjoint majorant

## 0. Result and exact boundary

R0.75J identifies a nonnegative adjoint majorant as the admissible
replacement for exact inversion of the sign-changing collar source.  The
present note tests whether the resulting initial boundary row can be paid
directly by the local spacetime cubic atom used in R0.75I.

The answer is negative for every fixed nontrivial nonnegative entrance
weight, even in a constant-shear one-dimensional subfamily.  There are
smooth real passive solutions `F_k` for which

\[
 \int_0^T\!\int |F_k|^3=O(k^{-2}),
 \qquad
 \int\Phi(0)|F_k(0)|^2\longrightarrow
 \frac{A^2}{2}\int\Phi(0)>0.
 \tag{K.1}
\]

Consequently no frequency-independent constant can bound the positive
majorant's entrance row by the two-thirds power of that spacetime cubic
mass.

For the explicit physical source `a=cos x_2`, the actual signed flux of
the same sequence is exactly zero.  Thus the obstruction is a loss in the
positive-majorant proof architecture, not a counterexample to E.24.  A
successful adjoint route must preserve signed/frequency cancellation,
adapt the test to the passive frequency content, or introduce an
independently controlled entrance-trace/frequency atom.  None of those
repairs is proved here.

## 1. Frozen setting

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` | signed flux and E.24 target |
| `research/r075i_diffusion_safe_block_participation.md` | `c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7` | local spacetime cubic atom |
| `research/r075j_mean_zero_adjoint_flux_obstruction.md` | `960e3cbc18ac8207253a8802da215b3eac07a714ddbcc7209985f27a00c9ff4d` | positive-majorant boundary architecture |

Work on `[0,T] times T`, where `T>0` is fixed and the circle is represented
by `[0,2pi]`.  The unused `x_1,x_3` variables can be restored as normalized
constant factors.  Take

\[
 \mathcal L=\partial_t+\partial_2-\partial_2^2,
 \qquad
 \mathcal L^*=-\partial_t-\partial_2-\partial_2^2.
 \tag{K.2}
\]

This is the frozen passive operator with smooth constant shear `b=1`.
Choose `eta=1` and `xi(x_2)=sin x_2`.  The physical signed source is

\[
 a=b\partial_2\xi=\cos x_2.
 \tag{K.3}
\]

Every construction below is smooth and periodic.  It is an exact passive
subfamily, not a Navier--Stokes solution.

## 2. A canonical smooth positive majorant

Define

\[
 q(x_2):=1+\cos x_2\ge a(x_2),
 \qquad q\ge0,
 \tag{K.4}
\]

and let

\[
 \mathcal L^*\Phi=q,
 \qquad \Phi(T)=0.
 \tag{K.5}
\]

After reversing time, semigroup positivity gives `Phi>=0`.  Because the
operator has constant coefficients and `q` contains only Fourier modes
`0,+/-1`, the entrance weight `Phi(0)` contains only those same modes.
Integrating (K.5) in space gives

\[
 -\frac d{dt}\int_0^{2\pi}\Phi(t,x_2)\,dx_2=2\pi,
 \qquad
 \boxed{\int_0^{2\pi}\Phi(0,x_2)\,dx_2=2\pi T.}
 \tag{K.6}
\]

Thus this admissible smooth majorant has a strictly positive zero Fourier
mode at the entrance time.  J.20 gives the valid upper bound

\[
 \mathcal T(F)
 \le\frac12\int_0^{2\pi}\Phi(0,x_2)|F(0,x_2)|^2\,dx_2.
 \tag{K.7}
\]

## 3. Exact high-frequency passive family

For every integer `k>=1` and amplitude `A>0`, set

\[
 F_k(t,x_2):=A e^{-k^2t}\cos\bigl(k(x_2-t)\bigr).
 \tag{K.8}
\]

The phase translation cancels the shear drift and the amplitude cancels
the Laplacian:

\[
 \boxed{\mathcal L F_k=0.}
 \tag{K.9}
\]

At the entrance time,

\[
 |F_k(0,x_2)|^2
 =\frac{A^2}{2}\bigl(1+\cos(2kx_2)\bigr).
 \tag{K.10}
\]

Since `Phi(0)` has only frequencies `0,+/-1`, Fourier orthogonality and
(K.6) give, for every integer `k>=1`,

\[
 \boxed{
 B_k:=\frac12\int_0^{2\pi}\Phi(0)|F_k(0)|^2
 =\frac{A^2\pi T}{2}.}
 \tag{K.11}
\]

The boundary payment is independent of `k`.

By contrast, `int_0^(2pi)|cos(kx)|^3 dx=8/3`, so the exact spacetime cubic
mass is

\[
 \begin{aligned}
 M_k
 &:=\int_0^T\!\int_0^{2\pi}|F_k|^3\,dx_2dt\\
 &=\frac{8A^3}{9k^2}\bigl(1-e^{-3k^2T}\bigr)
 \le\frac{8A^3}{9k^2}.
 \end{aligned}
 \tag{K.12}
\]

Therefore

\[
 \boxed{
 \frac{B_k}{M_k^{2/3}}
 \ge\frac{\pi T}{2}\left(\frac98\right)^{2/3}k^{4/3}
 \longrightarrow\infty.}
 \tag{K.13}
\]

For fixed `R,omega,T`, replacing `M_k` by the R0.75I atom
`p_k=R^(-2)omega M_k` changes only the fixed prefactor.  Hence there is no
constant independent of `k` for an estimate of the form

\[
 B_k\le C(R,\omega,T)p_k^{2/3}.
 \tag{K.14}
\]

This is an entrance-trace failure: rapid diffusion makes the spacetime
cubic mass small while the initial quadratic trace remains fixed.

## 4. The actual signed flux is zero

The physical signed flux for (K.3) and (K.8) is

\[
 \mathcal T_k
 :=\frac12\int_0^T\!\int_0^{2\pi}
 \cos x_2\,|F_k(t,x_2)|^2\,dx_2dt.
 \tag{K.15}
\]

For every time, `|F_k|^2` has only frequencies `0,+/-2k`.  Since no
integer `k>=1` satisfies `2k=1`, orthogonality gives

\[
 \boxed{\mathcal T_k=0.}
 \tag{K.16}
\]

The positive majorant has replaced the exact difference-frequency
cancellation by a positive zero mode.  Its boundary row is therefore
arbitrarily larger than the cubic payment even though the target signed
flux vanishes exactly.  This prevents using (K.13) as an E.24
counterexample.

## 5. General fixed-weight trace lemma

The mechanism is not special to (K.5).  Let `W` be any fixed continuous
nonnegative entrance weight on the circle with `int W>0`.  Then

\[
 \begin{aligned}
 \frac12\int_0^{2\pi}W(x)|F_k(0,x)|^2\,dx
 &=\frac{A^2}{4}\int_0^{2\pi}W(x)\,dx\\
 &\quad+\frac{A^2}{4}\int_0^{2\pi}W(x)\cos(2kx)\,dx.
 \end{aligned}
 \tag{K.17}
\]

The Riemann--Lebesgue lemma makes the second row tend to zero.  Combining
this positive limit with (K.12) proves that no fixed nontrivial
nonnegative entrance weight, independent of the passive frequency, can be
paid uniformly by `M_k^(2/3)` on this family.

This statement does not rule out an `F`-dependent adjoint test, a signed
kernel representation, frequency-localized cancellation, or payment by a
separate trace/frequency atom.  It only closes the tempting route

\[
 \text{fixed positive majorant}
 \quad+\quad
 \text{local spacetime cubic atom alone}.
 \tag{K.18}
\]

## 6. Consequence for the research route

The next admissible proposition must retain information destroyed by
source positivity.  There are three logically distinct options:

1. keep the signed adjoint kernel and control its negative dissipation row
   by frequency/phase cancellation;
2. build an `F`-dependent positive test whose entrance zero mode decays
   with the active frequency and whose dependence can be audited without
   circularity; or
3. add a genuinely available entrance-trace or frequency-weighted atom to
   the Version-M ledger and prove that its coefficient is affordable.

R0.75K proves none of these options.  It does prove that the raw
Feynman--Kac positivity route cannot simply invoke the existing local
spacetime cubic atom after (J.20).

## 7. Status boundary

**Proved:** the smooth positive majorant K.4--K.7; the exact real passive
family K.8--K.10; its frequency-independent boundary row K.11; the exact
cubic mass and divergent trace ratio K.12--K.14; the zero actual signed
flux K.15--K.16; and the general fixed-weight version K.17.

**Not proved:** failure of every adjoint/resolvent argument, failure of an
`F`-dependent test, failure of payment by any full Version-M row, a
counterexample to E.24, transition-band or periodic-copy control,
complete-clock extraction, fixed deletion, suitable-weak transfer, or any
regularity or singularity conclusion.  No novelty or priority claim is
made.  \(\mathbf{NOT\ CLAY}.\)
