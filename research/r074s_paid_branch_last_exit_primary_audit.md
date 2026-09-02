# R0.74S Step 10 — primary audit of the paid-branch last-exit residual

## 1. Verdict and locked source

**UNCONDITIONAL PASS ON THE LOCKED SOURCE.**  The audited source is

`research/r074s_paid_branch_last_exit_residual.md`

with SHA-256

`9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c`.

All twenty-five numbered statements (S.223)--(S.247) pass.  In particular:

- the positive terminal shells form one exact disjoint union of four paid
  classes and two residual classes;
- the Step 7 low-Rayleigh class is already contained in the Step 8
  \(\mathcal I_\beta\cup\mathcal I_\sigma\) classes, so it creates no
  additional residual or payment;
- the two disjoint \(Q\)-paid classes use one total-variation ledger with
  coefficient \(6\), not two separate ledgers;
- long non-\(D\) last-exit intervals carry an a.e. kinetic lower bound, and
  their cubic payment combines with the Step 8 \(\sigma\)-class before
  Hölder, producing one coefficient \(C_5\);
- the remaining stopped-flux vector satisfies
  \(T_k/6<r_k<T_k/2\) on its support;
- the fixed-good-terminal estimate passes to both terminal domains using
  continuity of the terminal \(K\)-vector, without asserting continuity or
  measurability of the moving last-exit mask;
- the residual best-\(N\) gate and the inherited clock best-\(N\) gate are
  equivalent at the quadratic scale for every fixed admissible profile;
- the plateau corollary pays exactly \(7B_{Q,R}^M\), while the full-domain
  residual gate is the domain-correct route to R0.74Q (Q.12); and
- the fixed universal residual packing estimate remains explicitly open.

This is a primary analytic audit.  It verifies the locked Step 10 note
against its frozen inputs.  It is not an independent reconstruction of all
inherited suitable-weak theory, a novelty or priority certificate, or a
regularity theorem.  **NOT CLAY.**

## 2. Frozen-source backtracking

| Input used by Step 10 | Direct source check | Audit result |
|---|---|---|
| Canonical clocks and absolute ledgers | R0.74P, (2.7)--(3.7), supplies continuous \(K=Q+F\), zero starts, \(K\ge0\), \(K_k(\tau)\le v_k\), \(B_Q\le C_QA_R\), \(\sum_k\operatorname{TV}F_k\le C_FP_R^M\), and \(Z_R=(\sum_kv_k^2)^{1/2}\) | **PASS** |
| Fixed-\(N\) terminal reduction | R0.74Q, (Q.7)--(Q.12), supplies the terminal-dependent exceptional set, the \(\sqrt N Z_R\) payment, and the full-terminal tail gate | **PASS / PDE TAIL BOUND OPEN** |
| Shell-dependent cubic payment | R0.74R, (R.209)--(R.214), permits a different measurable time set for each shell and supplies the padded-shell spatial Hölder estimate | **PASS** |
| Strict stopped-work boundary | R0.74S Step 2, (S.25)--(S.38), restricts an actual stopped local-energy argument to finite shell families and good stops | **PASS / NOT REUSED AS AN INFINITE TEST** |
| Low-Rayleigh genealogy | R0.74S Step 7, (S.142)--(S.155), supplies \(K=E+D\) at good times, monotonicity of \(D\), and \(\sigma(L)>T/(8\lambda)\) on \(\mathcal I_{\rm lo}\) | **PASS** |
| Full-history \(D\)-branch trichotomy | R0.74S Step 8, (S.163)--(S.176), supplies the priority classes \(\mathcal I_\beta,\mathcal I_\sigma,\mathcal I_x\) and the per-shell coefficient \(C_4\lambda_k2^k\gamma_k^{1/3}\) | **PASS** |
| Domain-safe last exits | R0.74S Step 9, (S.200)--(S.222), supplies the \(2/3\)-last-exit identity, absolute convergence, terminal-domain separation, and \(\ell^1\)-continuity of the terminal clock vector | **PASS / LAST-EXIT SELECTOR CONTINUITY NOT CLAIMED** |

The checked hashes are:

- locked Step 10 source:
  `9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c`;
- R0.74P:
  `a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867`;
- R0.74Q:
  `42efa94f5310d8f7ce3cea1896ee1e0a8ddd9bddf5d588f9bb853c8696a1a962`;
- R0.74R Step 2:
  `ac959f30b254001910e5b445264ea7c0d8714afc2f96dcf74505f5e1f794b6b7`;
- R0.74S Step 2:
  `3ec5f9b894f89e9febb95e5a100836b5b18e455f8366bf99e93b746ac6353da4`;
- R0.74S Step 7:
  `e835a104f4a6f4d2281bef877dd6bfeb73f1c2396f6bd28203bb0812f7f8e3d3`;
- R0.74S Step 8:
  `0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab`;
  and
- R0.74S Step 9:
  `85003b3fdfdf28618a82a57d241e86c086704ea3ed3a9b192de223f3b8c3a4dd`.

The profile \(\boldsymbol\lambda\) is chosen once and for all,
independently of \(R\), the terminal time, and the solution.  Its finite
ledger \(\mathscr L(\boldsymbol\lambda)\) may enter constants.  Allowing the
profile to vary with a solution would change the uniform quantifiers and is
not part of the locked statement.

## 3. Exact partition audit

Fix a local-energy good terminal time and put
\(\mathcal I_+(\tau)=\{k:T_k>0\}\).  The inherited Step 8 priority rule is

\[
 \mathcal I_D
 =\mathcal I_\beta\mathbin{\dot\cup}
  \mathcal I_\sigma\mathbin{\dot\cup}
  \mathcal I_x.
\]

Its complement in \(\mathcal I_+\) is \(\mathcal I_{\neg D}\).  On that
complement the duration tests partition the indices into
\(\mathcal I_{\rm long}\) and \(\mathcal I_{\rm short}\).  Finally, the
short class is partitioned by the exhaustive strict/non-strict pair

\[
 |\Delta Q_k|\ge T_k/6,
 \qquad
 |\Delta Q_k|<T_k/6.
\]

Therefore

\[
\begin{aligned}
 \mathcal I_+
 ={}&\mathcal I_\beta\mathbin{\dot\cup}\mathcal I_\sigma
  \mathbin{\dot\cup}\mathcal I_x
  \mathbin{\dot\cup}
  (\mathcal I_{\neg D}\cap\mathcal I_{\rm long})\\
 &\mathbin{\dot\cup}
  (\mathcal I_{\neg D}\cap\mathcal I_{\rm short}
       \cap\mathcal I_{Q+})
  \mathbin{\dot\cup}
  (\mathcal I_{\neg D}\cap\mathcal I_{\rm short}
       \cap\mathcal I_{Q-}).
\end{aligned}
\]

This is exactly (S.225).  Equality cases are assigned consistently:

- \(D(\tau)=T/2\) belongs to \(\mathcal I_D\);
- \(d=\lambda^{-3/2}\) belongs to the long class;
- \(|\Delta Q|=T/6\) belongs to the paid \(Q\)-large class;
- \(\beta(J_\tau)=T/6\) belongs to \(\mathcal I_\beta\); and
- after failure of the \(\beta\)-test,
  \(\sigma(J_\tau)=T/(12\lambda)\) fails the strict \(\sigma\)-test and
  belongs to \(\mathcal I_x\).

For the Step 7 compatibility, if \(k\in\mathcal I_{\rm lo}\), then

\[
 \sigma_k(J_\tau)\ge\sigma_k(L_{k,R})
 >{T_k\over8\lambda_k}>{T_k\over12\lambda_k}.
\]

Thus a shell outside \(\mathcal I_\beta\) is automatically in
\(\mathcal I_\sigma\).  Hence
\(\mathcal I_{\rm lo}\setminus
(\mathcal I_\beta\cup\mathcal I_\sigma)=\varnothing\), and the surviving
\(\mathcal I_x\) class lies in the union of the Step 7 anomalous-defect and
high-Rayleigh ancestors.  This is an ancestry statement, not a payment of
either surviving mechanism.

## 4. Equation-by-equation audit

| Equation | Primary check | Decision |
|---|---|---|
| (S.223) | Continuity, the zero start, and \(T_k>0\) give an interior last \(2T_k/3\) level.  Since \(\tau-s_R<4R^2\), \(0<d_k<4\).  Maximality gives \(K(t)>2T_k/3\) after the exit, and subtracting \(K=Q+F\) gives \(\Delta F=T_k/3-\Delta Q\). | **PASS** |
| (S.224) | The coefficient profile is positive, deterministic, independent of \(R,\tau\), and the solution, and satisfies the exact Step 7/8 summability ledger. | **PASS / FIXED PROFILE** |
| (S.225) | The Step 8 \(D\)-partition, the non-\(D\) duration split, and the short absolute-\(Q\) split give six pairwise disjoint classes whose union is every positive-terminal shell. | **PASS / EXACT PARTITION** |
| (S.226) | Step 7 gives \(\sigma(J_\tau)>T/(8\lambda)\) on \(\mathcal I_{\rm lo}\).  Failure of \(\mathcal I_\beta\) therefore forces the strict Step 8 \(\sigma\)-test.  The alleged extra low-Rayleigh class is empty, and \(\mathcal I_x\subset\mathcal I_{\rm def}\cup\mathcal I_{\rm hi}\). | **PASS / NO EXTRA PAYMENT** |
| (S.227) | \(\mathcal P_\beta\subset\mathcal I_D\) and \(\mathcal P_Q\subset\mathcal I_{\neg D}\) are disjoint shell sets.  Their two restricted variation sums are therefore bounded by one complete \(B_Q\), yielding exactly \(6B_Q\), not \(12B_Q\). | **PASS / ONE \(Q\)-LEDGER** |
| (S.228) | On a long non-\(D\) shell, monotonicity gives \(D(t)\le D(\tau)<T/2\), while last-exit maximality gives \(K(t)>2T/3\).  Thus \(e(t)=E(t)>T/6\) at a.e. good time.  The duration threshold produces the factor \(\lambda_k^{-3/2}\). | **PASS / A.E. PERSISTENCE** |
| (S.229) | Combining (S.228) with (R.214) and raising to the power \(2/3\) gives \(T_k\le6C_1^{2/3}\lambda_k2^k\gamma_k^{1/3}p_k^{2/3}\).  The displayed \(C_{\rm LE}=6C_1^{2/3}\) is smaller than \(C_4=12(2C_1)^{2/3}\). | **PASS / POWERS AND CONSTANTS** |
| (S.230) | Set \(J_k^{\rm pay}=J_\tau\) on \(\mathcal P_\sigma\), \(J_k^{\rm LE}\) on \(\mathcal P_{\rm LE}\), and \(\varnothing\) otherwise.  Finite-shell Hölder on the union, followed once by (R.211), gives \(C_4C_P^{2/3}\mathscr L^{1/3}A_R=C_5\mathscr L^{1/3}A_R\). | **PASS / ONE \(C_5\)-LEDGER** |
| (S.231) | The four paid classes are disjoint.  Adding (S.227) and (S.230) gives \(6B_Q+C_5\mathscr L^{1/3}A_R\), and \(B_Q\le C_QA_R\) gives the stated \(C_{\rm pay}\). | **PASS** |
| (S.232) | The residual is the \(2/3\)-last-exit physical-flux increment on the combined residual mask and is zero on paid and zero-terminal coordinates. | **PASS / WELL DEFINED IN \(\ell^1\)** |
| (S.233) | On \(\mathcal R_{\rm sh}\), \(|\Delta Q|<T/6\) is definitional.  On \(\mathcal I_x\), \(|\Delta Q|\le\beta(J_k^{\rm LE})\le\beta(J_\tau)<T/6\).  Hence \(T/6<T/3-\Delta Q<T/2\), giving both factors \(6\) and \(1/2\). | **PASS / STRICT BOUNDS** |
| (S.234) | Extending by zero gives \(0\le r_k\le T_k/2\le v_k/2\); summation gives \(\|r\|_2\le Z_R/2\).  Each positive residual increment is at most its shell's total \(F\)-variation, giving \(\sum_kr_k\le C_FP_R^M\). | **PASS / LINEAR FALLBACK ONLY** |
| (S.235) | For the same exceptional set \(S\), all paid coordinates outside \(S\) cost at most the complete paid sum, while every residual coordinate outside \(S\) costs less than \(6r_k\). | **PASS / SAME EXCEPTION SET** |
| (S.236) | Apply (S.235) to sets approaching the residual best-\(N\) infimum.  This yields the clock best-\(N\) tail bounded by the paid amount plus six times one combined residual tail. | **PASS** |
| (S.237) | The residual functional takes one supremum over good terminals after one best-\(N\) infimum.  The integer \(N\) is fixed, while the optimizing set may depend on the terminal time. | **PASS / CORRECT QUANTIFIER ORDER** |
| (S.238) | The terminal \(K\)-vector is continuous into \(\ell^1\), and \(\mathcal S_N\) is one-Lipschitz there.  Dense good terminals therefore recover the all-terminal left side on either \(I_R\) or \(\mathcal T_R\).  No continuity of \(r\) is used. | **PASS / DOMAIN-SAFE LIFT** |
| (S.239) | Coordinatewise \(r\le K/2\).  Applying this to a set approaching the clock-tail infimum and then taking the good-terminal supremum gives \(\mathfrak R_N(\mathcal D)\le\mathcal S_N^K(\mathcal D)/2\). | **PASS / REVERSE COMPARISON** |
| (S.240) | The forward implication is (S.238) plus \(B_Q\le C_QA_R\) and fixed \(\mathscr L(\lambda)\); the reverse implication is (S.239).  Both constants are uniform in \(R\) and the solution for the fixed profile. | **PASS / QUADRATIC-SCALE EQUIVALENCE** |
| (S.241) | The plateau terminal reduction contributes one \(B_Q\); (S.238) contributes six.  Hence the exact displayed coefficient is \(7B_Q\), or \(7C_Q\) after conversion to \(A_R\). | **PASS / COEFFICIENT SEVEN** |
| (S.242) | Since \(\mathcal S_N(r)\le\sum_kr_k\), (S.234) gives \(\mathfrak R_N\le C_FP_R^M\).  If \(P_R^M\le1\), then \(P_R^M\le(P_R^M)^{2/3}=A_R\). | **PASS / SMALL-PAYMENT COROLLARY** |
| (S.243) | This is explicitly labeled OPEN.  If it holds on \(\mathcal T_R\), (S.238) gives full-terminal (Q.12), and the inherited reduction gives (Q.1).  A bound only on \(I_R\) gives the plateau conclusion directly through (S.241), not full (Q.12). | **PASS / OPEN GATE, PROVED IMPLICATION** |
| (S.244) | With \(T=1\), the two rows approach residual ratios \(1/6\) and \(1/2\).  Thus the factors \(6\) and \(1/2\) cannot be improved using only \(|\Delta Q|<T/6\). | **PASS / ABSTRACT SHARPNESS TEST** |
| (S.245) | For \(r=(1,1)\), one shared exception leaves tail one.  Giving one exception separately to each labeled mechanism produces the forbidden value zero and has silently used two exceptions. | **PASS / SHARED-BUDGET TEST** |
| (S.246) | For \(T_k=2^{-k}\), deletion of the largest coordinate leaves \(1/2\).  The finite-prefix value is \(1/2-2^{-M}\), whereas allowing the budget to grow to \(M\) gives the irrelevant zero. | **PASS / FIXED-\(N\) TEST** |
| (S.247) | With the canonical profile \(\lambda=1\), the explicit clock has last exit \(\ell=1/4\), long duration \(d=7/4\), constant \(D=3/5\) afterward, and \(E(1)=7/100<1/6\).  Thus terminal \(D\)-dominance cannot be converted into last-exit kinetic persistence. | **PASS / CONTINUOUS CLOCK TEST** |

All twenty-five tags occur exactly once and in increasing order.  No sign,
strict boundary, power, displayed coefficient, or domain in
(S.223)--(S.247) requires repair.

## 5. Constant and payment audit

The literal constants follow from four short calculations.

### 5.1 One \(Q\)-ledger

The index sets \(\mathcal P_\beta\) and \(\mathcal P_Q\) are disjoint.
Consequently

\[
\begin{aligned}
 \sum_{\mathcal P_\beta\cup\mathcal P_Q}T_k
 &\le6\sum_{\mathcal P_\beta}\beta_k(J_\tau)
    +6\sum_{\mathcal P_Q}|\Delta Q_k|\\
 &\le6\sum_k\operatorname{TV}Q_k=6B_Q.
\end{aligned}
\]

Bounding each restricted sum separately by a complete \(B_Q\) would give a
valid but nonsharp \(12B_Q\).  The source correctly does not double-charge.

### 5.2 Long non-\(D\) coefficient

The lower and upper persistence estimates give

\[
 \lambda_k^{-3/2}(T_k/6)^{3/2}
 <C_1 2^{3k/2}\gamma_k^{1/2}p_k.
\]

Taking the power \(2/3\) gives

\[
 T_k<6C_1^{2/3}\lambda_k2^k\gamma_k^{1/3}p_k^{2/3}.
\]

Thus the duration threshold \(d_k\ge\lambda_k^{-3/2}\) is exactly what
places the long non-\(D\) branch in the same coefficient ledger as the
Step 8 \(\sigma\)-branch.

### 5.3 One cubic ledger

On both cubic-paid classes the coefficient is dominated by

\[
 C_4\lambda_k2^k\gamma_k^{1/3}.
\]

Hölder across their disjoint union gives

\[
 \sum_k\lambda_k2^k\gamma_k^{1/3}p_k^{2/3}
 \le\mathscr L(\boldsymbol\lambda)^{1/3}
     \left(\sum_kp_k\right)^{2/3}.
\]

Equation (R.211) bounds the last sum by \(C_PP_R^M\).  Hence the coefficient
is one

\[
 C_4C_P^{2/3}=C_5,
\]

not two copies of \(C_5\).

### 5.4 Residual and plateau coefficients

On the residual support,

\[
 {T_k\over6}<r_k<{T_k\over2}.
\]

The first inequality produces the factor \(6\) in the clock-tail reduction;
the second produces the reverse factor \(1/2\).  The plateau flux reduction
adds one further \(B_Q\) to the paid amount, so

\[
 6B_Q+B_Q=7B_Q.
\]

The coefficient table is therefore:

| Row | Audited coefficient | Decision |
|---|---:|---|
| Combined \(Q\)-paid shells | \(6B_Q\) | **PASS** |
| Long non-\(D\) per-shell row | \(6C_1^{2/3}\lambda_k\) | **PASS** |
| Combined cubic shells | \(C_5\mathscr L(\lambda)^{1/3}A_R\) | **PASS / ONE LEDGER** |
| Residual-to-clock comparison | \(T_k<6r_k\) | **PASS / SHARP FOR THIS SPLIT** |
| Clock-to-residual comparison | \(r_k<T_k/2\) | **PASS / SHARP FOR THIS SPLIT** |
| Plateau \(Q\)-coefficient | \(7B_Q\) | **PASS** |

## 6. Quantifier, topology, and domain audit

The quantifiers are:

\[
 \text{fix }\boldsymbol\lambda;
 \quad
 \text{fix }N;
 \quad
 \sup_{\tau\in\mathcal D\cap\mathcal G_R}
 \inf_{S_\tau\subset\mathbb N,\ \#S_\tau\le N}.
\]

The profile and integer do not depend on \(R\), the solution, or the
terminal time.  The exceptional set may depend on the terminal time, but
there is only one such set for the union
\(\mathcal R_{\rm sh}\cup\mathcal R_x\).  Giving each residual mechanism a
separate budget would replace \(N\) by as many as \(2N\).

For nonnegative \(x,y\in\ell^1\), comparison with the same exceptional set
gives

\[
 |\mathcal S_N(x)-\mathcal S_N(y)|\le\|x-y\|_1.
\]

The terminal \(K\)-vector is continuous into \(\ell^1\), so
\(\tau\mapsto\mathcal S_N(K(\tau))\) is continuous.  The common good-time
set is dense in each open domain.  This proves the all-terminal left side of
(S.238).  It does not prove or require continuity, measurability, or lower
semicontinuity of \(\ell_k(\tau)\), any branch mask, or \(r(\tau)\).

The two domains have different consequences:

| Domain | Consequence of a quadratic residual estimate |
|---|---|
| \(I_R\) | By (S.241), controls the inherited plateau observable \(\mathfrak C_R^M\) and hence the plateau target (Q.1); it does not establish full-terminal (Q.12). |
| \(\mathcal T_R=(s_R,t_0)\) | By (S.238), establishes the full-terminal clock tail (Q.12), which then implies (Q.1). |

Only
\(\mathfrak C_R^M\le\mathfrak C_{{\rm full},R}^M\) is inherited.  Equality
or a reverse inequality is neither used nor claimed.

## 7. Endpoint and source-boundary audit

1. **Positive terminal shell.**  If \(T_k>0\), the intermediate-value
   theorem places the \(2T_k/3\) level strictly between \(s_R\) and
   \(\tau\).  Thus \(J_k^{\rm LE}\) has positive length.
2. **Zero terminal shell.**  The convention \(\ell_k=\tau\) and \(r_k=0\)
   produces no fictitious strict upcrossing and no residual mass.
3. **Open terminal interval.**  Since \(\tau<t_0\),
   \(d_k<4\).  If \(\lambda_k^{-3/2}\ge4\), that shell has no long class.
4. **Possibly non-good stop.**  No value of \(E\) or \(D\) at \(\ell_k\)
   is used.  The last-exit property uses only continuity of \(K\).
5. **A.e. kinetic identity.**  On \(J_k^{\rm LE}\), the equality
   \(K=E+D\) is used only at the a.e. local-energy good times needed for
   the time integral.
6. **Direction of monotonicity.**  Terminal non-dominance gives
   \(D(t)\le D(\tau)<T/2\) for earlier times.  Terminal dominance gives no
   analogous kinetic lower bound; (S.247) exhibits the failure.
7. **Full-history Step 8 tests.**  The \(\beta/\sigma/x\) classes retain
   \(J_\tau=(s_R,\tau)\).  They are not redefined on the last-exit interval.
8. **Absolute \(Q\)-increment.**  Absolute continuity gives
   \(|\Delta Q_k|\le\beta_k(J_k^{\rm LE})\le\beta_k(J_\tau)\); endpoint
   conventions add no atoms.
9. **Shell-dependent payments.**  The family \(J_k^{\rm pay}\) is completed
   by \(\varnothing\) off the two cubic classes before (R.211) is invoked.
10. **Infinite tail.**  The variation ledgers and \(r_k\le T_k/2\) give
    absolute summability before an infimum or supremum is taken.  No one
    infinite stopped cutoff is used as a local-energy test.

All ten boundary checks pass.

## 8. Stress-test audit

| Stress row | What it tests | Result |
|---|---|---|
| Threshold assignment | Equality at the duration, \(Q\), \(D\), \(\beta\), and \(\sigma\) boundaries leaves no unassigned shell | **PASS** |
| Step 7 low-Rayleigh row | A proposed \(\mathcal I_{\rm lo}\setminus(\mathcal I_\beta\cup\mathcal I_\sigma)\) class is empty | **PASS / EXTRA CLASS RULED OUT** |
| Two \(Q\)-paid classes | Their disjoint shell supports permit one \(6B_Q\) bound | **PASS / NO DOUBLE CHARGE** |
| Two cubic-paid classes | Shell-dependent time sets permit one combined Hölder and one use of (R.211) | **PASS / NO DOUBLE CHARGE** |
| Residual boundary rows (S.244) | Ratios approach \(1/6\) and \(1/2\) from inside the strict residual class | **PASS / FACTORS SHARP AT CLOCK LEVEL** |
| Two labeled residual coordinates (S.245) | Separate best-\(N\) infima would spend two exception budgets | **PASS / ONE SHARED BUDGET REQUIRED** |
| Geometric tail (S.246) | A truncation-dependent exception count cannot replace one fixed \(N_0\) | **PASS** |
| Long terminal-\(D\) clock (S.247) | A long last-exit interval plus terminal \(D\)-dominance does not imply \(e>T/6\) | **PASS / EXPLICIT RATIONAL CLOCK** |
| Linear fallback | \(CP_R^M\) is quadratic-scale only when \(P_R^M\le1\); the large-payment gap is \((P_R^M)^{1/3}\) | **PASS / LARGE-PAYMENT GATE OPEN** |
| Plateau versus full domain | An \(I_R\) result controls the plateau observable but is not silently promoted to full (Q.12) | **PASS** |

The fixtures in (S.244)--(S.247) are scalar, sequence, or continuous-clock
tests.  They are not asserted to be Navier--Stokes solutions.  They certify
constants, quantifiers, and forbidden algebraic deductions only.

## 9. Claim and route ledger

| Claim | Audit status |
|---|---|
| Six-class paid/residual partition | **PROVED EXACTLY** |
| Absence of an additional Step 7 low-Rayleigh class | **PROVED EXACTLY** |
| Combined \(Q\)-payment \(6B_Q\) | **PROVED** |
| Long non-\(D\) a.e. persistence and cubic payment | **PROVED** |
| One combined \(C_5\) cubic ledger | **PROVED** |
| Residual positivity and \(T/6<r<T/2\) | **PROVED EXACTLY** |
| Fixed-good-terminal best-\(N\) reduction | **PROVED** |
| Good-time-to-all-time lift on \(I_R\) and \(\mathcal T_R\) | **PROVED FOR THE TERMINAL CLOCK TAIL** |
| Continuity or lower semicontinuity of the residual selector | **NOT PROVED / NOT CLAIMED / NOT NEEDED FOR (S.238)** |
| Quadratic-scale equivalence (S.240) | **PROVED FOR FIXED \(N_0\) AND FIXED ADMISSIBLE \(\boldsymbol\lambda\)** |
| Plateau coefficient \(7B_Q\) | **PROVED** |
| Linear fallback \(\mathfrak R_N\le C_FP_R^M\) | **PROVED; INSUFFICIENT WHEN \(P_R^M>1\)** |
| Full-domain residual estimate (S.243) | **OPEN** |
| Plateau residual estimate of order \(A_R\) | **OPEN; WOULD IMPLY THE PLATEAU TARGET DIRECTLY** |
| Packing short non-\(D\), \(Q\)-small shells | **OPEN** |
| Packing the surviving anomalous-defect/high-Rayleigh ancestry | **OPEN** |
| Full-terminal R0.74Q (Q.12) and fixed-scale (Q.1) | **OPEN** |
| Separate \(N\)-exception budgets for the two residual classes | **RULED OUT AS A CHANGE OF THE TARGET QUANTIFIER** |
| Localizing terminal \(D\)-dominance to \(J_k^{\rm LE}\) | **REFUTED AT THE COMPLETED-CLOCK LEVEL BY (S.247)** |
| Two complete \(Q\)- or cubic-ledger charges are necessary | **REFUTED; SEPARATE DOUBLE CHARGES ARE VALID BUT NONSHARP** |
| Canonical last exits alone create fixed-\(N\) compression | **REFUTED AT THE COMPLETED-CLOCK ALGEBRA LEVEL** |
| R0.74R extraction, scale contraction, prescribed-centre packing, and regularity | **OPEN** |
| Novelty, priority, singularity formation, or Millennium conclusion | **NOT CLAIMED / NOT CLAY** |

The two genuine residual mechanisms are therefore:

1. short non-\(D\), absolute-\(Q\)-small last-exit flux; and
2. the Step 8 scalar-excess class, which may retain anomalous-defect or
   high-Rayleigh ancestry.

The note proves no quadratic packing of either class.  Any later separate
analysis must recombine them before applying one shared best-\(N\) exception
budget.

## 10. Machine-verifiable and analytic boundaries

The following checks are mechanical:

- recomputing the eight frozen SHA-256 values;
- checking that the twenty-five tags (S.223)--(S.247) occur exactly once and
  in increasing order;
- evaluating the rational values in (S.244)--(S.247);
- checking literal occurrence of one \(6B_Q\), one \(C_5\), the plateau
  coefficient \(7B_Q\), and the two terminal domains; and
- checking that (S.243) remains labeled OPEN and that the claim ledger does
  not promote it to PROVED.

These checks do not prove:

- the inherited local-energy identity or dissipation-measure theory;
- the inherited shell payment (R.211) or spatial estimate (R.214);
- density and \(\ell^1\)-continuity facts beyond their source proofs;
- realization of the scalar stress fixtures by Navier--Stokes solutions; or
- the open residual best-\(N_0\) estimate.

Those points require the analytic backtracking above and, for the open
packing estimate, new PDE input.

## 11. Counted final decision

| Audit group | Passed | Failed |
|---|---:|---:|
| Locked source and seven dependency hash bindings | 8 | 0 |
| Numbered equations (S.223)--(S.247) | 25 | 0 |
| Partition, payment, and constant invariants | 6 | 0 |
| Quantifier and terminal-domain invariants | 6 | 0 |
| Endpoint and source boundaries | 10 | 0 |
| Explicit stress rows | 10 | 0 |
| Claim-status categories: PROVED, INHERITED, OPEN, NOT CLAIMED | 4 | 0 |

**Required source repairs remaining: 0.**  The locked note proves a
domain-safe paid-branch deletion and an exact quadratic-scale equivalence
between its residual best-\(N\) gate and the inherited terminal clock tail.
It leaves the residual packing estimate, full-terminal Q.12, fixed-scale
Q.1, and every regularity consequence open.

**NOT CLAY.**
