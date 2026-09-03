# R0.74U Step 20 — intrinsic certified residence of the canonical common-shear lobe

## 0. Result and exact claim boundary

R0.74T proves that an outer kinetic lobe with normalized dwell
\(\theta=|J|/R^3\) pays cubically, independently of the relative schedule
of the other target shell.  Its remaining explicit-family escape condition
requires the maximal available comparable-floor dwell to be exponentially
short.  This note tests that condition on the already constructed
common-shear heat packets.

The answer is negative in a stronger, geometry-resolved sense.  For each
canonical packet lobe whose horizontal reference centre is re-centred at a
time in the inherited terminal slab, there is an explicitly certified time
corridor on which that same lobe remains in its physical shell.  Its length
is comparable to

\[
 L_iR^3.
\]

The lower scale is the product of the physical horizontal shell room
\(L_iR\) and the reciprocal common-shear speed \(R^2\).  The upper estimate
proved here is an upper estimate for this **certified geometric corridor**,
not for the superlevel set of the full completed clock.  The latter receives
additional nonnegative endpoint and accumulated-dissipation contributions,
and may also see other packets and the common shear.  For the completed
clock this note proves only the lower inclusion and hence an
\(\Omega(L_iR^3)\) residence statement.

More precisely, the certified corridor satisfies

\[
 {72\over5}L_iR^3
 \le |\mathscr R_i^{\rm cert}|
 \le \min\left\{R^2,
 {256A(L_i)\over1-\varepsilon_i}L_iR^3\right\},
\]

where \(A(L)\) is an exact annular margin and
\(\varepsilon_i=4e^{-a_DL_i^2}\).  On this corridor the total field has the
same amplitude-weighted lobe floor as in R0.74Q--T.  Consequently the
corresponding completed-clock superlevel set has measure at least
\((72/5)L_iR^3\).

For the two explicit terminal phases in R0.74T (T.42), the certified lower
constants improve to \(96/5\) for the inner packet and \(144/5\) for the
outer packet.  Substitution of the certified outer dwell into R0.74T
(T.24)--(T.29) makes the exponential conflict strictly stronger: the actual
normalized certified dwell is at least \((72/5)L_2\), while bounded payment
would require an exponentially vanishing quantity.

This is a theorem for the frozen saturation-shear, derivative-heat-packet
architecture.  It is not a residence theorem for arbitrary packets, not an
upper bound for a completed-clock superlevel set, not an arbitrary-clock
extraction theorem, and not a regularity or singularity theorem.
**NOT CLAY.**  No simulation or numerical fit is used.

<!-- R074U_STEP20_STATUS_CERTIFIED_RESIDENCE_PROVED -->
<!-- R074U_STEP20_STATUS_K_SUPERLEVEL_LOWER_ONLY -->
<!-- R074U_STEP20_STATUS_MAXIMAL_K_DWELL_OPEN -->

## 1. Frozen dependencies and packet setting

The exact source snapshots used in this note are:

| Dependency | SHA-256 | Use |
|---|---|---|
| `research/r074p_temporal_observable_triage.md` | `a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867` | nonnegative defect-completed clock |
| `research/r074t_schedule_invariant_dwell_coercivity.md` | `8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd` | asynchronous re-centring and dwell coercivity |
| `research/r074q_common_shear_multipacket_gate.md` | `60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695` | common-shear exact solution and platform lemma |
| `research/r074q_relaxed_multipacket_cubic_obstruction.md` | `ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d` | all-packet dominance and periodic remainder |
| `research/r074f_two_packet_survival.md` | `0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb` | full-time bridge comparison and inverted-packet suppression |
| `research/r074s_moving_frame_taylor_vortex_obstruction.md` | `de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0` | Step 16 boundary comparison only |

Retain the rational parameters

\[
 \lambda={63\over32},\qquad
 c_h={15\over16},\qquad
 b_1={5\over4},\qquad
 b_2={3\over2},\qquad
 a_D={49\over14625},\qquad
 a_S={75\over22528},\qquad
 c_\gamma={8\over3969}.
 \tag{U.1}
\]

For \(i\in\{1,2\}\), put

\[
 L_i=\lambda2^{k_i},\qquad
 k_2=k_1+1,\qquad
 L_2=2L_1,\qquad
 r_i=L_iR,\qquad
 h_i=c_hr_i,
 \tag{U.2}
\]

and impose the inherited central-chart and survival-compatible conditions

\[
 L_1\ge9216,\qquad
 L_2R\le{5\over144},\qquad
 R^{-1}e^{-a_SL_1^2}\longrightarrow0.
 \tag{U.3}
\]

Use the saturation profile and common shear

\[
 \theta_R(t,x_3)=e^{t\partial_3^2}g_R(x_3),\qquad
 D_1=\int_{R^2}^{65R^2}\theta_R(t,h_1)\,dt,
 \qquad
 B={1\over2D_1},\qquad
 b(t,x_3)=B\theta_R(t,x_3).
 \tag{U.4}
\]

The terminal slab is

\[
 I_R=(64R^2,65R^2).
 \tag{U.5}
\]

Choose \(\tau_i\in\overline I_R\), translate the inversion-paired packet
datum horizontally as in R0.74T, and define

\[
 q_{{\rm pre},i}
 =-B\int_0^{\tau_i}\theta_R(s,h_i)\,ds,
 \qquad
 Q_i(t)=q_{{\rm pre},i}
       +B\int_0^t\theta_R(s,h_i)\,ds.
 \tag{U.6}
\]

Then \(Q_i(\tau_i)=0\).  Horizontal translation commutes with the common
scalar advection--diffusion equation, and the inversion partner preserves
the full oddness.  Therefore the two translated packets, re-evolved under
the one coefficient \(b\), remain part of the exact smooth periodic
unforced Navier--Stokes solution of R0.74Q, Proposition 1.1.
The full inversion oddness and the even frozen mollifier also give

\[
 X_R=a_R=a_R'=0,
\]

so the physical boxes below are the same boxes seen by the Version-M
moving frame.

## 2. Platform error and exact speed interval

Define the packetwise platform errors

\[
 \varepsilon_i:=4e^{-a_DL_i^2},
 \qquad i=1,2.
 \tag{U.7}
\]

The two-parameter platform lemma gives, uniformly on the full calibration
interval \(R^2\le t\le65R^2\),

\[
 1-\varepsilon_i
 \le\theta_R(t,h_i)\le1.
 \tag{U.8}
\]

At \(L_1=9216\), one has
\(a_DL_1^2=462422016/1625>4\).  The elementary power-series lower bound
\(e^4>16\) therefore gives \(\varepsilon_i<1/4\) for both packets.  In
particular,

\[
 {3\over4}<1-\varepsilon_i\le1.
 \tag{U.9}
\]

Integrating (U.8) for the inner packet over the interval of length
\(64R^2\) yields

\[
 64R^2(1-\varepsilon_1)
 \le D_1\le64R^2,
 \qquad
 {1\over128R^2}
 \le B\le{1\over128(1-\varepsilon_1)R^2}.
 \tag{U.10}
\]

Consequently every reference centre is strictly increasing on the slab and
obeys the exact uniform speed interval

\[
 \boxed{
 {1-\varepsilon_i\over128R^2}
 \le Q_i'(t)
 \le {1\over128(1-\varepsilon_1)R^2},
 \qquad t\in I_R.}
 \tag{U.11}
\]

This kinematic inequality, rather than a generic time norm for the clock,
is the temporal input of the proof.

## 3. The exact annular corridor

For each packet define its canonical positive box by

\[
 \Omega_i(t)=\left\{x\in\mathbb T^3:
 |x_1|<{r_i\over16},\quad
 b_1R<x_2-Q_i(t)<b_2R,\quad
 |x_3-h_i|<R\right\}.
 \tag{U.12}
\]

Its spatial volume is

\[
 |\Omega_i(t)|={1\over16}L_iR^3.
 \tag{U.13}
\]

The exact sufficient horizontal-centre margin is

\[
 \boxed{
 A(L):=
 \sqrt{\left({2\over\lambda}\right)^2
       -{1\over256}
       -\left(c_h+{1\over L}\right)^2}
 -{b_2\over L}.}
 \tag{U.14}
\]

This quantity is real and uniformly positive on the frozen range.  Indeed,
all corrections decrease with \(L\), and at \(L=9216\),

\[
 \left({2\over\lambda}\right)^2-{1\over256}
 -\left(c_h+{1\over L}\right)^2
 -\left({3\over8}+{b_2\over L}\right)^2
 ={15232043\over1849688064}>0.
 \tag{U.15}
\]

Hence

\[
 {3\over8}<A(L)<1,
 \qquad L\ge9216.
 \tag{U.16}
\]

Suppose now that \(|Q_i(t)|<A(L_i)r_i\).  The inner annular inequality
follows from the vertical coordinate alone:

\[
 {|x|\over r_i}
 \ge c_h-{1\over L_i}
 >{1\over\lambda},
 \qquad
 c_h-{1\over9216}-{1\over\lambda}
 ={9235\over21504}>0.
 \tag{U.17}
\]

For the outer inequality, (U.12) and (U.14) give

\[
 { |x|^2\over r_i^2}
 <{1\over256}
 +\left(A(L_i)+{b_2\over L_i}\right)^2
 +\left(c_h+{1\over L_i}\right)^2
 =\left({2\over\lambda}\right)^2.
 \tag{U.18}
\]

The chart is unambiguous: (U.3), \(L_i\ge9216\), and the coordinate bounds
in (U.12) keep the entire box inside the central lift.  Equations
(U.17)--(U.18) therefore prove

\[
 |Q_i(t)|<A(L_i)r_i
 \quad\Longrightarrow\quad
 \Omega_i(t)\subset A_{k_i}(R),
 \qquad
 \Psi_{k_i}^R=1\ \hbox{on }\Omega_i(t).
 \tag{U.19}
\]

Define the **certified geometric residence corridor** by

\[
 \boxed{
 \mathscr R_i^{\rm cert}
 :=\{t\in I_R:|Q_i(t)|<A(L_i)r_i\}.}
 \tag{U.20}
\]

This is a deliberately intrinsic definition tied to the canonical lobe and
the exact sufficient annular margin.  It is not defined as a clock
superlevel set.

## 4. Slab-truncated residence is \(\Theta(L_iR^3)\)

Because \(Q_i(\tau_i)=0\), the travel time from \(\tau_i\) to either edge
of the corridor, measured using the speed upper bound in (U.11), is at
least

\[
 128A(L_i)(1-\varepsilon_1)L_iR^3
 >36L_iR^3.
 \tag{U.21}
\]

At least one of the two sides of \(\tau_i\) inside the slab has length
\(R^2/2\).  The chart restriction gives

\[
 {R^2\over2}
 \ge {72\over5}L_iR^3,
 \qquad
 L_iR\le{5\over144}.
 \tag{U.22}
\]

Choose the side with that much slab room.  The minimum of the geometric
travel allowance in (U.21) and the slab allowance in (U.22) proves the
uniform lower bound

\[
 \boxed{
 |\mathscr R_i^{\rm cert}|
 \ge {72\over5}L_iR^3.}
 \tag{U.23}
\]

For the upper bound, \(Q_i\) is increasing and the centre interval in
(U.20) has width \(2A(L_i)r_i\).  The speed lower bound in (U.11) gives

\[
 \boxed{
 |\mathscr R_i^{\rm cert}|
 \le\min\left\{R^2,
 {256A(L_i)\over1-\varepsilon_i}L_iR^3\right\}
 <{1024\over3}L_iR^3.}
 \tag{U.24}
\]

Thus the certified canonical-lobe corridor has the two-sided scale law

\[
 \boxed{
 |\mathscr R_i^{\rm cert}|\asymp L_iR^3,}
 \tag{U.25}
\]

with absolute constants on the frozen parameter range.

Equation (U.24) is **not** an upper bound for all times on which
\(K_{k_i,R}\) is comparable to its target scale.  Even for this exact
solution, accumulated dissipation, the shear component, or a different
packet can keep the full clock above that level after the certified lobe
leaves the corridor.

## 5. Full-slab packet survival and total-field dominance

It remains to verify that increasing the geometric residence from the
previously selected \(R^3\) subinterval to (U.20) does not lose the
amplitude floor.  This is where the uniform time ranges in the inherited
estimates matter.

R0.74F Lemma 4.1, with the uniform common-shear parameter substitution
verified in R0.74Q Step 2 (Q.126)--(Q.130), gives, uniformly for
\(0\le t\le65R^2\), \(|y|\le R\), and all horizontal offsets \(z\),

\[
 \left|G_i^+(t,Q_i(t)+z,h_i+y)
 -R^3\partial_zK_{R^2+t}^{\rm per}(z)
       K_{R^2+t}^{\rm per}(y)\right|
 \le {C\over R}
 \left(e^{-a_DL_i^2}+e^{-a_SL_i^2}\right)
 +Ce^{-c/R^2}.
 \tag{U.26}
\]

On the full slab and the canonical box variables,

\[
 65<{R^2+t\over R^2}<66,
 \qquad
 {5\over4}<{z\over R}<{3\over2},
 \qquad
 {|y|\over R}<1.
 \tag{U.27}
\]

The central real-Gaussian derivative in (U.26), after scaling by \(R^3\),
has one sign and a strictly positive minimum on the compact parameter box
in (U.27).  Its noncentral periodic copies are \(O(e^{-c/R^2})\).  The
right side of (U.26) tends to zero uniformly in \(i\), because \(L_i\ge
L_1\), (U.3) is the inherited inner survival reserve, and the chart bound
forces \(R\to0\).  Therefore there
is a fixed \(c_0>0\) such that

\[
 |G_i^+(t,x_2,x_3)|\ge2c_0
 \quad\hbox{on }\Omega_i(t),
 \qquad t\in I_R.
 \tag{U.28}
\]

This re-runs the last compact-minimum step of R0.74F Proposition 4.2 on
the larger normalized-age box (U.27); it does not cite R0.74Q (Q.130)
beyond the shorter interval on which that statement was originally made.

The inverted partner remains negligible on the same full time range.
R0.74F Lemma 5.1 is uniform in the horizontal coordinate and gives a
vertical-separation majorant of the form

\[
 |G_i^-(t,x_2,h_i+y)|
 \le C\exp\left[-{(2c_hL_i-1)^2\over264}\right]
      +Ce^{-c/R^2}.
 \tag{U.29}
\]

For the other packet, R0.74Q Step 2 (Q.138)--(Q.153) gives the amplitude-weighted
vertical cross-tail estimates uniformly for \(0\le t\le65R^2\).  Those
bounds use a supremum of the horizontal derivative kernel, so neither
\(q_{{\rm pre},i}\) nor the size of \(Q_i(t)\) inside the certified corridor
changes their constants.  The adjacent outer-to-inner exponent reserve is

\[
 a_\times-{3\over2}c_\gamma
 ={67\over242550}>0,
 \qquad
 a_\times={49\over14850},
 \qquad
 \mu_{\rm in}={4601\over2910600}>0.
 \tag{U.30}
\]

The periodic remainder also stays negligible under the generalized chart
condition in (U.3).  With \(q=c_\gamma/2\),

\[
 C\exp\left(qL_2^2-{3\over22R^2}\right)
 \le C\exp(-c_*L_2^2)\longrightarrow0,
 \qquad
 c_*={3\over22}\left({144\over5}\right)^2-q>0.
 \tag{U.31}
\]

Combining (U.28)--(U.31) in the two-packet case gives, uniformly on the
moving \(i\)-th box throughout \(I_R\),

\[
 |G_i|\ge c_0,
 \qquad
 {\mathfrak a_{3-i}|G_{3-i}|\over
  \mathfrak a_i|G_i|}=o(1).
\]

Consequently the equal-target amplitudes

\[
 \Gamma_i=e^{-c_\gamma L_i^2},
 \qquad
 \mathfrak a_i=A_*(\Gamma_iL_i)^{-1/2},
 \qquad
 T:=A_*^2R^2,
 \tag{U.32}
\]

give the total-field lower bound

\[
 \boxed{
 |u(t,x)|\ge c\mathfrak a_i,
 \qquad
 x\in\Omega_i(t),\quad
 t\in\mathscr R_i^{\rm cert},}
 \tag{U.33}
\]

after increasing the base scale once.  This is the full-field statement;
no isolated packet summand is substituted for \(u\).

## 6. Completed-clock lower residence and cubic payment

The time cutoff equals one on \(I_R\), and (U.19) puts the shell cutoff
equal to one on the certified lobe.  Since every other endpoint and
dissipation contribution to the completed clock is nonnegative,

\[
 K_{k_i,R}(t)
 \ge {\Gamma_i\over2R}
      \int_{\Omega_i(t)}|u(t,x)|^2\,dx
 \ge c\Gamma_i\mathfrak a_i^2L_iR^2
 =cT
 \quad(t\in\mathscr R_i^{\rm cert}).
 \tag{U.34}
\]

Thus, for a fixed sufficiently small \(c_K>0\), the full-clock superlevel
set satisfies only the following proved inclusion and lower bound:

\[
 \boxed{
 \mathscr R_i^{\rm cert}
 \subset\{t\in I_R:K_{k_i,R}(t)\ge c_KT\},
 \qquad
 \left|\{K_{k_i,R}\ge c_KT\}\cap I_R\right|
 \ge {72\over5}L_iR^3.}
 \tag{U.35}
\]

No converse inclusion and no upper bound for this superlevel set are
claimed.

Define the normalized certified outer dwell by

\[
 \theta_{{\rm cert},2}
 :={|\mathscr R_2^{\rm cert}|\over R^3}
 \ge {72\over5}L_2.
 \tag{U.36}
\]

Applying R0.74T Lemma 2.1 on this measurable corridor gives, with the
corresponding persistent lobe kinetic floor \(h_2\ge cT\),

\[
 P_R^M
 \ge2\sqrt2\,\theta_{{\rm cert},2}h_2^{3/2}R
       \Gamma_2^{-5/4}L_2^{-1/2},
 \qquad
 { (P_R^M)^{2/3}\over T}
 \ge cR^{2/3}\Gamma_2^{-5/6}L_2^{1/3}.
 \tag{U.37}
\]

Now use the adjacent-shell survival sequence

\[
 S=\log{1\over R},
 \qquad
 d_L=a_SL_1^2-S\longrightarrow+\infty,
 \qquad
 L_2=2L_1.
 \tag{U.38}
\]

The exact R0.74T logarithmic identity and (U.36) yield

\[
 \boxed{
 \log\Lambda_2
 \ge{2\over3}\left[
 \log{72\over5}
 +(5c_\gamma-a_S)L_1^2+d_L
 +{1\over2}\log L_2\right],
 \qquad
 5c_\gamma-a_S
 ={603445\over89413632}>0.}
 \tag{U.39}
\]

In particular, \((P_R^M)^{2/3}/T\to\infty\).  More directly, the necessary
bounded-payment dwell condition R0.74T (T.28) would require

\[
 {72\over5}L_2
 \le\theta_{{\rm cert},2}
 \le CL_2^{1/2}
 e^{-(5c_\gamma-a_S)L_1^2-d_L},
 \tag{U.40}
\]

which is impossible.  Equivalently, the ratio of the proved certified lower
dwell to the largest dwell permitted by that necessary condition is bounded
below by

\[
 cL_2^{1/2}
 e^{(5c_\gamma-a_S)L_1^2+d_L}\longrightarrow\infty.
 \tag{U.41}
\]

This closes the exponentially short-dwell escape for the frozen canonical
common-shear lobe architecture.  It does not exclude a different shear,
packet geometry, shell placement, or a clock created mainly by
dissipation.

## 7. Strengthening the two explicit R0.74T phases

For the phases in R0.74T (T.42),

\[
 \tau_1=64R^2+2R^3,
 \qquad
 \tau_2=65R^2,
 \qquad
 R<{1\over3}.
 \tag{U.42}
\]

The inner packet has forward slab room

\[
 65R^2-\tau_1
 =R^2(1-2R)
 >{1\over3}R^2
 \ge {96\over5}L_1R^3,
 \tag{U.43}
\]

where \(L_1R=L_2R/2\le5/288\).  The outer packet has the full backward
slab room

\[
 \tau_2-64R^2=R^2
 \ge {144\over5}L_2R^3.
 \tag{U.44}
\]

Both constants are smaller than the geometric travel allowance
\(36L_iR^3\) in (U.21).  Hence the same certified corridors satisfy the
sharper directional lower bounds

\[
 \boxed{
 |\mathscr R_1^{\rm cert}\cap(\tau_1,65R^2)|
 \ge {96\over5}L_1R^3,
 \qquad
 |\mathscr R_2^{\rm cert}\cap(64R^2,\tau_2)|
 \ge {144\over5}L_2R^3.}
 \tag{U.45}
\]

The first strengthening uses the forward side of the inner re-centring
time; it does not assert that the original backward interval in (T.42) has
that length.  The second uses the backward side of the outer endpoint.

## 8. Why this is not Step 16 again

R0.74S Step 16 studies Taylor's decaying vortex while an
amplitude-dependent mollified trajectory crosses a fixed spatial phase.
Its residence time is \(O(A^{-1})\), and it is used to test absolute
\(L_t^p\) norms of the physical-flux derivative.  Step 17 then shows that
recurrence destroys every sublinear absolute temporal-tail proposal.

The present result uses none of those ingredients.  The observable is a
positive endpoint kinetic floor inside a specified physical shell; the
motion is the explicit packet centre with speed \(Q_i'\asymp R^{-2}\); and
the available spatial corridor has width \(A(L_i)L_iR\).  The conclusion
\(L_iR^3\) follows from this exact kinematic product and is inserted into a
nonnegative velocity-cubic payment.  No absolute flux variation, temporal
\(L^p\) envelope, recurrence count, or generic time-Lipschitz claim is used.

## 9. Claim ledger and next gate

The following are **PROVED** in this note:

- the platform-error speed interval (U.7)--(U.11);
- positivity and the exact formula for the annular corridor margin
  \(A(L)\), (U.14)--(U.19);
- the slab-truncated two-sided estimate for the certified geometric
  residence, (U.23)--(U.25);
- extension of the direct-packet, inverted-packet, cross-packet, and
  periodic-remainder estimates to the full terminal slab;
- the total-field lobe floor on the certified corridor, (U.33);
- the lower inclusion and \(\Omega(L_iR^3)\) measure bound for the full
  completed-clock superlevel set, (U.34)--(U.35);
- the strengthened dwell/payment conflict (U.36)--(U.41); and
- the two explicit constants \(96/5\) and \(144/5\) for the phases in
  R0.74T (T.42).

The following are **INHERITED**:

- the exact common-shear finite-packet Navier--Stokes construction and its
  inversion parity;
- the two-parameter saturation-platform estimate;
- the all-winding bridge comparison, inverted-packet suppression, and
  amplitude-weighted all-packet dominance estimates;
- the defect-completed clock and the fact that its endpoint and accumulated
  dissipation pieces are nonnegative; and
- R0.74T's schedule-invariant lobe coercivity and necessary exponential
  dwell threshold.

The following remain **OPEN**:

- any upper bound for
  \(|\{t:K_{k_i,R}(t)\ge cT\}|\); in particular, (U.24) must not be
  transferred from \(\mathscr R_i^{\rm cert}\) to the full clock;
- an upper bound for \(\mathfrak L^K_{1,R}\), including off-target clocks,
  the common shear, packet cross terms, and accumulated dissipation;
- extraction of a comparable endpoint lobe from an arbitrary large
  completed clock of a suitable weak solution;
- the high-Rayleigh and anomalous-defect dissipation branches;
- the fixed-deletion gate, direct hybrid gate, Q.12, Q.1, scale contraction,
  regularity, singularity formation, and the Millennium problem.

The next nonredundant explicit-family question is a full completed-clock
upper ledger.  Off-target endpoint rows, viscous accumulation, cross terms,
and the shear baseline must be estimated together; none is silently removed
by the present certified-residence theorem.

**NOT CLAY.**

<!-- R074U_STEP20_END -->
