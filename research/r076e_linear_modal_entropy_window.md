# R0.76E -- linear modal-entropy window for exact shears

## 0. Result and exact boundary

R0.76D counted the stable heat tail from time one and obtained the safe loss
`exp(Cq log(q+1))`.  That count ignores the full observed mass before the
tail becomes monotone.  The present note delays the tail split until
`S_N` of order `N log(N+1)`.  Holder pays the finite early interval; only the
already decaying part uses Turan--Nazarov.  This removes the factorial loss.

Fix

\[
 q\in\mathbb N,\quad q\ge1,\qquad
 1\le n_1<\cdots<n_q\le2n_1,
 \quad n_j\in\mathbb N,
 \quad A_j\ge0,\quad \phi_j,B\in\mathbb R,
 \tag{E.1}
\]

and let

\[
 F(t,x_2)=\sum_{j=1}^q A_j e^{-n_j^2t}
 \cos\bigl(n_jx_2-\phi_j-n_jBt\bigr).
 \tag{E.2}
\]

Retain R0.76D's frozen cutoff `eta_R`, collar profile `xi_{a,R}`, and plateau
tube `S_{a,R}^{plat}`, and define

\[
 \begin{aligned}
 \mathcal T_{\boldsymbol n,R}
 &:=\frac12\int_0^{4R^2}\!\int_{\mathbb T^3}
 \eta_R(t)B\,\partial_2\xi_{a,R}|F|^2\,dxdt,\\
 M_{\boldsymbol n,R}^{\rm plat}
 &:=\int_0^{4R^2}\!\int_{\mathcal S_{a,R}^{\rm plat}}
 |F|^3\,dxdt.
 \end{aligned}
\]

There are frozen constants `C_*<infinity` and `L_*<infinity`, independent
of `q`, `R`, the frequencies, amplitudes, phases, and `B`, such that every
frozen `L>=L_*` satisfies

\[
 \boxed{
 |\mathcal T_{\boldsymbol n,R}|
 \le e^{C_*q}a^{2/3}R^{-1/3}
 \bigl(M_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{E.3}
\]

Consequently, with

\[
 p_{\boldsymbol n,R}^{\rm plat}
 :=R^{-2}\omega M_{\boldsymbol n,R}^{\rm plat},
 \qquad
 \mathfrak X_{\boldsymbol n,R}
 :=\frac\omega R[\mathcal T_{\boldsymbol n,R}]_+,
\]

E.3 implies

\[
 \boxed{
 \mathfrak X_{\boldsymbol n,R}
 \le e^{C_*q}a^{2/3}\omega^{1/3}
 \bigl(p_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{E.4}
\]

Consequently every integer-valued mode count satisfying

\[
 q(L)=o(L^2)
 \tag{E.5}
\]

retains the strict frozen rate

\[
 \boxed{
 \limsup_{L\to\infty}\frac1{L^2}
 \log\!\left[e^{C_*q(L)}a^{2/3}\omega^{1/3}\right]
 =-\frac2{11907}.}
 \tag{E.6}
\]

The result remains confined to the exact real constant-shear family in one
dyadic band.  It is not uniform in `q` and is not an arbitrary-packet
estimate.

## 1. Frozen scale and inherited spatial row

Retain

\[
 a=pL,\qquad R=e^{-\rho L^2/4},\qquad
 \omega=e^{-c_\gamma L^2/4},\qquad
 s=t/R^2,\qquad z=x_2/(aR).
 \tag{E.7}
\]

Put

\[
 \begin{aligned}
 G(s,z)&=F(R^2s,aRz),\\
 h(s)&=\int_I|G(s,z)|^3dz,
 \qquad H=\int_0^4h(s)ds,\qquad I=[-1/2,1/2],\\
 \kappa_j&=n_jaR,\qquad \alpha=\kappa_1,
 \qquad v=BR/a,\qquad \lambda=(\alpha/a)^2=(n_1R)^2.
 \end{aligned}
 \tag{E.8}
\]

Then

\[
 G_s+vG_z-a^{-2}G_{zz}=0,\qquad
 \alpha=\kappa_1<\cdots<\kappa_q\le2\alpha.
 \tag{E.9}
\]

R0.76D's quantitative spatial observation supplies an absolute `D>1`:

\[
 \boxed{
 \|G(s)\|_{L^\infty(J)}
 +(\alpha+q)^{-1}\|G_z(s)\|_{L^\infty(J)}
 \le D^{2q}h(s)^{1/3},
 \qquad J=[-3/2,3/2].}
 \tag{E.10}
\]

The factor `D^(2q)` is retained.  R0.76E improves only the previous
factorial heat-tail count.

## 2. Delayed stable heat clock

Let

\[
 Q(\tau)=\sum_{r=1}^{N}c_re^{\mu_r\tau},
 \qquad N\ge1,\qquad
 -4\le\operatorname {Re}\mu_r\le-1.
 \tag{E.11}
\]

For a measurable family in `z in I`, with every `z`-fibre satisfying E.11,
define

\[
 k(\tau)=\int_I|Q(\tau;z)|^3dz,
 \qquad K_U:=\int_0^Uk(\tau)d\tau\quad(U>0),
 \qquad T\ge4.
 \tag{E.12}
\]

The centered Turan--Nazarov estimate proved in R0.76D gives, for `tau>=1`,

\[
 |Q(\tau;z)|^3
 \le D_0^{3N}(1+\tau)^{3(N-1)}e^{-3\tau}
 \int_0^1|Q(r;z)|^3dr.
 \tag{E.13}
\]

After integration in `z` and raising to the power `2/3`, with
`m=2(N-1)`,

\[
 k(\tau)^{2/3}
 \le D_0^{2N}(1+\tau)^me^{-2\tau}K_1^{2/3}.
 \tag{E.14}
\]

Choose one absolute `C_0` sufficiently large and set

\[
 S_N=C_0N\log(N+1),
 \qquad
 S_N\ge\max\{4,m+1\},
 \qquad
 D_0^{2N}2^mS_N^{m+1}e^{-2S_N}\le1.
 \tag{E.15}
\]

To see that one choice works for every `N`, note that

\[
 \log S_N
 \le\left(2+\frac{\log C_0}{\log2}\right)\log(N+1),
 \qquad m+1=2N-1\le2N.
\]

Hence the logarithm of the last expression in E.15 is at most

\[
 N\log(N+1)
 \left[
 \frac{2\log D_0}{\log2}+2
 +2\left(2+\frac{\log C_0}{\log2}\right)-2C_0
 \right].
\]

The bracket is nonpositive once the absolute `C_0` is sufficiently large,
because its only nonlinear positive term is logarithmic in `C_0`.  Enlarging
the same `C_0` also gives `S_N>=max{4,m+1}`.

On the early interval, Holder gives directly

\[
 \begin{aligned}
 \int_0^{\min\{T,S_N\}}\tau k(\tau)^{2/3}d\tau
 &\le K_T^{2/3}
 \left(\int_0^{S_N}\tau^3d\tau\right)^{1/3}\\
 &=4^{-1/3}S_N^{4/3}K_T^{2/3}.
 \end{aligned}
 \tag{E.16}
\]

For the late interval, E.14, `K_1<=K_T`, and monotonicity of
`tau^(m+1)e^(-tau)` on `[S_N,infinity)` give

\[
 \begin{aligned}
 D_0^{2N}\int_{S_N}^\infty
 \tau(1+\tau)^me^{-2\tau}d\tau
 &\le D_0^{2N}2^m\int_{S_N}^\infty
 \tau^{m+1}e^{-2\tau}d\tau\\
 &\le D_0^{2N}2^mS_N^{m+1}e^{-2S_N}\le1.
 \end{aligned}
 \tag{E.17}
\]

Combining E.16--E.17 proves the improved weighted estimate

\[
 \boxed{
 \int_0^T\tau k(\tau)^{2/3}d\tau
 \le C\,[N\log(N+1)]^{4/3}K_T^{2/3}.}
 \tag{E.18}
\]

This is polynomial rather than `exp(CN log(N+1))`.

## 3. Endpoint estimate without a factorial

A fixed-unit Turan--Nazarov argument supplies an absolute `D_1>1`.  For
every `T>=1`, a half-measure Chebyshev subset of `[T-1,T]` gives

\[
 |Q(T;z)|^3
 \le D_1^{3N}\int_{T-1}^T|Q(r;z)|^3dr.
 \tag{E.19}
\]

The interval length is one, so the real-part factor is absorbed in `D_1`.
After integration in `z`, if `4<=T<=S_N`,

\[
 k(T)^{2/3}
 \le D_1^{2N}S_N^{2/3}T^{-2/3}K_T^{2/3}
 \le e^{CN}T^{-2/3}K_T^{2/3}.
 \tag{E.20}
\]

If `T>=S_N`, E.14 and E.15 imply

\[
 \begin{aligned}
 T^{2/3}k(T)^{2/3}
 &\le D_0^{2N}T^{2/3}(1+T)^me^{-2T}K_T^{2/3}\\
 &\le D_0^{2N}2^mS_N^{m+2/3}e^{-2S_N}K_T^{2/3}
 \le K_T^{2/3}.
 \end{aligned}
 \tag{E.21}
\]

Here `T^(m+2/3)e^(-2T)` decreases for `T>=S_N`, and the last inequality
uses `S_N>=1` and the stronger power `m+1` in E.15.  Thus, for every `T>=4`,

\[
 \boxed{
 k(T)^{2/3}\le e^{CN}T^{-2/3}K_T^{2/3}.}
 \tag{E.22}
\]

The weighted and endpoint bounds use the full `K_T`.  The factorial in
R0.76D resulted from replacing that full mass by `K_1` over the entire tail.

## 4. Two carrier branches

If `lambda<=1`, the original `s`-clock and a fixed-interval
Turan--Nazarov estimate give

\[
 h(4)^{2/3}\le e^{Cq}H^{2/3}.
 \tag{E.23}
\]

If `lambda>1`, set

\[
 \tau=\lambda s,\qquad T=4\lambda,\qquad
 \widetilde G(\tau,z)=G(\tau/\lambda,z),\qquad
 K_T=\lambda H.
 \tag{E.24}
\]

The time exponents have real parts in `[-4,-1]` and their number is at most
`2q`.  Applying E.22 gives

\[
 h(4)^{2/3}
 \le e^{Cq}(4\lambda)^{-2/3}(\lambda H)^{2/3}
 \le e^{Cq}H^{2/3}.
 \tag{E.25}
\]

Define `zeta(s):=eta_R(R^2s)`.  The frozen cutoff satisfies

\[
 0\le\zeta\le1,
 \qquad \zeta(0)=0,
 \qquad |\zeta'|\le C_\eta,
 \qquad 0\le\zeta(s)\le C_\eta s.
 \tag{E.26}
\]

Using E.18 with `N<=2q` yields the sharper onset payment

\[
 \begin{aligned}
 \lambda\int_0^4\zeta(s)h(s)^{2/3}ds
 &\le\frac{C_\eta}{\lambda}
 \int_0^{4\lambda}\tau k(\tau)^{2/3}d\tau\\
 &\le C[q\log(q+1)]^{4/3}
 \lambda^{-1/3}H^{2/3}.
 \end{aligned}
 \tag{E.27}
\]

No positive power of `lambda` remains.

## 5. Complete-real energy payment

For the frozen profile retain

\[
 W_a(z)=-2\pi az\vartheta(a(|z|-1)),\qquad
 \Xi_a(z)=\int_{-\infty}^zW_a(r)dr,\qquad
 \|\Xi_a\|_1+\|\Xi_a\|_\infty\le C,\quad
 \|\Xi_a''\|_1\le Ca.
 \tag{E.28}
\]

With `E(s)=int Xi_aG^2`, the exact identity for the complete real square is

\[
 \begin{aligned}
 v\int_0^4\zeta\int W_aG^2
 &=\zeta(4)E(4)-\int_0^4\zeta'E\,ds\\
 &\quad-a^{-2}\int_0^4\zeta\int\Xi_a''G^2
 +2a^{-2}\int_0^4\zeta\int\Xi_a|G_z|^2.
 \end{aligned}
 \tag{E.29}
\]

Equation E.10 gives

\[
 \begin{aligned}
 |E(s)|+a^{-2}\left|\int\Xi_a''G^2\right|
 &\le D^{4q}h(s)^{2/3},\\
 a^{-2}\int|\Xi_a||G_z|^2
 &\le D^{4q}\left(\lambda+\frac{q^2}{a^2}\right)h(s)^{2/3}.
 \end{aligned}
 \tag{E.30}
\]

For `lambda<=1`, Holder and E.23 pay every row.  For `lambda>1`, E.25
pays the terminal row and E.27 pays the `lambda` part of the gradient row.
Since `a>=1`, the remaining `q^2/a^2` part costs at most `q^2`.  The factors
`D^(4q)`, `e^(Cq)`, `q^2`, and `[q log(q+1)]^(4/3)` are all absorbed by one
`e^(C_*q)`.  Therefore

\[
 \boxed{
 \left|v\int_0^4\zeta\int W_aG^2\right|
 \le e^{C_*q}H^{2/3}.}
 \tag{E.31}
\]

No density projection, localized-current sign, spectral-gap division, or
standalone carrier integration by parts is used.

## 6. Physical scale and asymptotic window

The exact physical conversion is

\[
 \mathcal T_{\boldsymbol n,R}
 =\frac{a^2R^3}{2}v\int_0^4\zeta\int W_aG^2,
 \qquad
 M_{\boldsymbol n,R}^{\rm plat}
 \ge4\pi\delta_0a^2R^5H.
 \tag{E.32}
\]

Equations E.31--E.32 prove E.3; normalization proves E.4.  Finally,

\[
 \frac{C_*q(L)}{L^2}\longrightarrow0,
 \qquad
 \frac1{L^2}\log a^{2/3}\longrightarrow0,
 \qquad
 \frac1{L^2}\log\omega^{1/3}=-\frac2{11907},
 \tag{E.33}
\]

so E.5 proves E.6.

## 7. Exact-solution and open boundary

The scalar field still satisfies

\[
 \partial_tF+B\partial_2F-\partial_2^2F=0
 \tag{E.34}
\]

and embeds in the smooth unforced shear `u=(0,B,F(t,x_2))` with constant
pressure.  When `B\ne0`, the constant background has not been shown to
belong to the frozen mean-zero, inversion-paired Version-M subclass.

If the complete clock and plateau tube belong to the same scale-`2R`
Version-M measurement row with weight at least `omega`, and `F` is an actual
component of that same velocity, E.4 gives the corresponding conditional
consequence.  It does not apply to a Fourier projection of a larger field.

**Closed here:** the factorial heat-tail loss in R0.76D; an `exp(Cq)`
complete signed-flux constant; and the exact-shear window `q(L)=o(L^2)`.

**Still open:** sharp dependence on `q`; a matching lower bound; removal of
the exponential spatial-observation loss; mode counts comparable with
`L^2` or larger; arbitrary packets; nonconstant shear; arbitrary-field E.24;
complete Version-M extraction; fixed deletion; suitable-weak transfer;
regularity; and singularity.

R0.75R concerns an arbitrary growing packet with exponentially many active
modes on a different short clock.  It lies far outside E.5 and is not
contradicted.  The proof is analytic.  Finite fixtures may audit the delayed
split and exponent ledgers but are not proof of Turan--Nazarov, Erdelyi, or
the continuum flux theorem.  No simulation or formal scientific figure is
claimed.  No novelty, priority, or sharpness claim is made.  **NOT CLAY.**
