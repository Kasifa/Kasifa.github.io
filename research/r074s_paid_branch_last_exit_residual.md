# R0.74S Step 10 — paid-branch deletion reduces the clock tail to a residual best-\(N\) last-exit gate

## 0. Result and scope

Step 9 showed that a canonical last exit represents the R0.74Q best-\(N\)
terminal tail but, by itself, does not compress that tail.  The next question
is therefore more specific: after deleting every shell already paid by the
quadratic \(Q\)-variation ledger or by the velocity-cubic ledger, what part
of the canonical last-exit tail actually remains?

This note gives an exact answer.  At every local-energy good terminal time,
the positive terminal shells split into four paid classes and two residual
classes.  The paid classes are bounded by exactly one copy of

\[
 6B_{Q,R}^M
 +C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R,
 \qquad A_R=(P_R^M)^{2/3},
\]

with one complete \(Q\)-ledger and one complete cubic ledger, not two copies
of either.  The remaining vector is the \(2/3\)-last-exit flux increment on

1. the Step 8 scalar-excess class \(\mathcal I_x\), whose Step 7 ancestry is
   necessarily anomalous-defect or high-Rayleigh; and
2. the non-dissipation terminal class whose last-exit interval is
   \(\boldsymbol\lambda\)-short and whose \(Q\)-increment is small.

On both residual classes the stopped flux is positive and quantitatively
equivalent to the terminal clock:

\[
 {1\over6}K_{k,R}(\tau)<r_{k,R}(\tau)
 <{1\over2}K_{k,R}(\tau).
\]

Consequently the full best-\(N\) clock tail is bounded by the paid amount
plus six times a residual best-\(N\) tail.  Conversely, the residual tail is
at most one half of the clock tail.  Thus the new gate is equivalent, modulo
already-proved payments, to the open full-terminal R0.74Q gate.  Its value is
structural: it identifies the two mechanisms a future PDE packing theorem
must control and removes every branch already known to be quadratic.

This is not such a packing theorem.  No fixed universal \(N_0\), residual
quadratic bound, scale contraction, regularity theorem, or solution of the
Millennium problem is proved.  Canonical last exits and the moving residual
mask are not claimed continuous or lower semicontinuous in the terminal
time, and no infinite stopped cutoff is inserted into the local-energy
inequality.  **NOT CLAY.**

No novelty or priority claim is made.

## 1. Inherited setting and the \(2/3\)-last exit

Retain the periodic suitable-weak Version-M setting, viscosity one, fixed
scale \(R\), full clock interval
\(\mathcal T_R=(s_R,t_0)\), plateau interval \(I_R\), and common full-measure
local-energy good-time set \(\mathcal G_R\) from R0.74P--R0.74S.  Write

\[
 A_R:=(P_R^M)^{2/3},\qquad
 B_{Q,R}^M:=\sum_{k\ge1}
  \operatorname {TV}_{[s_R,t_0)}Q_{k,R}\le C_QA_R,
 \qquad
 Z_R:=\left(\sum_{k\ge1}v_{k,R}^2\right)^{1/2}.
\]

The canonical completed clocks satisfy

\[
 K_{k,R}=Q_{k,R}+F_{k,R},\qquad K_{k,R}\ge0,
 \qquad K_{k,R}(s_R)=Q_{k,R}(s_R)=F_{k,R}(s_R)=0,
\]

and the three paths are continuous.  The absolute \(Q\)- and \(F\)-variation
ledgers are summable, \(K_{k,R}(\tau)\le v_{k,R}\), and the terminal vector
\((K_{k,R}(\tau))_k\) is continuous into \(\ell^1\).
Write \(C_F\) for the inherited absolute constant in
\(\sum_k\operatorname {TV}F_{k,R}\le C_FP_R^M\).

Fix \(\tau\in\mathcal G_R\cap\mathcal T_R\).  For every shell with
\(T_k:=K_{k,R}(\tau)>0\), use the Step 9 last exit at level \(2T_k/3\):

\[
 \boxed{
 \begin{gathered}
  \ell_k=\ell_{k,2/3}^{K}(\tau)
   :=\max\{t\in[s_R,\tau]:K_{k,R}(t)\le2T_k/3\},\\
  J_k^{\rm LE}:=(\ell_k,\tau),\qquad
  d_k:={\tau-\ell_k\over R^2},\\
  0<d_k<4,\qquad K_{k,R}(\ell_k)={2T_k\over3},\qquad
  K_{k,R}(t)>{2T_k\over3}\quad(t\in J_k^{\rm LE}),\\
  \Delta Q_k:=Q_{k,R}(\tau)-Q_{k,R}(\ell_k),\qquad
  \Delta F_k:=F_{k,R}(\tau)-F_{k,R}(\ell_k),\\
  \Delta K_k={T_k\over3},\qquad
  \Delta F_k={T_k\over3}-\Delta Q_k.
 \end{gathered}}
\tag{S.223}
\]

For \(T_k=0\), set \(\ell_k=\tau\), \(d_k=0\), and every residual
coordinate below equal to zero.  Such shells never enter a strict
upcrossing.  The canonical \(\ell_k\) need not itself be a good time; only
continuity of \(K_k\) is used in (S.223).

Fix once and for all the same positive deterministic profile
\(\boldsymbol\lambda=(\lambda_k)_{k\ge1}\) used in Steps 7--8, independently
of \(R\), \(\tau\), and the solution, with

\[
 \boxed{
 \mathscr L(\boldsymbol\lambda)
 :=\sum_{k\ge1}2^{3k}\gamma_k\lambda_k^3<\infty.}
\tag{S.224}
\]

Among positive-terminal shells define

\[
 \begin{aligned}
 \mathcal I_{\rm long}(\tau)
  &:=\{k:d_k\ge\lambda_k^{-3/2}\},&
 \mathcal I_{\rm short}(\tau)
  &:=\{k:d_k<\lambda_k^{-3/2}\},\\
 \mathcal I_{Q+}(\tau)
  &:=\{k:|\Delta Q_k|\ge T_k/6\},&
 \mathcal I_{Q-}(\tau)
  &:=\{k:|\Delta Q_k|<T_k/6\},\\
 \mathcal I_D(\tau)
  &:=\{k:D_{k,R}(\tau)\ge T_k/2\},&
 \mathcal I_{\neg D}(\tau)
  &:=\{k:D_{k,R}(\tau)<T_k/2\}.
 \end{aligned}
\]

All displayed sets in this paragraph are restricted to \(T_k>0\).
Equality is assigned to the long, absolute-\(Q\)-large, and
dissipation-dominated sides.  If \(\lambda_k^{-3/2}\ge4\), the corresponding
long class is empty because \(d_k<4\).  For the canonical choice
\(\lambda_k\equiv1\), long means exactly
\(|J_k^{\rm LE}|\ge R^2\), and
\(\mathscr L(\mathbf1)=\sum_k2^{3k}\gamma_k<\infty\).

## 2. The exact paid/residual partition

Keep the Step 8 *full-history* priority partition

\[
 \mathcal I_D(\tau)
 =\mathcal I_\beta(\tau)\mathbin{\dot\cup}
  \mathcal I_\sigma(\tau)\mathbin{\dot\cup}
  \mathcal I_x(\tau),
\]

where \(\mathcal I_\beta,\mathcal I_\sigma,\mathcal I_x\) are defined using
\(J_\tau=(s_R,\tau)\), not the last-exit interval.  In particular,

\[
 \begin{aligned}
 \mathcal I_\beta
  &=\{k\in\mathcal I_D:\beta_{k,R}(J_\tau)\ge T_k/6\},\\
 \mathcal I_\sigma
  &=\{k\in\mathcal I_D\setminus\mathcal I_\beta:
       \sigma_{k,R}(J_\tau)>T_k/(12\lambda_k)\},\\
 \mathcal I_x
  &=\mathcal I_D\setminus
       (\mathcal I_\beta\cup\mathcal I_\sigma).
 \end{aligned}
\]

Define four paid classes and two residual classes by the following
*D-first* priority rule:

\[
 \boxed{
 \begin{aligned}
 \mathcal P_\beta&:=\mathcal I_\beta,
 &\mathcal P_\sigma&:=\mathcal I_\sigma,\\
 \mathcal P_{\rm LE}
   &:=\mathcal I_{\neg D}\cap\mathcal I_{\rm long},
 &\mathcal P_Q
   &:=\mathcal I_{\neg D}\cap\mathcal I_{\rm short}
                         \cap\mathcal I_{Q+},\\
 \mathcal R_{\rm sh}
   &:=\mathcal I_{\neg D}\cap\mathcal I_{\rm short}
                         \cap\mathcal I_{Q-},
 &\mathcal R_x&:=\mathcal I_x,\\[1mm]
 \{k:T_k>0\}
   &=\mathcal P_\beta\mathbin{\dot\cup}\mathcal P_\sigma
     \mathbin{\dot\cup}\mathcal P_{\rm LE}
     \mathbin{\dot\cup}\mathcal P_Q
     \mathbin{\dot\cup}\mathcal R_{\rm sh}
     \mathbin{\dot\cup}\mathcal R_x.
 \end{aligned}}
\tag{S.225}
\]

This is an exact disjoint partition.  The \(D\)-branch is first split by
the inherited Step 8 trichotomy.  Its complement is split into long and
short last-exit intervals, and only the short part is then split by the
absolute size of \(\Delta Q_k\).  The symbol \(\mathcal P_Q\) therefore
means *absolute-\(Q\)-large*, not positive-sign \(Q\).

There is no additional Step 7 low-Rayleigh paid class hidden inside
\(\mathcal R_x\).  Indeed, (S.149) gives, for
\(k\in\mathcal I_{\rm lo}\),

\[
 \sigma_{k,R}(J_\tau)
 \ge\sigma_{k,R}(L_{k,R})>{T_k\over8\lambda_k}.
\]

If such a shell is not in \(\mathcal I_\beta\), it satisfies the strict
Step 8 \(\sigma\)-test and lies in \(\mathcal I_\sigma\).  Hence

\[
 \boxed{
 \mathcal I_{\rm lo}\subset
  \mathcal I_\beta\cup\mathcal I_\sigma,
 \qquad
 \mathcal I_{\rm lo}\setminus
  (\mathcal I_\beta\cup\mathcal I_\sigma)=\varnothing,
 \qquad
 \mathcal I_x
  =\mathcal I_x\cap(\mathcal I_{\rm def}\cup\mathcal I_{\rm hi}).}
\tag{S.226}
\]

Equation (S.226) is a genealogy and no-double-charge statement.  It does
not pay \(\mathcal I_x\): the surviving shells can still belong to the
anomalous-defect or high-Rayleigh branches.

## 3. The two already-paid ledgers

### 3.1 One, not two, \(Q\)-variation ledgers

For \(k\in\mathcal P_\beta\), Step 8 gives
\(T_k\le6\beta_{k,R}(J_\tau)\).  For
\(k\in\mathcal P_Q\), the definition and absolute continuity of \(Q_k\)
give

\[
 T_k\le6|\Delta Q_k|
 \le6\operatorname {TV}_{[s_R,t_0)}Q_{k,R}.
\]

The two index sets are disjoint because
\(\mathcal P_\beta\subset\mathcal I_D\) and
\(\mathcal P_Q\subset\mathcal I_{\neg D}\).  Summing their shellwise
contributions before enlarging to the complete ledger gives

\[
 \boxed{
 \begin{aligned}
 \sum_{k\in\mathcal P_\beta\cup\mathcal P_Q}T_k
 &\le6\left(
   \sum_{k\in\mathcal P_\beta}\beta_{k,R}(J_\tau)
   +\sum_{k\in\mathcal P_Q}|\Delta Q_k|\right)\\
 &\le6B_{Q,R}^M\le6C_QA_R.
 \end{aligned}}
\tag{S.227}
\]

Thus the correct coefficient is one copy of \(6B_Q\), not \(12B_Q\).

### 3.2 Long non-\(D\) last-exit persistence

Let \(k\in\mathcal P_{\rm LE}\).  Since \(D_{k,R}\) is nondecreasing and
the terminal lies in the non-\(D\) class, for almost every local-energy
good time \(t\in J_k^{\rm LE}\),

\[
 D_{k,R}(t)\le D_{k,R}(\tau)<{T_k\over2},
 \qquad
 K_{k,R}(t)>{2T_k\over3}.
\]

At those times the inherited clock identity is
\(K_{k,R}(t)=E_{k,R}(t)+D_{k,R}(t)\), with
\(E_{k,R}(t)=e_{k,R}(t)\).  Therefore

\[
 \boxed{
 e_{k,R}(t)>{T_k\over6}\quad\hbox{for a.e. }t\in J_k^{\rm LE},
 \qquad
 {1\over R^2}\int_{J_k^{\rm LE}}e_{k,R}(t)^{3/2}\,dt
 >d_k\left({T_k\over6}\right)^{3/2}
 \ge\lambda_k^{-3/2}\left({T_k\over6}\right)^{3/2}.}
\tag{S.228}
\]

No value of \(E_k\) or \(D_k\) at the possibly non-good stop \(\ell_k\)
is used.  The a.e. inequality is exactly what is needed for integration.

Apply the inherited padded-shell estimate (R.214) on
\(J_k^{\rm LE}\):

\[
 {1\over R^2}\int_{J_k^{\rm LE}}e_{k,R}^{3/2}\,dt
 \le C_1\,2^{3k/2}\gamma_k^{1/2}
      p_{k,R}^{u,\eta}(J_k^{\rm LE}).
\]

Rearranging (S.228) gives the per-shell payment

\[
 \boxed{
 T_k\le C_{\rm LE}\lambda_k2^k\gamma_k^{1/3}
     \bigl(p_{k,R}^{u,\eta}(J_k^{\rm LE})\bigr)^{2/3},
 \qquad
 C_{\rm LE}:=6C_1^{2/3}<C_4,
 \qquad C_4:=12(2C_1)^{2/3}.}
\tag{S.229}
\]

The constant \(C_4\) is the Step 8 coefficient for
\(k\in\mathcal P_\sigma\), where

\[
 T_k\le C_4\lambda_k2^k\gamma_k^{1/3}
       (p_{k,R}^{\tau})^{2/3},
 \qquad p_{k,R}^{\tau}=p_{k,R}^{u,\eta}(J_\tau).
\]

For the disjoint union
\(\mathcal P_\sigma\cup\mathcal P_{\rm LE}\), choose the shell-dependent
measurable set

\[
 J_k^{\rm pay}:=
 \begin{cases}
 J_\tau,&k\in\mathcal P_\sigma,\\
 J_k^{\rm LE},&k\in\mathcal P_{\rm LE},\\
 \varnothing,&k\notin\mathcal P_\sigma\cup\mathcal P_{\rm LE}.
 \end{cases}
\]

Use finite-shell Hölder first and then the inherited estimate (R.211),
which expressly permits a different measurable time set for every shell.
Since \(C_{\rm LE}<C_4\), monotone convergence yields

\[
 \boxed{
 \sum_{k\in\mathcal P_\sigma\cup\mathcal P_{\rm LE}}T_k
 \le C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R,
 \qquad C_5:=C_4C_P^{2/3}.}
\tag{S.230}
\]

The two branches must be combined before Hölder and (R.211); estimating
them as two complete global ledgers would lose an unnecessary second copy
of \(C_5\).

## 4. The residual stopped-flux vector

Put

\[
 \mathcal I_{\rm pay}(\tau)
 :=\mathcal P_\beta\cup\mathcal P_\sigma
    \cup\mathcal P_{\rm LE}\cup\mathcal P_Q,
 \qquad
 \mathcal I_{\rm res}(\tau)
 :=\mathcal R_{\rm sh}\cup\mathcal R_x.
\]

Equations (S.227) and (S.230) prove

\[
 \boxed{
 \sum_{k\in\mathcal I_{\rm pay}(\tau)}T_k
 \le6B_{Q,R}^M
   +C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R
 \le C_{\rm pay}(\boldsymbol\lambda)A_R,
 \quad
 C_{\rm pay}(\boldsymbol\lambda)
 :=6C_Q+C_5\mathscr L(\boldsymbol\lambda)^{1/3}.}
\tag{S.231}
\]

Define the residual vector by

\[
 \boxed{
 r_{k,R}^{\boldsymbol\lambda}(\tau)
 :=1_{\mathcal I_{\rm res}(\tau)}(k)
   \bigl[F_{k,R}(\tau)-F_{k,R}(\ell_k)\bigr],
 \qquad r_{k,R}^{\boldsymbol\lambda}(\tau):=0
 \quad\hbox{when }T_k=0.}
\tag{S.232}
\]

On \(\mathcal R_{\rm sh}\), the strict inequality
\(|\Delta Q_k|<T_k/6\) is part of the definition.  On
\(\mathcal R_x=\mathcal I_x\), failure of the first Step 8 priority test
gives

\[
 |\Delta Q_k|
 \le\beta_{k,R}(J_k^{\rm LE})
 \le\beta_{k,R}(J_\tau)<{T_k\over6}.
\]

Using the exact identity in (S.223), both residual classes therefore obey

\[
 \boxed{
 {T_k\over6}<r_{k,R}^{\boldsymbol\lambda}(\tau)<{T_k\over2},
 \qquad
 2r_{k,R}^{\boldsymbol\lambda}(\tau)<T_k
 <6r_{k,R}^{\boldsymbol\lambda}(\tau)
 \quad(k\in\mathcal I_{\rm res}).}
\tag{S.233}
\]

In particular, \(r(\tau)\in\ell^1_+\).  Globally, including paid and
zero-terminal coordinates,

\[
 \boxed{
 0\le r_{k,R}^{\boldsymbol\lambda}(\tau)\le{T_k\over2}
 \le{v_{k,R}\over2},\qquad
 \|r_R^{\boldsymbol\lambda}(\tau)\|_{\ell^2}\le{Z_R\over2},
 \qquad
 \sum_kr_{k,R}^{\boldsymbol\lambda}(\tau)
 \le\sum_k\operatorname {TV}F_{k,R}\le C_FP_R^M.}
\tag{S.234}
\]

The first inequality in (S.234) is non-strict only to include zero and paid
coordinates.  The \(\ell^2\) estimate does not imply a fixed-\(N\)
\(\ell^1\) tail bound.  The last estimate is only linear in \(P_R^M\).

## 5. Paid-branch deletion and the best-\(N\) theorem

For a nonnegative \(\ell^1\) vector \(x\), recall

\[
 \mathcal S_N(x)
 =\inf_{S\subset\mathbb N,\,\#S\le N}
       \sum_{k\notin S}x_k.
\]

For every single set \(S\) with \(\#S\le N\), the exact partition
(S.225), paid bound (S.231), and residual comparison (S.233) give

\[
 \boxed{
 \sum_{k\notin S}T_k
 \le6B_{Q,R}^M
  +C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R
  +6\sum_{k\notin S}r_{k,R}^{\boldsymbol\lambda}(\tau).}
\tag{S.235}
\]

Paid shells that happen to lie in \(S\) only decrease the left side.  To
take the infimum rigorously, choose sets approaching the infimum of the
residual tail and apply (S.235) to those same sets.  This gives the
fixed-good-terminal theorem

\[
 \boxed{
 \mathcal S_N((K_{k,R}(\tau))_k)
 \le6B_{Q,R}^M
  +C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R
  +6\mathcal S_N((r_{k,R}^{\boldsymbol\lambda}(\tau))_k).}
\tag{S.236}
\]

There is one exceptional set of size at most \(N\) for the *combined*
residual.  Assigning a separate set of \(N\) exceptions to
\(\mathcal R_x\) and \(\mathcal R_{\rm sh}\) would silently replace \(N\)
by as many as \(2N\).

For either terminal domain
\(\mathcal D\in\{I_R,\mathcal T_R\}\), define the good-terminal residual
gate

\[
 \boxed{
 \mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)
 :=\sup_{\tau\in\mathcal D\cap\mathcal G_R}
   \mathcal S_N((r_{k,R}^{\boldsymbol\lambda}(\tau))_k).}
\tag{S.237}
\]

No continuity of \(\tau\mapsto\ell_k(\tau)\), the six branch masks, or
\(r(\tau)\) is needed.  Only the inherited \(\ell^1\)-continuity of the
terminal \(K\)-vector is used: it identifies the supremum of the left side
of (S.236) on dense good times with its supremum on all terminal times.
Thus

\[
 \boxed{
 \mathcal S_{N,R}^{K}(\mathcal D)
 \le6B_{Q,R}^M
  +C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R
  +6\mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)
 \le C_{\rm pay}(\boldsymbol\lambda)A_R
  +6\mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D).}
\tag{S.238}
\]

Conversely, the coordinatewise upper bound in (S.234), applied with the
same exceptional set and then optimized, gives

\[
 \boxed{
 \mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)
 \le{1\over2}\mathcal S_{N,R}^{K}(\mathcal D).}
\tag{S.239}
\]

Equations (S.238)--(S.239) are the exact reduction.  For a fixed integer
\(N_0\), independent of the scale and the solution,

\[
 \boxed{
 \mathfrak R_{N_0,R}^{\boldsymbol\lambda}(\mathcal D)\lesssim A_R
 \quad\Longleftrightarrow\quad
 \mathcal S_{N_0,R}^{K}(\mathcal D)\lesssim A_R,}
\tag{S.240}
\]

where the implicit constants may depend on the fixed admissible profile.
The forward implication uses (S.238), and the reverse implication uses
(S.239).  This equivalence does not make the residual gate trivial: it
removes the known payments and states exactly where new PDE information is
required.

## 6. Plateau corollary, full-domain gate, and linear fallback

The sharp plateau terminal reduction inherited in Step 9 is

\[
 \mathfrak C_R^M
 \le B_{Q,R}^M+\sqrt N\,Z_R+
       \mathcal S_{N,R}^{K}(I_R).
\]

Combining it with (S.238) gives

\[
 \boxed{
 \begin{aligned}
 \mathfrak C_R^M
 &\le\sqrt N\,Z_R+7B_{Q,R}^M
   +C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R
   +6\mathfrak R_{N,R}^{\boldsymbol\lambda}(I_R)\\
 &\le\sqrt N\,Z_R+
   \bigl[7C_Q+C_5\mathscr L(\boldsymbol\lambda)^{1/3}\bigr]A_R
   +6\mathfrak R_{N,R}^{\boldsymbol\lambda}(I_R).
 \end{aligned}}
\tag{S.241}
\]

The coefficient seven consists of the six \(Q\)-variation units used in
the paid partition and the one unit in the terminal \(K\)-to-flux
reduction.  The plateau estimate is not a full-terminal statement.

The inherited absolute flux-variation bound in (S.234) supplies the
fallback

\[
 \boxed{
 \mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)
 \le C_FP_R^M.
 \quad
 P_R^M\le1\Longrightarrow
 \mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)\le C_FA_R.}
\tag{S.242}
\]

Thus this gate is already quadratic in the small-payment regime.  For
\(P_R^M>1\), the ratio between the inherited linear fallback and the target
is \((P_R^M)^{1/3}\), so no large-payment conclusion follows.

The genuinely open full-domain statement is

\[
 \boxed{
 \text{OPEN: there exist fixed }N_0<\infty, C_{\rm res}<\infty
 \text{ such that }
 \mathfrak R_{N_0,R}^{\boldsymbol\lambda}(\mathcal T_R)
 \le C_{\rm res}A_R
 \text{ uniformly in }R\text{ and the solution}.}
\tag{S.243}
\]

By (S.238), (S.243) implies the full-terminal R0.74Q estimate (Q.12).
The inherited terminal reduction (Q.9) then gives the fixed-scale target
(Q.1).  Neither implication reverses the distinction between
\(I_R\) and \(\mathcal T_R\): a proof of the residual bound only on
\(I_R\) yields (S.241), not full Q.12.  Such a plateau residual bound is
nevertheless already sufficient for the plateau target (Q.1), directly by
(S.241); full (S.243) is the stronger domain-correct route to Q.12.

## 7. Sharpness, boundary, and quantifier stress tests

### 7.1 The constants six and one half

The constants in (S.233) are optimal for the chosen one-sixth split at the
level of abstract continuous clocks.  Normalize \(T=1\) and choose a
short non-\(D\) last-exit interval.  For \(0<\varepsilon<1/6\), the two
admissible residual increments

\[
 \boxed{
 \begin{array}{c|c|c|c}
 \Delta Q&\Delta F=1/3-\Delta Q&T/\Delta F&\Delta F/T\\ \hline
 1/6-\varepsilon&1/6+\varepsilon
   &(1/6+\varepsilon)^{-1}&1/6+\varepsilon\\
 -1/6+\varepsilon&1/2-\varepsilon
   &(1/2-\varepsilon)^{-1}&1/2-\varepsilon
 \end{array}}
\tag{S.244}
\]

approach the lower and upper boundaries.  Hence no uniform coefficient below
six can replace the rightmost inequality in (S.233), and no coefficient
below one half can replace the coordinatewise upper bound in (S.234), using
only \(|\Delta Q|<T/6\).  At \(|\Delta Q|=T/6\), a short non-\(D\) shell
belongs to \(\mathcal P_Q\), so the residual inequalities are correctly
strict.  These are clock-algebra tests, not Navier--Stokes solutions.

### 7.2 One exception budget for both residual mechanisms

Take two residual coordinates with \(T_1=T_2=3\) and
\(r_1=r_2=1\).  The first may be assigned to \(\mathcal R_x\), for
example with \(D_1=3/2\) and failed \(\beta,\sigma\) tests; the second may
be assigned to \(\mathcal R_{\rm sh}\), for example with
\(D_2=1\), \(d_2=1/2\), \(\lambda_2=1\), and \(\Delta Q_2=0\).
Then

\[
 \boxed{
 \mathcal S_1((r_1,r_2))=1,
 \qquad
 \mathcal S_1((r_1,0))+\mathcal S_1((0,r_2))=0.}
\tag{S.245}
\]

The second expression is the forbidden operation of granting one exception
to each branch.  It proves why the combined residual must be formed before
the single best-\(N\) infimum.

Likewise, fixed \(N\) cannot be replaced by a truncation-dependent budget.
For \(T_k=2^{-k}\), \(k\ge1\),

\[
 \boxed{
 \mathcal S_1((T_k)_{k\ge1})={1\over2},
 \qquad
 \mathcal S_1((T_k)_{1\le k\le M})
 ={1\over2}-2^{-M}\longrightarrow{1\over2},
 \qquad
 \mathcal S_M((T_k)_{1\le k\le M})=0.}
\tag{S.246}
\]

The last zero is irrelevant to a theorem with one universal \(N_0\).

### 7.3 Why terminal \(D\)-dominance is not last-exit persistence

It would be invalid to apply the long non-\(D\) proof to
\(\mathcal I_D\).  Here is an explicit rational piecewise-linear clock.
Set \(R^2=1\), \(s_R=0\), \(\tau=2\), \(T=1\), and interpolate linearly
between

\[
 \begin{array}{c|ccccc}
 t&0&1/8&1/4&1&2\\ \hline
 K(t)&0&3/5&2/3&67/100&1\\
 D(t)&0&3/5&3/5&3/5&3/5.
 \end{array}
\]

Then \(K=E+D\) with \(E\ge0\), the last \(2T/3\) exit is
\(\ell=1/4\), and the interval has normalized length \(d=7/4\).  Yet

\[
 \boxed{
 D(\tau)={3T\over5}\ge{T\over2},
 \qquad \Delta D|_{(\ell,\tau)}=0,
 \qquad E(1)={7T\over100}<{T\over6}.}
\tag{S.247}
\]

The witness is continuous and nonnegative, but it is only a clock stress
test.  It shows precisely why the full-history Step 8 trichotomy must remain
in force on \(\mathcal I_D\).

The remaining boundary conventions are also forced:

- \(D_k(\tau)=T_k/2\) belongs to \(\mathcal I_D\);
- \(\beta_k(J_\tau)=T_k/6\) belongs to \(\mathcal I_\beta\);
- after failure of the \(\beta\)-test,
  \(\sigma_k(J_\tau)=T_k/(12\lambda_k)\) fails the strict
  \(\sigma\)-test and belongs to \(\mathcal I_x\);
- \(d_k=\lambda_k^{-3/2}\) belongs to \(\mathcal I_{\rm long}\); and
- \(T_k=0\) has \(r_k=0\) and belongs to none of the six positive-terminal
  classes.

## 8. Route decision

The paid-branch deletion has reached its natural endpoint.  The present
identities and inherited ledgers provide no further compression beyond
(S.240).  The next PDE stage should analyze the two residual mechanisms
separately while retaining one shared exception budget at the final
recombination:

1. **Short non-\(D\), \(Q\)-small packing.**  Here the positive stopped
   flux is comparable to \(T_k\), but it is created on a terminal interval
   shorter than \(R^2\lambda_k^{-3/2}\).  A useful theorem must exploit
   genuinely new cross-shell/PDE input, for example spatial crowding,
   overlap, or a Carleson-type constraint; an \(\ell^2\) sequence inequality
   alone cannot close the tail.
2. **Scalar-excess ancestry.**  Here \(\mathcal I_x\) is known by (S.226)
   to descend from anomalous-defect or high-Rayleigh shells, while its
   full-history \(Q\)-variation and kinetic mass are both below the Step 8
   thresholds.  A useful theorem must pack that remaining defect/high-
   Rayleigh mass; terminal \(D\)-dominance cannot be localized to the
   last-exit interval for free.

The two mechanisms can be investigated in parallel, but their final
best-\(N\) exceptional set cannot be duplicated.  Any proposed estimate
must be tested against (S.245)--(S.247) and against the inherited R0.74O/P
exact family, which refutes only the no-exception gate and does not prove
that \(N_0=1\) suffices.

## 9. Decision and claim ledger

The following are **PROVED**:

- the canonical \(2/3\)-last-exit identities and duration split (S.223)--
  (S.224);
- the exact six-class partition (S.225);
- the Step 7/8 compatibility and absence of a new low-Rayleigh residual
  payment (S.226);
- the single \(6B_Q\) payment and single combined cubic payment
  (S.227)--(S.231);
- positivity and two-sided terminal-clock comparability of the residual,
  together with its inherited \(\ell^2\) and linear bounds
  (S.232)--(S.234);
- the fixed-good-terminal and domain-level best-\(N\) reductions
  (S.235)--(S.240); and
- the plateau corollary and small-payment fallback (S.241)--(S.242); and
- the conditional implication that, *if* the explicitly open statement
  (S.243) holds, then full Q.12 and hence Q.1 follow.

The following are **INHERITED**:

- the canonical completed clocks, absolute variation ledgers,
  \(\ell^1\)-terminal continuity, and square function from R0.74P;
- the terminal best-\(N\) reduction from R0.74Q;
- the shell-dependent cubic payment and padded-shell spatial estimate
  (R.211), (R.214) from R0.74R;
- the Step 7 Rayleigh trichotomy and low-Rayleigh estimate (S.149);
- the Step 8 full-history \(\beta/\sigma/x\) priority trichotomy; and
- the Step 9 last-exit identity and finite good-stop closure.

The following are **REFUTED OR RULED OUT**:

- a new class
  \(\mathcal I_{\rm lo}\setminus
    (\mathcal I_\beta\cup\mathcal I_\sigma)\), because it is empty;
- the claim that two complete \(Q\)- or cubic-ledger charges are necessary;
  those separate double charges are valid but nonsharp and are not used;
- granting a separate \(N\)-exception budget to each residual mechanism;
- localizing terminal \(D\)-dominance to the last-exit interval; and
- obtaining fixed-\(N\) shell compression from last-exit algebra alone.

The following remain **OPEN**:

- the fixed, solution- and scale-independent \(N_0\) estimate (S.243);
- packing the short non-\(D\), \(Q\)-small residual;
- packing the surviving anomalous-defect/high-Rayleigh ancestry in
  \(\mathcal I_x\);
- the full-terminal R0.74Q gate Q.12, fixed-scale inequality Q.1, the
  R0.74R extraction hypotheses, scale contraction, prescribed-centre
  packing, and regularity.

The following are **NOT CLAIMED**:

- that \(\ell_k\) is a good time, or that an infinite family of canonical
  stops is one admissible local-energy test;
- continuity, measurability, or lower semicontinuity in \(\tau\) of the
  last-exit selector, branch masks, or residual vector;
- that Step 8's \(\mathcal I_\beta,\mathcal I_\sigma,\mathcal I_x\) may be
  redefined on \(J_k^{\rm LE}\);
- that terminal \(D\)-dominance or non-dominance is a statement about the
  increment of \(D\) on \(J_k^{\rm LE}\);
- that \(I_R\) and \(\mathcal T_R\) give the same terminal supremum;
- that the admissible profile \(\boldsymbol\lambda\) has been optimized;
- that the scalar stress tests are Navier--Stokes solutions; or
- novelty, priority, singularity formation, regularity, or a solution of
  the Navier--Stokes Millennium problem.

## 10. Inherited source ledger

| Use in this note | Frozen source | Status |
|---|---|---|
| Canonical clocks, absolute \(Q/F\) variation, \(\ell^1\)-terminal continuity, and square function | R0.74P, (2.7)--(3.7) | **INHERITED / PROVED** |
| Fixed-\(N\), terminal-dependent-exception reduction and full-domain Q.12 | R0.74Q, (Q.7)--(Q.12) | **INHERITED / PROVED REDUCTION; PDE TAIL BOUND OPEN** |
| Shell-dependent payment definition and padded-shell estimate | R0.74R, (R.209)--(R.214) | **INHERITED / PROVED** |
| Good-time identity \(K=E+D\), monotonicity of \(D\), low-Rayleigh trichotomy, and kinetic-mass lower bound | R0.74S Step 7, (S.142)--(S.155) | **INHERITED / PROVED** |
| Full-history \(\beta/\sigma/x\) priority trichotomy and paid rows | R0.74S Step 8, (S.163)--(S.199) | **INHERITED / PROVED; NO-EXCEPTION GATE REFUTED** |
| Domain-safe canonical best-\(N\) last exits | R0.74S Step 9, (S.200)--(S.222) | **INHERITED / PROVED; PDE PACKING OPEN** |

The new content is the paid/residual partition, the long non-\(D\)
persistence payment, the no-double-charge recombination, and the residual
best-\(N\) equivalence (S.223)--(S.247).  No novelty or priority claim is
made.

**NOT CLAY.**
