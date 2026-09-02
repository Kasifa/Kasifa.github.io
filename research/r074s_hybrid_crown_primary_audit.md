# R0.74S Step 15 — primary analytic audit of the hybrid and crown notes

## 0. Frozen objects and verdict

This audit binds the following two objects.

| Object | Equation range | SHA-256 |
|---|---:|---|
| `research/r074s_hybrid_flux_tail_equivalence.md` | (S.377)--(S.397) | `2e41f89e2ed13c09f64f09ace1b7884303e9add0b874e934ba210519b8a8ba5d` |
| `research/r074s_terminal_crown_coercivity.md` | (S.398)--(S.416) | `c62fc127c6d6381075653819a4672cae69f1ac4e2b7b45ee2d0b033ab770fd80` |

**Verdict: PASS within the stated exact, conditional, and abstract scopes.
The selected-crown estimate (S.407) and the temporal-tail estimate (S.342)
remain OPEN.  NOT CLAY.**

The audit supports five limited conclusions.

1. The short last-exit residual and the selected-excess residual are
   coordinatewise equivalent, up to literal constants, to one hybrid
   stopped-flux vector.  One common best-\(N\) deletion is retained.
2. The Step 13 full temporal flux tail controls the entire hybrid vector.
   Consequently, the still-open estimate (S.342) would close both residual
   branches with the same exception count.
3. Synchronizing short last-exit intervals creates the exact start-clock
   overshoot in (S.393)--(S.395).  Last-exit maximality does not pay it.
4. Finite-depth terminal crowns give a depth-independent cubic coefficient
   budget.  The resulting closure is conditional on the explicitly open
   nonlinear payment (S.407).
5. The converse-Hölder calculation is a formal nonnegative-ledger
   obstruction.  The periodic-measure tree and selected scalar clock are two
   separate stress tests, not one coupled fixture and not an NSE
   counterexample.

This audit does not prove (S.342), (S.407), (S.375), (S.288), (S.303),
(S.272), Step 10 (S.243), Q.12, Q.1, scale contraction, regularity,
singularity formation, or the Navier--Stokes Millennium problem.

## 1. Inherited source bindings

| Source | SHA-256 | Imported role |
|---|---|---|
| `research/r074s_defect_relaxed_total_rayleigh_excess.md` | `0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab` | Common zero start, selected-excess class, \(Q\)-variation, and \(x^{\rm sel}\le[F(\tau)]_+\). |
| `research/r074s_paid_branch_last_exit_residual.md` | `9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c` | Last \(2/3\)-exit, combined residual, best-\(N\) functional, and coefficient six in (S.238). |
| `research/r074s_shared_budget_terminal_trace_obstruction.md` | `fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693` | Selected-excess ancestry and the pure-defect scalar fixture (S.266). |
| `research/r074s_terminal_window_morrey_packing.md` | `03d1ae1fffd22d59ccb5bae7d860e3bd9bb9ab2f9e5dd7aafbee43b19153f84f` | Ancestor vector \(b\), moving tube, and open ancestor gate (S.288). |
| `research/r074s_temporal_integrability_morrey_threshold.md` | `d22a4e06b55325009b3d3930d0f8c0b96b4b4a7d3cdf1386a4158b0446e367de` | Dimensionless rate \(h\), common-deletion tail, and open estimate (S.342). |
| `research/r074s_outer_collar_corona_obstruction.md` | `c843284d68c0d7d441214b0b3e67e97ca4c5ebda5f527a957eb6e9bdc07f55f9` | Four-channel flux identity, lifted measure, density roots, relative jumps, incidences, and open lemma (S.375). |

The Step 15 notes do not change these definitions.  In particular,
\(A_R=(P_R^M)^{2/3}\), shell labels are physical annuli, the deletion count
is fixed independently of the solution and scale, and an optimizing shell
set may depend on the terminal only where the inherited best-\(N\)
definition permits it.

## 2. Hybrid stopped flux: (S.377)--(S.385)

### 2.1 Hybrid start and positivity: (S.377)--(S.379)

On the short branch, (S.377) starts at the canonical last exit \(\ell_k\),
so its increment is exactly the Step 10 residual.  On \(\mathcal I_x\), the
common initial good time satisfies \(F_k(\sigma_0)=0\), so the increment is
\(F_k(\tau)\).  Coordinates outside the disjoint residual union start at
\(\tau\) and vanish.  This proves (S.378), apart from positivity on
\(\mathcal I_x\), which follows from (S.380)--(S.381).

The Step 8 inequality \(x_k^{\rm sel}\le[F_k(\tau)]_+\), combined with this
positivity, proves (S.379).  The same \(\sigma_0\) is used for the whole
selected-excess branch.

### 2.2 One variation diamond and sharp constants: (S.380)--(S.382)

Put \(U=Q(\ell)\), \(V=Q(\tau)-Q(\ell)\).  Absolute continuity removes
endpoint atoms.  Since \(Q(\sigma_0)=0\),

\[
 |U|+|V|
 \le \operatorname{TV}_{(\sigma_0,\ell)}Q
    +\operatorname{TV}_{(\ell,\tau)}Q
 \le \operatorname{TV}_{J_\tau}Q<T/6.
\]

Thus (S.380) uses one full-history variation budget.  From \(K=Q+F\),
\(K(\ell)=2T/3\), and the common zero start,

\[
 z=T-U-V,\qquad r=T/3-V,
\]

which is (S.381).  It gives \(z>5T/6>0\).  Moreover,

\[
 5r-z=2T/3+U-4V,\qquad
 3z-7r=2T/3-3U+4V.
\]

Both are greater than \(2T/3-4(|U|+|V|)>0\).  Hence
\(z/5<r<3z/7\), with the directions and constants in (S.382) correct.

### 2.3 Common best-\(N\): (S.383)--(S.385)

On \(\mathcal R_{\rm sh}\), \(z=r\); on \(\mathcal I_x\), (S.382) holds;
all other coordinates vanish.  This proves (S.383).  Since \(z_k\le5r_k\),
the inherited \(r\in\ell^1_+\) also gives \(z\in\ell^1_+\).

For each one set \(S\subset\mathbb N\), \(\#S\le N\), summing outside that
same set and then optimizing proves (S.384).  Taking good-terminal suprema
afterward proves (S.385).  No union of branchwise exception sets occurs.

## 3. Temporal tail and conditional route: (S.386)--(S.391)

### 3.1 Exact time normalization: (S.386)--(S.387)

With \(t=s_R+R^2\sigma\),

\[
 \int_0^4 h_{k,R}(\sigma)\,d\sigma
 =\int_{s_R}^{t_0}|\dot F_{k,R}(t)|\,dt.
\]

There is no missing factor of \(R\).  Absolute continuity gives
\(0\le z_k\le\int_0^4h_k\), and Hölder on an interval of length four gives
\(\|h_k\|_1\le4^{1-1/p}\|h_k\|_p\), including the factor \(4\) for
\(p=\infty\).  Applying this outside one shell set and then taking the
infimum proves (S.387).  The deletion in
\(\mathfrak H^F_{p,N,R}\) is fixed before the time norm.

### 3.2 Open antecedent and coefficient six: (S.388)--(S.391)

Equation (S.388) restates the still-open quadratic tail estimate (S.342);
it is not supplied by fixed-solution \(L_t^{4/3}\) finiteness.  Combining it
with (S.387) proves (S.389) with the same \(N_F\).

Step 10 (S.238) has exact residual coefficient six:

\[
 \mathcal S^K_{N_F,R}(\mathcal T_R)
 \le C_{\rm pay}(\boldsymbol\lambda)A_R
    +6\mathfrak R_{N_F,R}^{\boldsymbol\lambda}(\mathcal T_R).
\]

Substitution yields exactly
\(C_{\rm pay}+6\,4^{1-1/p}C_H\), so (S.390) is correct.  Q.9 then gives
(S.391).  Its factor \(\sqrt{N_F}Y_{2,R}^{\rm sf}\) is absorbed because
\(N_F\) is fixed universally.  This is an implication, not a proof of
(S.388).

## 4. Signed channels and common-start debt: (S.392)--(S.397)

### 4.1 Four channels: (S.392)

The Step 14 identity
\(\dot F=\sum_{\alpha\in\{\rm cub,loc,har,dr\}}\dot F^\alpha\) integrates
on every hybrid active block.  Equation (S.392) restricts to a finite shell
set, so no countable interchange is assumed.  The regrouped total is exactly
the positive hybrid mass; algebraic regrouping alone is not an estimate.

### 4.2 Overshoot identity: (S.393)--(S.395)

For \(d_k\le\delta\),
\(\ell_k=\tau-d_kR^2\ge\max\{s_R,\tau-\delta R^2\}=a\).  Thus

\[
 r_k^{\rm sh}
 =F_k(\tau)-F_k(a)
  +K_k(a)-K_k(\ell_k)+Q_k(\ell_k)-Q_k(a),
\]

and \(K_k(\ell_k)=2T_k/3\), proving (S.393).  Summing over the same
complement of \(S\), replacing the signed common-window sum and clock term
by positive parts, and paying \(Q\) with global variation proves (S.394).

The countable passage is valid:

\[
 \sum_k|G_k|\le\sum_k\operatorname{TV}F_k<\infty,\qquad
 \omega_k\le K_k(a)+2T_k/3,
\]

and both clock vectors lie in \(\ell^1_+\).  Taking the infimum over that
same \(S\) proves (S.395).  Last-exit maximality applies after \(\ell_k\)
and supplies no bound on the earlier \(K_k(a)\).

### 4.3 Repaired scalar checks: (S.396)--(S.397)

The current (S.396) completes a continuous nondecreasing \(K\) by taking
pure defect \(D(t)=K(t)\), \(E=0\), and \(\sigma=0\).  Hence
\(K=E+D=Q+F\), \(D(\tau)=T=1\), and the row lies in \(\mathcal I_x\).
For \(U=0\) and \(V=1/6-\varepsilon\) or
\(V=-1/6+\varepsilon\),

\[
 {r\over z}
 ={1/6+\varepsilon\over5/6+\varepsilon}\to{1\over5},\qquad
 {r\over z}
 ={1/2-\varepsilon\over7/6-\varepsilon}\to{3\over7}.
\]

This repairs an earlier draft choice \(D=1/2,\sigma=0\), for which no
compatible continuous completed clock had been supplied.  The repaired
fixture proves scalar sharpness only.

For (S.397), \(G=3-M\), \(\omega=M-2\), and
\(G+\omega=1=r\).  A piecewise-linear descent from \(M\) to \(2\), followed
by a path strictly above \(2\), makes \(\ell\) the last level-\(2\) time.
This is an abstract debt check, not a short-branch NSE realization.

## 5. Ancestor ownership and crowns: (S.398)--(S.404)

### 5.1 Ancestor submeasure: (S.398)

The explicit \(\alpha^{\rm anc}_{k,\tau}\) contains the selected-shell
mask, pulled-back cutoffs, anomalous measure, and high-Rayleigh restriction
of the viscous measure.  Integrating gives the Step 12 coordinate \(b_k\).
Both cutoffs lie in \([0,1]\), so

\[
 0\le d\alpha^{\rm anc}_{k,\tau}
 \le\gamma_k\mathbf1_{\widehat{\mathcal U}_{k,R}(\tau)}d\nu_R.
\]

The \(R^{-1}\) normalization is in \(\nu_R\), and \(\gamma_k\) is explicit.
Thus equality, domination, and dimensions in (S.398) are correct.

### 5.2 Ownership and top content: (S.399)--(S.400)

A countable enumeration permits assignment to the first containing top;
half-open cells give Borel ownership sets.  The partition is separate for
each \(k\).  Top overlap does not duplicate one shell's ancestor mass, while
adjacent-shell incidence and deliberate repeated occurrence remain counted.
This verifies (S.399).

The general result assumes \(\mathscr C_{\rm top}<\infty\).  The displayed
\(O(2^{3k})\) count is used only for the bounded-overlap unit-radius
canonical cover, not for arbitrary small tops.  In that setting,

\[
 \mathscr C_{\rm top}
 \le C_{\rm geo}\sum_{k\ge1}2^{3k}\gamma_k<\infty.
\]

Shifted grids, lifted periodic portions, adjacent shells, and repeated top
labels remain in the incidence content.  Equation (S.400) is correct with
these stated hypotheses.

### 5.3 Roots and jumps: (S.401)--(S.402)

For \(m_T>0\), \(\lambda_T=m_T/\rho_T\) puts the top at equality, not above
the level.  First roots are disjoint and satisfy
\(m_S>\lambda_T\rho_S\).  Therefore

\[
 \sum_{S\in\mathscr R(T)}\rho_S
 \le m_T/\lambda_T=\rho_T,
\]

which is (S.401).  If \(m_T=0\), (S.398) shows that discarding the top loses
no ancestor mass.

Step 14 gives
\(\sum_{Q\in\mathscr J_\kappa(S)}\rho_Q\le\rho_S/\kappa\).
Recursive application on disjoint generations proves
\(\sum_{S\in\mathscr J_j(T)}\rho_S\le\kappa^{-j}\rho_T\) and the geometric
sum in (S.402).

### 5.4 Finite crowns and coefficient content: (S.403)--(S.404)

The top crown removes first roots.  Each nonterminal jump crown removes its
first jump descendants, and every depth-\(L\) node is retained whole.
Recursive substitution gives the exact disjoint partition (S.403).
Half-open cells handle boundary atoms.  Every infinite-jump remainder stays
inside the terminal-depth crown.

For one top--shell occurrence, the top crown contributes at most
\(\gamma_k\rho_T\), and generations zero through \(L\) contribute
\(\gamma_k\rho_T\sum_{j=0}^L\kappa^{-j}\).  Hence

\[
 C_{\kappa,L}
 =1+{\kappa\over\kappa-1}(1-\kappa^{-(L+1)})
 \le1+{\kappa\over\kappa-1}
 ={2\kappa-1\over\kappa-1}.
\]

Summing the full occurrence multiset proves (S.404), without a payment
estimate.

## 6. Conditional crown coercivity: (S.405)--(S.408)

Equation (S.405) fixes one exception set before any split.  The split is
formally available with \(q=0\).  On positive paid support, (S.406) gives

\[
 (p_{Sk}^{\rm crown})^2
 ={(a_{Sk}^{\rm pay})^3\over\gamma_k\rho_S},\qquad
 {(a_{Sk}^{\rm pay})^3\over(p_{Sk}^{\rm crown})^2}
 =\gamma_k\rho_S.
\]

The zero convention is correct.  The estimate

\[
 \sum p_{Sk}^{\rm crown}\le C_pP_R^M
 \tag{S.407}
\]

is **OPEN**.  It requires, for every solution, scale, and good terminal, an
admissible forest, one common exception set, a split, and finite depth, with
one universal \(C_p\).  The note does not derive it.

Conditional on (S.407), ownership and crowns give
\(\sum_{k\notin E_\tau}b_k=\sum a_{Sk}\).  Since

\[
 a_{Sk}^{\rm pay}
 =(\gamma_k\rho_S)^{1/3}(p_{Sk}^{\rm crown})^{2/3},
\]

Hölder, (S.404), and (S.407) yield

\[
 \sum a_{Sk}^{\rm pay}
 \le(C_\kappa\mathscr C_{\rm top})^{1/3}
      (C_pP_R^M)^{2/3}.
\]

Adding \(q\) and testing the same \(E_\tau\) proves (S.408).  Finite
truncation and monotone convergence justify countable incidences.

## 7. Converse Hölder and flat data: (S.409)--(S.412)

Hölder gives

\[
 \sum_i a_i
 \le\left(\sum_i{a_i^3\over p_i^2}\right)^{1/3}
       \left(\sum_i p_i\right)^{2/3}.
\]

Rearrangement proves (S.409).  The assignment
\(p_i=(P/A)a_i\), including zeros, gives equality.  Finite truncation and
monotone convergence prove the countable form.

With \(M=N_b+1\) coordinates \(b_{k_i}\ge H\), every \(N_b\)-deletion leaves
\(B_E\ge H\).  The constant \(C_M\) is fixed as \(H\to\infty\).  If
\(\sum q_k\le C_q(C_MH)^{2/3}\) and
\(H\ge(2C_qC_M^{2/3})^3\), then \(\sum q_k\le H/2\), so incidence mass is
at least \(H/2\).  If \(\sum p_i\le C_pC_MH\), then

\[
 \sum_i{a_i^3\over p_i^2}
 \ge{(H/2)^3\over(C_pC_MH)^2}
 ={H\over8C_p^2C_M^2},
\]

which verifies (S.411).  Conversely, a fixed coefficient bound
\(C_{\rm cor}\) gives incidence mass at most
\(C_{\rm cor}^{1/3}(C_pC_MH)^{2/3}\), and hence (S.412).  Forest, levels,
depth, assignments, and the one common exception set may be adaptive; every
repeated use must repeat payment.

## 8. Two separate stress tests: (S.413)--(S.416)

### 8.1 Periodic measure: (S.413)--(S.414)

For fixed \(R,M\), and selected indices, (S.413) is positive, periodic, and
locally finite.  A target cube has mass \(H/\gamma_{k_i}\), so shell
weighting gives \(H\).  The temporal atom chooses one of four half-open time
children and uniform spatial density gives one eighth of the mass to each
of eight spatial children.  Thus

\[
 \rho_v=2^{-d}\rho_0,\qquad
 m_v=8^{-d}m_0,\qquad
 \Theta(v)=4^{-d}\Theta(0),
\]

which proves (S.414) and excludes upward \(\kappa\)-jumps.

The period-copy count is \(O_R(1+2^{3k}R^3)\), and
\(\sum_k\gamma_k(1+2^{3k}R^3)<\infty\).  Periodic copies are therefore
counted rather than discarded.  This is a geometric screen only.

### 8.2 Scalar clock: (S.415)--(S.416)

Scaling Step 11 (S.266) by \(5H/3\) gives

\[
 r^x={5H\over9},\qquad
 \sigma={959H\over7200}<{1000H\over7200}={T\over12},
\]

and

\[
 x={2641H\over3600}>{1000H\over3600}={T\over6}.
\]

Also \(b=m=H\), \(\beta=0\).  Thus (S.415) is correct.  With
\(M=N_b+1\), one common deletion leaves one \(H\)-coordinate and

\[
 {\mathcal S_{N_b}(b)\over A_H}
 \ge {H\over(C_MH)^{2/3}}
 =C_M^{-2/3}H^{1/3}\to\infty,
\]

which proves (S.416) as a scalar screen.

An earlier draft blurred this fixture with the Dirac-in-time periodic
measure.  The current note explicitly repairs that error:
(S.413)--(S.414) and (S.415)--(S.416) are separate checks and do not satisfy
one common completed-clock/measure identity.  Enlarging \(C_M\) to dominate
their separate constants is only a comparison convention.  The formal
obstruction is (S.409)--(S.412), independently of these screens.

## 9. Equation-by-equation verdict matrix

| Equation | Verdict | Audited content |
|---|---|---|
| (S.377) | PASS | Branch-correct hybrid starts. |
| (S.378) | PASS | Exact short equality, positive selected terminal flux, zero complement. |
| (S.379) | PASS | Inherited selected excess is below \(z\). |
| (S.380) | PASS | One additive full-history \(Q\)-variation budget. |
| (S.381) | PASS | Exact clock identities. |
| (S.382) | PASS | Strict \(1/5\) and \(3/7\) constants. |
| (S.383) | PASS | Coordinate comparison and \(\ell^1\) membership. |
| (S.384) | PASS | One common best-\(N\) deletion. |
| (S.385) | PASS | Correct terminal-supremum order. |
| (S.386) | PASS | Correct \(R^2\) normalization and \(p=\infty\) factor. |
| (S.387) | PASS | Same \(N\) pays both branches. |
| (S.388) | OPEN ANTECEDENT | Restatement of (S.342), not a theorem. |
| (S.389) | PASS CONDITIONAL | Same \(N_F\). |
| (S.390) | PASS CONDITIONAL | Exact coefficient \(C_{\rm pay}+6\,4^{1-1/p}C_H\). |
| (S.391) | PASS CONDITIONAL | Q.1 follows only under (S.388). |
| (S.392) | PASS | Finite-shell four-channel integration. |
| (S.393) | PASS | Exact common-start identity. |
| (S.394) | PASS | Correct signs, \(Q\)-payment, and series passage. |
| (S.395) | PASS | Same deletion pays cancellation and overshoot. |
| (S.396) | PASS, REPAIRED | Pure-defect completion and sharp scalar limits. |
| (S.397) | PASS AS ABSTRACT CHECK | Start debt is algebraically necessary. |
| (S.398) | PASS | Explicit ancestor submeasure and dimensions. |
| (S.399) | PASS | Shellwise Borel ownership. |
| (S.400) | PASS | Honest incidence-weighted top content. |
| (S.401) | PASS | First-root radius sum. |
| (S.402) | PASS | Relative-jump geometric decay. |
| (S.403) | PASS | Exact finite-depth crown partition. |
| (S.404) | PASS | Exact depth-independent \(C_\kappa\). |
| (S.405) | PASS AS SPLIT | One exception set; \(q=0\) formally allowed. |
| (S.406) | PASS | Exact canonical factorization. |
| (S.407) | OPEN PDE INPUT | No crown \(3/2\)-coercivity theorem is proved. |
| (S.408) | PASS CONDITIONAL | Hölder closure under (S.407). |
| (S.409) | PASS | Countable converse Hölder and equality case. |
| (S.410) | PASS AS FORMAL DATA | \(N_b+1\) positive coordinates. |
| (S.411) | PASS | Threshold and lower-bound constants exact. |
| (S.412) | PASS | Correct fixed-coefficient tradeoff. |
| (S.413) | PASS AS GEOMETRIC SCREEN | Periodic copies explicit and locally finite. |
| (S.414) | PASS AS GEOMETRIC SCREEN | \(2^{-d},8^{-d},4^{-d}\) scaling. |
| (S.415) | PASS AS SCALAR SCREEN | Scaled rational constants correct. |
| (S.416) | PASS AS SCALAR SCREEN | Best-\(N_b\) ratio grows as \(H^{1/3}\). |

## 10. Claim boundary

The following are **PROVED** at the audited hashes:

- the hybrid identities, sharp scalar comparison, and exact common-deletion
  equivalence (S.377)--(S.385);
- the temporal-tail implication (S.386)--(S.391), conditional on its open
  antecedent;
- the signed common-window identity and debt (S.392)--(S.395);
- the repaired scalar screens (S.396)--(S.397);
- the ancestor submeasure, ownership, roots, jumps, and crowns
  (S.398)--(S.404);
- the crown factorization and conditional closure (S.405)--(S.408);
- the formal converse-Hölder obstruction (S.409)--(S.412); and
- the separate geometric and scalar calculations (S.413)--(S.416), only in
  their explicitly uncoupled scopes.

The following remain **OPEN**:

- the common-deletion temporal flux estimate (S.342), restated as (S.388);
- the selected-crown nonlinear payment (S.407);
- (S.375), (S.288), (S.303), (S.272), and Step 10 (S.243);
- a coupled completed-clock/measure realization of the two stress tests;
- Q.12, Q.1, scale contraction, regularity, singularity formation, and the
  Navier--Stokes Millennium problem.

The two material draft defects found during adversarial review are closed at
the audited hashes: (S.396) now has a consistent pure-defect completion, and
the two crown stress tests are explicitly uncoupled.  No remaining
algebraic, dimensional, common-deletion, ownership, periodic-copy, or
finite-depth remainder error was found.

**Primary analytic audit: PASS within scope.  S.342 OPEN.  S.407 OPEN.
NOT CLAY.**
