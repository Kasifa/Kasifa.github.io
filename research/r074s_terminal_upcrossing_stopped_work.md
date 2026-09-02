# R0.74S Step 2 — terminal net upcrossings reduce to one stopped signed-work functional

## 0. Result and scope

R0.74R states its third clock branch using recent positive variation.
The first result below strengthens that branch: if neither accumulated
dissipation nor preceding-window average kinetic energy is large, then one
can choose a single good stopping time \(\sigma<\tau\) at which the
completed clock has a genuine net increase of at least one quarter of its
terminal value.

For any finite family of such shells, all net increases reduce exactly to
one stopped signed-work integral built from the actual R0.74P padded
cutoffs.  The complete \(Q\)-increment is paid by
\(A_R=(P_R^M)^{2/3}\).  Taking absolute values on the stopped work gives
only the inherited linear bound \(CP_R^M\); therefore the remaining
large-payment question is one signed depletion estimate, not a BV
bookkeeping problem.

The stopped-work estimate at the quadratic scale remains **OPEN**.  No
regularity or Clay conclusion is claimed.  **NOT CLAY.**

## 1. The variation branch contains a single net upcrossing

Use the R0.74R completed-clock split

\[
 K_{k,R}=E_{k,R}+D_{k,R}=Q_{k,R}+F_{k,R},
 \qquad D_{k,R}\ \hbox{nondecreasing},
\tag{S.22}
\]

at local-energy good times.

### Proposition 1.1 — strengthened three-way terminal triage

Let \(\tau\in(s_R,t_0)\) be a good terminal time,
\(J=(a,\tau)\subset(s_R,t_0)\), and
\(T=K_{k,R}(\tau)\).  At least one of the following holds:

\[
 D_{k,R}(\tau)\ge\frac T2,
\qquad
 \fint_JE_{k,R}(t)\,dt\ge\frac T4,
\tag{S.23}
\]

or there exists a local-energy good time \(\sigma\in J\) such that

\[
 \boxed{
 K_{k,R}(\tau)-K_{k,R}(\sigma)>\frac T4.}
\tag{S.24}
\]

**Proof.**  If both alternatives in (S.23) fail, then
\(E_{k,R}(\tau)=T-D_{k,R}(\tau)>T/2\).  Since the window average is less
than \(T/4\), the positive-measure set
\(\{t\in J:E_{k,R}(t)<T/4\}\) contains a local-energy good time
\(\sigma\).  Monotonicity of \(D\) gives

\[
\begin{aligned}
 K_{k,R}(\tau)-K_{k,R}(\sigma)
 &=E_{k,R}(\tau)-E_{k,R}(\sigma)
   +D_{k,R}(\tau)-D_{k,R}(\sigma)\\
 &>T/2-T/4=T/4.
\end{aligned}
\]

This proves (S.24).  \(\square\)

Thus the last branch of R0.74R (R.207) can be represented by a terminal net
upcrossing, not merely by a sum of unrelated oscillations.

## 2. A family of upcrossings and the quadratic \(Q\)-payment

Fix a good terminal time \(\tau\), a finite shell set
\(I\subset\mathbb N\), and good stopping times
\(\sigma_k\in(s_R,\tau)\) satisfying

\[
 K_{k,R}(\tau)-K_{k,R}(\sigma_k)
 >\frac14K_{k,R}(\tau),
 \qquad k\in I.
\tag{S.25}
\]

Define the stopped signed work

\[
 W_R^M(\tau;I,\boldsymbol\sigma)
 :=\sum_{k\in I}
   \bigl[F_{k,R}(\tau)-F_{k,R}(\sigma_k)\bigr].
\tag{S.26}
\]

### Proposition 2.1 — terminal upcrossing reduction

For every family satisfying (S.25),

\[
 \boxed{
 \sum_{k\in I}K_{k,R}(\tau)
 \le4C_QA_R
   +4\bigl[W_R^M(\tau;I,\boldsymbol\sigma)\bigr]_+,}
\tag{S.27}
\]

where \(C_Q\) is the constant in the inherited bound
\(\sum_k\operatorname{TV}Q_{k,R}\le C_QA_R\).

**Proof.**  Sum (S.25) and use \(K=Q+F\):

\[
\begin{aligned}
 \frac14\sum_{k\in I}K_{k,R}(\tau)
 &<\sum_{k\in I}
   [K_{k,R}(\tau)-K_{k,R}(\sigma_k)]\\
 &=\sum_{k\in I}
   [Q_{k,R}(\tau)-Q_{k,R}(\sigma_k)]
   +W_R^M(\tau;I,\boldsymbol\sigma)\\
 &\le C_QA_R+W_R^M(\tau;I,\boldsymbol\sigma)\\
 &\le C_QA_R+
       [W_R^M(\tau;I,\boldsymbol\sigma)]_+.
\end{aligned}
\tag{S.28}
\]

Multiply by four.  \(\square\)

No absolute variation of \(F_{k,R}\) appears in (S.27).

## 3. Exact binding to the actual padded-shell flux

Write the R0.74P Version-M work vector

\[
 \mathcal W_R^M
 :=\frac12|v_R|^2(v_R-a_R)+(\pi_R-c_R)v_R.
\tag{S.29}
\]

For the stopped family define the time-dependent finite spatial weight

\[
 \Xi_{\tau,I,\boldsymbol\sigma}(t,y)
 :=\sum_{k\in I}
   \gamma_k1_{(\sigma_k,\tau]}(t)\Psi_k^R(y).
\tag{S.30}
\]

Linearity of the exact R0.74P flux primitive gives

\[
 \boxed{
 W_R^M(\tau;I,\boldsymbol\sigma)
 =\frac1R\int_{s_R}^{\tau}\!\int_{\mathbb T^3}
   \eta_R(t)\mathcal W_R^M(t,y)\cdot
   \nabla\Xi_{\tau,I,\boldsymbol\sigma}(t,y)
   \,dy\,dt.}
\tag{S.31}
\]

This is an identity for the actual periodized padded cutoffs; it does not
assume the ideal adjacent-boundary representation used in R0.74S Step 1.
The pressure gauge contributes zero shell by shell because
\(\nabla\cdot v_R=0\).

## 4. The stopped local-energy identity and its jump rows

At the good stopping and terminal times, subtract the completed-clock
identity at \(\sigma_k\) from the identity at \(\tau\), then sum over
\(I\).  One obtains

\[
\begin{aligned}
 &\sum_{k\in I}E_{k,R}(\tau)
 +\sum_{k\in I}
   [D_{k,R}(\tau)-D_{k,R}(\sigma_k)]\\
 &\qquad=
 \sum_{k\in I}E_{k,R}(\sigma_k)
 +\sum_{k\in I}
   [Q_{k,R}(\tau)-Q_{k,R}(\sigma_k)]
 +W_R^M(\tau;I,\boldsymbol\sigma).
\end{aligned}
\tag{S.32}
\]

Equation (S.32) is also what results from approximating the discontinuous
test \(\eta_R\Xi\) by smooth nonnegative time cutoffs.  Its distributional
time derivative contains a positive atom at each \(\sigma_k\); those atoms
are exactly the stopping-energy terms
\(\sum_kE_{k,R}(\sigma_k)\).  They cannot be silently discarded.

For the stops constructed in Proposition 1.1,

\[
 E_{k,R}(\sigma_k)<\frac14K_{k,R}(\tau),
\tag{S.33}
\]

while the post-stop dissipation on the left of (S.32) is nonnegative.
Thus the jump row has precisely the size already reserved in the
one-quarter upcrossing argument.

## 5. What absolute values prove, and no more

From (S.31),

\[
\begin{aligned}
 |W_R^M(\tau;I,\boldsymbol\sigma)|
 \le{}&\frac1R\sum_{k\in I}\gamma_k
 \int_{\sigma_k}^{\tau}\!\int_{\mathbb T^3}\eta_R
 \left[
  \frac12|v_R|^2(|v_R|+|a_R|)
  +|\pi_R-c_R|\,|v_R|
 \right]|\nabla\Psi_k^R|.
\end{aligned}
\tag{S.34}
\]

All summands are nonnegative, so insertion of the stopped time indicators
only decreases the R0.74P absolute shell ledger.  Therefore

\[
 \boxed{
 |W_R^M(\tau;I,\boldsymbol\sigma)|
 \le\mathfrak L_{{\rm abs},R}^M
 \le CP_R^M.}
\tag{S.35}
\]

If \(P_R^M\le1\), then \(P_R^M\le A_R\), and (S.27)--(S.35) already pay the
entire terminal-upcrossing family at the quadratic scale.  The unresolved
regime is exactly

\[
 P_R^M>1,
 \qquad
 \frac{P_R^M}{A_R}=(P_R^M)^{1/3}.
\tag{S.36}
\]

R0.74S Step 1 proves that an ideal adjacent-shell Abel transform followed
by absolute values cannot supply a compensating shell factor.  Equation
(S.35) shows the same linear payment directly for the actual padded
cutoffs.

## 6. The minimal stopped-work gate

Let \(\mathfrak W_{{\rm up},R}^M\) be the supremum of
\([W_R^M(\tau;I,\boldsymbol\sigma)]_+\) over all good terminal times,
finite shell sets, and good stopping families satisfying (S.25):

\[
 \mathfrak W_{{\rm up},R}^M
 :=\sup_{\substack{\tau,I,\boldsymbol\sigma\\\text{(S.25) holds}}}
   [W_R^M(\tau;I,\boldsymbol\sigma)]_+.
\tag{S.37}
\]

Then Proposition 2.1 gives the exact sufficient interface

\[
 \boxed{
 \mathfrak W_{{\rm up},R}^M\le C A_R
 \quad\Longrightarrow\quad
 \sum_{k\in I}K_{k,R}(\tau)\le C A_R}
\tag{S.38}
\]

for every terminal-upcrossing family.

The left side of (S.38) is weaker than the full shellwise absolute-flux
variation: it retains a common terminal time, one low-energy stop per
shell, and the sign after summing all stopped work.  It is nevertheless not
controlled by the present ledgers beyond (S.35).

## 7. Exact remaining boundary

The following are now **PROVED**:

- the strengthened terminal triage (S.23)--(S.24);
- the family reduction (S.27), with the entire \(Q\) row paid by \(A_R\);
- the actual padded-cutoff stopped-work identity (S.31);
- the complete stopped balance including temporal jump energies (S.32);
- the absolute estimate (S.35); and
- automatic quadratic payment of this branch when \(P_R^M\le1\).

The following remain **OPEN**:

- the large-payment stopped-work depletion estimate in (S.38);
- any sign relation between the stopped boundary work, negative
  work/backscatter, and exterior leakage;
- a PDE payment or finite-exception theorem for the dissipation-dominated
  branch of (S.23);
- the persistence packing hypotheses of R0.74R;
- the unconditional fixed-scale inequality (Q.1), a contraction or
  prescribed-centre scale-packing theorem, regularity, singularity
  formation, and the Clay problem.

The next gate is not another absolute estimate.  It must split the signed
integrand in (S.31) into forward work, negative work/backscatter, exterior
supply/leakage, pressure, and moving-frame drift without discarding their
signs.  **NOT CLAY.**

## 8. Inherited source ledger

| Use in this note | Frozen source | Status |
|---|---|---|
| \(K=E+D=Q+F\), good-time endpoint interpretation, and canonical continuous clocks | r074p_temporal_observable_triage.md, (2.6)--(2.10), (5.9)--(5.10) | **INHERITED / PROVED** |
| Full \(Q\)-variation estimate used in (S.28) | r074p_temporal_observable_triage.md, (3.4)--(3.6) | **INHERITED / PROVED** |
| Exact Version-M flux primitive used in (S.29)--(S.31) | r074p_temporal_observable_triage.md, (2.9) | **INHERITED / PROVED** |
| Absolute stopped-flux domination in (S.34)--(S.35) | r074p_temporal_observable_triage.md, (3.4a), (3.6); R0.74H (6.3)--(6.6) | **INHERITED / PROVED** |
| Abel-plus-absolute-values coefficient no-gain | r074s_weighted_abel_no_gain.md, (S.1)--(S.21) | **PROVED IN STEP 1 / IDEAL ADJACENT MODEL** |

The new analytic results are Proposition 1.1, Proposition 2.1, the stopped
identities (S.31)--(S.32), and the conditional interface (S.38).  No
novelty or priority claim is made.
