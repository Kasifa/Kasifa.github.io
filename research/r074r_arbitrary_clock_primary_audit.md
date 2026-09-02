# R0.74R Step 2 — primary mathematical audit

## Status

**PASS AFTER SCOPE REPAIR.**  This is a primary self-audit of the analytic
argument and its inherited source bindings.  It is not an independent audit.
The first draft stated its extraction hypothesis only for good terminal times
in \(I_R\) but concluded the R0.74Q tail supremum over every
\(\tau<t_0\).  That inference was not justified.  The theorem has been
repaired on the full cutoff interval \((s_R,t_0)\), using cutoff-weighted
kinetic persistence and an explicit good-time-to-all-time closure.

No unconditional extraction theorem, fixed-scale inequality, regularity
criterion, or Clay conclusion is certified here.  **PRIMARY AUDIT ONLY. NOT
CLAY.**

## 1. Inherited-source backtracking

| Input used in Step 2 | Direct source check | Audit result |
|---|---|---|
| \(K_{k,R}=E_{k,R}+D_{k,R}=Q_{k,R}+F_{k,R}\), \(K_{k,R}(s_R)=0\), \(K_{k,R}\ge0\), with \(D_{k,R}\) nondecreasing | R0.74P (2.6)--(2.10) and problem freeze (F.9)--(F.11) | **PASS.**  \(E+D\) is read at local-energy good times; \(Q+F\) selects the canonical absolutely continuous clock at every time. |
| \(\sum_k\operatorname{TV}Q_{k,R}\le C(P_R^M)^{2/3}\) and \(\sum_k\operatorname{TV}F_{k,R}\le CP_R^M\) | R0.74P (3.4)--(3.7) | **PASS.**  Both variations are on \([s_R,t_0)\), and the pressure gauge is removed before absolute estimation. |
| Padded-shell volume and periodization/unfolding | R0.74E (4.12b)--(4.12d); R0.74H (2.1)--(2.7) | **PASS.**  The support volume is \(O(2^{3k}R^3)\); the physical shell weight \(\gamma_k\) is already inside the unfolded sum. |
| Complete cubic support payment | R0.74H (4.1)--(4.6) | **PASS.**  \(R^{-2}\sum_k\gamma_k\int_{I_{2R}}\int_{\operatorname{supp}\psi_k^R}|\widetilde v_R|^3\le CP_R^M\).  Shell-dependent indicators \(1_{J_k}(t)\) may be inserted because every integrand is nonnegative. |
| Full terminal best-\(N\) reduction | R0.74Q (Q.7)--(Q.12) | **PASS.**  The target is \(\sup_{\tau<t_0}\mathcal S_N((K_{k,R}(\tau))_k)\), not merely a supremum over \(I_R\).  This check exposed the original scope gap. |

## 2. Endpoint averaging and triage

At a good terminal time and for almost every good \(t<\tau\),

\[
 E_{k,R}(\tau)-E_{k,R}(t)
 =K_{k,R}(\tau)-K_{k,R}(t)
  -\bigl[D_{k,R}(\tau)-D_{k,R}(t)\bigr].
\]

The last bracket is nonnegative.  Taking the terminal-inclusive positive
variation of \(K\) and averaging in \(t\) proves (R.204).  Subadditivity of
positive variation under \(K=Q+F\) gives (R.205).  If
\(D(\tau)<K(\tau)/2\), then \(E(\tau)>K(\tau)/2\); splitting the right side of
(R.204) at \(E(\tau)/2\) proves the two remaining \(K(\tau)/4\) alternatives.

**Decision: PASS.**  The open interval \(J=(a,\tau)\) does not discard the
terminal increment because the definition of
\(\operatorname{Var}^{+}_{J\rightsquigarrow\tau}\) explicitly ends its
partitions at \(\tau\).

## 3. Full-interval persistence repair

The corrected endpoint row is

\[
 e_{k,R}^{\eta}(t)
 =\frac{\gamma_k\eta_R(t)}{2R}
   \int\psi_k^R|\widetilde v_R(t)|^2,
\]

and its matching cubic row uses \(\eta_R^{3/2}\).  Spatial Hölder gives

\[
\begin{aligned}
 \left(\int\psi_k^R|\widetilde v_R|^2\right)^{3/2}
 &\le |\operatorname{supp}\psi_k^R|^{1/2}
       \int_{\operatorname{supp}\psi_k^R}|\widetilde v_R|^3,\\
 (e_{k,R}^{\eta})^{3/2}
 &\le C\,2^{3k/2}R^2\gamma_k^{1/2}
 \left[R^{-2}\gamma_k\eta_R^{3/2}
       \int_{\operatorname{supp}\psi_k^R}|\widetilde v_R|^3\right].
\end{aligned}
\]

Thus every power in (R.213) is forced:

\[
 2^{3k/2}\mapsto2^k,\qquad
 \gamma_k^{1/2}\mapsto\gamma_k^{1/3},\qquad
 (\Theta^\eta)^{-1}\mapsto(\Theta^\eta)^{-2/3},\qquad
 p\mapsto p^{2/3}.
\]

Because \(0\le\eta_R^{3/2}\le1\) and \(\eta_R\) is supported in
\(I_{2R}\), arbitrary shell-dependent preterminal sets obey

\[
 \sum_k p_{k,R}^{u,\eta}(J_k)\le CP_R^M.
\]

Hölder across shells with exponents \(3\) and \(3/2\) then cubes the
coefficient to
\(2^{3k}\gamma_k\Lambda_k^3(\Theta_k^\eta)^{-2}\).

**Decision: PASS.**  On \(I_R\), \(\eta_R=1\), so this correction retains
the plateau theorem while also covering the transition part of the clock.

## 4. Good times versus the all-time R0.74Q supremum

For nonnegative \(x\in\ell^1\), define for finite \(G\subset\mathbb N\)

\[
 s_{N,G}(x)
 :=\inf_{\substack{S\subset G\\\#S\le N}}
   \sum_{k\in G\setminus S}x_k.
\]

Then

\[
 \mathcal S_N(x)=\sup_{G\Subset\mathbb N}s_{N,G}(x).
\]

Each \(s_{N,G}\) is a minimum of finitely many continuous
finite-coordinate functions.  Therefore \(\mathcal S_N\) is lower
semicontinuous for coordinatewise convergence.  The R0.74P canonical clocks
are continuous coordinatewise, and local-energy good times have full measure
and hence are dense.  If \(\tau_m\) are good and \(\tau_m\to\tau\), then

\[
 \mathcal S_N(K(\tau))\le
 \liminf_{m\to\infty}\mathcal S_N(K(\tau_m)).
\]

Consequently, the conditional \(CA_R\) bound at every good time in
\((s_R,t_0)\) extends to every terminal time.  The frozen zero extension
handles times at or before \(s_R\).

**Decision: PASS AFTER REPAIR.**  No uniform \(\ell^1\)-continuity of the
whole clock vector is assumed or needed.

## 5. Conditional theorem and exact boundary

Under (R.216)--(R.217), summing outside \(S_\tau\), applying the shell
Hölder estimate, and using the cubic support ledger gives

\[
 \sum_{k\notin S_\tau}K_{k,R}(\tau)
 \le C_qA_R+C C_*^{1/3}(P_R^M)^{2/3}\le CA_R.
\]

Section 4 promotes this good-time estimate to the all-time best-\(N_0\)
tail, so R0.74Q (Q.9) yields (R.219).  This proves only the implication.
The existence of universal \(N_0,C_q,C_*\) and of the data
\(S_\tau,q_k,\Lambda_k,J_k\) remains **OPEN**.

## 6. Functional no-go checks

- Proposition 5.1 exactly satisfies the completed-clock algebra with all
  mass in the monotone dissipation row and no kinetic window.
- Proposition 5.2 is placed inside \(I_R\), where \(\eta_R=1\); its endpoint
  energy is fixed while both cubic payment and \(\Theta^\eta\) vanish with
  the time thickness.
- In Proposition 5.3,
  \(w_n=\nabla\times(n^{-2}\zeta\sin(nx_1)e_3)\) is divergence free,
  \(\|w_n\|_3=O(n^{-1})\), and the leading term in
  \(\partial_1(w_n)_2\) has nonzero \(L^2\) limit size.

**Decision: PASS WITH BOUNDARY.**  These are algebraic or functional
witnesses, not Navier--Stokes solutions and not counterexamples to (Q.1).

## 7. Reproducibility gate

The repaired finite certificate passes 13/13 exact rational checks, 3/3
exponent ledgers, and 25/25 structural checks.  A second run regenerated the
JSON and report byte for byte.  A mutation replacing the cubed shell factor
\(2^{3k}\) by \(2^{2k}\) was rejected.

| Artifact | SHA-256 |
|---|---|
| r074r_arbitrary_clock_extraction_gate.md | ac959f30b254001910e5b445264ea7c0d8714afc2f96dcf74505f5e1f794b6b7 |
| r074r_arbitrary_clock_gate_certificate.py | d2d9efa939d49b659a5bbbff5a99b02933234c168590b93a9f13dcd8e3321c63 |
| r074r_arbitrary_clock_gate_certificate.json | b4c743ba1d0caa1ad2a18e15d001f2e28116dc9d2def52030bfb29f2f8824ec6 |
| r074r_arbitrary_clock_gate_certificate_report.md | c666496221c0f1d87395ed51db61aea3d996acb0a3d36fb09612f7dfa038be5a |

These checks certify arithmetic, exponent and scope sentinels only.  An
independent mathematical audit remains required before R0.74R can be frozen
for publication.
