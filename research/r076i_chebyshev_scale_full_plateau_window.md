# R0.76I -- Chebyshev-scale full-plateau window for exact shears

## 0. Result, imported input, and exact boundary

R0.76E proves a uniform full-plateau estimate for exact constant shears with
loss `exp(Cq)`, and therefore retains the frozen negative rate only when
`q=o(L^2)`.  The present note replaces that spatial loss by the endpoint
Chebyshev scale

\[
 \exp\!\left(12\sqrt2\,q\sqrt{\Delta_a}\right),
 \qquad
 \Delta_a:=\frac{\delta+\delta_0}{a-\delta_0}=O(a^{-1}).
 \tag{I.1}
\]

The only new nonlocal input is Proposition 4.2 of Ruizhe Zhang's July 2026
arXiv v1 preprint, *Optimal Extrapolation Bounds for Sparse Fourier Sums*.
It treats arbitrary real frequencies without a separation assumption.  We
verify its statement and every scaling step used below, but do not reproduce
the preprint's Hardy-space proof.  Accordingly, the boxed R0.76I theorem is
**CONDITIONAL-LITERATURE**: the local implication is proved, conditional on
the correctness of that cited proposition.  It is not presented as a fully
independent proof of the imported theorem.

Fix

\[
 q\in\mathbb N,\quad q\ge1,\qquad
 1\le n_1<\cdots<n_q\le2n_1,
 \quad n_j\in\mathbb N,
 \quad A_j\ge0,\quad \phi_j,B\in\mathbb R,
 \tag{I.2}
\]

and

\[
 F(t,x_2)=\sum_{j=1}^q A_j e^{-n_j^2t}
 \cos\bigl(n_jx_2-\phi_j-n_jBt\bigr).
 \tag{I.3}
\]

Retain R0.76E's `eta_R`, `xi_(a,R)`, full plateau tube, and functionals

\[
 \begin{aligned}
 \mathcal T_{\boldsymbol n,R}
 &:=\frac12\int_0^{4R^2}\!\int_{\mathbb T^3}
 \eta_R(t)B\,\partial_2\xi_{a,R}|F|^2\,dxdt,\\
 M_{\boldsymbol n,R}^{\rm plat}
 &:=\int_0^{4R^2}\!\int_{\mathcal S_{a,R}^{\rm plat}}
 |F|^3\,dxdt.
 \end{aligned}
 \tag{I.4}
\]

There are frozen constants `C_I<infinity` and `L_I<infinity`, independent
of `q`, `R`, the frequencies, amplitudes, phases, and `B`, such that every
frozen `L>=L_I` satisfies

\[
 \boxed{
 |\mathcal T_{\boldsymbol n,R}|
 \le C_I a^{2/3}R^{-1/3}q^7
 \exp\!\left(12\sqrt2\,q\sqrt{\Delta_a}\right)
 \bigl(M_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{I.5}
\]

For

\[
 p_{\boldsymbol n,R}^{\rm plat}
 :=R^{-2}\omega M_{\boldsymbol n,R}^{\rm plat},
 \qquad
 \mathfrak X_{\boldsymbol n,R}
 :=\frac\omega R[\mathcal T_{\boldsymbol n,R}]_+,
\]

this gives

\[
 \boxed{
 \mathfrak X_{\boldsymbol n,R}
 \le C_Ia^{2/3}q^7\omega^{1/3}
 \exp\!\left(12\sqrt2\,q\sqrt{\Delta_a}\right)
 \bigl(p_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{I.6}
\]

Consequently, every integer-valued mode count satisfying

\[
 q(L)=o(L^{5/2})
 \tag{I.7}
\]

retains the strict frozen rate

\[
 \boxed{
 \limsup_{L\to\infty}\frac1{L^2}
 \log\!\left[
 C_Ia^{2/3}q(L)^7\omega^{1/3}
 e^{12\sqrt2q(L)\sqrt{\Delta_a}}
 \right]
 =-\frac2{11907}.}
 \tag{I.8}
\]

This includes `q(L)` of order `L^2`.  The theorem is uniform over I.2 but
remains confined to exact real constant shears in one dyadic band.  It is
not an arbitrary Navier--Stokes packet estimate.

## 1. Full-plateau geometry and the shrinking exterior gap

Retain the frozen scaling

\[
 a=pL,\qquad R=e^{-\rho L^2/4},\qquad
 \omega=e^{-c_\gamma L^2/4},\qquad
 s=t/R^2,\qquad z=x_2/(aR),
 \tag{I.9}
\]

and set

\[
 \begin{aligned}
 G(s,z)&=F(R^2s,aRz),\\
 \kappa_j&=n_jaR,\qquad \alpha=\kappa_1,
 \qquad v=BR/a,\qquad
 \lambda=(\alpha/a)^2=(n_1R)^2.
 \end{aligned}
 \tag{I.10}
\]

Then

\[
 G_s+vG_z-a^{-2}G_{zz}=0,
 \qquad
 \alpha=\kappa_1<\cdots<\kappa_q\le2\alpha.
 \tag{I.11}
\]

Define

\[
 e_a:=1-\frac{\delta_0}{a},\qquad
 E_a=[-e_a,e_a],\qquad
 I_a=\left[-1-\frac\delta a,1+\frac\delta a\right],
 \tag{I.12}
\]

\[
 h(s):=\int_{E_a}|G(s,z)|^3dz,
 \qquad H:=\int_0^4h(s)ds.
 \tag{I.13}
\]

For large frozen `L`, `a>=delta+2delta_0`, `e_a>=1/2`, and
`0<=Delta_a<=1`.  After the map `z=e_ax`, the right endpoint becomes
`(1+delta/a)/e_a=1+Delta_a`; reflection gives the identical left
overshoot.  Thus `Delta_a` is the endpoint overshoot in the normalized
`x` coordinate, not the unscaled `z`-distance.  The shell
cross-section from R0.76H is exactly

\[
 \mathcal A_a(z)=\pi\left(
 [(a+\delta_0)^2-a^2z^2]_+
 -[(a-\delta_0)^2-a^2z^2]_+
 \right),
 \tag{I.14}
\]

so

\[
 \mathcal A_a(z)=4\pi a\delta_0\quad(z\in E_a),
 \qquad
 M_{\boldsymbol n,R}^{\rm plat}
 \ge4\pi\delta_0a^2R^5H.
 \tag{I.15}
\]

With

\[
 W_a(z)=-2\pi az\vartheta(a(|z|-1)),
 \qquad
 \Xi_a(z)=\int_{-\infty}^zW_a(r)dr,
 \tag{I.16}
\]

the factor `vartheta(a(abs(z)-1))` is even in `z`, so `W_a` is odd and
has total integral zero.
Since `supp vartheta` is contained in `(-delta,delta)`, both `Xi_a` and
the derivatives used below are supported in `I_a`.  The largest relative
distance from `E_a` to either endpoint of `I_a` is precisely I.1.

## 2. The imported endpoint extrapolation input

Let

\[
 \mathcal T_N=\left\{
 g(x)=\sum_{r=1}^Nc_re^{i\mu_rx}:c_r\in\mathbb C,
 \ \mu_r\in\mathbb R\right\}.
\]

Zhang's Proposition 4.2 states that for `g in T_N`, `0<=d<=1`,

\[
 |g(1+d)|
 \le\sqrt{\frac{9A_{\rm fr}}2}\,N
 e^{3\sqrt2N\sqrt d}\,
 \|g\|_{L^2[-1,1]},
 \qquad A_{\rm fr}\le8191.
 \tag{I.17}
\]

At each fixed `s`, the real function `G(s,.)` has at most `N=2q`
complex Fourier branches with real frequencies `+-kappa_j`.  Apply I.17
to `x -> G(s,e_ax)` on the right exterior, and to its reflection on the
left exterior.  After squaring, using `N<=2q`, and changing variables,

\[
 \sup_{I_a\setminus E_a}|G(s,z)|^2
 \le\frac{18A_{\rm fr}}{e_a}q^2
 e^{12\sqrt2q\sqrt{\Delta_a}}
 \int_{E_a}|G(s,z)|^2dz.
 \tag{I.18}
\]

On `E_a`, the endpoint Nikolskii inequality of Erdelyi gives the same
bound without the exponential factor.  Finally,

\[
 \int_{E_a}|G|^2
 \le |E_a|^{1/3}\left(\int_{E_a}|G|^3\right)^{2/3}
 \le2^{1/3}h(s)^{2/3}.
\]

Thus one frozen absolute `C_s` satisfies

\[
 \boxed{
 \|G(s)\|_{L^\infty(I_a)}^2
 \le C_sq^2e^{\Phi_a}h(s)^{2/3},
 \qquad
 \Phi_a:=12\sqrt2q\sqrt{\Delta_a}.}
 \tag{I.19}
\]

No frequency gap, amplitude lower bound, or phase condition is used.  If
all coefficients vanish, I.19 is trivial; otherwise zero coefficients and
duplicate branches are removed before applying the literature theorem.

## 3. A polynomial spatial derivative payment

Erdelyi's Markov-type inequality for a pure-imaginary `N`-term exponential
sum on `[0,1]` is

\[
 \|f'\|_{L^\infty[0,1]}
 \le(1+\epsilon_N)
 \left(108N^5+\sum_{r=1}^N\mu_r^2\right)^{1/2}
 \|f\|_{L^\infty[0,1]}.
 \tag{I.20}
\]

The factors `1+epsilon_N` are bounded by one absolute constant.  Map
`I_a`, whose length is uniformly bounded above and below, onto `[0,1]`.
There are at most `2q` frequencies, and

\[
 \sum_{j=1}^q\bigl(\kappa_j^2+(-\kappa_j)^2\bigr)
 \le8q\alpha^2.
\]

Scaling I.20 back and using I.19 gives

\[
 \boxed{
 \|G_z(s)\|_{L^\infty(I_a)}^2
 \le C_d(q^7+q^3\alpha^2)e^{\Phi_a}h(s)^{2/3}.}
 \tag{I.21}
\]

The powers are not optimized.  The `q^7` term is the product of the
`N^5` Markov payment and the `q^2` observation payment.

## 4. A polynomial terminal-time payment

For fixed `z` and `0<=r<=1`, reverse the final unit of the heat clock.
Writing `sigma in {+1,-1}`, the complex-branch representation of I.3 is

\[
 \begin{aligned}
 G(4-r,z)
 &=\sum_{j=1}^q\sum_{\sigma=\pm1}
 c_{j,\sigma}(z)e^{\gamma_{j,\sigma}r},\\
 \gamma_{j,\sigma}
 &=\left(\frac{\kappa_j}{a}\right)^2+i\sigma v\kappa_j,\\
 c_{j,\sigma}(z)
 &=\frac{A_j}{2}e^{-4(\kappa_j/a)^2}
 e^{i\sigma(\kappa_jz-\phi_j-4v\kappa_j)}.
 \end{aligned}
 \qquad
 N_z\le2q,\quad \operatorname {Re}\gamma_{j,\sigma}>0.
 \tag{I.22}
\]

Kós's endpoint inequality for `E_N^+`, recorded as equation (1.2) in
Erdelyi's journal paper, gives

\[
 |G(4,z)|
 \le2N_z\left(\int_3^4|G(s,z)|^2ds\right)^{1/2}.
 \tag{I.23}
\]

Because the time interval has length one, its `L^3` norm dominates its
`L^2` norm.  Cube I.23 and integrate over `E_a` to obtain

\[
 h(4)\le64q^3\int_3^4h(s)ds\le64q^3H,
 \qquad
 h(4)^{2/3}\le16q^2H^{2/3}.
 \tag{I.24}
\]

This replaces the `exp(Cq)` terminal row of R0.76E by a polynomial.

## 5. The inherited high-carrier onset payment

The delayed heat-clock proof of R0.76E is fibrewise in `z` and remains
valid after replacing its central interval by the measurable interval
`E_a`.  With `zeta(s)=eta_R(R^2s)`, it gives, when `lambda>1`,

\[
 \lambda\int_0^4\zeta(s)h(s)^{2/3}ds
 \le C_h[q\log(q+1)]^{4/3}\lambda^{-1/3}H^{2/3}.
 \tag{I.25}
\]

When `lambda<=1`, ordinary Hölder gives instead

\[
 \lambda\int_0^4\zeta(s)h(s)^{2/3}ds
 \le C_hH^{2/3}.
 \tag{I.26}
\]

Unlike R0.76E's old endpoint row, I.25 is already polynomial in `q`, so no
further imported time-observability theorem is needed.

## 6. Rebuilding the complete-real energy identity

Retain the exact profile bounds

\[
 \|\Xi_a\|_1+\|\Xi_a\|_\infty\le C_\Xi,
 \qquad
 \|\Xi_a''\|_1\le C_\Xi a,
 \tag{I.27}
\]

and put `mathcal E(s)=int Xi_aG^2`.  R0.76E's exact complete-real identity
is

\[
 \begin{aligned}
 v\int_0^4\zeta\int W_aG^2
 &=\zeta(4)\mathcal E(4)-\int_0^4\zeta'\mathcal E\,ds\\
 &\quad-a^{-2}\int_0^4\zeta\int\Xi_a''G^2
 +2a^{-2}\int_0^4\zeta\int\Xi_a|G_z|^2.
 \end{aligned}
 \tag{I.28}
\]

All spatial integrals in I.28 are supported in `I_a`.  Equations
I.19 and I.24 pay the terminal row:

\[
 |\mathcal E(4)|
 \le Cq^2e^{\Phi_a}h(4)^{2/3}
 \le Cq^4e^{\Phi_a}H^{2/3}.
 \tag{I.29}
\]

The cutoff row and curvature row obey

\[
 \int_0^4|\zeta'\mathcal E|ds
 \le Cq^2e^{\Phi_a}H^{2/3},
 \tag{I.30}
\]

\[
 a^{-2}\int_0^4\zeta
 \left|\int\Xi_a''G^2\right|ds
 \le Ca^{-1}q^2e^{\Phi_a}H^{2/3}.
 \tag{I.31}
\]

For the derivative row, I.21 gives

\[
 \begin{aligned}
 a^{-2}\int_0^4\zeta\int|\Xi_a||G_z|^2
 &\le Ce^{\Phi_a}
 \left[
 \frac{q^7}{a^2}\int_0^4\zeta h^{2/3}ds
 +q^3\lambda\int_0^4\zeta h^{2/3}ds
 \right].
 \end{aligned}
 \tag{I.32}
\]

The first term is at most `Cq^7e^(Phi_a)H^(2/3)`.  For `lambda<=1`,
I.26 pays the second.  For `lambda>1`, I.25 and `lambda^(-1/3)<=1` give

\[
 q^3[q\log(q+1)]^{4/3}H^{2/3}
 \le Cq^7H^{2/3},
 \tag{I.33}
\]

where only `q>=1` and `log(q+1)<=Cq` are used.  Combining I.28--I.33,

\[
 \boxed{
 \left|v\int_0^4\zeta\int W_aG^2\right|
 \le Cq^7e^{\Phi_a}H^{2/3}.}
 \tag{I.34}
\]

The proof keeps the complete real square until after I.28.  It does not use
a density projection, localized-current sign, spectral-gap division, or a
standalone carrier integration by parts.

## 7. Physical conversion and the enlarged mode window

The exact physical conversion is

\[
 \mathcal T_{\boldsymbol n,R}
 =\frac{a^2R^3}{2}v\int_0^4\zeta\int W_aG^2.
 \tag{I.35}
\]

Equations I.15, I.34, and I.35 prove I.5, and the definitions of
`mathfrak X` and `p^(plat)` prove I.6.  Since `a=pL`,

\[
 \Delta_a=\frac{\delta+\delta_0}{pL-\delta_0}=O(L^{-1}),
 \qquad
 \frac{q(L)\sqrt{\Delta_a}}{L^2}
 =O\!\left(\frac{q(L)}{L^{5/2}}\right).
 \tag{I.36}
\]

Condition I.7 also implies `log q(L)=o(L^2)`.  Therefore

\[
 \frac1{L^2}\log\!\left(C_Ia^{2/3}q(L)^7\right)\to0,
 \qquad
 \frac{\Phi_a}{L^2}\to0,
 \qquad
 \frac1{L^2}\log\omega^{1/3}=-\frac2{11907},
 \tag{I.37}
\]

which proves I.8.  In particular, the former `exp(Cq)` barrier at
`q` comparable with `L^2` is not intrinsic to the full plateau in this
exact-shear class.

## 8. Sharpness, source status, and open boundary

For `N>=2` and `N^(-2)<=Delta<=1`, Zhang's Proposition 8.4 proves that
the scale `exp(Theta(N sqrt Delta))` is unavoidable, up to polynomial
factors, in the full class `T_N`.  It makes no lower-bound assertion from
that proposition when `0<=Delta<N^(-2)`, where the exponent is only
`O(1)`.  Its
lower witnesses are confluent complex Fourier sums.  They are not, as
stated, mean-zero real conjugate-paired dyadic heat shears.  Therefore that
literature lower bound does not prove sharpness of I.5 inside I.2.

The scalar field I.3 satisfies

\[
 \partial_tF+B\partial_2F-\partial_2^2F=0
 \tag{I.38}
\]

and embeds in the smooth unforced shear `u=(0,B,F(t,x_2))` with constant
pressure.  When `B!=0`, the constant background has not been shown to lie
in the frozen mean-zero, inversion-paired Version-M subclass.

**LITERATURE:** Zhang Proposition 4.2 and its explicit constant; Erdelyi
journal Theorems 2.3 and 2.20; and the Kós `E_N^+` endpoint inequality
recorded as Erdelyi equation (1.2).  Erdelyi equation (1.5) records the
stronger `pi N/2` extension, but the proof keeps the sufficient `2N`
constant.

**PROVED LOCALLY:** the bilateral rescaling I.18; full-plateau geometry
I.15; polynomial spatial derivative and terminal payments I.21 and I.24;
the four-row reconstruction I.28--I.34; physical conversion I.35; and the
conditional implication I.5--I.8.

**FINITE COMPUTATION:** a certificate may check constants, interval maps,
mode counts, powers, rates, source hashes, and claim boundaries.  It is not
the continuum proof and cannot certify the imported 34-page preprint.

**OPEN:** an independent proof of the imported extrapolation theorem;
sharp polynomial dependence in I.5; a matching lower bound within I.2;
multiple dyadic bands; nonconstant shear; arbitrary nonlinear packets;
arbitrary-field E.24; complete Version-M extraction; fixed deletion;
suitable-weak transfer; regularity; and singularity.

No simulation or formal scientific figure is claimed.  No novelty,
priority, or Clay implication is claimed.  **NOT CLAY.**
