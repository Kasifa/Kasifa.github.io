# R0.74S Step 6 — exact cross-channel recombination is circular, even for one block

## 0. Result and scope

R0.74S Steps 4--5 complete all four geometric collar channels by
nonnegative boundary or ball clocks.  This note tests the strongest
remaining linear possibility: retain the signs of all completed clocks
until after the four channels have been recombined.

The outcome is exact and negative.

1. For each of the five linear rows \(E,D,Q,F,K\), the signed root,
   outer, weight-drop, and mismatch terms recombine to the original sum of
   stopped shell increments.
2. If the mismatch is kept separate, the other three channels form one
   nonnegative genealogy cutoff.  Its insertion jumps have the favorable
   sign, so every stop/merge debt disappears and only one terminal
   genealogy clock remains.
3. That terminal clock has an exact nonnegative \(\ell^1\) decomposition
   into one root-boundary clock per final block and all shell residuals.
   Adding the mismatch back reconstructs the unknown positive upcrossing
   sum exactly.
4. A smooth scalar clock family with one simultaneous activation epoch,
   one active block, and no block merger has stopped work \(N\), while its
   matched square function is only \(\sqrt N\).  The entire contribution
   is carried by the outer and weight-drop rows with the same sign.

Thus component count, activation-epoch count, or merger count cannot by
themselves repair the \(\ell^1/\ell^2\) mismatch.  This is a rigorous
route rejection inside the scalar completed-clock algebra.  It is not a
Navier--Stokes solution or a PDE counterexample.  A PDE-weighted block
length charge, cross-channel dynamical sign theorem, and the
dissipation-dominated branch remain **OPEN / NOT CLAIMED**.  **NOT CLAY.**

All notation and suitable-weak conventions are inherited from R0.74S
Steps 2--5.

## 1. A universal stopped-row recombination

For a scalar row \(X\), write

\[
 \Delta_a^bX:=X(b)-X(a).
\tag{S.112}
\]

Take

\[
 X\in\{E,D,Q,F,K\}.
\]

Let \(X_{k,R}\) be the weighted shell row,
\(X_{m,R}^{\partial}\) the weighted boundary-bump row, and
\(\mathscr X_{m,R}^{\pm}\) the two unweighted ball rows.  At every
admissible endpoint, linearity and the cutoff identities from Step 5 give

\[
\boxed{
\begin{aligned}
 X_{k,R}
 &=\gamma_k
   (\mathscr X_{k+1,R}^+-\mathscr X_{k,R}^-),\\
 X_{m,R}^{\partial}
 &=\gamma_m
   (\mathscr X_{m,R}^+-\mathscr X_{m,R}^-).
\end{aligned}}
\tag{S.113}
\]

For \(Q,F,K\), these are identities of their canonical representatives at
every time.  For \(E,D\), they are used only at the good stopping and
terminal times.

Retain the Step-5 sets \(I_{\rm rt},I_{\rm out},I^\partial\) and endpoints
\(\rho_k,\lambda_k,\widehat\sigma_m\).  Define the four-channel row

\[
\begin{aligned}
 \mathfrak C_X
 :={}&-\sum_{k\in I_{\rm rt}}\gamma_k
   \Delta_{\sigma_k}^{\rho_k}\mathscr X_{k,R}^-\\
 &+\sum_{k\in I_{\rm out}}\gamma_k
   \Delta_{\sigma_k}^{\lambda_k}\mathscr X_{k+1,R}^+\\
 &+\sum_{m\in I^\partial}d_m
   \Delta_{\widehat\sigma_m}^{\tau}\mathscr X_{m,R}^+\\
 &+\sum_{m\in I^\partial}
   \Delta_{\widehat\sigma_m}^{\tau}X_{m,R}^{\partial}.
\end{aligned}
\tag{S.114}
\]

### Theorem 1.1 — exact stopped-row recombination

For every finite stopped family and every row in (S.113),

\[
\boxed{
 \mathfrak C_X
 =\sum_{k\in I}\Delta_{\sigma_k}^{\tau}X_{k,R}.}
\tag{S.115}
\]

**Proof.**  At a non-stopping time, decompose the active set into maximal
blocks.  On one block \([p,q]_{\mathbb Z}\), the first identity in
(S.113) gives

\[
\begin{aligned}
 \sum_{k=p}^qX_{k,R}
 ={}&-\gamma_p\mathscr X_{p,R}^-
     +\gamma_q\mathscr X_{q+1,R}^+\\
 &+\sum_{m=p+1}^q
   \left[d_m\mathscr X_{m,R}^+
         +X_{m,R}^{\partial}\right].
\end{aligned}
\tag{S.116}
\]

Indeed, the internal coefficient is

\[
 \gamma_{m-1}\mathscr X_m^+
 -\gamma_m\mathscr X_m^-
 =d_m\mathscr X_m^+
  +\gamma_m(\mathscr X_m^+-\mathscr X_m^-).
\]

Shell \(k\) is a root on \((\sigma_k,\rho_k]\), is an outer edge on
\((\sigma_k,\lambda_k]\), and an internal boundary \(m\) is present on
\((\widehat\sigma_m,\tau]\).  Summing (S.116) over the finitely many
event intervals gives (S.114)--(S.115).  Equivalently, direct expansion at
the stopping endpoints gives the same finite identity, so no time
differentiability of the \(E,D\) rows is used.  \(\square\)

## 2. Recombining the actual stopped work

For \(X=F\), the first three rows of (S.114) are exactly the root, signed
outer, and weight-drop formulas (S.97)--(S.99).  The last row is the
boundary-mismatch formula (S.73).  Therefore

\[
\boxed{
 \mathfrak C_F
 =W_R^M(\tau;I,\boldsymbol\sigma).}
\tag{S.117}
\]

Since every completed row satisfies \(F=K-Q\), Theorem 1.1 gives

\[
\boxed{
\begin{aligned}
 W_R^M
 &=\mathfrak C_K-\mathfrak C_Q\\
 &=\sum_{k\in I}\Delta_{\sigma_k}^{\tau}K_{k,R}
   -\sum_{k\in I}\Delta_{\sigma_k}^{\tau}Q_{k,R}.
\end{aligned}}
\tag{S.118}
\]

The quadratic row is already paid:

\[
 |\mathfrak C_Q|
 \le\sum_{k\ge1}\operatorname {TV}Q_{k,R}
 \le C_QA_R.
\tag{S.119}
\]

On the other hand, the defining terminal upcrossings (S.25) imply

\[
\boxed{
 \mathfrak C_K
 =\sum_{k\in I}\Delta_{\sigma_k}^{\tau}K_{k,R}
 >\frac14\sum_{k\in I}K_{k,R}(\tau).}
\tag{S.120}
\]

Thus the signed completed-clock recombination has not made the difficult
term smaller: it has reconstructed the target that Proposition 2.1 of
Step 2 is trying to bound.  An estimate for \(\mathfrak C_K\) at the
quadratic scale would be a valid new theorem, but it does not follow from
(S.113)--(S.120).  Replacing its signed pieces separately by clock
positivity instead produces the \(\ell^1\) terminal/start debts isolated
in Step 5.

## 3. One-block saturation of the complete recombination

The circularity is sharp within the scalar clock algebra.  Fix
\(s_R<\sigma<\tau\) and \(N\ge1\).  Choose a smooth nondecreasing
\(h:[s_R,\tau]\to[0,1]\) that vanishes on \([s_R,\sigma]\) and satisfies
\(h(\tau)=1\).  Put

\[
 I_N=\{1,\ldots,N\},
 \qquad
 \sigma_k=\sigma\quad(k\in I_N),
\tag{S.121}
\]

and define the abstract shell and boundary clocks by

\[
 K_{k,R}=F_{k,R}
 =\begin{cases}
   h,&1\le k\le N,\\
   0,&k>N,
  \end{cases}
 \qquad
 Q_{k,R}=0,
 \qquad
 K_{m,R}^{\partial}=F_{m,R}^{\partial}=Q_{m,R}^{\partial}=0.
\tag{S.122}
\]

Set \(B_1=0\) and recursively define

\[
 B_{m+1}=B_m+\gamma_m^{-1}K_{m,R},
 \qquad
 \mathscr K_{m,R}^-=\mathscr K_{m,R}^+=B_m.
\tag{S.123}
\]

For every shell, boundary, and ball clock, assign the scalar rows

\[
 E=K,\qquad D=0,\qquad Q=0,\qquad F=K.
\tag{S.124}
\]

Then all scalar completed-clock identities (S.90), cutoff relations
(S.113), and tower relations (S.91)--(S.92) hold.  Every selected shell
has

\[
 \Delta_{\sigma}^{\tau}K_{k,R}=1
 >\frac14K_{k,R}(\tau),
\tag{S.125}
\]

so this is a stopped terminal-upcrossing family.  Its active set is empty
up to \(\sigma\) and equals the single block \([1,N]_{\mathbb Z}\)
afterward.  Hence

\[
 \sup_tN(t)=1,
 \qquad
 \#\{\hbox{activation epochs}\}=1,
 \qquad
 \#\{\hbox{block mergers}\}=0.
\tag{S.126}
\]

The root and mismatch completed rows vanish.  The outer and weight-drop
rows are

\[
\begin{aligned}
 \mathfrak C_K^{\rm out}
 &=\gamma_NB_{N+1}(\tau),\\
 \mathfrak C_K^{\rm gap}
 &=\sum_{m=2}^{N}d_mB_m(\tau).
\end{aligned}
\tag{S.127}
\]

Because

\[
 B_m(\tau)=\sum_{j=1}^{m-1}\gamma_j^{-1},
\]

finite telescoping gives

\[
\boxed{
 \gamma_NB_{N+1}(\tau)
 +\sum_{m=2}^{N}d_mB_m(\tau)=N.}
\tag{S.128}
\]

Indeed, for \(j<N\), the coefficient of \(\gamma_j^{-1}\) is
\(\gamma_N+\sum_{m=j+1}^{N}d_m=\gamma_j\), while the \(j=N\) term is
paid by \(\gamma_N\).

More precisely, with

\[
 \varepsilon_N:=\sum_{j=1}^{N-1}\frac{\gamma_N}{\gamma_j},
\]

the two nonzero channels satisfy

\[
 \mathfrak C_K^{\rm out}=1+\varepsilon_N,
 \qquad
 \mathfrak C_K^{\rm gap}=N-1-\varepsilon_N.
\]

For \(N\ge2\), the frozen super-Gaussian weights give

\[
 0\le\varepsilon_N
 \le(N-1)\exp\!\left(-\frac{3\cdot4^{N-2}}{32}\right).
\]

Thus the outer and gap contributions have the same nonnegative sign; the
gap row alone is \(N-1-o(1)\).

Define the scalar stopped-work value of this abstract family by
\(W_N^{\rm sc}:=\mathfrak C_F\).  The shell clocks are nondecreasing, so
their positive variations satisfy

\[
\boxed{
 W_N^{\rm sc}=\mathfrak C_F=\mathfrak C_K=N,
 \qquad
 Y_{2,R}^{\rm sf}=\sqrt N.}
\tag{S.129}
\]

Consequently there is no universal constant \(C\), derived only from the
scalar completion, cutoff linearity, tower identities, and the three
fixed genealogy statistics in (S.126), for which

\[
\boxed{
 [W_N^{\rm sc}]_+\le C Y_{2,R}^{\rm sf}.}
\tag{S.130}
\]

This is a statement about what cannot be deduced from the listed scalar
axioms.  The symbol \(W_N^{\rm sc}\) is not the work of a constructed PDE
solution.  The witness remains valid if the stops are chosen with
\(\sigma_1<\cdots<\sigma_N\) inside a common interval on which \(h=0\);
then the block grows one adjacent shell at a time and never splits or
merges.  The one-epoch formulation is retained because tied good stopping
times are allowed by Step 2.

## 4. The strongest three-channel genealogy completion

The full recombination is circular because it includes the mismatch clock.
There is nevertheless a sharper statement for the three channels that
remain after Step 4 has isolated that mismatch.  For a finite shell set
\(A\), define the periodized genealogy cutoff

\[
 \Omega_A^R
 :=\sum_{k\in A}\gamma_k\Psi_k^R
   -\sum_{m\in A^\partial}\gamma_mB_m^R,
 \qquad
 A^\partial:=\{m\ge2:m-1,m\in A\}.
\tag{S.131}
\]

Here \(B_m^R\) is the Step-4 boundary-bump periodization, not either
Step-5 ball cutoff.  The Euclidean support geometry gives the pointwise
inequality

\[
\boxed{
 0\le
 \gamma_kB_k^R+\gamma_{k+1}B_{k+1}^R
 \le\gamma_k\Psi_k^R.}
\tag{S.132}
\]

On the lift, (S.87) gives the exact identity

\[
 \psi_k^R-\beta_k^R-\beta_{k+1}^R
 =\chi_{k+1,R}^- -\chi_{k,R}^+\ge0.
\]

The last inequality follows from
\(r_{k+1}-r_k>2\delta\): wherever \(\chi_{k,R}^+\) is nonzero,
\(\chi_{k+1,R}^-=1\).  Thus the two boundary bumps fit inside the
padded shell without overlap loss.  Summing this lifted inequality over
each lattice translate, and using \(\gamma_{k+1}\le\gamma_k\), proves
(S.132); no disjointness of different periodic copies is required.

If \(k\notin A\), adding shell \(k\) changes (S.131) by

\[
\begin{aligned}
 \Omega_{A\cup\{k\}}^R-\Omega_A^R
 ={}&\gamma_k\Psi_k^R
 -1_{\{k-1\in A\}}\gamma_kB_k^R\\
 &-1_{\{k+1\in A\}}\gamma_{k+1}B_{k+1}^R
 \ge0.
\end{aligned}
\tag{S.133}
\]

Thus \(\Omega_A^R\ge0\), and inclusion of shell sets increases the
cutoff.  Let

\[
 \Phi_A(t):=\mathscr K_R[\Omega_A^R](t)
 =\sum_{k\in A}K_{k,R}(t)
  -\sum_{m\in A^\partial}K_{m,R}^{\partial}(t)\ge0.
\tag{S.134}
\]

For each distinct value \(a\) among the stopping times, write

\[
 A_a^-:=\{k\in I:\sigma_k<a\},
 \qquad
 A_a^+:=\{k\in I:\sigma_k\le a\}.
\]

All shells with stop \(a\) may be inserted one at a time in any order.
Equation (S.133) and positivity of the completed clock imply

\[
\boxed{
 \Phi_{A_a^+}(a)-\Phi_{A_a^-}(a)\ge0.}
\tag{S.135}
\]

Define the stopped work without the mismatch channel by

\[
 W_{R,3}^M
 :=\frac1R\int_{s_R}^{\tau}\eta_R(t)
 [\mathcal R_R(t)-\mathcal L_R(t)+\mathcal G_R(t)]\,dt.
\]

Writing \(\Phi_A^X:=\mathscr X_R[\Omega_A^R]\), summing the fixed-cutoff
flux increments over the event intervals gives

\[
\boxed{
 W_{R,3}^M
 =\Phi_I^F(\tau)
  -\sum_a[\Phi_{A_a^+}^F(a)-\Phi_{A_a^-}^F(a)].}
\tag{S.136}
\]

This is also obtained by subtracting the Step-4 mismatch formula from the
four-channel identity (S.117).  Put

\[
 \delta\Omega_a:=\Omega_{A_a^+}^R-\Omega_{A_a^-}^R\ge0.
\]

Applying the same event identity to (X=Q) identifies the next left side
with the root, outer, and weight-drop (Q)-channels.  It is paid
explicitly by (S.94):

\[
\begin{aligned}
 &\left|\Phi_I^Q(\tau)
  -\sum_a\mathscr Q_R[\delta\Omega_a](a)\right|\\
 &\quad\le
 \sum_{k\in I_{\rm rt}}\gamma_k
       \operatorname {TV}\mathscr Q_{k,R}^-
 +\sum_{k\in I_{\rm out}}\gamma_k
       \operatorname {TV}\mathscr Q_{k+1,R}^+\\
 &\qquad
 +\sum_{m\in I^\partial}d_m
       \operatorname {TV}\mathscr Q_{m,R}^+
 \le CA_R.
\end{aligned}
\]

There is a slightly stronger use of the completed local-energy identity
than merely dropping the nonnegative insertion clocks.  Define

\[
 D_{\rm post}
 :=\sum_a\left(
   \mathscr D_R[\delta\Omega_a](\tau)
  -\mathscr D_R[\delta\Omega_a](a)\right).
\]

Each summand is nonnegative because \(\delta\Omega_a\ge0\) and the
dissipation row is nondecreasing.  Moreover,
\(\sum_a\delta\Omega_a=\Omega_I^R\), so linearity gives

\[
 0\le D_{\rm post}\le\Phi_I^D(\tau).
\]

Now expand \(F=E+D-Q\) in (S.136).  The kinetic insertion values
\(\mathscr E_R[\delta\Omega_a](a)\) are nonnegative, while the
dissipation bracket is exactly \(D_{\rm post}\).  More explicitly,

\[
\begin{aligned}
 W_{R,3}^M
 ={}&\Phi_I^E(\tau)
   -\sum_a\mathscr E_R[\delta\Omega_a](a)
   +D_{\rm post}\\
  &-\left(\Phi_I^Q(\tau)
   -\sum_a\mathscr Q_R[\delta\Omega_a](a)\right).
\end{aligned}
\]

Hence

\[
\boxed{
 [W_{R,3}^M]_+
 \le\Phi_I^E(\tau)+D_{\rm post}+CA_R
 \le\Phi_I(\tau)+CA_R.}
\tag{S.137}
\]

In particular, all starting and merge-time completed clocks from the
separate bounds (S.100)--(S.102) have disappeared.  The remaining terminal
clock, however, has no hidden cancellation.  If \([a,b]_{\mathbb Z}\) is
one final block and

\[
 r_m(t):=K_{m,R}(t)-K_{m,R}^{\partial}(t)\ge0,
\]

then the Step-5 tower gives

\[
\begin{aligned}
 &\gamma_b\mathscr K_{b+1,R}^+(t)
 +\sum_{m=a+1}^{b}d_m\mathscr K_{m,R}^+(t)\\
 &\qquad
 =\gamma_a\mathscr K_{a,R}^+(t)
  +\sum_{m=a}^{b}r_m(t).
\end{aligned}
\tag{S.138}
\]

Combining the right side with the negative root-ball term in (S.116)
yields the exact nonnegative block decomposition

\[
\boxed{
 \Phi_I(t)
 =\sum_{[a,b]\in\operatorname {Comp}(I)}
 \left[K_{a,R}^{\partial}(t)
       +\sum_{m=a}^{b}r_m(t)\right]
  =\sum_{[a,b]\in\operatorname {Comp}(I)}
  \left[K_{a,R}(t)
       +\sum_{m=a+1}^{b}r_m(t)\right].}
\tag{S.139}
\]

Thus the favorable three-channel combination removes temporal genealogy
debts but ends at one root-boundary term per final block plus the complete
\(\ell^1\) residual mass.  In the witness (S.121)--(S.129), every boundary
clock is zero and every selected residual is one, so
\(\Phi_{I_N}(\tau)=N\).  The bound (S.137) is therefore sharp inside the
same scalar algebra.

## 5. Exact finite genealogy count

The event bookkeeping itself is also linear in the number of selected
shells.  Let \(n=|I|\), let \(c(I)\) be the number of connected components
of \(I\), and put

\[
 e_{\rm tie}(I,\boldsymbol\sigma)
 :=\#\{m\in I^\partial:\sigma_{m-1}=\sigma_m\}.
\tag{S.140}
\]

Every static component contributes one unconditional root and one
unconditional outer edge.  Every unequal adjacent stop contributes to
exactly one of \(I_{\rm rt}\) or \(I_{\rm out}\), while an equal adjacent
stop contributes to neither.  Hence

\[
\boxed{
\begin{aligned}
 |I^\partial|&=n-c(I),\\
 |I_{\rm rt}|+|I_{\rm out}|&=n+c(I)-e_{\rm tie},\\
 |I_{\rm rt}|+|I_{\rm out}|+|I^\partial|&=2n-e_{\rm tie}.
\end{aligned}}
\tag{S.141}
\]

This is an exact finite-complexity statement, but its scale is \(O(n)\),
not a dimension-free \(\ell^2\) packing.  For the simultaneous one-block
witness, \(c=1\) and \(e_{\rm tie}=N-1\); the three families still contain
\(N+1\) rows and carry total mass \(N\).

## 6. What is and is not ruled out

Equations (S.115)--(S.120) prove a precise dichotomy for the present
linear route.

- Keeping all completed-clock signs recombines exactly to the unknown
  stopped shell increment sum.
- Applying nonnegativity to the pieces before recombination returns the
  unmatched \(\ell^1\) clocks from Step 5.
- Bounding only the number of active components, activation epochs, or
  block mergers cannot bridge the gap, because all three statistics are
  fixed in (S.126) while \(N\to\infty\).

The witness does **not** rule out a theorem that charges block length,
clock amplitude, or an incidence measure to local dissipation or another
Navier--Stokes quantity at the quadratic scale.  It also does not rule out
a PDE sign relation between kinetic, pressure, drift, and dissipation
rows.  Those assertions use information absent from the scalar algebra.

The three-channel improvement (S.137) is not discarded: it proves that
stop and merge clocks are artifacts of estimating the channels
separately.  The obstruction is now localized to the terminal quantity
(S.139), not to the temporal genealogy.

## 7. Decision and next gate

The following are **PROVED**:

- the universal four-channel recombination (S.112)--(S.116);
- its exact identification with stopped work and the original completed
  shell increments (S.117)--(S.120); and
- the one-block scalar saturation (S.121)--(S.130);
- the nonnegative genealogy cutoff, favorable insertion signs, and
  three-channel terminal estimate (S.131)--(S.139); and
- the exact finite genealogy count (S.140)--(S.141).

The result closes only a method class: linear cutoff completion plus
unweighted block-component genealogy.  The next viable gate must add a
PDE-paid quantity that sees block length or signed transport before local
energy is compressed to scalar clocks.  A concrete alternative is to
return to the dissipation branch of (S.23), where the positive measure may
provide such a charge.

A PDE-weighted genealogy theorem, cross-channel flux sign/depletion,
quadratic control of the dissipation branch, the R0.74R persistence
hypotheses, unconditional fixed-scale (Q.1), scale contraction,
regularity, singularity formation, and the Millennium problem remain
**OPEN / NOT CLAIMED**.  **NOT CLAY.**

## 8. Inherited source ledger

| Use | Frozen source | Status |
|---|---|---|
| Terminal upcrossing and stopped-work reduction | R0.74S Step 2, (S.22)--(S.38) | **INHERITED / PROVED** |
| Actual four-channel collar decomposition | R0.74S Step 3, (S.39)--(S.59) | **INHERITED / PROVED** |
| Boundary mismatch completion | R0.74S Step 4, (S.60)--(S.84) | **INHERITED / PROVED** |
| Ball cutoff identities and stopped orientations | R0.74S Step 5, (S.85)--(S.111) | **INHERITED / PROVED** |

No novelty or priority claim is made.
