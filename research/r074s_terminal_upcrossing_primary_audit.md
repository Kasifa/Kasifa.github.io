# R0.74S Step 2 — primary audit of the terminal-upcrossing reduction

## Result

**PASS AFTER ENDPOINT-REPRESENTATIVE REPAIR.**  The first stopped-weight
draft used \(1_{(\sigma_k,\tau)}\).  That is harmless inside the time
integral but gives the wrong literal value if the same representative is
evaluated at the terminal time.  The frozen weight now uses
\(1_{(\sigma_k,\tau]}\), so the terminal energy is retained and the
stopped-test interpretation agrees with the difference of the canonical
clock identities.

This is a primary self-audit, not an independent mathematical audit.
**NOT CLAY.**

## 1. Net-upcrossing selection

If the dissipation branch fails, then

\[
 E_{k,R}(\tau)
 =K_{k,R}(\tau)-D_{k,R}(\tau)>\frac12K_{k,R}(\tau).
\]

If the window-average branch also fails, the set on which
\(E_{k,R}(t)<K_{k,R}(\tau)/4\) has positive measure and therefore contains a
local-energy good time.  At such a \(\sigma\), monotonicity of \(D\) gives

\[
 K_{k,R}(\tau)-K_{k,R}(\sigma)
 \ge E_{k,R}(\tau)-E_{k,R}(\sigma)
 >\frac14K_{k,R}(\tau).
\]

The conclusion uses the two failed branches, not an invalid general claim
that every large positive variation contains a net increment of equal size.

**Decision: PASS.**

## 2. Family reduction and signs

For each selected shell,
\(\Delta K_k=\Delta Q_k+\Delta F_k\).  Summing the strict quarter
upcrossings and using only
\(\sum_k|\Delta Q_k|\le\sum_k\operatorname{TV}Q_k\le C_QA_R\) yields

\[
 \frac14\sum_{k\in I}K_{k,R}(\tau)
 <C_QA_R+W_R^M.
\]

Replacing \(W_R^M\) by its positive part is an upper enlargement, and
multiplication by four gives (S.27).  No absolute value is placed on the
individual \(F_k\) increments.

**Decision: PASS.**

## 3. Actual padded-cutoff binding

Expanding the finite sum in (S.26) using the inherited R0.74P flux primitive
gives

\[
\begin{aligned}
 W_R^M
 &=\frac1R\int_{s_R}^{\tau}\!\int\eta_R\mathcal W_R^M\cdot
   \sum_{k\in I}\gamma_k1_{(\sigma_k,\tau]}\nabla\Psi_k^R\\
 &=\frac1R\int_{s_R}^{\tau}\!\int
   \eta_R\mathcal W_R^M\cdot\nabla\Xi.
\end{aligned}
\]

The sum is finite, so no infinite-series or Fubini issue occurs.  The value
of the indicator at \(\tau\) does not affect the integral, but it is required
for the terminal trace in the stopped local-energy test.  The pressure gauge
cancels separately for every shell by incompressibility.

**Decision: PASS AFTER REPRESENTATIVE REPAIR.**

## 4. Temporal jumps and measure row

Subtracting \(K=E+D=Q+F\) at the two good times gives (S.32) directly.
The difference \(D(\tau)-D(\sigma)\) is nonnegative even if the temporal
marginal of the local-energy measure has an atom at \(\sigma\), because the
canonical clock is defined through \(Q+F\) and the measure difference is
monotone.  In the smooth approximation to the stopped test, the positive
turn-on derivative produces \(E(\sigma)\) on the right side.  No hard-time
measure section is used to define the canonical clock.

**Decision: PASS.**

## 5. Absolute-payment boundary

Taking absolute values in (S.31), then expanding the finite stopped sum,
gives a subintegral of the inherited nonnegative absolute shell ledger.
Therefore \(|W_R^M|\le CP_R^M\).  This becomes a quadratic-scale estimate
only when \(P_R^M\le1\), since then \(P_R^M\le(P_R^M)^{2/3}\).  For
\(P_R^M>1\), the unresolved ratio is exactly \((P_R^M)^{1/3}\).

**Decision: PASS.**  The audit does not promote the linear bound to the open
quadratic stopped-work estimate.

## 6. Finite certificate

The certificate passes 5/5 exact rational checks, 1/1 exact four-shell
balance fixture, and 19/19 structural checks.  Two consecutive runs
regenerated the outputs byte for byte.  A mutation replacing the quarter
threshold by a third was rejected.

| Artifact | SHA-256 |
|---|---|
| r074s_terminal_upcrossing_stopped_work.md | 3ec5f9b894f89e9febb95e5a100836b5b18e455f8366bf99e93b746ac6353da4 |
| r074s_terminal_upcrossing_certificate.py | 2733bc02e295e4b19fcf62599814994cc6321dd281862cf6d46c9e75533dd85e |
| r074s_terminal_upcrossing_certificate.json | ab277a9f8eb8477223272b35d3abfda2ce713491760a7ce38a3bc7f17aa8965d |
| r074s_terminal_upcrossing_certificate_report.md | 77585266cb7bcc1af7a6cbfafc1b47a33dadf6612c543a1a1ddef31a82404045 |

The finite certificate does not prove good-time selection, local-energy
identities, inherited variation/payment estimates, or the open signed
depletion theorem.

## 7. Exact open gate

R0.74S Step 2 reduces the recent-upcrossing family to
\(\mathfrak W_{{\rm up},R}^M\).  The remaining bound

\[
 \mathfrak W_{{\rm up},R}^M\stackrel{?}{\le}C(P_R^M)^{2/3}
\]

must use signed Navier--Stokes structure in the large-payment regime.  The
dissipation branch and R0.74R persistence packing also remain open.
