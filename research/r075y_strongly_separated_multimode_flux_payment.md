# R0.75Y -- complete flux payment for a strongly separated multimode shear

## 0. Result and exact boundary

R0.75X pays the low-carrier signed collar flux for every fixed finite
harmonic family, without a frequency-gap condition.  The high-carrier
sector for three or more modes remained open.  This note closes a
quantitatively separated part of that sector.

Fix an integer `q>=1`, let

\[
 1\le n_1<n_2<\cdots<n_q\le2n_1,
 \qquad
 \ell=aR,
 \tag{Y.1}
\]

and define the separation of the signed spectrum by

\[
 \delta_{\boldsymbol n}
 :=\min\!\left(
 \{2n_1\}\cup
 \{n_j-n_i:1\le i<j\le q\}
 \right).
 \tag{Y.2}
\]

For `q=1`, the second set in Y.2 is empty, so
`\delta_{\boldsymbol n}=2n_1`.  Assume

\[
 \boxed{\ell\delta_{\boldsymbol n}\ge8q.}
 \tag{Y.3}
\]

For `q>=2`, Y.1 and Y.3 imply
`n_1\ell>=8q(q-1)`.  Thus this is genuinely a high-carrier, increasingly
sparse class when `q` grows; it is not a dense-packet hypothesis in another
form.

Consider the exact real diffusive shear

\[
 \begin{aligned}
 F(t,x_2)
 &=\sum_{j=1}^q A_j(t)
   \cos\bigl(n_jx_2-\phi_j(t)\bigr),\\
 A_j(t)&=A_je^{-n_j^2t},\qquad
 \phi_j(t)=\phi_j+n_jBt,
 \end{aligned}
 \tag{Y.4}
\]

where `A_j>=0`, the phases are arbitrary, and `B` is any real constant.
With the frozen complete clock `T_R=4R^2`, put

\[
 \begin{aligned}
 \mathcal T_{\boldsymbol n,R}
 &:=\frac12\int_0^{T_R}\!\int_{\mathbb T^3}
 \eta_R(t)B\,\partial_2\xi_{a,R}|F|^2\,dxdt,\\
 M_{\boldsymbol n,R}^{\rm plat}
 &:=\int_0^{T_R}\!\int_{\mathcal S_{a,R}^{\rm plat}}
 |F|^3\,dxdt.
 \end{aligned}
 \tag{Y.5}
\]

Then

\[
 \boxed{
 |\mathcal T_{\boldsymbol n,R}|
 \le Cq^2a^{2/3}R^{-1/3}
 \bigl(M_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{Y.6}
\]

Here `C` depends only on the frozen radial profile, plateau width, and time
cutoff.  It is independent of `q`, `R`, the admissible frequencies,
amplitudes, phases, and `B`; all displayed mode-count dependence is the
explicit factor `q^2`.

With

\[
 p_{\boldsymbol n,R}^{\rm plat}
 :=R^{-2}\omega M_{\boldsymbol n,R}^{\rm plat},
 \qquad
 \mathfrak X_{\boldsymbol n,R}
 :=\frac{\omega}{R}[\mathcal T_{\boldsymbol n,R}]_+,
 \tag{Y.7}
\]

equation Y.6 gives

\[
 \boxed{
 \mathfrak X_{\boldsymbol n,R}
 \le Cq^2a^{2/3}\omega^{1/3}
 \bigl(p_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{Y.8}
\]

For fixed `q`, and more generally whenever `\log q=o(L^2)`, the exact
`L^2`-scale coefficient remains

\[
 \lim_{L\to\infty}\frac1{L^2}
 \log\!\left(q^2a^{2/3}\omega^{1/3}\right)
 =-\frac2{11907}.
 \tag{Y.9}
\]

The theorem does not cover unresolved spectral clusters
`\ell\delta_{\boldsymbol n}<8q`.  It therefore neither contradicts nor
removes the consecutive-frequency outer-cap packet obstruction of R0.75R.

## 1. Frozen inputs

Retain

\[
 a=pL,\qquad R=e^{-\rho L^2/4},\qquad
 \omega=e^{-c_\gamma L^2/4},\qquad T_R=4R^2,
 \tag{Y.10}
\]

and the frozen radial chart and cutoff conditions

\[
 0<\delta_0<\delta,\qquad a\ge4\delta_0,\qquad
 (a+\delta)R<\frac\pi2,
 \qquad
 0\le\eta_R\le1,\qquad \eta_R(0)=0,\qquad
 |\eta_R'(t)|\le C_\eta R^{-2}.
 \tag{Y.11}
\]

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | complete clock and cutoff |
| `research/r075r_outer_cap_spectral_concentration_obstruction.md` | `e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3` | radial fibre and unresolved-packet boundary |
| `research/r075u_two_harmonic_difference_frequency_payment.md` | `f9fb331cf880b20f3b407fe66453bce71517ac1ef2af4fa0863c00325c1022a4` | radial quotient and complete-clock scaling |
| `research/r075x_fixed_finite_mode_low_carrier_payment.md` | `8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763` | complementary low-carrier theorem |

No external observability theorem is needed below.  The only spatial
estimate is a finite Gram-matrix calculation with its constant shown.

## 2. Signed-spectrum Gram coercivity

Let

\[
 I_\ell=[-\ell/2,\ell/2],
 \qquad
 S(t)^2:=\sum_{j=1}^q A_j(t)^2.
 \tag{Y.12}
\]

At a fixed time, write

\[
 F(t,y)=\sum_{\lambda\in\Lambda}c_\lambda(t)e^{i\lambda y},
 \qquad
 \Lambda=\{-n_q,\ldots,-n_1,n_1,\ldots,n_q\},
 \tag{Y.13}
\]

where

\[
 c_{n_j}(t)=\frac{A_j(t)}2e^{-i\phi_j(t)},
 \qquad
 c_{-n_j}(t)=\overline{c_{n_j}(t)}.
 \tag{Y.14}
\]

The minimum distance between two distinct members of `\Lambda` is exactly
`\delta_{\boldsymbol n}`.  Direct integration gives

\[
 \begin{aligned}
 \int_{I_\ell}|F(t,y)|^2\,dy
 &=\ell\sum_{\lambda\in\Lambda}|c_\lambda(t)|^2\\
 &\quad+\sum_{\substack{\lambda,\mu\in\Lambda\\\lambda\ne\mu}}
 c_\lambda(t)\overline{c_\mu(t)}
 \frac{2\sin((\lambda-\mu)\ell/2)}{\lambda-\mu}.
 \end{aligned}
 \tag{Y.15}
\]

Since `|\Lambda|=2q`,

\[
 \sum_{\lambda\ne\mu}|c_\lambda||c_\mu|
 \le(2q-1)\sum_{\lambda\in\Lambda}|c_\lambda|^2.
 \tag{Y.16}
\]

Consequently, the absolute value of the off-diagonal row in Y.15 is at
most

\[
 \frac{2(2q-1)}{\delta_{\boldsymbol n}}
 \sum_{\lambda\in\Lambda}|c_\lambda(t)|^2
 \le\frac\ell2\sum_{\lambda\in\Lambda}|c_\lambda(t)|^2,
 \tag{Y.17}
\]

where the final inequality uses Y.3.  Because
`\sum_{\lambda\in\Lambda}|c_\lambda|^2=S(t)^2/2`, equations
Y.15--Y.17 yield

\[
 \boxed{
 \int_{I_\ell}|F(t,y)|^2\,dy
 \ge\frac\ell4S(t)^2.}
 \tag{Y.18}
\]

Holder's inequality on `I_\ell` then gives

\[
 \boxed{
 \int_{I_\ell}|F(t,y)|^3\,dy
 \ge\ell^{-1/2}
 \left(\int_{I_\ell}|F(t,y)|^2\,dy\right)^{3/2}
 \ge\frac\ell8S(t)^3.}
 \tag{Y.19}
\]

This is phase-uniform and contains no hidden compactness or inverse-gap
constant: the price of separation is stated entirely in Y.3.

## 3. A phase-free complete-clock row

The next lemma is the phase-free version of the moving-phase estimate.  It
is sufficient because Y.19 controls the individual modal amplitudes, rather
than only a cancellation defect.

**Lemma Y.1.**  Let `\zeta` be absolutely continuous on `[0,4]` and satisfy

\[
 0\le\zeta\le1,\qquad \zeta(0)=0,\qquad
 |\zeta'|\le C_\eta.
 \tag{Y.20}
\]

For every `\Lambda_0\ge0`, `\sigma,\alpha\in\mathbb R`,

\[
 \boxed{
 \left|\sigma\int_0^4\zeta(s)e^{-\Lambda_0s}
 \sin(\alpha+\sigma s)\,ds\right|
 \le C
 \left(\int_0^4e^{-3\Lambda_0s/2}\,ds\right)^{2/3}.}
 \tag{Y.21}
\]

The constant depends only on `C_\eta`.

To prove it, let

\[
 \tau=\begin{cases}
 1,&0\le\Lambda_0\le1,\\
 \Lambda_0^{-1},&\Lambda_0\ge1.
 \end{cases}
 \tag{Y.22}
\]

The right side of Y.21 is comparable from above and below to
`\tau^{2/3}`.

If `|\sigma|\tau\le1` and `\Lambda_0\le1`, estimate the left side by
`4|\sigma|\le4`.  If `|\sigma|\tau\le1` and `\Lambda_0\ge1`, use
`\zeta(s)\le C_\eta s` to obtain

\[
 |\sigma|\int_0^4\zeta(s)e^{-\Lambda_0s}\,ds
 \le C|\sigma|\Lambda_0^{-2}
 \le C\tau
 \le C\tau^{2/3}.
 \tag{Y.23}
\]

If `|\sigma|\tau\ge1`, set
`w(s)=\zeta(s)e^{-\Lambda_0s}` and integrate the sine once:

\[
 \left|\sigma\int_0^4w(s)\sin(\alpha+\sigma s)\,ds\right|
 \le |w(4)|+\int_0^4|w'(s)|\,ds.
 \tag{Y.24}
\]

For `\Lambda_0\le1`, the last row is bounded by a constant.  For
`\Lambda_0\ge1`, Y.20 and `\zeta(s)\le C_\eta s` give

\[
 |w(4)|+\int_0^4|w'(s)|\,ds
 \le C\Lambda_0^{-1}
 =C\tau
 \le C\tau^{2/3}.
 \tag{Y.25}
\]

Equations Y.22--Y.25 prove the lemma.  Notice that no division by `\sigma`
occurs in the slow-phase case and no phase-distance lower bound is used.

## 4. Exact modal expansion and row payment

Use the frozen odd radial kernel

\[
 D_R(y)=-2\pi y\vartheta(|y|/R-a),
 \qquad
 J_{r,R}:=\int_{-\pi}^{\pi}D_R(y)\sin(ry)\,dy.
 \tag{Y.26}
\]

The exact radial quotient from R0.75U is

\[
 \boxed{\frac{|J_{r,R}|}{r}\le Ca^2R^3
 \qquad(r\ge1).}
 \tag{Y.27}
\]

Oddness of `D_R` and the product-to-sum identity expand Y.5 into exactly
`q^2` nonconstant sine rows:

\[
 \begin{aligned}
 \mathcal T_{\boldsymbol n,R}
 &=\frac B4\sum_{j=1}^qJ_{2n_j,R}
 \int_0^{T_R}\eta_R A_j(t)^2\sin(2\phi_j(t))\,dt\\
 &\quad+\frac B2\sum_{1\le i<j\le q}
 J_{n_j-n_i,R}\int_0^{T_R}\eta_R A_i(t)A_j(t)
 \sin(\phi_j(t)-\phi_i(t))\,dt\\
 &\quad+\frac B2\sum_{1\le i<j\le q}
 J_{n_i+n_j,R}\int_0^{T_R}\eta_R A_i(t)A_j(t)
 \sin(\phi_i(t)+\phi_j(t))\,dt.
 \end{aligned}
 \tag{Y.28}
\]

The count is `q+2\binom q2=q^2`: one self row per mode and one difference
plus one sum row per unordered pair.

Every row has the form

\[
 B J_{r,R}\int_0^{T_R}\eta_R(t)P_0e^{-\lambda t}
 \sin(\alpha+rBt)\,dt,
 \tag{Y.29}
\]

up to a factor `1/4` or `1/2`, where `r` is a positive integer,
`P(t)=P_0e^{-\lambda t}` is either `A_j(t)^2` or
`A_i(t)A_j(t)`, and `\lambda` is respectively `2n_j^2` or
`n_i^2+n_j^2`.

Scale `t=R^2s` and put

\[
 \Lambda_0=\lambda R^2,\qquad
 \sigma=rBR^2,\qquad
 \zeta(s)=\eta_R(R^2s).
 \tag{Y.30}
\]

Lemma Y.1 gives the exact physical-time estimate

\[
 \boxed{
 \left|B\int_0^{T_R}\eta_R(t)P(t)
 \sin(\alpha+rBt)\,dt\right|
 \le\frac{C}{rR^{4/3}}
 \left(\int_0^{T_R}P(t)^{3/2}\,dt\right)^{2/3}.}
 \tag{Y.31}
\]

Indeed, the left side after scaling is `P_0/r` times the left side of
Y.21, while

\[
 \left(\int_0^{T_R}P(t)^{3/2}\,dt\right)^{2/3}
 =R^{4/3}P_0
 \left(\int_0^4e^{-3\Lambda_0s/2}\,ds\right)^{2/3}.
 \tag{Y.32}
\]

For every self or cross row,

\[
 P(t)^{3/2}\le S(t)^3.
 \tag{Y.33}
\]

Multiplying Y.31 by Y.27 and summing the exactly `q^2` rows of Y.28
therefore yields

\[
 |\mathcal T_{\boldsymbol n,R}|
 \le Cq^2a^2R^{5/3}
 \left(\int_0^{T_R}S(t)^3\,dt\right)^{2/3}.
 \tag{Y.34}
\]

Absolute values are safe here because the strong-separation observation
Y.19 controls every modal product.  This is precisely the step that is not
available for an unresolved cluster.

## 5. Plateau mass and scale conversion

The frozen radial fibre inequality is

\[
 \int_{\mathcal S_{a,R}^{\rm plat}}|F(t,x_2)|^3\,dx
 \ge4\pi a\delta_0R^2
 \int_{I_\ell}|F(t,y)|^3\,dy.
 \tag{Y.35}
\]

Equations Y.19 and Y.35 imply

\[
 \boxed{
 M_{\boldsymbol n,R}^{\rm plat}
 \ge\frac{\pi\delta_0}{2}a^2R^3
 \int_0^{T_R}S(t)^3\,dt.}
 \tag{Y.36}
\]

Substitute Y.36 into Y.34:

\[
 \begin{aligned}
 |\mathcal T_{\boldsymbol n,R}|
 &\le Cq^2a^2R^{5/3}
 \left(\frac{M_{\boldsymbol n,R}^{\rm plat}}
 {a^2R^3}\right)^{2/3}\\
 &=Cq^2a^{2/3}R^{-1/3}
 \bigl(M_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3}.
 \end{aligned}
 \tag{Y.37}
\]

This proves Y.6.  Substituting
`M=R^2\omega^{-1}p` into `(\omega/R)` times Y.6 proves Y.8.  The frozen
identity `-c_\gamma/12=-2/11907`, together with
`\log q=o(L^2)` and `\log a=o(L^2)`, proves Y.9.

## 6. Exact-solution and Version-M boundary

The field Y.4 satisfies

\[
 \partial_tF+B\partial_2F-\partial_2^2F=0
 \tag{Y.38}
\]

and embeds in the exact smooth unforced shear `u=(0,B,F(t,x_2))` with
constant pressure.  The nonzero constant background has not been shown to
belong to the frozen mean-zero, inversion-paired Version-M subclass.

If the complete clock and plateau tube are in the same scale-`2R`
Version-M measurement row with weight at least `\omega`, and `F` is an
actual component of that same velocity, then Y.8 gives the conditional
payment

\[
 \mathfrak X_{\boldsymbol n,R}
 \le Cq^2(P_R^M)^{2/3}.
 \tag{Y.39}
\]

This is not valid merely for a Fourier projection of a larger velocity.

## 7. What is closed and what remains open

**Closed here:** the complete signed collar-flux estimate for every
strongly separated finite harmonic family in one dyadic band; all
self-, sum-, and difference-frequency rows; arbitrary amplitudes, phases,
and constant shear speed; an explicit `q^2` payment factor; and the exact
negative normalized rate whenever `\log q=o(L^2)`.

**Open:** unresolved high-carrier clusters with
`\ell\delta_{\boldsymbol n}<8q`; removal or weakening of the strong
separation hypothesis; arbitrary dyadic packets; inter-packet aggregation;
nonconstant or vertically dependent shear; projection from a larger
velocity; arbitrary-field E.24; complete Version-M extraction; fixed
deletion; suitable-weak transfer; regularity; and singularity.

R0.75Y does not control the consecutive-frequency packet in R0.75R, whose
signed-spectrum separation is far below Y.3 on the frozen collar scale.
The proof is analytic, and no simulation or formal scientific figure is
needed.  No completeness, novelty, or priority claim is made.
**NOT CLAY.**
