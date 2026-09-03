# R0.75E -- horizontal cross-mode flux reduction

## 0. Result and exact boundary

R0.75D reduces the passive outer-collar dissipation to a paid quadratic
row plus a localized shear-transport flux. The present note identifies the
exact horizontal spectral content of that flux.

For the frozen common-shear equation

\[
 (\partial_t+b(t,x_3)\partial_2-\Delta_{23})F=0,
 \tag{E.1}
\]

and the fixed outer-collar cutoff \(\xi=\xi_k^R(x_1,x_2,x_3)\), every
horizontal Fourier-diagonal contribution to the localized transport flux
vanishes. Only differences of distinct horizontal modes remain. As a
rigorous consequence,

\[
 \boxed{
 \partial_2F=0
 \quad\Longrightarrow\quad
 D_{k,R}^{{\rm out},F}
 \le C L^{2/3}\omega^{1/3}(P_R^M)^{2/3}
 \le C(P_R^M)^{2/3}\quad(L\ge L_0).}
 \tag{E.2}
\]

This holds for arbitrarily large payment and arbitrary vertical frequency
inside the admissible real zero-mode subclass. Thus the high-vertical-
frequency zero mode in R0.75D (D.9) obstructs a horizontal-to-full Rayleigh
inference, but it does **not** obstruct the target outer-dissipation
estimate itself.

The general real-valued field is different. A nonzero real horizontal
harmonic contains the pair \(\{n,-n\}\), and its \(2n\) difference frequency
can couple to the physical cutoff. Hence this note does not close the
arbitrary-field target, the complete clock, or any regularity statement.

## 1. Frozen inputs and notation

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | cutoff and local energy identity |
| `research/r075c_background_shear_packing_false_positive.md` | `1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89` | paid shear row and large-background boundary |
| `research/r075d_passive_gradient_route_screen.md` | `54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6` | passive fallback and remaining transport term |

Let

\[
 s_R=61R^2,\qquad t_2=65R^2,
 \tag{E.3}
\]

and retain the frozen time cutoff \(\eta_R\), which vanishes near \(s_R\),
equals one on \((64R^2,65R^2)\), and obeys
\(|\eta_R'|\le CR^{-2}\). The smooth periodic spatial cutoff satisfies

\[
 0\le\xi\le C,\qquad
 |\nabla\xi|\le CR^{-1},\qquad
 |\Delta\xi|\le CR^{-2},
 \tag{E.4}
\]

and is supported in the fixed enlargement of the spherical outer collar.
It generally depends on \(x_2\); suppressing that dependence would delete
the very flux under study.

Every statement below involving the Version-M payment \(P_R^M\) is
restricted to the same smooth periodic inversion-paired common-shear
solutions as R0.75B. In the real horizontal zero-mode sector, the required
pairing includes, for example, data \(f_0(x_3)\) odd in \(x_3\).

For smooth real \(F\), or for the algebraic complexification of (E.1), set

\[
 \begin{aligned}
 f_n(t,x_3)
 &:=\frac1{2\pi}\int_{-\pi}^{\pi}
 F(t,x_2,x_3)e^{-inx_2}\,dx_2,\\
 \widehat\xi_\ell(x_1,x_3)
 &:=\frac1{2\pi}\int_{-\pi}^{\pi}
 \xi(x_1,x_2,x_3)e^{-i\ell x_2}\,dx_2,\\
 \Xi_\ell(x_3)
 &:=\int_{-\pi}^{\pi}\widehat\xi_\ell(x_1,x_3)\,dx_1.
 \end{aligned}
 \tag{E.5}
\]

The \(x_1\)-average \(\Xi_\ell\), rather than the pointwise coefficient
\(\widehat\xi_\ell\), is the sharp object because \(F\) and \(b\) are
independent of \(x_1\).

## 2. Local energy identity, including the endpoint

Multiply (E.1) by \(\eta_R\xi\overline F\), integrate, and take the real
part. Because \(\eta_R(s_R)=0\),

\[
 \begin{aligned}
 &\frac12\int_{\mathbb T^3}\xi|F(t_2)|^2
 +\int_{s_R}^{t_2}\!\int_{\mathbb T^3}
 \eta_R\xi|\nabla_{23}F|^2\\
 &\qquad=\frac12\int_{s_R}^{t_2}\!\int_{\mathbb T^3}
 [\eta_R'\xi+\eta_R\Delta_{23}\xi]
 |F|^2+\mathcal T_\xi(F,b),
 \end{aligned}
 \tag{E.6}
\]

where the signed transport flux is

\[
 \mathcal T_\xi(F,b)
 :=\frac12\int_{s_R}^{t_2}\!\int_{\mathbb T^3}
 \eta_R b\,\partial_2\xi\,|F|^2.
 \tag{E.7}
\]

The sign in (E.7) is positive on the right because

\[
 -\operatorname {Re}\int\eta_R\xi b\overline F\,\partial_2F
 =\frac12\int\eta_Rb\,\partial_2\xi\,|F|^2.
 \tag{E.8}
\]

The endpoint in (E.6) is nonnegative. It may be discarded in an upper
estimate for the dissipation, but it is not itself silently identified
with a payment row.

## 3. Exact cross-mode identity

The horizontal modes remain invariant because \(b\) is independent of
\(x_2\):

\[
 \partial_tf_n-\partial_3^2f_n+(n^2+inb)f_n=0.
 \tag{E.9}
\]

In particular, an initially vanishing mode stays zero. Smoothness justifies
termwise multiplication and integration in the following identity:

\[
 \boxed{
 \mathcal T_\xi(F,b)
 =\pi\operatorname {Re}\sum_{n,m\in\mathbb Z}
 i(m-n)\int_{s_R}^{t_2}\!\int_{\mathbb T_{x_3}}
 \eta_R b\,\Xi_{m-n}f_n\overline{f_m}\,dx_3dt.}
 \tag{E.10}
\]

Indeed, the \(x_2\) integral selects
\(\ell+n-m=0\), hence \(\ell=m-n\). The common factor \(2\pi\) from the
period integral combines with the factor \(1/2\) in (E.7). Every diagonal
term \(n=m\) vanishes because its multiplier is \(i(m-n)=0\). Therefore

\[
 \boxed{\mathcal T_\xi\text{ is a purely off-diagonal,
 difference-frequency quantity.}}
 \tag{E.11}
\]

This is stronger information than the absolute estimate in R0.75D: a
large background cubic atom \(p_b\) does not by itself imply a large
localized transport flux.

## 4. Zero-flux spectral sectors

Let \(S\subset\mathbb Z\) contain the horizontal Fourier support of the
initial datum. By (E.9), it contains the support for every later time. If

\[
 \Xi_{m-n}(x_3)=0
 \quad\hbox{for a.e. }x_3
 \quad\hbox{whenever }n,m\in S,\ n\ne m,
 \tag{E.12}
\]

then every summand in (E.10) vanishes and

\[
 \mathcal T_\xi(F,b)=0.
 \tag{E.13}
\]

Condition (E.12) is a sufficient spectral-orthogonality condition; no
claim is made that a generic radial collar cutoff satisfies it for a
nontrivial real support.

Two exact special cases must be distinguished:

1. If \(S=\{0\}\), then \(F=f_0(t,x_3)\) is real-admissible and
   \(|F|^2\) is independent of \(x_2\). Thus (E.13) also follows directly
   from \(\int_{-\pi}^{\pi}\partial_2\xi\,dx_2=0\).
2. In the complexified scalar equation, a singleton \(S=\{n\}\) also has
   \(|F|^2=|f_n|^2\), so (E.13) holds. For \(n\ne0\), however, this is not
   by itself a real Navier--Stokes velocity field and is used only as an
   algebraic diagnostic.

## 5. Pure \(P^{2/3}\) payment on a zero-flux sector

Retain the R0.75D local cubic atom

\[
 p_F:=R^{-2}\omega
 \int_{I_{2R}}\!\int_{\operatorname {supp}\xi}|F|^3,
 \qquad p_F\le CP_R^M.
 \tag{E.14}
\]

When (E.13) holds, discard the nonnegative endpoint in (E.6), use (E.4),
and apply spacetime Hölder on the \(O(L^2R^5)\) collar cylinder. Exactly as
in R0.75D (D.18),

\[
 \begin{aligned}
 D_{k,R}^{{\rm out},F}
 &:=\frac\omega R\int_{s_R}^{t_2}\!\int
 \eta_R\xi|\nabla_{23}F|^2\\
 &\le C\omega R^{-3}
 \int_{I_{2R}}\!\int_{\operatorname {supp}\xi}|F|^2\\
 &\le CL^{2/3}\omega^{1/3}p_F^{2/3}\\
 &\le CL^{2/3}\omega^{1/3}(P_R^M)^{2/3}.
 \end{aligned}
 \tag{E.15}
\]

For the frozen calibration,

\[
 L^{2/3}\omega^{1/3}
 =L^{2/3}\exp\!\left(-\frac{c_\gamma}{12}L^2\right)
 \longrightarrow0.
 \tag{E.16}
\]

This proves (E.2) for all sufficiently large \(L\), with no small-payment
hypothesis and no use of the R0.75D interaction condition
\(p_bp_F^2\lesssim(P_R^M)^2\).

## 6. Why a real nonzero harmonic is not a singleton

For real \(F\),

\[
 f_{-n}=\overline{f_n}.
 \tag{E.17}
\]

Thus a nonzero real single harmonic has support \(S=\{n,-n\}\), not
\(S=\{n\}\). Writing

\[
 F=a(t,x_3)\cos(nx_2)+c(t,x_3)\sin(nx_2),
 \tag{E.18}
\]

gives

\[
 F^2=\frac{a^2+c^2}{2}
 +\frac{a^2-c^2}{2}\cos(2nx_2)
 +ac\sin(2nx_2).
 \tag{E.19}
\]

The constant term makes no contribution to (E.7), but the \(\pm2n\)
terms can couple to \(\Xi_{\pm2n}\). Even an \(x_2\)-even radial cutoff
does not force cancellation when the \(ac\sin(2nx_2)\) term is present.
Moreover, (E.9) is equivalent to

\[
 \begin{aligned}
 \partial_ta-\partial_3^2a+n^2a+nbc&=0,\\
 \partial_tc-\partial_3^2c+n^2c-nba&=0,
 \end{aligned}
 \tag{E.20}
\]

so the shear generally rotates a cosine component into a sine component.
There is no invariant real-singleton cancellation for \(n\ne0\).

## 7. The exact remaining gate

Define the positive signed cross-mode flux at the target normalization by

\[
 \begin{aligned}
 \mathfrak X_{\xi,R}(F,b)
 :=\frac{\pi\omega}{R}\Bigg[
 \operatorname {Re}\sum_{n\ne m}i(m-n)
 \int_{s_R}^{t_2}\!\int_{\mathbb T_{x_3}}
 \eta_Rb\,\Xi_{m-n}f_n\overline{f_m}\,dx_3dt
 \Bigg]_+.
 \end{aligned}
 \tag{E.21}
\]

Equations (E.6) and (E.15) yield the exact reduction

\[
 \boxed{
 D_{k,R}^{{\rm out},F}
 \le CL^{2/3}\omega^{1/3}(P_R^M)^{2/3}
 +\mathfrak X_{\xi,R}(F,b).}
 \tag{E.22}
\]

The absolute Hölder estimate from R0.75D gives

\[
 \mathfrak X_{\xi,R}(F,b)
 \le Cp_b^{1/3}p_F^{2/3},
 \tag{E.23}
\]

and D.23 is one sufficient way to make (E.23) quadratic in \(P_R^M\).
But (E.10)--(E.11) show why that condition can be wasteful: it discards
the flux sign, every modal phase, the diagonal cancellation, and the decay
of cutoff coefficients at separated frequencies.

The next proof target is therefore not a separate estimate for the total
background atom \(p_b\). It is a bound

\[
 \mathfrak X_{\xi,R}(F,b)\le C(P_R^M)^{2/3}
 \tag{E.24}
\]

obtained from signed phase mixing, difference-frequency decay, or a
localized cross-mode observability estimate. No such bound is proved here
for arbitrary real \(F\).

## 8. Status boundary

**Proved:** the complex local energy identity including its endpoint and
sign; horizontal support invariance; the exact difference-frequency
formula; diagonal cancellation; zero-flux closure under (E.12); and the
all-payment real zero-mode estimate (E.2).

**Algebraic diagnostic only:** the nonzero complex-singleton closure. It is
not promoted to a physical real Navier--Stokes result.

**Open:** (E.24) for arbitrary real fields, control of real \(\pm n\)
pairs and general cross-mode aggregation, cutoff Fourier tails at the
required norm, suitable-weak transfer, complete-clock extraction, fixed
deletion, and every regularity or singularity conclusion.

This is a strict structural reduction inside the frozen smooth exact
family. It neither solves nor materially claims to solve the Clay
Navier--Stokes problem. \(\mathbf{NOT\ CLAY}.\)
