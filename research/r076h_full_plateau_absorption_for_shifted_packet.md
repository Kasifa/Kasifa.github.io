# R0.76H -- the full plateau absorbs the shifted-binomial obstruction

## 0. Result and exact boundary

R0.76G constructs a real exact shear whose complete signed collar flux is
exponentially large relative to a central-fibre proxy.  The physical
plateau, however, contains fibres only `O(1/a)` from the positive transition
cap.  This note proves that those fibres absorb the exponential contrast for
that explicit packet over the complete clock.

Retain

\[
 a=\frac{32}{63}L,\qquad
 R=e^{-9L^2/40000},\qquad
 \omega=e^{-2L^2/3969},\qquad
 m=\left\lfloor\frac{a^2}{1024}\right\rfloor,\quad
 q=2m+1,\quad\varepsilon=aR,\quad\beta=\frac1{100}.
 \tag{H.1}
\]

With `y=x_2+aR/2`, use exactly the R0.76G packet and drift

\[
 f_L(x_2)=A\left(2\sin\frac y2\right)^{2m}\cos(3my),\qquad
 B=-\frac{\beta a}{R},\qquad
 F_L(t,x_2)=e^{t\partial_2^2}f_L(x_2-Bt).
 \tag{H.2}
\]

After translating the absolute frozen clock `61R^2--65R^2` to elapsed time,
put

\[
 \begin{aligned}
 G_L(s,z)&=F_L(R^2s,aRz),\\
 \mathcal S_L
 &:=-\beta\int_0^4\!\zeta(s)
 \int_{\mathbb R}W_a(z)|G_L(s,z)|^2\,dzds,\qquad
 W_a(z)=-2\pi az\vartheta(a(|z|-1)).
 \end{aligned}
 \tag{H.3}
\]

Here \(A>0\), \(0\le\vartheta\le1\), and the frozen clock cutoff satisfies
\(\zeta(s)=1\) on \(3<s<4\).

Let the frozen plateau be
`S_(a,R)^plat={x: ||x|/R-a|<=delta_0}` and define

\[
 \begin{aligned}
 M_L^{\rm plat}
 &:=\int_0^{4R^2}\!\int_{\mathcal S_{a,R}^{\rm plat}}
 |F_L(t,x_2)|^3\,dxdt,\qquad
 \mathcal T_L:=\frac{a^2R^3}{2}\mathcal S_L,\\
 p_L^{\rm plat}&:=R^{-2}\omega M_L^{\rm plat},\qquad
 \mathfrak X_L:=\frac\omega R[\mathcal T_L]_+.
 \end{aligned}
 \tag{H.4}
\]

There are constants `C_*,L_*<infinity`, depending only on the frozen
geometry and cutoff, such that for `L>=L_*`,

\[
 \boxed{
 \frac{[\mathcal S_L]_+}{P_L^{2/3}}
 \le C_*\beta a^{2/3}\exp\!\left(C_*\frac ma\right),}
 \qquad
 P_L:=\int_0^4\!\int_{J_{a,p}}|G_L(s,z)|^3\,dzds.
 \tag{H.5}
\]

Here `J_(a,p)` is the inner plateau interval defined in H.9.  Its width is
fixed in the rescaled collar coordinate `r=a(z-1)`, while its `z`-width is
`delta_0/a`.
Consequently,

\[
 \boxed{
 \frac{[\mathcal T_L]_+}{(M_L^{\rm plat})^{2/3}}
 \le C_*\beta a^{4/3}R^{-1/3}
 \exp\!\left(C_*\frac ma\right).}
 \tag{H.6}
\]

The matching lower bound proved in Section 5 shows that the normalized
quotient has the exact rate

\[
 \boxed{
 \lim_{L\to\infty}\frac1{L^2}
 \log\frac{\mathfrak X_L}{(p_L^{\rm plat})^{2/3}}
 =-\frac2{11907}<0.}
 \tag{H.7}
\]

Thus the explicit R0.76G packet is not a full-plateau counterexample even
though `q(L)/L^2 -> 2/3969`.  This does not prove that the `exp(Cq)` upper
loss in R0.76E is removable for arbitrary packets.

## 1. A robust plateau strip adjacent to the cap

Recall \(0<\delta_0<\delta\) and
\(\operatorname{supp}\vartheta\subset(-\delta,\delta)\).  The positive
support of `W_a` obeys

\[
 \mathcal C_{a,+}:=\{z>0:W_a(z)\ne0\}
 \subset\left[1-\frac\delta a,1+\frac\delta a\right].
 \tag{H.8}
\]

Choose the inner plateau strip

\[
 J_{a,p}:=\left[1-\frac{3\delta_0}{a},
                      1-\frac{2\delta_0}{a}\right],qquad
 |J_{a,p}|=\frac{\delta_0}{a}.
 \tag{H.9}
\]

For `w(s,z)=z+beta s+1/2` and all sufficiently large `L`, every
`0<=s<=4`, `z_o in C_(a,+)`, and `z_p in J_(a,p)` satisfy

\[
 \frac75\le w(s,z_o),w(s,z_p)\le\frac85,qquad
 |w(s,z_o)-w(s,z_p)|\le\frac Da,qquad
 D:=\delta+3\delta_0.
 \tag{H.10}
\]

For a fixed scaled coordinate `z`, write the exact dimensionless
`(x_1,x_3)` cross-sectional area as

\[
 \begin{aligned}
 \mathcal A_a(z)
 &:=\pi\left([(a+\delta_0)^2-a^2z^2]_+
             -[(a-\delta_0)^2-a^2z^2]_+\right),\\
 0\le\mathcal A_a(z)&\le4\pi a\delta_0,
 \qquad
 \mathcal A_a(z)=4\pi a\delta_0
 \quad\left(|z|\le1-\frac{\delta_0}{a}\right).
 \end{aligned}
 \tag{H.11}
\]

The physical area is `R^2 A_a(z)`.  The central chart contains the shell
for large frozen `L`.  Using `dx_2=aR dz` and `dt=R^2ds`, H.11 gives the
exact formula and the retained strip lower bound

\[
 M_L^{\rm plat}=aR^5\int_0^4\!\int_{\mathbb R}
 \mathcal A_a(z)|G_L(s,z)|^3\,dzds
 \ge4\pi\delta_0a^2R^5P_L.
 \tag{H.12}
\]

## 2. Uniform comparison with an even Gaussian moment

Let `Z` be standard real Gaussian and, for `0<=s<=4`, define

\[
 \sigma_s:=\frac{\sqrt{2s}}a,qquad
 \mathcal M_{m,s}(w):=\mathbb E|w+\sigma_sZ|^{2m}.
 \tag{H.13}
\]

The exact periodic heat-kernel formula is

\[
 G_L(s,z)=A\,\mathbb E\left[
 \left(2\sin\frac{\varepsilon X}{2}\right)^{2m}
 \cos(3m\varepsilon X)\right],qquad
 X=w(s,z)+\sigma_sZ.
 \tag{H.14}
\]

The global inequalities `|2sin(r/2)|<=|r|` and `|cos r|<=1` imply

\[
 |G_L(s,z)|\le
 A\varepsilon^{2m}\mathcal M_{m,s}(w(s,z)).
 \tag{H.15}
\]

On `|X|<=3`, uniformly in `s` and in `7/5<=w<=8/5`,

\[
 \left(\frac{2\sin(\varepsilon X/2)}{\varepsilon X}\right)^{2m}
 =1+o(1),\qquad
 \cos(3m\varepsilon X)=1+o(1),
 \tag{H.16}
\]

because `m epsilon^2 -> 0` and `m epsilon -> 0`.  The omitted moment is
uniformly negligible: the same Cauchy--Schwarz estimate as in R0.76G gives

\[
 \mathbb E[|X|^{2m};|X|>3]
 \le\left(\frac95\right)^{2m}\sqrt2\,e^{-49a^2/800}
 =o\left(\left(\frac75\right)^{2m}\right).
 \tag{H.17}
\]

Indeed, after division by `(7/5)^(2m)`, the logarithm is at most
`2m log(9/7)-49a^2/800+O(1)`, which tends to minus infinity because
`2m<=a^2/512` and `log(9/7)<2/7`.

Since `M_(m,s)(w)>=w^(2m)` by Jensen, H.14--H.17 give, uniformly on the
same compact `w` interval and for all sufficiently large `L`,

\[
 \left|
 \frac{G_L(s,z)}{A\varepsilon^{2m}}-\mathcal M_{m,s}(w)
 \right|=o(1)\mathcal M_{m,s}(w),\qquad
 \frac12A\varepsilon^{2m}\mathcal M_{m,s}(w)
 \le G_L(s,z)
 \le A\varepsilon^{2m}\mathcal M_{m,s}(w).
 \tag{H.18}
\]

In particular `G_L` is positive there.  Differentiating the even moment and
using Hölder and Jensen yields

\[
 \left|\partial_w\log\mathcal M_{m,s}(w)\right|
 \le2m\,\mathcal M_{m,s}(w)^{-1/(2m)}
 \le\frac{2m}{w}\le\frac{10m}{7}.
 \tag{H.19}
\]

Therefore any `w,w' in [7/5,8/5]` obey

\[
 \frac{\mathcal M_{m,s}(w)}{\mathcal M_{m,s}(w')}
 \le\exp\!\left(\frac{10m}{7}|w-w'|\right).
 \tag{H.20}
\]

This logarithmic moment comparison, rather than the coarser Minkowski
allowance `4sqrt(m)/a`, is the mechanism that sees the `O(1/a)` adjacency.

## 3. The cap is paid by the adjacent plateau strip

Set

\[
 U_L(s):=\sup_{z\in\mathcal C_{a,+}}|G_L(s,z)|,qquad
 Q_L:=\int_0^4U_L(s)^3\,ds.
 \tag{H.21}
\]

Equations H.10, H.18, and H.20 show that, for every `0<=s<=4`,

\[
 U_L(s)
 \le2\exp\!\left(\frac{10D}{7}\frac ma\right)
 \inf_{z\in J_{a,p}}G_L(s,z).
 \tag{H.22}
\]

Cubing, integrating, and using H.9 gives

\[
 P_L\ge\frac{\delta_0}{8a}
 \exp\!\left(-\frac{30D}{7}\frac ma\right)Q_L.
 \tag{H.23}
\]

The positive-cap `L^1` weight is uniformly bounded:

\[
 \int_{\mathcal C_{a,+}}(-W_a(z))\,dz
 \le C_\vartheta,
 \tag{H.24}
\]

because `r=a(z-1)` reduces the integral to a fixed compact interval.  The
positive cap is the only favourable sign in H.3; hence the full negative
cap may only reduce the signed integral, and

\[
 [\mathcal S_L]_+
 \le\beta C_\vartheta\int_0^4U_L(s)^2\,ds.
 \tag{H.25}
\]

Hölder on the time interval of length four gives

\[
 \int_0^4U_L(s)^2\,ds
 \le4^{1/3}Q_L^{2/3}.
 \tag{H.26}
\]

Combining H.23, H.25, and H.26 proves the explicit form of H.5,

\[
 \frac{[\mathcal S_L]_+}{P_L^{2/3}}
 \le C\beta a^{2/3}
 \exp\!\left(\frac{20D}{7}\frac ma\right).
 \tag{H.27}
\]

No cancellation inside the favourable cap is needed for this upper bound.

## 4. Physical scaling and frozen exponent

The exact scale conversion and the plateau lower bound are

\[
 [\mathcal T_L]_+=\frac{a^2R^3}{2}[\mathcal S_L]_+,qquad
 M_L^{\rm plat}\ge4\pi\delta_0a^2R^5P_L.
 \tag{H.28}
\]

Thus H.27 proves H.6.  Directly from the definitions,

\[
 \frac{\mathfrak X_L}{(p_L^{\rm plat})^{2/3}}
 =R^{1/3}\omega^{1/3}
 \frac{[\mathcal T_L]_+}{(M_L^{\rm plat})^{2/3}}
 \le C\beta a^{4/3}\omega^{1/3}
 \exp\!\left(C\frac ma\right).
 \tag{H.29}
\]

Finally,

\[
 \frac{q(L)}{L^2}\longrightarrow\frac2{3969},\qquad
 \frac{m}{aL^2}\longrightarrow0,qquad
 \frac{\log a}{L^2}\longrightarrow0,qquad
 \frac1{L^2}\log\omega^{1/3}=-\frac2{11907}.
 \tag{H.30}
\]

Equations H.29--H.30 prove the upper half of H.7.  The reverse bound, and
positivity of the signed flux for all large `L`, follow from the terminal
boxes below.

## 5. Matching subquadratic bounds for this packet

The even Gaussian moment has the exact nonnegative-coefficient expansion

\[
 \mathcal M_{m,s}(w)
 =\sum_{\ell=0}^m
 \frac{(2m)!}{(2m-2\ell)!\,\ell!}
 \left(\frac{s}{a^2}\right)^\ell w^{2m-2\ell}.
 \tag{H.31}
\]

Set

\[
 s_0:=4-\frac1a,\qquad
 w_*:=\frac32+4\beta=\frac{77}{50},\qquad
 w_0:=w_*-\frac{4\delta_0+\beta}{a},\qquad
 K_0:=\mathcal M_{m,s_0}(w_0).
 \tag{H.32}
\]

Retain the R0.76G positive-subcap constants `s_*`, `h`, and `c_vartheta>0`,
chosen so that
`delta_0<s_*-3h<s_*+3h<delta` and
`vartheta(r)>=c_vartheta` for `|r-s_*|<=3h`.  For large `L`, define the
terminal plateau and positive-cap boxes

\[
 \begin{aligned}
 \mathcal B_p&:=\left[4-\frac1a,4\right]
 \times\left[1-\frac{4\delta_0}{a},
                   1-\frac{3\delta_0}{a}\right],\\
 \mathcal B_+&:=\left[4-\frac1a,4\right]
 \times\left\{z:a(z-1)\in[s_*-h,s_*+h]\right\}.
 \end{aligned}
 \tag{H.33}
\]

Both boxes lie in the compact comparison range of H.18.  On `B_p`, the
plateau cross-section is exactly H.11.  On both boxes, `s>=s_0` and
`w>=w_0`; since every coefficient in H.31 is nonnegative,
`M_(m,s)(w)>=K_0`.  The two box widths are each of order `1/a`, so H.11,
the exact scaling, and H.18 give the lower mass bound below.

For the reverse mass bound, the full plateau has
`|z|<=1+delta_0/a`, hence `|w|<=w_*+delta_0/a`.  Term-by-term comparison in
H.31 gives, uniformly on the full plateau and complete clock,
`M_(m,s)(w)<=exp(Cm/a)K_0<=exp(Ca)K_0`.  The scaled plateau has bounded
`z`-length and cross-sectional area at most `4pi a delta_0`.  Therefore

\[
 cR^5A^3\varepsilon^{6m}K_0^3
 \le M_L^{\rm plat}
 \le Ca^2e^{Ca}R^5A^3\varepsilon^{6m}K_0^3.
 \tag{H.34}
\]

On `B_+`, `zeta=1` almost everywhere, `-W_a>=ca`, and H.18 gives

\[
 \mathcal F_{L,+}
 :=\beta\iint_{\mathcal B_+}(-W_a)G_L^2\,dzds
 \ge c\beta a^{-1}A^2\varepsilon^{4m}K_0^2.
 \tag{H.35}
\]

Define the adverse negative-cap magnitude and retain the R0.76G bound

\[
 \mathcal F_{L,-}
 :=\beta\int_0^4\!\zeta(s)\int_{-\infty}^0
 W_a(z)|G_L(s,z)|^2\,dzds
 \le C\beta A^2\varepsilon^{4m}
 \left(\frac23\right)^{4m},\qquad
 \frac{\mathcal F_{L,-}}{\mathcal F_{L,+}}
 \le Ca\left(\frac{2}{3w_0}\right)^{4m}=o(1),
 \tag{H.36}
\]

where `K_0>=w_0^(2m)` was used.  Thus `S_L>0` for all large `L`.
The lower bound H.35, the absorption H.36, and the positive-cap upper bound
obtained from H.15 and the same termwise comparison yield

\[
 c\beta a^{-1}A^2\varepsilon^{4m}K_0^2
 \le\mathcal S_L
 \le C\beta e^{Ca}A^2\varepsilon^{4m}K_0^2.
 \tag{H.37}
\]

Combining H.34, H.37, and the exact physical scaling gives

\[
 c\beta a^{-1/3}e^{-Ca}R^{-1/3}
 \le\frac{\mathcal T_L}{(M_L^{\rm plat})^{2/3}}
 \le C\beta a^2e^{Ca}R^{-1/3}.
 \tag{H.38}
\]

Since `m/a=O(a)=O(L)`, all factors other than `R` and `omega` in these
bounds are subquadratic on the logarithmic scale.  Hence

\[
 \lim_{L\to\infty}\frac1{L^2}
 \log\frac{\mathcal T_L}{(M_L^{\rm plat})^{2/3}}
 =\frac3{40000},\qquad
 \lim_{L\to\infty}\frac1{L^2}
 \log\frac{\mathfrak X_L}{(p_L^{\rm plat})^{2/3}}
 =-\frac2{11907}.
 \tag{H.39}
\]

This proves H.7 and quantifies exactly how the factor `R^(-1/3)` is
cancelled by the normalization.

## 6. What this closes and what remains open

The theorem is a candidate-killing result.  R0.76G's complete-clock
central-fibre lower bound is correct, but the adjacent plateau strip pays
that same explicit packet at subquadratic logarithmic cost.  The normalized
full-plateau quotient therefore decays at exactly the original strict frozen
rate, even though the packet has a quadratic number of modes.

This does not improve R0.76E's uniform `exp(Cq)` upper bound.  It does not
prove a subexponential coefficient for arbitrary real dyadic packets, nor
does it rule out a different packet whose cap values cannot be compared to
an adjacent plateau strip.  R0.75R uses a different short clock and a much
more sharply localized family; it is not contradicted.

The exact field remains the smooth unforced shear `u=(0,B,F_L(t,x_2))`.
The constant background has not been shown to lie in the frozen mean-zero,
inversion-paired Version-M subclass.  Arbitrary packets, nonconstant shear,
arbitrary-field E.24, complete Version-M extraction, fixed deletion,
suitable-weak transfer, regularity, and singularity remain open.

The proof is analytic and uses only the exact Gaussian representation,
Hölder, Jensen, and the frozen plateau geometry.  Finite fixtures can audit
the rational, frequency, distance, and exponent ledgers but do not prove the
uniform moment comparison.  No simulation or formal scientific figure is
claimed.  **NOT CLAY.**
