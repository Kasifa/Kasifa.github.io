# R0.74S Step 12 — primary audit of terminal windows and Morrey packing

## 1. Verdict and locked source

**PASS ON THE LOCKED SOURCE, WITH THE UNIVERSAL PDE GATES LEFT OPEN.**

The audited source is

research/r074s_terminal_window_morrey_packing.md

with SHA-256

03d1ae1fffd22d59ccb5bae7d860e3bd9bb9ab2f9e5dd7aafbee43b19153f84f.

The audit backtracks all thirty-four statements (S.273)--(S.306).  The
terminal-window reduction, continuity statement, layer-cake identity,
averaged-terminal exponent, exception accounting, conditional moving-tube
theorem, mixed-norm benchmark, and single-packet kinematic screen pass in
their stated scopes.

The audit does not prove the universal window estimate (S.280), the
universal ancestor estimate (S.288), their conjunction (S.303), Step 11
(S.272), Q.12, Q.1, scale contraction, or regularity.  The Morrey and
mixed-norm conclusions require their displayed uniform bounds.  The
literature search is bounded and is not a novelty opinion.  **NOT CLAY.**

## 2. Frozen-source backtracking

| Input | SHA-256 | Use in Step 12 | Decision |
|---|---|---|---|
| R0.74P temporal observable | a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867 | Canonical clocks, absolute flux variation, total dissipation measure, moving cutoffs | **PASS / INHERITED** |
| R0.74R arbitrary-clock gate | ac959f30b254001910e5b445264ea7c0d8714afc2f96dcf74505f5e1f794b6b7 | Shell-dependent cubic payment and support geometry | **PASS / INHERITED** |
| R0.74R persistent-lobe theorem | e7f151048e85d95133f8c6414849c0fe9dc40cc48b7a12666b7e21496ddb99b5 | Terminal-lobe payment boundary | **PASS / DESIGN-SPECIFIC** |
| R0.74S Step 8 | 0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab | Defect/high-Rayleigh ancestry and linear excess payment | **PASS / INHERITED** |
| R0.74S Step 11 | fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693 | Residual split and positive-depth estimate (S.259) | **PASS / BRANCH GATES OPEN** |
| R0.74F packet survival | 0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb | Exact packet-centre formula and speed bound | **PASS / EXACT FAMILY** |

The fixed shell weights and cutoff constants may enter constants, but none
of them depends on the solution, scale, or terminal time.

## 3. Equation audit

| Equations | Direct check | Decision |
|---|---|---|
| (S.273)--(S.275) | If (d_k\le\delta), the last-exit interval lies in the common terminal window.  The complementary (d_k>\delta) indices are controlled by Step 11 (S.259) after deleting the same shell set. | **PASS** |
| (S.276)--(S.277) | Window symmetric differences tend to zero against (g_R\in L^1); best-(N) deletion is 1-Lipschitz on (ell^1).  Uniform absolute continuity is asserted only for fixed ((u,R)). | **PASS / NONUNIFORM MODULUS** |
| (S.278)--(S.280) | Deleting the (N) largest coordinates gives the exact integrated distribution formula.  The all-threshold hypothesis is sufficient; the universal hypothesis itself remains explicit. | **PASS AS REDUCTION / OPEN INPUT** |
| (S.281) | (N+1) synchronized AC spikes have total variation ((N+1)H), best-(N) window tail (H), and ratio (H^{1/3}/(N+1)^{2/3}\to\infty). | **PASS / ABSTRACT LEDGER TEST** |
| (S.282)--(S.284) | Fubini supplies the factor (delta R^2); Markov removes at most (eta R^2) of terminal times.  Interior optimization gives the stated (P^{4/5}) exponent and retains the condition (delta\in(0,4)). | **PASS / AVERAGED TERMINALS ONLY** |
| (S.285)--(S.288) | The defect and high-Rayleigh ancestors may overlap, so their deletion sets are unioned and their budgets add.  Holder with exponents (3) and (3/2) proves the displayed sufficient charging lemma. | **PASS AS IMPLICATION / PDE CONSTRUCTION OPEN** |
| (S.289)--(S.294) | Time/arc-length stopping gives (C(1+L2^{-k})) pieces; each needs (C2^{3k}) radius-(R) spatial balls.  Exact decomposition (mu=|\nabla u|^2dxdt+D) prevents a duplicated measure factor. | **PASS / CONDITIONAL MORREY THEOREM** |
| (S.295)--(S.300) | Periodic Calderon--Zygmund is used only for finite (r).  Every localized energy term has one final power of (R), and the normalized path exponent is zero. | **PASS / CONDITIONAL MIXED-NORM BENCHMARK** |
| (S.301)--(S.302) | A finite atomic support has zero parabolic one-dimensional Hausdorff measure without a mass-packing bound.  High-Rayleigh viscous mass need not lie in the singular set. | **PASS / LOGICAL COUNTERMODELS ONLY** |
| (S.303) | The common-window supremum is over all terminals by continuity; the ancestor vector remains restricted to local-energy good terminals. | **PASS AS COMBINED TARGET / OPEN** |
| (S.304)--(S.305) | The exact packet speed yields less than one physical winding.  Monotone change of variables bounds periodic occupation by complete-period counts. | **PASS / KINEMATIC** |
| (S.306) | After deleting indices (0,\ldots,N-1), consecutive majorants have ratio at most (q_N<1), so their tail is geometric. | **PASS / ABSTRACT SEQUENCE FILTER** |

The equation tags are consecutive and unique.  Display delimiters balance,
the main note contains no control characters, and all three universal
claims remain marked **OPEN**.

## 4. Common-window and layer-cake reconstruction

For every retained short coordinate with (d_k\le\delta),

\[
 \ell_k=\tau-d_kR^2\ge\tau-\delta R^2,
 \qquad
 r_k^{\rm sh}
 \le\int_{J_{\tau,\delta}}|\dot F_{k,R}|.
\]

For an arbitrary deletion set (S), this controls the shallow indices.
The positive-depth theorem controls the complementary indices using the
same (S).  Taking the infimum only after the two estimates are added is
why (S.275) has no hidden second exception budget.

For (z\in\ell^1_+), let (z_1^*\ge z_2^*\ge\cdots) be the decreasing
rearrangement.  Then

\[
 \int_0^\infty(n_z(t)-N)_+\,dt
 =\sum_{j>N}\int_0^{z_j^*}dt
 =\sum_{j>N}z_j^*
 =\mathcal S_N(z).
\]

This reconstruction also shows why one count at one amplitude cannot close
the estimate.  A bound proportional to (1/t) has a logarithmically
divergent integral unless another endpoint improvement is available.

## 5. Fixed-solution continuity versus a universal modulus

For fixed ((u,R)), every terminal window has length at most
(delta R^2).  Uniform absolute continuity of the integral of (g_R)
therefore proves

\[
 \sup_\tau\sum_k\int_{J_{\tau,\delta}}|\dot F_{k,R}|
 \longrightarrow0.
\]

This statement cannot be made uniform from the scalar (L_t^1) ledger.
The synchronized-spike family places the same height (H) in (N+1)
coordinates inside one terminal window.  It satisfies every abstract AC and
total-mass premise used in that attempted implication, while the normalized
best-(N) tail diverges.  The witness is not an NSE trajectory and is not
used as one.

The averaged-terminal route reaches

\[
 \eta^{-1}\delta P+\delta^{-2/3}P^{2/3}.
\]

Balancing the terms at an admissible interior (delta) gives
(eta^{-2/5}P^{4/5}), not the required (P^{2/3}).  This is an exact
method boundary, not a sharpness claim for NSE.

## 6. Conditional moving-tube theorem

The tube is divided when either elapsed time reaches (O(R^2)) or lifted
path variation reaches (O(2^kR)).  The number of pieces is

\[
 C(1+L2^{-k}).
\]

On one piece the padded shell stays in a ball of radius (C2^kR), which
requires at most (C2^{3k}) balls of radius (R).  A fixed number of
backward time slabs then gives

\[
 C(1+L2^{-k})2^{3k}
 =C(2^{3k}+L2^{2k}).
\]

The defect term and the restricted viscous term are two restrictions of
the exact nonnegative decomposition

\[
 d\mu=|\nabla u|^2dxdt+dD.
\]

Their sum is therefore bounded by one copy of the tube's total measure.
After multiplication by (gamma_k/R) and summation, the super-Gaussian
weights pay both cover powers.  This proves the finite cap
(B(M,L)).  Combining it with the inherited linear cap gives

\[
 \min\{C_0P,B(M,L)\}
 \le\max\{C_0,B(M,L)\}P^{2/3}.
\]

The last inequality uses (P\le P^{2/3}) for (P\le1), and
(1\le P^{2/3}) for (P\ge1).  It is uniform only when (M,L) are common
to the entire restricted class.

## 7. Mixed-norm scale audit

Let (	heta=3/r+2/q) and
(|u|_{L_t^qL_x^r}\le M_*R^{\theta-1}).  Before inserting this bound,
the three local-energy terms have powers

\[
 R^{3-2\theta}|u|^2,
 \qquad
 R^{4-3\theta}|u|^3,
 \qquad
 R^{4-3\theta}|p-\bar p|,|u|.
\]

The pressure bound contributes
(|p-\bar p|\le C|u|^2).  Substitution gives respectively
(RM_*^2), (RM_*^3), and (RM_*^3).  The path exponent is

\[
 -1-{3\over r}+2-{2\over q}+\theta-1=0.
\]

The proof allows (q=\infty) with (1/q=0), but excludes (r=\infty):
the displayed Calderon--Zygmund step has no (L^\infty\)-to-(L^\infty)
endpoint.

## 8. Single-packet kinematic audit

The R0.74F bounds give

\[
 \operatorname {Var}_{[0,65R^2]}Q
 \le {65R^2\over32R^2}={65\over32}<2\pi,
 \qquad
 \operatorname {Var}_{I_{2R}}Q
 \le {4R^2\over32R^2}={1\over8}.
\]

For a hypothetical monotone extension, the change of variables
(s=q(t)) gives (1/B\le dt/ds\le1/(\beta B)).  An interval of
(s)-length (D=2\pi m+r), (0\le r<2\pi), contains (m) complete
periods and one remainder.  Its periodic (J)-occupation therefore lies
between (m|J|) and ((m+1)|J|), which proves (S.305).

For the discrete filter, put
(a_\ell=H2^{p\ell}\Gamma^{4^\ell}).  Then

\[
 {a_{\ell+1}\over a_\ell}
 =2^p\Gamma^{3\cdot4^\ell}\le q_N
 \quad(\ell\ge N).
\]

The geometric tail proves (S.306).  Occupation changes a common scale but
does not reverse the super-Gaussian shell ratio.  This screens uniform
speed-up of one rigid packet.  It does not identify earlier deposited
dissipation with the complete ancestor vector and is not a PDE no-go.

## 9. Literature boundary

The bounded primary-source review distinguishes four different statements:
singular-set dimension, anomalous-dissipation support under extra
integrability, terminal singular-point counts under Type-I control, and
critical Morrey regularity assumptions.  None of the inspected statements
has the bare quantifiers and full-history prescribed-centre annular
observable of (S.280) or (S.288).

This comparison supports only the stated boundary.  It neither proves that
no such theorem exists nor establishes priority for the present reduction.

## 10. Final scope

**PROVED:** the common-window reduction; terminal continuity; exact
best-(N) layer cake; fixed-solution modulus; abstract (L_t^1) no-go;
averaged (P^{4/5}) boundary; exception-budget algebra; conditional Morrey
packing; mixed-norm sufficient benchmark; literal no-winding; monotone
occupation; and the abstract super-Gaussian tail.

**INHERITED:** suitable-weak clock construction, absolute ledgers, the
positive-depth estimate, ancestor domination, shell-dependent cubic
payment, and the R0.74F/R exact-family bounds.

**OPEN:** (S.280), (S.288), (S.303), Step 11 (S.272), Q.12, Q.1, a
uniform critical Morrey/path coefficient derived from the frozen payment,
deposited-tube identification, a universal fixed shell count, scale
contraction, and regularity.

**NOT CLAIMED:** NSE realizability of the abstract spikes or atomic
measure; an (r=\infty) pressure endpoint; exhaustiveness of the
literature search; novelty; or a solution of the Millennium problem.

**NOT CLAY.**
