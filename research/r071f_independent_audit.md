# R0.71F Independent Mathematical Audit

**Date:** 2026-08-25

**Audit type:** internal three-way mathematical audit

**Final status:** **PASS AFTER LISTED CORRECTIONS**

## 1. Scope and non-claims

This audit evaluates the internal mathematical consistency, adversarial stress
tests, finite computational certificates, and bounded primary-source boundary
of R0.71F.  It is based on the following frozen inputs:

- `research/r071f_report-source.md`;
- `research/r071f_gap_matrix.md`;
- `research/r071f_literature_audit.md`;
- `research/r071f_exact_audit.py`;
- `research/r071f_independent_audit.py`;
- `requirements-research.txt`.

The audit is independent in the limited internal sense that the analytic
derivations were rechecked against the report, the adversarial tests were read
against the gap matrix, and the second numerical checker does not import the
symbolic producer.  It is **not** external peer review.  It does not establish
originality, priority, global literature nonexistence, an unconditional
Navier--Stokes regularity theorem, or a singularity construction.

The pass verdict means only that the claims now stated in R0.71F follow from
the displayed proofs and declared hypotheses, that the finite checkers support
the finite algebra they actually implement, and that the literature language
has been restricted to the four version-pinned primary sources reviewed.

## 2. Three-way audit design

### 2.1 Analytic lane

I rederived the moving-cutoff integrations by parts, the projected/material
conversion, the stabilized local denominator comparison, the local-to-global
Cauchy step, the heat-semigroup moment integral, the exact cutoff witness, the
matched-partition inequalities, and the whole-space scaling exponents.  I also
checked that every continuation or Leray-level assertion carries its stated
solution-class and prior-result dependencies.

### 2.2 Adversarial lane

The gap matrix was used as a rejection checklist.  In particular, I tested the
report against cutoff--curl collars, moving-cutoff shape residuals, zero or
collar-dominated denominators, independent covers at infinitely many radii,
high-frequency fixed-energy data, the distinction between an initial datum and
its later solution, and constants hidden in the interior scaling statement.

The two programs supply complementary finite checks:

1. the exact producer reconstructs the relevant Fourier block from the full
   six-mode initial datum and checks symbolic identities and constants;
2. the independent checker begins from the full trigonometric velocity, uses
   separate FFT differentiation and Leray projection, inserts a nonconstant
   positive cutoff in physical space, and checks four dyadic frequencies by
   numerical quadrature.

### 2.3 Literature lane

The source audit is bounded to the following version-pinned primary sources:

- Yang, arXiv:2008.05588v2;
- Vasseur--Yang, arXiv:2009.14291v1;
- Chen--Liang--Tsai, arXiv:2606.16438v1;
- Yu, arXiv:2606.27560v1.

The audit checks theorem direction and applicability only.  The resulting
negative finding is restricted to these sources and cannot be promoted to a
novelty, priority, or global nonexistence claim.

## 3. Reproducibility record

### 3.1 Reviewed input hashes

| Input | SHA-256 |
|---|---|
| `research/r071f_report-source.md` | `0f2e88884a174fb0794bc1259fcf9f52fdd2cf2378d7c1e6773b0c3b110a4f6e` |
| `research/r071f_exact_audit.py` | `d6f7fe73cd73fad52bf2c59fb3020bb2198a599b333f1a64bfbee1b9d8bc7155` |
| `research/r071f_independent_audit.py` | `f32347b6b019f8826c0ca0736e9e2236e87264c95599057bbcbde8d8d51c59bb` |
| `research/r071f_gap_matrix.md` | `ae25fe62f9f4a1088db34819c56e89c3d82b03c3f09672db14a45212debe1eaa` |
| `research/r071f_literature_audit.md` | `074d357a6b677f79d4ab7673671aebff6209a5972878231d7bd1ab06ec779910` |
| `requirements-research.txt` | `ec302032d513e8f83827bcc7c1f2a58bb63d6b6b40c3e6f54ce3fdc27b7f8b17` |

### 3.2 Execution environment

The default bundled Python lacked SymPy and SciPy, so that initial launch was
not treated as evidence.  Both checkers were then rerun successfully in the
existing research environment matching `requirements-research.txt`:

- SymPy 1.14.0;
- NumPy 2.3.5;
- SciPy 1.16.1.

The commands were equivalent to

```text
<research-python> research/r071f_exact_audit.py --output <exact.json>
<research-python> research/r071f_independent_audit.py --output <independent.json>
```

### 3.3 Checker results

| Checker | Result | Implemented evidence |
|---|---|---|
| Exact symbolic producer | exit 0; all 9 declared Boolean checks true | Low-block Fourier reconstruction, cutoff--curl integration by parts, exact exponential trace, Gamma moment, and matched-partition algebra |
| Independent FFT checker | exit 0; status `pass`; all 6 declared Boolean checks true | Full-velocity FFT differentiation and projection, one fixed nonconstant positive cutoff, (K=1,2,4,8), heat decay, and finite-height quadrature |

For the independent checker, the largest observed errors over the four cases
were

| Quantity | Maximum observed | Required tolerance |
|---|---:|---:|
| divergence error | (0) | (2\times10^{-11}) |
| low-vorticity field error | (6.10\times10^{-14}) | (2\times10^{-11}) |
| low projected-Lamb field error | (9.06\times10^{-14}) | (2\times10^{-11}) |
| cutoff-work identity error | (1.25\times10^{-12}) | (2\times10^{-10}) |
| heat-decay relative error | (6.38\times10^{-16}) | (2\times10^{-12}) |
| finite-trace relative residual | (3.73\times10^{-16}) | (2\times10^{-12}) |

The symbolic producer also recovered, at (a=K=1), low-block enstrophy (4),
palinstrophy (4), projected-Lamb (L^2)-norm squared (2), positive work
(2), and positive quotient (1).  Its exact infinite-height trace factor is
(2K^2).

These executions are finite certificates.  A Boolean label in the JSON is not
by itself a proof of an arbitrary-cutoff, arbitrary-partition, Leray-limit, or
continuation quantifier.  Those quantifiers are accepted only where the report
contains the corresponding analytic argument.

## 4. Corrections required before the pass verdict

The following issues were material during the audit and are corrected in the
current report or literature ledger.

| Issue found | Correction now present | Residual boundary |
|---|---|---|
| Moving ledger could omit or double-count boundary terms | Equations (3.4) and (3.9) retain both heat-height faces, time faces, cutoff--curl work, shape/transport residual, and viscous collar; the two heat-taper terms cancel exactly when representations are converted | The identity is used only on smooth or strong intervals |
| Projected and material forms could be charged as separate defects | Equation (4.5) proves they are the same ledger and identifies the transport integration-by-parts term | No independent gain may be claimed from counting both forms |
| Local palinstrophy could hide the cutoff collar | Equations (5.3)--(5.6) stabilize the denominator with (r^{-2}M_{j,Q}) and use annular Bernstein only at matched radius | The collar cost remains explicit outside the matched annular setting |
| A heat taper or a Carleson label could be mistaken for trace gain | Sections 3, 7, and 10 show that tapering only moves the same face term and that the witness retains the full (K^2\simeq h^{-1}) cost | A critical (Cr^{-2}) estimate is saturated, not disproved |
| The six-mode description could be read as an all-time modal truncation | The claim is now restricted to a six-mode initial datum generating a true global-smooth 2D3C solution and to its exact initial trace | The later solution is not claimed to remain six-mode |
| The partition statement could rely on Yang for pointwise bounded overlap | The literature audit now distinguishes Yang's pairwise-disjoint Vitali subcollection from the separately assumed or constructed matched bounded-overlap partition in R0.71F | Yang's theorem supplies no heat-height trace gain |
| The interior no-go originally risked overbroad constants and frames | Section 9 now constructs compactly supported divergence-free data, moves to a strictly interior smooth time, fixes the covariant one-block frame, states the pure multiplicative form, and lists five exclusions | It does not reject other fixed frames, critical factors, fixed-distance interior cylinders, or estimates with additional terms |
| The caloric trace analogy could reverse a theorem's logical direction | The Chen--Liang--Tsai comparison now states that interior normal derivatives control boundary Besov/Triebel--Lizorkin norms for their exact parabolic Poisson extension | It gives no zero-order bottom-from-bulk theorem for (e^{s\Delta_x}) |
| Yu's conditional closure could be reported as energy-driven vanishing | The exact whole-space setting, principal cutoff-residual alternative, separate exterior tail, and all three summability inputs are now explicit | None of those closure inputs is derived from Leray energy in that paper |
| Criterion comparisons could imply an unproved strict improvement | Only the Serrin endpoint implication from (5.10) is asserted; BMO, Besov, BKM-type, and dissipation-wavenumber relations are recorded as unproved | A different observable is not evidence of a weaker criterion |

The gap matrix remains a working burden-of-proof document rather than a
theorem.  Its statement that geometry may supply bounded overlap is read as an
allowed separately constructed partition input, not as a conclusion of
Yang's Proposition 12.

## 5. Item-by-item verdicts

### 5.1 Moving projected-Lamb ledger

**Analytic check.**  Starting from

\[
 (\partial_t-\nu\partial_s)W_{j,s}=\nabla\times F_{j,s},
\]

time integration produces the two time faces and
\(-\int e_{j,s}\partial_t\chi_Q).  Writing
\(\partial_t\chi_Q=R_Q-V_r\cdot\nabla\chi_Q\) gives exactly the shape term in
(3.4).  Heat-height integration gives both (s)-faces and the displayed
\(\zeta'\) term.  Spatial curl integration produces
\(\langle F_{j,s},\nabla\times(\chi_QW_{j,s})\rangle\), including the
cutoff--curl collar.  Substitution of
\(\partial_s e=\Delta e-|\nabla W|^2\) yields (3.9) with the two taper terms
cancelling and the sign of (\Delta\chi_Q) as displayed.

**Program boundary.**  Neither checker integrates the complete moving
((t,s,x)) ledger with arbitrary time-dependent cutoff.  The exact producer
checks only the spatial cutoff--curl identity used by the ledger.

**Verdict:** **PASS by analytic proof.**

### 5.2 Projected/material equivalence

**Analytic check.**  The identity

\[
 G_{j,s}=u\cdot\nabla W_{j,s}+\nabla\times F_{j,s}
\]

and incompressibility give

\[
 \int\chi_QW_{j,s}\cdot G_{j,s}
 =B_Q^L-\int e_{j,s}u\cdot\nabla\chi_Q.
\]

This converts (4.4) exactly into (3.4).  The projected cutoff--curl collar and
the material relative-transport term are alternative representations, not
independent losses.  The Bernoulli-gradient contribution also annihilates
against the curl test as stated in (11.2).

**Program boundary.**  This equivalence and the pressure cancellation are
proof-only claims in the present audit.

**Verdict:** **PASS by analytic proof.**

### 5.3 Stabilized local continuation criterion

**Analytic check.**  The two-sided comparison (5.3) follows from expanding
\(\nabla\times(\chi_QW)\) and retaining the cutoff collar.  Uniform overlap,
cutoff derivative bounds, the matched radius (r_j\simeq K_j^{-1}), and
annular Bernstein give (5.6).  Since the partition sums to one,
\(\sum_Q B_Q^L=b_{j,s}); Cauchy applied to the positive parts then gives
(5.7).  Integrability of (A_{\rm loc,+}) therefore feeds the previously
established R0.71C continuation consumer.  Equation (5.10) correctly shows
only the one-way Serrin endpoint implication.

**Program boundary.**  The symbolic producer checks the matched-partition
algebra for the explicit witness.  It does not prove the general continuation
theorem or re-audit the R0.71C consumer.

**Verdict:** **PASS as a conditional theorem with an explicit R0.71C
dependency.**  It is more restrictive than the global shell condition; no
strict improvement over a published criterion is claimed.

### 5.4 Heat packing and Gamma moments

**Analytic check.**  Local Cauchy gives

\[
 q_{j,Q}\le
 \|1_{\operatorname{supp}\chi_{j,Q}}F_{j,s}\|_2^2.
\]

Bounded overlap and tight-frame summation yield (6.2) and (1.1).  Fourier
integration of
\(s^{\alpha-1}e^{-2s|k|^2}\) gives
\(\Gamma(\alpha)/(2^\alpha|k|^{2\alpha})\), proving (6.3).  At
\(\alpha=1\), the negative-derivative Lamb norm is bounded by
\(\|u\|_4^2\), and the stated interpolation/energy argument gives the
periodic Leray--Hopf (L_t^1) bound in the finite-truncation/Fatou sense.

**Program support.**  The exact producer symbolically checks the Gamma moment
and its (2^{-\alpha}\) constant.  It does not prove tight-frame completeness,
arbitrary-cover overlap, or passage to Leray solutions.

**Verdict:** **PASS.**  Bounded overlap at every independent radius does not
give an unweighted sum over infinitely many radii; (6.7) records that separate
boundary.

### 5.5 Exact local cutoff witness

**Analytic check.**  The full six-mode initial datum is divergence-free and
2D3C and therefore generates a global-smooth solution.  On the fixed low
sphere, the report reconstructs (W_s) and (F_s) and keeps the complete
\(\nabla\chi\times W\) term.  Curl integration by parts gives the nonnegative
density

\[
 4a^3K^6e^{-2K^2s}\phi(x)\sin^2(Kx_2),
\]

whose integral is strictly positive for every nonzero smooth
\(\phi\ge0\).  Common spherical heat decay gives
\(q_\phi(s)=e^{-2K^2s}q_\phi(0)\) and hence the exact finite-height factor in
(7.7).

**Program support.**  The exact producer verifies the symbolic Fourier block,
cutoff--curl identity, decay, and trace factor.  The independent checker
confirms the same mechanism for one fixed nonconstant positive cutoff and
\(K=1,2,4,8\).  The arbitrary-cutoff quantifier and global-smooth 2D3C fact
remain analytic statements, not finite-grid conclusions.

**Verdict:** **PASS.**  The witness proves the frequency-square trace cost; it
does not prove blow-up and does not reject the critical trace scale.

### 5.6 Matched-partition bounds

**Analytic check.**  Nonnegativity of each (B_Q), partition unity, the
square-cutoff and gradient-cutoff bounds, and reverse Cauchy give the lower
bound in (8.4).  Local Cauchy and support overlap give the upper bound.  With
total enstrophy (Y=8a^2K^4) and (a=K^{-1}), the kinetic energy is fixed,
the normalized bottom remains bounded away from zero, and the normalized
infinite heat bulk is smaller by (2K^2).

**Program support.**  The exact producer verifies the algebraic constants
under the declared (C_0,C_1,N,\rho) assumptions.  Neither checker constructs
all admissible partitions or verifies their geometry dynamically.

**Verdict:** **PASS under the stated partition hypotheses.**

### 5.7 Interior scaling boundary

**Analytic check.**  The vector-potential construction gives compactly
supported smooth divergence-free data equal to the affine field in a core.
There (\omega_0=(1,0,0)) and
\(\nabla\times L_0=(1,0,0)\), so a suitable cutoff has positive work and
positive denominator.  Small amplitude, smooth local existence, and
continuity move the test to a strictly interior center time.  A sufficiently
small symmetric cylinder is Yang-admissible.  Under exact NSE scaling,

\[
 B\mapsto\lambda^3B,
 \quad d\mapsto\lambda^3d,
 \quad q\mapsto\lambda^3q,
 \quad Y\mapsto\lambda Y,
\]

so (A_Q\mapsto\lambda^2A_Q) while the normalized heat bulk is invariant.
This proves the (c_*r^{-2}) ratio for the covariant one-block family.

**Program boundary.**  Neither checker implements the compactly supported
datum, positive-time NSE evolution, flow-adapted cylinder, or scaling family.
This theorem is supported only by the displayed analytic construction.

**Verdict:** **PASS with all five boundaries in Section 9 retained.**  In
particular it rejects only pure multiplicative (o(r^{-2})) factors with
constants depending on the stated uniform geometry/admissibility parameters.

### 5.8 Literature and novelty boundary

**Source check.**  The current literature ledger now preserves the exact
directions needed here:

- Yang's Definition 2 uses (<\eta); Proposition 14 allows arbitrary
  (\eta>0), while the covering/maximal theorem uses fixed
  (\eta<\eta_0).  Proposition 12 gives a pairwise-disjoint Vitali
  subcollection, not R0.71F's pointwise bounded-overlap partition.
- Vasseur--Yang use skewed cylinders to globalize a local theorem whose
  mixed-norm smallness is an input, not a geometric consequence.
- Chen--Liang--Tsai control boundary Besov/Triebel--Lizorkin norms by interior
  normal derivatives for their exact half-space parabolic Poisson extension;
  they do not recover the R0.71F bottom trace from zero-order heat bulk.
- Yu's unweighted closure is conditional in an exact whole-space setting and
  assumes treatment of the principal cutoff residual, full far-field
  summability with a separate exterior-tail estimate, commutator-increment
  summability, and remaining shell-budget summability.

The criterion table asserts only the internally proved Serrin endpoint
implication.  It records the relations to Koch--Tataru (BMO^{-1}), critical
Besov, BKM-type, and dissipation-wavenumber criteria as unknown rather than
claiming a strict improvement.

**Program boundary.**  No program can certify this literature or novelty
boundary.  It rests on the bounded primary-source audit and explicit cautious
wording.

**Verdict:** **PASS as a bounded source audit.**  No originality or global
nonexistence verdict is made.

## 6. Proof versus finite-certificate ledger

| Claim | Analytic proof required | Exact producer | Independent FFT checker |
|---|---:|---:|---:|
| Complete moving ((t,s,x)) ledger | yes | spatial cutoff identity only | no |
| Projected/material equivalence | yes | no | no |
| Conditional continuation theorem | yes, plus R0.71C | witness algebra only | no |
| General bounded-overlap heat packing | yes | moment/constant support | no |
| Gamma spectral factor | yes | exact symbolic support | no |
| Arbitrary nonzero smooth cutoff witness | yes | symbolic density support | one fixed cutoff only |
| (K=1,2,4,8) full-field reconstruction | no beyond code specification | (K=1) symbolic normalization and scaling formulas | yes |
| General matched-partition inequalities | yes | exact algebra under abstract constants | no |
| Interior smooth scaling family | yes | no | no |
| Literature and novelty boundary | primary-source reasoning | no | no |

## 7. Claims explicitly not passed

The following statements are not results of R0.71F and are not implied by this
audit:

1. standard Leray--Hopf budgets imply bottom-trace integrability;
2. bounded overlap yields unweighted packing over infinitely many independent
   spatial scales;
3. a critical (Cr^{-2}) trace estimate is false;
4. the interior obstruction holds for every prescribed frame or for cylinders
   staying a fixed positive time from the initial face;
5. pressure has a universal beneficial sign in a strain or local-energy
   ledger;
6. the localized criterion is strictly weaker than Serrin, Koch--Tataru,
   Besov, BKM-type, or dissipation-wavenumber criteria;
7. a global regularity theorem, singular solution, novelty theorem, priority
   result, or Millennium-problem solution has been obtained.

## 8. Final disposition

**Final status: PASS AFTER LISTED CORRECTIONS.**

The analytic identities, conditional criterion, bounded-overlap heat packing,
exact initial-trace witness, matched-partition obstruction, and narrowly scoped
interior scaling theorem are internally consistent with their current
hypotheses and boundaries.  Both finite checkers pass in the pinned research
environment, and their evidentiary limits are now explicit.  The literature
comparison is theorem-direction accurate within the four audited sources and
does not claim originality or exhaustive nonexistence.

R0.71F may therefore be archived as an internal research-stage result with a
negative route decision: flow-adapted localization preserves the heat bulk but
does not provide a free bottom-trace upgrade.  Any later change to the reviewed
files invalidates the hash manifest above and requires a fresh audit.
