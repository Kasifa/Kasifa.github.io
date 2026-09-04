# R0.76G -- complete-clock exponential lower bound for the central-fibre flux row

## 0. Result and exact boundary

R0.76F proves that the spatial observation used in R0.76E must lose
exponentially in the number of modes.  That static example has zero drift,
so its collar flux vanishes.  The present note closes that particular gap:
the exponential obstruction survives a nonzero drift, the frozen complete
clock, and the fully integrated signed collar flux when the payment is the
central fibre used in the R0.76E proof.

Retain

\[
 a=pL,\qquad p=\frac{32}{63},\qquad
 R=e^{-\rho L^2/4},\qquad
 \omega=e^{-c_\gamma L^2/4},
 \tag{G.1}
\]

with `rho=9/10000` and `c_gamma=8/3969`.  Put

\[
 m=m(L):=\left\lfloor\frac{a^2}{1024}\right\rfloor,
 \qquad q=2m+1,\qquad \varepsilon=aR,
 \qquad \beta=\frac1{100}.
 \tag{G.2}
\]

For all sufficiently large frozen `L`, there is a real trigonometric
polynomial `f_L` with exactly `q` positive frequencies

\[
 2m,2m+1,\ldots,4m,
 \tag{G.3}
\]

and a nonzero constant drift

\[
 B=-\frac{\beta a}{R},\qquad v=\frac{BR}{a}=-\beta,
 \tag{G.4}
\]

such that its transported heat evolution

\[
 F_L(t,x_2)=e^{t\partial_2^2}f_L(x_2-Bt)
 \tag{G.5}
\]

is an exact smooth unforced Navier--Stokes shear.  In the scaled variables

\[
 G_L(s,z)=F_L(R^2s,aRz),\qquad
 H_L=\int_0^4\!\int_{-1/2}^{1/2}|G_L(s,z)|^3\,dzds,
 \tag{G.6}
\]

let `zeta` be the translated frozen complete-clock cutoff and let

\[
 \mathcal S_L
 :=v\int_0^4\!\zeta(s)\int_{\mathbb R}W_a(z)|G_L(s,z)|^2\,dzds,
 \qquad
 W_a(z)=-2\pi az\vartheta(a(|z|-1)).
 \tag{G.7}
\]

Then

\[
 \boxed{
 \frac{\mathcal S_L}{H_L^{2/3}}
 \ge c_*\beta
 \left(\frac97\right)^{4m}.}
 \tag{G.8}
\]

Here and below, `c_*`, `c_j`, and `C_j` are positive constants depending
only on the frozen cutoff profile and the fixed cap interval, never on `L`
or `A`.

The numerator in G.8 is the complete signed flux, not its absolute-value
majorant and not a single-time observation.  Since

\[
 \frac{q(L)}{L^2}\longrightarrow\frac2{3969}>0,
 \tag{G.9}
\]

G.8 proves an `exp(cq)` lower bound for the complete-real central-fibre row
G.7.  It therefore upgrades R0.76F from a static observation obstruction to
an actual complete-clock flux obstruction for that intermediate row.

This does **not** prove an exponential lower bound for R0.76E's final
physical estimate against the full three-dimensional plateau mass
`M_(n,R)^plat`.  The plateau contains fibres adjacent to the transition cap
and can see values that the central interval in G.6 misses.  Section 7 makes
this non-transfer explicit.  No counterexample to R0.76E, E.24, or Version-M
is claimed.

## 1. Frozen clock and a positive cap

The absolute clock in R0.75B runs from `s_R=61R^2` to `t_2=65R^2`.  Write

\[
 \widetilde\eta_R(t):=\eta_R(s_R+t),\qquad
 \zeta(s):=\widetilde\eta_R(R^2s),\qquad 0\le s\le4.
 \tag{G.10}
\]

On the original absolute interval, use the translated solution
\(\widehat F_L(t,x_2):=F_L(t-s_R,x_2)\).  All occurrences of `t` after
this clock reset denote elapsed time in `[0,4R^2]`; this is exactly the
change of variables used again in G.35.

The frozen definition gives

\[
 0\le\zeta\le1,\qquad \zeta(0)=0,\qquad
 |\zeta'|\le C_\eta,\qquad
 \zeta(s)=1\quad(3<s<4).
 \tag{G.11}
\]

This last terminal identity is stronger than the onset bound retained in
R0.76C--E and is essential for the lower bound.

Recall that the frozen cutoff has \(0<\delta_0<\delta\) and
\(\operatorname{supp}\vartheta\subset(-\delta,\delta)\).  Choose the
positive transition subcap from R0.75R.  There are fixed `s_*`, `h`, and
`c_0>0` such that

\[
 \delta_0<s_*-3h<s_*+3h<\delta,
 \qquad \vartheta(r)\ge c_0
 \quad(|r-s_*|\le3h).
 \tag{G.12}
\]

In scaled coordinates set

\[
 I_{a,+}:=\left[1+\frac{s_*-2h}{a},
                     1+\frac{s_*+2h}{a}\right].
 \tag{G.13}
\]

Its length is `4h/a`, and the exact radial cross-section gives

\[
 -W_a(z)\ge c_1a\quad(z\in I_{a,+}),
 \qquad
 W_a(z)\ge0\quad(z<0).
 \tag{G.14}
\]

The second inequality is strict wherever
`vartheta(a(|z|-1))>0`.

Thus `v=-beta` makes the positive cap favourable.  Only the negative cap can
contribute with the adverse sign.

## 2. A real dyadic packet and its exact NSE evolution

Let `y=x_2+aR/2` and define

\[
 f_L(x_2)
 :=A\left(2\sin\frac y2\right)^{2m}\cos(3my),
 \qquad A>0.
 \tag{G.15}
\]

The even trigonometric polynomial `(2 sin(y/2))^(2m)` has every frequency
from `-m` through `m`, with nonzero real coefficients.  Multiplication by
`cos(3my)` shifts these frequencies into the two disjoint bands

\[
 [-4m,-2m]\cup[2m,4m].
 \tag{G.16}
\]

Consequently the positive frequencies are exactly G.3.  They are strictly
ordered and satisfy `n_q=4m=2n_1`; coefficient signs are absorbed into real
phases, so the packet has the amplitude--phase form used in R0.76E.

The scalar field G.5 satisfies

\[
 (\partial_t+B\partial_2-\partial_2^2)F_L=0.
 \tag{G.17}
\]

Therefore

\[
 u_L(t,x)=(0,B,F_L(t,x_2))
 \tag{G.18}
\]

is divergence free and obeys the unforced three-dimensional Navier--Stokes
equation with constant pressure.  The constant background has not been
shown to belong to the frozen mean-zero, inversion-paired Version-M
subclass; the exact-shear benchmark is not promoted to that class here.

## 3. Heat-kernel moment lemma

Let `Z` be a standard real Gaussian and put

\[
 \sigma_s=\frac{\sqrt{2s}}a,\qquad
 w=z+\beta s+\frac12,\qquad X=w+\sigma_sZ.
 \tag{G.19}
\]

The periodic heat-kernel representation of G.5 is exactly

\[
 G_L(s,z)=A\,\mathbb E\left[
 \left(2\sin\frac{\varepsilon X}{2}\right)^{2m}
 \cos(3m\varepsilon X)\right].
 \tag{G.20}
\]

Two elementary bounds are needed.  Uniformly for `0<=s<=4`,

\[
 |G_L(s,z)|
 \le A\varepsilon^{2m}
 \left(|w|+\frac{4\sqrt m}{a}\right)^{2m}.
 \tag{G.21}
\]

Indeed, `|2sin(r/2)|<=|r|`, Minkowski's inequality, and
`(E|Z|^(2m))^(1/(2m))<=sqrt(2m)` prove G.21.

There is also a coherent lower bound: uniformly for

\[
 0\le s\le4,\qquad \frac32\le w\le\frac85,
 \tag{G.22}
\]

and all sufficiently large frozen `L`,

\[
 G_L(s,z)\ge\frac A2\varepsilon^{2m}w^{2m}.
 \tag{G.23}
\]

For completeness, split the expectation at `|X|=3`.  On `|X|<=3`,

\[
 \left(\frac{2\sin(\varepsilon X/2)}{\varepsilon X}\right)^{2m}
 =1+o(1),\qquad \cos(3m\varepsilon X)=1+o(1),
 \tag{G.24}
\]

uniformly, because

\[
 m\varepsilon^2\longrightarrow0,
 \qquad m\varepsilon\longrightarrow0.
 \tag{G.25}
\]

The omitted Gaussian moment is negligible.  Cauchy--Schwarz gives

\[
 \begin{aligned}
 \mathbb E\bigl[|X|^{2m};|X|>3\bigr]
 &\le (\mathbb E|X|^{4m})^{1/2}
       \mathbb P(|X|>3)^{1/2}\\
 &\le \left(\frac95\right)^{2m}
       \sqrt2\,e^{-49a^2/800}
 =o\bigl((3/2)^{2m}\bigr).
 \end{aligned}
 \tag{G.26}
\]

Here `m/a^2<=1/1024`, `sigma_s^2<=8/a^2`, and `w<=8/5` were used.  If
\(E_{\rm tail}:=\mathbb E[|X|^{2m};|X|>3]\), the good/bad decomposition
gives explicitly
\(G_L/(A\varepsilon^{2m})\ge
(1-o(1))(\mathbb E|X|^{2m}-E_{\rm tail})-E_{\rm tail}\).
Finally, convexity gives `E|X|^(2m)>=|EX|^(2m)=w^(2m)`, while G.26 is
`o(w^(2m))` uniformly on G.22.  This proves G.23.  The finite certificate
checks the constant ledger; it is not the proof of this limiting Gaussian
estimate.

## 4. The central fibre remains exponentially small

For `z in I=[-1/2,1/2]` and `0<=s<=4`, G.19 gives

\[
 |w|\le1+4\beta=\frac{26}{25},\qquad
 \frac{4\sqrt m}{a}\le\frac18.
 \tag{G.27}
\]

The exact rational comparison

\[
 \frac{26}{25}+\frac18=\frac{233}{200}<\frac76
 \tag{G.28}
\]

and G.21 imply

\[
 H_L\le4A^3\varepsilon^{6m}\left(\frac76\right)^{6m}.
 \tag{G.29}
\]

This is a spacetime bound over the full central observation window, not a
single-time estimate.

## 5. Complete signed-flux lower bound

On `(3,4) x I_(a,+)`, equations G.13 and G.19 give
`3/2<=w<=8/5` for all large `L`.  Equations G.11, G.14, and G.23 therefore
give the favourable contribution

\[
 (-v)\int_3^4\!\int_{I_{a,+}}
 (-W_a)|G_L|^2\,dzds
 \ge c_2\beta A^2\varepsilon^{4m}
       \left(\frac32\right)^{4m}.
 \tag{G.30}
\]

On the negative support of `W_a`,

\[
 |w|\le\frac12+\frac{\delta}{a}.
 \tag{G.31}
\]

Indeed, on this cap `w=-1/2-r/a+beta s` with `|r|<delta`.  For large
`L`, \(\delta/a+4\beta<1/2\), so `w<0` throughout and the positive drift
term can only decrease `|w|`; this proves G.31.  Taking also
`delta/a<=1/24`, equations G.21 and G.27 then give

\[
 |G_L(s,z)|
 \le A\varepsilon^{2m}\left(\frac23\right)^{2m}
 \qquad(z<0\hbox{ on }\operatorname{supp}W_a).
 \tag{G.32}
\]

The negative-cap `L^1` norm of `W_a` is bounded by a frozen constant.
Since `0<=zeta<=1`, its entire adverse contribution is at most

\[
 C_3\beta A^2\varepsilon^{4m}
 \left(\frac23\right)^{4m}.
 \tag{G.33}
\]

The rest of the positive cap has the favourable sign and may be discarded.
Because `(4/9)^(4m)` tends to zero, G.33 is absorbed by one half of G.30 for
large `L`.  Hence

\[
 \mathcal S_L\ge c_4\beta A^2\varepsilon^{4m}
 \left(\frac32\right)^{4m}>0.
 \tag{G.34}
\]

Dividing G.34 by G.29 to the power `2/3` proves G.8.

## 6. Frozen normalized consequence

The physical complete-clock flux is exactly

\[
 \mathcal T_L=\frac{a^2R^3}{2}\mathcal S_L.
 \tag{G.35}
\]

To state only what G.8 proves, define the central-fibre proxy

\[
 M_L^I:=a^2R^5H_L,\qquad
 p_L^I:=R^{-2}\omega M_L^I,
 \qquad \mathfrak X_L:=\frac\omega R[\mathcal T_L]_+.
 \tag{G.36}
\]

This `M_L^I` is not the full physical plateau mass.  Equations G.8 and
G.35--G.36 give

\[
 \frac{\mathfrak X_L}{(p_L^I)^{2/3}}
 \ge c_5\beta a^{2/3}\omega^{1/3}
 \left(\frac97\right)^{4m}.
 \tag{G.37}
\]

Since `a^2/L^2=1024/3969`,

\[
 \liminf_{L\to\infty}\frac1{L^2}
 \log\frac{\mathfrak X_L}{(p_L^I)^{2/3}}
 \ge
 \frac{4\log(9/7)}{3969}-\frac2{11907}>0.
 \tag{G.38}
\]

The sign is rigorous without decimal arithmetic: the elementary inequality
\(\log(1+x)>x/(1+x)\) at `x=2/7` gives `log(9/7)>2/9>1/6`, so the right
side of G.38 is greater than `2/35721`.  Thus a central-fibre-only payment
loses the frozen exponential gain along the explicit quadratic mode density
G.9.

## 7. Why this is not a lower bound against the physical plateau

The physical plateau is

\[
 \mathcal S_{a,R}^{\rm plat}
 =\{x:||x|/R-a|\le\delta_0\}.
 \tag{G.39}
\]

It contains robust fibres far beyond `I`.  For example, at
`z_p=1-3delta_0/a` and `x_3=0`, the transverse radius is at most
`(a-2delta_0)R`, so the exact fibre formula from R0.75P supplies an
`x_1` interval of length at least `4delta_0R`.

The outer transition point `z_o=1+s_*/a` is only `O(1/a)` away in the
scaled coordinate.  At the initial time the envelope in G.15 obeys

\[
 \log\frac{
  (2\sin(\varepsilon(z_o+1/2)/2))^{2m}}
  {(2\sin(\varepsilon(z_p+1/2)/2))^{2m}}
 \le C_{\delta_0,s_*}\frac ma.
 \tag{G.40}
\]

Indeed, `x cot x<=1` on the relevant small positive interval, and
`z_o-z_p=(s_*+3delta_0)/a`.  The carrier cosine tends uniformly to one at
both points because `m epsilon ->0`.  Thus the same shifted packet has an
`exp(O(m/a))`, not an `exp(cm)`, static contrast between the transition cap
and a nearby plateau fibre.

Equation G.40 is not a complete spacetime upper bound for
`mathcal T_L/(M_L^plat)^(2/3)`.  Its role is narrower and decisive: G.8 uses
the central proxy G.36, while the actual plateau contains additional large
values.  Therefore G.8 cannot be substituted into R0.76E as a counterexample
to E.3.  Determining the sharp mode dependence against the full physical
plateau remains open.

## 8. Literature and claim boundary

General heat observability and spectral inequalities quantify propagation
from observation sets, often with costs controlled by geometry and time.
They do not state G.8 for a signed radial derivative, a shrinking collar,
the explicit dyadic packet G.15, and a local spacetime `L^3` denominator.
The proof here imports no observability theorem; it uses the exact Gaussian
heat representation and elementary moment estimates.

The exponential order is consistent with the Turan--Nazarov and Remez
phenomena already cited in R0.76F.  That consistency is not a novelty or
priority claim.

**Closed here:** a nonzero-drift, complete-clock, full signed-flux
`exp(cq)` lower bound relative to the central fibre `H_L`; an explicit
quadratic mode sequence; and the positive normalized obstruction G.38 for
the central-fibre proxy.

**Still open:** a matching lower bound relative to the full physical
plateau mass; the optimal exponential base; arbitrary packets; nonconstant
shear; membership of the constant background in the frozen Version-M
subclass; arbitrary-field E.24; complete Version-M extraction; fixed
deletion; suitable-weak transfer; regularity; and singularity.

The result is analytic.  Finite fixtures audit exact frequency, rational,
clock, and exponent ledgers but do not prove the Gaussian limiting lemma.
No simulation or formal scientific figure is claimed.  **NOT CLAY.**
