# Figure R0.71J - Parent-frame positive creation exceeds the heat-payment scale

**A.** For a finite parent-shell family, let
\(A_w=\sum_j\kappa_j^{-2}a_j\),
\(Z_\pm=\sum_j\kappa_j^{-2}z_jJ_j^\pm\), and
\(J_j=J_j^+-J_j^-\). The exact identity is

\[
 2Z_+=\partial_tA_w+2\nu\sum_j a_j+2Z_-.
\]

Only the derivative telescopes in time; the other two terms are
nonnegative. The panel evaluates the selected parent shell in the pure-heat
limit of panel B. With \(\theta=\nu K^2t\), \(\kappa=4K\), and
\(s=zJ/(\nu K^2)\), it becomes

\[
 2s_+=\partial_\theta A_0+32A_0+2s_-.
\]

At \(\theta_*=\log2/18\), the four displayed values are
\(2s_+=9.9575949356\times10^{-4}\),
\(\partial_\theta A_0=6.1286460100\times10^{-4}\),
\(32A_0=3.8289489256\times10^{-4}\), and \(2s_-=0\).
The two bar heights therefore agree exactly to the archived binary64
precision.

**B.** The fixed-energy, global-smooth 2D3C datum has the pure-heat limiting
profiles

\[
 B_0=4(e^{-34\theta}-e^{-52\theta}),
\]

\[
 D_0=32e^{-32\theta}+1156e^{-34\theta}
      +50e^{-50\theta}+2704e^{-52\theta},
\]

\[
 Y_0=2e^{-2\theta}+2e^{-32\theta}+68e^{-34\theta}
      +2e^{-50\theta}+104e^{-52\theta},
\qquad
 A_0=\frac{B_0^2}{D_0Y_0}.
\]

For a common ordinate the panel plots
\(B_0/B_0(\theta_*)\), \(D_0/3942\), \(Y_0/178\), and \(A_0/A_*\), where

\[
 A_*=A_0(\theta_*)=
 \frac{4}{57(2^{1/9}+44)(3\,2^{1/9}+4\,2^{7/9}+120)}
 \approx1.1965465392\times10^{-5}.
\]

These are closed-form fixed-window limiting profiles, not a finite-\(K\)
PDE trajectory.

**C.** For the broad parent frame from R0.71E section 10.1 and the global
cell \(\chi=1\), the selected parent shell gives, for all sufficiently large
dyadic \(K\),

\[
 Z_{\rm full}\geq\frac{A_*}{64K^2}.
\]

The parent support estimate and the exact 2D3C identity
\(L=(0,0,-V\partial_2w)\) give

\[
 H_{\rm full}\leq
 \frac{1-2^{-1/9}}{2\nu K^4}.
\]

The panel fixes \(\nu=1\) and plots these algebraic reference coefficients on
eleven dyadic frequencies. Their exponents are exact, not fitted. The ratio
obeys

\[
 \frac{Z_{\rm full}}{H_{\rm full}}
 \geq\frac{\nu A_*}{32(1-2^{-1/9})}K^2.
\]

The construction proves existence of a large-\(K\) threshold, but does not
quantify \(K_0\). The plotted locations therefore illustrate the exact
scaling laws; they are not individual finite-\(K\) certificates.

**D.** At the initial time, horizontal Fourier groups have the exact ledger

| group | \(\|F\|^2/K^2\) | \(d/K^4\) | \(B/K^3\) |
|---:|---:|---:|---:|
| \(|m|=0\) | 328 | 82 | 36 |
| \(|m|=1\) | 8 | 3860 | -36 |
| \(|m|=2\) | 164 | 0 | 0 |

Thus \(\sum B=0\), \(\sum\|F\|^2=500K^2\), and
\(\sum d=3942K^4\). The lower strip plots every normalized radius
\(\sqrt{m^2+n^2}/4\) for \(|m|\in\{0,1,2\}\) and
\(|n|\in\{4,5\}\). All six values lie in \([1,\sqrt2]\), where the selected
parent multiplier is exactly one. This verifies the frame support used in
panels A--C without replacing the parent frame by a specially chosen
two-ring multiplier.

All plotted values are closed-form evaluations. There is no DNS, ODE/PDE
time stepping, random sampling, regression, or fitted exponent. The result
is confined to the parent-only broad frame, global cell, and heat height
zero. It does not cover the later child refinement, matched cells,
denominator or refresh faces, another Navier--Stokes-specific budget, or a
full face-paid weighted-BV estimate. It proves no continuation theorem,
regularity statement, singularity statement, originality claim, or
Millennium-problem conclusion.
