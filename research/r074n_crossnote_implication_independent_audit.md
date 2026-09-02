# R0.74N independent cross-note implication audit

## 1. Fail-closed history, binding, and verdict

This audit was opened because the first R0.74N synthesis correctly closed the
collar observable but incorrectly left the exact-family endpoint quantity
\(X_j\) marked open.  Before writing this file, the rebind also failed closed
on an overly strong proposed source-diff invariant: the old 55 displays were
not all byte-identical.  The authorized and verified invariant is instead
53/55 unchanged, with (0.3) extended by the cross-note summary and (0.6)
expanded to state the complete inherited cutoff.  All 49 shell-body displays
(1.1)--(6.5) are unchanged, and (6.6)--(6.11) are new.

This verdict binds the following exact objects.

| Object | SHA-256 | Role |
|---|---|---|
| research/r074n_all_shell_synthesis.md | ca1ddabb6ea931b2f1a96b5cb000e955492c6852b0ea3b2aaa6148c6f3fa9e1e | final proof and Corollary 6.2 |
| research/r074n_problem_freeze.md | 4b2df724cf81cf28d0c9b89636ae166ade11746f623ca2a3466f08e4e1adfacc | frozen question, complete cutoff, post-closure correction |
| research/r074n_gap_matrix.md | 986a2ddc20318f6f70a968f80fd972c671e7ae43fe769e2acd00d4230d08fb06 | final claim boundary |
| research/r074f_two_packet_survival.md | 0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb | exact family and endpoint-energy lower bound |
| research/r074h_collar_flux_two_regime_closure.md | 8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1 | signed-flux energy closure and component estimates |
| research/r074j_matching_payment_law.md | d495ff3d069eceea9dd7bbf1c467f8836cb72033cde7a9d9c17e9b585478dbad | common complete payment and logarithmic scale |
| research/r074k_single_collar_shear_lag_reduction.md | 8f21248603551c39f34864dd921847dc8b9c6f70962209864901d476fe6722e3 | exact collar normalization and sufficient conversion |

**Verdict: PASS.**  For the one frozen smooth periodic unforced family and all
sufficiently large \(j\), the cited results rigorously imply

\[
 X_j\asymp\mathfrak C_j\asymp B_j^2L_jR_j^2
 \asymp P_j^{2/3}\sqrt{1+\log_+P_j}.
\]

They also imply a matching lower and upper bound for the endpoint exterior
energy component and only an upper bound for the exterior dissipation
component.  No arbitrary-flow or regularity statement follows.

## 2. Object identity: family, amplitude, and the two frames

R0.74F (1.12)--(1.13) defines

\[
 u_j=(\mathfrak a_jF_j,B_j\theta_j,0),\qquad p_j=0,
\]

as an exact smooth periodic mean-zero unforced solution and proves that its
terminally anchored mollified trajectory and both acceleration rows vanish:

\[
 X_{R_j}(t)\equiv0,\qquad a_{R_j}=a_{R_j}'=0.
\]

Here \(X_{R_j}(t)\) is the trajectory; it is not the endpoint quantity
\(X_{R_j}^{\alpha}\).  The zero trajectory makes \(v_{R_j}=w_{R_j}=u_j\),
so Versions M and F use the same field, pressure, annuli, endpoint quantities,
collar flux, and payment.  R0.74J (1.4)--(1.7) independently records the same
family with

\[
 \mathfrak a_j=B_j\Gamma_j^{-1/2},\qquad
 P_j=P_{R_j}^M=P_{R_j}^F.
\]

There is therefore no frame or amplitude substitution hidden in the
cross-note implication.  The Version-F acceleration payment is exactly zero,
not merely discarded.

## 3. Time windows and the complete cutoff

R0.74F fixes \(t_{0,j}=65R_j^2\).  R0.74H uses

\[
 I_R=(t_0-R^2,t_0),\qquad s_R=t_0-4R^2,
\]

which become

\[
 I_{R_j}=(64R_j^2,65R_j^2),\qquad s_{R_j}=61R_j^2.
\]

Its hypothesis \(\overline I_{8R_j}\Subset(0,T)\) is satisfied: the exact
solution is smooth beyond \(t_{0,j}\), while
\(I_{8R_j}=(R_j^2,65R_j^2)\).  R0.74F uses the positive-measure terminal
interval

\[
 J_j=(t_{0,j}-R_j^3,t_{0,j})\subset I_{R_j},
\]

so the essential supremum defining the endpoint exterior energy sees the
surviving packet.

The R0.74H cutoff is smooth and nondecreasing and satisfies

\[
 \eta_R=0\ \hbox{near }s_R,\qquad
 \eta_R=1\ \hbox{on }I_R,\qquad
 0\le\eta_R\le1,\qquad |\eta_R'|\le CR^{-2}.
\]

The final problem freeze (F.4) and proof (0.6) now state this complete system.
The shell estimate itself uses only \(0\le\eta_R\le1\), but the appeal to the
R0.74H weighted identity uses the same complete cutoff.  Hence there is no
cutoff or endpoint mismatch.

## 4. Collar identity, sign, and normalization

R0.74H defines

\[
 \mathfrak C_R^\alpha
 =\sup_{\tau\in I_R}[\mathfrak F_R^\alpha(\tau)]_+.
\]

On the exact family, its full flux reduces exactly to

\[
 \mathfrak F_R(\tau)
 =\frac{\mathfrak a^2B}{2R}
 \int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb R^3}\theta F^2
 \partial_2\vartheta_R^{\rm ann}\,dx\,dt.
\]

R0.74K (4.1)--(4.3) uses this same smooth annular weight, time cutoff, full
periodic lift, and signed packet integral.  R0.74N Theorem 6.1 proves exactly
the K hypothesis.  Since \(B_j>0\) for all sufficiently large \(j\), pulling
the prefactor through the positive part does not reverse its sign.

Substituting \(\mathfrak a_j^2=B_j^2/\Gamma_j\) into the K conversion gives

\[
\begin{aligned}
 \mathfrak C_j
 &\le \frac{B_j^3}{2R_j\Gamma_j}
       C_I\Gamma_jL_jR_j^5\\
 &=\frac{C_I}{2}(B_jR_j^2)B_j^2L_jR_j^2.
\end{aligned}
\]

Because \(B_jR_j^2\to1/128\), this is

\[
 \mathfrak C_j\le C B_j^2L_jR_j^2.
\]

Thus the factors \(1/(2R_j)\), \(B_j\), \(\Gamma_j^{-1}\), and \(R_j^5\)
are all accounted for.  No sign, factor-two, or power-of-\(R_j\) mismatch is
present.

## 5. Exact definitions of \(X\), \(\mathcal U\), and \(\mathcal D\)

R0.74H retains the R0.74E endpoint definitions and writes

\[
 X_R^\alpha
 =\mathcal U_{\rm ext}^{\infty,\alpha,R}
 +\mathcal D_{\rm ext}^{\alpha,R}.
\]

Both summands are nonnegative.  The proof of H Theorem 5.1 gives them
separately, not merely after summation:

\[
 \mathcal U_{\rm ext}^{\infty,\alpha,R},\quad
 \mathcal D_{\rm ext}^{\alpha,R}
 \le C\left[(P_R^\alpha)^{2/3}+\mathfrak C_R^\alpha\right].
\]

For the endpoint energy this follows by taking the essential supremum of H
(5.1a); for dissipation it is H (5.1b).  The final N definitions (6.6) are
therefore exact aliases, not new endpoints.

Put

\[
 T_j=B_j^2L_jR_j^2.
\]

R0.74J Theorem 3.3 gives

\[
 cB_j^3R_j^3\le P_j\le CB_j^3R_j^3,
\]

and therefore

\[
 P_j^{2/3}\le CB_j^2R_j^2\le CT_j
\]

once \(L_j\ge1\).  Together with the completed collar upper bound, H gives

\[
 \mathcal U_j\le CT_j,\qquad
 0\le\mathcal D_j\le CT_j,\qquad
 X_j\le CT_j.
\]

R0.74F Theorem 6.2 is sharper about the source of the lower bound.  Its proof
shows

\[
 \mathcal U_j
 \ge c\mathfrak a_j^2\Gamma_jL_jR_j^2
 =cT_j.
\]

Consequently

\[
 cT_j\le\mathcal U_j\le X_j\le CT_j,
 \qquad 0\le\mathcal D_j\le CT_j.
\]

The argument proves no lower bound \(\mathcal D_j\ge cT_j\).  In particular,
the lower bound for \(X_j\) must not be relabelled as dissipation production.

## 6. Square-root-log conversion

R0.74J (4.6) proves, on this exact sequence,

\[
 P_j^{2/3}\sqrt{1+\log_+P_j}
 \asymp B_j^2L_jR_j^2=T_j.
\]

Combining this identity with the two-sided endpoint and collar bounds gives

\[
 X_j\asymp\mathfrak C_j\asymp T_j
 \asymp P_j^{2/3}\sqrt{1+\log_+P_j}.
\]

This uses the complete payment \(P_j\), not a packet-only or pre-acceleration
surrogate.  Since acceleration vanishes on this family, the M and F complete
payments coincide exactly.

## 7. Uniformity and threshold intersection

The H constant depends only on the frozen mollifier, cutoff profiles, and
torus convention and is independent of the solution, frame, and \(j\).  The
F, J, K, and N statements likewise use constants independent of \(j\) after
their respective threshold indices.  Taking the maximum of finitely many
thresholds simultaneously ensures

- the F packet survival and \(J_j\subset I_{R_j}\);
- \(B_j>0\), \(L_j\ge1\), and bounded \(B_jR_j^2\);
- the K conversion and N all-shell estimate; and
- the H time-window and cutoff hypotheses.

No constant in the final comparison grows with \(j\).

## 8. Non-circular dependency audit

The implication is not circular.

1. R0.74F obtains the \(\mathcal U_j\) lower bound from packet survival and
   terminal annular residence; it assumes no endpoint upper bound.
2. R0.74H obtains the signed-flux energy closure from the exact weighted
   energy identity; it assumes no familywise collar upper bound.
3. R0.74J obtains the payment law from a nonnegative fifth-shell velocity
   cubic row and the earlier direct payment upper bound; it assumes neither
   the N all-shell estimate nor the \(X_j\) upper bound.
4. R0.74K is a one-way algebraic conversion from its signed integral
   hypothesis to the collar upper bound; it does not assume \(X_j\).
5. R0.74N proves the K hypothesis by the inward/target/outer shell split; its
   shell argument does not estimate \(\mathcal U_j\), \(\mathcal D_j\), or
   \(X_j\) directly.

Only after these independent arrows are complete does H transfer the N collar
bound and J payment bound to the endpoint upper bound.

## 9. Exact boundary

The proved result concerns one constructed smooth periodic 2D3C family.  It
does not prove

- a matching lower bound for \(\mathcal D_j\) alone;
- a universal square-root-log endpoint estimate for arbitrary smooth flows;
- an arbitrary-flow all-shell collar estimate;
- payment-to-admissibility or prescribed-point core-from-shell control;
- singularity formation or exclusion; or
- global existence and smoothness.

No novelty or priority claim follows from this implication audit.
**NOT CLAY.**

\[
 \boxed{\text{R0.74N CROSS-NOTE IMPLICATION: PASS; FAMILYWISE ONLY; NOT CLAY.}}
\]
