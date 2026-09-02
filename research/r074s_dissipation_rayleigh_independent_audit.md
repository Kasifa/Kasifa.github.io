# R0.74S Step 7 — independent dissipation--Rayleigh audit

## 1. Independent verdict

**PASS.**  On the frozen source bytes, the low-Rayleigh theorem is a valid
consequence of the R0.74P dissipation split and the R0.74R padded-shell cubic
payment.  The new argument closes exactly one part of the
dissipation-dominated terminal family: shells for which neither anomalous
defect nor high-Rayleigh viscous dissipation reaches the prescribed
one-eighth threshold.  It does not close either residual family.

The independently audited source is
`research/r074s_dissipation_rayleigh_gate.md`, SHA-256
`e835a104f4a6f4d2281bef877dd6bfeb73f1c2396f6bd28203bb0812f7f8e3d3`.
All tags (S.142)--(S.162) occur exactly once and in order.  The definitions,
strict inequalities, powers of \(R\), powers of \(\gamma_k\), and the
cross-shell exponent ledger are consistent.  The exact-shear paragraph is
properly restricted to the time set \(H_{k,R}\), and its use of the
conditional interface (R.216)--(R.217) treats both endpoint-energy cases
without a \(0\cdot\infty\) ambiguity.

This verdict independently audits the displayed mathematics; it does not
re-prove the inherited suitable-weak local-energy theory, (R.211), or
(R.214).  It is not a novelty or priority opinion.  The high-Rayleigh and
anomalous-defect residuals, (Q.1), regularity, and the Millennium problem
remain open.  **NOT CLAY.**

## 2. Independent analytic reconstruction

### 2.1 The direct low set and the factor two

Write

\[
 A(t)=\int\Psi_k^R|v_R|^2,
 \qquad B(t)=\int\Psi_k^R|\nabla v_R|^2.
\]

At times for which \(\eta_R>0\) and \(A>0\), (S.142) gives

\[
 {g_{k,R}\over e_{k,R}}=2{B\over A}.
\]

Consequently

\[
 g_{k,R}\le {2\lambda_k\over R^2}e_{k,R}
 \quad\Longleftrightarrow\quad
 R^2{B\over A}\le\lambda_k.
\]

The hypothesis \(\eta_R>0\) is essential for this quotient
reformulation and is present in (S.145).  The actual definition (S.144)
does not divide.  If \(\eta_R=0\), both rows vanish.  If \(A=0\), Sobolev
locality gives \(\nabla v_R=0\) almost everywhere on the open positivity set
of \(\Psi_k^R\), so the weighted gradient row also vanishes.  Hence the
zero rows belong to \(L_{k,R}\) directly, with no \(0/0\) convention.

### 2.2 Priority trichotomy and strict residual

For \(T_k>0\) in the dissipation branch,
\(D_{k,R}(\tau)\ge T_k/2\).  A shell enters the defect class first if
\(m_{k,R}\ge T_k/8\), and otherwise enters the high class if
\(\int_Hg_{k,R}\ge T_k/8\).  A shell left over therefore satisfies both
strict failures.  Using the exact nonnegative split,

\[
 \int_Lg_{k,R}
 =D_{k,R}-m_{k,R}-\int_Hg_{k,R}
 >\left({1\over2}-{1\over8}-{1\over8}\right)T_k
 ={T_k\over4}.
\]

The priority ordering makes the classes disjoint and exhaustive.  It is
also what justifies the two separate residual bounds
\(T_k\le8m_{k,R}\) and \(T_k\le8\int_Hg_{k,R}\) in (S.160).

### 2.3 From low dissipation to cubic payment

On \(L=L_{k,R}\), the direct defining inequality and the preceding strict
bound give

\[
 {1\over R^2}\int_Le_{k,R}>{T_k\over8\lambda_k}.
\]

Let \(\delta=|L|/R^2\).  The right side is positive, so \(\delta>0\), and
\(L\subset(s_R,\tau)\subset(s_R,t_0)\) gives \(\delta\le4\).  Hölder on
\(L\), with all powers of \(R\) retained, is

\[
 {1\over R^2}\int_Le_{k,R}^{3/2}
 \ge \delta^{-1/2}
 \left({1\over R^2}\int_Le_{k,R}\right)^{3/2}
 \ge {1\over2}
 \left({1\over R^2}\int_Le_{k,R}\right)^{3/2}.
\]

Combining this with inherited (R.214) yields

\[
 {1\over2}\left({T_k\over8\lambda_k}\right)^{3/2}
 <C_1 2^{3k/2}\gamma_k^{1/2}p_{k,R}^{\rm lo}.
\]

Raising to \(2/3\) gives precisely

\[
 T_k\le 8(2C_1)^{2/3}\lambda_k2^k\gamma_k^{1/3}
 (p_{k,R}^{\rm lo})^{2/3}.
\]

There is no missing factor of \(R\), and replacing the resulting strict
inequality by a weak upper bound is harmless.

### 2.4 The all-shell ledger

For a finite shell set, Hölder with exponents \(3\) and \(3/2\) gives

\[
 \sum_k
 \bigl(\lambda_k2^k\gamma_k^{1/3}\bigr)
 (p_{k,R}^{\rm lo})^{2/3}
 \le
 \left(\sum_k2^{3k}\gamma_k\lambda_k^3\right)^{1/3}
 \left(\sum_kp_{k,R}^{\rm lo}\right)^{2/3}.
\]

The selected time set is allowed to depend on the shell in inherited
(R.211), so its nonnegative payment sum is bounded by \(C_PP_R^M\).
Increasing finite shell sets then gives (S.155) by monotone convergence.
The same finite-first argument validates (S.160), including cases in which
an unbounded residual is interpreted as \(+\infty\).

For the near-critical profile,

\[
 2^{3k}\gamma_k
 \left(2^{-(1+\varepsilon)k}\gamma_k^{-1/3}\right)^3
 =2^{-3\varepsilon k}.
\]

Thus the sum from \(k=1\) is
\(2^{-3\varepsilon}/(1-2^{-3\varepsilon})\).  At
\(\varepsilon=0\), every coefficient equals one, so the boundary diverges;
at \(\varepsilon=1\), it is \(1/7\).  For
\(\lambda_k=\gamma_k^{-\alpha}\), the remaining exponent
\(1-3\alpha>0\) exactly in the stated subcritical range, and the
super-Gaussian tail dominates \(2^{3k}\).

### 2.5 Conditional and shear boundaries

If a future theorem supplies
\(\#(\mathcal I_{\rm def}\cup\mathcal I_{\rm hi})\le N_D\), then
\(K_{k,R}(\tau)\le v_{k,R}\) and Cauchy--Schwarz give the second line of
(S.161).  Step 7 does not supply this cardinality bound, so the implication
is correctly marked conditional.

For the inherited smooth shear with \(A\ne0\) and integer \(N\), the
amplitude cancels from the quotient and

\[
 \rho_{k,R}^{(N)}=(NR)^2{M_k^R+c_{k,N}^R\over M_k^R-c_{k,N}^R},
 \qquad c_{k,N}^R\longrightarrow0.
\]

This proves only that the high-Rayleigh **time set** can occur at high
frequency.  It does not put a shell into the priority class
\(\mathcal I_{\rm hi}\), because that class also requires the integrated
one-eighth threshold and failure of the defect test.  Periodicity in the
shear direction gives \(F_{k,R}=0\), hence \(K=Q\), so this same family is
already paid by the inherited \(Q\)-variation ledger.

For (R.216)--(R.217), taking
\(q_k=\operatorname{TV}Q_k\) and \(\Lambda_k=0\) is legitimate.  When the
endpoint kinetic row is positive, the source chooses a positive-measure
set where \(\eta_R>0\), so \(0<\Theta_k^\eta<\infty\).  When it vanishes,
the inherited convention gives \(\Theta_k^\eta=+\infty\), hence
\((\Theta_k^\eta)^{-2}=0\).  In either case the coefficient row in (R.217)
is literally zero.

## 3. Independent executable audit

The independent verifier is
`scripts/r074s_dissipation_rayleigh_certificate_independent.rb`, SHA-256
`a4ce5bb0d3f20f549e70b7196487fd9540a5ff7be658d4cd52573d65f1a77ff3`.
It uses only the Ruby standard library and exact `Rational` arithmetic.
The note, primary certificate, primary generator, and primary report paths
are independently overridable by environment variables.

The verifier returned **PASS** with:

- 12/12 exact exponent and threshold rows;
- 7,332/7,332 eligible priority-trichotomy cases inside 8,788 exact grid
  configurations;
- 180/180 low-Rayleigh mass fixtures;
- 7,875/7,875 rational step-function Jensen fixtures, including 315
  equality cases;
- 1,728/1,728 exact cross-shell Hölder fixtures, including 48 equality
  cases;
- 9/9 near-critical rational profile rows, together with the constant,
  subcritical, canonical-\(1/7\), and critical-divergence boundaries;
- 31/31 independent structural and claim-boundary checks; and
- 9/9 adversarial mutations rejected.

The rejected mutations were: a stale note hash, a shifted terminal tag, a
changed near-critical profile, a one-eighth-to-one-quarter threshold change,
removal of the positive-\(\eta_R\) condition needed at the (R.217) interface,
a tampered producer profile row, a stale producer summary, promotion of the
finite certificate to an analytic PDE claim, and a stale generator hash.

Two clean executions and one execution through all four environment path
overrides produced byte-identical stdout, SHA-256
`0cda558db75d6a6bd748cce287dc22e0924a1281543a47d64bd338d8d7956499`.
The output contains no time, randomness, floating-point arithmetic,
network access, or non-standard dependency.

## 4. Primary-producer cross-check

Only after completing the independent arithmetic did the Ruby verifier
open the Python-produced certificate.  The producer cross-check is
**PASS**:

| Frozen artifact | SHA-256 |
|---|---|
| Primary Python generator | `61bb1322151b66fc0cf780d2dfc15e0e06dde9a6cc59cc192be1b8c9e8d5e76a` |
| Primary JSON certificate | `4f26fefe25ec92cdae86c2a45f384d0ed87ab3afe83a7d9ef7829ff829be6be1` |
| Primary certificate report | `5c566f53e378c9f3fba2a690c3962051142ac00990c1177548b9ae3e956b14cb` |

The JSON binds the final note and generator hashes, has the expected schema
and finite-only scope, and reports 16/16 exact rows, 8/8 finite checks,
52/52 structural checks, and 9/9 negative mutations.  Every row is marked
passing, every failure list is empty, identifiers are unique and complete,
the summary counts agree with the arrays, and the Markdown report reproduces
the same hashes and scope boundary.

## 5. Final boundary

The following are supported by this audit:

- the exact dissipation/defect split, conditional on the inherited
  suitable-weak measure identity;
- the measurable direct low/high time split;
- the one-eighth/one-eighth/one-quarter priority trichotomy;
- the low-Rayleigh kinetic-mass, Jensen, per-shell, and all-shell payments;
- the admissible and critical sequence profiles;
- the residual ledger; and
- the stated finite-exception consequence as a conditional implication.

The following are not supported and remain **OPEN**: a universal payment or
finite-exception theorem for high-Rayleigh shells, a corresponding theorem
for anomalous-defect shells, stopped-work depletion, arbitrary-clock
extraction, (Q.1), scale contraction, regularity, or any Millennium
conclusion.

**FINITE/ALGEBRAIC MACHINE CHECKS ONLY.  INHERITED ANALYSIS IS NOT
MACHINE-PROVED.  NOT CLAY.**
