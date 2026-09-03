# R0.74V Step 21 route memo — the full completed-clock upper ledger

## 0. Decision, status, and exact scope

R0.74U proves the one-sided inclusion

\[
 \mathscr R_i^{\rm cert}
 \subset \{t\in I_R:K_{k_i,R}(t)\ge c_KT\},
 \qquad
 |\mathscr R_i^{\rm cert}|\asymp L_iR^3,
 \tag{V.1}
\]

for each of the two re-centred common-shear packets.  It deliberately does
not prove the reverse inclusion.  This memo isolates exactly what a reverse
estimate would have to control.

There are two different prospective conclusions, and they must not be
identified:

1. a **target-coordinate duration estimate**

   \[
    |\{t\in I_R:K_{k_i,R}(t)\ge \kappa T\}|
    \lesssim_\kappa L_iR^3,
    \qquad i=1,2;
    \tag{V.2}
   \]

2. an **all-shell upper estimate**, such as a bound for
   \(\mathfrak L^K_{1,R}\), the whole vector \((K_{k,R})_k\), or
   \(Y_{2,R}^{\rm sf}\).

The first is a temporal occupation problem for two specified shell
coordinates.  The second also sees every inward and outward shell and, for
\(Y_{2,R}^{\rm sf}\), the entire positive-variation history.  A proof of
(V.2) would not prove the second conclusion.

The route decision is as follows.

- The exact clock splits into a nonnegative common-shear clock, a
  nonnegative total-packet endpoint, a nondecreasing total-packet viscous
  accumulation, and (outside the present smooth family) a nondecreasing
  anomalous-defect accumulation.
- Packet-packet cross terms are real and signed when the packet square is
  expanded, but they are not an independent upper-bound obstruction:
  Cauchy--Schwarz/Young absorbs them into the two diagonal packet rows.
- The genuine duration obstructions are the pieces that do not leave when a
  packet centre leaves the annulus: the shear baseline and every accumulated
  dissipation row.  They must be strictly below the chosen level
  \(\kappa T\).  Otherwise an \(O(L_iR^3)\) upper bound is unavailable and
  may be false.
- The first missing analytic input is a whole-annulus, moving-centre
  \(L^2\)-and-\(H^1\) occupation estimate for the finite central-chart
  table (V.67).  The existing lobe comparison is pointwise on
  \(|x_3-h_i|\le R\) and is not such an estimate.  Extending it to every
  periodized shell is a separate lifted-copy summation problem.
- Before attempting an all-shell upper theorem, there is a smaller
  obstruction-first calculation.  For the free heat comparator, the packet
  tail in the adjacent inward shell gains a **positive** net exponential
  after the shell weight is inserted.  A relative common-shear bridge
  comparison on that remote strip would therefore disprove a matching
  \(O(T)\) all-shell upper bound for the frozen placement.

Accordingly, this document is an evidence-backed route memo, not a completed
upper theorem.  It proves the algebraic decompositions and coarse scale
budgets below, states the smallest next analytic proposition, and records
the exact failure conditions.  It does not alter R0.74U, does not make a
claim about arbitrary suitable weak solutions, and proves no regularity,
singularity, or Millennium statement.  **NOT CLAY.**

<!-- R074V_STEP21_STATUS_ROUTE_ONLY -->
<!-- R074V_STEP21_STATUS_K_SUPERLEVEL_UPPER_OPEN -->
<!-- R074V_STEP21_STATUS_ADJACENT_INWARD_TAIL_GATE -->
<!-- R074V_STEP21_STATUS_LIFTED_MULTIPLICITY_INCLUDED -->
<!-- R074V_STEP21_STATUS_PERIODIZED_VOLUME_USES_LIFTED_INTEGRAL -->
<!-- R074V_STEP21_STATUS_OCCUPATION_CENTRAL_FINITE_ONLY -->
<!-- R074V_STEP21_STATUS_ALL_K_LIFTED_COPY_SUMMATION_OPEN -->
<!-- R074V_STEP21_STATUS_RAW_ENDPOINT_MEASURE_GOOD_TIMES_ONLY -->

## 1. Frozen source ledger

This memo was prepared at source commit
`d74e7b297928147334136f4c3cb29c5226d66381`.  The relevant committed
snapshots are:

| Dependency | SHA-256 | Exact use here |
|---|---|---|
| `research/r074e_local_mollified_frame_gate.md` | `3a0ea093c42016b78cb589738a666d7b40019fd860c934be9c46418cb1fb05d7` | Euclidean shell, padded cutoff, and periodization definitions |
| `research/r074f_two_packet_survival.md` | `0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb` | all-winding packet representation, near-lobe comparison, inversion suppression |
| `research/r074h_collar_flux_two_regime_closure.md` | `8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1` | periodized cutoff identity, derivative majorant, and lifted-copy bookkeeping |
| `research/r074p_temporal_observable_triage.md` | `a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867` | total dissipation measure, completed clock, \(K=Q+F\), BV ledger |
| `research/r074q_common_shear_multipacket_gate.md` | `60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695` | exact common-shear solution and exact two-packet clock/cross ledger |
| `research/r074q_relaxed_multipacket_cubic_obstruction.md` | `ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d` | relaxed placement, equal-target amplitudes, on-lobe packet dominance |
| `research/r074t_schedule_invariant_dwell_coercivity.md` | `8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd` | arbitrary re-centring inside the terminal slab and lobe-payment coercivity |
| `research/r074u_intrinsic_certified_residence.md` | `e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99` | intrinsic corridor and lower-only completed-clock residence |

The precise inherited boundaries are:

- R0.74E (4.12b)--(4.12d) and R0.74H (2.1)--(2.5a) fix the Euclidean
  padded cutoff and its sum-periodization.  They do not identify
  \(\Psi_k^R\) with a \(0\)-\(1\) projected indicator at large \(k\);
  lifted multiplicity must be retained.
- R0.74P (2.1)--(2.10) proves the nonnegative defect-completed clock and its
  canonical absolutely continuous balance representative.
- R0.74Q Step 1 (Q.66)--(Q.73) writes the exact two-packet diagonal and
  cross terms.
- R0.74T (T.9)--(T.18) converts a separately supplied persistent kinetic
  lobe into cubic payment; it is not a \(K\)-only extraction theorem.
- R0.74U (U.24) is an upper bound for the geometric centre corridor only.
  R0.74U (U.34)--(U.35) supplies only the inclusion (V.1), and its Section 9
  explicitly leaves every \(K\)-superlevel upper bound open.

## 2. Frozen adjacent-shell solution

Retain the R0.74T--U constants and restrictions

\[
 \lambda={63\over32},\qquad c_h={15\over16},\qquad
 a_D={49\over14625},\qquad a_S={75\over22528},\qquad
 c_\gamma={8\over3969},
 \tag{V.3}
\]

\[
 L_i=\lambda2^{k_i},\qquad k_2=k_1+1,\qquad L_2=2L_1,
 \qquad r_i=L_iR,\qquad h_i=c_hr_i,
 \tag{V.4}
\]

\[
 L_1\ge9216,\qquad L_2R\le{5\over144},\qquad
 R^{-1}e^{-a_SL_1^2}\longrightarrow0.
 \tag{V.5}
\]

Let

\[
 I_R=(64R^2,65R^2),\qquad s_R=61R^2,
 \tag{V.6}
\]

and retain the nondecreasing cutoff

\[
 0\le\eta_R\le1,\qquad \eta_R=0\ \hbox{near }s_R,
 \qquad \eta_R=1\ \hbox{on }I_R,
 \qquad 0\le\eta_R'\lesssim R^{-2}.
\tag{V.7}
\]

The frozen radial shell weight and cutoff are

\[
 \gamma_k=\exp(-4^{k-1}/32),
 \qquad
 \psi_k^R(x)=
 \vartheta\!\left({|x|-2^kR\over R/8}\right)
 \vartheta\!\left({2^{k+1}R-|x|\over R/8}\right),
 \tag{V.7a}
\]

Here \(\vartheta\) is the frozen R0.74E cutoff: it is nondecreasing,
\(\vartheta(s)=0\) for \(s\le-1\), and \(\vartheta(s)=1\) for \(s\ge0\).
With \(\Psi_k^R\) the periodization of \(\psi_k^R\), its central
support is contained in the \(R/8\)-padding of
\(A_k(R)=\{2^kR\le|x|<2^{k+1}R\}\).

Use the saturation heat shear

\[
 \theta_R=e^{t\partial_3^2}g_R,\qquad
 D_1=\int_{R^2}^{65R^2}\theta_R(t,h_1)\,dt,\qquad
 B={1\over2D_1},\qquad b=B\theta_R.
 \tag{V.8}
\]

For arbitrary \(\tau_i\in\overline I_R\), the packet centres are

\[
 Q_i(t)=-B\int_0^{\tau_i}\theta_R(s,h_i)\,ds
       +B\int_0^t\theta_R(s,h_i)\,ds,
 \qquad Q_i(\tau_i)=0.
 \tag{V.9}
\]

The R0.74U platform estimate, originally stated on the full interval
\(R^2\le t\le65R^2\), and the bounds on \(B\) give, also on the entire
clock interval \([s_R,65R^2]\),

\[
 {1-\varepsilon_i\over128R^2}
 \le Q_i'(t)
 \le {1\over128(1-\varepsilon_1)R^2},
 \qquad \varepsilon_i=4e^{-a_DL_i^2}<\frac14.
 \tag{V.10}
\]

Thus each \(Q_i\) is one-to-one and its inverse has scale \(R^2\).  This
is the kinematic fact needed for every occupation estimate below.

Let \(G_i^\pm\) be the translated inversion-paired solutions of the common
scalar equation and put

\[
 G_i=G_i^++G_i^-,\qquad
 g_i=\mathfrak a_iG_i,\qquad G=g_1+g_2,
 \tag{V.11}
\]

\[
 \Gamma_i=\gamma_{k_i}=e^{-c_\gamma L_i^2},\qquad
 \mathfrak a_i=A_*(\Gamma_iL_i)^{-1/2},\qquad
 T=A_*^2R^2.
 \tag{V.12}
\]

Then

\[
 u=(G,b,0),\qquad p=0,
 \qquad X_R=a_R=a_R'=0
 \tag{V.13}
\]

is the exact smooth periodic common-shear solution.  The factor \(A_*>0\)
is not fixed by R0.74U.  This freedom is important: the shear does not scale
with \(A_*\), while the comparison level \(T\) does.

## 3. Exact nonnegative completion ledger

### 3.1 General Version-M completion

R0.74P defines

\[
 \boldsymbol\mu[u,p]
 =-\partial_t{|u|^2\over2}
  -\nabla\!\cdot\!\left[\left({|u|^2\over2}+p\right)u\right]
  +\Delta {|u|^2\over2},
 \tag{V.14}
\]

with

\[
 \boldsymbol\mu=|\nabla u|^2\,dx\,dt+\boldsymbol D,
 \qquad \boldsymbol D\ge0.
 \tag{V.15}
\]

At every local-energy good time, the literal general Version--M
endpoint-plus-measure formula is

\[
\begin{aligned}
 K_{k,R}(t)
 ={}&{\gamma_k\eta_R(t)\over2R}
       \int_{\mathbb T^3}\Psi_k^R(y)|v_R(t,y)|^2\,dy\\
 &+{\gamma_k\over R}\int_{(s_R,t)\times\mathbb T^3}
       \eta_R(r)\Psi_k^R(x-X_R(r))|\nabla u(r,x)|^2\,dx\,dr\\
 &+{\gamma_k\over R}\int_{(s_R,t)\times\mathbb T^3}
       \eta_R(r)\Psi_k^R(x-X_R(r))\,d\boldsymbol D(r,x),
\end{aligned}
\tag{V.16}
\]

where \(v_R(t,y)=u(t,y+X_R(t))\) and \(a_R=\dot X_R\).  In the exact
family (V.13), \(X_R=a_R=0\), so (V.16) reduces to the unshifted formula
used below and holds at every time.  For a general suitable weak solution,
at a non-good time \(K_{k,R}\) instead means R0.74P's canonical absolutely
continuous balance representative \(K_{k,R}=Q_{k,R}+F_{k,R}\); (V.16)
must not be read as a raw hard-time endpoint identity there.

These are the three and only three nonnegative completion rows:

1. endpoint kinetic energy;
2. accumulated ordinary viscosity;
3. accumulated anomalous local-energy defect.

For later reference, denote the third row by

\[
 D^{\rm an}_{k,R}(t)
 :={\gamma_k\over R}
   \int_{(s_R,t)\times\mathbb T^3}
   \eta_R(r)\Psi_k^R(x-X_R(r))\,d\boldsymbol D(r,x).
 \tag{V.16a}
\]

The third row is exactly zero for (V.13), because the solution is smooth.
It must nevertheless be retained as a separate obstruction before any
statement is transferred to suitable weak solutions.

### 3.2 Shear/packet splitting for the exact family

For (V.13), orthogonality of the velocity components gives the exact
nonnegative splitting

\[
 \boxed{K_{k,R}=K^b_{k,R}+K^G_{k,R},}
 \tag{V.17}
\]

where

\[
\begin{aligned}
 K^b_{k,R}(t)
 :={}&{\gamma_k\eta_R(t)\over2R}\int\Psi_k^Rb^2
 +{\gamma_k\over R}\int_{s_R}^t\!\!\int
       \eta_R\Psi_k^R|\partial_3b|^2,\\
 K^G_{k,R}(t)
 :={}&{\gamma_k\eta_R(t)\over2R}\int\Psi_k^RG^2
 +{\gamma_k\over R}\int_{s_R}^t\!\!\int
       \eta_R\Psi_k^R|\nabla_{23}G|^2.
\end{aligned}
\tag{V.18}
\]

Both clocks in (V.18) are nonnegative.  In particular, the common shear
may be subtracted exactly to define an architecture-specific packet clock
\(K^G=K-K^b\), without losing positivity.  That subtraction changes the
observable: an upper theorem for \(K^G\) is not an upper theorem for the
canonical R0.74P clock \(K\).

Write

\[
\begin{aligned}
 E_k^m(t)&={\gamma_k\eta_R(t)\over2R}
              \int\Psi_k^Rg_m^2,\\
 D_k^m(t)&={\gamma_k\over R}\int_{s_R}^t\!\!\int
              \eta_R\Psi_k^R|\nabla g_m|^2,
 \qquad m=1,2,
\end{aligned}
\tag{V.19}
\]

and

\[
\begin{aligned}
 E_k^{12}(t)&={\gamma_k\eta_R(t)\over R}
                \int\Psi_k^Rg_1g_2,\\
 D_k^{12}(t)&={2\gamma_k\over R}\int_{s_R}^t\!\!\int
                \eta_R\Psi_k^R\nabla g_1\!\cdot\!\nabla g_2.
\end{aligned}
\tag{V.20}
\]

Then the exact expansion from R0.74Q is

\[
 K^G_{k,R}=E_k^1+E_k^2+E_k^{12}
            +D_k^1+D_k^2+D_k^{12}.
 \tag{V.21}
\]

The cross rows in (V.20) are signed, but

\[
 |E_k^{12}|\le E_k^1+E_k^2,
 \qquad
 |D_k^{12}|\le D_k^1+D_k^2.
 \tag{V.22}
\]

Consequently the safe pointwise upper decomposition is

\[
 \boxed{
 K_{k,R}(t)
 \le K^b_{k,R}(t)
     +2\sum_{m=1}^2\bigl(E_k^m(t)+D_k^m(t)\bigr).}
 \tag{V.23}
\]

This is stronger for an upper route than treating
\(\operatorname {TV}K^{12}\) as a new independent quantity.  The latter
is still required if one seeks the positive variation \(v_{k,R}\), because
positive variation is not linear.

Each \(G_m\) itself contains its positive and inverted packets.  A second
application of \(|f+g|^2\le2(f^2+g^2)\), and the same gradient inequality,
absorbs that internal cross term.  The inverted packet is therefore a
factor-level issue in an upper bound, not a missing sign cancellation.  Its
spatial location must still be retained in the occupation estimate.

### 3.3 The cutoff/source representation is an alternative ledger

For the exact zero-frame, zero-pressure family, the R0.74P balance reduces
to

\[
 K_{k,R}=Q^{\eta}_{k,R}+Q^{\Delta}_{k,R}+F^G_{k,R},
 \tag{V.24}
\]

where

\[
 Q^{\eta}_{k,R}(t)
 ={\gamma_k\over2R}\int_{s_R}^t\!\!\int
   \eta_R'\Psi_k^R\,(b^2+G^2),
 \tag{V.25}
\]

\[
 Q^{\Delta}_{k,R}(t)
 ={\gamma_k\over2R}\int_{s_R}^t\!\!\int
   \eta_R\Delta\Psi_k^R\,(b^2+G^2),
 \tag{V.26}
\]

\[
 F^G_{k,R}(t)
 ={\gamma_k\over2R}\int_{s_R}^t\!\!\int
   \eta_R bG^2\partial_2\Psi_k^R.
 \tag{V.27}
\]

The \(\partial_1\Psi_k^R\) row integrates to zero because the field is
independent of \(x_1\); the pure \(b^3\partial_2\Psi_k^R\) row integrates
to zero because \(b\) is independent of \(x_2\); pressure and drift are
zero.  Expanding \(G^2\) in (V.25)--(V.27) gives exactly the R0.74Q
diagonal and cross terms.

Equations (V.24)--(V.27) must not be added to (V.16).  They are the signed
balance representation of the same clock, not extra completion pieces.
For a superlevel bound on \(I_R\), the direct representation (V.16) is the
clean one: \(\eta_R=1\) at the endpoint and \(0\le\eta_R\le1\) in the
accumulation.  The cutoff/source representation becomes necessary only when
one seeks \(v_{k,R}\), total variation, or a signed-flux conclusion.

## 4. Coarse upper budgets that already follow from the frozen equations

This section records bounds that can be proved without a new bridge
estimate.  They are amplitude ceilings, not duration estimates.

### 4.1 Global packet energy

Every \(G_m^\pm\) solves

\[
 (\partial_t+b\partial_2-\Delta_{23})G_m^\pm=0.
 \tag{V.28}
\]

Because \(b\) is independent of \(x_2\), its transport is skew in
\(L^2(\mathbb T^2)\).  The periodic heat-kernel initial data give

\[
 \|G_m^\pm(0)\|_2^2
 =R^6\|\partial K_{R^2}^{\rm per}\|_2^2
       \|K_{R^2}^{\rm per}\|_2^2
 \le CR^2.
 \tag{V.29}
\]

Hence

\[
 \sup_{0\le t\le65R^2}\|G_m(t)\|_2^2
 +\int_0^{65R^2}\|\nabla G_m(t)\|_2^2\,dt
 \le CR^2.
 \tag{V.30}
\]

Let the outer radius of the Euclidean padded support and its
lifted-multiplicity chord scale be

\[
 s_k:=\left(2^{k+1}+{1\over8}\right)R,
 \qquad
 \ell_k:=s_k+s_k^3.
 \tag{V.31}
\]

This chord cannot be capped by the length of one torus period, because
\(\Psi_k^R\) is a sum, not the indicator of the projected shell.  Indeed,
for fixed \(\widetilde x_2,\widetilde x_3\in(-\pi,\pi]\), Tonelli and the
\(x_1\)-tiling identity give

\[
\begin{aligned}
 \int_{\mathbb T}\Psi_k^R(x_1,x_2,x_3)\,dx_1
 =\sum_{(n_2,n_3)\in\mathbb Z^2}
   \int_{\mathbb R}
   \psi_k^R(y_1,\widetilde x_2+2\pi n_2,
                  \widetilde x_3+2\pi n_3)\,dy_1
 \le C\ell_k.
\end{aligned}
\tag{V.32}
\]

At most \(C(1+s_k^2)\) lifted pairs can meet the ball of radius \(s_k\),
and each corresponding \(y_1\)-chord has length at most \(2s_k\).
Consequently the left side of (V.32) is bounded by
\(C(s_k+s_k^3)=C\ell_k\), uniformly in \(k\).

Equations (V.19), (V.30), and (V.32) therefore prove

\[
 \boxed{
 \sup_tE_k^m(t)+D_k^m(65R^2)
 \le C H_{k\leftarrow m},
 \qquad
 H_{k\leftarrow m}:=\gamma_k\mathfrak a_m^2\ell_kR.}
 \tag{V.33}
\]

When \(s_k\lesssim1\), and in particular for every shell in the finite
central table (V.67), \(\ell_k\asymp s_k\asymp2^kR\), so

\[
 H_{k\leftarrow m}\asymp
 \gamma_k\mathfrak a_m^2\,2^kR^2.
 \tag{V.34}
\]

At the intended coordinate,

\[
 H_{k_i\leftarrow i}\asymp T.
 \tag{V.35}
\]

At the other target coordinate, the same coarse bound gives

\[
 {H_{k_2\leftarrow1}\over T}\asymp \Gamma_1^3,
 \qquad
 {H_{k_1\leftarrow2}\over T}\asymp \Gamma_1^{-3}.
 \tag{V.36}
\]

Harmless fixed factors involving \(\lambda\) and \(2\) are suppressed in
(V.35)--(V.36).  The first row is small by shell weight alone.  The second
is exponentially large until the vertical separation of packet 2 from
shell \(k_1\) is used.  R0.74Q's on-lobe dominance estimate does not supply
that whole-target-annulus \(L^2\) gain.

### 4.2 Common-shear scale

Put

\[
 V_k:=\int_{\mathbb T^3}\Psi_k^R(x)\,dx
     =\int_{\mathbb R^3}\psi_k^R(y)\,dy
     \le Cs_k^3,
 \qquad
 S_k:=\gamma_kB^2{V_k\over R}.
 \tag{V.37}
\]

The equality is the exact tiling identity for the periodization.  In
particular, \(V_k\) is a lifted multiplicity integral and cannot be capped
by \((2\pi)^3\) when the projected Euclidean shells overlap.

The maximum principle gives \(|\theta_R|\le1\).  Since
\(t\ge61R^2\) on the clock interval, one-dimensional heat smoothing gives
\(|\partial_3\theta_R|\le C/R\).  The endpoint and the four-
\(R^2\)-long viscous accumulation therefore obey

\[
 \boxed{\sup_{t\in I_R}K^b_{k,R}(t)\le CS_k.}
 \tag{V.38}
\]

For a target shell,

\[
 S_{k_i}\asymp\Gamma_iB^2L_i^3R^2,
 \qquad
 \Xi_i^{\rm sh}:={S_{k_i}\over T}
 \asymp {\Gamma_iB^2L_i^3\over A_*^2}.
 \tag{V.39}
\]

Here the matching lower scale follows directly from an explicit box.  Put
\[
 \mathcal B_i
 :=\{|x_1|<r_i/16,\ |x_2|<r_i/16,\
               3r_i/4<x_3<13r_i/16\}.
 \tag{V.39a}
\]
Since \(r_i=\lambda2^{k_i}R\), one has
\(3/4>1/\lambda\) and
\(171/256<(2/\lambda)^2\).  Hence
\(\mathcal B_i\subset A_{k_i}(R)\), so \(\Psi_{k_i}^R\ge1\) there, and
\(|\mathcal B_i|=r_i^3/1024\).  The saturation datum is one at distance
\(\asymp L_iR\) from its transition; the one-dimensional periodic heat
kernel therefore gives, uniformly for \(t\in I_R\),
\(\theta_R\ge1-Ce^{-cL_i^2}\) on \(\mathcal B_i\).  Keeping only the
nonnegative endpoint row in \(K^b\) proves
\[
 \inf_{t\in I_R}K^b_{k_i,R}(t)
 \ge c\,\Gamma_iB^2L_i^3R^2
 \quad\hbox{for all sufficiently large }L_i.
 \tag{V.39b}
\]
Thus
\(\Xi_i^{\rm sh}\ll\kappa\) is not merely a convenient sufficient
condition for (V.2); some condition of this type is necessary for a
uniform level-\(\kappa T\) theorem for the canonical clock.

Across all shells,
\(\sum_k\gamma_ks_k^3\le CR^3\) by super-Gaussian summation.  Therefore

\[
 \sum_{k\ge1}S_k\le CB^2R^2,
 \qquad
 \left(\sum_{k\ge1}S_k^2\right)^{1/2}\le CB^2R^2.
 \tag{V.40}
\]

Consequently, closing an all-shell upper at scale \(T=A_*^2R^2\) through
the direct shear budget (V.40) requires the stronger normalization

\[
 {B^2\over A_*^2}\lesssim1
 \quad\hbox{(and }B^2/A_*^2=o(1)\hbox{ if the shear is to be negligible).}
 \tag{V.41}
\]

Since \(B\asymp R^{-2}\), this is an amplitude condition on \(A_*\).  No
uniform estimate over every \(A_*>0\) allowed by R0.74U can hold: letting
\(A_*\downarrow0\) sends \(T\downarrow0\) while the nonzero shear clock
is unchanged.  At sufficiently small \(A_*\), the full terminal slab is a
\(K\)-superlevel set.

### 4.3 What the coarse cutoff ledger does and does not pay

For the central-chart shells used in the finite table below, the time-cutoff
row in (V.25) satisfies, packetwise,

\[
 \operatorname {TV}Q^{\eta,m}_{k,R}\le CH_{k\leftarrow m},
 \tag{V.42}
\]

because \(\eta_R'\ge0\) and \(\int\eta_R'\le1\).  The Laplacian row has
the same coarse scale,

\[
 \operatorname {TV}Q^{\Delta,m}_{k,R}\le CH_{k\leftarrow m},
 \tag{V.43}
\]

using \(|\Delta\Psi_k^R|\lesssim R^{-2}\), the four-
\(R^2\) clock interval, and (V.30)--(V.32).  The shear parts of
(V.42)--(V.43) are bounded by \(CS_k\).  Cross cutoff rows are absorbed by
the corresponding diagonal absolute rows.  An infinite outer-shell version
must instead use the inherited periodized derivative majorant before
super-Gaussian summation; (V.43) is not asserting a uniform unperiodized
formula beyond the central chart.

Still on this finite central table, the physical collar term is different.
A global-in-time estimate using only \(|b|\le B\),
\(|\nabla\Psi_k^R|\lesssim R^{-1}\), and (V.30) loses

\[
 \operatorname {TV}F^{m}_{k,R}
 \le C(BR)H_{k\leftarrow m},
 \qquad BR\asymp R^{-1}.
 \tag{V.44}
\]

The missing factor is precisely the time for which a width-\(R\) packet
meets a width-\(R\) cutoff collar.  A moving-centre collar occupation lemma
would replace an \(R^2\) time bound by an \(R^3\) crossing bound and remove
the factor \(BR\).  Thus the cutoff/time rows cannot be omitted from a
positive-variation or signed-flux theorem, even though they are not extra
terms in the direct nonnegative clock (V.16).

## 5. The missing finite-table whole-annulus occupation estimate

This section is strictly restricted to the six central-chart pairs
\[
 k\in\{k_1-1,k_1,k_2\},\qquad m\in\{1,2\},
\]
recorded as the finite set (V.67) below.  In particular, (V.46)--(V.50)
are not statements for arbitrary \(k\).

For a packet sign \(\sigma\in\{+,-\}\), let

\[
 c_m^\sigma(t)=(0,\sigma Q_m(t),\sigma h_m)
 \tag{V.45}
\]

be its reference centre.  Let \(\mathcal A_k^{\rm pad}(R)\) denote the
central-lift support of the padded shell cutoff, and set

\[
 d_{k,m}(t)
 :=R^{-1}\operatorname {dist}
   \bigl(c_m^+(t),\mathcal A_k^{\rm pad}(R)\bigr).
 \tag{V.46}
\]

Radial symmetry makes the same distance valid for the inverted centre.

For this finite table, the analytic estimate needed for a completed-clock
upper route has the following form.  It is stated here as a target, not as
a proved theorem.

### Proposed finite-table annular packet-occupation proposition

There should exist absolute \(c,C>0\) and explicit remainders
\(\varepsilon_{k,m}\) such that, for the six pairs above and uniformly on
the full clock interval,

\[
\begin{aligned}
 &{\gamma_k\mathfrak a_m^2\over R}
   \int\Psi_k^R
   \left(|G_m(t)|^2+R^2|\nabla G_m(t)|^2\right)\\
 &\qquad\le
 C H_{k\leftarrow m}
 \left[e^{-c(d_{k,m}(t)-C)_+^2}+\varepsilon_{k,m}\right].
\end{aligned}
\tag{V.47}
\]

The estimate must include both inversion partners and all periodic copies
of each packet, but its shell index remains in the central table.  It must
be global over the selected annulus; the R0.74F estimate near
\(|x_3-h_m|\le R\) is not enough.

Provided the weighted flat remainder is below half the tested level,

\[
 CH_{k\leftarrow m}\varepsilon_{k,m}\le {z\over2}T,
 \tag{V.47a}
\]

the speed bound (V.10) would then give the distribution estimate

\[
\begin{aligned}
 &\left|\left\{t\in I_R:
 {\gamma_k\mathfrak a_m^2\over R}
 \int\Psi_k^R|G_m(t)|^2\ge zT\right\}\right|\\
 &\quad\le
 CR^3\left[
 2^k+1+\sqrt{\log_+{C\mathcal A^I_{k,m}\over z}}
 \right],
\end{aligned}
\tag{V.48}
\]

where the instantaneous and full-clock amplifications must be distinguished:

\[
 \mathcal A^I_{k,m}
 :={H_{k\leftarrow m}\over T}
   \sup_{t\in I_R}e^{-c(d_{k,m}(t)-C)_+^2},
 \qquad
 \mathcal A^{\rm clk}_{k,m}
 :={H_{k\leftarrow m}\over T}
   \sup_{t\in[s_R,65R^2]}e^{-c(d_{k,m}(t)-C)_+^2}.
 \tag{V.48a}
\]

The same estimate should imply the integrated viscous budget

\[
 D_k^m(65R^2)
 \le CT\,\mathcal A^{\rm clk}_{k,m}(2^kR+R)
      +CH_{k\leftarrow m}\varepsilon_{k,m}
      +\operatorname {Err}_{k,m}^{\rm occ}.
\tag{V.49}
\]

For the derivative-collar support, whose radial thickness is \(O(R)\), the
same proof should give

\[
 \operatorname {TV}F^m_{k,R}
 \le CT\,\mathcal A^{\rm clk}_{k,m}
      +\operatorname {Err}_{k,m}^{\rm collar},
\tag{V.50}
\]

rather than the coarse loss (V.44).

Without (V.47a), the right side of (V.48) must contain the additional
trivial term
\(R^2\mathbf 1_{\{CH_{k\leftarrow m}\varepsilon_{k,m}>zT/2\}}\).
The three lines have different uses:

- (V.47)--(V.48) control endpoint/off-corridor mass and its time set;
- (V.49) decides whether viscosity leaves a permanent level-\(T\) floor;
- (V.50), together with (V.42)--(V.43), is needed only for positive
  variation and signed flux.

One viable proof route uses the exact stochastic representation, conditioned
Brownian bridges, and the monotone centre speed.  A maximum-principle
\(L^\infty\) estimate loses the Gaussian location and cannot prove
(V.48).  The remainder must be controlled after multiplying by the
amplitude and shell-weight ratios; an unweighted \(o(1)\) error is
insufficient.

## 6. Conditional target-coordinate superlevel upper bound

The algebra after (V.47)--(V.49) is short and exact.  For a fixed target
\(k_i\), define the persistent baseline

\[
 \mathcal B_i
 :=\sup_{t\in I_R}K^b_{k_i,R}(t)
   +2\sum_{m=1}^2D_{k_i}^m(65R^2)
   +D^{\rm an}_{k_i,R}(65R^2),
 \tag{V.51}
\]

where the last term is zero for the smooth family.  By (V.23),

\[
 K_{k_i,R}(t)
 \le\mathcal B_i+2E_{k_i}^1(t)+2E_{k_i}^2(t).
 \tag{V.52}
\]

If

\[
 \boxed{\mathcal B_i\le{\kappa\over2}T,}
 \tag{V.53}
\]

then

\[
 \{K_{k_i,R}\ge\kappa T\}\cap I_R
 \subset
 \bigcup_{m=1}^2
 \left\{E_{k_i}^m\ge{\kappa\over8}T\right\}\cap I_R.
 \tag{V.54}
\]

Since \(E_k^m\) is one half of the left side in (V.48), this application
uses \(z=\kappa/4\) and requires the explicit endpoint-remainder gates
\[
 CH_{k_i\leftarrow m}\varepsilon_{k_i,m}
 \le{\kappa\over8}T,\qquad m=1,2.
 \tag{V.54a}
\]
Under (V.54a), applying (V.48) gives

\[
\begin{aligned}
 |\{K_{k_i,R}\ge\kappa T\}\cap I_R|
 \le{}&CR^3\sum_{m=1}^2
 \left[
 2^{k_i}+1+\sqrt{\log_+{C\mathcal A^I_{k_i,m}\over\kappa}}
 \right].
\end{aligned}
\tag{V.55}
\]

In this two-packet family every shell-weight and packet-amplitude ratio has
logarithm \(O(L_2^2)\).  Hence, if (V.53) and (V.54a) hold and the remaining
occupation errors obey the required weighted scale, (V.55) reduces to

\[
 \boxed{
 |\{t\in I_R:K_{k_i,R}(t)\ge\kappa T\}|
 \le C_\kappa L_2R^3
 \asymp C_\kappa L_iR^3.}
 \tag{V.56}
\]

This is the precise route to the desired target-coordinate upper.  Notice
that a second packet whose instantaneous off-target mass is much larger
than \(T\) does not by itself destroy the duration scale: its exponential
height only contributes a square root of a logarithm in (V.55).  Its
**accumulated dissipation**, however, enters (V.53) without a logarithm and
can destroy the conclusion.

Using (V.38)--(V.39) and (V.49), a transparent sufficient form of (V.53)
is

\[
 \boxed{
 \Xi_i^{\rm sh}
 +\sum_{m=1}^2
   \left[
    \mathcal A^{\rm clk}_{k_i,m}(2^{k_i}R+R)
    +{H_{k_i\leftarrow m}\varepsilon_{k_i,m}\over T}
   \right]
 +{D^{\rm an}_{k_i,R}(65R^2)\over T}
 +{\operatorname {Err}_i^{\rm occ}\over T}
 \le c\kappa.}
 \tag{V.57}
\]

Here \(\operatorname {Err}_i^{\rm occ}\) denotes the sum of the non-flat
occupation errors in (V.49); the flat
\(H_{k_i\leftarrow m}\varepsilon_{k_i,m}\) rows are displayed separately.
For the intended packet,
\(\mathcal A^{\rm clk}_{k_i,i}\asymp1\), so its expected viscous residue is
\(O(TL_iR)\).  R0.74U assumes only
\(L_2R\le5/144\), not \(L_2R=o(1)\); therefore even the intended diagonal
viscosity needs either an explicit constant comparison with \(\kappa\) or
the stronger asymptotic \(L_2R\to0\).

## 7. Obstruction-first audit: the adjacent inward shell

The all-shell route has a sharper preliminary issue.  Consider packet
\(m\) at its re-centring time \(\tau_m\), and its adjacent inward shell
\(k_m-1\).  The weight ratio is exact:

\[
 {\gamma_{k_m-1}\over\Gamma_m}
 =\Gamma_m^{-3/4}
 =\exp\!\left({3\over4}c_\gamma L_m^2\right).
 \tag{V.58}
\]

At \(Q_m(\tau_m)=0\), the packet height is \(c_hL_mR\), while the outer
radius of shell \(k_m-1\) is \(L_mR/\lambda\).  The leading vertical gap
in packet units is

\[
 d_0L_m,
 \qquad
 d_0:=c_h-{1\over\lambda}
 ={433\over1008}.
 \tag{V.59}
\]

For the free derivative-heat comparator, the total heat age is

\[
 a_mR^2:=R^2+\tau_m,
 \qquad 65\le a_m\le66.
 \tag{V.60}
\]

Squaring the vertical heat kernel costs
\(\exp[-d_0^2L_m^2/(2a_m)+O(L_m)]\).  After inserting (V.58), the leading
exponent is

\[
 \chi(a_m)
 :={3\over4}c_\gamma-{d_0^2\over2a_m}.
 \tag{V.61}
\]

This exponent is strictly positive throughout the inherited slab.  At the
earliest age,

\[
 \boxed{
 \chi(65)
 ={2\over1323}-{(433/1008)^2\over130}
 ={12191\over132088320}>0,}
 \tag{V.62}
\]

and at the latest age,

\[
 \chi(66)={15263\over134120448}>0.
 \tag{V.63}
\]

A width-\(R\) strip just inside the outer face of shell \(k_m-1\) has an
\(x_1\)-chord of order \(\sqrt{L_m}R\).  Thus the free comparator predicts
the lower scale

\[
 {E^{m,\rm free}_{k_m-1}(\tau_m)\over T}
 \gtrsim L_m^{-1/2}
 \exp\!\left[(\chi(65)-o(1))L_m^2\right].
 \tag{V.64}
\]

Equation (V.64) records the exact leading-exponent arithmetic and the
geometric polynomial predicted by the free comparator.  A stripwise lower
bound is part of Proposition V.0 below; (V.64) is not yet a lower bound for
the common-shear solution.  The present R0.74F comparison is proved near
\(|x_3-h_m|\le R\); it does not reach the remote strip (V.59).  A relative
bridge estimate on that strip, including the other packet and the inversion
partner, is still required.

This sign cannot be ignored in an upper memo.  If the common-shear packet
is relatively comparable to the free packet on that strip and no other
packet cancels it, then:

- the adjacent inward endpoint clock is exponentially larger than \(T\);
- a matching \(O(T)\) all-shell or \(Y_2\) upper bound is false for this
  frozen placement;
- for the two adjacent packets, the candidate large shells
  \(k_1-1\) (from packet 1) and \(k_2-1=k_1\) (from packet 2) are distinct,
  so deleting one fixed coordinate does not automatically remove both.

At exponential accuracy the same calculation suggests a candidate
viscous-residue gate for the inner target coordinate.  Packet 2 has the
candidate exponential amplification \(\exp(4\chi L_1^2)\); the as-yet
unproved remote \(H^1\) and occupation estimates determine its polynomial
prefactor.  Even taking the larger slab value \(\chi(66)\), the original
R0.74Q scale
\(R=e^{-\rho L_1^2}\), \(\rho=1/320\), has the positive reserve

\[
 \rho-4\chi(66)
 ={447593\over167650560}>0.
 \tag{V.65}
\]

Hence that particular scale has enough exponential room to beat every fixed
polynomial, if V.0--V.1 validate the candidate exponent.  The generalized
R0.74U conditions give no such uniform implication: they allow, for example,
\(R\) of polynomial size in \(L_1^{-1}\).  A candidate sufficient gate, at
exponential accuracy, has the form

\[
 P(L_1)R\,e^{4\chi(66)L_1^2}\longrightarrow0,
 \qquad
 \liminf_{R\downarrow0}{\log(1/R)\over L_1^2}>4\chi(66)
 \ \Longrightarrow\ \hbox{this for every fixed polynomial }P.
 \tag{V.66}
\]

The polynomial \(P\) must be fixed by V.0--V.1.  R0.74U's one-sided
survival reserve does not imply this candidate gate.

## 8. The smallest next proposition and the order of attack

### Proposition V.0 to prove first — remote adjacent-inward comparison

For each \(m\in\{1,2\}\), choose an explicit width-\(R\) core strip inside
the outer face of \(A_{k_m-1}(R)\) and a fixed horizontal derivative-kernel
interval.  Prove one of the following mutually exclusive outcomes,
uniformly for \(\tau_m\in\overline I_R\):

1. **relative survival:** the common-shear packet on that strip is bounded
   below by a fixed fraction of its free derivative-heat comparator, all
   periodic windings and inversion partners included, and the other packet
   is quantitatively noncancelling; or
2. **relative failure with mechanism:** identify a common-shear displacement
   term whose size is comparable to or larger than the free tail and give
   its sharp weighted exponent.

The proposition must be relative to the free tail.  The absolute
\(o(1)\) error used for the main lobe is much larger than the remote signal
after the shell/amplitude weights are inserted and cannot decide (V.64).

This is the minimum next result because it decides whether the proposed
all-shell \(O(T)\) upper statement is true before a much larger upper-ledger
proof is attempted.  If outcome 1 holds, the frozen all-shell matching upper
route is closed by an explicit obstruction; only the target-coordinate
duration question remains.  If outcome 2 holds, its sharp exponent becomes
an input to \(\mathcal A^I_{k,m}\) and
\(\mathcal A^{\rm clk}_{k,m}\) in (V.47)--(V.57).

### Proposition V.1 only after V.0 — weighted annular occupation

Prove (V.47)--(V.50), first for the finite set

\[
 k\in\{k_1-1,k_1,k_2\},\qquad m\in\{1,2\},
 \tag{V.67}
\]

with explicit exponent tables.  This finite set contains both target
coordinates and both adjacent-inward tests.  Only after the finite table
closes should an all-\(k\) extension be attempted.  Such an extension is a
separate lifted-copy summation proposition: it must replace the single
central-lift distance (V.46) by distances to every relevant Euclidean lift,
count their multiplicities, and only then combine the result with the
super-Gaussian shell weights.  Neither (V.46) nor (V.47)--(V.50) currently
asserts that extension.

The proof order should be:

1. exact all-winding stochastic formula on the remote vertical strips;
2. conditional bridge localization relative to the free kernel;
3. endpoint \(L^2\) and instantaneous \(H^1\) envelopes;
4. time occupation via (V.10);
5. cumulative viscosity and derivative-collar occupation;
6. diagonal summation, then cross absorption by (V.22);
7. common shear and, only if leaving the smooth family, defect.

## 9. Exact failure conditions

Each of F1--F6 is a gate for a level-\(\kappa T\) target-coordinate upper
bound of the form (V.2).  F7 is the additional scope gate for an all-shell
extension.

### F1. Common-shear floor

If \(\sup_{I_R}K^b_{k_i,R}\) is not below a strict fraction of
\(\kappa T\), endpoint localization of the packets cannot prove (V.2).
If the shear endpoint is itself at least \(\kappa T\) throughout the slab,
then the superlevel set has measure \(R^2\).  Uniformity over arbitrary
\(A_*>0\) is therefore impossible.

### F2. Viscous or anomalous persistent floor

Let

\[
 D^{\rm tot}_{k_i}(t)
 :=D^b_{k_i}(t)+D^G_{k_i}(t)+D^{\rm an}_{k_i}(t).
 \tag{V.68}
\]

This function is nondecreasing.  If
\(D^{\rm tot}_{k_i}(t_*)\ge\kappa T\), then

\[
 [t_*,65R^2)\subset\{K_{k_i,R}\ge\kappa T\}.
 \tag{V.69}
\]

Thus a packet may leave geometrically while its clock never falls.  This is
the decisive distinction between a lobe residence estimate and a completed-
clock residence estimate.

### F3. Nonintegrable amplified tail remainder

An error that tends to zero before amplitude weighting may become large
after multiplication by \(\gamma_k/\Gamma_m\).  Every remainder in
(V.47)--(V.50) must be tested in the normalized quantities
\(\mathcal A^I_{k,m}\), \(\mathcal A^{\rm clk}_{k,m}\), and (V.57).
R0.74Q's pointwise dominance on the intended lobe does not perform that
test on a whole off-target shell.

### F4. Generalized scale too slow

The inherited conditions (V.5) do not force the candidate exponential
gate (V.66), or even \(L_2R\to0\).  A proof that uses either property must
state it as an additional hypothesis.  It may not be read into the
R0.74U family.

### F5. Full cutoff interval instead of the terminal plateau

The duration target (V.2) is posed on \(I_R\), where \(\eta_R=1\).  On
the full interval \((s_R,t_0)\), the inherited cutoff may ramp over an
\(O(R^2)\) interval.  The current cutoff class does not force an
\(O(L_iR^3)\) support for that ramp.  A full-cutoff-interval duration theorem
would require an additional time-profile hypothesis.

### F6. Confusing height, duration, and variation

A duration bound for \(\{K_k\ge\kappa T\}\) does not bound
\(v_{k,R}=\operatorname {Var}^+K_{k,R}\).  Repeated sublevel excursions can
create large positive variation with small superlevel measure.  Conversely,
the coarse inequality \(K_k\le v_k\) gives only an amplitude ceiling, not a
nontrivial duration estimate.  Any claim about \(Y_{2,R}^{\rm sf}\) must
return to (V.24)--(V.27) and pay the time-cutoff, Laplacian-cutoff, and
physical-collar variations.

### F7. Reusing one central-lift distance at large shell index

For large \(k\), the projected cutoff carries many Euclidean lifts.  The
single distance \(d_{k,m}\) in (V.46) neither finds every relevant lift nor
pays its multiplicity.  Thus applying (V.47)--(V.50) outside the finite
central table (V.67) is invalid until the independent lifted-copy
summation proposition described after (V.67) is proved.

## 10. What can and cannot follow

### Established in this memo

- the exact good-time three-row nonnegative completion and the separate
  canonical-AC hard-time convention in (V.16);
- the exact shear/packet splitting (V.17)--(V.18);
- the exact two-packet diagonal/cross decomposition and safe absorption
  (V.19)--(V.23);
- the reduced cutoff/source balance (V.24)--(V.27), including every term
  that survives the frozen symmetries;
- the lifted-multiplicity global-energy/chord packet ceiling
  (V.31)--(V.36);
- the periodized-volume common-shear scale budget (V.37)--(V.41);
- the exact conditional superlevel algebra (V.51)--(V.57), whose analytic
  inputs remain proposed on the finite table; and
- the exact positive free-comparator exponent (V.58)--(V.63).

### Not established

- the proposed finite-table whole-annulus localization estimates
  (V.47)--(V.50);
- any all-\(k\) lifted-copy occupation and summation extension of those
  estimates;
- the target-coordinate upper bound (V.56);
- relative survival or noncancellation on the adjacent inward strip;
- a full all-shell upper, a matching upper for \(Y_{2,R}^{\rm sf}\), or a
  bound for \(\mathfrak L^K_{1,R}\);
- a signed cumulative-flux upper or lower inferred from clock residence;
- any anomalous-defect estimate for a nonsmooth suitable weak solution; or
- any arbitrary-clock extraction, scale contraction, regularity,
  singularity, or Navier--Stokes Millennium conclusion.

The immediate research action is therefore obstruction-first: prove
Proposition V.0.  Only if it does not produce the predicted adjacent-inward
clock obstruction should the finite-shell occupation proposition V.1 be
developed into the conditional target-superlevel theorem (V.56).

**NOT CLAY.**

<!-- R074V_STEP21_END -->
