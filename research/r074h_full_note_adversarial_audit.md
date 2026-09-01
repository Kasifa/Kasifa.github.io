# R0.74H — full-note adversarial pre-freeze audit

## Verdict and source binding

**FINAL ADVERSARIAL PASS.** No fatal analytic error, circular inference,
reversed inequality, missing scale, broken cross-reference, or claim-boundary
violation was found in the complete note.

This read-only audit is bound to

    research/r074h_collar_flux_two_regime_closure.md
    SHA-256 14ec43c55d833ea498d9ccd1a9e4514b015d8db41194615360af7376ccc433fe

The verdict applies only to that byte sequence. The main note and all other
research artifacts were left unchanged during this audit.

## 1. Definition closure and geometry

The note is definitionally closed relative to the frozen R0.74E source it
identifies at the start. It imports the local trajectory, gauges, annuli,
energy, cubic, harmonic, and acceleration ledgers, then explicitly defines
every quantity newly used in R0.74H:

| Quantity | Definition or source | Audit result |
|---|---|---|
| \(X_R^\alpha\) | (1.12) | nonnegative exterior endpoint plus dissipation |
| \(P_{0,R}^\alpha\) | (1.9) | pre-acceleration nonnegative payment |
| \(P_R^M,P_R^F\) | (1.10)--(1.11) | Version F alone adds \(\mathcal J_{\mathrm{acc}}^{3/2}\) |
| \(\Theta_{R,N},\Theta_R\) | (2.3)--(2.6) | legitimate periodic finite tests and licensed \(C^2\) limit |
| \(\mathfrak F_R^\alpha,\mathfrak C_R^\alpha\) | (3.8)--(3.9) | cumulative signed flux and its nonnegative positive part |
| \(\mathfrak Q_R^\alpha\) | (4.7) | nonnegative majorant for both quadratic cutoff rows |
| \(\widehat P_R^\alpha\) | (5.2) | repaired payment with the required \(3/2\) flux power |
| \(\vartheta_R^{\mathrm{ann}}\) | (7.1a) | nonperiodized lift-side weight used only after unfolding |

There is one trajectory \(X_R\) throughout. No radius-dependent replacement
trajectory is introduced. The spatial and temporal buffers are consistent:

| Role | Radius/time interval | What it pays |
|---|---|---|
| target | \(R\), \(I_R=(t_0-R^2,t_0)\) | \(U_\gamma\), \(G_\gamma\), and \(X_R\) |
| collar/payment | \(2R\), \(I_{2R}=(t_0-4R^2,t_0)\) | time cutoff, padded shells, cubic/pressure/harmonic rows, shell acceleration |
| core buffer | \(8R\), \(I_{8R}=(t_0-64R^2,t_0)\) | inner collars, local pressure source, and core acceleration |

The time cutoff starts at \(s_R=t_0-4R^2\), vanishes there, and equals one
on \(I_R\). The hypothesis
\(\overline I_{8R}\Subset(0,T)\) licenses every interval. The exact shift
\(A_k(R)=A_{k-1}(2R)\) is used in the correct direction. The first inner
shells are not forced through that shift; they are paid by the \(8R\) core.

## 2. Weighted identities and uniform constants

The Version-M and Version-F equations, pressure Poisson identities, signs,
and normalizations close consistently. In particular:

1. the moving Version-M field retains \(v_R-a_R\) in its transport and has
   no body force;
2. the Version-F field has canonical transport \(w_R\) and the separate
   constant force \(-a_R'\);
3. the scalar pressure gauge vanishes under periodic integration by parts;
4. the Version-F shell-force term has size at most
   \(\mathcal J_{\mathrm{acc,sh}}/2\); and
5. the \(3/2\) acceleration power inside \(P_R^F\) becomes linear after the
   outer \(2/3\) power.

The constants in the proof come from the fixed mollifier/cutoff profiles,
lattice summability, Hölder/Sobolev interpolation, Calderón--Zygmund, and
harmonic estimates. They are independent of the particular smooth
solution, \(R\), \(z_0\), and the explicit-family index \(j\). This is the
standard meaning of the letter \(C\) in the displayed theorems and is the
uniformity required in Section 7.

For publication clarity, the note could state this constant convention in
one sentence after Section 1. The omission is not an analytic gap because
the displayed proof supplies the uniform constants and never selects a
solution-dependent bound.

## 3. Theorem 5.1 to Theorem 6.2 to Corollary 6.3

The quantifier chain is valid for both
\(\alpha\in\{M,F\}\) and every smooth periodic unforced solution satisfying
the interior-time hypothesis.

First, the exact identities and the nonnegative cutoff majorant give

\[
 X_R^\alpha
 \le C\left[(P_R^\alpha)^{2/3}+\mathfrak C_R^\alpha\right].
\]

The endpoint-energy and full-dissipation parts are obtained separately and
then added, so neither part is silently used twice. In Version F the
acceleration is already included in \((P_R^F)^{2/3}\).

Second, Lemma 6.1 bounds the absolute collar flux by the pre-acceleration
ledger:

\[
 \sup|\mathfrak F_R^M|\le CP_R^M,
 \qquad
 \sup|\mathfrak F_R^F|\le CP_{0,R}^F.
\]

Combining these rows yields exactly (6.7)--(6.8). No hypothesis or
conclusion from Section 7 is used in this derivation.

Finally, when \(P_R^\alpha\le1\),

\[
 P_R^\alpha\le(P_R^\alpha)^{2/3},
 \qquad P_{0,R}^F\le P_R^F,
\]

so Corollary 6.3 follows with the same scope. The note correctly calls this
a one-scale size implication rather than propagation, absorption, or
epsilon regularity.

## 4. Non-circular audit of equation (7.5a)

The large-payment conclusion does not reverse or misuse the R0.74G upper
bound. Its logic is:

1. R0.74F and the amplitude choice give

   \[
   X_{R_j}\ge cB_j^2L_jR_j^2\longrightarrow\infty.
   \]

2. If \(P_{R_j}\le1\) occurred along an unbounded subsequence, Theorem 6.2
   (equivalently Corollary 6.3) would give a uniform bound for \(X_{R_j}\),
   contradicting step 1.

3. Hence \(P_{R_j}>1\) eventually. Then
   \(P_{R_j}^{2/3}\le P_{R_j}\), and Theorem 6.2 gives

   \[
   X_{R_j}\le CP_{R_j}.
   \]

4. Therefore

   \[
   P_{R_j}\ge cX_{R_j}
   \ge cB_j^2L_jR_j^2\longrightarrow\infty.
   \]

This proves (7.5a) without using (7.5). The inherited R0.74G row

\[
 P_{R_j}\le CB_j^3R_j^3
\]

is used only afterward, through (4.8), to obtain
\(\mathfrak Q_{R_j}\le CB_j^2R_j^2\). It is never promoted to a matching
lower bound. Thus there is no circular dependence between Theorem 6.2 and
the explicit-family diagnosis.

## 5. Direction of the Section 7 claims

Unfolding uses the nonperiodized radial weight

\[
 \vartheta_R^{\mathrm{ann}}=\sum_{k\ge1}\gamma_k\psi_k^R.
\]

Its derivatives are integrable, so (7.2) is a legitimate
\(\mathbb R^3\) identity. Parity removes every \(\partial_1\) row and the
pure-shear \(\partial_2\) row. The remaining packet--shear term has the
displayed sign, factor \(1/(2R)\), and amplitude \(\mathfrak a^2B\).

The terminal weighted energy is larger than the quadratic cutoff row by a
factor \(L_j\). Nonnegative dissipation in the exact identity therefore
forces only the lower statements

\[
 \mathfrak C_{R_j}\ge cB_j^2L_jR_j^2,
 \qquad
 \mathfrak C_{R_j}^{3/2}
 \ge cB_j^3L_j^{3/2}R_j^3.
\]

The note does not claim a reverse flux comparison, matching upper bound,
two-sided asymptotic, or equivalence. It also explicitly declines a
matching \(P_R\gtrsim B_j^3R_j^3\) claim. The Section 7 conclusions have
the correct one-sided direction.

## 6. Literature, novelty, and Millennium boundary

The four primary arXiv records cited in Section 8 have matching titles,
authors, and abstract-level scopes:

- weighted \(L^2\) weak solutions and weighted energy controls;
- a broader weighted Leray/suitable-solution theory with an axisymmetric
  no-swirl application;
- local-energy solutions under truncated Morrey-type hypotheses; and
- local-energy solutions in Wiener-amalgam spaces.

The note uses these papers only as methodological context. It does not
attribute the R0.74H periodic moving-frame theorem to them. The bounded
source ledger explicitly says that failure to locate the exact theorem is
not evidence of novelty. The main note repeats that the comparison is not
exhaustive and makes no novelty or priority claim.

The conclusions are also correctly separated from the Millennium problem.
The note proves a smooth-solution positive-scale size estimate. It leaves
open weak-solution stability, independent payment of the positive flux,
scale iteration, absorption, epsilon regularity, continuation, singularity
exclusion, and global regularity. Both the opening scope and final gap list
state **NOT CLAY**.

## 7. Cross-references and conclusion audit

All equation tags in the note are unique. The internal references to
(2.2), (2.7)--(2.9), (3.1)--(3.7), (4.4)--(4.8), (5.1)--(5.5),
(6.1)--(6.9), and (7.4)--(7.8) point to existing rows and are used in the
correct direction. References explicitly prefixed by R0.74E, R0.74F, or
R0.74G refer to the frozen predecessor notes rather than an identically
numbered row in R0.74H.

The summary in Section 9 matches the proved inventory. It does not promote
the identity-level flux to an independent regularity budget, the
small-payment implication to a scale iteration, or the explicit-family
lower bound to a two-sided theorem.

## 8. Required corrections and final decision

**Required corrections: none.**

One optional clarity improvement is to state explicitly that theorem
constants depend only on the fixed cutoff/mollifier choices and not on the
solution, scale, centre, or explicit-family index. The proof already has
this uniformity, so this is not required for the bound source SHA to pass.

The complete note at the bound SHA is internally coherent, correctly
quantified under standard constant conventions, non-circular, one-sided
where required, and conservative about literature, novelty, regularity, and
the Millennium problem.

**FINAL ADVERSARIAL PASS. NOT CLAY.**
