# R0.74S Step 15A — hybrid-start flux equivalence and the common-window start debt

## 0. Result and scope

This note makes one exact reduction that was not recorded in Steps 10--14.
The short last-exit residual and the Step 8 selected-excess residual can be
encoded by one nonnegative physical-flux vector.  The vector uses only two
start rules: the canonical last exit on the short branch and the inherited
common zero start on the selected-excess branch.

There are five conclusions.

1. On the short branch, the new flux coordinate is exactly the Step 10
   residual.  On the selected-excess branch, it is the positive terminal
   flux \(F_{k,R}(\tau)\).
2. The full-history total-variation bound for \(Q_{k,R}\), used across both
   the terminal and last-exit subintervals, gives the sharp scalar comparison

   \[
      {1\over5}z_k<r_k<{3\over7}z_k
      \qquad(k\in\mathcal I_x).
   \]
   Treating \(Q(\tau)\) and \(Q(\tau)-Q(\ell_k)\) as unrelated would lose
   this correlation and give weaker constants.
3. Consequently, for the combined residual and every common deletion budget
   \(N\),

   \[
      {1\over5}\mathcal S_N(z(\tau))
      \le \mathcal S_N(r(\tau))
      \le \mathcal S_N(z(\tau)).
   \]
   This is a two-sided equivalence, including after the good-terminal
   supremum.
4. The global common-deletion temporal flux tail
   \(\mathfrak H^F_{p,N,R}\) from Step 13 pays this entire hybrid vector with
   one deletion set.  Thus the open estimate (S.342), if proved, closes both
   residual branches at once; it is not only a short-branch input and it
   makes the separate ancestor gate unnecessary along that route.
5. Synchronizing shallow last-exit intervals to one signed terminal window
   creates an exact start-clock overshoot debt.  Last-exit maximality does not
   control that debt.  This identifies the extra estimate required by any
   common-window signed-cancellation argument.

All assertions below are for the frozen Version-M suitable-weak setting.
The new content is a rigorous reduction and a scalar sharpness audit.  The
common-deletion estimate (S.342), Step 10 (S.243), Q.12, and Q.1 remain open.
No abstract scalar witness below is a Navier--Stokes counterexample.  No
claim of novelty, regularity, singularity formation, or a solution of the
Millennium problem is made.  **NOT CLAY.**

## 1. Frozen data and the hybrid start

Fix one admissible deterministic profile
\(\boldsymbol\lambda=(\lambda_k)_{k\ge1}\), one Version-M suitable weak
solution, one admissible scale \(R\), and one local-energy good terminal time
\(\tau\in\mathcal G_R\cap\mathcal T_R\).  Retain the Step 10 notation

\[
 T_k=K_{k,R}(\tau),\qquad
 \ell_k=\ell_{k,2/3}^K(\tau),\qquad
 \Delta Q_k=Q_{k,R}(\tau)-Q_{k,R}(\ell_k),
\]

and the disjoint residual classes

\[
 \mathcal I_{\rm res}(\tau)
 =\mathcal R_{\rm sh}(\tau)\mathbin{\dot\cup}\mathcal I_x(\tau).
\]

Choose once, as in Step 8 (S.194), a common local-energy good time
\(\sigma_0\) in the initial interval on which the frozen time cutoff and its
derivative vanish.  Then, simultaneously for all \(k\),

\[
 K_{k,R}(\sigma_0)=Q_{k,R}(\sigma_0)=F_{k,R}(\sigma_0)=0.
\]

Define the terminal-dependent hybrid start and stopped physical-flux vector
by

\[
 \boxed{
 \sigma_k^{\rm hyb}(\tau):=
 \begin{cases}
   \ell_k(\tau),&k\in\mathcal R_{\rm sh}(\tau),\\
   \sigma_0,&k\in\mathcal I_x(\tau),\\
   \tau,&k\notin\mathcal I_{\rm res}(\tau),
 \end{cases}
 \qquad
 z_{k,R}^{\boldsymbol\lambda}(\tau)
 :=F_{k,R}(\tau)-F_{k,R}(\sigma_k^{\rm hyb}(\tau)).}
 \tag{S.377}
\]

The definition immediately gives

\[
 \boxed{
 z_k=r_k^{\rm sh}=r_k
 \quad(k\in\mathcal R_{\rm sh}),
 \qquad
 z_k=F_{k,R}(\tau)=[F_{k,R}(\tau)]_+
 \quad(k\in\mathcal I_x),
 \qquad
 z_k=r_k=0\quad(k\notin\mathcal I_{\rm res}).}
 \tag{S.378}
\]

The positivity asserted on \(\mathcal I_x\) follows again below.  In
particular, the Step 8 comparison (S.193) becomes

\[
 \boxed{0\le x_k^{\rm sel}(\tau)\le z_k(\tau)
 \qquad\hbox{for every }k.}
 \tag{S.379}
\]

Thus selected anomalous-defect/high-Rayleigh excess and the short residual
are subcoordinates of one physical stopped-flux vector.  This statement
does not estimate that vector.

## 2. Sharp selected-excess comparison from one \(Q\)-variation budget

Fix \(k\in\mathcal I_x(\tau)\) and abbreviate

\[
 U_k:=Q_{k,R}(\ell_k),\qquad
 V_k:=Q_{k,R}(\tau)-Q_{k,R}(\ell_k).
\]

There are two different inherited \(Q\)-bounds, but they arise from one
full-history variation measure.  Since \(Q_{k,R}(\sigma_0)=0\),
\(\sigma_0<\ell_k<\tau\), and
\(\beta_{k,R}(J_\tau)=\operatorname{TV}_{J_\tau}Q_{k,R}<T_k/6\) on
\(\mathcal I_x\), additivity of variation gives the stronger joint
constraint

\[
 \boxed{
 |U_k|+|V_k|
 \le \operatorname{TV}_{(\sigma_0,\ell_k)}Q_{k,R}
      +\operatorname{TV}_{(\ell_k,\tau)}Q_{k,R}
 \le\beta_{k,R}(J_\tau)<{T_k\over6}.}
 \tag{S.380}
\]

The possible endpoint convention causes no loss because \(Q_{k,R}\) is
absolutely continuous and vanishes on a common neighborhood of the left
endpoint.  Notice that (S.380) is stronger than separately writing
\(|Q(\tau)|<T_k/6\) and \(|\Delta Q_k|<T_k/6\).

The terminal clock identity and the last-exit identity now read

\[
 \boxed{
 z_k=T_k-U_k-V_k,
 \qquad
 r_k={T_k\over3}-V_k.}
 \tag{S.381}
\]

In particular, (S.380) first gives
\(5T_k/6<z_k<7T_k/6\), so \(z_k>0\).  More sharply,

\[
 \begin{aligned}
 5r_k-z_k
 &= {2T_k\over3}+U_k-4V_k
  > {2T_k\over3}-4(|U_k|+|V_k|)>0,\\
 3z_k-7r_k
 &= {2T_k\over3}-3U_k+4V_k
  > {2T_k\over3}-4(|U_k|+|V_k|)>0.
 \end{aligned}
\]

Therefore

\[
 \boxed{
 {1\over5}z_k<r_k<{3\over7}z_k
 \qquad(k\in\mathcal I_x(\tau)).}
 \tag{S.382}
\]

Together with the exact equality on \(\mathcal R_{\rm sh}\), this yields
the global coordinatewise comparison

\[
 \boxed{
 {1\over5}z_k(\tau)\le r_k(\tau)\le z_k(\tau)
 \quad(k\ge1),
 \qquad z(\tau)\in\ell^1_+.}
 \tag{S.383}
\]

Here \(z\in\ell^1\) follows from \(z_k\le5r_k\) and the inherited
\(r(\tau)\in\ell^1_+\).  No summation or exceptional-set optimization has
yet been used.

## 3. Exact common-deletion equivalence

For every integer \(N\ge0\), apply (S.383) outside the same arbitrary set
\(S\subset\mathbb N\), \(\#S\le N\), and only then optimize.  This proves

\[
 \boxed{
 {1\over5}\mathcal S_N(z(\tau))
 \le\mathcal S_N(r(\tau))
 \le\mathcal S_N(z(\tau)).}
 \tag{S.384}
\]

For either terminal domain
\(\mathcal D\in\{I_R,\mathcal T_R\}\), put

\[
 \mathfrak Z_{N,R}^{\boldsymbol\lambda}(\mathcal D)
 :=\sup_{\tau\in\mathcal D\cap\mathcal G_R}
       \mathcal S_N(z_R^{\boldsymbol\lambda}(\tau)).
\]

Taking suprema in (S.384) gives

\[
 \boxed{
 {1\over5}\mathfrak Z_{N,R}^{\boldsymbol\lambda}(\mathcal D)
 \le\mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)
 \le\mathfrak Z_{N,R}^{\boldsymbol\lambda}(\mathcal D).}
 \tag{S.385}
\]

Thus, for any fixed universal \(N\), the full hybrid-flux gate and the full
combined residual gate are equivalent up to the literal factor \(5\).
The deletion set may depend on \(\tau\), exactly as in Step 10 (S.243).

This equivalence is different from Step 11 (S.263).  That result compares
only \(r^x\) with the scalar excess \(x^{\rm sel}\).  Equations
(S.384)--(S.385) compare the full two-branch residual with one physical
flux vector and retain a single shared deletion budget.

## 4. One global temporal flux tail pays both branches

Retain the Step 13 dimensionless density

\[
 h_{k,R}(\sigma)=R^2|\dot F_{k,R}(s_R+R^2\sigma)|,
 \qquad 0<\sigma<4,
\]

extended by zero as there.  Absolute continuity of \(F_{k,R}\), (S.377),
and positivity of \(z_k\) give, for every shell,

\[
 \boxed{
 0\le z_k(\tau)
 \le\int_0^4h_{k,R}(\sigma)\,d\sigma
 \le4^{\,1-1/p}\|h_{k,R}\|_{L^p(0,4)},
 \qquad 1\le p\le\infty.}
 \tag{S.386}
\]

For \(p=\infty\), the last factor is \(4\).  Apply (S.386) outside one
arbitrary shell set and choose a sequence of sets approaching the infimum
in the Step 13 definition of \(\mathfrak H^F_{p,N,R}\).  The result is

\[
 \boxed{
 \mathcal S_N(r(\tau))
 \le\mathcal S_N(z(\tau))
 \le4^{\,1-1/p}\mathfrak H^F_{p,N,R}.}
 \tag{S.387}
\]

The same deletion set controls the full time norm before any terminal or
branch is chosen.  Hence (S.387) is stronger in quantifiers than choosing
one exceptional set for the short branch and another for the excess
branch.  It also proves simultaneously

\[
 \mathcal S_N(x^{\rm sel}(\tau))
 \le\mathcal S_N(z(\tau))
 \le4^{\,1-1/p}\mathfrak H^F_{p,N,R}.
\]

This answers the interface left implicit after Step 13: the open
common-deletion estimate (S.342) is by itself a sufficient route through
both residual classes.  No ancestor coefficient \(b_k\), separate budget
\(N_b\), or jump--corona lemma is needed if that route succeeds.  The
converse is not asserted; \(\mathfrak H^F_{p,N,R}\) controls full absolute
time variation and is substantially stronger than the terminal hybrid
gate.  The upper bound for \(r_k\) by the full variation can also be read
directly from its own stopped-increment definition; the new content here is
the single hybrid zero-start/last-exit interpretation, its exact two-sided
best-\(N\) equivalence, and the consequent correction of the route map.

## 5. Conditional chain to Q.12 and Q.1

Suppose, as an explicit antecedent, that fixed
\(p\in(1,\infty]\), \(N_F<\infty\), and \(C_H<\infty\), independent of the
solution and \(R\), satisfy the still-open Step 13 estimate

\[
 \boxed{
 \mathfrak H^F_{p,N_F,R}\le C_HA_R,
 \qquad A_R=(P_R^M)^{2/3}.}
 \tag{S.388}
\]

Equations (S.387) and (S.237) then give the full-domain residual estimate

\[
 \boxed{
 \mathfrak R_{N_F,R}^{\boldsymbol\lambda}(\mathcal T_R)
 \le4^{\,1-1/p}C_HA_R.}
 \tag{S.389}
\]

Thus (S.388) implies the open Step 10 statement (S.243) with exactly the
same exception count \(N_F\).  Substitution in Step 10 (S.238) gives

\[
 \boxed{
 \mathcal S_{N_F,R}^{K}(\mathcal T_R)
 \le\left[C_{\rm pay}(\boldsymbol\lambda)
          +6\,4^{\,1-1/p}C_H\right]A_R.}
 \tag{S.390}
\]

This is the \(K\)-version of Q.12.  The inherited terminal reduction (Q.9)
therefore yields

\[
 \boxed{
 \mathfrak C_R^M
 \le C(\boldsymbol\lambda,p,N_F,C_H)
       \left[A_R+Y_{2,R}^{\rm sf}\right],}
 \tag{S.391}
\]

which is Q.1.  Equations (S.388)--(S.391) are a proved implication, not a
proof of the antecedent.  Here the factor \(\sqrt{N_F}\) multiplying
\(Y_{2,R}^{\rm sf}\) in the inherited reduction is absorbed into the
constant because \(N_F\) is fixed universally.  In particular, these
equations do not establish scale
contraction or regularity.

## 6. What signed channel cancellation would have to prove

The Step 14 four-channel identity (S.345) can be integrated on the hybrid
active blocks.  For every finite shell set \(G\),

\[
 \boxed{
 \sum_{k\in G\cap\mathcal I_{\rm res}(\tau)}z_k(\tau)
 =\sum_{\alpha\in\{{\rm cub,loc,har,dr}\}}
   \sum_{k\in G\cap\mathcal I_{\rm res}(\tau)}
   \int_{\sigma_k^{\rm hyb}(\tau)}^\tau
       \dot F_{k,R}^{\alpha}(t)\,dt.}
 \tag{S.392}
\]

The left side is nonnegative and, by (S.383), is comparable to the actual
combined residual on the same shells.  Therefore retaining the signs of
the four Step 14 channels, or regrouping inner and outer collar rows, is
compatible with a successful proof but is not itself a gain: on these
terminal-dependent blocks the regrouped total is exactly the positive
hybrid tail that must be bounded.  A successful cancellation argument must
supply a new quantitative PDE estimate for the right side of (S.392) at
the \(A_R\) scale.  Algebraic rearrangement alone does not change the
functional.

This is a boundary statement, not a new impossibility theorem for PDE
cancellation.  In particular, it does not exclude correlations supplied by
the local energy balance, pressure, incompressibility, or a new temporal
anti-concentration estimate.  The actual disjoint-collar and weighted
telescoping obstructions remain those proved in Steps 3 and 6.

## 7. Exact debt created by a signed common terminal window

There is one further exact interface for the short branch.  Fix
\(0<\delta<4\), set

\[
 a=a_{\tau,\delta}:=\max\{s_R,\tau-\delta R^2\},
 \qquad
 \mathcal R_{\rm sh}^{\le\delta}(\tau)
 :=\{k\in\mathcal R_{\rm sh}(\tau):d_k\le\delta\},
\]

and define the signed common-window increment

\[
 G_{k,\tau,\delta}:=F_{k,R}(\tau)-F_{k,R}(a).
\]

For \(k\in\mathcal R_{\rm sh}^{\le\delta}(\tau)\), one has
\(a\le\ell_k\).  Since \(K_k(\ell_k)=2T_k/3\) and \(K=Q+F\), direct
subtraction gives

\[
 \boxed{
 r_k^{\rm sh}
 =G_{k,\tau,\delta}
  +\left[K_{k,R}(a)-{2T_k\over3}\right]
  +\left[Q_{k,R}(\ell_k)-Q_{k,R}(a)\right].}
 \tag{S.393}
\]

Define the nonnegative start-clock overshoot

\[
 \omega_{k,\tau,\delta}
 :=\mathbf1_{\mathcal R_{\rm sh}^{\le\delta}(\tau)}(k)
   \left[K_{k,R}(a)-{2T_k\over3}\right]_+.
\]

For every \(S\subset\mathbb N\), summing (S.393), retaining cancellation
inside the common-window \(G\)-sum, and using the global \(Q\)-variation
ledger gives

\[
 \boxed{
 \begin{aligned}
 \sum_{k\in\mathcal R_{\rm sh}^{\le\delta}(\tau)\setminus S}r_k^{\rm sh}
 \le{}&
 \left[\sum_{k\in\mathcal R_{\rm sh}^{\le\delta}(\tau)\setminus S}
          G_{k,\tau,\delta}\right]_+
 +\sum_{k\notin S}\omega_{k,\tau,\delta}\\
 &+\sum_k\operatorname{TV}_{[s_R,t_0)}Q_{k,R}\\
 \le{}&
 \left[\sum_{k\in\mathcal R_{\rm sh}^{\le\delta}(\tau)\setminus S}
          G_{k,\tau,\delta}\right]_+
 +\sum_{k\notin S}\omega_{k,\tau,\delta}
 +C_QA_R.
 \end{aligned}}
 \tag{S.394}
\]

The passage from finite shell sets to (S.394) is legitimate because
\(\sum_k|G_{k,\tau,\delta}|\le\sum_k\operatorname{TV}F_{k,R}<\infty\).
Moreover,
\(\omega_{k,\tau,\delta}\le K_{k,R}(a)+2T_k/3\), and both clock vectors
are in \(\ell^1_+\); hence the overshoot series is absolutely convergent.

Consequently,

\[
 \boxed{
 \begin{aligned}
 \mathcal S_N(r^{{\rm sh},\le\delta}(\tau))
 \le C_QA_R+
 \inf_{\#S\le N}\Bigg\{
 &\left[\sum_{k\in\mathcal R_{\rm sh}^{\le\delta}(\tau)\setminus S}
          G_{k,\tau,\delta}\right]_+\\
 &+\sum_{k\notin S}\omega_{k,\tau,\delta}\Bigg\}.
 \end{aligned}}
 \tag{S.395}
\]

Equation (S.395) is the minimal signed common-window gate exposed by the
last-exit construction.  It separates two genuinely different tasks:
cross-shell cancellation of the common-window increments and control of
the start-clock overshoot using the same deletion set.  Last-exit
maximality only says \(K_k(t)>2T_k/3\) for
\(\ell_k<t\le\tau\).  It gives no inequality
\(K_k(a)\le2T_k/3\) at the earlier common start \(a\), because the clock
may have made a previous excursion above the threshold and returned to it
at \(\ell_k\).

Thus signed synchronization does not eliminate the Step 12 absolute-window
problem for free.  It trades the absolute value of each flux increment for
the explicit start-clock debt in (S.395).  A new PDE theorem controlling
that debt, or ruling out repeated threshold excursions on all but finitely
many shells, would be a legitimate alternative input.

## 8. Scalar sharpness and debt checks

### 8.1 Sharp constants in (S.382)

Normalize \(T=1\).  For \(0<\varepsilon<1/6\), take an absolutely
continuous scalar \(Q\) which is zero through \(\ell\) and then changes
monotonically to

\[
 V_\varepsilon^+= {1\over6}-\varepsilon
 \qquad\hbox{or}\qquad
 V_\varepsilon^-=-{1\over6}+\varepsilon
\]

at \(\tau\).  Then \(U=0\) and
\(\operatorname{TV}Q=|V_\varepsilon^\pm|<1/6\).  Choose a continuous,
nondecreasing clock with \(K(\ell)=2/3\), \(K(t)>2/3\) on
\((\ell,\tau]\), and \(K(\tau)=1\), and put \(F=K-Q\).  Complete the
scalar ledger by taking pure defect \(D(t)=K(t)\), local energy \(E=0\),
and kinetic occupation \(\sigma=0\).  Then \(K=E+D=Q+F\),
\(D(\tau)=T=1\), and
\(\beta=\operatorname{TV}Q<T/6\).  Thus the row lies in the abstract
\(\mathcal I_x\) branch, with
\(x=D(\tau)-\beta-2\lambda\sigma>5/6>T/6\).  The two ratios are

\[
 \boxed{
 {r\over z}
 ={1/6+\varepsilon\over5/6+\varepsilon}
 \longrightarrow{1\over5},
 \qquad
 {r\over z}
 ={1/2-\varepsilon\over7/6-\varepsilon}
 \longrightarrow{3\over7}.}
 \tag{S.396}
\]

Hence neither strict constant in (S.382) can be improved from the scalar
constraints used in its proof.

This is an **ABSTRACT SCALAR-LEDGER WITNESS**.  It is not asserted to arise
from a Navier--Stokes solution and does not disprove a stronger PDE
comparison.

### 8.2 Why the start debt is real at the clock level

Take \(s=0<a=1<\ell=2<\tau=3\), \(T=3\), and \(M>3\).  Let \(K\) be a
nonnegative piecewise-linear clock with

\[
 K(0)=0,\qquad K(a)=M,\qquad K(\ell)=2,
 \qquad K(t)>2\ (\ell<t\le\tau),\qquad K(\tau)=3.
\]

Set \(Q=0\) and \(F=K\).  Then \(\ell\) is the last exit from the level
\(2T/3=2\), while

\[
 \boxed{
 r=1,\qquad G=F(\tau)-F(a)=3-M,
 \qquad \omega=K(a)-2=M-2,
 \qquad r=G+\omega.}
 \tag{S.397}
\]

The signed common-window increment can therefore be arbitrarily negative
while the last-exit residual stays fixed and positive; the start debt
restores the identity exactly.  This too is only an **ABSTRACT CLOCK
CHECK**, not a Navier--Stokes counterexample and not a realization of the
full short-branch PDE constraints.

## 9. Quantifiers and route decision

The proved statements (S.377)--(S.397) hold for each fixed solution, fixed
admissible scale, and fixed good terminal time.  The two-sided equivalence
is uniform because its constants are literal.  A closure claim requires a
single integer \(N\) and a constant independent of the solution, \(R\), and
\(\tau\), with the terminal supremum taken over
\(\mathcal G_R\cap\mathcal T_R\).  Fixed-solution tail compactness does not
supply those quantifiers.

The immediate alternatives are now precise.

1. Prove (S.342).  By (S.387)--(S.391), this one theorem closes the entire
   combined residual using the same \(N_F\); the Step 14 jump--corona route
   is then unnecessary.
2. Prove the weaker hybrid terminal gate
   \(\mathfrak Z_{N,R}^{\boldsymbol\lambda}(\mathcal T_R)\lesssim A_R\)
   directly by signed local-energy cancellation.  By (S.385), this is
   exactly equivalent to the Step 10 residual gate up to factor \(5\).
3. On shallow short intervals, prove the two-term same-deletion estimate in
   (S.395): signed common-window cancellation plus start-clock overshoot.
   The existing \(Q\)-prefix is already paid.
4. If none of these succeeds, return to the independent Step 14 ancestor
   gate (S.375).  That remains a valid sufficient route, but it is no longer
   the only way to absorb \(\mathcal I_x\).

Useful primary-literature collision-search phrases for the new interfaces
are: ``prescribed-centre local energy flux suitable weak solution'',
``terminal trace equi-integrability Navier--Stokes local energy flux'',
``physical-space energy flux locality ensemble average'', ``variation norm
local energy balance'', ``annular pressure flux Carleson measure'', and
``upcrossing inequality local energy martingale analogue''.  Existing
ensemble-averaged physical-flux locality results do not by themselves have
the prescribed-centre, terminal-dependent active-block, or common fixed
shell-deletion quantifiers used above.  In particular, the physical-space
flux-locality theorem of R. Dascaliuc and Z. Grujić,
[*Energy cascades and flux locality in physical scales of the 3D
Navier--Stokes equations*](https://arxiv.org/abs/1101.2193), uses time and
ensemble averages over optimal covers under an inertial-range/Taylor-scale
condition; it does not supply (S.342), the hybrid terminal gate, or the
start-debt estimate (S.395).  This is a bounded collision boundary, not an
exhaustive search or a novelty claim.
