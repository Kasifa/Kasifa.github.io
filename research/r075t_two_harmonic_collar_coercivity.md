# R0.75T -- sharp collar coercivity for one dyadic pair

## 0. Result and exact boundary

R0.75S closes the complete-clock collar payment for one real horizontal
harmonic.  R0.75R rules out the corresponding plateau-only estimate for an
arbitrary concentrated high-band packet.  The first unresolved case between
those results is therefore not another frequency endpoint: it is the
destructive interference of exactly two harmonics.

This note resolves the spatial part of that problem.  Let

\[
 f(x_2)=A\cos(kx_2-\phi)+C\cos(mx_2-\psi),
 \qquad 0\le C,A,\quad 1\le m<k\le2m,
 \tag{T.1}
\]

put `d=k-m`, `ell=aR`, and define

\[
 \begin{aligned}
 \delta_\pi&:=\operatorname {dist}
  (\phi-\psi,\pi+2\pi\mathbb Z),\\
 q_{d,\ell}^2&:=\min\{1,(d\ell)^2+\delta_\pi^2\},\\
 H_{d,\ell}^2&:=(A-C)^2+ACq_{d,\ell}^2.
 \end{aligned}
 \tag{T.2}
\]

There is an absolute constant `C_0>0` and a constant `c_0>0` depending only
on the frozen plateau width `delta_0` such that, whenever `maR>=C_0`,

\[
 \boxed{
 \int_{\mathcal S_{a,R}^{\rm plat}}|f(x_2)|^3\,dx
 \ge c_0a^2R^3H_{d,aR}^3.}
 \tag{T.3}
\]

The lower bound is uniform in the carrier frequency, the two amplitudes, and
both phases.  Its degeneracy is also sharp: when `A=C`, the relative phase is
`pi`, and `dell<<1`, the two waves cancel to first order and both sides have
size `A^3(dell)^3a^2R^3`.

For the exact diffusive constant-shear pair

\[
 \begin{aligned}
 F(t,x_2)&=A_t\cos(kx_2-\phi_t)
          +C_t\cos(mx_2-\psi_t),\\
 A_t&=Ae^{-k^2t},\quad C_t=Ce^{-m^2t},\\
 \phi_t&=\phi+kBt,\quad\psi_t=\psi+mBt,
 \end{aligned}
 \tag{T.4}
\]

the same estimate holds at every time, with

\[
 \delta_\pi(t)=\operatorname {dist}
 (\phi-\psi+dBt,\pi+2\pi\mathbb Z)
 \tag{T.5}
\]

and `A,C` replaced by `A_t,C_t`.  Define the complete-clock plateau mass by

\[
 M_{k,m,R}^{\rm plat}:=
 \int_0^{T_R}\!\int_{\mathcal S_{a,R}^{\rm plat}}
 |F(t,x_2)|^3\,dxdt.
\]

Then

\[
 \boxed{
 M_{k,m,R}^{\rm plat}
 \ge c_0a^2R^3\int_0^{T_R}H_{d,aR}(t)^3\,dt.}
 \tag{T.6}
\]

Equation T.6 is the exact spatial coercivity input needed for the remaining
difference-frequency time estimate.  This note does **not** yet prove that
the complete two-harmonic signed flux is bounded by
`(M_(k,m,R)^plat)^(2/3)`.

## 1. Frozen inputs and plateau fibre

Retain

\[
 a=pL,\qquad R=e^{-\rho L^2/4},\qquad
 T_R=4R^2,
 \tag{T.7}
\]

and the radial profile from R0.75R--S:

\[
 \xi_{a,R}(x)=\vartheta(|x|/R-a),\qquad
 \vartheta=1\ \hbox{on }[-\delta_0,\delta_0],
 \quad a\ge4\delta_0,
 \tag{T.8}
\]

with `(a+delta)R<pi/2`.  The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` | exact difference-frequency flux |
| `research/r075m_dyadic_packet_diffusive_flux_gain.md` | `13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7` | dyadic within-packet boundary |
| `research/r075r_outer_cap_spectral_concentration_obstruction.md` | `e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3` | arbitrary-packet obstruction |
| `research/r075s_full_frequency_single_harmonic_clock_payment.md` | `d2736eaa43443048bd620567c4acd72024dc4c662320a8aa58af31ccc6047ccd` | one-harmonic complete-clock theorem |

For every `|y|<=aR/2`, both radial boundaries of the plateau shell meet the
`(x_1,x_3)` fibre.  Their squared radii differ by

\[
 ((a+\delta_0)R)^2-y^2-
 (((a-\delta_0)R)^2-y^2)=4a\delta_0R^2.
 \tag{T.9}
\]

Consequently the fibre area is exactly

\[
 \left|\{(x_1,x_3):(x_1,y,x_3)
 \in\mathcal S_{a,R}^{\rm plat}\}\right|
 =4\pi a\delta_0R^2.
 \tag{T.10}
\]

Taking `I_ell=[-ell/2,ell/2]` therefore gives

\[
 \int_{\mathcal S_{a,R}^{\rm plat}}|f(x_2)|^3\,dx
 \ge4\pi a\delta_0R^2\int_{I_\ell}|f(y)|^3\,dy.
 \tag{T.11}
\]

No observability theorem is hidden in this geometric reduction.

## 2. A slow-envelope sampling lemma

The only analytic issue is cancellation of the two waves.  The following
elementary two-dimensional lemma keeps the sharp beat defect.

**Lemma T.1.**  There are absolute constants `M_0,c_1>0` with the following
property.  Let `I=[-1/2,1/2]`, `0<=beta<=1`, `mu>=M_0`, and
`alpha,gamma in C`.  Set

\[
 Z(s)=\alpha e^{i\beta s/2}+\gamma e^{-i\beta s/2}.
 \tag{T.12}
\]

Then

\[
 \int_I|\operatorname {Re}(e^{i\mu s}Z(s))|^2\,ds
 \ge c_1\int_I|Z(s)|^2\,ds.
 \tag{T.13}
\]

To prove the lemma without a singular constant as `beta` tends to zero, use
the regular basis

\[
 u_\beta(s)=\cos(\beta s/2),\qquad
 v_\beta(s)=
 \begin{cases}
  2\beta^{-1}\sin(\beta s/2),&\beta>0,\\
  s,&\beta=0.
 \end{cases}
 \tag{T.14}
\]

The Gram matrix of `(u_beta,v_beta)` on `I` is continuous and positive
definite for `0<=beta<=1`.  Compactness of this closed parameter interval
therefore gives the uniform inverse bounds

\[
 \|Z\|_{L^\infty(I)}+\|Z'\|_{L^2(I)}
 \le C\|Z\|_{L^2(I)}.
 \tag{T.15}
\]

The identity

\[
 \int_I|\operatorname {Re}(e^{i\mu s}Z)|^2
 =\frac12\int_I|Z|^2
 +\frac12\operatorname {Re}\int_Ie^{2i\mu s}Z^2
 \tag{T.16}
\]

and one integration by parts give

\[
 \left|\int_Ie^{2i\mu s}Z^2\right|
 \le\frac C\mu\int_I|Z|^2.
 \tag{T.17}
\]

Choosing `M_0` once proves T.13.  This is a fixed two-dimensional norm
equivalence, not an invocation of a general spectral inequality.

## 3. The sharp two-wave `L^2` row

Write

\[
 d=k-m,\quad c=\frac{k+m}{2},\quad
 \Delta=\phi-\psi,\quad\Sigma=\phi+\psi.
 \tag{T.18}
\]

Then T.1 has the exact carrier-envelope representation

\[
 f(y)=\operatorname {Re}
 \left[e^{i(cy-\Sigma/2)}Z(y)\right],
 \quad
 Z(y)=Ae^{i(dy/2-\Delta/2)}
      +Ce^{-i(dy/2-\Delta/2)}.
 \tag{T.19}
\]

### 3.1 Unresolved beat: `dell<=1`

Rescale `y=ell s`.  Since `cell>=mell`, Lemma T.1 applies once
`mell>=C_0`.  It yields

\[
 \int_{I_\ell}|f|^2\,dy
 \ge c\int_{I_\ell}|Z|^2\,dy.
 \tag{T.20}
\]

The envelope integral is exact:

\[
 \frac1\ell\int_{I_\ell}|Z|^2\,dy
 =A^2+C^2+2AC\operatorname {sinc}(d\ell/2)\cos\Delta,
 \tag{T.21}
\]

where `sinc z=sin(z)/z`.  With
`theta=dist(Delta,pi+2pi Z)`, the last row is

\[
 (A-C)^2+2AC
 \left[1-\operatorname {sinc}(d\ell/2)\cos\theta\right].
 \tag{T.22}
\]

For `0<=dell<=1`, elementary Taylor bounds give

\[
 1-\operatorname {sinc}(d\ell/2)\cos\theta
 \ge c\min\{1,(d\ell)^2+\theta^2\}.
 \tag{T.23}
\]

Thus

\[
 \int_{I_\ell}|f|^2\,dy
 \ge c\ell H_{d,\ell}^2.
 \tag{T.24}
\]

### 3.2 Resolved beat: `dell>=1`

Direct integration gives

\[
 \begin{aligned}
 \int_{I_\ell}|f|^2
 &=\frac\ell2(A^2+C^2)
 +\frac{A^2\sin(k\ell)\cos(2\phi)}{2k}
 +\frac{C^2\sin(m\ell)\cos(2\psi)}{2m}\\
 &\quad+AC\ell\operatorname {sinc}(d\ell/2)\cos\Delta
 +AC\ell\operatorname {sinc}((k+m)\ell/2)\cos\Sigma.
 \end{aligned}
 \tag{T.25}
\]

For `dell>=1`,

\[
 |\operatorname {sinc}(d\ell/2)|
 \le2\sin(1/2)<1.
 \tag{T.26}
\]

The three remaining boundary-frequency errors in T.25 are at most
`C(mell)^(-1)ell(A^2+C^2)`.  Increasing `C_0` if necessary gives

\[
 \int_{I_\ell}|f|^2\,dy
 \ge c\ell(A^2+C^2)
 \ge c\ell H_{d,\ell}^2.
 \tag{T.27}
\]

Equations T.24 and T.27 cover all beat frequencies.

## 4. Cubic coercivity and the diffusive corollary

Holder's inequality on an interval of length `ell` gives

\[
 \int_{I_\ell}|f|^3\,dy
 \ge\ell^{-1/2}
 \left(\int_{I_\ell}|f|^2\,dy\right)^{3/2}
 \ge c\ell H_{d,\ell}^3.
 \tag{T.28}
\]

Combining T.28 with the exact fibre T.10 proves T.3.

For T.4, each time slice is again a dyadic pair with nonnegative amplitudes
`A_t,C_t` and relative phase T.5.  The frequency condition is unchanged.
Applying T.3 pointwise in time and integrating proves T.6.  Notice that
unequal heat rates are retained exactly in `A_t-C_t`; they are not replaced
by a common dyadic damping factor.

## 5. Exact flux decomposition and the next scalar target

Let

\[
 J_{n,R}:=\int_{-\pi}^{\pi}D_R(y)\sin(ny)\,dy,
 \qquad
 D_R(y)=-2\pi y\vartheta(|y|/R-a).
 \tag{T.29}
\]

Oddness of `D_R` and the product-to-sum identity give the exact signed-flux
decomposition

\[
 \begin{aligned}
 \mathcal T_{k,m,R}
 &=\frac B4\int_0^{T_R}\eta(t)
 \left[A_t^2J_{2k,R}\sin(2\phi_t)
       +C_t^2J_{2m,R}\sin(2\psi_t)\right]dt\\
 &\quad+\frac B2\int_0^{T_R}\eta(t)A_tC_t
 \left[J_{d,R}\sin(\phi_t-\psi_t)
       +J_{k+m,R}\sin(\phi_t+\psi_t)\right]dt.
 \end{aligned}
 \tag{T.30}
\]

The dangerous term is now explicit: it is the low difference frequency
`d`, and its phase is exactly the phase entering `H_(d,aR)(t)`.  The next
positive theorem must prove a weighted moving-phase estimate of the form

\[
 \left|B J_{d,R}\int_0^{T_R}
 \eta A_tC_t\sin(\phi-\psi+dBt)\,dt\right|
 \le Ca^{2/3}R^{-1/3}
 \left(a^2R^3\int_0^{T_R}H_{d,aR}(t)^3dt\right)^{2/3},
 \tag{T.31}
\]

together with compatible control of the two self frequencies and the sum
frequency.  T.31 is not assumed or proved here.

## 6. Meaning and open boundary

**Proved:** the exact plateau-fibre identity T.10; the uniform slow-envelope
sampling lemma T.13; the sharp unresolved-beat defect T.21--T.24; the
resolved-beat estimate T.25--T.27; the local cubic lower bound T.3; its exact
diffusive time-slice integration T.6; and the four-frequency flux identity
T.30.

**What changes:** destructive interference of one dyadic pair is no longer
an unstructured loss.  It is measured by one explicit scalar defect.  The
defect simultaneously records amplitude mismatch, beat distance `dell`, and
distance from the cancelling relative phase.  No carrier-frequency or
mode-count loss occurs once the collar contains a fixed number of periods of
the lower carrier.

**Not proved:** T.31; complete two-harmonic flux payment; low-carrier pairs
with `maR<C_0`; three or more harmonics; arbitrary packets; inter-packet
summation; nonconstant or vertically dependent shear; projection from a
larger velocity; arbitrary-field E.24; complete Version-M extraction;
suitable-weak transfer; regularity; or singularity.  The result does not
contradict R0.75R, whose concentrating packet uses an increasing number of
modes.  No novelty or priority claim is made.  \(\mathbf{NOT\ CLAY}.\)
