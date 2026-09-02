# R0.74S Step 8 — independent defect-relaxed Rayleigh-excess audit

## 1. Independent verdict

**PASS.** On the frozen source bytes, the Step 8 measure construction,
priority trichotomy, kinetic payment, endpoint lower-semicontinuity argument,
smooth formula, and stopped-work bridge are mathematically consistent in
their stated fixed-scale Version-M scope.

The independently audited source is
research/r074s_defect_relaxed_total_rayleigh_excess.md, SHA-256
0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab.
All tags (S.163)--(S.199) occur exactly once and in order. The strict and
weak threshold choices, the distinction \(x\le X\), the powers of \(R\),
\(\gamma_k\), and \(\lambda_k\), and the open-terminal convention all pass.

The most important independent check is the terminal-clock reduction. The
scalar excess is not a new uncontrolled channel: it obeys
\(x_k(\tau)\le[F_k(\tau)]_+\), its global sum is bounded linearly by the
inherited absolute flux ledger, and it is a subledger of the existing Step 2
stopped-work gate. On the priority residual class the stronger estimate is
\(F_k(\tau)>5K_k(\tau)/6\), hence \(K_k(\tau)<6F_k(\tau)/5\). The Jordan
envelope \(X\) has fixed-scale finiteness but does not inherit this terminal
flux bound.

This closes an accounting question and also eliminates one proposed target.
The Step 2 supremum already permits the common initial zero stops used here,
so it differs from the full terminal ℓ1 clock, and from the full-cutoff
positive cumulative flux, only by the already-paid (Q)-variation. The
R0.74O/P exact family therefore refutes a universal no-exception quadratic
bound for that supremum. The conditional implication (S.38) remains valid;
its antecedent is not universally true. This audit does not
re-prove the inherited suitable-weak local-energy theory, R0.74P compactness,
(R.211), or (R.214), and it is not a novelty or priority opinion. The
fixed best-(N) exception gate, (Q.1), regularity, and the Millennium
problem remain open. **NOT CLAY.**

## 2. Independent analytic reconstruction

### 2.1 Scalar mass and Jordan local mass

On \(J_\tau=(s_R,\tau)\), write

\[
 \alpha=\nu-\beta-2\lambda_k\sigma,
 \qquad x=[\alpha(J_\tau)]_+,
 \qquad X=\alpha^+(J_\tau).
\]

The Jordan variational identity

\[
 \alpha^+(J_\tau)
 =\sup_{A\subset J_\tau}\alpha(A)
 =\sup_{\substack{\phi\in C_c(J_\tau)\\0\le\phi\le1}}
       \int\phi\,d\alpha
\]

holds for a finite signed Radon measure on this open interval. The first
supremum follows from a Hahn positive set. The second follows by inner
regularity of \(\alpha^+\), outer regularity of \(\alpha^-\), and a
compactly supported Urysohn cutoff. It detects interior atoms and gives

\[
 0\le x\le X,
 \qquad
 \nu(J_\tau)\le\beta(J_\tau)+2\lambda_k\sigma(J_\tau)+x.
\]

Cancellation can make \(x=0<X\): equal positive and negative masses on two
disjoint time regions are the simplest witness. Thus every use of \(x\) as
the sharper terminal quantity and \(X\) as the stronger local envelope has
the correct order.

There is also a useful measure order. Since
\(\alpha=\nu-(\beta+2\lambda_k\sigma)\le\nu\) and \(\nu\ge0\),
\(\alpha^+\le\nu\). Consequently

\[
 \sum_kX_{k,R}(\tau)
 \le {1\over R}\int_{J_\tau\times\mathbb T^3}
       \eta_R\Theta_R(x-X_R(t))\,d\boldsymbol\mu<\infty.
\]

The last inequality is fixed-scale only: \(\Theta_R\) is the inherited
\(C^2\)-convergent nonnegative shell weight, and the time support is
compactly contained because \(\eta_R\) vanishes near \(s_R\) and
\(\tau<t_0\).

### 2.2 The one-sixth priority split

For a dissipation-dominated shell put \(T=K_k(\tau)>0\) and
\(y=2\lambda_k\sigma_k(J_\tau)\). Since
\(\nu_k(J_\tau)=D_k(\tau)\ge T/2\), the exact scalar definition gives

\[
 \beta_k+y+x_k\ge\nu_k(J_\tau)\ge {T\over2}.
\]

The priority order is therefore

\[
 \beta_k\ge {T\over6},
 \quad\hbox{else }y>{T\over6},
 \quad\hbox{else }x_k>{T\over6}.
\]

The middle test is exactly
\(\sigma_k(J_\tau)>T/(12\lambda_k)\). If its strict inequality fails,
\(y\le T/6\); failure of the first test is strict, so the last conclusion is
also strict. The three classes are disjoint and exhaustive.

Among three nonnegative contributions known only to sum to at least \(T/2\),
\(T/6\) is the largest common guaranteed share: a larger common threshold is
impossible, while \(T/6+T/6+T/6=T/2\) reaches the boundary. This is the
precise maximin sense in which the displayed
\(\beta\to\sigma\to x\) constants are optimized; it is not an optimization
over all possible analytic decompositions.

### 2.3 Jensen and the shell coefficient

Let \(\delta_\tau=|J_\tau|/R^2\), so \(0<\delta_\tau<4\). With
\(\sigma_k=R^{-2}\int_{J_\tau}e_k\), Hölder gives

\[
 {1\over R^2}\int_{J_\tau}e_k^{3/2}
 \ge\delta_\tau^{-1/2}\sigma_k^{3/2}
 >{1\over2}\left({T\over12\lambda_k}\right)^{3/2}.
\]

Combining this with inherited (R.214),

\[
 {1\over R^2}\int e_k^{3/2}
 \le C_1 2^{3k/2}\gamma_k^{1/2}p_k^\tau,
\]

and raising to power \(2/3\) gives exactly

\[
 T\le12(2C_1)^{2/3}\lambda_k2^k\gamma_k^{1/3}
       (p_k^\tau)^{2/3}.
\]

There is no missing power of \(R\). Hölder across shells uses exponents
\(3\) and \(3/2\), cubes the coefficient, and produces

\[
 \sum_k2^{3k}\gamma_k\lambda_k^3.
\]

The inherited selected-payment estimate (R.211) then proves (S.176) by a
finite-shell argument followed by monotone convergence.

### 2.4 Selected and global terminal ledgers

On the first priority branch \(T_k\le6\beta_k(J_\tau)\), while on the third
branch \(T_k<6x_k(\tau)\). Summing those relations together with the kinetic
payment gives (S.178). Replacing the selected scalar sum first by
\(\sum_kx_k\) and then by \(\sum_kX_k\) preserves the inequality because

\[
 \sum_{k\in\mathcal I_x}x_k\le\sum_kx_k\le\sum_kX_k.
\]

These replacements are weaker but use fixed index sets. They do not imply
that the moving selected sum is lower semicontinuous.

For comparison with Step 7, on the low-Rayleigh set
\(g-2\lambda_kR^{-2}e\le0\); on its complement, the positive part is no
larger than \(g\). Subtracting \(\beta\ge0\) can only reduce positive mass,
so

\[
 x_k\le X_k\le m_k+\int_{H_k}g_k.
\]

This is a shellwise domination by the raw Step 7 residual. It does not
compare the two differently prioritized all-shell sums.

### 2.5 Endpoint-safe lower semicontinuity

Under the frozen R0.74P topology, fixed-shell path convergence and strong
\(L^3\) convergence give strong \(L^1_t\) convergence of both \(e_k\) and
the explicit quadratic density \(\dot Q_k\). Hence
\(\sigma_k^{(n)}\) and \(\beta_k^{(n)}=|\dot Q_k^{(n)}|dt\) converge in
total variation. The total dissipation measures give only local weak-*
convergence \(\nu_k^{(n)}\rightharpoonup^*\nu_k\).

The target interval is open at \(\tau\). Because all three weighted measures
vanish on one common neighborhood of \(s_R\), it can be replaced by a
relatively compact open interval before applying Portmanteau. Therefore

\[
 \nu_k(J_\tau)\le\liminf_n\nu_k^{(n)}(J_\tau).
\]

Subtracting the two convergent nonnegative masses and applying the monotone
continuous map \(z\mapsto[z]_+\) proves lower semicontinuity of \(x_k\).
For \(X_k\), fix one \(\phi\in C_c(J_\tau)\), pass its signed integral to
the limit, and then take the supremum in the Jordan variational formula.
A finite-shell Fatou argument and monotone convergence give both global
statements.

The direction is sharp. If \(a_n\uparrow\tau\), then
\(\delta_{a_n}\rightharpoonup^*\delta_\tau\) in the ambient interval, but
the limiting mass of \(J_\tau\) is zero while every approximating mass is
one. Uniform convergence of primitives is also insufficient for \(\beta\):
\(n^{-1}\sin(nt)\to0\) uniformly although \(|\cos(nt)|\) does not converge
to zero in \(L^1\).

### 2.6 Smooth formula and approximation boundary

For a smooth solution the anomalous defect vanishes and all three measures
are absolutely continuous. Thus

\[
 \begin{aligned}
 x_k(\tau)
 &=\left[\int_{s_R}^{\tau}
   \left(g_k-|\dot Q_k|-{2\lambda_k\over R^2}e_k\right)dt\right]_+,\\
 X_k(\tau)
 &=\int_{s_R}^{\tau}
   \left[g_k-|\dot Q_k|-{2\lambda_k\over R^2}e_k\right]_+dt.
 \end{aligned}
\]

These are, respectively, positive part after integration and integration of
the positive part. Passing them through the preceding liminf inequalities is
valid if a smooth Navier--Stokes sequence satisfying the stated R0.74P
topology is supplied. Nothing here constructs such an approximation.

### 2.7 Exact shear boundary

For the inherited heat shear, \(F_k=0\) and \(K_k=Q_k\), with zero initial
primitives. If \(T_k=K_k(\tau)>0\), then

\[
 D_k(\tau)\le T_k=Q_k(\tau)
 \le\operatorname {TV}_{J_\tau}Q_k=\beta_k(J_\tau),
\]

so \(x_k=0\) and the shell enters the \(\beta\)-priority branch. This proves
neither that the local Jordan mass \(X_k\) vanishes nor that high pointwise
Rayleigh ratio is impossible. A two-cell scalar witness with signed excess
\((2,-3)\) has \(x=0<X=2\), illustrating why terminal totals alone cannot
settle \(X\).

### 2.8 Terminal physical flux and stopped work

Absolute continuity and the zero initial primitive give

\[
 \beta_k(J_\tau)\ge|Q_k(\tau)|.
\]

At a good time, \(D_k=K_k-E_k=Q_k+F_k-E_k\). Hence

\[
 \alpha_k(J_\tau)
 =(Q_k-\beta_k)+F_k-E_k-2\lambda_k\sigma_k
 \le F_k-E_k-2\lambda_k\sigma_k\le F_k,
\]

and consequently

\[
 x_k(\tau)\le[F_k(\tau)]_+,
 \qquad
 \mathfrak x_{1,R}(\tau)
 \le\sum_k\operatorname {TV}F_k\le CP_R^M.
\]

The countable intersection of shellwise local-energy good-time sets has full
measure. Choose one such \(\sigma_0\) in the common initial interval where
\(\eta_R=\eta_R'=0\). Then all \(K_k,Q_k,F_k\) vanish at \(\sigma_0\).
If \(x_k(\tau)>0\), then \(D_k(\tau)>0\) and \(K_k(\tau)>0\), so this stop
satisfies (S.25). For every finite nonempty subset \(G\) of the positive-
\(x\) shells,

\[
 W_R^M(\tau;G,(\sigma_0)_{k\in G})
 =\sum_{k\in G}F_k(\tau)
 \ge\sum_{k\in G}x_k(\tau)>0.
\]

Taking the supremum over finite \(G\) gives
\(\mathfrak x_{1,R}(\tau)\le\mathfrak W_{{\rm up},R}^M\).

Finally, if \(k\in\mathcal I_x\), failure of the first priority test gives

\[
 |Q_k(\tau)|\le\beta_k(J_\tau)<{T_k\over6}.
\]

Because \(T_k=Q_k(\tau)+F_k(\tau)\),

\[
 F_k(\tau)\ge T_k-|Q_k(\tau)|>{5T_k\over6},
 \qquad T_k<{6\over5}F_k(\tau).
\]

The same finite-first stopped-work argument proves (S.196). This is an exact
bridge to Step 2, but not a smaller gate: (S.37) already ranges over all good
stops satisfying (S.25), including the common zero-start family.

### 2.9 The no-exception gate is equivalent to the full terminal ledger

Set

\[
 B_Q=\sum_k\operatorname {TV}Q_k,\qquad
 \mathcal K=\sup_{\tau\in\mathcal G_R}\sum_kK_k(\tau),\qquad
 \mathfrak C_{\rm full}
 =\sup_{s_R<\tau<t_0}\left[\sum_kF_k(\tau)\right]_+.
\]

For any stopped family \((\tau,I,\boldsymbol\sigma)\),

\[
 \begin{aligned}
 W-\sum_kF_k(\tau)
 &=-\sum_{k\in I}F_k(\sigma_k)
   -\sum_{k\notin I}F_k(\tau)\\
 &=\sum_{k\in I}\bigl(Q_k(\sigma_k)-K_k(\sigma_k)\bigr)
   +\sum_{k\notin I}\bigl(Q_k(\tau)-K_k(\tau)\bigr)\\
 &\le\sum_{k\in I}\operatorname {TV}Q_k
   +\sum_{k\notin I}\operatorname {TV}Q_k=B_Q.
 \end{aligned}
\]

The partition of shells is essential: it spends every \(Q\)-variation row
at most once. Therefore \(W_{\rm up}\le\mathfrak C_{\rm full}+B_Q\), not
merely the weaker bound with \(2B_Q\).

Conversely, at a good terminal time use the common zero stop on finite
subsets of shells with \(K_k(\tau)>0\) and \(F_k(\tau)>0\). Positive flux
on an omitted zero-clock shell satisfies \(F_k=-Q_k\le\operatorname {TV}Q_k\).
Finite approximation, followed by uniform convergence and density of the
common good-time set, gives

\[
 \mathfrak C_{\rm full}\le W_{\rm up}+B_Q.
\]

The same zero-start calculation compared with \(\sum_kK_k(\tau)\) gives

\[
 \mathcal K-B_Q\le W_{\rm up}\le\mathcal K+B_Q.
\]

Hence

\[
 \left|W_{\rm up}-\mathfrak C_{\rm full}\right|\le B_Q.
\]

The coefficient one is sharp. In the single-shell scalar stress row
\(K=0,\ Q=-B,\ F=B\), the full positive flux is \(B\), while no strict
positive terminal upcrossing is admissible and \(W_{\rm up}=0\). This row
also disproves the tempting stronger assertion
\(\mathfrak C_{\rm full}\le W_{\rm up}\).

For the inherited exact family,

\[
 \mathfrak C_R^{M,*}\asymp T_*,
 \qquad
 \mathfrak C_{{\rm full},R}^{M,*}\ge\mathfrak C_R^{M,*},
 \qquad
 (P_R^{M,*})^{2/3}\asymp {T_*\over K_*},
 \qquad K_*\to\infty.
\]

Since \(B_Q\lesssim(P_R^{M,*})^{2/3}\), the sharp comparison yields

\[
 {\mathfrak W_{{\rm up},R}^{M,*}\over(P_R^{M,*})^{2/3}}\to\infty.
\]

Thus the universal all-solution antecedent
\(\mathfrak W_{{\rm up},R}^M\lesssim(P_R^M)^{2/3}\) is **REFUTED** by a
smooth periodic exact solution. The conditional implication (S.38) is
preserved: if its antecedent holds for a particular family or restricted
class, its conclusion still follows. The viable route returns to the fixed
best-\(N\), terminal-dependent exception quantifier of R0.74Q.

## 3. Independent executable audit

The independent verifier is
scripts/r074s_defect_relaxed_total_rayleigh_certificate_independent.rb,
SHA-256 b18b0a0b9937b106c5879a9e28996dd6892ab53f19decb7bca4db38c70a11343. It uses only the Ruby standard library
and exact Rational arithmetic. The note, primary certificate, primary
generator, and primary report paths are independently overridable by
environment variables.

The verifier returned **PASS** with:

- 22/22 independent exact threshold, exponent, and gate-equivalence rows;
- 5,780/5,780 eligible priority cases among 19,652 rational configurations;
- a 325-allocation maximin search, whose unique grid maximizer is
  \((1/6,1/6,1/6)\);
- 625/625 rational Jensen fixtures, including 25 equality cases;
- 1,728/1,728 exact cross-shell Hölder fixtures, including 48 equality cases;
- 625/625 scalar-versus-Jordan atomic fixtures, including 464 strict
  cancellation cases;
- 125/125 total-mass fixtures and 768/768 raw Step 7 residual comparisons;
- 192/192 smooth-density fixtures, including 104 strict cancellation cases;
- the open-endpoint and Jordan lower-semicontinuity direction tests;
- 432/432 terminal-flux fixtures, including 252 selected residual cases with
  the strict \(5/6\) and \(6/5\) conclusions;
- 9/9 exact-shear terminal fixtures plus an \(x=0<X\) logical witness;
- 6,561/6,561 two-shell discrete-clock gate fixtures, including 46 sharp
  \(\mathfrak C_{\rm full}-\mathfrak W_{\rm up}=B_Q\) cases and the
  \(K=0,Q=-B,F=B\) zero-clock stress row;
- five exact-family scale rows with lower stopped-work ratios
  \(1,3,7,15,31\);
- 61/61 independent source and claim-boundary checks;
- 14/14 adversarial source mutations rejected; and
- 10/10 adversarial primary-artifact mutations rejected.

The rejected source mutations reverse the \(x\le X\) order, alter either
one-sixth threshold, alter \(C_4\), reverse the open-set Portmanteau
inequality, erase the shear boundary, remove the stopped-work bridge,
replace the sharp \(B_Q\) error by \(2B_Q\), assert the false
\(\mathfrak C_{\rm full}\le\mathfrak W_{\rm up}\) ordering, erase the
zero-clock stress row, promote the refuted universal gate, refute the still
valid conditional implication, promote a functional field to a PDE
solution, or remove the NOT-CLAY boundary. The rejected producer mutations include stale source hashes,
wrong schema, a false producer status, a missing exact row even after its
summary is forged consistently, duplicate identifiers, a failed structural
row, an analytic-scope promotion, and a stale summary.

Two clean executions and one execution through all four environment path
overrides produced byte-identical stdout, SHA-256
e73fda5e966253567ecfce564564dc8854b3c6f17d3fd0fcf1398f49df40bc11. The output contains no time, randomness,
floating-point arithmetic, network access, or non-standard dependency.

## 4. Primary-producer cross-check

Only after the independent rational and source checks were complete did the
Ruby verifier inspect the Python-produced artifact. The producer cross-check
is **PASS**:

| Frozen artifact | SHA-256 |
|---|---|
| Primary Python generator | 18735df5a8eff96167ef6314dad04150636c800c276e2fcffc7cbd8177fce9cf |
| Primary JSON certificate | 3639edbccfddd97781805ed121fc91407771b9bf051ffefae5a17ad80087c69c |
| Primary certificate report | 3a6d1e263daa7041edc4083a76c38af44f4fbcd7d2efc8f57592eecbd19ec55a |

The JSON binds the final note and generator hashes, has the expected schema
and finite-only scope, and reports 16/16 exact rows, 19/19 finite checks,
75/75 structural checks, and 20/20 negative mutations. Every row is marked
passing, every failure list is empty, identifiers are unique and complete,
the summary agrees with the four row collections, and the Markdown report
reproduces the same hashes and scope boundary.

## 5. Final boundary

The independent audit supports:

- \(0\le x_k\le X_k\), with the correct scalar/Jordan meanings;
- the exact \(\beta\to\sigma\to x\) trichotomy and inherited cubic payment;
- fixed-scale Version-M lower semicontinuity for each global interface;
- the smooth formulas only under their stated hypotheses;
- \(x_k=0\), but not necessarily \(X_k=0\), for the inherited exact shear;
- fixed-scale finiteness of \(X\) and linear flux control of \(x\); and
- containment of the scalar excess in the already-open stopped signed-work
  gate, with selected-shell coefficient \(6/5\);
- the sharp comparison
  \(|\mathfrak W_{\rm up}-\mathfrak C_{\rm full}|\le B_Q\) and the
  analogous two-sided full-clock comparison; and
- exact-family refutation of the universal no-exception quadratic
  stopped-work antecedent, while preserving (S.38) as a conditional
  implication.

The audit does not support a no-exception quadratic estimate for the
stopped-work gate (that estimate is refuted), a quadratic estimate for the
Jordan envelope, a fixed best-\(N\) exception theorem, cross-scale
compactness, a Version-F theorem, (Q.1), regularity, or a Clay claim.

**INDEPENDENT FINITE/ALGEBRAIC AND SOURCE AUDIT: PASS. NOT CLAY.**
