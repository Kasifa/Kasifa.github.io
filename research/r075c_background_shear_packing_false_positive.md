# R0.75C -- background-shear packing false positive and paid dissipation

## 0. Result and boundary

R0.75B reduces its remaining full-clock question to the accumulated
dissipation in the outer transition collar.  Its blockwise estimate gives a
sufficient condition in terms of the effective cubic packing number
\(N_{\rm eff}\).  The present note tests whether that condition can be the
right universal next theorem.

It cannot.  Already for the saturation shear with no passive packet,

\[
 u^{\rm sh}=(0,b,0),\qquad
 b(t,x_3)=B\theta_R(t,x_3),
 \qquad \theta_R=e^{t\partial_3^2}g_R,
 \tag{C.1}
\]

the block payments in the outer collar are comparable on all
\(N\asymp R^{-1}\) blocks.  Therefore

\[
 N_{\rm eff}^{\rm sh}\asymp N\asymp R^{-1},
 \qquad
 \lim_{L\to\infty}\frac{\log N_{\rm eff}^{\rm sh}}{L^2}
 =\frac\rho4.
 \tag{C.2}
\]

This violates the sufficient R0.75B threshold by the exact amount

\[
 \frac\rho4-\frac{4279}{79380000}
 =\frac{27163}{158760000}>0.
 \tag{C.3}
\]

Nevertheless the corresponding accumulated shear dissipation is paid:

\[
 \boxed{
 D_{k,R}^{{\rm out},b}
 \le C\omega^{1/3}L^{-1/3}(P_R^M)^{2/3}
 =o\bigl((P_R^M)^{2/3}\bigr).}
 \tag{C.4}
\]

Thus a large \(N_{\rm eff}\) computed from the **total velocity cubic row**
is a false positive: it can count a low-frequency background which is spread
across every time block but whose gradient cost is still cheaply paid.  The
universal form of (B.44) is **DISPROVED** inside the exact smooth family;
the direct outer-dissipation estimate (B.45) is neither proved nor
disproved.

After removing the paid shear row, the only remaining term is

\[
 D_{k,R}^{{\rm out},F}
 :=\frac\omega R\int_{I_{2R}}\!\int
 \eta_R\xi_k^R|\nabla_{23}F|^2.
 \tag{C.5}
\]

This is a route-pruning lemma for one explicit smooth periodic solution and
a rigorous reduction for the exact common-shear family.  It is not a theorem
for arbitrary suitable weak solutions, not a counterexample to the desired
complete-clock estimate, and \(\mathbf{NOT\ CLAY}\).

<!-- R075C_UNIVERSAL_NEFF_THRESHOLD_DISPROVED -->
<!-- R075C_BACKGROUND_SHEAR_DISSIPATION_PAID -->
<!-- R075C_TOTAL_CUBIC_PACKING_FALSE_POSITIVE -->
<!-- R075C_PASSIVE_DISSIPATION_OPEN -->
<!-- R075C_NOT_CLAY -->

## 1. Frozen setting

The note is bound to the following local snapshots.

| source | SHA-256 | use |
|---|---|---|
| `research/r074q_common_shear_multipacket_gate.md` | `60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695` | exact common-shear solution and zero Version-M path |
| `research/r074u_intrinsic_certified_residence.md` | `e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99` | saturation shear and calibration bounds |
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | outer cutoff, block payment, and sufficient packing threshold |

Keep the frozen parameters

\[
 r=r_k^+=pLR,\qquad p=\frac{32}{63},\qquad
 \omega=\exp\!\left(-\frac{c_\gamma}{4}L^2\right),
 \qquad R=\exp\!\left(-\frac\rho4L^2\right),
 \tag{C.6}
\]

where

\[
 c_\gamma=\frac8{3969},\qquad \rho=\frac9{10000}.
 \tag{C.7}
\]

Let

\[
 g_R(x_3)=\sigma\!\left(\frac{\sin x_3}{16R}\right),
 \qquad \theta_R(t)=e^{t\partial_3^2}g_R,
 \tag{C.8}
\]

with the frozen smooth odd saturation profile \(\sigma\).  The calibration
in R0.74U gives

\[
 \frac1{128R^2}\le B
 \le\frac1{128(1-\varepsilon_1)R^2},
 \qquad \varepsilon_1<\frac14.
 \tag{C.9}
\]

The field (C.1) is smooth, periodic, mean zero, inversion odd, and solves the
unforced three-dimensional Navier--Stokes equations with pressure zero.  The
even mollifier therefore gives

\[
 X_R(t)=a_R(t)=0.
 \tag{C.10}
\]

Let \(\xi_k^R\) be the R0.75B outer-collar cutoff.  Its support lies in a
fixed enlargement of the spherical collar of radius \(r\) and thickness
\(O(R)\), and

\[
 |\operatorname {supp}\xi_k^R|\le CL^2R^3,
 \qquad W_{2R}\ge\omega
 \quad\hbox{on }\operatorname {supp}\xi_k^R.
 \tag{C.11}
\]

## 2. A fixed positive cap inside the collar

The particular \(\chi/\xi\) partition used in R0.75B may be chosen so that
\(\xi_k^R=\Psi_k^R=1\) on a radial subcollar of thickness \(cR\) immediately
inside \(r\).  Intersect that subcollar with the upper angular band

\[
 \frac r4\le x_3\le\frac r2
 \tag{C.12}
\]

in the central lift, and call the resulting set \(S_{k,R}\).  Elementary
spherical-shell geometry gives

\[
 |S_{k,R}|\ge c r^2R\ge cL^2R^3.
 \tag{C.13}
\]

For \(x_3\) in (C.12), its distance from both transition sets of the periodic
saturation datum is at least \(cLR\).  The periodic heat-kernel tail estimate,
uniformly for \(61R^2\le t\le65R^2\), gives

\[
 \theta_R(t,x_3)\ge1-Ce^{-cL^2}\ge\frac12
 \tag{C.14}
\]

for all sufficiently large frozen \(L\).  Consequently

\[
 |b(t,x_3)|\ge\frac B2
 \quad\hbox{on }[61R^2,65R^2]\times S_{k,R}.
 \tag{C.15}
\]

Only this fixed positive cap is used for lower bounds.  No assertion is made
that the shear is constant on the whole collar.

## 3. The total-cubic packing condition fails

Partition

\[
 I_{2R}=(61R^2,65R^2)
 \tag{C.16}
\]

into consecutive blocks of length comparable to \(R^3\), with the
fixed-overlap enlargements \(\widetilde J_m\) of R0.75B.  Then

\[
 cR^{-1}\le N\le CR^{-1},
 \qquad cR^3\le|\widetilde J_m|\le CR^3.
 \tag{C.17}
\]

For the shear-only field define exactly the R0.75B block payment

\[
 p_m^{\rm sh}:=R^{-2}\omega
 \int_{\widetilde J_m}\!\int_{\operatorname {supp}\xi_k^R}|b|^3.
 \tag{C.18}
\]

The upper bounds in (C.9), (C.11), and (C.17) give

\[
 p_m^{\rm sh}\le
 C R^{-2}\omega B^3(L^2R^3)R^3
 \le C\omega L^2R^{-2}.
 \tag{C.19}
\]

The lower bounds (C.9), (C.13), (C.15), and (C.17) give the reverse estimate

\[
 p_m^{\rm sh}\ge
 c R^{-2}\omega B^3(L^2R^3)R^3
 \ge c\omega L^2R^{-2}.
 \tag{C.20}
\]

Hence all \(p_m^{\rm sh}\) are comparable to the same positive number.  If

\[
 N_{\rm eff}^{\rm sh}
 =\frac{\bigl(\sum_m(p_m^{\rm sh})^{2/3}\bigr)^3}
        {\bigl(\sum_mp_m^{\rm sh}\bigr)^2},
 \tag{C.21}
\]

then (C.19)--(C.20) imply

\[
 cN\le N_{\rm eff}^{\rm sh}\le CN.
 \tag{C.22}
\]

Using (C.6)--(C.7),

\[
 \lim_{L\to\infty}\frac{\log N_{\rm eff}^{\rm sh}}{L^2}
 =\lim_{L\to\infty}\frac{\log R^{-1}}{L^2}
 =\frac\rho4=\frac9{40000}.
 \tag{C.23}
\]

The sufficient threshold in (B.44) is \(4279/79380000\), and

\[
 \frac9{40000}-\frac{4279}{79380000}
 =\frac{27163}{158760000}>0.
 \tag{C.24}
\]

Therefore (B.44) is false as a universal statement even in the smooth
inversion-paired common-shear class.

## 4. The counted shear dissipation is still paid

For every fixed \(x_3\), the two-dimensional cross-section of the enlarged
spherical collar satisfies

\[
 \left|\left\{(x_1,x_2):(x_1,x_2,x_3)
 \in\operatorname {supp}\xi_k^R\right\}\right|
 \le C rR\le CLR^2.
 \tag{C.25}
\]

The saturation data have uniformly bounded one-dimensional total variation:

\[
 \|\partial_3g_R\|_{L^1(\mathbb T)}\le C_\sigma.
 \tag{C.26}
\]

Indeed, \(\sigma'\) is supported where \(|\sin x_3|\lesssim R\); a change of
variable on the two transition intervals removes the factor \(R^{-1}\).
The periodic heat kernel \(K_t^{\rm per}\) obeys

\[
 \|K_t^{\rm per}\|_{L^2(\mathbb T)}^2\le Ct^{-1/2},
 \qquad 0<t\le1.
 \tag{C.27}
\]

Since \(\partial_3\theta_R=K_t^{\rm per}*\partial_3g_R\), Young's inequality
gives

\[
 \|\partial_3\theta_R(t)\|_2^2
 \le Ct^{-1/2}\|\partial_3g_R\|_1^2
 \le Ct^{-1/2}.
 \tag{C.28}
\]

It follows that

\[
 \int_{61R^2}^{65R^2}
 \|\partial_3\theta_R(t)\|_2^2\,dt
 \le CR.
 \tag{C.29}
\]

Using \(0\le\eta_R,\xi_k^R\le C\), (C.25), and (C.29), the shear part of
the outer accumulated dissipation satisfies

\[
\begin{aligned}
 D_{k,R}^{{\rm out},b}
 &:=\frac\omega R\int_{I_{2R}}\!\int
     \eta_R\xi_k^R|\partial_3b|^2\\
 &\le C\frac\omega R (LR^2)B^2
      \int_{61R^2}^{65R^2}
      \|\partial_3\theta_R(t)\|_2^2\,dt\\
 &\le C\omega LR^2B^2.
\end{aligned}
\tag{C.30}
\]

On the other hand, the nonnegative scale-\(2R\) exterior velocity row in
\(P_R^M\), restricted to the cap in (C.13), gives

\[
\begin{aligned}
 P_R^M
 &\ge cR^{-2}\omega
   \int_{61R^2}^{65R^2}\!\int_{S_{k,R}}|b|^3\\
 &\ge c\omega B^3L^2R^3.
\end{aligned}
\tag{C.31}
\]

The same lower bound remains valid after adding any passive component
\(F\), because pointwise
\((F^2+b^2)^{3/2}\ge |b|^3\).  Thus the shear-dissipation payment proved
below is uniform over the exact family with this frozen common shear, not
only over the test field \(F=0\).

Therefore

\[
 (P_R^M)^{2/3}
 \ge c\omega^{2/3}B^2L^{4/3}R^2,
 \tag{C.32}
\]

and division of (C.30) by (C.32) proves

\[
 \frac{D_{k,R}^{{\rm out},b}}{(P_R^M)^{2/3}}
 \le C\omega^{1/3}L^{-1/3}\longrightarrow0.
 \tag{C.33}
\]

This proves (C.4).  The large block count in (C.22) measures persistence of
the low-frequency amplitude \(|b|^3\), whereas (C.30) measures its much more
localized gradient.  The mismatch is structural, not a defect in the exact
fraction arithmetic of R0.75B.

## 5. Corrected next gate

For a general exact common-shear field \(u=(F,b,0)\), nonnegativity gives

\[
 D_{k,R}^{\rm out}
 =D_{k,R}^{{\rm out},F}+D_{k,R}^{{\rm out},b}.
 \tag{C.34}
\]

The second term is paid by (C.4) for the frozen saturation shear.  The
minimum unresolved proposition is consequently

\[
 \boxed{
 D_{k,R}^{{\rm out},F}
 \stackrel{?}{\le}C(P_R^M)^{2/3}.}
 \tag{C.35}
\]

A replacement packing observable must see the passive gradient or its
frequency scale.  It cannot be formed from the total \(|u|^3\) block masses
alone, because those masses include the persistent paid shear exhibited
above.  Two admissible next moves are:

1. derive a frequency-sensitive block estimate for \(F\) from the exact
   passive advection--diffusion semigroup; or
2. construct an exact forward passive family whose outer gradient occupies
   enough short blocks and whose complete Version-M payment remains too
   small.

No finite arithmetic certificate or bounded literature search decides
(C.35).  Full \(K\), fixed deletion, arbitrary suitable weak solutions, and
every regularity consequence remain open.

\[
 \boxed{\textbf{TOTAL-CUBIC PACKING REJECTED; PASSIVE DISSIPATION OPEN; NOT CLAY.}}
 \tag{C.36}
\]
