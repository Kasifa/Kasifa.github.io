# R0.74S Step 8 — primary analytic audit of the defect-relaxed total Rayleigh excess

## 1. Verdict

**UNCONDITIONAL PASS ON THE LOCKED SOURCE.**  After the in-source repairs
described below, the final source is analytically
consistent with the frozen R0.74P, R0.74R, R0.74S Step 2, and R0.74S Step 7
inputs.  All equations (S.163)--(S.199) pass.  In particular:

- the one-sixth priority thresholds are exhaustive with the stated strict
  remainder;
- Jensen gives the literal \(1/2\) factor and the per-shell constant is
  \(C_4=12(2C_1)^{2/3}\);
- the shell coefficient cubes to
  \(2^{3k}\gamma_k\lambda_k^3\);
- the scalar terminal excess and the Jordan local envelope are kept
  distinct;
- the open-terminal Portmanteau argument, strong \(L^1\) convergence of the
  explicit \(Q\)-density, and both shellwise and all-shell lower
  semicontinuity passages are valid;
- both global excess ledgers are finite at fixed scale;
- the scalar excess is bounded by terminal positive flux and by the
  inherited stopped-work gate; and
- on the priority-selected excess class,
  \(F_k(\tau)>5K_k(\tau)/6\), giving the sharp displayed coefficient
  \(6/5\) in the stopped-work reduction;
- the no-exception stopped-work supremum is equivalent, modulo the already
  paid \(Q\)-variation, to both the full terminal clock supremum and the
  full-cutoff positive cumulative flux, with the sharp coefficient one in
  the latter comparison; and
- the inherited smooth exact family refutes a universal quadratic bound for
  that no-exception supremum.

The final audited source is
research/r074s_defect_relaxed_total_rayleigh_excess.md, SHA-256
0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab.

The audit initially found two material omissions in source SHA-256
58e9d7856402e639528fd9c2c166b590d293ce68c891d397d9c1de47d2c05766:
the scalar excess was not connected to terminal flux/stopped work, and the
prose incorrectly allowed the fixed-scale global excess sums to be infinite.
The final source repairs both points in (S.192)--(S.196), updates the
claim/source ledgers, and states the exact remaining boundary.

A second audit pass separated the inherited plateau supremum
\(\mathfrak C_R^M\) from the full-cutoff supremum required by (S.37).
The locked source defines \(\mathfrak C_{{\rm full},R}^M\), proves the
direct coefficient-one comparison in (S.198), includes its sharp scalar
stress test, and uses only
\(\mathfrak C_R^M\le\mathfrak C_{{\rm full},R}^M\) in (S.199).

This is a primary mathematical audit, not an independent proof of all
inherited suitable-weak theory and not a novelty or priority certificate.
The universal no-exception stopped-work antecedent is refuted, not open.
The conditional implications (S.38) and (S.196) remain correct, and a
fixed best-\(N\), terminal-dependent-exception estimate remains open.  The
note does not prove (Q.1), regularity, or the Millennium problem.
**NOT CLAY.**

## 2. Frozen-source backtracking

| Input used by Step 8 | Direct source check | Audit result |
|---|---|---|
| Total dissipation and anomalous split | R0.74P, (2.1)--(2.4), gives \(\boldsymbol\mu=|\nabla u|^2dxdt+\boldsymbol D\), with \(\boldsymbol D\ge0\) | **PASS** |
| Open-terminal completed clock | R0.74P, (2.6)--(2.10), gives \(K=E+D=Q+F\), \(Q(s_R)=F(s_R)=K(s_R)=0\), and agreement with the physical rows at good times | **PASS** |
| Absolute clock ledgers | R0.74P, (3.4)--(3.6), gives \(\sum_k\operatorname{TV}Q_k\le C(P_R^M)^{2/3}\) and \(\sum_k\operatorname{TV}F_k\le CP_R^M\) | **PASS** |
| Fixed-scale compactness | R0.74P, Lemmas 5.1--5.3, gives uniform path convergence, strong moving-field convergence, local weak-* convergence of \(\boldsymbol\mu_n\), and strong \(L^1_t\) convergence of the quadratic \(Q\)-density | **PASS** |
| Shell-dependent cubic payment | R0.74R, (R.209)--(R.215), permits one measurable time set per shell and has coefficient \(2^{3k/2}\gamma_k^{1/2}\) before the \(2/3\) power | **PASS** |
| Functional dissipation witness | R0.74R, Proposition 5.3, supplies the high-frequency divergence-free fields but explicitly does not supply Navier--Stokes trajectories | **PASS** |
| Stopped-work gate | R0.74S Step 2, (S.25)--(S.38), permits every finite shell family satisfying the strict terminal upcrossing inequality and retains the sign only after summation | **PASS** |
| Rayleigh split and old residual | R0.74S Step 7, (S.142)--(S.162), supplies \(e,g,L,H\), the coefficient ledger, the raw defect/high-Rayleigh residual, and the exact-shear audit | **PASS** |
| Smooth exact-family separation | R0.74O, (4.1)--(4.6), (6.1), (6.5)--(6.9), and R0.74P, (0.1)--(0.2), (4.1)--(4.4), give \(\mathfrak C_*^M\asymp T_*\), \((P_*^M)^{2/3}\asymp T_*/K_*\), \(K_*\to\infty\), a target clock \(\gtrsim T_*\), and target \(Q\)-variation \(O(T_*/K_*)\) | **PASS** |

The checked frozen sources have SHA-256 values

- R0.74P:
  a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867;
- R0.74O:
  471158de1db718ac96f38adc729464d8717006f47c8c6bb57834cc4e159bd9bb;
- R0.74R Step 2:
  ac959f30b254001910e5b445264ea7c0d8714afc2f96dcf74505f5e1f794b6b7;
- R0.74S Step 2:
  3ec5f9b894f89e9febb95e5a100836b5b18e455f8366bf99e93b746ac6353da4;
  and
- R0.74S Step 7:
  e835a104f4a6f4d2281bef877dd6bfeb73f1c2396f6bd28203bb0812f7f8e3d3.

## 3. Equation-by-equation audit

| Equation | Independent check | Decision |
|---|---|---|
| (S.163) | \(I_{2R}=(t_0-4R^2,t_0)=(s_R,t_0)\), and \(J_\tau=(s_R,\tau)\) matches the inherited open-terminal convention. | **PASS** |
| (S.164) | All three definitions are nonnegative Borel measures.  The factors are exactly \(R^{-2}\) for kinetic time mass and \(\gamma_k/R\) for total dissipation.  Absolute continuity of \(Q_k\) gives \(d\beta_k=|\dot Q_k|dt\). | **PASS** |
| (S.165) | Translating \(d\boldsymbol\mu=|\nabla u|^2dxdt+d\boldsymbol D\) by \(X_R(t)\) produces \(g_kdt+d\boldsymbol\delta_k\), with no Jacobian or missing shell weight. | **PASS** |
| (S.166) | At good \(\tau\), the first identity is exactly (S.143); the second is the variation formula for an absolutely continuous primitive on \(J_\tau\). | **PASS** |
| (S.167) | The scalar positive part \(x=[\alpha(J)]_+\) and Jordan mass \(X=\alpha^+(J)\) are correctly distinguished. | **PASS** |
| (S.168) | For a finite signed Radon measure, the Hahn formula gives \(\alpha^+(J)=\sup_A\alpha(A)\).  Inner/outer regularity and Urysohn approximation give the equivalent \(C_c(J)\), \(0\le\phi\le1\), formula, including interior atoms. | **PASS** |
| (S.169) | Writing \(a=\nu(J)-\beta(J)-2\lambda\sigma(J)\) gives \(\nu(J)=\beta(J)+2\lambda\sigma(J)+a\le\beta+2\lambda\sigma+[a]_+\), and (S.168) gives \(x\le X\). | **PASS** |
| (S.170) | The priority definitions are pairwise disjoint and exhaustive in \(\mathcal I_D(\tau)\).  Positivity of \(\lambda_k\) makes the kinetic threshold literal. | **PASS** |
| (S.171) | Outside the first branch, \(\beta<T/6\); outside the second, \(2\lambda\sigma\le T/6\); and \(\nu=D\ge T/2\).  Therefore \(\alpha(J)>T/6\), with strictness supplied by the failed \(\beta\)-test. | **PASS** |
| (S.172) | With \(\delta=|J_\tau|/R^2\in(0,4)\), Jensen gives \(R^{-2}\int e^{3/2}\ge\delta^{-1/2}\sigma(J)^{3/2}\).  Since \(\delta^{-1/2}>1/2\) and \(\sigma>T/(12\lambda)\), the displayed strict bound follows. | **PASS** |
| (S.173) | This is exactly the R0.74R nonnegative shell payment \(p_{k,R}^{u,\eta}(J)\) with \(J=J_\tau\). | **PASS** |
| (S.174) | From \(\frac12(T/(12\lambda))^{3/2}<C_1 2^{3k/2}\gamma^{1/2}p\), the \(2/3\) power gives \(T<12(2C_1)^{2/3}\lambda 2^k\gamma^{1/3}p^{2/3}\).  Weakening to \(\le\) is valid. | **PASS** |
| (S.175) | Cubing \(\lambda_k2^k\gamma_k^{1/3}\) gives exactly \(2^{3k}\gamma_k\lambda_k^3\). | **PASS** |
| (S.176) | Finite-shell Hölder with exponents \(3\) and \(3/2\), followed by (R.211), gives \(C_5=C_4C_P^{2/3}\).  Nonnegative monotone convergence closes the shell sum. | **PASS** |
| (S.177) | On \(\mathcal I_\beta\), \(T_k\le6\beta_k(J_\tau)\); restriction decreases total variation, and inherited (3.5) pays the all-shell sum quadratically. | **PASS** |
| (S.178) | Summing the three priority classes gives the displayed selected-residual inequality, with \(T_k\le6x_k\) on \(\mathcal I_x\). | **PASS** |
| (S.179) | The two global sums and \(\mathfrak x_1\le\mathcal X_1\) are correctly defined first as extended nonnegative quantities; (S.192) later proves actual fixed-scale finiteness. | **PASS** |
| (S.180) | Replacing the selected nonnegative subseries first by the global \(x\)-sum and then by the global \(X\)-sum is valid. | **PASS** |
| (S.181) | On \(L_k\), \(g_k-2\lambda_kR^{-2}e_k\le0\); on \(H_k\), its positive part is at most \(g_k\); subtracting \(\beta_k\ge0\) cannot increase the variational supremum.  Thus \(X_k\le m_k+\int_{H_k}g_k\). | **PASS** |
| (S.182) | For the inherited shear, \(F_k=0\), hence \(K_k=Q_k\).  Since \(Q_k(s_R)=0\), \(T_k=Q_k(\tau)\le\int|\dot Q_k|=\beta_k(J_\tau)\); also \(D_k\le K_k\), so \(x_k=0\). | **PASS** |
| (S.183) | This is precisely the inherited fixed-scale suitable-weak topology.  Since \(\overline I_{8R}\Subset(0,T)\), the fixed cylinder used below lies in a compact subcylinder. | **PASS AS HYPOTHESIS** |
| (S.184) | Uniform path convergence makes the moving weights converge uniformly with common compact support.  Local weak-* convergence of \(\boldsymbol\mu_n\) plus uniform local mass bounds handles the varying-test error. | **PASS** |
| (S.185) | Strong \(L^3\) on the fixed finite cylinder implies strong \(L^2\).  The quadratic difference estimate yields \(e_n\to e\) in \(L^1_t\); applying it to the explicit bounded-coefficient density in (2.8) yields \(\dot Q_n\to\dot Q\) in \(L^1_t\). | **PASS** |
| (S.186) | Total-variation convergence of the \(\beta\)- and \(\sigma\)-measures plus vague convergence of \(\nu_n\) gives vague convergence of \(\alpha_n\).  Portmanteau on a relatively compact open interval after removing the common zero-cutoff neighborhood gives the lower bound for \(\nu(J_\tau)\). | **PASS** |
| (S.187) | If \(a\le\liminf a_n\) and \(b_n\to b\), monotonicity and continuity of the positive-part map give \([a-b]_+\le\liminf[a_n-b_n]_+\). | **PASS** |
| (S.188) | For each fixed \(0\le\phi\le1\) in \(C_c(J_\tau)\), \(\int\phi\,d\alpha_n\to\int\phi\,d\alpha\).  Comparing with the supremum defining \(X_n\), taking \(\liminf\), then the supremum over \(\phi\), proves the result. | **PASS** |
| (S.189) | Fatou on each finite shell prefix and monotone convergence give both all-shell lower-semicontinuity inequalities. | **PASS** |
| (S.190) | Smoothness removes \(\boldsymbol D\); therefore \(d\alpha=(g-|\dot Q|-2\lambda R^{-2}e)dt\).  Scalar positive part after integration gives \(x\), while integration of the pointwise positive density gives the Jordan mass \(X\). | **PASS** |
| (S.191) | Substitute the smooth identities (S.190) into the proved lower-semicontinuity statements.  The conclusion is valid only for a supplied smooth sequence satisfying (S.183), exactly as stated. | **PASS / CONDITIONAL** |
| (S.192) | Since \(\alpha_k=\nu_k-\zeta_k\) with \(\zeta_k\ge0\), the lattice/variational identity gives \(\alpha_k^+\le\nu_k\).  Tonelli turns \(\sum_k\nu_k\) into the integral against bounded \(\Theta_R\); the cutoff support lies in a compact subcylinder, so the mass is finite. | **PASS** |
| (S.193) | \(\beta_k(J_\tau)\ge|Q_k(\tau)|\), and \(D_k=Q_k+F_k-E_k\) at good times.  Hence \(\alpha_k(J_\tau)\le F_k-E_k-2\lambda_k\sigma_k\le F_k\), so \(x_k\le[F_k]_+\).  The full scalar sum is bounded by \(\sum_k\operatorname{TV}F_k\le CP_R^M\). | **PASS** |
| (S.194) | The inherited common full-measure good set meets the initial interval where \(\eta_R=\eta_R'=0\).  At such a common stop, \(K_k=Q_k=F_k=0\) for every shell.  Any nonempty finite positive-\(x\) family then satisfies strict (S.25), and its stopped work is \(\sum_G F_k(\tau)\ge\sum_Gx_k>0\).  Supremum over finite \(G\) proves \(\mathfrak x_1\le\mathfrak W_{\rm up}\). | **PASS** |
| (S.195) | Failure of the \(\beta\)-test gives \(|Q_k(\tau)|\le\beta_k(J_\tau)<T_k/6\).  Since \(F_k=T_k-Q_k\ge T_k-|Q_k|>5T_k/6\), one gets \(T_k<(6/5)F_k\). | **PASS** |
| (S.196) | The common zero stop makes \(\sum_G F_k(\tau)\) an admissible positive stopped work for every finite \(G\subset\mathcal I_x\).  Apply (S.195), take increasing finite subsets, and combine with (S.176)--(S.177). | **PASS** |
| (S.197) | \(B_{Q,R}^M\) is finite and quadratically paid by (3.5).  Uniform convergence of the absolutely summable \(Q\)- and \(F\)-series makes \(\sum_kK_k\) continuous and finite; density of the common good set identifies its good-time supremum with the full-time supremum.  The newly named \(\mathfrak C_{{\rm full},R}^M\) uses the same full cutoff interval as (S.37). | **PASS** |
| (S.198) | Every admissible work obeys \(W-\sum_kF_k(\tau)=\sum_{k\in I}(Q_k(\sigma_k)-K_k(\sigma_k))+\sum_{k\notin I}(Q_k(\tau)-K_k(\tau))\le B_Q\), because the two shell sets partition the \(Q\)-ledger and \(K_k\ge0\).  Conversely, common zero stops on the \(K_k>0,F_k>0\) shells capture every positive terminal-flux shell except possible \(K_k=0<F_k=-Q_k\), whose total is at most \(B_Q\).  Thus \(|W_{\rm up}-\mathfrak C_{\rm full}|\le B_Q\).  The analogous positive-clock argument gives \(\mathcal K-B_Q\le W_{\rm up}\le\mathcal K+B_Q\). | **PASS / COEFFICIENT ONE** |
| (S.199) | R0.74O/P gives the inherited plateau flux \(\mathfrak C_R^{M,*}\asymp T_*\), payment \((P_R^{M,*})^{2/3}\asymp T_*/K_*\), and \(K_*\to\infty\).  Since \(\mathfrak C_{\rm full}\ge\mathfrak C_R\) and \(B_Q=O(T_*/K_*)\), (S.198) gives \(W_{\rm up}\gtrsim T_*\), hence the displayed ratio diverges. | **PASS / UNIVERSAL ANTECEDENT REFUTED** |

All thirty-seven tags (S.163)--(S.199) occur once and in order.  No
displayed constant, strict inequality, sign, normalization, or exponent in
the final source requires repair.

## 4. Threshold and coefficient ledger

For \(k\in\mathcal I_x(\tau)\), failure of the first two priority tests gives

\[
 \beta_k(J_\tau)<\frac{T_k}{6},
 \qquad
 2\lambda_k\sigma_k(J_\tau)\le\frac{T_k}{6}.
\]

Together with \(D_k=\nu_k(J_\tau)\ge T_k/2\), this yields

\[
 \alpha_k(J_\tau)>
 \frac{T_k}{2}-\frac{T_k}{6}-\frac{T_k}{6}
 =\frac{T_k}{6}.
\]

For the kinetic branch, \(\delta_\tau=|J_\tau|/R^2<4\), so
\(\delta_\tau^{-1/2}>1/2\).  Combining Jensen with the R0.74R pointwise
spatial estimate gives

\[
 \frac12\left(\frac{T_k}{12\lambda_k}\right)^{3/2}
 <C_1\,2^{3k/2}\gamma_k^{1/2}p_{k,R}^{\tau}.
\]

Taking the \(2/3\) power gives exactly

\[
 T_k<
 12(2C_1)^{2/3}\lambda_k2^k\gamma_k^{1/3}
 (p_{k,R}^{\tau})^{2/3}.
\]

Hölder then cubes the coefficient and produces
\(\mathscr L(\boldsymbol\lambda)
=\sum_k2^{3k}\gamma_k\lambda_k^3\), with no missing \(R\), \(2^k\), or
\(\gamma_k\) factor.

The later \(6/5\) is independent of the generic \(T_k\le6x_k\) bound.
It comes directly from the failed \(\beta\)-test:

\[
 F_k(\tau)=T_k-Q_k(\tau)
 \ge T_k-|Q_k(\tau)|
 >\frac56T_k.
\]

This is the strongest literal coefficient available from that threshold.

## 5. Scalar excess, Jordan envelope, and Step 7 comparison

The two excess tiers have genuinely different roles:

\[
 x_k=[\alpha_k(J_\tau)]_+,
 \qquad
 X_k=\alpha_k^+(J_\tau),
 \qquad
 0\le x_k\le X_k.
\]

The first permits cancellation between disjoint time regions.  The second
retains every positive local contribution and has the compact-test
variational formula needed for weak stability.  The equal-positive/negative
density stress test correctly gives \(x=0<X\).

The Step 7 comparison is also exact.  On the low-Rayleigh set,
\(g-2\lambda R^{-2}e\le0\); on its complement, the positive density is at
most \(g\); and anomalous mass contributes at most \(m_k\).  Hence

\[
 x_k\le X_k\le m_k+\int_{H_k}g_k.
\]

This is a per-shell domination by the raw two-channel Step 7 residual.  It
does not compare the two different priority-selected shell sums.

At a good terminal time the scalar tier has the stronger clock identity

\[
\begin{aligned}
 \alpha_k(J_\tau)
 &=Q_k(\tau)+F_k(\tau)-E_k(\tau)
   -\beta_k(J_\tau)-2\lambda_k\sigma_k(J_\tau)\\
 &\le F_k(\tau),
\end{aligned}
\]

because \(\beta_k(J_\tau)\ge|Q_k(\tau)|\).  Thus the scalar remainder is a
subledger of terminal positive physical flux, while no analogous conclusion
is proved for the Jordan envelope.

## 6. Exact stopped-work bridge

Choose \(\sigma_0\) from the inherited common full-measure good set inside
the common initial zero-cutoff interval.  There

\[
 K_k(\sigma_0)=Q_k(\sigma_0)=F_k(\sigma_0)=0
\]

for every shell.  If \(x_k(\tau)>0\), then \(D_k(\tau)>0\), so
\(K_k(\tau)>0\); hence

\[
 K_k(\tau)-K_k(\sigma_0)=K_k(\tau)>
 \frac14K_k(\tau),
\]

which is exactly the strict admissibility condition (S.25).  For each
finite nonempty \(G\subset\{k:x_k(\tau)>0\}\),

\[
 W_R^M(\tau;G,(\sigma_0)_{k\in G})
 =\sum_{k\in G}F_k(\tau)
 \ge\sum_{k\in G}x_k(\tau)>0.
\]

Taking finite-subset suprema proves

\[
 \mathfrak x_{1,R}^{\boldsymbol\lambda}(\tau)
 \le\mathfrak W_{{\rm up},R}^M
 \le\mathfrak L_{{\rm abs},R}^M
 \le CP_R^M.
\]

Restricting instead to \(\mathcal I_x(\tau)\) and using (S.195) proves

\[
 \sum_{k\in\mathcal I_x(\tau)}K_{k,R}(\tau)
 \le\frac65\mathfrak W_{{\rm up},R}^M.
\]

The passage to countably many shells is valid: apply the inequality to
arbitrary finite subsets, note that every selected \(F_k(\tau)\) is
positive, and use monotone convergence.

This is an exact unification, but not a successful depletion estimate.  The
definition of \(\mathfrak W_{\rm up}\) already admits the same zero-start
competitors for every finite positive-clock family.  Step 8 identifies the
selected dissipation residual with that existing gate and improves its
branch coefficient.  Equations (S.197)--(S.199) then show that the universal
quadratic antecedent for this no-exception gate is false; the viable route
must restore terminal-dependent exceptions.

## 7. Fixed-scale finiteness and weak stability

For \(\alpha_k=\nu_k-\zeta_k\) with \(\zeta_k\ge0\), the variational
formula gives \(\alpha_k^+(B)\le\nu_k(B)\) for every Borel \(B\).  Therefore

\[
\begin{aligned}
 \mathcal X_{1,R}^{\boldsymbol\lambda}(\tau)
 &\le\sum_{k\ge1}\nu_{k,R}(J_\tau)\\
 &=\frac1R\int_{J_\tau\times\mathbb T^3}
   \eta_R(t)\Theta_R(x-X_R(t))\,d\boldsymbol\mu(t,x)<\infty.
\end{aligned}
\]

The \(C^2\)-convergent shell sum \(\Theta_R\) is bounded.  The frozen cutoff
vanishes near \(s_R\), and \(\tau<t_0\), so the integrand is supported in a
compact subcylinder on which the Radon measure \(\boldsymbol\mu\) is finite.
This proves fixed-scale finiteness, not any uniform-in-\(R\), quadratic, or
square-function estimate for \(\mathcal X_1\).

The lower-semicontinuity proof correctly avoids hard-time mass convergence.
Uniform path convergence makes the moving tests in (S.184) converge
uniformly with common compact support.  Strong \(L^1\) convergence of the
explicit \(Q\)-densities, not merely uniform convergence of \(Q_n\), gives
total-variation convergence of \(\beta_n\).  The same argument gives
total-variation convergence of \(\sigma_n\).

For the open interval \(J_\tau\), the common zero-cutoff neighborhood removes
the noncompact left endpoint.  Portmanteau on the remaining relatively
compact open set gives
\(\nu(J_\tau)\le\liminf_n\nu_n(J_\tau)\).  Subtraction of the convergent
\(\beta\)- and \(\sigma\)-masses followed by the positive-part map proves
(S.187).  Convergence against one \(C_c(J_\tau)\) test at a time followed by
the variational supremum proves (S.188).  Fatou and monotone convergence
then prove both global statements (S.189).

## 8. Smooth formula and stress tests

| Test | Verification | Decision |
|---|---|---|
| Smooth density formula | With \(\boldsymbol D=0\), the signed measure has density \(g-|\dot Q|-2\lambda R^{-2}e\); scalar and Jordan positive parts give the two lines of (S.190). | **PASS** |
| Conditional smooth approximation | Apply (S.187)--(S.188) to a supplied smooth sequence and substitute (S.190).  No existence of such a sequence is inferred. | **PASS / CONDITIONAL** |
| Interior atom | \(\nu=T\delta_a\), \(\beta=\sigma=0\) gives \(x=X=T\); the \(C_c\) variational formula detects the atom. | **PASS / MEASURE TEST ONLY** |
| Already paid density | \(d\nu=d\beta=r(t)dt\), \(\sigma=0\) gives \(\alpha=0\), hence \(x=X=0\). | **PASS / ABSTRACT CLOCK TEST** |
| High-frequency functional family | The curl construction has \(\int|\nabla w_n|^2\gtrsim1\), \(\int|w_n|^3=O(n^{-3})\), and \(\int|w_n|^2=O(n^{-2})\); hence \(\nu\gtrsim1\) while \(\sigma,\beta,p_n^{2/3}=O(n^{-2})\), so \(x,X\gtrsim1\). | **PASS / NOT A NAVIER--STOKES TRAJECTORY** |
| Scalar versus Jordan tier | Equal positive and negative density masses give \(x=0<X\), verifying that \(X\) retains locally uncancelled excess. | **PASS** |
| Endpoint escape | \(a_n\uparrow\tau\) gives \(x_n=X_n=1\) but limiting open-interval mass zero, so only lower semicontinuity survives. | **PASS** |
| Uniform primitive convergence | \(Q_n=n^{-1}\sin(nt)\to0\) uniformly while \(\int|\dot Q_n|=\int|\cos(nt)|\not\to0\). | **PASS** |

The high-frequency functional family does not contradict (S.193).  That
formula uses the exact PDE completed balance \(K=E+D=Q+F\), while the
functional witness is explicitly not a Navier--Stokes evolution.

For the inherited exact heat shear, \(F_k=0\), \(K_k=Q_k\), and
\(D_k\le K_k\le\beta_k(J_\tau)\).  Thus \(x_k=0\) exactly.  The note
correctly makes no claim that \(X_k=0\).

## 9. No-exception equivalence and exact-family refutation

Write

\[
 S_K(\tau)=\sum_kK_k(\tau),\qquad
 S_Q(\tau)=\sum_kQ_k(\tau),\qquad
 S_F(\tau)=\sum_kF_k(\tau).
\]

The inherited total-variation ledgers imply uniform absolute convergence of
the \(Q\)- and \(F\)-series, hence uniform convergence and continuity of
\(S_K=S_Q+S_F\).  Since the common good set is dense,

\[
 \mathcal K_R^M=\sup_{s_R<\tau<t_0}S_K(\tau).
\]

For an admissible stopped family,

\[
\begin{aligned}
 W(\tau;I,\boldsymbol\sigma)
 &=\sum_{k\in I}\bigl(K_k(\tau)-K_k(\sigma_k)\bigr)
   -\sum_{k\in I}\bigl(Q_k(\tau)-Q_k(\sigma_k)\bigr)\\
 &\le \mathcal K_R^M+B_{Q,R}^M.
\end{aligned}
\]

Conversely, common zero stops and increasing finite subsets of the positive
terminal clocks give

\[
 \mathfrak W_{{\rm up},R}^M
 \ge \mathcal K_R^M-B_{Q,R}^M.
\]

The comparison with the full terminal flux can be made directly, without a
triangle inequality.  For every admissible finite stopped family,

\[
\begin{aligned}
 W_R^M(\tau;I,\boldsymbol\sigma)-S_F(\tau)
 &=
 \sum_{k\in I}\bigl(Q_k(\sigma_k)-K_k(\sigma_k)\bigr)\\
 &\quad+\sum_{k\notin I}\bigl(Q_k(\tau)-K_k(\tau)\bigr)
 \le B_{Q,R}^M.
\end{aligned}
\]

The two index sets partition the shell ledger, every \(K_k\ge0\), and one
value of \(Q_k\) per shell is bounded by that shell's total variation.
Therefore

\[
 \mathfrak W_{{\rm up},R}^M
 \le\mathfrak C_{{\rm full},R}^M+B_{Q,R}^M.
\]

Conversely, at a good terminal time take common zero stops on finite subsets
of

\[
 A_\tau=\{k:K_k(\tau)>0,\ F_k(\tau)>0\}.
\]

These are strict (S.25) competitors and their stopped work increases to
\(\sum_{A_\tau}F_k(\tau)\).  Positive terminal flux omitted from
\(A_\tau\) can only occur on shells with \(K_k(\tau)=0<F_k(\tau)\); there
\(F_k(\tau)=-Q_k(\tau)\), so its total is at most \(B_Q\).  Shells with
\(F_k\le0\) do not increase the positive full sum.  Hence

\[
 \mathfrak C_{{\rm full},R}^M
 \le\mathfrak W_{{\rm up},R}^M+B_{Q,R}^M.
\]

Uniform convergence of the shell series and density of the common good set
extend this good-time inequality to the full-time supremum.  This proves the
coefficient-one estimate

\[
 \left|\mathfrak W_{{\rm up},R}^M
 -\mathfrak C_{{\rm full},R}^M\right|
 \le B_{Q,R}^M.
\]

The coefficient is sharp at the scalar algebraic level: take one shell with
\(K\equiv0\), \(Q(s_R)=0\), \(Q(\tau)=-B\), and \(F=-Q\).  Then no
nonempty family satisfies strict (S.25), so
\(\mathfrak W_{\rm up}=0\), whereas
\(\mathfrak C_{\rm full}=B=B_Q\).

Introducing the full-cutoff quantity is essential: the inherited
\(\mathfrak C_R^M\) takes its supremum only on the plateau \(I_R\).
The source correctly states only
\(\mathfrak C_R^M\le\mathfrak C_{{\rm full},R}^M\), not equality.

For the inherited R0.74O/P exact family,

\[
 \mathfrak C_{R_j}^{M,*}\asymp T_*,
 \qquad
 (P_{R_j}^{M,*})^{2/3}\asymp\frac{T_*}{K_*},
 \qquad
 K_*\to\infty.
\]

Since the full-cutoff supremum dominates the plateau one and
\(B_{Q,R_j}^M=O(T_*/K_*)\), (S.198) yields

\[
 \mathfrak W_{{\rm up},R_j}^{M,*}
 \ge cT_*-O(T_*/K_*),
\]

and therefore

\[
 \frac{\mathfrak W_{{\rm up},R_j}^{M,*}}
 {(P_{R_j}^{M,*})^{2/3}}\longrightarrow\infty.
\]

The family is a smooth, periodic, mean-zero, unforced, pressure-free
Navier--Stokes family.  It therefore refutes the universal antecedent
\(\mathfrak W_{\rm up}\lesssim(P_R^M)^{2/3}\).  It does not refute the
logical conditional implication (S.38), the algebraic inequality (S.196),
an estimate with terminal exceptions paid by \(Y_{2,R}^{\rm sf}\), or
(Q.1).  On the same exact family \(Y_{2,R}^{\rm sf}\gtrsim T_*\), so the
exception/square-function route is not contradicted.

## 10. Claim boundary

| Claim | Audit status |
|---|---|
| Time measures, Jordan formula, and one-sixth trichotomy | **PROVED** |
| Kinetic and \(Q\)-visible payments | **PROVED FROM FROZEN R0.74P/R INPUTS** |
| Selected residual inequality and global consequences | **PROVED** |
| Global scalar excess \(\mathfrak x_1\) | **FINITE; BOUNDED BY \(\mathfrak W_{\rm up}\le CP_R^M\) AT GOOD TIMES** |
| Global Jordan envelope \(\mathcal X_1\) | **FINITE AND LOWER SEMICONTINUOUS; NO QUADRATIC OR STOPPED-WORK BOUND PROVED** |
| Raw Step 7 comparison | **PROVED SHELLWISE; NOT A COMPARISON OF THE DIFFERENT PRIORITY SUMS** |
| Exact-shear scalar excess | **ZERO; NO CLAIM THAT THE JORDAN ENVELOPE VANISHES** |
| Full dissipation branch | **REDUCED TO QUADRATIC PAID TERMS PLUS \((6/5)\mathfrak W_{\rm up}\)** |
| Fixed-scale lower semicontinuity | **PROVED UNDER (S.183)** |
| Smooth approximation formula | **CONDITIONAL ON A SUPPLIED CONVERGENT SMOOTH NAVIER--STOKES SEQUENCE** |
| Universal no-exception quadratic stopped-work antecedent in (S.37)--(S.38) | **REFUTED BY THE SMOOTH R0.74O/P EXACT FAMILY** |
| Conditional implication (S.38) and algebraic reduction (S.196) | **PROVED AND UNAFFECTED BY THE REFUTATION OF THEIR UNIVERSAL ANTECEDENT** |
| Fixed best-\(N\), terminal-dependent-exception route | **OPEN** |
| Selected-index-set lower semicontinuity | **NOT PROVED / NOT CLAIMED** |
| Cross-scale compactness, (Q.1), regularity, or Millennium conclusion | **OPEN / NOT CLAIMED / NOT CLAY** |

The exact research meaning is now correctly bounded: Step 8 proves that the
defect/high-Rayleigh scalar remainder feeds the same common-terminal
signed-flux gate rather than creating another obstruction, and then proves
that a universal no-exception quadratic estimate for that gate is impossible.
The next viable quantifier is a fixed best-\(N\), terminal-dependent
exception estimate.
