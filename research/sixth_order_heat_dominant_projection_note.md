# R0.67C-2 — A strict sign for the dominant sixth-order heat projection

## Claim boundary

R0.67A found a strictly negative dominant coefficient for the zero-time
sixth-order correlation. R0.67B lifted the mass and four first moments and
proved the zero-affine resolvent gap \(256<\mu\). R0.67C-1 checked the complete
heat kernel at the first finite cycle \(M=16\), where the signed sum is
positive.

This note resolves the remaining asymptotic heat-cancellation question for
the same periodic target family. A degree-six centred Taylor-jet lift, exact
signed-shift aggregation, and a global seventh-derivative estimate give

\[
 \boxed{
 -1.71549\times10^{-6}
 < C_{6,\mathrm{heat}}
 < -2.02514\times10^{-7}.}
\tag{0.1}
\]

Thus the dominant complete heat projection is strictly negative and is not
annihilated by time integration. This is one fixed sixth-order coefficient
in one periodic model. It does not control the sum over all Picard orders and
does not prove norm inflation, singularity, or three-dimensional
Navier--Stokes regularity.

## 1. The limiting heat observable

Repeat the least-significant-bit-first word \(0100\). After \(r\) blocks,

\[
 M_r=16^r,\qquad
 q_r=\frac{2(16^r-1)}{15},\qquad
 \theta_r=\frac{q_r}{M_r}\longrightarrow\theta_\infty=\frac2{15}.
\tag{1.1}
\]

For \(x=(x_A,x_B,x_C,x_D)\in[0,1]^4\), put

\[
\begin{aligned}
 a&=1+\frac{x_A}{4},&
 b&=1+\frac{x_B}{4},&
 c&=1+\frac{x_C}{4},\\
 d&=1+\frac{x_D}{4},&
 e&=1+\frac{x_A+x_B+x_C-x_D-\theta}{4},&
 h&=1+\frac{\theta}{4}.
\end{aligned}
\tag{1.2}
\]

There are ten order-preserving shuffles of the positive carriers
\((a,b,c)\) and negative carriers \((-d,-e)\). For one signed sequence
\(k_0,\ldots,k_4\), define

\[
 p_0=-h,\qquad p_{j+1}=p_j+k_j,\qquad
 r_j=p_j^2+\sum_{\ell=j}^4 k_\ell^2.
\tag{1.3}
\]

The constraint gives \(p_5=0\). At \(T=\log(2)/2\), the complete limiting
observable is

\[
 F_{\theta_\infty}(x)
 =\sum_{\text{10 shuffles}}
 \int_{\substack{\tau_j\ge0\\\sum_{j=0}^4\tau_j\le T}}
 \exp\!\left(-\sum_{j=0}^4r_j(x)\tau_j\right)d\tau.
\tag{1.4}
\]

No single ordering or zero-time surrogate is substituted for this full
five-simplex factor.

## 2. Why the affine lift is not enough

The R0.67B five-atom term already has the desired sign:

\[
 B_1=-8.7844512025308\times10^{-7}.
\tag{2.1}
\]

Its global \(C^{1,1}\)-dual error bound is nevertheless too wide to decide
the full sign. This is a limitation of the estimate, not evidence that the
projection vanishes. Increasing the jet degree improves the spatial
contraction by an exact factor \(1/16\) per degree.

## 3. The centred degree-six jet

Let \(c=(1/2,1/2,1/2,1/2)\) and define, state by state,

\[
 \widehat M_{\alpha,i}=\int(x-c)^\alpha\,d\nu_i(x),
 \qquad |\alpha|\le6.
\tag{3.1}
\]

There are

\[
 \binom{10}{4}=210
\tag{3.2}
\]

channels per state and \(320\times210=67{,}200\) finite coordinates. The
centred jet distribution is

\[
 (J_6\widehat M)_i(f)
 =\sum_{|\alpha|\le6}
 \frac{\widehat M_{\alpha,i}}{\alpha!}\partial^\alpha f(c).
\tag{3.3}
\]

It agrees with \(\nu_i\) on every polynomial of degree at most six. The
degree-\(d\) diagonal moment block is \(W/16^d\), so no new eigenvalue competes
with

\[
 402.425429345624<\mu<402.4254293456256.
\tag{3.4}
\]

The audit isolates the \(q_4\) primary component by an exact Chinese
remainder projector and then selects this root. Pairing (3.3) with the Taylor
jet of (1.4) gives

\[
 B_6=-9.5893838936721\times10^{-7}.
\tag{3.5}
\]

Only the guarded enclosure

\[
 -9.70\times10^{-7}<B_6<-9.48\times10^{-7}
\tag{3.6}
\]

is used below.

## 4. Signed-shift defect

Every four-bit branch is

\[
 x\longmapsto\frac{x+e}{16},
 \qquad e\in\{0,\ldots,15\}^4.
\tag{4.1}
\]

Set \(R_6=\mathcal PJ_6-J_6L_6\). Each component of \(R_6v\) annihilates all
polynomials of degree at most six. The audit first combines every signed path
landing at the same shift \(e\), then takes absolute values. If
\(g_{i,\alpha}(e)\) is the resulting coefficient, Taylor's theorem in the
\(\ell^1\) metric gives

\[
 b_i=\sum_{|\alpha|\le6}\sum_e
 |g_{i,\alpha}(e)|
 \frac{s(e)^{7-|\alpha|}}{(7-|\alpha|)!},
 \qquad
 s(e)=\left\|\frac{e+c}{16}-c\right\|_1.
\tag{4.2}
\]

The raw results are

\[
 b_{\rm obs}=4.8605634222351,\qquad
 \max_i\frac{b_i}{w_i}=8.8474298122\times10^{-5}.
\tag{4.3}
\]

The proof uses only

\[
 b_{\rm obs}<5,\qquad \max_i\frac{b_i}{w_i}<10^{-4}.
\tag{4.4}
\]

## 5. The zero-sixth-jet resolvent

The seventh-order Taylor remainder contracts by \(16^{-7}\). Combining this
with the exact absolute branch weight \(65536\) gives

\[
 \boxed{
 \|\mathcal P\zeta\|_{(C^{6,1})^*,w}
 \le\frac{65536}{16^7}\|\zeta\|_{(C^{6,1})^*,w}
 =\frac1{4096}\|\zeta\|_{(C^{6,1})^*,w}.}
\tag{5.1}
\]

Keeping the zeroth resolvent term statewise and bounding the tail by the
weighted norm yields

\[
 Z_{\rm obs}\le
 \frac{b_{\rm obs}}{\mu}
 +\frac{w_{\rm obs}\|b\|_w}{\mu}
 \frac{(4096\mu)^{-1}}{1-(4096\mu)^{-1}},
 \qquad w_{\rm obs}=631131.
\tag{5.2}
\]

The guarded data imply

\[
 \boxed{Z_{\rm obs}<0.012425.}
\tag{5.3}
\]

## 6. A global seventh-derivative bound

Write \(g(x,\tau)=\sum_jr_j(x)\tau_j\). For a multiindex \(\gamma\), define
\(P_\gamma\) by

\[
 \partial^\gamma e^{-g}=e^{-g}P_\gamma.
\tag{6.1}
\]

Because every \(r_j\) is quadratic, all derivatives through degree seven
follow from

\[
 P_0=1,\qquad
 P_{\gamma+e_i}=\partial_iP_\gamma-(\partial_i g)P_\gamma.
\tag{6.2}
\]

For every shuffle, the audit expands \(P_\gamma\) in \(y=x-c\) and the five
simplex variables. Since each rate is a sum of squares, \(e^{-g}\le1\).
Every absolute time monomial is integrated by

\[
 \int_{\substack{\tau_j\ge0\\\sum\tau_j\le T}}
 \tau^\beta\,d\tau
 =\frac{T^{|\beta|+5}\beta!}{(|\beta|+5)!}.
\tag{6.3}
\]

The complete raw bound is

\[
 \max_{|\gamma|=7}\sup_{x\in[0,1]^4}
 |\partial^\gamma F_{\theta_\infty}(x)|
 \le5.1612521669\times10^{-5},
\tag{6.4}
\]

attained at \(\gamma=(0,0,7,0)\). The proof uses the wider guard

\[
 \boxed{L_7<6\times10^{-5}.}
\tag{6.5}
\]

## 7. The strict interval

Let

\[
 \eta=(\mu-\mathcal P)^{-1}R_6v,\qquad
 \rho_v=J_6v+\eta.
\tag{7.1}
\]

Equations (5.3) and (6.5) imply

\[
 |\eta(F_{\theta_\infty})|
 <0.012425\cdot6\times10^{-5}
 <7.455\times10^{-7}.
\tag{7.2}
\]

Combining (3.6) and (7.2) proves

\[
 \boxed{
 -1.71549\times10^{-6}
 <\rho_v(F_{\theta_\infty})
 <-2.02514\times10^{-7}.}
\tag{7.3}
\]

## 8. Consequence and research value

The finite complement has spectral radius below \(300\), while the R0.67B
zero-affine remainder contracts at \(256\); both are below \(\mu\). Moreover

\[
 \theta_r-\theta_\infty=-\frac{2}{15M_r}.
\tag{8.1}
\]

The normalized complete sixth-order signed heat correlation therefore obeys

\[
 \mu^{-r}\mathcal S_{6,r}^{\rm heat}
 \longrightarrow C_{6,\mathrm{heat}}<0.
\tag{8.2}
\]

Its critical spatial normalization keeps the supercritical block ratio
\(\mu/256>1\). The positive first-cycle result R0.67C-1 and negative
asymptotic coefficient are compatible: they imply a finite-scale crossover.

The real gain is that full heat integration is no longer a cancellation
loophole at order six. The remaining barriers are decisive:

1. this is one even order, not the full nonlinear Picard series;
2. at the quartic-critical amplitude, the sixth-order term carries an
   additional small amplitude factor;
3. the packet lies in a globally smooth invariant shear class and cannot
   itself produce a three-dimensional singularity.

R0.68 will therefore seek a uniform all-even-order majorant/minorant
compatible with the exact fourth- and sixth-order spectral data.

## 9. Reproducibility

Run the following command:

    python3 research/sixth_order_heat_dominant_projection_audit.py \
      --output /tmp/r067c2-dominant-heat-audit.json \
      --r067b-certificate \
        research/certificates/r067b/sixth-order-affine-moment-audit.json \
      --progress

The full audit takes about ten minutes on the current workstation and emits
progress after every shuffle. The certificate records fourteen checks, the
upstream hash, guarded interval, runtime, and resource log.
