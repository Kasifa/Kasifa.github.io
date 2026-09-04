# R0.76D -- quantitative growing-mode entropy window for exact shears

## 0. Result and exact boundary

R0.76C closes every carrier frequency for each fixed finite real harmonic
family, but leaves the dependence of its constant on the number of modes
unquantified.  The present note replaces the compactness derivative step by
an explicit Bernstein-type inequality and counts the polynomial heat tail.
The resulting loss is at most exponential in the modal entropy
`q log(q+1)`.

Let `q>=1` be an integer and

\[
 n_1,\ldots,n_q\in\mathbb N,
 \qquad 1\le n_1<n_2<\cdots<n_q\le2n_1.
 \tag{D.1}
\]

For

\[
 F(t,x_2)=\sum_{j=1}^q A_j e^{-n_j^2t}
 \cos\bigl(n_jx_2-\phi_j-n_jBt\bigr),
 \qquad A_j\ge0,\quad \phi_j\in\mathbb R,
 \quad B\in\mathbb R,
 \tag{D.2}
\]

define the complete-clock collar flux and plateau cubic mass by

\[
 \begin{aligned}
 \mathcal T_{\boldsymbol n,R}
 &:=\frac12\int_0^{4R^2}\!\int_{\mathbb T^3}
 \eta_R(t)B\,\partial_2\xi_{a,R}|F|^2\,dxdt,\\
 M_{\boldsymbol n,R}^{\rm plat}
 &:=\int_0^{4R^2}\!\int_{\mathcal S_{a,R}^{\rm plat}}
 |F|^3\,dxdt.
 \end{aligned}
 \tag{D.3}
\]

There are frozen constants `C_*<infinity` and `L_*<infinity`, independent of
`q`, `R`, the frequencies, amplitudes, phases, and `B`, such that for every
frozen `L>=L_*`,

\[
 \boxed{
 |\mathcal T_{\boldsymbol n,R}|
 \le \exp\!\bigl(C_*q\log(q+1)\bigr)
 a^{2/3}R^{-1/3}
 \bigl(M_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{D.4}
\]

With

\[
 p_{\boldsymbol n,R}^{\rm plat}
 =R^{-2}\omega M_{\boldsymbol n,R}^{\rm plat},
 \qquad
 \mathfrak X_{\boldsymbol n,R}
 =\frac\omega R[\mathcal T_{\boldsymbol n,R}]_+,
 \tag{D.5}
\]

this becomes

\[
 \boxed{
 \mathfrak X_{\boldsymbol n,R}
 \le \exp\!\bigl(C_*q\log(q+1)\bigr)
 a^{2/3}\omega^{1/3}
 \bigl(p_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{D.6}
\]

Consequently, for every integer-valued mode count `q=q(L)` satisfying

\[
 q(L)\log(q(L)+1)=o(L^2),
 \tag{D.7}
\]

the complete coefficient retains the strict frozen rate

\[
 \boxed{
 \limsup_{L\to\infty}\frac1{L^2}
 \log\!\left[
 e^{C_*q(L)\log(q(L)+1)}a^{2/3}\omega^{1/3}
 \right]
 =-\frac2{11907}.}
 \tag{D.8}
\]

The estimate is not uniform over arbitrary packets.  It gives a quantitative
growing-mode window only for the exact constant-shear family D.2 in one
dyadic band.

## 1. Frozen scaling

Retain

\[
 a=pL,\qquad R=e^{-\rho L^2/4},\qquad
 \omega=e^{-c_\gamma L^2/4},\qquad
 0\le\eta_R\le1,\qquad \eta_R(0)=0,
 \qquad |\eta_R'|\le C_\eta R^{-2}.
 \tag{D.9}
\]

Set

\[
 s=t/R^2,\qquad z=x_2/(aR),\qquad
 \kappa_j=n_jaR,\qquad \alpha=\kappa_1,
 \qquad v=BR/a,
 \tag{D.10}
\]

and

\[
 \begin{aligned}
 G(s,z)&=F(R^2s,aRz),\\
 G_s+vG_z-a^{-2}G_{zz}&=0,\\
 h(s)&=\int_I|G(s,z)|^3dz,
 \qquad H=\int_0^4h(s)ds,
 \qquad I=[-1/2,1/2].
 \end{aligned}
 \tag{D.11}
\]

The dyadic band is

\[
 \alpha=\kappa_1<\cdots<\kappa_q\le2\alpha.
 \tag{D.12}
\]

Write

\[
 J=[-3/2,3/2],\qquad J^+=[-2,2],
 \qquad \lambda=(\alpha/a)^2=(n_1R)^2.
 \tag{D.13}
\]

## 2. Quantitative spatial observation

**Lemma D.1.**  There is an absolute `D>1` such that every exponential sum

\[
 g(z)=\sum_{r=1}^{N}c_re^{i\nu_rz},
 \qquad N\le2q,\qquad |\nu_r|\le2\alpha,
 \tag{D.14}
\]

satisfies

\[
 \boxed{
 \|g\|_{L^\infty(J)}
 +(\alpha+q)^{-1}\|g'\|_{L^\infty(J)}
 \le D^{2q}\|g\|_{L^3(I)}.}
 \tag{D.15}
\]

Repeated exponents are first combined; zero coefficients are deleted.  Thus
the active frequencies may be ordered strictly before applying the external
derivative theorem.

Let `h_g=int_I|g|^3` and choose

\[
 E=\{z\in I:|g(z)|^3\le2h_g\},
 \qquad |E|\ge\frac12.
 \tag{D.16}
\]

The spatial exponents are purely imaginary.  Turan--Nazarov on `J^+`, whose
length is four, gives

\[
 \|g\|_{L^\infty(J^+)}
 \le (8A)^{N-1}(2h_g)^{1/3}
 \le D^{2q}h_g^{1/3},
 \tag{D.17}
\]

where `A` is the absolute Turan--Nazarov constant.  There is no dependence on
the size or separation of the imaginary frequencies.

For `z_0 in J`, define `f(t)=g(z_0+t/2)` on `[-1,1]`.  Its at most `N`
frequencies have absolute value at most `alpha`.  The explicit
Bernstein-type inequality for pure-imaginary exponential sums gives

\[
 |f'(0)|\le\bigl(\alpha+2e(N+1)\bigr)
 \|f\|_{L^\infty([-1,1])}.
 \tag{D.18}
\]

Since `f'(0)=g'(z_0)/2`, its observation interval is contained in `J^+`, and
`N<=2q`, D.17--D.18 prove D.15.  In particular, at every fixed time,

\[
 \boxed{
 \|G(s)\|_{L^\infty(J)}\le D^{2q}h(s)^{1/3},
 \qquad
 \|G_z(s)\|_{L^\infty(J)}
 \le D^{2q}(\alpha+q)h(s)^{1/3}.}
 \tag{D.19}
\]

This makes the formerly compactness-only derivative constant explicit.

## 3. Quantitative stable heat-clock lemma

**Lemma D.2.**  Let

\[
 Q(\tau)=\sum_{r=1}^{N}c_re^{\mu_r\tau},
 \qquad N\le2q,
 \qquad -4\le\operatorname {Re}\mu_r\le-1.
 \tag{D.20}
\]

There is an absolute `C` such that, for `tau>=1`,

\[
 |Q(\tau)|^3
 \le D^{3N}(1+\tau)^{3(N-1)}e^{-3\tau}
 \int_0^1|Q(r)|^3dr.
 \tag{D.21}
\]

For a measurable family `Q(tau;z)` on `z in I`, with every `Q(.;z)`
satisfying D.20, put

\[
 k(\tau)=\int_I|Q(\tau;z)|^3dz,
 \qquad K_T=\int_0^Tk(\tau)d\tau,
 \qquad T\ge4.
 \tag{D.22}
\]

Then

\[
 \boxed{
 \begin{aligned}
 \int_0^T\tau k(\tau)^{2/3}d\tau
 &\le \exp\!\bigl(CN\log(N+1)\bigr)K_T^{2/3},\\
 k(T)^{2/3}
 &\le \exp\!\bigl(CN\log(N+1)\bigr)
 T^{-2/3}K_T^{2/3}.
 \end{aligned}}
 \tag{D.23}
\]

The centering `Y=exp(5tau/2)Q` and the half-measure subset of `[0,1]`
give D.21 exactly as in R0.76C, now retaining the term count.

After integration in `z`, raise D.21 to the power `2/3`.  With
`m=2(N-1)`, the tail constant is bounded by

\[
 \begin{aligned}
 \int_1^\infty\tau(1+\tau)^me^{-2\tau}d\tau
 &\le2^m\int_1^\infty\tau^{m+1}e^{-2\tau}d\tau\\
 &\le\frac{(m+1)!}{4}
 \le\exp\!\bigl(CN\log(N+1)\bigr).
 \end{aligned}
 \tag{D.24}
\]

Holder controls `[0,1]`.  For the endpoint, with `r=m+2/3`,

\[
 T^{2/3}(1+T)^me^{-2T}
 \le\left(\frac54\right)^mT^{m+2/3}e^{-2T},
 \qquad
 \sup_{T\ge4}T^{m+2/3}e^{-2T}
 \le2^{-r}(r/e)^r,
 \tag{D.25}
\]

and hence

\[
 \sup_{T\ge4}T^{2/3}(1+T)^me^{-2T}
 \le\exp\!\bigl(CN\log(N+1)\bigr).
 \tag{D.26}
\]

These two estimates prove D.23.  Imaginary parts and exponent gaps never
enter.

## 4. Endpoint trace in the bounded heat branch

If `lambda<=1`, then at fixed `z` the original `s`-clock exponents of `G`
have real parts in `[-4,0]`.  On `[0,4]`, a half-measure Chebyshev subset and
Turan--Nazarov give

\[
 h(4)\le D^{6q}H,
 \qquad
 h(4)^{2/3}\le D^{4q}H^{2/3}.
 \tag{D.27}
\]

This estimate is independent of `v` and all frequency gaps.

If `lambda>1`, use the heat clock

\[
 \tau=\lambda s,\qquad T=4\lambda,
 \qquad \widetilde G(\tau,z)=G(\tau/\lambda,z).
 \tag{D.28}
\]

Its exponents are

\[
 -\frac{\kappa_j^2}{\alpha^2}
 \pm i\frac{\kappa_jv}{\lambda},
 \qquad -4\le\operatorname {Re}\mu_{j,\pm}\le-1,
 \tag{D.29}
\]

and `K_T=lambda H`.  Lemma D.2 yields

\[
 \boxed{
 h(4)^{2/3}
 \le \exp\!\bigl(Cq\log(q+1)\bigr)H^{2/3}.}
 \tag{D.30}
\]

Thus D.27 and D.30 give one quantitative endpoint trace for every carrier.

## 5. Quantitative complete-real energy payment

For the frozen radial profile retain

\[
 W_a(z)=-2\pi az\vartheta(a(|z|-1)),
 \qquad \Xi_a(z)=\int_{-\infty}^zW_a(r)dr,
 \tag{D.31}
\]

and, for `L>=L_*`,

\[
 \operatorname {supp}\Xi_a\subset J,
 \qquad
 \|\Xi_a\|_1+\|\Xi_a\|_\infty\le C,
 \qquad \|\Xi_a''\|_1\le Ca,
 \qquad a\ge1.
 \tag{D.32}
\]

With `zeta(s)=eta_R(R^2s)` and `E(s)=int Xi_aG^2`, the exact real-square
identity is

\[
 \begin{aligned}
 v\int_0^4\zeta\int W_aG^2
 &=\zeta(4)E(4)-\int_0^4\zeta'E\,ds\\
 &\quad-a^{-2}\int_0^4\zeta\int\Xi_a''G^2
 +2a^{-2}\int_0^4\zeta\int\Xi_a|G_z|^2.
 \end{aligned}
 \tag{D.33}
\]

The value row in D.19 and D.32 give

\[
 |E(s)|+a^{-2}\left|\int\Xi_a''G^2\right|
 \le D^{4q}h(s)^{2/3}.
 \tag{D.34}
\]

The explicit derivative row gives

\[
 a^{-2}\int|\Xi_a||G_z|^2
 \le D^{4q}\left(\lambda+\frac{q^2}{a^2}\right)h(s)^{2/3}.
 \tag{D.35}
\]

When `lambda<=1`, Holder on `[0,4]`, D.27, and `a>=1` pay every row by
`exp(Cq log(q+1))H^(2/3)`.

When `lambda>1`, the onset bound

\[
 0\le\zeta(s)\le C_\eta s
 \tag{D.36}
\]

and Lemma D.2 give

\[
 \begin{aligned}
 \lambda\int_0^4\zeta(s)h(s)^{2/3}ds
 &\le\frac{C_\eta}{\lambda}
 \int_0^{4\lambda}\tau k(\tau)^{2/3}d\tau\\
 &\le\exp\!\bigl(Cq\log(q+1)\bigr)
 \lambda^{-1/3}H^{2/3}.
 \end{aligned}
 \tag{D.37}
\]

The remaining `q^2/a^2` part of D.35 is bounded by
`q^2H^(2/3)` using Holder, and that polynomial factor is absorbed by the same
modal-entropy exponential.  Equation D.30 pays the endpoint.  Consequently,
in both branches,

\[
 \boxed{
 \left|v\int_0^4\zeta\int W_aG^2\right|
 \le\exp\!\bigl(C_*q\log(q+1)\bigr)H^{2/3}.}
 \tag{D.38}
\]

The identity is formed for the complete real square before absolute values.
No analytic-density split, localized-current sign, spectral separation, or
standalone carrier integration by parts is used.

## 6. Physical scales and growing-mode consequence

The exact cross section and plateau fibre are

\[
 \mathcal T_{\boldsymbol n,R}
 =\frac{a^2R^3}{2}v\int_0^4\zeta\int W_aG^2,
 \qquad
 M_{\boldsymbol n,R}^{\rm plat}
 \ge4\pi\delta_0a^2R^5H.
 \tag{D.39}
\]

Combining D.38 and D.39 proves D.4.  Multiplication by `omega/R` and
substitution of D.5 prove D.6.

Since

\[
 \frac1{L^2}\log a^{2/3}\longrightarrow0,
 \qquad
 \frac1{L^2}\log\omega^{1/3}=-\frac2{11907},
 \tag{D.40}
\]

D.7 and D.40 prove D.8.  The growing-mode statement is therefore an asymptotic
corollary of the explicit constant ledger, not a uniform-in-`q` estimate.

## 7. Exact-solution and Version-M boundary

The scalar field satisfies

\[
 \partial_tF+B\partial_2F-\partial_2^2F=0
 \tag{D.41}
\]

and embeds in the exact smooth unforced shear `u=(0,B,F(t,x_2))` with
constant pressure.  The nonzero constant background has not been shown to
belong to the frozen mean-zero, inversion-paired Version-M subclass.

If the complete clock and plateau tube belong to the same scale-`2R`
Version-M measurement row with weight at least `omega`, and `F` is an actual
component of that same velocity, D.6 gives the corresponding conditional
modal-entropy-weighted consequence.  It cannot be applied merely to a
Fourier projection of a larger solution.

## 8. What is closed and what remains open

**Closed here:** an explicit `exp(Cq log(q+1))` upper bound for the complete
signed collar-flux constant of every finite exact real dyadic shear family;
the growing-mode window D.7; arbitrary carrier frequency, phase, amplitude,
constant speed, and frequency collision within that family.

**Not closed:** a matching lower bound or sharp `q` dependence; the removal
of the modal-entropy loss; mode counts outside D.7 on the frozen scale;
arbitrary packets; nonconstant or vertically dependent shear; projection
from a larger velocity; arbitrary-field E.24; complete Version-M extraction;
fixed deletion; suitable-weak transfer; regularity; and singularity.

R0.75R already rules out a `q`-uniform plateau-only conclusion for arbitrary
growing packets.  D.4 is consistent with that obstruction because its
constant grows with `q`.  The proof is analytic.  Finite fixtures may audit
the factorial and scale ledgers but are not proof of either imported
exponential-sum inequality.  No formal scientific figure or simulation is
claimed.  The source screen makes no completeness, novelty, or priority
claim.  **NOT CLAY.**
