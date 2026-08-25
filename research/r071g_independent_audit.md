# R0.71G Independent Mathematical Audit

**Date:** 2026-08-25

**Audit type:** internal analytic, adversarial, computational, and bounded-literature review

**Final status:** **PASS AFTER THE CORRECTIONS RECORDED BELOW**

## 1. Scope and non-claims

This audit checks the internal consistency of the R0.71G projected-Lamb
residence analysis, its two finite certificate programs, the formal figure
package, and the bounded primary-source comparison.  The frozen release
inputs are:

- `research/r071g_report-source.md`;
- `research/r071g_gap_matrix.md`;
- `research/r071g_literature_audit.md`;
- `research/r071g_exact_audit.py`;
- `research/r071g_independent_audit.py`;
- `figures/r071g-residence/fig-r071g-residence-gate/`;
- `requirements-research.txt`.

The word *independent* has a limited internal meaning.  The second program
does not import the exact producer, begins from the full trigonometric
velocity, reconstructs the initial NSE derivative by a separate FFT route,
and integrates the reduced chain with a different method and two truncation
radii.  This is not external peer review.  The audit does not establish
originality, priority, a global literature nonexistence result, an
unconditional Navier--Stokes regularity theorem, or a singularity.

The pass verdict means that the stated claims follow after the quantifiers
and boundaries in Section 4 are retained.  It does not turn finite numerical
checks into proofs of the report's arbitrary-cutoff, arbitrary-duration, or
Leray-level statements.

## 2. Analytic findings

### 2.1 Projected-Lamb evolution and shell ledger

For a smooth incompressible solution and
\(L=\mathbb P(u\times\omega)=u_t-\nu\Delta u\), direct differentiation gives

\[
 L_t=\nu\Delta L
 -\mathbb P\bigl((L\cdot\nabla)u+(u\cdot\nabla)L\bigr)
 +2\nu\mathbb P\sum_m
   \bigl((\partial_m u\cdot\nabla)\partial_m u\bigr).
\]

The cross-product form in the report is equivalent.  Expanding dyadic
pieces requires all interacting shell pairs; no near-diagonal truncation is
available from this identity alone.

For fixed heat height and cutoff, the displayed formulas for \(B_t\) and
\(d_t\) follow by product differentiation, including the cutoff collar and
moving-partition terms.  With \(E=C/\sqrt d\) and
\(\beta=\langle F,E\rangle\), the radial part of \(C_t\) cancels:

\[
 \beta_t
 =\langle A L_t,E\rangle
 +d^{-1/2}\langle P_{E^\perp}F,C_t\rangle.
\]

Therefore the positive square appearing in the unnormalized work derivative
does not alone control the normalized positive quotient.  At \(d=0\), the
unregularized quotient can jump; either an \(\varepsilon\)-regularization or
the corresponding internal time faces must remain explicit.

### 2.2 True-solution residence witness

The 2D3C datum in the report generates a global-smooth NSE solution.  Its
vertical component obeys the exact infinite sideband chain

\[
 c_m'=-(m^2+1)c_m+i\mu e^{-\theta}(c_{m-1}+c_{m+1}).
\]

The phase-invariant real subspace \(c_m=i^m x_m\), \(x_m\in\mathbb R\),
justifies the local sign-density formula.  The Duhamel estimate

\[
 \|c_\mu-c_0\|_{\ell^2}
 \le 2\sqrt2\,\mu e^{-\theta}(1-e^{-\theta})
\]

keeps the signed low-shell work positive on every prescribed finite interval
\([0,M]\) when \(\mu\) is sufficiently small.  With \(a=K^{-1}\), the
initial kinetic energy stays fixed and \(\mu=(\nu K)^{-1}\).  This disproves
only a universal finite constant for sign-only residence on the stated
family.  It neither creates a singularity nor contradicts critical residence
for fixed positive relative levels.

The reduced coefficients extend analytically to \(\mu=0\).  Physical ratios
are interpreted through the limit \(\mu\downarrow0\), not by dividing the
zero-amplitude solution by its zero initial value.  In that limit the fixed
relative \(B\), \(q\), and \(q/Y\) exits are fixed multiples of
\((\nu K^2)^{-1}\).

### 2.3 Residence is not summability

The disjoint-event construction with \(K_n=2^n\), \(n\ge1\), has critical
residence at each shell, finite \(K_n^{-2}\)-weighted bulk, and divergent
unweighted bottom trace.  It is an abstract logical obstruction, not an NSE
trajectory.

For a continuous nonnegative BV function whose every positive superlevel
component has length at most \(CK^{-2}\), layer cake and one-dimensional
coarea give

\[
 \int_I a(t)\,dt
 \le \frac C2K^{-2}
 \left[\operatorname{TV}_I(a)+a(t_-)+a(t_+)\right].
\]

Its multiscale use is conditional on one uniform residence constant for all
shells, cells, and regularizations, plus a uniform-in-\(\varepsilon\) weighted
BV sum.  Standard Leray energy does not supply the required source,
direction, denominator, crossing-count, or BV budgets.

## 3. Computational audit

### 3.1 Exact producer

The exact producer exited successfully.  All nine declared Boolean fields
are true.  It checks the two projected-Lamb evolution forms, the exact NSE
initial derivatives, normalized radial cancellation, denominator-zero jump,
linear 2D3C limit, scaling ledger, and the abstract residence-only no-go.

The field `analyticDuhamelBoundRecorded` means only that the certificate
records the analytic Duhamel bound used by the report.  It intentionally does
not say that the program proves the arbitrary-\(M\) theorem.

### 3.2 Independent FFT and chain checker

The independent program exited successfully with all nine declared checks
true.  Across the three FFT cases, the largest relative error among the ten
initial formulas was
\(1.30\times10^{-15}\).  Across the five coupling values, the largest event-
time difference between chain radii 12 and 18 was
\(3.38\times10^{-14}\).  The largest sampled chain-energy residual was
\(1.78\times10^{-15}\).

These are binary64 finite checks.  The FFT reconstructs only the initial
physical-time identities.  DOP853 integrates a finite truncation of the
reduced sideband chain; it is not DNS and is not 3D PDE time stepping.

### 3.3 Figure-package comparison

`validation.json` passes all 45 declared data checks.
`independent-validation.json` passes all 17 declared checks.  Its largest
fixed-step versus adaptive differences are
\(4.54\times10^{-8}\) for the sign exit and
\(1.38\times10^{-7}\) for the relative-level exits.  The vector PDF is one
page at 178 by 108 millimetres, and the PNG is 4204 by 2551 pixels at the
declared 600 dpi export setting.  Original, grayscale, and independently
rasterized PDF inspections are recorded in `qa-report.md`.

The figure uses fixed-step RK4 on the exact reduced chain with
\(|m|\le24\), not a fitted surrogate.  Panel D is an exact functional partial
sum, not a simulated NSE trajectory.  The dashed inverse-coupling line is an
illustrative guide and is not used as a theorem.

## 4. Corrections required for the pass verdict

The following corrections are part of the audited claim boundary:

1. Every viscous source term retains the complete factor
   \(((\partial_m u\cdot\nabla)\partial_m u)\), and the shell expansion keeps
   both interacting indices.
2. The phase-invariant real subspace is stated before the localized
   sign-density formula, and the cutoff quantifier is pointwise in time:
   \(\chi(t,\cdot)\ge0\) and \(\chi(t,\cdot)\not\equiv0\).
3. The weak-coupling formulas are described as analytic extensions of the
   reduced coefficients and limits as \(\mu\downarrow0\), not as physical
   ratios at zero amplitude.
4. The matched aggregate explicitly assumes
   \(\phi_Q\ge0\), \(\sum_Q\phi_Q=1\), and overlap at most \(N\), in addition
   to the square and gradient bounds.
5. The BV application states a single uniform \(C\), the componentwise
   superlevel residence hypothesis for every shell, cell, and regularization,
   and the uniform-in-\(\varepsilon\) sum.
6. The source budget distinguishes the unnormalized \(q\) target from the
   normalized \(a=q/Y\) target; the latter carries
   \(K^{-4}\|T_j\partial_tL\|_2^2/Y\).
7. The whole-space scaling conclusion is restricted to covariant thresholds,
   geometry, and parameters with a scale-invariant constant.  It does not
   reject laws depending on additional non-scale-invariant data.
8. The disjoint interval construction states \(n\ge1\), and the fixed-level
   exit constant is written directly without a redundant intermediate
   exponent expression.
9. Reader-facing formulas retain literal LaTeX delimiters and `\quad` tokens;
   no source-language escape loss is accepted in the synchronized HTML/PDF.
10. The exact JSON label is `analyticDuhamelBoundRecorded`, so the finite
    certificate does not overstate the analytic proof.

## 5. Bounded literature verdict

The primary-source comparison is limited to the version-pinned works listed
in `research/r071g_literature_audit.md`.  The nearest mechanisms include a
conditional time-frequency regularity criterion, bad-interval or
dissipation-wavenumber formulations, positive-strain geometry, and a
conditional filtered-stretching closure.  None of the sources in this
bounded search supplies the fixed-shell signed projected-Lamb
\(CK^{-2}\)-occupation estimate from standard Leray budgets.

This is a bounded search result only.  It must not be stated as a proof that
no such result exists, or as a novelty or priority claim for R0.71G.

## 6. Final verdict

After the corrections in Section 4, the exact identities, true-solution
sign-only no-go, fixed-relative-level family limits, residence-only
summability obstruction, and conditional BV lemma are internally consistent
with their declared hypotheses.  The two finite certificate routes agree at
the recorded tolerances, and the figure package accurately separates exact
formulas, reduced-chain checks, and the abstract functional example.

**Verdict: PASS AFTER CORRECTIONS.**  The release provides a negative and
conditional structural result.  It does not provide the missing Leray-level
angular/source-curvature budget, a general residence theorem, or a solution
of the Navier--Stokes regularity problem.
