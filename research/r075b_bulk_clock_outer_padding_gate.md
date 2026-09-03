# R0.75B -- bulk complete-clock extraction and the outer-padding gate

## 0. Result and exact boundary

R0.75A closes endpoint-only temporal focusing for the W remote kinetic
witness.  Its minimum next proposition asks for the **complete** clock at
that remote coordinate.  The present note separates this request into a
paid part and one precise unresolved collar.

Let

\[
 k=k_2-1,\qquad L=L_2,\qquad
 \omega=\gamma_k=\Gamma^{1/4},\qquad
 pL=2^{k_2}.
 \tag{B.1}
\]

For every smooth periodic inversion-paired total common-shear field in the
frozen exact family (so the Version-M mollified trajectory is identically
zero)

\[
 u=(F,b,0),\qquad
 (\partial_t+b\partial_2-\Delta_{23})F=0,
 \qquad \partial_tb-\partial_3^2b=0,
 \tag{B.2}
\]

the endpoint energy and accumulated physical dissipation localized away
from the outer transition collar of the frozen shell cutoff obey

\[
 \boxed{
 K_{k,R}^{\rm safe}(t_2)
 \le C L R^{-1}\omega^{5/6}(P_R^M)^{2/3}.}
 \tag{B.3}
\]

For the frozen R0.74Y parameters,

\[
 \limsup_{L\to\infty}\frac1{L^2}
 \log\bigl(LR^{-1}\omega^{5/6}\bigr)
 =\frac\rho4-\frac5{24}c_\gamma
 =-\frac{92837}{476280000}<0.
 \tag{B.4}
\]

Thus the complete **safe subclock** is asymptotically paid by
\((P_R^M)^{2/3}\).  This includes its endpoint row and the full
time-accumulated smooth dissipation row; it is stronger than endpoint
persistence on that subregion.

The outer transition collar is different because the scale-\(2R\) payment
may carry only the same weight \(\omega\), rather than \(\omega^{1/4}\).
Nevertheless, its **endpoint row is still paid**.  A terminal \(R^3\)
local-energy dichotomy and the collar's smaller spatial volume give

\[
 (P_R^M)^{2/3}
 \ge cH_{k,R}^{\rm out}(t_2)
 R^{2/3}\omega^{-1/3}L^{-2/3},
 \tag{B.5}
\]

whose exponential gain is

\[
 \frac{c_\gamma}{12}-\frac\rho6
 =\frac{4279}{238140000}>0.
 \tag{B.6}
\]

Only the **full-time accumulated dissipation** in that collar remains.  The
coarse full-window estimate has coefficient

\[
 D_{k,R}^{\rm out}
 \le C L^{2/3}R^{-1}\omega^{1/3}(P_R^M)^{2/3},
 \qquad
 \frac\rho4-\frac{c_\gamma}{12}
 =\frac{27163}{476280000}>0.
 \tag{B.6a}
\]

The positive sign is a **failure of this estimate**, not a counterexample
to complete-clock extraction.  No solution realizing the upper ledger
sharply is constructed.  The exact status is

\[
\boxed{
\begin{gathered}
\textbf{SAFE COMPLETE SUBCLOCK: PAID;}\\
\textbf{INNER PADDING: PAID BY A NO-WORSE INWARD WEIGHT;}\\
\textbf{OUTER-COLLAR ENDPOINT: PAID;}\\
\textbf{OUTER-COLLAR ACCUMULATED DISSIPATION: OPEN;}\\
\textbf{FULL }K_{k,R}\textbf{ AND FIXED DELETION: NOT PROVED.}
\end{gathered}}
\tag{B.7}
\]

This is an exact smooth-family Caccioppoli extraction theorem and a
fail-closed route diagnosis.  It is not a theorem for arbitrary suitable
weak solutions, not a singularity or regularity result, and
\(\mathbf{NOT\ CLAY}\).

<!-- R075B_SAFE_COMPLETE_SUBCLOCK_PAID -->
<!-- R075B_OUTER_PADDING_ENDPOINT_PAID -->
<!-- R075B_OUTER_PADDING_DISSIPATION_OPEN -->
<!-- R075B_METHOD_FAILURE_NOT_COUNTEREXAMPLE -->
<!-- R075B_FULL_CLOCK_OPEN -->
<!-- R075B_NOT_CLAY -->

## 1. Frozen sources and geometry

The note is bound to these local snapshots.

| source | SHA-256 | use |
|---|---|---|
| `research/r074h_collar_flux_two_regime_closure.md` | `8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1` | shell cutoffs, doubled-radius payment, and weighted Holder ledger |
| `research/r074p_temporal_observable_triage.md` | `a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867` | completed clock and time cutoff |
| `research/r074u_intrinsic_certified_residence.md` | `e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99` | exact common shear and bound on \(B\) |
| `research/r075a_spectral_persistence_payment_dichotomy.md` | `f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388` | total-field equation and frozen exponents |

Use the nonperiodized annuli

\[
 A_j(R)=\{2^jR\le |x|<2^{j+1}R\}
 \tag{B.8}
\]

and smooth cutoffs from R0.74H,

\[
 \psi_j^R=1\ \hbox{on }A_j(R),\qquad
 \operatorname {supp}\psi_j^R
 \subset\{\operatorname {dist}(x,A_j(R))\le R/8\},
 \tag{B.9}
\]

with first and second derivative bounds \(CR^{-1}\) and \(CR^{-2}\).
Their periodic lifts are \(\Psi_j^R\).  Since the remote shell lies in the
central chart, the local estimates below may be proved for one lift and
then summed over the nonnegative periodic copies.

The exact annular identity is

\[
 A_k(R)=A_{k-1}(2R),\qquad
 W_{2R}\ge\gamma_{k-1}=\omega^{1/4}
 \quad\hbox{on }A_k(R).
 \tag{B.10}
\]

The support padding in (B.9) has two sides.  Its inward part meets only
scale-\(2R\) shells with weights at least \(\gamma_{k-1}\).  Its outward
part meets \(A_k(2R)\), whose weight is \(\gamma_k=\omega\).  This one-index
distinction is the entire source of the sign change between (B.4) and
(B.6).

Let \(r_k^+=2^{k+1}R=pLR\) be the outer radius.  Choose a fixed smooth
\(0\le\chi_k^R\le\Psi_k^R\) which equals \(\Psi_k^R\) outside the outer
collar

\[
 \mathcal C_{k,R}^{\rm out}
 :=\{x:\bigl||x|-r_k^+\bigr|<R/4\}
 \tag{B.11}
\]

and vanishes before reaching that collar's outer half.  It can be chosen
with

\[
 |\nabla\chi_k^R|\le CR^{-1},\qquad
 |\Delta\chi_k^R|\le CR^{-2},
 \tag{B.12}
\]

and with support contained in the union of scale-\(2R\) shells having
weight at least \(\omega^{1/4}\).  The complementary clock contribution is
covered by a cutoff \(\xi_k^R\) supported in a fixed enlargement of
\(\mathcal C_{k,R}^{\rm out}\), with the same derivative bounds and
\(\Psi_k^R\le\chi_k^R+\xi_k^R\).  Only the inequalities
\(0\le\chi,\xi\le C\) and finite overlap are used.

## 2. Time-cutoff Caccioppoli identity

Let \(s_R=61R^2\), \(t_0=65R^2\), and let \(\eta_R\) be the frozen
nondecreasing cutoff satisfying

\[
 \eta_R=0\ \hbox{near }s_R,\qquad
 \eta_R=1\ \hbox{on }I_R=(64R^2,65R^2),\qquad
 |\eta_R'|\le CR^{-2}.
 \tag{B.13}
\]

Take \(t_2=t_0\), interpreted by smooth continuity from below.  For any
fixed smooth nonnegative spatial cutoff \(\chi\), multiply the first
equation in (B.2) by \(\eta_R\chi F\).  Integration by parts gives

\[
\begin{aligned}
 &\frac12\int\chi|F(t_2)|^2
 +\int_{s_R}^{t_2}\!\int\eta_R\chi|\nabla_{23}F|^2\\
 &\qquad=
 \frac12\int_{s_R}^{t_2}\!\int
 \bigl[\eta_R'\chi+\eta_R\Delta_{23}\chi
       +\eta_R b\,\partial_2\chi\bigr]|F|^2.
\end{aligned}
\tag{B.14}
\]

There is no initial term because \(\eta_R\) vanishes near \(s_R\).  The
transport sign is plus on the right:

\[
 -\int\eta_R\chi bF\partial_2F
 =\frac12\int\eta_Rb\,\partial_2\chi\,|F|^2.
 \tag{B.15}
\]

Similarly, because \(b\) solves the one-dimensional heat equation,

\[
\begin{aligned}
 &\frac12\int\chi|b(t_2)|^2
 +\int_{s_R}^{t_2}\!\int\eta_R\chi|\partial_3b|^2\\
 &\qquad=
 \frac12\int_{s_R}^{t_2}\!\int
 [\eta_R'\chi+\eta_R\partial_3^2\chi]|b|^2.
\end{aligned}
\tag{B.16}
\]

The R0.74U platform bound and the maximum principle give

\[
 |b|\le B\le\frac1{96R^2}.
 \tag{B.17}
\]

For \(R\le1\), (B.12)--(B.13) therefore imply

\[
 |\eta_R'\chi|+|\eta_R\Delta_{23}\chi|
 +|\eta_Rb\partial_2\chi|
 \le CR^{-3}\mathbf1_{\operatorname {supp}\chi},
 \tag{B.18}
\]

where the deliberately crude \(R^{-3}\) also dominates every \(R^{-2}\)
term.  Adding (B.14) and (B.16), and multiplying by \(\omega/R\), proves

\[
 \boxed{
 K^{\chi}_{k,R}(t_2)
 \le C\omega R^{-4}
 \int_{I_{2R}}\!\int_{\operatorname {supp}\chi}|u|^2.}
 \tag{B.19}
\]

Here

\[
\begin{aligned}
 K^{\chi}_{k,R}(t_2):={}&
 \frac\omega{2R}\int\chi|u(t_2)|^2\\
 &+\frac\omega R\int_{s_R}^{t_2}\!\int
 \eta_R\chi\bigl(|\nabla_{23}F|^2+|\partial_3b|^2\bigr).
\end{aligned}
\tag{B.20}
\]

For a smooth common-shear solution this is exactly the localized endpoint
plus physical-dissipation part of the defect-completed clock; the anomalous
defect is zero.  Taking \(\chi=\chi_k^R\) defines
\(K_{k,R}^{\rm safe}\).  Since \(0\le\chi_k^R\le\Psi_k^R\), it is a
nonnegative subclock of \(K_{k,R}\), not an upper bound for that full clock.

## 3. Safe-region conversion to the cubic payment

The safe support has spatial volume at most

\[
 |\operatorname {supp}\chi_k^R|
 \le C(2^{k+1}R)^3\le CL^3R^3.
 \tag{B.21}
\]

Since \(|I_{2R}|=4R^2\), its spacetime volume is at most \(CL^3R^5\).
Spacetime Holder gives

\[
 \int_{I_{2R}}\!\int_{\operatorname {supp}\chi_k^R}|u|^2
 \le CL R^{5/3}
 \left(
 \int_{I_{2R}}\!\int_{\operatorname {supp}\chi_k^R}|u|^3
 \right)^{2/3}.
 \tag{B.22}
\]

By (B.10), nonnegativity of the exterior velocity row, and the fact that
\((2R)^{-2}\asymp R^{-2}\),

\[
 \int_{I_{2R}}\!\int_{\operatorname {supp}\chi_k^R}|u|^3
 \le CR^2\omega^{-1/4}P_R^M.
 \tag{B.23}
\]

Substituting (B.22)--(B.23) into (B.19) yields

\[
\begin{aligned}
 K_{k,R}^{\rm safe}(t_2)
 &\le C\omega R^{-4}
       LR^{5/3}(R^2\omega^{-1/4}P_R^M)^{2/3}\\
 &\le CLR^{-1}\omega^{5/6}(P_R^M)^{2/3},
\end{aligned}
\tag{B.24}
\]

which is (B.3).

For the remote coordinate,

\[
 \omega=\exp\!\left(-\frac{c_\gamma}{4}L^2\right),
 \qquad
 \log(1/R)=\frac\rho4L^2,
 \qquad
 c_\gamma=\frac8{3969},\quad \rho=\frac9{10000}.
 \tag{B.25}
\]

Therefore

\[
 \frac\rho4-\frac5{24}c_\gamma
 =-\frac{92837}{476280000}<0,
 \tag{B.26}
\]

and the polynomial factor \(L\) does not affect the strict sign.  This
proves (B.4).

## 4. The outer transition collar

The enlarged outer collar has spatial volume

\[
 |\operatorname {supp}\xi_k^R|
 \le C(2^{k+1}R)^2R\le CL^2R^3.
 \tag{B.27}
\]

On its outward half, the only uniform scale-\(2R\) lower weight is

\[
 W_{2R}\ge\gamma_k=\omega.
 \tag{B.28}
\]

This loses the fourth-root shift, but the endpoint and the full accumulated
dissipation have different time geometries and must not be merged.

### 4.1 The endpoint row is still paid

Let

\[
 E_{\rm out}(t):=\int\xi_k^R|u(t)|^2,
 \qquad
 M_{\rm out}(t):=\int_{\operatorname {supp}\xi_k^R}|u(t)|^2,
 \tag{B.29}
\]

and let \(J_*=[t_2-c_0R^3,t_2]\subset I_{2R}\), with fixed sufficiently
small \(c_0>0\).  Applying the unweighted-in-time versions of
(B.14)--(B.16), dropping the nonnegative gradient terms, and using (B.17)
gives

\[
 E_{\rm out}'(t)\le CR^{-3}M_{\rm out}(t).
 \tag{B.30}
\]

The same two exhaustive cases as R0.75A now yield

\[
 X_{\rm out}:=\int_{J_*}M_{\rm out}(t)\,dt
 \ge cE_{\rm out}(t_2)R^3.
 \tag{B.31}
\]

Indeed, either \(E_{\rm out}\ge E_{\rm out}(t_2)/2\) throughout \(J_*\),
or integrating (B.30) from a time where it is smaller than one half forces
(B.31).

By (B.27), the spacetime tube has volume at most \(CL^2R^6\).  Holder and
(B.31) imply

\[
 \int_{J_*}\!\int_{\operatorname {supp}\xi_k^R}|u|^3
 \ge cE_{\rm out}(t_2)^{3/2}R^{3/2}L^{-1}.
 \tag{B.32}
\]

Using (B.28) in the nonnegative exterior velocity row gives

\[
 P_R^M
 \ge c\omega E_{\rm out}(t_2)^{3/2}R^{-1/2}L^{-1}.
 \tag{B.33}
\]

Define the outer-collar endpoint cover

\[
 H_{k,R}^{\rm out}(t_2)
 :=\frac\omega{2R}E_{\rm out}(t_2).
 \tag{B.34}
\]

Then

\[
 \boxed{
 (P_R^M)^{2/3}
 \ge cH_{k,R}^{\rm out}(t_2)
 R^{2/3}\omega^{-1/3}L^{-2/3}.}
 \tag{B.35}
\]

Its exact exponential gain is

\[
 \frac{c_\gamma}{12}-\frac\rho6
 =\frac{4279}{238140000}>0.
 \tag{B.36}
\]

Thus the same-weight collar endpoint is paid, although with a much smaller
strict margin than the safe subclock.  Since
\(\Psi_k^R\le\chi_k^R+\xi_k^R\), (B.24) and (B.35) control the full
endpoint row of \(K_{k,R}(t_2)\).

### 4.2 Only accumulated outer-collar dissipation remains

Put

\[
 D_{k,R}^{\rm out}
 :=\frac\omega R\int_{I_{2R}}\!\int
 \eta_R\xi_k^R
 \bigl(|\nabla_{23}F|^2+|\partial_3b|^2\bigr).
 \tag{B.37}
\]

The full-window Caccioppoli estimate (B.19), the spacetime volume
\(CL^2R^5\), and (B.28) give

\[
 \boxed{
 D_{k,R}^{\rm out}
 \le CL^{2/3}R^{-1}\omega^{1/3}(P_R^M)^{2/3}.}
 \tag{B.38}
\]

The coefficient has rate

\[
 \frac\rho4-\frac{c_\gamma}{12}
 =\frac{27163}{476280000}>0.
 \tag{B.39}
\]

Therefore (B.38) cannot be absorbed uniformly with the frozen exponents.
This does not show that the clock ratio diverges: Holder, Caccioppoli, and
the worst shell weight need not all be saturated by one exact forward
solution.

There is a sharper temporal formulation.  Cover \(I_{2R}\) by \(N\le
CR^{-1}\) consecutive \(R^3\)-blocks with fixed-overlap enlargements.
Let

\[
 p_m:=R^{-2}\omega
 \int_{\widetilde J_m}\!\int_{\operatorname {supp}\xi_k^R}|u|^3,
 \qquad
 \sum_mp_m\le CP_R^M,
 \tag{B.40}
\]

and define the effective \(2/3\)-packing number

\[
 N_{\rm eff}:=
 \frac{\bigl(\sum_mp_m^{2/3}\bigr)^3}
      {\bigl(\sum_mp_m\bigr)^2},
 \qquad 1\le N_{\rm eff}\le N
 \tag{B.41}
\]

when \(\sum_mp_m>0\), with \(N_{\rm eff}=1\) otherwise.  A time cutoff on
each enlarged block, equal to one on the block being charged, gives

\[
 D_{k,R}^{\rm out}
 \le CL^{2/3}R^{-2/3}\omega^{1/3}
       N_{\rm eff}^{1/3}(P_R^M)^{2/3}.
 \tag{B.42}
\]

For one effective block the coefficient has the favorable rate

\[
 \frac\rho6-\frac{c_\gamma}{12}
 =-\frac{4279}{238140000}<0.
 \tag{B.43}
\]

Consequently a sufficient temporal-packing condition is

\[
 \boxed{
 \limsup_{L\to\infty}\frac{\log N_{\rm eff}}{L^2}
 <3\left(\frac{c_\gamma}{12}-\frac\rho6\right)
 =\frac{4279}{79380000}.}
 \tag{B.44}
\]

The worst count \(N\asymp R^{-1}\) recovers the unfavorable full-window
rate (B.39).  Thus the remaining issue is not endpoint persistence; it is
the effective number of short time blocks carrying outer-collar
dissipation.

## 5. Minimum next proposition

The next theorem must decide one of the following mutually testable
statements.

1. **Outer-dissipation packing.**  Prove (B.44), or directly prove

   \[
    D_{k,R}^{\rm out}\le C(P_R^M)^{2/3},
    \tag{B.45}
   \]

   for every admissible finite inversion-paired common-shear correction
   family.

2. **Exact counterexample.**  Construct a forward smooth periodic
   common-shear solution which spreads effective outer-collar dissipation
   over enough \(R^3\)-blocks to violate (B.44) and makes
   \(D_{k,R}^{\rm out}/(P_R^M)^{2/3}\to\infty\), including all initial,
   central, pressure, harmonic, and periodic-copy payment rows.

Until one of these is proved, the correct conclusion is

\[
 \boxed{
 \text{A.63 reduces to temporal packing of outer-collar dissipation.}}
 \tag{B.46}
\]

No strip lower bound has been used as a whole-shell upper bound.  No
bounded literature search or finite certificate can decide (B.45).  Full
\(K\), fixed deletion, arbitrary suitable weak solutions, and all Clay
consequences remain open.  \(\mathbf{NOT\ CLAY}\).
