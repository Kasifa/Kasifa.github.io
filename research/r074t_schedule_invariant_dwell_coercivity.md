# R0.74T Step 19 — schedule-invariant outer-lobe coercivity and the exponential dwell barrier

## 0. Result and exact scope

Step 18 reduced the fixed-deletion route to the completed-clock simultaneous
height

\[
 \mathfrak L^K_{N,R}(D)
 :=\inf_{\#S\le N}\sup_{t\in D}\sum_{k\notin S}K_{k,R}(t).
\]

The disjoint triangular clocks showed that different shells may in principle
reach their peaks at different times.  This note asks the next narrower
question: can merely separating two packet lobes in time make their completed
clock witness cheap relative to the Version-M payment?

At the explicit lobe-floor witness level, the answer is negative for every
construction that retains the inherited outer-lobe geometry and a
non-negligible dwell interval.

1. A persistent outer-lobe kinetic floor \(h_2\) on an interval of length
   \(\theta R^3\) forces

   \[
    P_R^M\ge
    2\sqrt2\,\theta h_2^{3/2}R
    \Gamma _2^{-5/4}L_2^{-1/2}
   \]

   for the exact R0.74Q lobe volume and shell weight.  This is just
   Hölder's inequality inside the nonnegative exterior velocity-cubic row;
   it does not use overlap with the inner lobe.
2. The common-shear packet construction can in fact be re-centred so that two
   adjacent-shell lobes occupy two prescribed admissible windows inside the
   terminal slab.  In particular, two disjoint \(R^3\)-long lobe windows are
   realized by one exact smooth periodic Navier--Stokes solution.
3. Two target shells with persistent floors \(h_1,h_2\), on arbitrary and
   possibly disjoint positive-measure subsets of the observation domain, give
   \(\mathfrak L^K_{1,R}(D)\ge\min(h_1,h_2)\).  They do **not** directly
   lower-bound the stopped-flux functional
   \(\mathfrak H^{\rm fix}_{1,R}\).
4. For the inherited adjacent-shell parameters
   \(L_2=2L_1\),
   \(\Gamma _2=e^{-c_\gamma L_2^2}\), and the sufficient bridge-survival
   window of R0.74Q, bounded payment relative to the lobe-floor witness
   requires

   \[
    \log\theta
    \le -(5c_\gamma-a_S)L_1^2-d_L
       +\frac12\log L_2+O(1),
   \]

   where \(d_L=a_SL_1^2-\log(1/R)\to+\infty\).  The exact positive margin is

   \[
    5c_\gamma-a_S=\frac{603445}{89413632}>0.
   \]

Thus changing the relative peak times does not rescue the inherited
\(R^3\)-long packet-lobe lower witness: its normalized dwell is
\(\theta=1\).  Any escape based on that witness must instead create an
   exponentially collapsing maximal outer dwell while preserving its kinetic
   floor and all PDE gates, with no comparable floor on a longer interval.

This is a rigorous local coercivity theorem and a route reduction.  It does
not upper-bound the full clock, prove the open estimate for
\(\mathfrak L^K_{1,R}\), prove the Step 18 fixed-deletion gate, prove an
arbitrary-real-time scheduling theorem, prove singularity or regularity, or solve the
Navier--Stokes Millennium problem.  **NOT CLAY.**

No simulation or numerical fit is used.

<!-- R074T_STEP19_STATUS_LOCAL_COERCIVITY_PROVED -->
<!-- R074T_STEP19_STATUS_DWELL_THRESHOLD_PROVED -->
<!-- R074T_STEP19_STATUS_FULL_CLOCK_GATE_OPEN -->

## 1. Frozen Version-M setting

Fix \(R>0\), a terminal time \(t_0\), and a smooth periodic unforced
Navier--Stokes solution in the R0.74P Version-M setting.  The complete
payment contains the nonnegative exterior velocity row

\[
 P_R^M\ge \mathcal G_u,
 \qquad
 \mathcal G_u
 :=(2R)^{-2}\int_{I_{2R}}\!\int_{\mathbb T^3}
 W_{2R}(x)|u(t,x)|^3\,dx\,dt.
 \tag{T.1}
\]

Let \(k_2\) be an outer target shell and write

\[
 L_2:=\lambda2^{k_2},
 \qquad
 \Gamma _2:=\gamma_{k_2}=e^{-c_\gamma L_2^2}.
 \tag{T.2}
\]

The corresponding R0.74Q physical lobe lies in

\[
 A_{k_2}(R)=A_{k_2-1}(2R).
 \tag{T.3}
\]

Consequently the exterior weight on that lobe is

\[
 W_{2R}\ge\gamma_{k_2-1}
 =e^{-(c_\gamma/4)L_2^2}=\Gamma _2^{1/4}.
 \tag{T.4}
\]

Let \(J_2\subset I_R\subset I_{2R}\) be measurable and set

\[
 |J_2|=\theta R^3,
 \qquad \theta>0.
 \tag{T.5}
\]

For every \(t\in J_2\), let \(\Omega _2(t)\) be a measurable target lobe.
Assume also that the moving set
\(\{(t,x):t\in J_2,\ x\in\Omega _2(t)\}\) is measurable in
\(J_2\times\mathbb T^3\), and that

\[
 \Omega _2(t)\subset A_{k_2}(R),
 \qquad
 |\Omega _2(t)|=\frac1{16}L_2R^3,
 \qquad
 \Psi_{k_2}^R=1\quad\hbox{on }\Omega _2(t).
 \tag{T.6}
\]

The time cutoff is one on \(I_R\).  Define the persistent normalized lobe
kinetic floor

\[
 h_2
 :=\operatorname*{ess\,inf}_{t\in J_2}
 \frac{\Gamma _2}{2R}
 \int_{\Omega _2(t)}|u(t,x)|^2\,dx.
 \tag{T.7}
\]

We assume \(h_2>0\).  Since the defect-completed clock is a sum of its
nonnegative endpoint kinetic and accumulated dissipation terms, (T.6)--(T.7)
give

\[
 K_{k_2,R}(t)\ge h_2
 \quad\hbox{for almost every }t\in J_2.
 \tag{T.8}
\]

The inclusion \(J_2\subset I_R\) is needed for (T.8), because that is where
the endpoint time cutoff equals one.  The cubic estimate below itself only
needs \(J_2\subset I_{2R}\).

## 2. Exact schedule-invariant coercivity

### Lemma 2.1 — one persistent outer lobe pays cubically

Under (T.1)--(T.7),

\[
 \boxed{
 P_R^M\ge
 2\sqrt2\,\theta h_2^{3/2}R
 \Gamma _2^{-5/4}L_2^{-1/2}.}
 \tag{T.9}
\]

Equivalently,

\[
 \boxed{
 (P_R^M)^{2/3}
 \ge 2\Lambda _2h_2,\qquad
 \Lambda _2
 :=\theta^{2/3}R^{2/3}
 \Gamma _2^{-5/6}L_2^{-1/3}.}
 \tag{T.10}
\]

**Proof.**  For almost every \(t\in J_2\), spatial Hölder gives

\[
 \int_{\Omega _2(t)}|u|^3
 \ge |\Omega _2(t)|^{-1/2}
 \left(\int_{\Omega _2(t)}|u|^2\right)^{3/2}.
 \tag{T.11}
\]

Equations (T.6)--(T.7) therefore imply

\[
 \begin{aligned}
 \int_{\Omega _2(t)}|u|^3
 &\ge
 4L_2^{-1/2}R^{-3/2}
 \left(\frac{2R}{\Gamma _2}h_2\right)^{3/2}\\
 &=2^{7/2}h_2^{3/2}
   \Gamma _2^{-3/2}L_2^{-1/2}.
 \end{aligned}
 \tag{T.12}
\]

Restrict the nonnegative integral in (T.1) to the lobe, then use (T.4),
(T.5), and (T.12):

\[
 \begin{aligned}
 P_R^M
 &\ge(2R)^{-2}\Gamma _2^{1/4}
 \int_{J_2}\!\int_{\Omega _2(t)}|u|^3\,dx\,dt\\
 &\ge
 2\sqrt2\,\theta h_2^{3/2}R
 \Gamma _2^{-5/4}L_2^{-1/2}.
 \end{aligned}
 \tag{T.13}
\]

This proves (T.9).  Since
\((2\sqrt2)^{2/3}=2\), taking the \(2/3\) power proves (T.10).
\(\square\)

Nothing in the proof names an inner packet, its target time, or an overlap
between target intervals.  The estimate is therefore invariant under every
relative schedule for which the outer lobe hypotheses remain true.

### Corollary 2.2 — robust volume and weight constants

If (T.4) and (T.6) are weakened, for constants
\(c_W,C_\Omega>0\), to

\[
 W_{2R}\ge c_W\Gamma _2^{1/4},
 \qquad
 |\Omega _2(t)|\le C_\Omega L_2R^3,
 \tag{T.14}
\]

then

\[
 P_R^M\ge
 2^{-1/2}c_WC_\Omega^{-1/2}
 \theta h_2^{3/2}R
 \Gamma _2^{-5/4}L_2^{-1/2}.
 \tag{T.15}
\]

For \(c_W=1\) and \(C_\Omega=1/16\), (T.15) is exactly (T.9).

## 3. Two clocks at arbitrary times

Let \(k_1\ne k_2\), let \(J_i\subset D\) be arbitrary measurable terminal
sets of positive measure, and suppose

\[
 K_{k_i,R}(t)\ge h_i>0
 \quad\hbox{for almost every }t\in J_i,\qquad i=1,2.
 \tag{T.16}
\]

No overlap between \(J_1\) and \(J_2\) is assumed.  For the completed-clock
fixed-deletion functional with budget one,

\[
 \boxed{
 \mathfrak L^K_{1,R}(D)\ge h_*:=\min(h_1,h_2).}
 \tag{T.17}
\]

Indeed, any set \(S\) with \(\#S\le1\) leaves at least one of
\(k_1,k_2\) undeleted.  Taking a time in that coordinate's target set and
using nonnegativity of all clocks proves (T.17), after which the infimum over
\(S\) is harmless.

Combining (T.10) with \(h_2\ge h_*\) gives

\[
 \boxed{(P_R^M)^{2/3}\ge2\Lambda _2h_*.}
 \tag{T.18}
\]

Equations (T.17)--(T.18) have a deliberately one-sided interpretation.  They
show that the explicit lower witness \(h_*\) for \(\mathfrak L^K_{1,R}\)
cannot simultaneously dominate the payment when \(\Lambda _2\) is large.
They do **not** give

\[
 (P_R^M)^{2/3}\gtrsim\mathfrak L^K_{1,R}(D),
 \tag{T.19}
\]

because other times, shells, or accumulated dissipation may make the full
functional much larger than \(h_*\).  Nor may (T.17) be rewritten with
Step 18's \(\mathfrak H^{\rm fix}\), which is built from stopped forward
flux increments \(z_k\), not from \(K_k\).  The only proved bridge between
those functionals carries the known payment terms and has the direction
recorded in Step 18 (S.483)--(S.484).

## 4. The exponential dwell threshold

Now consider a sequence indexed by \(n\), with
\(L_{1,n}\to\infty\), \(0<R_n<1\), and the inherited adjacent-shell
parameters

\[
 L_2=2L_1,
 \qquad
 \Gamma _2=e^{-c_\gamma L_2^2},
 \qquad
 S:=\log\frac1R,
 \tag{T.20}
\]

with

\[
 c_\gamma=\frac8{3969},
 \qquad
 a_S=\frac{75}{22528}.
 \tag{T.21}
\]

For readability, the index \(n\) is suppressed in (T.20)--(T.26); every
limit in this section is taken along the displayed sequence.

The inherited R0.74F proof closes its inner-packet shift error in the
sufficient survival window

\[
 S-a_SL_1^2\longrightarrow-\infty.
 \tag{T.22}
\]

This is a condition for that proof, not a necessary condition for every
possible packet.  Write

\[
 d_L:=a_SL_1^2-S\longrightarrow+\infty.
 \tag{T.23}
\]

Substitution of (T.20)--(T.23) into (T.10) gives the exact logarithmic
identity

\[
 \boxed{
 \log\Lambda _2
 =\frac23\left[
 \log\theta+(5c_\gamma-a_S)L_1^2+d_L
 -\frac12\log L_2\right].}
 \tag{T.24}
\]

The exponent reserve is strictly positive:

\[
 \boxed{
 5c_\gamma-a_S
 =\frac{40}{3969}-\frac{75}{22528}
 =\frac{603445}{89413632}>0.}
 \tag{T.25}
\]

Therefore the following statements are immediate.

1. If \(\theta=1\), then \(\Lambda _2\to\infty\).
2. More generally, if

   \[
    \log\theta+(5c_\gamma-a_S)L_1^2+d_L
       -\frac12\log L_2\longrightarrow+\infty,
   \tag{T.26}
   \]

   then \((P_R^M)^{2/3}/h_*\to\infty\).
3. Consider a sequence of such configurations for which

   \[
    \sup_n\frac{(P_{R_n}^M)^{2/3}}{h_{*,n}}<\infty.
   \tag{T.27}
   \]

   Equation (T.18) first forces \(\Lambda _{2,n}=O(1)\), and solving its
   definition for the dwell gives the exact necessary bound

   \[
    \boxed{
    \theta_n\le C L_{2,n}^{1/2}
    \exp\!\left[S_n-\frac54c_\gamma L_{2,n}^2\right]
    =C L_{2,n}^{1/2}
    e^{-(5c_\gamma-a_S)L_{1,n}^2-d_{L,n}}.}
   \tag{T.28}
   \]

   Equivalently,

   \[
    \boxed{
    \log\theta
    \le-(5c_\gamma-a_S)L_1^2-d_L
       +\frac12\log L_2+O(1).}
   \tag{T.29}
   \]

The R0.74F and R0.74Q lobe interval is
\(J=(t_0-R^3,t_0)\), hence \(\theta=1\).  Arbitrarily shifting an inner
lobe relative to this outer interval never appears in (T.24) and cannot
alter the conclusion.

Equations (T.28)--(T.29) are the exact escape budget for the present
mechanism.  An asynchronous construction escaping this obstruction would
have to make the maximal available outer persistence exponentially short,
with no comparable kinetic floor on a longer interval; merely restricting an
already long-lived lobe to a shorter subinterval does not change the payment
it already incurred.

## 5. Recovery of the packet-amplitude formula

For the explicit common-shear packet family, all-lobe dominance gives a
constant \(c_0>0\) such that \(|u|\ge c_0\mathfrak a_2\) on the outer
lobe.  With (T.6),

\[
 h_2\ge c\Gamma _2\mathfrak a_2^2L_2R^2.
 \tag{T.30}
\]

Substitution into (T.9) recovers, for an arbitrary normalized dwell
\(\theta\),

\[
 P_R^M
 \ge c\theta\mathfrak a_2^3
 \Gamma _2^{1/4}L_2R^4.
 \tag{T.31}
\]

At \(\theta=1\), this is R0.74Q (Q.168).  The useful route clarification is
that its proof
needs only the outer lobe: simultaneity with every other target is absent
from the coercive step.

This amplitude recovery is conditional on retaining the lobe, its shell
inclusion, and its dominance inside one exact common-shear solution.  Section
7 verifies those inputs for independently prescribed terminal phases inside
the inherited admissible slab; it makes no assertion outside that slab.

## 6. Sharp abstract stress tests

The powers in (T.9) cannot be improved using only its measure-theoretic
hypotheses.  Take a spacetime rectangle with
\(|J_2|=\theta R^3\),
\(|\Omega _2|=L_2R^3/16\), constant shell weight
\(\Gamma _2^{1/4}\), and a constant vector field of magnitude \(A\) on the
rectangle.  Then

\[
 h_2=\frac{\Gamma _2}{32}A^2L_2R^2,
 \tag{T.32}
\]

and equality holds in the spatial Hölder step.  Direct substitution gives
exactly the powers

\[
 \theta^1h_2^{3/2}R^1
 \Gamma _2^{-5/4}L_2^{-1/2}.
 \tag{T.33}
\]

Likewise, sending \(\theta\downarrow0\) with the instantaneous height held
fixed makes the cubic payment vanish linearly in \(\theta\).  Thus no
peak-only estimate can replace the persistence input in Lemma 2.1.

These rectangles are **ABSTRACT SHARPNESS TESTS**.  They are not divergence-
free periodic solutions, do not realize the Version-M ledger, and are not
Navier--Stokes counterexamples.

## 7. Two genuinely asynchronous packet lobes

The coercivity lemma did not require construction of an asynchronous family.
For completeness, the existing common-shear estimates also allow such a
family inside the admissible terminal slab.  Work along the sequence in
Section 4, suppress the index \(n\), and impose the inherited common-shear
platform conditions

\[
 \lambda=\frac{63}{32},\qquad c_h=\frac{15}{16},\qquad
 L_i=\lambda2^{k_i},\qquad k_2=k_1+1,\qquad
 L_2=2L_1,\qquad y_i^\circ=c_hL_iR,
\]

\[
 R\le\frac1{32},\qquad L_2R\le\frac5{144},\qquad
 L_1\ge9216,\qquad
 R^{-1}e^{-a_SL_1^2}\longrightarrow0.
\]

The last limit is exactly (T.22).  The central-chart inequalities are stated
separately because they do not follow from (T.22) alone.  Retain the saturation
profile \(\theta_R\), set \(q_*=1/2\), and use the inherited common shear

\[
 D_1:=\int_{R^2}^{65R^2}\theta_R(t,y_1^\circ)\,dt,
 \qquad B:=\frac{q_*}{D_1},
 \qquad
 b(t,x_3)=B\theta_R(t,x_3),
 \qquad
 I_R=(64R^2,65R^2).
 \tag{T.34}
\]

Choose \(0<\theta_i\le1\) and terminal times \(\tau_i\) such that

\[
 J_i=(\tau_i-\theta_iR^3,\tau_i)\subset I_R,
 \qquad i=1,2.
 \tag{T.35}
\]

Set the desired horizontal terminal centres equal to zero and define

\[
 q_{{\rm pre},i}
 :=-B\int_0^{\tau_i}\theta_R(s,y_i^\circ)\,ds,
 \qquad
 Q_i(t):=q_{{\rm pre},i}
       +B\int_0^t\theta_R(s,y_i^\circ)\,ds.
 \tag{T.36}
\]

Then

\[
 Q_i(\tau_i)=0,
 \qquad
 |Q_i(t)|\le B|t-\tau_i|
 \le B\theta_iR^3\le BR^3\le\frac R{64}
 \quad(t\in J_i)
 \tag{T.37}
\]

for all sufficiently large \(L_1\), using the inherited asymptotic
\(B=(128R^2)^{-1}(1+o(1))\).  Translate the two inversion-paired initial
packets by the respective \(q_{{\rm pre},i}\), re-evolve both under the same
coefficient \(b\), and use the equal-target amplitudes

\[
 \Gamma_i:=\gamma_{k_i}=e^{-c_\gamma L_i^2},
 \qquad
 \mathfrak a_i=A_*(\Gamma_iL_i)^{-1/2},
 \qquad i=1,2.
 \tag{T.38}
\]

Horizontal translation commutes with the common scalar advection--diffusion
equation.  The inversion partner preserves full oddness.  Hence the finite
sum

\[
 u=(\mathfrak a_1G_1+\mathfrak a_2G_2,b,0),
 \qquad p=0,
 \tag{T.39}
\]

is the exact smooth periodic mean-zero unforced Navier--Stokes solution from
R0.74Q, Step 1, Proposition 1.1; packets evolved under different shears have
not been added.

The analytic estimates used for the lobe survive the re-centring uniformly:

- R0.74F Lemma 4.1 controls the shear error for every
  \(0\le t\le65R^2\);
- on (T.35), the normalized free heat age lies in the compact interval
  \(65<(R^2+t)/R^2<66\), so the derivative-packet lower bound on
  \(5R/4<x_2-Q_i(t)<3R/2\) is uniform;
- inversion suppression is uniform in the horizontal coordinate;
- the R0.74Q vertical cross-tail bounds are uniform for
  \(0\le t\le65R^2\) and do not depend on \(q_{{\rm pre},i}\); and
- (T.37) preserves the annular margins used in R0.74Q (Q.133)--(Q.136).

For completeness, the generalized sequence also closes the periodic remainder
used in the amplitude-weighted cross-tail estimate.  With
\(q=c_\gamma/2\), the central-chart bound gives

\[
 C\exp\!\left(qL_2^2-\frac3{22R^2}\right)
 \le C\exp(-c_*L_2^2)\longrightarrow0,
 \qquad
 c_*:=\frac3{22}\left(\frac{144}{5}\right)^2-q>0.
\]

Thus the special choice \(R=e^{-\rho L^2}\) used in R0.74Q is not being
silently assumed here.

Consequently, after increasing the base scale once, each \(J_i\) carries a
target lobe \(\Omega_i(t)\subset A_{k_i}(R)\) with

\[
 |\Omega_i(t)|=\frac1{16}L_iR^3,
 \qquad
 \Psi_{k_i}^R=1\quad\hbox{on }\Omega_i(t),
 \qquad
 |u(t,x)|\ge c\mathfrak a_i
 \quad(x\in\Omega_i(t),\ t\in J_i),
 \tag{T.40}
\]

where \(c>0\) is independent of the two chosen admissible terminal times.
Moreover, the frozen time cutoff satisfies \(\eta_R=1\) throughout \(I_R\).
With

\[
 T:=A_*^2R^2,
\]

the nonnegative endpoint and dissipation rows of the clock therefore give

\[
 K_{k_i,R}(t)\ge cA_*^2R^2=cT
 \quad(t\in J_i),
 \qquad
 \mathfrak L^K_{1,R}(I_R)\ge cT.
 \tag{T.41}
\]

This gives arbitrary relative scheduling **inside the stated slab**, not
independent time translation of already evolved solutions and not arbitrary
real target times.

There are explicit disjoint unit-dwell choices.  For \(R<1/3\), take

\[
 \begin{aligned}
 &\theta_1=\theta_2=1,\\
 &\tau_1=64R^2+2R^3,
 \qquad \tau_2=65R^2.
 \end{aligned}
 \tag{T.42}
\]

Then
\(J_1=(64R^2+R^3,64R^2+2R^3)\) and
\(J_2=(65R^2-R^3,65R^2)\) lie in \(I_R\) and are disjoint.  Nevertheless
the outer interval has \(\theta_2=1\), so (T.24)--(T.26) give

\[
 \frac{(P_R^M)^{2/3}}{T}\longrightarrow\infty
 \tag{T.43}
\]

along the inherited survival-compatible adjacent-shell asymptotic.  The
construction therefore realizes asynchronous clock floors but cannot turn
those floors into a low-payment witness.

## 8. Claim ledger and next gate

The following are **PROVED** in this note:

- exact outer-lobe Hölder coercivity (T.9)--(T.10);
- invariance of that estimate under every relative target-time schedule for
  which the lobe hypotheses hold;
- existence of two disjoint admissible lobe windows in one exact common-shear
  solution, (T.34)--(T.43);
- the two-clock completed-height witness (T.17), with the correct
  \(K\)-clock rather than stopped-flux quantifier;
- the logarithmic dwell identity and necessary collapse threshold
  (T.24)--(T.29); and
- sharpness of all exponents within the stated measure-theoretic class.

The following are **INHERITED** inputs:

- the Version-M payment and shell weights;
- the exact common-shear finite-packet Navier--Stokes solution;
- the R0.74F lobe interval, R0.74Q shell placement, all-lobe dominance, and
  positive lobe kinetic floor; and
- the sufficient bridge-survival proof window (T.22).

The following remain **OPEN**:

- scheduling outside the inherited terminal slab, or constructing a packet
  family whose maximal time set with a comparable outer kinetic floor is
  exponentially short in the sense of (T.28), while retaining uniform packet
  survival and lobe height;
- a payment-scale upper bound for the full
  \(\mathfrak L^K_{1,R}(D)\), including off-target clocks and accumulated
  dissipation;
- an implication from completed-clock floors to the stopped-flux
  \(\mathfrak H^{\rm fix}\) without paying the Step 18 terms;
- the fixed-deletion and direct hybrid estimates, Q.12, Q.1, scale
  contraction, regularity, and the Clay problem.

The route decision is consequently precise.  A future asynchronous packet
stress test must first exhibit an outer lobe whose maximal comparable-floor
persistence is exponentially short, with no comparable floor on any longer
interval, or abandon one of the inherited shell-weight, survival, or
lobe-floor hypotheses.  Merely changing the order of two ordinary
\(R^3\)-long lobes, or truncating them in the analysis, is not a live escape.

<!-- R074T_STEP19_END -->
