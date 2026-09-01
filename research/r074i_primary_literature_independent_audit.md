# R0.74I primary-literature independent audit

**Audit date:** 2026-09-02
**Overall verdict:** **CONDITIONAL**
**Scope:** primary-source audit of `r074i_report-source.md` and Section 5 of
`r074i_suitable_weak_tube_and_log_obstruction.md`. This audit checks source
identity, theorem content, collision boundaries, and the finite non-hit
wording. It does not audit the analytic proofs in Sections 2--4 and is not a
novelty or priority opinion.

## 1. Snapshot binding

The verdict below applies to these exact inputs:

- `r074i_report-source.md`
  SHA-256 `eb729a014ec89ee6c3f7fc715805b4f2e0bc421d41d0c347c1af522c9d31db73`
- `r074i_suitable_weak_tube_and_log_obstruction.md`
  SHA-256 `9b6dfdbc87990e0a31550881799b0aa6f421df6afbfe5f251db1adc9a8227084`

Any later change to either file requires at least a focused re-audit of the
changed claims.

Status scale: **PASS** means the checked statement and its boundary are
source-supported as written; **CONDITIONAL** means the source is sound but the
draft needs the listed precision or metadata repair; **FAIL** means a material
false attribution or unsupported theorem claim. No checked item received
**FAIL**.

## 2. Verdict and direct answer

No fatal source mismatch was found. The report correctly identifies the
standard suitable-weak local energy framework, the fixed-cylinder cubic
interpolation estimate, and a pressure-free one-scale cubic regularity gate.
It also correctly treats its collision search as bounded and expressly refuses
to infer novelty, priority, or a solution of the Millennium problem.

The freeze is nevertheless **conditional** because the current prose does not
state the closest geometric collision sharply enough. Yang, and especially
Vasseur--Yang, do not merely use generic transported neighborhoods:
Vasseur--Yang prescribe a spatially mollified flow by

\[
 \dot X(s)=u_\varepsilon(s,X(s)),\qquad X(t)=x,
\]

and use a one-sided backward skewed cylinder based at the reference time
\(t\). Thus reference-time anchoring (terminal anchoring when the cylinder is
viewed backward from \(t\)) and one-sided backward skewed geometry are already
explicit primary-source precedents. What the screened sources do **not** state
is the full R0.74I combination: its exact moving local-energy test and
approximation passage, Version-M payment, positive collar-flux estimate,
moving-to-fixed inclusion with its constants, and the resulting small-payment
epsilon implication.

The logarithmic comparisons are directionally correct, but two of them should
name their actual observables. Chemin's square-root logarithm compares a
global-in-space scaling-invariant time functional of
\(\|\nabla u(t)\|_{L^2}^2\) with an
\(L_t^\infty\dot B^{1/2}_{2,\infty}\) norm. Ogawa--Taniuchi's exponent
\(1/2\) comes from the Besov summability parameters in a critical logarithmic
interpolation/uniqueness argument. Neither is the local scalar payment
\(P_R\), and neither supplies a \(P_R^{2/3}\sqrt{\log P_R}\) moving-tube
estimate.

## 3. Required repairs before literature freeze

1. **Disclose the closest trajectory collision explicitly.** In the report
   rows for Yang and Vasseur--Yang, and in manuscript Section 5, add that the
   flow is anchored by \(X(t)=x\) and that Vasseur--Yang use a one-sided
   backward skewed cylinder. Replace any wording that could be read as treating
   terminal anchoring or backward skewness themselves as new. Reserve the
   non-collision statement for the exact weighted local-energy/payment/epsilon
   theorem.

2. **Separate the logarithmic observables.** Expand the Chemin boundary to name
   \(N_T(u)\) and
   \(\|u\|_{L_t^\infty\dot B^{1/2}_{2,\infty}}\); expand the
   Ogawa--Taniuchi boundary to say that the exponent is
   \(1/\nu-1/\rho\), with \((\nu,\rho)=(1,2)\) giving \(1/2\), and that
   the application is a global vorticity uniqueness criterion. This prevents
   a shared square-root logarithm from being mistaken for a shared theorem.

3. **Remove an ambiguity in the Montgomery-Smith description.** Change
   “a global critical Serrin condition” to “a global-in-space critical
   Prodi--Serrin-type condition on a finite time interval.” The theorem is an
   endpoint regularity criterion up to \(T\), not a claim whose hypothesis is
   intrinsically global in time.

4. **Complete the Tao bibliography.** Record the published source as Terence
   Tao, *Quantitative bounds for critically bounded solutions to the
   Navier--Stokes equations*, in *Nine Mathematical Challenges---An
   Elucidation*, Proceedings of Symposia in Pure Mathematics 104 (AMS, 2021),
   149--193, DOI
   [10.1090/pspum/104/01874](https://doi.org/10.1090/pspum/104/01874), with
   [arXiv:1908.04958](https://arxiv.org/abs/1908.04958).

5. **Make the reproducibility ledger complete enough to audit.** The current
   report already supplies the Chan--Vasseur DOI
   [10.4310/maa.2007.v14.n2.a5](https://doi.org/10.4310/maa.2007.v14.n2.a5)
   both in its ledger and in its reproducibility note, so no repair is needed
   there. Add at least the Chemin, Montgomery-Smith, Tao, and Lin stable
   identifiers to that note, or state explicitly that the note is only a
   selected identifier list.

Items 1--3 are claim-boundary repairs. Items 4--5 are bibliographic and
reproducibility repairs. None changes the mathematical conclusion of the
report.

The abbreviated references in manuscript Section 5 are accurate rather than
false. For uniform publication formatting, it would still be useful (but is
not freeze-blocking for this audit) to add the journal/volume/pages already
present in the report ledger, and to add the Guevara--Phuc DOI beside its arXiv
link.

## 4. Claim-by-claim audit

| Claim/source | Status | Primary-source finding | R0.74I boundary |
|---|---|---|---|
| Caffarelli--Kohn--Nirenberg, suitable weak solutions and local energy inequality | **PASS** | The 1982 CPAM paper establishes the suitable-weak framework and local energy inequality. The title, authors, year, journal, pages, and DOI in the report are correct. | It licenses smooth nonnegative compactly supported tests. It does not by citation alone justify an absolutely-continuous, solution-dependent moving weight; R0.74I must perform the time-regularization/admissibility passage. |
| Lin, compactness-based CKN proof | **PASS** | Lin's 1998 CPAM paper is correctly titled and identified and is a standard compactness-based proof of the CKN theorem. | It does not state the R0.74I trajectory, payment, or logarithmic frontier. |
| Guevara--Phuc, Lemma 2.6 | **PASS** | Lemma 2.6 of arXiv:1702.00449 / Calc. Var. 56 (2017), Article 68 gives the scale-explicit local interpolation estimate, including the \((\rho/r)^3A(\rho)^{3/4}B(\rho)^{3/4}\) and \((r/\rho)^3A(\rho)^{3/2}\) terms. Metadata and DOI are correct. | The lemma is a fixed-cylinder functional estimate. Applying it after moving coordinates still requires the R0.74I energy-space and containment arguments. |
| Wang--Wu--Zhou, Theorem 1.1 with \(\delta=1/2\) | **PASS** | The theorem states that, for every \(\delta>0\), small \(\int_{Q_1}|u|^{5/2+\delta}\) for a suitable weak solution yields boundedness in a smaller cylinder. With \(\delta=1/2\), this is the cubic condition; Navier--Stokes scaling gives \(r^{-2}\int_{Q_r}|u|^3\). The report's 2019 JDE metadata and DOI are correct. | It is a fixed-cylinder theorem. It supplies the final epsilon gate only after R0.74I proves a fixed cylinder lies in the controlled moving tube. |
| Yang, mollified flow and skewed cylinders | **CONDITIONAL** | Yang defines trajectories generated by a spatially mollified incompressible velocity and tubular/skewed cylinders, then proves covering and maximal-function results. The title, 2022 journal data, DOI, and arXiv identifier are correct. | This is direct prior art for anchored mollified-flow geometry. It is not the R0.74I local-energy epsilon implication. Current prose should say both halves explicitly. |
| Vasseur--Yang, suitable solutions on skewed cylinders | **CONDITIONAL** | The 2021 ARMA paper fixes the path by \(X(t)=x\) and uses a one-sided backward skewed cylinder in its suitable-solution higher-derivative analysis. Title, authors, journal data, DOI, and arXiv identifier are correct. | This is the closest geometric collision. Terminal/reference-time anchoring and backward skewness are established; the exact Version-M weighted energy estimate and its epsilon implication were not found there. |
| Chan--Vasseur logarithmic Prodi--Serrin improvement | **PASS** | The 2007 paper proves regularity under spacetime integrability of \(|u|^5/\log(1+|u|)\). The report and manuscript now give the correct DOI, journal, volume, pages, and arXiv identifier. | This is a global-in-space Orlicz-type hypothesis, not a local moving-tube output with power \(2/3\). |
| Montgomery-Smith logarithmic Serrin criterion | **CONDITIONAL** | The 2005 paper gives, for critical \(2/p+3/q=1\), a regularity criterion of the form \(\int_0^T \|u(t)\|_q^p/(1+\log^+\|u(t)\|_q)\,dt<\infty\). Source metadata are correct. | Distinct observable and logical direction. “Global” should be qualified as global in space/on a finite time interval. |
| Chemin, Theorem 1.3 | **CONDITIONAL** | The 2025 paper genuinely contains a \(\sqrt{\log}\) factor in nonlinear estimates between scaling-invariant quantities. One quantity is \(N_T(u)=\sup_{I\subset[0,T)}|I|^{-1/2}\int_I\|\nabla u(t)\|_{L^2}^2dt\); the other is an \(L_t^\infty\dot B^{1/2}_{2,\infty}\) norm. The report's title, year, volume, pages, and DOI are correct. | A shared log exponent is the only resemblance. The domain, observable, leading power, and logical use all differ from the R0.74I local payment. |
| Ogawa--Taniuchi, Theorem 3.1 and uniqueness application | **CONDITIONAL** | Their critical logarithmic interpolation carries exponent \(1/\nu-1/\rho\); setting \((\nu,\rho)=(1,2)\) gives \(1/2\). It is used in a vorticity uniqueness criterion in Besov/Orlicz spaces. The 2004 Tohoku Math. J. metadata and DOI are correct. | It does not estimate \(X_R\) or \(\mathfrak C_R\) from a scalar payment. The parameter source of the exponent should be stated to prevent conflation. |
| Lei--Ren quantitative partial regularity | **PASS** | The 2024 Advances in Mathematics paper gives a logarithmically improved parabolic Hausdorff gauge (in particular \(r|\log r|\), with a stated iterated-log refinement) and quantitative regular regions. Metadata and DOI are correct. | Its logarithm measures singular-set geometry across scales; it is not a scalar payment in a one-scale moving tube. |
| Tao quantitative critical endpoint | **CONDITIONAL** | Tao obtains quantitative derivative bounds under a critical \(L_t^\infty L_x^3\) bound and an iterated-logarithmic necessary growth statement near possible blow-up. The arXiv identifier and 2021 year are correct. | The content summary is sound, but the report should include the published venue/pages/DOI and should continue to distinguish this global critical-norm mechanism from the local payment frontier. |

## 5. Exact primary-source checks

### 5.1 Suitable-weak and one-scale chain

The following chain is literature-supported, with the qualifications stated:

1. CKN/Lin provide the suitable-weak local energy framework.
2. Guevara--Phuc provide the needed fixed-cylinder kinetic/dissipation-to-cubic
   interpolation estimate.
3. Wang--Wu--Zhou provide a pressure-free one-scale condition; fixing
   \(\delta=1/2\) gives the cubic exponent.

The citations do not themselves prove the two R0.74I-specific links: admission
of the time-dependent solution-generated test in the local energy inequality,
and confinement of a standard fixed cylinder inside the controlled moving
tube. The report correctly lists both as separate analytic obligations.

### 5.2 Closest trajectory collision

The relevant source-level distinction is:

- **Already established:** spatial mollification of a weak velocity;
  reference-time-anchored flow trajectories; tubular/skewed parabolic
  neighborhoods; and, in Vasseur--Yang, a one-sided backward skewed cylinder
  used for suitable solutions.
- **Not located in the bounded screen:** the exact R0.74I cutoff and weak-test
  passage, the frozen Version-M observables, the same positive collar-flux
  inequality, and the exact small moving-energy/payment implication to the
  Wang--Wu--Zhou fixed-cylinder gate.

Accordingly, “terminal anchoring” cannot serve as a novelty-bearing
descriptor. A defensible descriptor must name the entire analytic combination,
not one established geometric ingredient.

### 5.3 Logarithmic non-collision matrix

| Source | Location of logarithm | Logical role | Same as R0.74I observable? |
|---|---|---|---|
| Chan--Vasseur | \(|u|^5/\log(1+|u|)\) | Weakened sufficient regularity hypothesis | **No** |
| Montgomery-Smith | Critical \(L^q\) Serrin quantity divided by a logarithm | Weakened sufficient regularity hypothesis | **No** |
| Chemin | \(\sqrt{\log}\) in a nonlinear comparison of global scaling-invariant Besov/time functionals | Norm comparison | **No** |
| Ogawa--Taniuchi | Exponent \(1/\nu-1/\rho\), equal to \(1/2\) for \((1,2)\) | Critical interpolation used for uniqueness | **No** |
| Lei--Ren | Logarithmic parabolic Hausdorff gauge | Quantitative singular-set geometry | **No** |
| Tao | Iterated logarithms in quantitative critical-norm bounds near possible blow-up | Quantitative endpoint control/necessary growth | **No** |

The table supports the report's finite non-hit. It does not support a novelty
claim, and it does not transfer any cited square-root logarithm to
\(P_R^{2/3}\sqrt{1+\log_+P_R}\).

## 6. Collision and non-collision judgment

### Collision: **PASS after mandatory wording repair**

The report has found and cited the material geometric precedents. Its current
statement that mollified trajectories and skewed cylinders have “direct
precedents” is correct. The missing precision is that terminal/reference-time
anchoring and a one-sided backward cylinder are among those precedents, not
merely generic flow tubes. Once that sentence is added, the collision boundary
is appropriately conservative.

### Observable-level non-collision: **PASS**

Within the explicitly bounded mechanisms, no checked primary source states the
same local scalar-payment estimate

\[
Y_R\lesssim P_R^{2/3}\sqrt{1+\log_+P_R},
\qquad Y_R\in\{X_R,\mathfrak C_R\},
\]

nor the full R0.74I moving-energy epsilon implication. This is a finite
source-screen result only.

### Bounded non-hit wording: **PASS**

The report states that its comparison is bounded, identifies the mechanisms
screened, gives a stopping rule, calls the result a “finite non-hit,” and says
explicitly that it is not evidence of novelty. It further excludes novelty,
priority, global regularity, and a Millennium-problem solution from the claims
certified by the literature. Those safeguards are adequate.

The handling of arXiv:2503.19944 is also appropriately bounded: the report does
not rely on it and does not make a global judgment about the paper. A displayed
interpolation step in that preprint attempts to reach two spatial derivatives
from derivative orders \(0\) and \(2s<2\); that step is not justified by the
standard interpolation invoked there. The report's weaker statement—its proof
was not independently established for this audit—is therefore safe.

## 7. Primary-source ledger

1. L. Caffarelli, R. Kohn, and L. Nirenberg, “Partial regularity of suitable
   weak solutions of the Navier--Stokes equations,” *Communications on Pure and
   Applied Mathematics* 35 (1982), 771--831,
   [DOI 10.1002/cpa.3160350604](https://doi.org/10.1002/cpa.3160350604).
2. F.-H. Lin, “A new proof of the Caffarelli--Kohn--Nirenberg theorem,”
   *Communications on Pure and Applied Mathematics* 51 (1998), 241--257,
   [DOI 10.1002/(SICI)1097-0312(199803)51:3<241::AID-CPA2>3.0.CO;2-A](https://doi.org/10.1002/(SICI)1097-0312(199803)51:3%3C241::AID-CPA2%3E3.0.CO;2-A).
3. C. Guevara and N. C. Phuc, “Local energy bounds and epsilon-regularity
   criteria for the 3D Navier--Stokes system,” *Calculus of Variations and
   Partial Differential Equations* 56 (2017), Article 68,
   [DOI 10.1007/s00526-017-1151-7](https://doi.org/10.1007/s00526-017-1151-7),
   [arXiv:1702.00449](https://arxiv.org/abs/1702.00449).
4. Y. Wang, G. Wu, and D. Zhou, “A regularity criterion at one scale without
   pressure for suitable weak solutions to the Navier--Stokes equations,”
   *Journal of Differential Equations* 267 (2019), 4673--4704,
   [DOI 10.1016/j.jde.2019.05.003](https://doi.org/10.1016/j.jde.2019.05.003),
   [arXiv:1811.09927](https://arxiv.org/abs/1811.09927).
5. J. Yang, “Construction of maximal functions associated with skewed cylinders
   generated by incompressible flows and applications,” *Annales de l'Institut
   Henri Poincare C* 39 (2022), 793--818,
   [DOI 10.4171/AIHPC/20](https://doi.org/10.4171/AIHPC/20),
   [arXiv:2008.05588](https://arxiv.org/abs/2008.05588).
6. A. Vasseur and J. Yang, “Second derivatives estimate of suitable solutions
   to the 3D Navier--Stokes equations,” *Archive for Rational Mechanics and
   Analysis* 241 (2021), 683--727,
   [DOI 10.1007/s00205-021-01661-4](https://doi.org/10.1007/s00205-021-01661-4),
   [arXiv:2009.14291](https://arxiv.org/abs/2009.14291).
7. C. H. Chan and A. Vasseur, “Log improvement of the Prodi--Serrin criteria
   for Navier--Stokes equations,” *Methods and Applications of Analysis* 14
   (2007), 197--212,
   [DOI 10.4310/maa.2007.v14.n2.a5](https://doi.org/10.4310/maa.2007.v14.n2.a5),
   [arXiv:0705.3659](https://arxiv.org/abs/0705.3659).
8. S. Montgomery-Smith, “Conditions implying regularity of the three
   dimensional Navier--Stokes equation,” *Applications of Mathematics* 50
   (2005), 451--464,
   [DOI 10.1007/s10492-005-0032-0](https://doi.org/10.1007/s10492-005-0032-0),
   [arXiv:math/0301207](https://arxiv.org/abs/math/0301207).
9. J.-Y. Chemin, “Non linear equivalence of some scaling invariant norms for
   solutions of incompressible Navier--Stokes equations,” *Communications in
   Analysis and Mechanics* 17 (2025), 944--954,
   [DOI 10.3934/cam.2025038](https://doi.org/10.3934/cam.2025038).
10. T. Ogawa and Y. Taniuchi, “The limiting uniqueness criterion by vorticity
    for Navier--Stokes equations in Besov spaces,” *Tohoku Mathematical
    Journal* 56 (2004), 65--77,
    [DOI 10.2748/tmj/1113246381](https://doi.org/10.2748/tmj/1113246381).
11. Z. Lei and X. Ren, “Quantitative partial regularity of the Navier--Stokes
    equations and applications,” *Advances in Mathematics* 445 (2024), Article
    109654,
    [DOI 10.1016/j.aim.2024.109654](https://doi.org/10.1016/j.aim.2024.109654),
    [arXiv:2210.01783](https://arxiv.org/abs/2210.01783).
12. T. Tao, “Quantitative bounds for critically bounded solutions to the
    Navier--Stokes equations,” in *Nine Mathematical Challenges---An
    Elucidation*, Proceedings of Symposia in Pure Mathematics 104 (AMS, 2021),
    149--193,
    [DOI 10.1090/pspum/104/01874](https://doi.org/10.1090/pspum/104/01874),
    [arXiv:1908.04958](https://arxiv.org/abs/1908.04958).

## 8. Final freeze condition

After the five repairs in Section 3, the literature component can be marked
**PASS** for the limited purpose stated here: accurate primary-source support
and a conservative collision/non-collision boundary. That PASS would not audit
the manuscript's new analytic estimates and would not establish novelty,
priority, global regularity, or a solution of the three-dimensional
Navier--Stokes Millennium problem.

**NOT CLAY.**
