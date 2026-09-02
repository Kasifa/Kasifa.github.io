# R0.74S Step 11 — primary audit of shared budgets and the terminal trace

## 1. Verdict and locked source

**PASS ON THE LOCKED SOURCE, SUBJECT ONLY TO THE EXPLICITLY OPEN PDE
HYPOTHESES.**  The audited source is

research/r074s_shared_budget_terminal_trace_obstruction.md

with SHA-256

fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693.

All twenty-five statements (S.248)--(S.272) have been backtracked to the
frozen R0.74P/Q/R and R0.74S Step 8/10 inputs.  The shared-budget identity,
short-branch inverse-duration estimate, nested-tent inequality, positive-
depth corollary, and selected-excess equivalence pass.  The four families of
finite stress tests also pass their stated scalar or clock scopes.

This audit does not promote the terminal anti-concentration hypothesis
(S.261), selected-excess packing (S.269), either branch theorem in (S.272),
Step 10 (S.243), Q.12, Q.1, or regularity.  The literature search is bounded
and not an originality opinion.  **NOT CLAY.**

## 2. Frozen-source backtracking

| Input | Use in Step 11 | Audit result |
|---|---|---|
| R0.74P | Continuous nonnegative completed clocks, absolute variation, \(K_k(\tau)\le v_k\), \((v_k)\in\ell^1\), and \(Y_2^{\rm sf}\) | **PASS / INHERITED** |
| R0.74Q | Best-\(N\) terminal reduction, Q.12, Q.1 implication, and multi-packet program | **PASS / PDE TAIL OPEN** |
| R0.74R Step 2 | Shell-dependent cubic sets (R.211) and spatial Hölder row (R.214) | **PASS / INHERITED** |
| R0.74R persistent-lobe audit | Positive second-shell exponent \(8831/1905120\) | **PASS / DESIGN-SPECIFIC OBSTRUCTION** |
| R0.74S Step 8 | Scalar/Jordan excess, ancestry, linear stopped-work ledger, and threshold conventions | **PASS / NO-EXCEPTION GATE REFUTED** |
| R0.74S Step 10 | Six-class paid/residual partition, \(T/6<r<T/2\), one paid ledger, and residual reduction | **PASS / FIXED-\(N\) PDE GATE OPEN** |

The fixed profile \(\boldsymbol\lambda\) may enter constants but does not
depend on the solution, scale, or terminal time.

## 3. Equation-by-equation audit

| Equation | Direct check | Decision |
|---|---|---|
| (S.248) | The Step 10 masks \(\mathcal R_{\rm sh}\) and \(\mathcal R_x\) are disjoint, and the combined residual is zero off their union. | **PASS** |
| (S.249) | A joint deletion set splits across the two disjoint supports; the converse takes the union.  Unused budget is harmless because \(\mathcal S_n\) decreases in \(n\). | **PASS / EXACT** |
| (S.250) | Pointwise infimal convolution followed by \(\sup_\tau\min_n\le\min_n\sup_\tau\).  No exchange of supremum and minimum is claimed. | **PASS** |
| (S.251) | The exception counts add.  Step 10 contributes \(6C_Q+C_5\mathscr L^{1/3}\) to the clock tail and one additional \(C_Q\) to the plateau flux estimate. | **PASS / CONSTANTS 6 AND 7** |
| (S.252) | One exception deletes either of two disjoint entries, not both; two exceptions delete both. | **PASS / SHARP BUDGET TEST** |
| (S.253) | Integrating \(e>T/6\) on a normalized duration \(d\), applying (R.214), and using \(r<T/2\) gives the coefficient \(3C_1^{2/3}(2^{3k}\gamma_kd^{-2})^{1/3}\). | **PASS** |
| (S.254) | Finite-shell Hölder and \(\sum p_k\le C_PP_R^M\) give \(C_P^{2/3}A_R\); the same set is used before the best-\(N\) infimum. | **PASS / SUFFICIENT INTERFACE** |
| (S.255) | \(w h^{-2}=a\lambda^3(d\lambda^{3/2})^{-2}=ad^{-2}\).  On one dyadic layer, \(4^j<h^{-2}\le4^{j+1}\); all sums are restricted to \(\mathcal H_\tau\). | **PASS** |
| (S.256) | \(h^{-2}=1+2\int_h^1s^{-3}\,ds\); Tonelli is valid for nonnegative terms, including the value \(+\infty\). | **PASS / EXACT LAYER CAKE** |
| (S.257) | The frozen weights are eventually decreasing at ratio below \(1/2\); with \(h_k=\sqrt{w_k}\), the critical distribution estimate holds but each inverse moment equals one. | **PASS / ENDPOINT FAILURE** |
| (S.258) | At backward depth \(s\), exactly the intervals with \(d_k>s\) are active.  Weighted Hölder and (R.214) give the displayed tent integrand; \(ds=dt/R^2\). | **PASS** |
| (S.259) | For \(0<s<\delta\), the \(d_k>\delta\) residual is below \(M_I(s)\) and \(V_I(s)\le\mathscr A_0\).  Integrate over length \(\delta\) and take the power \(2/3\). | **PASS** |
| (S.260) | The piecewise-linear clock starts at zero, reaches \(2T/3=2\) exactly at \(1-d_k\), remains above it afterward, and ends at \(T=3\).  The intervals are strictly nested and the abstract cubic density saturates the spatial row. | **PASS / CLOCK WITNESS ONLY** |
| (S.261) | Splitting the residual into \(d\le\delta_*\) and \(d>\delta_*\), then using (S.259), gives the stated constant after moving \(\theta_*M\) to the left. | **PASS AS CONDITIONAL IMPLICATION / HYPOTHESIS OPEN** |
| (S.262) | On \(\mathcal I_x\), \(x>T/6\), \(x\le T-\beta\), \(|q|\le\beta<T/6\), and \(r=T/3-q\).  Hence \(r<3x\) and \(x<5r\). | **PASS / SHARP SCALAR CONSTANTS** |
| (S.263) | Apply the coordinate inequalities with one common deletion set, then optimize. | **PASS / EXACT BEST-\(N\) EQUIVALENCE UP TO CONSTANTS** |
| (S.264) | Step 8 gives \(x^{\rm sel}\le b\); \(b_k\le D_k\le K_k\le v_k\), and the scalar excess has the inherited linear flux bound. | **PASS / LINEAR ONLY** |
| (S.265) | Delete the fixed prefix for which the \(\ell^1\) tail of \(v\) is below \(2\varepsilon\).  The prefix is uniform in \(\tau\) but depends on the solution, scale, and tolerance. | **PASS / NONUNIFORM** |
| (S.266) | The rational defect clock has \(K(1)=2/3\), \(K(2)=1\), \(\int h=959/12000\), \(x=3/5-2\int h=2641/6000\), and no last-exit defect increment. | **PASS / SCALAR WITNESS** |
| (S.267) | \(\int e_0=1/500\), \(\int g=3/5\), so \(\sigma=983/12000\), \(x=2617/6000\), while the high-Rayleigh support precedes the last exit. | **PASS / SCALAR WITNESS** |
| (S.268) | Repeating the monotone pure-defect row gives \(v_k=1\), \(Z=\sqrt M\), a linear ledger \(P_M\asymp M\), and residual tail \((M-N)_+/3\). | **PASS / ABSTRACT, NOT PDE** |
| (S.269) | By (S.263), the selected-excess theorem is equivalent, up to \(1/5\) and \(3\), to the \(\mathcal R_x\) branch gate. | **PASS AS TARGET / OPEN** |
| (S.270) | A paid target would contradict the \(O(A_R)\) total paid sum.  With \(N+1\) residual targets, any \(N\)-deletion leaves one and \(r>T/6\). | **PASS AS CONDITIONAL FALSIFICATION TEST** |
| (S.271) | The formula is the inherited nonnegative exterior cubic lower bound with \(A_R^{(N)}=(P_R^{M,(N)})^{2/3}\).  It overwhelms only the presently certified \(NT\) clock scale and is not used as a clock upper bound. | **PASS / DESIGN-SPECIFIC** |
| (S.272) | Combine the two fixed branch budgets using (S.249)--(S.251).  The solution and scale quantifiers are explicit and \(N_0=N_{\rm sh}+N_x\) is fixed. | **PASS AS CONDITIONAL IMPLICATION / BRANCH ESTIMATES OPEN** |

The tags are consecutive and unique.  Display-math delimiters balance, no
moving selector is claimed measurable, and every finite/abstract witness is
kept outside the NSE claim boundary.

## 4. Shared-budget quantifier audit

For finite vectors the identity can also be read as

\[
 \|a+b\|_{\ell^1}
 -\sum_{\text{largest }N\text{ coordinates of }a+b}(a_k+b_k)
 =
 \min_{n+m=N}\bigl[\mathcal S_n(a)+\mathcal S_m(b)\bigr].
\]

This verifies three separate quantifier points.

1. Branch supports, not shell indices, determine how a joint deletion set
   divides its budget.
2. The split \(n=n(\tau)\) may change with the terminal time.
3. A proof with budgets \(N_{\rm sh}\) and \(N_x\) closes the original
   existence theorem with the finite sum \(N_0=N_{\rm sh}+N_x\).  It need
   not preserve either branch count verbatim.

The finite counterexample in (S.252) rejects only the false same-\(N\)
recombination.  It does not reject fixed-\(2N\) recombination.

## 5. Short-branch constant audit

On \(\mathcal R_{\rm sh}\),

\[
 d_k(T_k/6)^{3/2}
 <C_1a_k^{1/2}p_k.
\]

Thus

\[
 T_k<6C_1^{2/3}a_k^{1/3}d_k^{-2/3}p_k^{2/3},
 \qquad
 r_k<T_k/2
 <3C_1^{2/3}(a_kd_k^{-2})^{1/3}p_k^{2/3}.
\]

For a finite shell set \(I\),

\[
\begin{aligned}
 \sum_{k\in I}r_k
 &<3C_1^{2/3}
 \left(\sum_{k\in I}a_kd_k^{-2}\right)^{1/3}
 \left(\sum_{k\in I}p_k\right)^{2/3}\\
 &\le3C_1^{2/3}C_P^{2/3}
 \left(\sum_{k\in I}a_kd_k^{-2}\right)^{1/3}A_R.
\end{aligned}
\]

This proves (S.253)--(S.254).  The inverse duration cannot be hidden in
\(\lambda\), because \(w_kh_k^{-2}=a_kd_k^{-2}\) identically.

For the tent estimate, weighted Hölder on the active set gives

\[
 {(\sum r_k)^{3/2}\over(\sum a_k)^{1/2}}
 <3^{3/2}\sum {e_k^{3/2}\over a_k^{1/2}}.
\]

The time integral of the \(k\)-th right-hand term is bounded by \(C_1p_k\).
This verifies the absence of an extra factor of \(R^2\), and proves
(S.258).  The estimate is integrated in backward depth and cannot be
evaluated at depth zero without a new trace theorem.

## 6. Scalar-excess constant audit

Put \(q=\Delta Q\).  On \(\mathcal I_x\),

\[
 x>T/6,\qquad x\le T-\beta,\qquad |q|\le\beta<T/6,
 \qquad r=T/3-q.
\]

The upper estimate is immediate:

\[
 r<T/2<3x.
\]

For the lower estimate,

\[
 5r-x\ge2T/3-5q+\beta.
\]

If \(q\ge0\), this is at least \(2T/3-4q>0\).  If \(q<0\), it is at least
\(2T/3-6q>0\).  Therefore \(x/5<r\).  The limiting tuples in the source
show that neither constant can be improved using only these scalar
constraints.

## 7. Rational localization witnesses

For the common function \(h\),

\[
\begin{aligned}
 \int_{9/10}^{1}h&=1/300,\\
 \int_{1}^{39/20}h&=15561/240000,\\
 \int_{39/20}^{2}h&=2819/240000.
\end{aligned}
\]

Their sum is \(959/12000\).  The pure-defect row therefore has

\[
 x=3/5-2(959/12000)=2641/6000.
\]

For the high-Rayleigh bump,

\[
 \int_{1/10}^{3/5}{12\over125}(t-1/10)(3/5-t)\,dt=1/500.
\]

Adding this to the kinetic integral gives \(983/12000\), and

\[
 x=3/5-2(983/12000)=2617/6000.
\]

Both rows reach the last \(2/3\) level at \(t=1\), and every part of the
selected ancestor lies before that time.  They refute last-exit
localization at the scalar-clock level only.

## 8. Literature and exact-family boundary

The source accurately distinguishes primary results about singular-set
dimension, anomalous-dissipation support under extra integrability,
Type-I singular-point counts, and ensemble/time-averaged flux locality from
the desired prescribed-centre terminal annular tail.  The inference is only
that the inspected theorems do not directly imply (S.261) or (S.269).

The exact-family logic is also one-sided in the correct direction.  The
single-packet work certifies one large target and therefore kills only the
zero-exception claim.  The multi-packet work certifies multiple terminal
lobes but also a prohibitive nonnegative cubic lower bound at its intended
scale.  Step 11 does not infer an upper bound on uncomputed clocks and does
not claim that every alternative exact-family architecture fails.

## 9. Final claim ledger

**PROVED:** shared-budget algebra; inverse-duration and tent estimates;
positive-depth control; selected-excess equivalence; linear/fixed-solution
tail bounds; finite scalar and clock stress-test arithmetic; all displayed
conditional implications.

**INHERITED:** suitable-weak clock construction, absolute ledgers, spatial
Hölder, the Step 8 excess/ancestry theorem, Step 10 paid deletion, and the
specific exact-family payment obstructions.

**OPEN:** (S.261), (S.269), both estimates in (S.272), a universal fixed
count, Step 10 (S.243), Q.12, Q.1, scale contraction, prescribed-centre
packing, and regularity.

**NOT CLAIMED:** PDE realizability of the stress tests, selector
measurability, interchange of terminal supremum and budget minimum,
exhaustiveness of the literature search, novelty, or a Clay solution.

**NOT CLAY.**
