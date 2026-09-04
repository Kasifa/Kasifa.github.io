# R0.76C -- full-frequency signed-flux payment for every fixed finite harmonic family

## 0. Result and exact boundary

R0.76B pays every fixed finite real dyadic shear through the inverse-radius
carrier scale `n_1R<=1`.  Above that scale the spatial derivative row appears
to lose `(n_1R)^2`, but the frozen cutoff vanishes at the initial time.  The
present note combines that onset with the fast heat decay of the ultra-high
carrier and removes the carrier restriction completely.

Fix an integer `q>=1` and

\[
 n_1,\ldots,n_q\in\mathbb N,
 \qquad 1\le n_1<n_2<\cdots<n_q\le2n_1.
 \tag{C.1}
\]

Let

\[
 F(t,x_2)=\sum_{j=1}^q A_j e^{-n_j^2t}
 \cos\bigl(n_jx_2-\phi_j-n_jBt\bigr),
 \qquad A_j\ge0,\qquad \phi_j\in\mathbb R,
 \qquad B\in\mathbb R.
 \tag{C.2}
\]

For the frozen collar, plateau, and complete-clock cutoff, set

\[
 \begin{aligned}
 \mathcal T_{\boldsymbol n,R}
 &:=\frac12\int_0^{4R^2}\!\int_{\mathbb T^3}
 \eta_R(t)B\,\partial_2\xi_{a,R}|F|^2\,dxdt,\\
 M_{\boldsymbol n,R}^{\rm plat}
 &:=\int_0^{4R^2}\!\int_{\mathcal S_{a,R}^{\rm plat}}
 |F|^3\,dxdt.
 \end{aligned}
 \tag{C.3}
\]

For every fixed `q` and all sufficiently large frozen `L`, there is `C_q`,
depending on `q` and the frozen profiles but not on `R`, the frequencies,
amplitudes, phases, or `B`, such that, with no carrier upper bound,

\[
 \boxed{
 |\mathcal T_{\boldsymbol n,R}|
 \le C_q a^{2/3}R^{-1/3}
 \bigl(M_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{C.4}
\]

Define

\[
 p_{\boldsymbol n,R}^{\rm plat}
 =R^{-2}\omega M_{\boldsymbol n,R}^{\rm plat},
 \qquad
 \mathfrak X_{\boldsymbol n,R}
 =\frac\omega R[\mathcal T_{\boldsymbol n,R}]_+.
 \tag{C.5}
\]

Then

\[
 \boxed{
 \mathfrak X_{\boldsymbol n,R}
 \le C_q a^{2/3}\omega^{1/3}
 \bigl(p_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3},
 \qquad
 \lim_{L\to\infty}\frac1{L^2}
 \log(a^{2/3}\omega^{1/3})=-\frac2{11907}.}
 \tag{C.6}
\]

This is a full-frequency theorem only for each fixed finite `q` and for the
exact constant-shear family C.2.  It is not uniform for growing packets and is
not an arbitrary-field Navier--Stokes estimate.

## 1. Frozen inputs and ultra-high scaling

The directly used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | complete clock and onset `eta_R(0)=0` |
| `research/r075r_outer_cap_spectral_concentration_obstruction.md` | `e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3` | frozen radial geometry and growing-packet obstruction |
| `research/r075x_fixed_finite_mode_low_carrier_payment.md` | `8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763` | bounded scaled-carrier branch |
| `research/r076b_moderate_carrier_fixed_mode_flux_payment.md` | `a8a4cc853ec1029cb52afee724a4a783da156bd57de5399c58a7f42e2ab0306d` | inverse-radius branch and high-carrier spatial observation |

Retain

\[
 a=pL,\qquad R=e^{-\rho L^2/4},\qquad
 \omega=e^{-c_\gamma L^2/4},\qquad
 0\le\eta_R\le1,\qquad \eta_R(0)=0,
 \qquad |\eta_R'|\le C_\eta R^{-2}.
 \tag{C.7}
\]

Use the scaled variables

\[
 s=t/R^2,\qquad z=x_2/(aR),\qquad
 \kappa_j=n_jaR,\qquad \alpha=\kappa_1,
 \qquad v=BR/a,
 \tag{C.8}
\]

and define

\[
 G(s,z)=F(R^2s,aRz),\qquad
 G_s+vG_z-a^{-2}G_{zz}=0,
 \qquad
 h(s)=\int_{-1/2}^{1/2}|G(s,z)|^3dz,
 \qquad H=\int_0^4h(s)ds.
 \tag{C.9}
\]

R0.76B proves C.4 when `alpha<=a`.  It remains to assume

\[
 \lambda=\frac{\alpha^2}{a^2}=(n_1R)^2>1,
 \qquad
 \alpha=\kappa_1<\cdots<\kappa_q\le2\alpha.
 \tag{C.10}
\]

For all sufficiently large `L`, C.10 implies `alpha>8q`; hence the spatial
observation proved in R0.76B applies at every time:

\[
 \boxed{
 \|G(s)\|_{L^\infty(J)}
 +\alpha^{-1}\|G_z(s)\|_{L^\infty(J)}
 \le C_qh(s)^{1/3},
 \qquad J=[-3/2,3/2].}
 \tag{C.11}
\]

## 2. Stable exponential-polynomial clock lemma

**Lemma C.1.**  Fix `q`.  Let

\[
 Q(\tau)=\sum_{r=1}^{N}c_re^{\mu_r\tau},
 \qquad N\le2q,\qquad -4\le\operatorname {Re}\mu_r\le-1.
 \tag{C.12}
\]

There is `C_q`, independent of all imaginary parts and exponent gaps, such
that for every `tau>=1`,

\[
 \boxed{
 |Q(\tau)|^3
 \le C_q(1+\tau)^{3(2q-1)}e^{-3\tau}
 \int_0^1|Q(r)|^3dr.}
 \tag{C.13}
\]

For a measurable family `Q(tau;z)` on `z in I=[-1/2,1/2]`, with every
`Q(.;z)` an exponential polynomial satisfying C.12, put

\[
 k(\tau)=\int_I|Q(\tau;z)|^3dz,
 \qquad K_T=\int_0^Tk(\tau)d\tau,
 \qquad T\ge4.
 \tag{C.14}
\]

Then

\[
 \boxed{
 \int_0^T\tau k(\tau)^{2/3}d\tau
 \le C_qK_T^{2/3},
 \qquad
 k(T)^{2/3}\le C_qT^{-2/3}K_T^{2/3}.}
 \tag{C.15}
\]

To prove C.13, let `I_Q=int_0^1|Q|^3`.  If `I_Q=0`, analyticity makes the
claim immediate.  Otherwise

\[
 E=\{r\in[0,1]:|Q(r)|^3\le2I_Q\},
 \qquad |E|\ge\frac12.
 \tag{C.16}
\]

Define the centered exponential polynomial

\[
 Y(r)=e^{5r/2}Q(r).
 \tag{C.17}
\]

Its exponents have real parts in `[-3/2,3/2]`.  Turan--Nazarov on `[0,tau]`
with the subset E gives the interval factor
`(C tau/|E|)^(N-1)<=C_q(1+tau)^(2q-1)`, while
`sup_E|Y|<=e^(5/2)(2I_Q)^(1/3)`.  Hence

\[
 \begin{aligned}
 |Q(\tau)|
 &\le e^{-5\tau/2}\sup_{[0,\tau]}|Y|\\
 &\le C_q(1+\tau)^{2q-1}e^{-\tau}I_Q^{1/3},
 \end{aligned}
 \tag{C.18}
\]

because the theorem contributes at most `e^(3 tau/2)` from the shifted real
parts and a polynomial factor of degree at most `2q-1`.  This proves C.13.
After cubing and integrating in `z`,

\[
 k(\tau)
 \le C_q(1+\tau)^{3(2q-1)}e^{-3\tau}K_1
 \qquad(\tau\ge1).
 \tag{C.19}
\]

Holder's inequality on `[0,1]` and the integrable tail in C.19 yield

\[
 \int_0^1\tau k^{2/3}d\tau
 +\int_1^\infty\tau k^{2/3}d\tau
 \le C_qK_T^{2/3}.
 \tag{C.20}
\]

At `tau=T`, C.19 and `K_1<=K_T` give

\[
 k(T)^{2/3}
 \le C_qT^{2(2q-1)}e^{-2T}K_T^{2/3}
 \le C_qT^{-2/3}K_T^{2/3},
 \tag{C.21}
\]

since `T^(2(2q-1)+2/3)e^(-2T)` is bounded for `T>=4`.  This proves C.15.

## 3. Rescaled ultra-high clock

Set

\[
 \tau=\lambda s,\qquad T=4\lambda,\qquad
 \widetilde G(\tau,z)=G(\tau/\lambda,z).
 \tag{C.22}
\]

At fixed `z`, its at most `2q` temporal exponents are

\[
 \mu_{j,\pm}
 =-\frac{\kappa_j^2}{\alpha^2}
 \pm i\frac{\kappa_jv}{\lambda},
 \qquad -4\le\operatorname {Re}\mu_{j,\pm}\le-1.
 \tag{C.23}
\]

Thus Lemma C.1 applies with arbitrary `v` and arbitrary frequency gaps.  If
`k(tau)=int_I|widetilde G|^3`, then

\[
 K_T=\int_0^{4\lambda}k(\tau)d\tau=\lambda H.
 \tag{C.24}
\]

For `zeta(s)=eta_R(R^2s)`, the frozen onset and derivative bound imply

\[
 0\le\zeta(s)\le C_\eta s,
 \qquad 0\le s\le4.
 \tag{C.25}
\]

The apparently large gradient row is therefore paid with a gain:

\[
 \begin{aligned}
 \lambda\int_0^4\zeta(s)h(s)^{2/3}ds
 &\le\frac{C_\eta}{\lambda}
 \int_0^{4\lambda}\tau k(\tau)^{2/3}d\tau\\
 &\le C_q\lambda^{-1/3}H^{2/3}
 \le C_qH^{2/3}.
 \end{aligned}
 \tag{C.26}
\]

The terminal row also remains uniform.  Equations C.15 and C.24 give

\[
 h(4)^{2/3}=k(4\lambda)^{2/3}
 \le C_q(4\lambda)^{-2/3}(\lambda H)^{2/3}
 \le C_qH^{2/3}.
 \tag{C.27}
\]

Both uses would fail without retaining the heat decay.  The gradient payment
also uses `zeta(0)=0` essentially.

## 4. Full-real-field local energy identity

For the frozen radial profile retain

\[
 W_a(z)=-2\pi az\vartheta(a(|z|-1)),
 \qquad \Xi_a(z)=\int_{-\infty}^zW_a(r)dr,
 \qquad
 \|\Xi_a\|_1+\|\Xi_a\|_\infty\le C,
 \qquad \|\Xi_a''\|_1\le Ca.
 \tag{C.28}
\]

With `E(s)=int Xi_aG^2`, the exact real-square identity is

\[
 v\int W_aG^2
 =E'(s)-a^{-2}\int\Xi_a''G^2
 +2a^{-2}\int\Xi_a|G_z|^2.
 \tag{C.29}
\]

Since `zeta(0)=0`, its complete-clock form is

\[
 \begin{aligned}
 v\int_0^4\zeta\int W_aG^2
 &=\zeta(4)E(4)-\int_0^4\zeta'E\,ds\\
 &\quad-a^{-2}\int_0^4\zeta\int\Xi_a''G^2
 +2a^{-2}\int_0^4\zeta\int\Xi_a|G_z|^2.
 \end{aligned}
 \tag{C.30}
\]

The value part of C.11, the frozen kernel norms, and Holder on `[0,4]` give

\[
 \int_0^4|\zeta'E|ds
 +a^{-2}\int_0^4\zeta\left|\int\Xi_a''G^2\right|ds
 \le C_qH^{2/3}.
 \tag{C.31}
\]

The derivative part of C.11 gives
`a^(-2)int Xi_a|G_z|^2<=C_q lambda h^(2/3)`; C.26 pays its time integral.
Equation C.27 pays the terminal row.  Hence

\[
 \boxed{
 \left|v\int_0^4\zeta\int W_aG^2\right|
 \le C_qH^{2/3}.}
 \tag{C.32}
\]

As in R0.76B, the identity is formed for the complete real square before any
absolute value.  No density/carrier splitting, standalone oscillatory
integration by parts, or localized-current sign is used.

## 5. Return to physical scales

The exact cross section and plateau fibre give

\[
 \mathcal T_{\boldsymbol n,R}
 =\frac{a^2R^3}{2}v\int_0^4\zeta\int W_aG^2,
 \qquad
 M_{\boldsymbol n,R}^{\rm plat}
 \ge4\pi\delta_0a^2R^5H.
 \tag{C.33}
\]

Combining C.32 and C.33 yields

\[
 \begin{aligned}
 |\mathcal T_{\boldsymbol n,R}|
 &\le C_qa^2R^3H^{2/3}\\
 &\le C_qa^{2/3}R^{-1/3}
 \bigl(M_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3}.
 \end{aligned}
 \tag{C.34}
\]

This proves C.4 for the ultra-high branch.  R0.76B supplies the complementary
branch `alpha<=a`, so C.4 holds at every carrier.  Substitution of C.5 proves
C.6.

## 6. Exact-solution and Version-M boundary

The scalar field satisfies

\[
 \partial_tF+B\partial_2F-\partial_2^2F=0
 \tag{C.35}
\]

and embeds in the exact smooth unforced shear `u=(0,B,F(t,x_2))` with constant
pressure.  The nonzero constant background has not been shown to belong to
the frozen mean-zero, inversion-paired Version-M subclass.

If the complete clock and plateau tube belong to the same scale-`2R`
Version-M measurement row with weight at least `omega`, and `F` is an actual
component of that same velocity, C.6 gives the same conditional
`C_q(P_R^M)^(2/3)` consequence.  It cannot be applied merely to a Fourier
projection of a larger solution.

## 7. What is closed and what remains open

**Closed here:** for every fixed `q`, all carrier frequencies in the complete
signed collar-flux estimate for the exact real dyadic constant-shear family;
all coefficient cancellations and frequency collisions; arbitrary real
phases and constant speed; and the fixed-`q` normalized decay rate.

**Open:** a quantitative constant suitable for `q=q(L)`; arbitrary growing
packets; nonconstant or vertically dependent shear; projection from a larger
velocity; arbitrary-field E.24; complete Version-M extraction; fixed deletion;
suitable-weak transfer; regularity; and singularity.

The R0.75R outer-cap example still prevents promotion from fixed `q` to an
arbitrary packet.  The proof is analytic.  Finite fixtures may audit the time
rescaling, decay weights, endpoint powers, and one exact ultra-high family,
but they are not proof of the continuum exponential-polynomial lemma.  No
formal scientific figure or simulation is claimed.  The source screen makes
no completeness, novelty, or priority claim.  **NOT CLAY.**
