# R0.74S Step 7 — primary audit of the dissipation--Rayleigh gate

## 1. Verdict

**PASS AFTER IN-SOURCE PRECISION REPAIRS.**  Equations
(S.142)--(S.162) are analytically consistent with the frozen R0.74P,
R0.74R, R0.74S Step 2, R0.73Y, R0.74B, and R0.73U inputs.  The
one-eighth/one-eighth/one-quarter partition is exhaustive; the factor \(2\)
in the low-Rayleigh definition, the Jensen constant, the per-shell constant,
and the cubed cross-shell coefficient all have the stated values.  The
finite-subset-to-infinite-shell passages use only nonnegative terms and are
valid.

The audited final source is
`research/r074s_dissipation_rayleigh_gate.md`, SHA-256
`e835a104f4a6f4d2281bef877dd6bfeb73f1c2396f6bd28203bb0812f7f8e3d3`.
During the audit, the source was sharpened in three places: (S.142) now fixes
measurable representatives on the common exceptional null set; the shear
diagnostic states \(A\ne0\) and \(N\in\mathbb N\); and its conclusion is
restricted to the high-Rayleigh **time set** \(H_{k,R}\), rather than the
priority shell class \(\mathcal I_{\rm hi}\).  Separately, the exact-shear
discussion of (R.217) chooses a positive-measure set on which \(\eta_R>0\)
when the endpoint kinetic row is positive.  This removes a possible literal
\(0^3\cdot0^{-2}\) ambiguity.  The final source handles both the
positive-endpoint and zero-endpoint cases explicitly.  No analytic defect
remains.

This is a primary mathematical audit, not an independent proof of the
inherited suitable-weak theory and not a novelty or priority certificate.
The high-Rayleigh and anomalous-defect residuals remain open.  The note does
not prove (Q.1), regularity, or the Millennium problem.  **NOT CLAY.**

## 2. Frozen-source backtracking

| Input used by Step 7 | Direct source check | Audit result |
|---|---|---|
| Total dissipation and anomalous defect | R0.74P, (2.1)--(2.4), gives \(\boldsymbol\mu=\lvert\nabla u\rvert^2\,dx\,dt+\boldsymbol D\) with \(\boldsymbol D\ge0\) | **PASS** |
| Completed shell clock | R0.74P, (2.6)--(2.10), and R0.74R, (R.200)--(R.201), give \(K=E+D=Q+F\), \(K(s_R)=0\), and \(K\ge0\) | **PASS** |
| Shell-dependent cubic payment | R0.74R, (R.208)--(R.211), permits a different measurable time set for each shell and bounds their nonnegative payment sum | **PASS** |
| Padded-shell spatial estimate | R0.74R, (R.214), has exactly the \(2^{3k/2}\gamma_k^{1/2}\) coefficient used in (S.152) | **PASS** |
| Dissipation terminal branch | R0.74S Step 2, (S.23), is \(D_{k,R}(\tau)\ge K_{k,R}(\tau)/2\) | **PASS** |
| Conditional extraction interface | R0.74R, (R.216)--(R.217), permits nonnegative \(q_k\), nonnegative \(\Lambda_k\), and shell-dependent positive-measure \(J_k\) | **PASS** |
| Smooth shear diagnostic | R0.73Y supplies the exact nontrivial periodic shear class; R0.74B, Section 6, supplies the same-window high-frequency use and its limited scope | **PASS** |
| Instantaneous sign warning | R0.73U compares \(u\) and \(-u\) at one initial time and explicitly denies trajectory symmetry or a universal one-sided no-go | **PASS** |

The torus integral in (S.142) and the unfolded integral in (R.208) agree by
the inherited periodization/unfolding identity.  Translation by the
Version-M path also preserves \(|\nabla u|^2dx\), so the absolutely continuous
part of the measure clock in (S.143) is exactly the time integral of
\(g_{k,R}\).

## 3. Equation-by-equation audit

| Equation | Check | Decision |
|---|---|---|
| (S.142) | The kinetic row agrees almost everywhere with \(E_{k,R}\); the viscous row has the coefficient \(\gamma_k\eta_R/R\).  Both rows are measurable and nonnegative. | **PASS** |
| (S.143) | Substituting \(\boldsymbol\mu=\lvert\nabla u\rvert^2\,dx\,dt+\boldsymbol D\) into the R0.74P clock gives the displayed viscous/defect split, with both terms nonnegative. | **PASS** |
| (S.144) | After choosing measurable representatives for \(e\) and \(g\) and setting them arbitrarily on their common exceptional null set, \(L_{k,R}\) and \(H_{k,R}\) are measurable complements in \((s_R,\tau)\). | **PASS** |
| (S.145) | For \(\eta_R>0\) and positive cutoff-weighted spatial energy, \(g/e=2\int\Psi\lvert\nabla v\rvert^2/\int\Psi\lvert v\rvert^2\).  Hence \(g\le2\lambda_kR^{-2}e\) is exactly \(\rho\le\lambda_k\). | **PASS** |
| (S.146) | It is the defining inequality multiplied by \(1_L\).  If \(\eta_R=0\), both rows vanish.  If \(\int\Psi\lvert v\rvert^2=0\), Sobolev locality gives \(\nabla v=0\) almost everywhere on \(\{\Psi>0\}\), hence \(e=g=0\).  No quotient convention is used. | **PASS** |
| (S.147) | The priority definition makes the three shell sets pairwise disjoint and exhaustive in \(\mathcal I_D(\tau)\). | **PASS** |
| (S.148) | On the residual class, \(D\ge T/2\), \(m<T/8\), and \(\int_Hg<T/8\); therefore \(\int_Lg=D-m-\int_Hg>T/4\). | **PASS** |
| (S.149) | Integrating (S.146) and combining with (S.148) gives \(T/4<(2\lambda_k/R^2)\int_Le\), hence the factor \(1/(8\lambda_k)\). | **PASS** |
| (S.150) | Hölder/Jensen gives \(R^{-2}\int_Le^{3/2}\ge\delta^{-1/2}(R^{-2}\int_Le)^{3/2}\).  Since \(0<\delta=\lvert L\rvert/R^2\le4\), \(\delta^{-1/2}\ge1/2\). | **PASS** |
| (S.151) | This is exactly the R0.74R payment \(p_{k,R}^{u,\eta}(J)\) with \(J=L_{k,R}\). | **PASS** |
| (S.152) | Integrating (R.214) on \(L_{k,R}\) and dividing by \(R^2\) cancels the pointwise \(R^2\) factor and leaves \(C_1 2^{3k/2}\gamma_k^{1/2}p_{k,R}^{\rm lo}\), with no missing \(R\) or \(\gamma_k\). | **PASS** |
| (S.153) | From \(\frac12(T/(8\lambda))^{3/2}<C_1 2^{3k/2}\gamma^{1/2}p\), raising to \(2/3\) gives \(T<8(2C_1)^{2/3}\lambda\,2^k\gamma^{1/3}p^{2/3}\).  Replacing strict by weak is valid. | **PASS** |
| (S.154) | Cubing the coefficient \(\lambda_k2^k\gamma_k^{1/3}\) gives exactly \(2^{3k}\gamma_k\lambda_k^3\). | **PASS** |
| (S.155) | Hölder with exponents \(3\) and \(3/2\) on every finite shell subset gives the first line.  (R.211) gives \(\sum p_k^{\rm lo}\le C_P P_R^M\), so \(C_3=C_2C_P^{2/3}\).  Monotone convergence closes the countable sum. | **PASS** |
| (S.156) | \(\gamma_{k+1}/\gamma_k=\exp[-3\cdot4^{k-1}/32]\); multiplication by \(2^3\) gives the stated ratio, which tends to zero. | **PASS** |
| (S.157) | For \(\lambda_k=\gamma_k^{-\alpha}\), the ledger weight is \(2^{3k}\gamma_k^{1-3\alpha}\), summable exactly for the stated subcritical range \(0\le\alpha<1/3\). | **PASS** |
| (S.158) | Cubing \(2^{-(1+\varepsilon)k}\gamma_k^{-1/3}\) cancels \(\gamma_k\) and leaves \(2^{-3\varepsilon k}\); summing from \(k=1\) gives \(2^{-3\varepsilon}/(1-2^{-3\varepsilon})\). | **PASS** |
| (S.159) | At the critical profile each ledger summand equals one, so the series diverges.  This is a sequence-space boundary only, as stated. | **PASS** |
| (S.160) | Split the left side over the priority partition.  Use (S.155) on \(\mathcal I_{\rm lo}\), \(T_k\le8m_k\) on \(\mathcal I_{\rm def}\), and \(T_k\le8\int_Hg_k\) on \(\mathcal I_{\rm hi}\).  Finite subsets followed by monotone convergence prove the displayed residual inequality. | **PASS** |
| (S.161) | Under \(\#\mathcal B_\tau\le N_D\), \(K_k(\tau)\le v_{k,R}\) and Cauchy--Schwarz give \(\sum_{\mathcal B_\tau}K_k\le\sqrt{N_D}(\sum_kv_k^2)^{1/2}\).  No cardinality theorem is inferred. | **PASS** |
| (S.162) | For the nontrivial shear, \(\lvert v\rvert^2=A_t^2\sin^2(Nx_2)\) and \(\lvert\nabla v\rvert^2=A_t^2N^2\cos^2(Nx_2)\).  The factors \(A_t^2\) cancel.  Writing the squares with \(\cos(2Nx_2)\) and applying Riemann--Lebesgue gives the displayed ratio and limit. | **PASS** |

All twenty-one tags (S.142)--(S.162) occur once in the R0.74S source
sequence and are consecutive after Step 6.

## 4. Measurability, null rows, and infinite sums

The suitable-weak integrability ledger gives measurable representatives of
the two nonnegative time rows.  Extending those representatives by zero on
the exceptional set of times where a slice was not initially selected does
not alter any integral.  This makes the set definitions in (S.144) literal.

There are two distinct zero cases.

1. If \(\eta_R(t)=0\), then \(e_{k,R}(t)=g_{k,R}(t)=0\), so \(t\in L_{k,R}\)
   directly.
2. If \(\eta_R(t)>0\) but the cutoff-weighted spatial energy is zero, then
   \(v_R(t)=0\) almost everywhere on the open positivity set of
   \(\Psi_k^R\).  Its weak gradient vanishes there; multiplication by
   \(\Psi_k^R\) then gives \(g_{k,R}(t)=0\).  Again \(t\in L_{k,R}\), with no
   \(0/0\) ratio.

The all-shell estimates are first proved on arbitrary finite subsets.  The
coefficient ledger, payments, clocks, defect masses, and high-Rayleigh
dissipation integrals are nonnegative, so increasing finite subsets and
monotone convergence justify (S.155) and (S.160), even as extended-real
statements before the right side is known finite.  When
\(\mathscr L<\infty\), (R.211) makes the low-Rayleigh term finite.  No
unproved exchange of signed infinite series occurs.

## 5. Exact-shear and conditional-interface audit

Choose the common zero-phase anchor \(x_{0,2}=0\).  The mollified shear is
parallel to \(e_1\) and vanishes at the anchor, so uniqueness of the smooth
path ODE gives a stationary Version-M centre in the transverse coordinate.
The moving shear therefore retains the displayed sine/cosine form.  For a
nonzero nonnegative cutoff, \(M_k^R>0\), and

\[
 \int\Psi\cos^2(Nx_2)=\frac12(M_k^R+c_{k,N}^R),
 \qquad
 \int\Psi\sin^2(Nx_2)=\frac12(M_k^R-c_{k,N}^R).
\]

Riemann--Lebesgue gives \(c_{k,N}^R\to0\), so the denominator is positive
and \(\rho_{k,R}^{(N)}\sim (NR)^2\).  This proves high-Rayleigh membership
for every fixed \(k,R,\lambda_k\) and all sufficiently large integer \(N\).
It does not turn the ratio into a Fourier-support theorem.

The physical-work integrand is parallel to \(e_1\), while its scalar
coefficient is independent of \(y_1\).  Periodic integration of
\(\partial_1\Psi_k^R\) therefore gives \(F_{k,R}=0\).  Consequently
\(K_{k,R}=Q_{k,R}\), termwise \(D_{k,R}\le K_{k,R}\), and absolute
convergence from the \(Q\)-variation ledger gives

\[
 \sum_kD_{k,R}(\tau)
 \le\sum_kK_{k,R}(\tau)
 =\sum_kQ_{k,R}(\tau)
 \le\sum_k\operatorname{TV}Q_{k,R}
 \le C_QA_R.
\]

For the conditional R0.74R interface, take
\(S_\tau=\varnothing\), \(q_{k,R,\tau}=\operatorname{TV}Q_{k,R}\), and
\(\Lambda_{k,R,\tau}=0\).  Then (R.216) follows shellwise from
\(|Q_k(\tau)|\le\operatorname{TV}Q_k\) and after summation from the inherited
quadratic \(Q\)-ledger.  If the endpoint kinetic row is positive, the final
source chooses \(J_{k,\tau}\) where \(\eta_R>0\), making
\(0<\Theta_{k,R}^{\eta}<\infty\); if it vanishes, the inherited convention
sets \(\Theta_{k,R}^{\eta}=+\infty\).  Thus every coefficient in (R.217) is
literally zero.  This proves only that this smooth shear subclass is already
zero-exception paid; it is not a counterexample to (S.155) and does not
close the general high-Rayleigh branch.

## 6. Claim and source boundary

| Claim | Audit status |
|---|---|
| Exact viscous/defect decomposition | **PROVED / INHERITED MEASURE IDENTITY** |
| Measurable low/high-Rayleigh time split | **PROVED** |
| Low-Rayleigh kinetic-mass lower bound and Jensen conversion | **PROVED** |
| Per-shell and simultaneous all-shell low-Rayleigh payment | **PROVED** |
| Residual defect/high-Rayleigh ledger | **PROVED AS AN INEQUALITY; RESIDUALS NOT BOUNDED** |
| Finite-exception consequence | **PROVED CONDITIONAL IMPLICATION ONLY** |
| Exact-shear high-Rayleigh time-set diagnostic | **PROVED FOR THE INHERITED SMOOTH NONTRIVIAL SHEAR; NO PRIORITY-SHELL CLAIM** |
| Uniform finite-exception theorem for \(\mathcal I_{\rm def}\cup\mathcal I_{\rm hi}\) | **OPEN / NOT CLAIMED** |
| Arbitrary-clock extraction, stopped-work depletion, or (Q.1) | **OPEN / NOT CLAIMED** |
| Regularity or Millennium conclusion | **OPEN / NOT CLAIMED / NOT CLAY** |

The source ledger does not transfer a literature theorem across incompatible
hypotheses.  The exact shear is explicitly reused rather than claimed as
new, the R0.73U sign pair is kept only as an instantaneous route sentinel,
and the Step 7 theorem is confined to the newly proved low-Rayleigh branch.
The final claim boundary is therefore accurate.
