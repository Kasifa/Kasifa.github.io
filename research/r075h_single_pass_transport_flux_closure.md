# R0.75H -- terminal-tube closure for the pure-transport collar flux

## 0. Result and exact boundary

R0.75G identifies `R^(1/3)` as a sufficient gain for the frozen signed
collar flux. The present note proves that gain in the exact pure-transport
benchmark, with the frozen nondecreasing time cutoff and a terminal tube of
the same collar volume.

Let `H` solve

\[
 \partial_tH+q'(t)\partial_2H=0
 \tag{H.1}
\]

on the periodic spatial domain, and let `xi` be a fixed nonnegative outer-
collar cutoff. Under the precise terminal-tube hypotheses in Section 1,
the full weighted signed flux obeys

\[
 \boxed{
 \mathfrak X_{\xi,R}^{\rm tr}(H,q)
 \le C L^{2/3}\omega^{1/3}R^{-2/3}
 (p_{F,J}^{\rm tr})^{2/3}.}
 \tag{H.2}
\]

The coefficient has the strict frozen rate

\[
 \lim_{L\to\infty}\frac1{L^2}
 \log\!\left(L^{2/3}\omega^{1/3}R^{-2/3}\right)
 =\frac\rho6-\frac{c_\gamma}{12}
 =-\frac{4279}{238140000}<0.
 \tag{H.3}
\]

Thus the pure-transport flux is paid by the corresponding benchmark
Version-M functional whenever the terminal tube lies in the frozen
scale-`2R` exterior measurement region. In a background with the matching
common-shear cubic size, (H.2) is exactly the `alpha=1/3` interaction scale
selected by R0.75G. The benchmark pair is not asserted to solve
Navier--Stokes.

This does **not** prove the passive advection-diffusion target E.24. When
diffusion is restored, the localized identity contains the unknown
dissipation itself; the terminal-tube argument alone then becomes circular.
The note proves the ballistic benchmark and isolates the diffusion
remainder, nothing more.

## 1. Frozen geometry and terminal tube

The note uses the following frozen inputs.

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | time cutoff, outer collar, and payment region |
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` | signed flux normalization |
| `research/r075f_modal_phase_integration_identity.md` | `f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440` | diffusive circularity boundary |
| `research/r075g_signed_flux_gain_threshold.md` | `f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41` | sufficient gain threshold |

Retain

\[
 R=\exp\!\left(-\frac\rho4L^2\right),\qquad
 \omega=\exp\!\left(-\frac{c_\gamma}{4}L^2\right),
 \qquad
 \rho=\frac9{10000},\quad c_\gamma=\frac8{3969}.
 \tag{H.4}
\]

Let `[s,t_2]` be the full time interval and let the frozen cutoff satisfy

\[
 0\le\eta_R\le1,qquad
 \eta_R(s)=0,qquad
 \eta_R(t_2)=1,qquad
 \eta_R'\ge0.
 \tag{H.5}
\]

Fix a terminal interval

\[
 J=[t_2-\delta_R,t_2],
 \qquad c_-R^3\le\delta_R\le c_+R^3,
 \tag{H.6}
\]

contained in the region where `eta_R=1`. Let `0<=xi<=1`, and denote its
spatial support by `Omega_0`. Suppose there is a measurable enlarged tube
`Omega_+` such that

\[
 \Omega_0-\bigl(q(t_2)-q(t)\bigr)e_2
 \subset\Omega_+
 \quad(t\in J),
 \qquad
 |\Omega_+|\le C_VL^2R^3.
 \tag{H.7}
\]

The subtraction in (H.7) is on the periodic domain using one fixed lift;
no seam crossing is allowed in this terminal passage. For the frozen
outer collar, (H.7) follows from its `O(R)` padding whenever

\[
 |q(t_2)-q(t)|\le c_qR
 \quad(t\in J).
 \tag{H.8}
\]

In particular, `|q'|<=C_q R^(-2)` and (H.6), with a sufficiently small
fixed `c_+`, imply (H.8). No lower speed is required for the theorem.

Finally assume the scale-`2R` exterior weight satisfies

\[
 W_{2R}\ge\omega
 \quad\hbox{on }J\times\Omega_+.
 \tag{H.9}
\]

These hypotheses are stated explicitly because the result is a local
terminal-tube theorem, not a whole-annulus or all-winding assertion.

## 2. Exact weighted transport identity

Define

\[
 E_\xi(t):=\int\xi(x)|H(t,x)|^2\,dx.
 \tag{H.10}
\]

Multiplication of (H.1) by `xi H` and periodic integration by parts gives

\[
 \frac12E_\xi'(t)
 =\frac12\int q'(t)\partial_2\xi|H|^2\,dx.
 \tag{H.11}
\]

Set

\[
 \mathcal T_{\xi,\eta}^{\rm tr}
 :=\frac12\int_s^{t_2}\!\int
 \eta_R q'(t)\partial_2\xi|H|^2\,dxdt.
 \tag{H.12}
\]

Using (H.5) and integrating (H.11) in time yields

\[
 \mathcal T_{\xi,\eta}^{\rm tr}
 =\frac12E_\xi(t_2)
 -\frac12\int_s^{t_2}\eta_R'(t)E_\xi(t)\,dt.
 \tag{H.13}
\]

Both `eta_R'` and `E_xi` are nonnegative, so

\[
 \boxed{
 [\mathcal T_{\xi,\eta}^{\rm tr}]_+
 \le\frac12E_\xi(t_2).}
 \tag{H.14}
\]

This is the full-window signed cancellation. It does not estimate the
absolute flux and introduces no block-count factor.

## 3. Terminal persistence and cubic payment

The characteristic formula is

\[
 H(t,x)=H\bigl(t_2,x+(q(t_2)-q(t))e_2\bigr).
 \tag{H.15}
\]

By (H.7), a change of variables gives, for every `t in J`,

\[
 \int_{\Omega_+}|H(t,x)|^2\,dx
 \ge\int_{\Omega_0}|H(t_2,x)|^2\,dx
 \ge E_\xi(t_2).
 \tag{H.16}
\]

Consequently

\[
 \int_J\!\int_{\Omega_+}|H|^2
 \ge\delta_RE_\xi(t_2).
 \tag{H.17}
\]

Spacetime Holder on `J times Omega_+` gives

\[
 \int_J\!\int_{\Omega_+}|H|^2
 \le(\delta_R|\Omega_+|)^{1/3}
 \left(\int_J\!\int_{\Omega_+}|H|^3\right)^{2/3}.
 \tag{H.18}
\]

Combining (H.17)--(H.18),

\[
 \boxed{
 E_\xi(t_2)
 \le\delta_R^{-2/3}|\Omega_+|^{1/3}
 \left(\int_J\!\int_{\Omega_+}|H|^3\right)^{2/3}.}
 \tag{H.19}
\]

No endpoint pointwise lower bound, frequency truncation, or observability
constant is used.

## 4. Exact `R^(1/3)` gain

Define the terminal-tube cubic atom

\[
 p_{F,J}^{\rm tr}
 :=R^{-2}\omega
 \int_J\!\int_{\Omega_+}|H|^3.
 \tag{H.20}
\]

Let \(P_R^{M,{\rm tr}}\) denote the same nonnegative Version-M measurement formula
evaluated on this pure-transport benchmark. This notation does not assert
that the benchmark pair is a Navier--Stokes solution. By (H.9), the atom is
bounded by a constant multiple of its scale-`2R` exterior velocity row and
hence

\[
 p_{F,J}^{\rm tr}\le C P_R^{M,{\rm tr}}.
 \tag{H.21}
\]

Normalize the positive flux exactly as in R0.75E:

\[
 \mathfrak X_{\xi,R}^{\rm tr}
 :=\frac\omega R
 [\mathcal T_{\xi,\eta}^{\rm tr}]_+.
 \tag{H.22}
\]

Equations (H.6), (H.7), (H.14), (H.19), and (H.20) give

\[
 \begin{aligned}
 \mathfrak X_{\xi,R}^{\rm tr}
 &\le C\frac\omega R
 (R^3)^{-2/3}(L^2R^3)^{1/3}
 (R^2\omega^{-1}p_{F,J}^{\rm tr})^{2/3}\\
 &\le C L^{2/3}\omega^{1/3}R^{-2/3}
 (p_{F,J}^{\rm tr})^{2/3}.
 \end{aligned}
 \tag{H.23}
\]

This proves (H.2). Using (H.4), its coefficient has rate

\[
 -\frac{c_\gamma}{12}+\frac\rho6
 =-\frac{4279}{238140000},
 \tag{H.24}
\]

which proves (H.3) and, with (H.21),

\[
 \boxed{
 \mathfrak X_{\xi,R}^{\rm tr}
 \le C(P_R^{M,{\rm tr}})^{2/3}
 \quad\hbox{for all sufficiently large }L.}
 \tag{H.25}
\]

If the background atom also has the frozen matching lower scale
`p_b >= c L^2 omega R^(-3)`, then

\[
 L^{2/3}\omega^{1/3}R^{-2/3}
 \le C R^{1/3}p_b^{1/3}.
 \tag{H.26}
\]

Thus (H.23) realizes the R0.75G `alpha=1/3` scale in this exact benchmark.

## 5. Why diffusion is not covered

For the actual passive equation

\[
 (\partial_t+b\partial_2-\Delta_{23})F=0,
 \tag{H.27}
\]

the frozen localized identity instead gives

\[
 \begin{aligned}
 \mathcal T_{\xi,\eta}(F,b)
 ={}&\frac12\int\xi|F(t_2)|^2
 +\int_s^{t_2}\!\int\eta_R\xi|\nabla_{23}F|^2\\
 &-\frac12\int_s^{t_2}\!\int
 [\eta_R'\xi+\eta_R\Delta_{23}\xi]|F|^2.
 \end{aligned}
 \tag{H.28}
\]

The first and last rows can be handled by terminal persistence and the
already-paid cutoff estimate. The middle row is precisely the unknown
outer-collar accumulated dissipation. Bounding the flux through (H.28)
would therefore assume the quantity needed to close E.24; this is the
R0.75F circularity in physical-space form.

The characteristic identity (H.15) also fails after diffusion. A valid
extension must replace it with information that is independent of the
target dissipation, for example a Feynman--Kac occupation estimate with a
separately paid initial/source row, a resolvent estimate for the signed
cutoff functional, or a plateau/transition decomposition with a genuinely
small commutator. None is proved here.

## 6. Status and minimum next proposition

**Proved:** the full-window signed pure-transport identity H.13--H.14,
terminal-tube persistence H.16--H.19, the exact payment estimate H.23,
the favorable frozen rate H.24, and the conditional identification with
the R0.75G `alpha=1/3` scale H.26.

**Open:** any analogue of H.16 or H.23 for the arbitrary diffusing frozen
passive field that does not reuse the unknown dissipation; shear-transition
bands; periodic recrossing beyond the terminal tube; E.24; complete-clock
extraction; fixed deletion; suitable-weak transfer; and all regularity or
singularity conclusions.

The minimum next proposition is a one-terminal-tube Feynman--Kac or
resolvent estimate that retains the signed cutoff functional and produces
some gain `R^alpha` with

\[
 \alpha>\frac{27163}{107163}
 \tag{H.29}
\]

without placing the target dissipation on its right-hand side. No
simulation or numerical fit is used. \(\mathbf{NOT\ CLAY}.\)
