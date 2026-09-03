# R0.74X — three-packet fixed-deletion gate

## 0. Decision and exact status

This note tests the smallest apparent repair of the R0.74W obstruction.
Replace the frozen two-packet common-shear field by three packets at

\[
k_2=k_1+1,\qquad k_3=k_1+2,
\qquad L_2=2L_1,\qquad L_3=4L_1.
\tag{X.1}
\]

There are two different conclusions.

1. The three-packet extension is an exact smooth periodic unforced
   Navier--Stokes solution.  Under the natural outermost-chart condition
   and the inherited U-reserve, packets \(2\) and \(3\) both satisfy the
   R0.74W relative-survival estimate.  All inversion, cross-packet, and
   periodic-copy errors are exponentially smaller after the true
   amplitudes are inserted.  Consequently,

   \[
   \frac{K_{k_1,R}(\tau_2)}{T_*}\longrightarrow\infty,
   \qquad
   \frac{K_{k_2,R}(\tau_3)}{T_*}\longrightarrow\infty.
   \tag{X.2}
   \]

   The times may be different.  They may also be chosen equal.

2. Equation (X.2) disproves a matching
   \(\mathfrak L^K_{1,R}=O(T_*)\) statement, but it does not disprove the
   actual fixed-deletion gate.  The latter is normalized by
   \((P_R^M)^{2/3}\), not by \(T_*\).  The outer packet alone forces an
   exterior velocity-cubic payment whose exponent is much larger than
   either W-type strip witness.  Thus the proposed three-packet argument
   stops at a strict payment-normalization blocker.

The verdict is therefore:

\[
\boxed{
\begin{gathered}
\textbf{THREE-PACKET TWO-COORDINATE ENDPOINT OBSTRUCTION: PROVED,}\\
\textbf{ACTUAL FIXED-DELETION GATE COUNTEREXAMPLE: NOT PROVED,}\\
\textbf{EQUAL-TARGET W-STRIP ROUTE: NO-GO BY CUBIC PAYMENT.}
\end{gathered}}
\tag{X.3}
\]

No whole-shell upper bound, positive-variation upper bound, scale
contraction, regularity, or singularity theorem is claimed.
\(\mathbf{NOT\ CLAY}\).

## 1. Frozen sources and the deletion quantifier

The local source hashes used here are:

| source | SHA-256 | use |
|---|---|---|
| research/r074p_temporal_observable_triage.md | a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867 | canonical nonnegative shell clock |
| research/r074q_common_shear_multipacket_gate.md | 60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695 | exact finite-packet common-shear NSE solution |
| research/r074q_relaxed_multipacket_cubic_obstruction.md | ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d | target-lobe cross margins and exterior cubic payment |
| research/r074s_fixed_deletion_simultaneous_height.md | 305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1 | exact fixed-deletion definition |
| research/r074t_schedule_invariant_dwell_coercivity.md | 8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd | different-time pigeonhole |
| research/r074u_intrinsic_certified_residence.md | e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99 | common-shear corridor and reserve |
| research/r074v_completed_clock_upper_route.md | 031c9ca8600c776d9897b247147bc4ecebff68a71e6b3c5906b310463d5b627c | completed-clock endpoint ledger |
| research/r074w_remote_adjacent_inward_comparison.md | d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10 | remote-strip dichotomy |

The r074v hash displayed in the table is intentionally rechecked below;
the full recomputed value is

\[
\texttt{031c9ca8600c776d9897b247147bc4ecebff68a71e6b3c5906b310463d5b627c}.
\]

R0.74P (2.6)--(2.10) defines, at good times, the endpoint-plus-total
dissipation clock and then selects its canonical absolutely continuous
representative:

\[
K_{k,R}=Q_{k,R}+F_{k,R},\qquad
K_{k,R}(s_R)=0,\qquad K_{k,R}\ge0.
\tag{X.4}
\]

R0.74V (V.16) specializes this clock to the exact smooth family.  Its only
three nonnegative rows are endpoint kinetic energy, accumulated ordinary
viscosity, and accumulated anomalous defect; the last row vanishes for the
smooth family.

Neither R0.74P nor R0.74V newly defines the deletion order.  R0.74V invokes
the inherited object \(\mathfrak L^K_{1,R}\).  Tracing that notation to its
definition, R0.74S (S.481), gives

\[
\boxed{
\mathfrak L^K_{1,R}(\mathcal D)
=
\inf_{\substack{S\subset\mathbb N\\ \#S\le1}}
\sup_{t\in\mathcal D}
\sum_{k\notin S}K_{k,R}(t).}
\tag{X.5}
\]

The deletion set is chosen once for the fixed solution, scale, centre, and
terminal domain.  It may not depend on \(t\).  The time supremum is taken
after that common set is fixed.

The actual completed-clock fixed-deletion target, R0.74S (S.487), is

\[
\bigl(\mathfrak L^K_{1,R}(\mathcal T_R)\bigr)^{3/2}
\le C_LP_R^M,
\tag{X.6}
\]

or equivalently

\[
\mathfrak L^K_{1,R}(\mathcal T_R)
\le C_L^{2/3}(P_R^M)^{2/3}.
\tag{X.7}
\]

This distinction between \(T_*\) and \((P_R^M)^{2/3}\) is decisive below.

## 2. Three-packet exact solution and normalization

Retain

\[
\lambda=\frac{63}{32},\qquad
c_h=\frac{15}{16},\qquad
p=\lambda^{-1}=\frac{32}{63},\qquad
d=c_h-p=\frac{433}{1008},
\tag{X.8}
\]

\[
a_S=\frac{75}{22528},\qquad
c_\gamma=\frac8{3969},\qquad
q=\frac{c_\gamma}{2}=\frac4{3969}.
\tag{X.9}
\]

For the three-packet extension impose the natural outermost version of the
central-chart hypothesis:

\[
L_1\ge9216,\qquad
L_3R\le\frac5{144},\qquad
R^{-1}e^{-a_SL_1^2}\longrightarrow0.
\tag{X.10}
\]

The replacement of \(L_2R\le5/144\) by \(L_3R\le5/144\) is an additional
three-packet chart gate.  It is not silently inferred from the literal
two-packet statement.

Use the same saturation heat shear, calibrated only once at \(h_1\):

\[
h_m=c_hL_mR,\qquad
B=\frac1{2D_1},\qquad
b(t,x_3)=B\theta_R(t,x_3).
\tag{X.11}
\]

Choose arbitrary interior re-centring times
\(\tau_m\in I_R=(64R^2,65R^2)\) and set

\[
Q_m(t)
=-B\int_0^{\tau_m}\theta_R(s,h_m)\,ds
 +B\int_0^t\theta_R(s,h_m)\,ds.
\tag{X.12}
\]

For each \(m=1,2,3\), translate an inversion-paired derivative-heat packet
so that \(Q_m(\tau_m)=0\), and re-evolve it under this one common
coefficient:

\[
(\partial_t+b\partial_2-\Delta_{23})G_m^\pm=0,
\qquad G_m=G_m^++G_m^-.
\tag{X.13}
\]

Define

\[
\Gamma_m=\gamma_{k_m}=e^{-c_\gamma L_m^2},
\qquad
\mathfrak a_m=A_*(\Gamma_mL_m)^{-1/2},
\tag{X.14}
\]

\[
U_3=\sum_{m=1}^3\mathfrak a_mG_m,\qquad
u^{(3)}=(U_3,b,0),\qquad p^{(3)}=0.
\tag{X.15}
\]

R0.74Q, Proposition 1.1, applies to every finite packet number.  The
linearity is used only after all packets have been re-evolved under the
same \(b\).  Thus (X.15) is a smooth periodic mean-zero solution of the
unforced Navier--Stokes equations.  Full inversion oddness and the even
mollifier give

\[
X_R=a_R=a_R'=0.
\tag{X.16}
\]

All three intended target clocks have the same normalization

\[
\boxed{
\Gamma_m\mathfrak a_m^2L_mR^2
=A_*^2R^2=:T_*,
\qquad m=1,2,3.}
\tag{X.17}
\]

The weights and amplitude ratios are

\[
\Gamma_2=\Gamma_1^4,\qquad
\Gamma_3=\Gamma_1^{16},
\tag{X.18}
\]

\[
\frac{\mathfrak a_2}{\mathfrak a_1}
=2^{-1/2}e^{3qL_1^2},\qquad
\frac{\mathfrak a_3}{\mathfrak a_2}
=2^{-1/2}e^{12qL_1^2},\qquad
\frac{\mathfrak a_3}{\mathfrak a_1}
=\frac12e^{15qL_1^2}.
\tag{X.19}
\]

Equal target-clock normalization is not equal raw-energy normalization.
The initial packet norms satisfy

\[
\|G_m^\pm(0)\|_2^2\asymp R^2.
\tag{X.20}
\]

Gaussian separation makes the amplitude-weighted off-diagonal inner
products negligible, and hence

\[
\|U_3(0)\|_2^2
\asymp R^2\sum_{m=1}^3\mathfrak a_m^2
\asymp\frac{T_*}{\Gamma_3L_3}.
\tag{X.21}
\]

Also \(\|b(0)\|_2^2\asymp B^2\asymp R^{-4}\).  Therefore

\[
\|u^{(3)}(0)\|_2^2
\asymp R^{-4}+\frac{T_*}{\Gamma_3L_3}.
\tag{X.22}
\]

Every member is finite-energy and smooth, but the family has no
scale-uniform raw initial-energy normalization.  The common factor \(A_*\)
does not repair the payment ratio in Section 8.

## 3. Packets 2 and 3 survive the remote strip

For \(m=2,3\), use the R0.74W strip

\[
\begin{aligned}
\mathcal S_m=\{x:\;&
|x_1|<\tfrac14\sqrt{pL_m}\,R,\quad
\tfrac54R<x_2<\tfrac32R,\\
&pL_mR-R<x_3<pL_mR-\tfrac12R\}.
\end{aligned}
\tag{X.23}
\]

Condition (X.10) puts both strips in the central chart and gives

\[
\mathcal S_m\subset A_{k_m-1}(R),\qquad
\Psi_{k_m-1}^R=1,\qquad
|\mathcal S_m|=\frac1{16}\sqrt{pL_m}\,R^3.
\tag{X.24}
\]

Let

\[
q_{65}=\frac{256}{257985}.
\tag{X.25}
\]

The direct-packet part of the R0.74W proof depends only on the common shear,
the packet height, and its own bridge; it is unchanged by adding finitely
many other passive packets.  The survival condition for packet \(m\) is

\[
\frac1{RL_m^2}
e^{-q_{65}L_m^2+CL_m}\longrightarrow0.
\tag{X.26}
\]

For packet \(2\), the U-reserve factorization uses

\[
4q_{65}-a_S
=\frac{3719797}{5811886080}>0.
\tag{X.27}
\]

For packet \(3\), the corresponding reserve is even larger:

\[
16q_{65}-a_S
=\frac{72925813}{5811886080}>0.
\tag{X.28}
\]

Thus (X.26) holds for both \(m=2,3\), uniformly for
\(\tau_m\in[64R^2,65R^2]\).  Their direct positive packets are relatively
asymptotic to the free comparators

\[
H_m(t,z,y)
=R^3\partial_zK_{R^2+t}^{\rm per}(z)
K_{R^2+t}^{\rm per}(y)
\tag{X.29}
\]

on \(\mathcal S_m\).

## 4. Every amplitude-weighted cross margin

It remains to prove that the two direct comparisons survive inside the
three-packet sum.  At time \(t=\tau_m\), write
\(a=1+\tau_m/R^2\in[65,66]\) and put

\[
r=\frac{L_j}{L_m}.
\]

The vertical supremum estimate inherited from R0.74W is

\[
|G_j^\pm(t,x)|
\le CRK_{R^2+t}^{\rm per}(x_3\mp h_j).
\tag{X.30}
\]

For the positive \(j\)-packet on \(\mathcal S_m\), comparison with
\(H_m\), including the amplitude ratio, has leading margin

\[
\delta_{m\leftarrow j}(a)
:=
\frac{(c_hr-p)^2-d^2}{4a}
-q(r^2-1).
\tag{X.31}
\]

If the first numerator is positive, the worst heat age is \(a=66\); if it
is negative, the worst heat age is \(a=65\).  Exact reduction gives

\[
\begin{array}{c|c|c|c}
\text{target strip }m&\text{other packet }j&r&
\inf_{65\le a\le66}\delta_{m\leftarrow j}(a)\\ \hline
2&1&1/2&\displaystyle\frac{3667}{70447104}\\[4pt]
2&3&2&\displaystyle\frac{100043}{29804544}\\[4pt]
3&2&1/2&\displaystyle\frac{3667}{70447104}\\[4pt]
3&1&1/4&\displaystyle\frac{147359}{281788416}
\end{array}
\tag{X.32}
\]

Every entry is positive.  In particular, the potentially dangerous huge
outer packet on the packet-2 inward strip obeys

\[
\frac{\mathfrak a_3|G_3^+|}
{\mathfrak a_2|H_2|}
\le
C\exp\!\left[
-\frac{100043}{29804544}L_2^2+CL_2
\right]
+\mathcal R_{\rm per}.
\tag{X.33}
\]

Thus its \(e^{3qL_2^2}\) amplitude advantage is strictly absorbed by its
vertical separation.

For the intended inversion partner,

\[
\frac{(c_h+p)^2-d^2}{4a}
=\frac{c_hp}{a}
\ge\frac5{693}>0.
\tag{X.34}
\]

Every negative partner of another packet is farther from the positive
remote strip than its positive partner.  It is therefore absorbed by
(X.32)--(X.34).

Finally, after the largest amplitude ratio is inserted, all noncentral
vertical copies are bounded by

\[
\mathcal R_{\rm per}
\le C\exp\!\left(qL_3^2-\frac3{22R^2}\right).
\tag{X.35}
\]

The outermost chart condition gives

\[
\mathcal R_{\rm per}
\le Ce^{-c_*L_3^2},
\qquad
c_*=\frac3{22}\left(\frac{144}{5}\right)^2-q
=\frac{123450676}{1091475}>0.
\tag{X.36}
\]

Equations (X.30)--(X.36) include all inversions, all adjacent and
non-adjacent cross packets, and all periodic windings.  Consequently,

\[
\sup_{x\in\mathcal S_m}
\left|
\frac{U_3(\tau_m,x)}
{\mathfrak a_mH_m(\tau_m,x_2,x_3-h_m)}-1
\right|\longrightarrow0,
\qquad m=2,3.
\tag{X.37}
\]

## 5. Two distinct adjacent-inward endpoint divergences

The adjacent-shell weight identity is unchanged:

\[
\frac{\gamma_{k_m-1}}{\Gamma_m}
=e^{(3/4)c_\gamma L_m^2}.
\tag{X.38}
\]

Set

\[
\chi(a)=\frac34c_\gamma-\frac{d^2}{2a}.
\tag{X.39}
\]

The exact endpoint, volume, amplitude, and shell-weight calculation from
R0.74W gives

\[
K_{k_m-1,R}(\tau_m)
\ge
cT_*L_m^{-1/2}
e^{\chi(65)L_m^2-CL_m},
\qquad m=2,3,
\tag{X.40}
\]

where

\[
\chi(65)=\frac{12191}{132088320}>0.
\tag{X.41}
\]

Because \(k_2-1=k_1\) and \(k_3-1=k_2\), (X.40) proves (X.2).  These are
lower bounds obtained from explicit strips.  No strip upper bound is being
promoted to a whole-shell upper bound.

The solution permits \(\tau_2=\tau_3=\tau\), in which case

\[
K_{k_1,R}(\tau)/T_*\to\infty,
\qquad
K_{k_2,R}(\tau)/T_*\to\infty
\tag{X.42}
\]

at the same smooth time.  This is a genuine simultaneous vector-height
statement for that optional schedule.

Equality of the times is unnecessary.  Suppose only that a terminal domain
\(\mathcal D\) contains \(\tau_2\) and \(\tau_3\).  For every
\(S\subset\mathbb N\) with \(\#S\le1\):

- if \(k_1\notin S\), take \(t=\tau_2\);
- if \(k_1\in S\), then \(k_2\notin S\), so take \(t=\tau_3\).

Nonnegativity of every clock coordinate and (X.5) give

\[
\boxed{
\mathfrak L^K_{1,R}(\mathcal D)
\ge
\min\{K_{k_1,R}(\tau_2),K_{k_2,R}(\tau_3)\}.}
\tag{X.43}
\]

This is exactly the R0.74T (T.17) pigeonhole.  It uses the
\(\inf_S\sup_t\) order.  It would be false for a deletion set allowed to
depend on \(t\).

Since \(I_R\subset\mathcal T_R\), both \(\tau_2\) and \(\tau_3\) belong to
the terminal domain in the actual gate.  Taking
\(\mathcal D=\mathcal T_R\) in (X.43) and combining with (X.40) yields

\[
\boxed{
\frac{\mathfrak L^K_{1,R}(\mathcal T_R)}{T_*}
\longrightarrow\infty.}
\tag{X.44}
\]

Thus a matching \(O(T_*)\) fixed-deletion all-shell upper is false for this
three-packet extension.

## 6. Smooth-time and canonical-clock boundary

The field (X.15) is smooth, so every time is a local-energy good time and
the literal R0.74V endpoint-plus-viscosity formula holds at
\(\tau_2,\tau_3\).  The anomalous-defect row is zero.  Hence (X.40) uses
the nonnegative endpoint kinetic row without a hard-time representative
issue.

For a later suitable-weak limit, the clock at a non-good time would instead
mean the canonical absolutely continuous representative (X.4).  The
present endpoint calculation alone does not justify passage to such a
limit.  No compactness or scale-contraction conclusion is used here.

## 7. Initial energy is not the missing normalization

Equation (X.17) is the equal target-clock normalization needed for the two
endpoint comparisons.  It does not make the raw packet energy, the common
shear, or the complete payment comparable to \(T_*\).

In particular, the outer packet makes
\(T_*/(\Gamma_3L_3)\) appear already in the global initial packet energy,
while the shear contributes \(R^{-4}\).  Choosing \(A_*\) changes the
relative shear size, but the ratio \((P_R^M)^{2/3}/T_*\) forced by the
packet-cubic payment is independent of \(A_*\).  Therefore no choice of the
common amplitude factor can turn (X.44) by itself into a counterexample to
(X.7).

## 8. The exact payment blocker

To compare with the actual fixed-deletion gate, retain an \(R^3\)-length
subinterval of the packet-3 certified target corridor.  Choose
\(\tau_3\) in the interior of \(I_R\), so this subinterval lies in the
payment window.

The ordinary near-lobe comparison and the same amplitude-weighted vertical
tail estimates show that packet \(3\) dominates the full three-packet sum
on its target lobe.  The lobe has spatial volume comparable to
\(L_3R^3\).

For completeness, put
\[
a_\times=\frac{49}{14850}.
\]
On a target lobe, the adjacent outer-packet margin and adjacent
inner-packet margin are respectively
\[
a_\times-3q=\frac{67}{242550}>0,
\qquad
\frac14a_\times+\frac34q
=\frac{4601}{2910600}>0.
\]
For packet \(1\) on the packet-3 target lobe, the non-adjacent inner
margin in \(L_3^2\)-units is
\[
\frac9{16}a_\times+\frac{15}{16}q
=\frac{32609}{11642400}>0.
\]
All negative partners are farther away, and (X.36) controls their
noncentral copies.  Thus the packet-3 target-lobe lower bound used here is
an amplitude-weighted three-packet statement, not a diagonal-only
assumption.

At payment radius \(2R\), the exact shell and weight identities are

\[
A_{k_3}(R)=A_{k_3-1}(2R),
\qquad
\gamma_{k_3-1}=\Gamma_3^{1/4}.
\tag{X.45}
\]

The nonnegative exterior velocity-cubic row of \(P_R^M\) therefore gives

\[
P_R^M
\ge
c\mathfrak a_3^3\Gamma_3^{1/4}L_3R^4
=cA_*^3R^4\Gamma_3^{-5/4}L_3^{-1/2}.
\tag{X.46}
\]

Taking the two-thirds power and using \(T_*=A_*^2R^2\),

\[
\boxed{
\frac{(P_R^M)^{2/3}}{T_*}
\ge
cR^{2/3}L_3^{-1/3}
e^{(5/6)c_\gamma L_3^2}.}
\tag{X.47}
\]

This ratio is independent of \(A_*\).  Write
\(\rho_R=\log(1/R)/L_1^2\).  The U-reserve implies
\(\rho_R\le a_S+o(1)\).  Since \(L_3^2=16L_1^2\), the lower exponential
rate in (X.47) is at least

\[
\frac{40}{3}c_\gamma-\frac23a_S
=\frac{3306805}{134120448}>0.
\tag{X.48}
\]

For comparison, the largest possible W-strip exponent over
\(m=2,3\) and \(a\in[65,66]\) is the packet-3 value
\(16\chi(66)L_1^2\), where

\[
\chi(66)=\frac{15263}{134120448}.
\tag{X.49}
\]

The payment rate exceeds even that larger strip rate by the exact amount

\[
\left(\frac{40}{3}c_\gamma-\frac23a_S\right)
-16\chi(66)
=\frac{3062597}{134120448}>0.
\tag{X.50}
\]

Denote the actual endpoint contribution of the audited strip by
\[
E_m^{\rm strip}
:=\frac{\gamma_{k_m-1}}{2R}
\int_{\mathcal S_m}|U_3(\tau_m,x)|^2\,dx.
\]
The relative comparison (X.37), together with the two-sided free-kernel
bounds, gives
\[
E_m^{\rm strip}
\le
CT_*L_m^{-1/2}e^{\chi(66)L_m^2+CL_m},
\qquad m=2,3.
\]
Thus the sum of the two actual W-strip endpoint witnesses is
\(o((P_R^M)^{2/3})\), including every polynomial and \(O(L_m)\)
transition factor:

\[
\frac{E_2^{\rm strip}+E_3^{\rm strip}}
{(P_R^M)^{2/3}}
\longrightarrow0.
\tag{X.51}
\]

Equation (X.51) does not upper-bound the full shell clocks.  It proves the
precise no-go needed here: the two W-type strip lower bounds, although
divergent relative to \(T_*\), cannot contradict the payment-normalized
fixed-deletion inequality (X.7).  A whole-shell or accumulated-dissipation
effect could make \(\mathfrak L^K_{1,R}\) larger, but no such estimate is
proved.

## 9. Exact arithmetic ledger

All fractions below were independently reduced:

| quantity | exact value |
|---|---:|
| \(p\) | \(32/63\) |
| \(d\) | \(433/1008\) |
| \(q\) | \(4/3969\) |
| \(q_{65}\) | \(256/257985\) |
| packet-2 survival reserve \(4q_{65}-a_S\) | \(3719797/5811886080\) |
| packet-3 survival reserve \(16q_{65}-a_S\) | \(72925813/5811886080\) |
| \(\delta_{2\leftarrow1}\) in \(L_2^2\)-units | \(3667/70447104\) |
| \(\delta_{2\leftarrow3}\) in \(L_2^2\)-units | \(100043/29804544\) |
| \(\delta_{3\leftarrow2}\) in \(L_3^2\)-units | \(3667/70447104\) |
| \(\delta_{3\leftarrow1}\) in \(L_3^2\)-units | \(147359/281788416\) |
| intended inversion margin | \(5/693\) |
| target-lobe adjacent outer margin | \(67/242550\) |
| target-lobe adjacent inner margin | \(4601/2910600\) |
| target-lobe packet \(3\leftarrow1\) margin | \(32609/11642400\) |
| periodic-copy margin \(c_*\) | \(123450676/1091475\) |
| \(\chi(65)\) | \(12191/132088320\) |
| \(\chi(66)\) | \(15263/134120448\) |
| payment lower rate in \(L_1^2\)-units | \(3306805/134120448\) |
| payment rate minus \(16\chi(66)\) | \(3062597/134120448\) |

Every margin used as strict is positive.

## 10. Minimal next proposition

The exact next target is not another \(T_*\)-normalized adjacent-strip
estimate.  It is the payment-compatible two-coordinate proposition:

\[
\boxed{
\begin{gathered}
\text{construct one exact family and two distinct coordinates }r\ne s\\
\text{with times }t_r,t_s\in\mathcal T_R\text{ such that}\\
\frac{\min\{K_{r,R}(t_r),K_{s,R}(t_s)\}}
{(P_R^M)^{2/3}}\longrightarrow\infty.
\end{gathered}}
\tag{X.52}
\]

By the fixed-deletion quantifier (X.5), (X.52) would immediately contradict
the budget-one gate (X.7), whether or not \(t_r=t_s\).

The equal-target three-packet W architecture cannot prove (X.52), because
its outermost target lobe already enforces (X.47)--(X.51).  Any viable next
construction must decouple the two undeletable clock heights from the
outer exterior cubic payment.  Changing only the common amplitude \(A_*\)
cannot do so.  A changed amplitude law, shell placement, exterior weight
interaction, or packet geometry would require a new exact normalization,
survival proof, and all-cross-packet audit.

This is a construction-level obstruction only.  It does not prove the open
fixed-deletion theorem, and it does not address arbitrary suitable weak
solutions or Navier--Stokes regularity.  \(\mathbf{NOT\ CLAY}\).
