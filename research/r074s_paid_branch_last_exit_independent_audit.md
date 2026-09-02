# R0.74S Step 10 — independent analytic audit of the paid-branch last-exit residual

## 1. Verdict and locked source

**PASS, with no mathematical reservation.**  This audit independently
re-derives the partition, the two paid ledgers, the residual comparison, the
best-\(N\) quantifiers, and the good-time/domain passage in the locked note

`research/r074s_paid_branch_last_exit_residual.md`

at SHA-256

`9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c`.

The result is an exact reduction, not a residual packing theorem.  In
particular, the audit confirms that the full-domain assertion (S.243) remains
**OPEN** and is not among the proved statements.

This is a human analytic audit.  Finite symbolic checks could test the
six-class set algebra and the constants in sample vectors, but they would not
prove the suitable-weak good-time identities, the measure monotonicity, the
velocity-cubic estimate, or any uniform PDE residual bound.

## 2. Noncircular source boundary

The derivation uses only the following frozen inputs.

| Input | Exact use here | Audit status |
|---|---|---|
| R0.74P, (2.7)--(3.7) | Continuous canonical \(Q,F,K\) paths, zero start, \(K=Q+F\), summable variation, \(K_k(\tau)\le v_k\), and \(\ell^1\)-continuity of the terminal vector | **INHERITED / PASS** |
| R0.74Q, (Q.7)--(Q.12) | Fixed-\(N\), terminal-dependent exceptional set and the terminal clock-to-flux reduction | **INHERITED / PASS; TAIL BOUND OPEN** |
| R0.74R, (R.209)--(R.214) | Definition of \(p_{k,R}^{u,\eta}(J)\), the arbitrary shell-dependent measurable-set budget, and padded-shell spatial Hölder | **INHERITED / PASS** |
| Step 7, (S.142)--(S.155) | \(e=E\) a.e., good-time \(K=E+D\), monotonicity of cumulative \(D\), and the low-Rayleigh kinetic-mass lower bound | **INHERITED / PASS** |
| Step 8, (S.163)--(S.176) | Full-history \(J_\tau\), the \(\beta,\sigma,x\) priority partition, and the \(C_4,C_5\) cubic payment | **INHERITED / PASS** |
| Step 9, (S.200)--(S.222) | Plateau/full domains, \(\mathcal S_N\), \(\ell^1\)-Lipschitz continuity, \(2/3\)-last exits, and finite good-stop closure | **INHERITED / PASS** |

No estimate from Step 10 is imported into its own proof.

## 3. Independent reconstruction of the six classes

Fix a common local-energy good terminal time
\(\tau\in\mathcal G_R\cap\mathcal T_R\), and put
\(T_k=K_{k,R}(\tau)\).  If \(T_k>0\), continuity, zero start, and
\(K_k(\tau)=T_k>2T_k/3\) give the well-defined last exit

\[
 \ell_k=\max\{t\in[s_R,\tau]:K_{k,R}(t)\le 2T_k/3\}.
\]

Maximality and continuity imply

\[
 K_k(\ell_k)=\frac23T_k,\qquad
 K_k(t)>\frac23T_k\quad(\ell_k<t\le\tau),\qquad
 \ell_k<\tau.
\]

Define

\[
 J_k^{\rm LE}=(\ell_k,\tau),\qquad
 d_k=\frac{\tau-\ell_k}{R^2},\qquad
 \Delta Q_k=Q_k(\tau)-Q_k(\ell_k).
\]

Because \(s_R=t_0-4R^2\) and \(\tau<t_0\), one has
\(0<d_k<4\).  The completed-clock identity gives

\[
 \Delta F_k=\frac13T_k-\Delta Q_k.
\]

For \(T_k=0\), the convention \(\ell_k=\tau\), \(d_k=0\), and
\(r_k=0\) is consistent and creates no strict upcrossing.

Fix one positive deterministic profile \(\boldsymbol\lambda\), independent
of the solution, scale, and terminal time, such that

\[
 \mathscr L(\boldsymbol\lambda)
 =\sum_{k\ge1}2^{3k}\gamma_k\lambda_k^3<\infty.
\]

Among positive-terminal shells, use the complementary boundary conventions

\[
\begin{aligned}
 \mathcal I_D&=\{D_k(\tau)\ge T_k/2\},&
 \mathcal I_{\neg D}&=\{D_k(\tau)<T_k/2\},\\
 \mathcal I_{\rm long}&=\{d_k\ge\lambda_k^{-3/2}\},&
 \mathcal I_{\rm short}&=\{d_k<\lambda_k^{-3/2}\},\\
 \mathcal I_{Q+}&=\{|\Delta Q_k|\ge T_k/6\},&
 \mathcal I_{Q-}&=\{|\Delta Q_k|<T_k/6\}.
\end{aligned}
\]

On \(\mathcal I_D\), retain the Step 8 partition exactly as defined on
the full preterminal interval \(J_\tau=(s_R,\tau)\):

\[
 \mathcal I_D
 =\mathcal I_\beta\dot\cup\mathcal I_\sigma
  \dot\cup\mathcal I_x.
\]

In particular, \(\mathcal I_\sigma\) is already defined after exclusion
of \(\mathcal I_\beta\); no additional exclusion is required.  The six
classes are therefore

\[
\begin{aligned}
 \mathcal P_\beta&=\mathcal I_\beta,\qquad
 \mathcal P_\sigma=\mathcal I_\sigma,\\
 \mathcal P_{\rm LE}&=\mathcal I_{\neg D}\cap\mathcal I_{\rm long},\\
 \mathcal P_Q&=\mathcal I_{\neg D}\cap\mathcal I_{\rm short}
                         \cap\mathcal I_{Q+},\\
 \mathcal R_{\rm sh}&=\mathcal I_{\neg D}\cap\mathcal I_{\rm short}
                         \cap\mathcal I_{Q-},\\
 \mathcal R_x&=\mathcal I_x.
\end{aligned}
\]

They are pairwise disjoint and exhaust \(\{k:T_k>0\}\): the \(D\)
branch is exhausted by Step 8, while its complement is split first by
duration and then, only on the short side, by the absolute \(Q\)-increment.
The notation \(Q+\) means absolute-\(Q\)-large, not positive sign.

## 4. Step 7/8 compatibility does not create a seventh class

If \(k\in\mathcal I_{\rm lo}\), Step 7 gives

\[
 \sigma_k(J_\tau)\ge\sigma_k(L_{k,R})
 >\frac{T_k}{8\lambda_k}.
\]

If this shell is not in \(\mathcal I_\beta\), then
\(T_k/(8\lambda_k)>T_k/(12\lambda_k)\) puts it in the strict
Step 8 \(\sigma\)-branch.  Hence

\[
 \mathcal I_{\rm lo}\subset
 \mathcal I_\beta\cup\mathcal I_\sigma,\qquad
 \mathcal I_x\cap\mathcal I_{\rm lo}=\varnothing.
\]

Since Step 7 partitions \(\mathcal I_D\) into
\(\mathcal I_{\rm def}\), \(\mathcal I_{\rm hi}\), and
\(\mathcal I_{\rm lo}\), it follows that

\[
 \mathcal I_x
 =\mathcal I_x\cap
  (\mathcal I_{\rm def}\cup\mathcal I_{\rm hi}).
\]

This identifies ancestry only.  It neither pays \(\mathcal I_x\) nor
localizes defect or high-Rayleigh mass to \(J_k^{\rm LE}\).

## 5. Exactly one \(Q\)-variation ledger

For \(k\in\mathcal P_\beta\), Step 8 gives

\[
 T_k\le6\beta_{k,R}(J_\tau).
\]

For \(k\in\mathcal P_Q\), the defining boundary gives

\[
 T_k\le6|\Delta Q_k|
 \le6\operatorname {TV}_{[s_R,t_0)}Q_{k,R}.
\]

The two shell sets are disjoint because the first lies in
\(\mathcal I_D\) and the second in \(\mathcal I_{\neg D}\).
Moreover, on each selected shell both \(\beta(J_\tau)\) and
\(|\Delta Q_k|\) are bounded by that shell's full \(Q\)-variation.
Therefore disjointness must be used before enlarging to the global ledger:

\[
 \sum_{k\in\mathcal P_\beta\cup\mathcal P_Q}T_k
 \le6B_{Q,R}^M\le6C_QA_R.
\]

There is one \(6B_Q\), not two.  A bound by \(12B_Q\) would remain
true but would be a nonsharp double charge.

## 6. Long non-\(D\) persistence and the cubic ledger

Let \(k\in\mathcal P_{\rm LE}\).  The cumulative dissipation clock
\(D_k\) is nondecreasing.  Hence, for every \(t<\tau\),

\[
 D_k(t)\le D_k(\tau)<\frac12T_k.
\]

At almost every common good time in \(J_k^{\rm LE}\), the physical and
canonical clocks agree and \(e_k=E_k\).  Combining this with last-exit
persistence gives

\[
 e_k(t)=K_k(t)-D_k(t)>\frac16T_k
 \quad\text{for a.e. }t\in J_k^{\rm LE}.
\]

Consequently,

\[
 \frac1{R^2}\int_{J_k^{\rm LE}}e_k(t)^{3/2}\,dt
 >d_k\left(\frac{T_k}{6}\right)^{3/2}
 \ge\lambda_k^{-3/2}
       \left(\frac{T_k}{6}\right)^{3/2}.
\]

R0.74R (R.214), integrated on this measurable open interval, gives

\[
 \frac1{R^2}\int_{J_k^{\rm LE}}e_k^{3/2}\,dt
 \le C_1 2^{3k/2}\gamma_k^{1/2}
       p_{k,R}^{u,\eta}(J_k^{\rm LE}).
\]

Raising the resulting inequality to the power \(2/3\) yields

\[
 T_k\le C_{\rm LE}\lambda_k2^k\gamma_k^{1/3}
       p_{k,R}^{u,\eta}(J_k^{\rm LE})^{2/3},\qquad
 C_{\rm LE}=6C_1^{2/3}.
\]

The Step 8 \(\mathcal P_\sigma\) estimate has the same sequence
coefficient and the larger constant

\[
 C_4=12(2C_1)^{2/3}>C_{\rm LE},\qquad
 T_k\le C_4\lambda_k2^k\gamma_k^{1/3}
       p_{k,R}^{u,\eta}(J_\tau)^{2/3}.
\]

Choose, shell by shell,

\[
 J_k^{\rm pay}=
 \begin{cases}
  J_\tau,&k\in\mathcal P_\sigma,\\
  J_k^{\rm LE},&k\in\mathcal P_{\rm LE},\\
  \varnothing,&\text{otherwise}.
 \end{cases}
\]

These are measurable subsets of \((s_R,t_0)\).  R0.74R (R.211)
explicitly permits a different measurable set for every shell.  Finite-shell
Hölder on the union, followed by (R.211) and monotone convergence, gives

\[
\begin{aligned}
 \sum_{k\in\mathcal P_\sigma\cup\mathcal P_{\rm LE}}T_k
 &\le C_4
 \left(\sum_k2^{3k}\gamma_k\lambda_k^3\right)^{1/3}
 \left(\sum_kp_{k,R}^{u,\eta}(J_k^{\rm pay})\right)^{2/3}\\
 &\le C_4C_P^{2/3}\mathscr L(\boldsymbol\lambda)^{1/3}A_R.
\end{aligned}
\]

Thus \(C_5=C_4C_P^{2/3}\) is correct.  Combining the branches before
Hölder is what avoids a second complete cubic-ledger charge.

The proof is valid only in the non-\(D\) branch.  Terminal
\(D_k(\tau)\ge T_k/2\) does not imply a lower bound for \(E_k\), or
for the increment of \(D_k\), on the last-exit interval.  The full-history
Step 8 payment is indispensable there.

## 7. Residual positivity and exact comparison constants

Put

\[
 \mathcal I_{\rm res}=\mathcal R_{\rm sh}\cup\mathcal I_x,\qquad
 r_k=1_{\mathcal I_{\rm res}}(k)\Delta F_k.
\]

On \(\mathcal R_{\rm sh}\), \(|\Delta Q_k|<T_k/6\) holds by
definition.  On \(\mathcal I_x\), failure of the first Step 8 test and
absolute continuity of \(Q_k\) give

\[
 |\Delta Q_k|
 \le\beta_k(J_k^{\rm LE})\le\beta_k(J_\tau)<\frac16T_k.
\]

Therefore every residual coordinate satisfies

\[
 \frac16T_k
 <r_k=\frac13T_k-\Delta Q_k
 <\frac12T_k,\qquad
 2r_k<T_k<6r_k.
\]

The strictness depends on assigning \(|\Delta Q_k|=T_k/6\) to the paid
side.  Globally, after setting \(r_k=0\) off the residual set,

\[
 0\le r_k\le\frac12T_k\le\frac12v_{k,R}.
\]

Hence

\[
 r(\tau)\in\ell^1_+,\qquad
 \|r(\tau)\|_{\ell^2}\le\frac12Z_R,\qquad
 \sum_kr_k\le\sum_k\operatorname {TV}F_k\le C_FP_R^M.
\]

The \(\ell^2\) bound does not control a fixed-\(N\) \(\ell^1\) tail.
The constants \(6\) and \(1/2\) are sharp in the abstract clock
algebra as \(\Delta Q/T\) approaches \(1/6\) and \(-1/6\),
respectively, from inside the residual region.

## 8. Best-\(N\) deletion and the quantifier order

For every individual \(S\subset\mathbb N\) with \(\#S\le N\), split the
nonexceptional terminal mass by the six-class partition.  Paid shells lying
inside \(S\) only decrease the left side.  The two paid estimates and the
residual comparison give

\[
 \sum_{k\notin S}T_k
 \le6B_{Q,R}^M
  +C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R
  +6\sum_{k\notin S}r_k.
\]

To pass to the infimum, take a sequence of sets \(S_j\) approaching the
infimum of the residual tail and apply the preceding inequality to those
same sets.  Since the clock vector is nonnegative,

\[
 \mathcal S_N(K(\tau))
 \le6B_{Q,R}^M
  +C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R
  +6\mathcal S_N(r(\tau)).
\]

There is no invalid interchange of two unrelated infima.  There is also only
one terminal-dependent exceptional set for the combined residual.  Giving
each residual mechanism its own \(N\)-element set would change the theorem
to an exception budget as large as \(2N\).

Conversely, \(0\le r_k\le T_k/2\) and use of the same exceptional set give

\[
 \mathcal S_N(r(\tau))\le\frac12\mathcal S_N(K(\tau)).
\]

All infinite sums are legitimate: \(T(\tau),r(\tau)\in\ell^1_+\), the
paid sums have nonnegative summands, and finite-shell Hölder followed by
monotone convergence precedes every infinite cubic sum.  No infinite family
of stopped cutoffs is used as one local-energy test.

## 9. Good terminals and the two terminal domains

For \(\mathcal D\in\{I_R,\mathcal T_R\}\), define

\[
 \mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)
 =\sup_{\tau\in\mathcal D\cap\mathcal G_R}
   \mathcal S_N(r(\tau)).
\]

The residual is deliberately defined only at good terminal times.  The map
\(\tau\mapsto K(\tau)\) is continuous into \(\ell^1\), while
\(\mathcal S_N\) is one-Lipschitz there.  The common good set is dense in
each terminal interval.  Consequently only the left side extends from good
times to all terminal times:

\[
 \mathcal S_{N,R}^{K}(\mathcal D)
 \le6B_{Q,R}^M
  +C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R
  +6\mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D).
\]

No continuity, measurability in \(\tau\), or lower semicontinuity of the
last-exit selector, branch masks, or residual vector is invoked.  The reverse
bound is

\[
 \mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)
 \le\frac12\mathcal S_{N,R}^{K}(\mathcal D).
\]

Thus, for fixed \(N_0\) and fixed admissible \(\boldsymbol\lambda\),

\[
 \mathfrak R_{N_0,R}^{\boldsymbol\lambda}(\mathcal D)\lesssim A_R
 \quad\Longleftrightarrow\quad
 \mathcal S_{N_0,R}^{K}(\mathcal D)\lesssim A_R.
\]

This is a no-gain equivalence after deletion of known paid branches, not a
proof of either side.

For the plateau observable, R0.74Q/Step 9 gives

\[
 \mathfrak C_R^M
 \le B_{Q,R}^M+\sqrt N\,Z_R+\mathcal S_{N,R}^{K}(I_R).
\]

Substitution yields the exact bookkeeping

\[
 \mathfrak C_R^M
 \le\sqrt N\,Z_R+7B_{Q,R}^M
   +C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R
   +6\mathfrak R_{N,R}^{\boldsymbol\lambda}(I_R).
\]

The coefficient seven is six units from paid-branch deletion plus one unit
from the clock-to-flux reduction.  A quadratic residual bound on \(I_R\)
would already imply the plateau target (Q.1), but would not prove the stronger
full-domain Q.12.  A bound on \(\mathcal T_R\) would imply both.

Finally,

\[
 \mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)\le C_FP_R^M.
\]

Hence it is quadratically bounded when \(P_R^M\le1\), since then
\(P_R^M\le(P_R^M)^{2/3}=A_R\).  This gives no conclusion in the
large-payment regime.

## 10. Endpoint, measurability, and good-stop audit

All boundary assignments are exact and exhaustive:

- \(D_k(\tau)=T_k/2\) belongs to \(\mathcal I_D\);
- \(\beta_k(J_\tau)=T_k/6\) belongs to \(\mathcal I_\beta\);
- after failure of \(\mathcal I_\beta\), equality
  \(\sigma_k(J_\tau)=T_k/(12\lambda_k)\) fails the strict
  \(\sigma\)-test and belongs to \(\mathcal I_x\);
- \(d_k=\lambda_k^{-3/2}\) belongs to the long class;
- \(|\Delta Q_k|=T_k/6\) belongs to the paid \(Q\)-large side when
  that split is reached; and
- \(T_k=0\) belongs to none of the positive-terminal classes and has
  zero residual.

The open intervals \(J_k^{\rm LE}\) and \(J_\tau\) are Borel.  Endpoint
removal changes neither an absolutely continuous \(Q\)-variation integral nor
the time integral in (R.214).  A possible dissipation atom at \(\tau\) is not
silently inserted: the good-time clock identity and Step 8 both use the
inherited open-terminal convention.

For fixed \(\tau\), no joint measurability of \(k\mapsto J_k^{\rm pay}\) is
required; R.211 is stated for an arbitrary countable family of measurable
sets.  Likewise, a supremum over the good terminal set does not require the
moving residual map to be measurable in \(\tau\).

At a good terminal, \(\theta=2/3<3/4\) gives the strict Step 2 margin

\[
 K_k(\tau)-K_k(\ell_k)=T_k/3>T_k/4.
\]

For every finite positive-terminal shell family, density of the common good
set supplies good stops converging to the canonical last exits while
retaining this strict inequality.  This is only finite-family good-stop
closure.  It neither makes \(\ell_k\) good nor authorizes one infinite,
temporally discontinuous cutoff.

## 11. Equation-by-equation decision

| Main-note row | Independent result |
|---|---|
| (S.223) | **PASS** — existence, equality at exit, strict persistence, and \(\Delta F=T/3-\Delta Q\) |
| (S.224) | **PASS** — same fixed positive profile and correct \(\ell^3\) ledger |
| (S.225) | **PASS** — six pairwise-disjoint classes exhaust exactly the positive-terminal shells |
| (S.226) | **PASS** — \(\mathcal I_{\rm lo}\subset\mathcal I_\beta\cup\mathcal I_\sigma\); no extra paid class |
| (S.227) | **PASS** — disjoint shell indices cost one \(6B_Q\) ledger |
| (S.228) | **PASS** — a.e. non-\(D\) kinetic persistence; no value at the stop is used |
| (S.229) | **PASS** — \(C_{\rm LE}=6C_1^{2/3}\) and the \(\lambda_k\) exponent are correct |
| (S.230) | **PASS** — one shell-dependent R.211 application gives \(C_5=C_4C_P^{2/3}\) |
| (S.231) | **PASS** — \(C_{\rm pay}=6C_Q+C_5\mathscr L^{1/3}\) |
| (S.232) | **PASS** — residual is defined only on the two unpaid classes |
| (S.233) | **PASS** — strict \(T/6<r<T/2\), hence \(2r<T<6r\) |
| (S.234) | **PASS** — global nonnegativity, \(\ell^1\), \(\ell^2\), and linear fallback |
| (S.235) | **PASS** — valid for every single exceptional set \(S\) |
| (S.236) | **PASS** — the infimum is taken using the same residual-approximating sets |
| (S.237) | **PASS** — residual gate is correctly restricted to good terminals |
| (S.238) | **PASS** — only the left clock tail is extended by \(\ell^1\)-continuity |
| (S.239) | **PASS** — same-set monotonicity gives the factor \(1/2\) |
| (S.240) | **PASS** — exact fixed-profile, fixed-\(N_0\) equivalence modulo paid rows |
| (S.241) | **PASS** — plateau constant is \(7B_Q\), not \(6B_Q\) |
| (S.242) | **PASS** — linear fallback becomes quadratic only for \(P_R^M\le1\) |
| (S.243) | **OPEN, CORRECTLY LABELLED** — no uniform residual theorem is proved |
| (S.244) | **PASS AS ABSTRACT CLOCK STRESS** — constants six and one half are limiting-sharp |
| (S.245) | **PASS AS QUANTIFIER STRESS** — two residual branches share one exception budget |
| (S.246) | **PASS AS INFINITE-TAIL STRESS** — truncation-dependent exceptions are inadmissible |
| (S.247) | **PASS AS LOGICAL FALSIFIER** — terminal \(D\)-dominance does not localize to the last-exit interval |

## 12. Claim boundary and explicit nonclaims

The audit confirms as **PROVED** only:

- the six-class good-terminal partition;
- the Step 7/8 compatibility identity;
- one \(6B_Q\) payment and one \(C_5\mathscr L^{1/3}A_R\) payment;
- long non-\(D\) persistence;
- positivity and two-sided comparability of the selected residual;
- the fixed-good-terminal and domain-parametrized best-\(N\) reductions;
- the plateau corollary and the small-payment fallback; and
- the conditional implication from a future full-domain residual estimate to
  Q.12 and Q.1.

The audit confirms as **OPEN**:

- any solution- and scale-independent fixed \(N_0\) residual estimate;
- packing either the short non-\(D\), \(Q\)-small residual or the
  anomalous-defect/high-Rayleigh \(\mathcal I_x\) residual;
- Q.12, Q.1, scale contraction, prescribed-centre packing, and regularity.

The following are explicitly **NOT CLAIMED**:

- continuity, measurability, or lower semicontinuity of the last-exit map,
  branch masks, or residual path;
- that canonical last exits are good times;
- that an infinite last-exit family is one admissible local-energy test;
- that Step 8's full-history classes may be redefined on
  \(J_k^{\rm LE}\);
- that terminal \(D\)-dominance controls a \(D\)-increment or kinetic
  persistence on \(J_k^{\rm LE}\);
- that the \(\ell^2\) estimate closes a fixed-\(N\) \(\ell^1\) tail;
- equality between plateau and full terminal domains;
- optimization or adaptive choice of \(\boldsymbol\lambda\);
- that any scalar stress fixture is a Navier--Stokes solution; or
- novelty, priority, singularity formation, regularity, or a Millennium
  conclusion.

Subject to these boundaries, the locked Step 10 note is internally complete
and dependency-correct.  **NOT CLAY.**
