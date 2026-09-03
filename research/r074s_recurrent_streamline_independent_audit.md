# R0.74S Step 17 recurrent-streamline obstruction — independent adversarial audit

## 0. Scope and status

This audit checks the draft
`research/r074s_recurrent_streamline_temporal_tail_obstruction.md` at frozen
Step-16 commit

```text
159ea3c548e51b918512855cf79959460e882b48
```

The final recheck is bound to the corrected main-note SHA-256

```text
7d204b326be45a82bc0d8531ea2f2d894c0c125b76e3ccbf02fdc1978a6011c5
```

The checked range is (S.445)--(S.475), with particular attention to:

- the topology and recurrence of the level set \(\Gamma\);
- the orientation of the Version-M phase and the periodic-averaging bound;
- the dimensionless \(L_t^p\) normalization, all powers of \(R\), and the
  \(p=\infty\) endpoint;
- simultaneous activation of \(N+1\) physical shells and the order of the
  fixed-deletion infimum;
- the upper and lower bounds for the complete Version-M payment \(P_R^M\);
- the signed integration-by-parts identity, the forward positive-excursion
  lower bound, and the BV/Jordan decomposition; and
- the infimum directions in (S.470) and all five comparisons in (S.475).

This is an analytic audit.  It is not a finite certificate, a literature
priority claim, or an independent novelty claim.

**Final draft decision:** `PASS`.
The recurrent-streamline counterexample, all amplitude exponents, the
positive-excursion successor, and the completed-clock comparisons pass
after the five repairs below.  The findings are retained as an audit trail
and are marked with their final resolution.

## 1. Equation-level reconstruction

For the Taylor field

\[
 W=(\partial_2\psi,-\partial_1\psi,0),
 \qquad \psi=\sin x_1\sin x_2,
\]

the actual Version-M phase is

\[
 \theta_A(t)=\mu_R\int_{t_0}^{t}b_A(r)\,dr,
 \qquad d\theta=\mu_Rb_A\,dt,
\]

so on \(I_R\) it runs from \(-L_A\) to \(0\), where

\[
 L_A={\mu_RA\over2}(e^{2R^2}-1).
\]

Using the exact shell multiplier from Step 16 gives

\[
 \dot F_{k,R}
 ={\gamma_k\mu_Rc_{k,R}\over2R}\eta_Rb_A^3q(\theta_A).
\]

For \(1\le p<\infty\), the dimensionless definition therefore gives

\[
 \|h_{k,R}\|_p^p
 =R^{2p-2}\int_{s_R}^{t_0}|\dot F_{k,R}|^pdt.
\]

After restricting to \(I_R\), where \(\eta_R=1\), and changing variables,
the coefficient is

\[
 { (\gamma_kc_{k,R})^p\mu_R^{p-1}R^{p-2}\over2^p},
\]

and periodic averaging supplies the additional factor

\[
 {\mu_RV_p(e^{2R^2}-1)\over4T_*}A.
\]

Thus the second line of (S.456), including the power \(R^{p-2}\) and the
denominator \(2^{p+2}\), is correct.  The \(p=\infty\) normalization in
(S.457) is also correct: \(R^2/(2R)=R/2\).

The complete payment reconstruction also passes.  At fixed \(R\), every
translated smooth profile is uniformly bounded, giving
\(P_R^M\le C_RA^3\), while the terminal buffered local-energy row gives
\(P_R^M\ge c_RA^3\).  No Version-M payment row is omitted.

## 2. Five required findings

### Finding 1 — the topology argument for \(\Gamma\) is incomplete

**Final status:** `RESOLVED / PASS`.

Regularity of a level set inside the open cell \((0,\pi)^2\) does not by
itself show that its component is compact, is a circle, or contains both
sample points used to prove that \(g\) is nonconstant.  This affects the
logical support for (S.447)--(S.449), including \(V_1\ge1/2\).

The proof should explicitly note that
\(\sin x_1\sin x_2=1/2\) implies
\(\sin x_i\ge1/2\), hence
\(x_i\in[\pi/6,5\pi/6]\).  It should then give the two branches

\[
 x_2=\arcsin {1\over2\sin x_1},
 \qquad
 x_2=\pi-\arcsin {1\over2\sin x_1},
 \quad \pi/6\le x_1\le5\pi/6,
\]

which join at their endpoints to form one compact connected oval.  This
also proves directly that \((\pi/4,\pi/4)\) and
\((\pi/2,\pi/6)\) are on the same component.  The text should state that
the three-dimensional trajectory lies on \(\Gamma\times\{0\}\).

The corrected main note now includes both branch formulas, the compact
coordinate bounds, endpoint joining, membership of the comparison points,
and the embedding \(\Gamma\times\{0\}\).  Equations (S.447)--(S.449) now
have a complete topological foundation.

### Finding 2 — the large-amplitude hypothesis is dropped after (S.456)

**Final status:** `RESOLVED / PASS`.

The lower bound in (S.456) assumes \(L_A\ge2T_*\), and (S.457) assumes at
least one complete period.  The boxes (S.458)--(S.459) then omit the
qualification.  Near \(A=0\), the selected terminal phase has \(q(0)=0\),
so the displayed uniform \(dA^3\) lower bound is not justified.

State explicitly that (S.458)--(S.459), the lower assertion following
(S.466), and (S.471) hold for all \(A\ge A_0(R)\), or equivalently as
\(A\to\infty\).  This does not weaken the counterexample or any quantifier
negation, because \(A\) is the final free parameter.

The corrected main note states \(A\ge A_0(R)\) in (S.458), carries this
qualification through (S.459), and states the (S.471) comparison as
\(A\to\infty\).  The quantifier negation in (S.463) remains exact because
\(A\) is chosen only after \(p,N,\beta,C\), and \(R\).

### Finding 3 — two-sided oscillation does not yet prove (S.471)

**Final status:** `RESOLVED / PASS`.

The paragraph after (S.466) states only a lower bound for
\(\operatorname{osc}F\).  The lower half of (S.471), however, needs a
lower bound for the forward quantity \(\operatorname{osc}^+F\).  A large
backward drop alone would not establish that statement.

The repair should choose \(s_*\in(0,T_*)\) with

\[
 \chi(s_*)=(\pi/2,\pi/6,0),
 \qquad g(s_*)-g(0)=1/4,
\]

and select past times \(t_A^-<t_A^+\) by

\[
 \theta_A(t_A^-)=-T_*,
 \qquad
 \theta_A(t_A^+)=-T_*+s_*.
\]

For large \(A\), these times lie in \(I_R\), occur in forward order, and
satisfy \(t_0-t_A^-,t_0-t_A^+=O_R(A^{-1})\).  Since \(\eta_R=1\) there,
(S.465) yields, for \(1\le k\le M\),

\[
 F_{k,R}(t_A^+)-F_{k,R}(t_A^-)
 ={\gamma_kc_{k,R}\over2R}
 \left[{A^2\over4}+O_R(A)
       +4\int_{t_A^-}^{t_A^+}b_A(t)^2g(\theta_A(t))\,dt\right]
 \ge c'_{k,R}A^2.
\]

The integral is nonnegative and \(c_{k,R}>0\) on all activated shells.
The \(N+1\) pigeonhole then proves the required positive-excursion lower
bound.  The present phrase saying that the “boundary term is
\(c_{k,R}A^2/4\)” should be replaced by the full leading increment above,
or should clearly refer only to the bracketed boundary difference; the
outer factor \(\gamma_kc_{k,R}/(2R)\) must not disappear.

The corrected main note now chooses the forward phase pair
\(-T_*<-T_*+s_*<0\), places both corresponding times inside \(I_R\), keeps
the full factor \(\gamma_kc_{k,R}/(2R)\), and uses nonnegativity of the
remaining integral.  It proves \(\operatorname{osc}^+F_{k,R}\ge
c'_{k,R}A^2\) on every activated shell, so the lower half of (S.471)
passes the fixed-deletion pigeonhole.

### Finding 4 — the coordinatewise backtracking claim cites an aggregate bound

**Final status:** `RESOLVED / PASS`.

The prose after (S.468) says that (S.459) and (S.466) imply
\(B_{k,R}\asymp A^3\) on each activated shell.  Equation (S.459) is an
aggregate best-\(N\) statement and cannot imply a coordinatewise lower
bound.

Use instead the coordinatewise \(p=1\) estimate in (S.456), the
coordinatewise upper bound obtained directly from (S.454), the range bound
in (S.466), and the exact identity (S.468).  These give

\[
 B_{k,R}
 ={\operatorname{TV}F_{k,R}-|F_{k,R}(t_0^-)|\over2}
 \asymp_{k,R}A^3,
 \qquad 1\le k\le M,
\]

for sufficiently large \(A\).

The corrected main note now cites the coordinatewise \(p=1\) lower bound
(S.456), the coordinatewise upper bound from (S.454), and
(S.466)--(S.468).  It no longer derives a coordinatewise conclusion from
the aggregate best-\(N\) statement (S.459).

### Finding 5 — the stated \(\beta\)-range is inconsistent

**Final status:** `RESOLVED / PASS`.

The opening and closing prose say “every \(\beta<1\),” whereas
(S.462)--(S.463) assume and prove \(0\le\beta<1\) using the upper payment
bound.  Either consistently state \(0\le\beta<1\), or extend the displayed
quantifier to all real \(\beta<1\).  For \(\beta<0\), the latter extension
must use the lower half of (S.461), because the map \(x\mapsto x^\beta\)
reverses inequalities:

\[
 P_R^M\ge c_RA^3
 \quad\Longrightarrow\quad
 (P_R^M)^\beta\le c_R^\beta A^{3\beta}.
\]

If the broader range is adopted, the sentence saying that (S.462) uses
only the upper half of (S.461) must also be split according to the sign of
\(\beta\).

The corrected main note adopts the broader range \(\beta<1\).  It uses
the upper payment bound for \(\beta\ge0\) and the lower payment bound for
\(\beta<0\), then states the same range in both (S.462) and (S.463).

## 3. Infimum and BV audit

No correction is required to (S.470).  For every terminal time \(\tau\)
and every fixed deletion set \(S\),

\[
 \sum_{k\notin S}z_k(\tau)
 \le\sum_{k\notin S}\operatorname{osc}^+F_k.
\]

Taking the infimum on both sides and then the terminal supremum gives

\[
 \sup_\tau\inf_S\sum_{k\notin S}z_k(\tau)
 \le\inf_S\sum_{k\notin S}\operatorname{osc}^+F_k.
\]

Thus the minimax direction in (S.470) is correct.

All five inequalities in (S.475) also have the correct direction.  For
each coordinate, with \(q_k=\operatorname{TV}Q_k\),

\[
 o_k\le m_k+q_k,
 \qquad m_k\le o_k+q_k,
 \qquad v_k\le\operatorname{TV}F_k+q_k,
\]

\[
 \operatorname{TV}F_k\le2v_k+q_k,
 \qquad m_k\le v_k.
\]

Here \(K_k\ge0\), \(K_k(s_R)=0\) imply
\(\operatorname{TV}K_k\le2\operatorname{Var}^+K_k\).  For each aggregate
inequality, choose an approximating deletion set for the functional on its
right-hand side and bound the remaining \(Q\)-tail by
\(B_{Q,R}=\sum_kq_k\).  No interchange of incompatible infima is used.

## 4. Final corrected recheck

The final draft contains all five required repairs:

1. an explicit compact-connected-oval proof for \(\Gamma\), including the
   two comparison points and the embedding \(\Gamma\times\{0\}\);
2. an explicit sufficiently-large-\(A\) qualification wherever a complete
   circuit is used;
3. a forward-ordered, \(\eta_R=1\) positive-increment construction proving
   the lower half of (S.471), with the full coefficient retained;
4. a coordinatewise citation to (S.456), rather than aggregate (S.459), in
   the backtracking-debt conclusion; and
5. one consistent range for \(\beta\), with the correct side of (S.461)
   used when exponentiation reverses inequalities.

The recheck also recomputed (S.455)--(S.457), (S.465), (S.468),
(S.470), and (S.475) directly rather than relying on textual assertions.
That recomputation has been completed.  The normalization
\(R^{2p-2}\), the post-substitution power \(R^{p-2}\), the factor
\(2^{p+2}\), and the \(p=\infty\) factor \(R/2\) all pass.  The sign in
(S.465), the Jordan identity (S.468), the minimax direction (S.470), and
all five optimized inequalities in (S.475) also pass unchanged.

## 5. Final PASS/FAIL boundary

| Claim | Present decision | Boundary |
|---|---|---|
| Exact Taylor NSE family, multiplier, and recurrent phase | `PASS` | Explicit compact connected oval and \(\Gamma\times\{0\}\) now proved |
| Periodic averaging and \(A^3\) absolute-tail exponent | `PASS` | For sufficiently large \(A\) |
| \(p\)-normalization and all displayed \(R\)-powers | `PASS` | Includes \(p=1\) and \(p=\infty\) |
| \(N+1\) activation and fixed-deletion pigeonhole | `PASS` | \(R\) is chosen after the proposed finite \(N\) |
| Complete payment \(P_R^M\asymp_RA^3\) | `PASS` | Full energy, exterior cubic/pressure, and harmonic rows retained |
| Exact negation of (S.444) | `PASS` | For every proposed finite \(N\) and constant, choose \(R\) and then sufficiently large \(A\) |
| Signed integration by parts and \(O_R(A^2)\) range upper bound | `PASS` | Uses \(\eta_R'\ge0\), \(\int|\eta_R'|=1\) |
| Positive-excursion law (S.471) | `PASS` | Forward phase pair and full positive increment now supplied |
| Jordan/backtracking identity (S.468) | `PASS` | Coordinatewise asymptotic now uses (S.456) and (S.454) |
| Minimax direction (S.470) | `PASS` | Fixed deletion is stronger than terminal-dependent deletion |
| Completed-clock comparisons (S.475) | `PASS` | All five infimum directions checked |
| Full claim ledger | `PASS` | All five findings repaired and independently rechecked |
