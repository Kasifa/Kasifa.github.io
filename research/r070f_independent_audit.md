# R0.70F independent internal audit

> **Audit date:** 2026-08-24
>
> **Final status:** PASS after correction
>
> **Scope:** mathematical consistency, primary-source boundaries, exact
> construction geometry, and claim calibration. This is an internal
> adversarial audit, not external peer review.

## 1. Audit disposition

Three audits were run independently against
`research/r070f_report-source.md`:

| audit | initial finding | correction | final status |
|---|---|---|---|
| Taylor/tensor ledger | the quadratic tensor constraints were omitted while the report claimed the first three jets were closed | added all symmetry, trace, divergence, and harmonic constraints for \(C_{ij\ell m}\) | PASS |
| construction/counterexample search | coarser carriers contribute constant filtered vorticity on the selected source band, so transition isolation alone did not imply (6.7) | retained that cross source and annihilated its core strain with a fixed radial partition and the Newton radial-shell lemma | PASS |
| primary-source and claim audit | three formulations needed sharper boundaries: Yu's unweighted estimate, Koch--Tataru uniqueness, and the two distinct tent norms | restricted the statements to Yu's dual-summability hypothesis, the small \(X\) class, and respectively the caloric initial-data and solution-space tents | PASS |

The initial failures are recorded because they are mathematically material.
The final PASS applies only to the corrected report snapshot locked by the
R0.70F certificate hashes.

## 2. Taylor and tensor audit

The scale ledger was recomputed from the degree-\(n\) Taylor field size
\(\theta^n r_j^{-3/2}S_{j,k}\) and Yu's extra normalized work factor
\(r_k/r_j=\theta\). The resulting powers are

\[
 \theta,\qquad \theta^2,\qquad \theta^3,\qquad \theta^4
\]

for the constant term, linear term, affine remainder, and quadratic
remainder. The explicit constant and linear contraction coefficients in
(6.9)--(6.10) were also recomputed and agree with the symbolic certificate.

For the quadratic coefficient, the corrected report now records

\[
 C_{ij\ell m}=C_{ji\ell m}=C_{ijm\ell},\quad C_{ii\ell m}=0,
 \quad \sum_i C_{ijim}=0,
 \quad \sum_\ell C_{ij\ell\ell}=0.
\]

These are exactly the symmetry, trace-free, divergence-free, and harmonic
constraints inherited from the exterior strain. They do not force the
zeroth or first enstrophy-moment pairings to vanish.

## 3. Construction audit and repaired cross source

The adversarial construction audit caught the main proof gap in the first
draft. On the \(R_n\)-source band, every coarser carrier \(V_{r_m}\),
\(m<n\), has constant filtered vorticity. It therefore remains inside
\(\psi_{j_n}\Omega_{\ell_n}\) even though it has no transition there.

The corrected proof closes this point without deleting the source:

1. the base mollifier is even, has unit mass, and is supported in \(B_1\);
2. one radial annular partition, independent of \(N\), has an explicit
   plateau covering the complete mollified generator transition;
3. all nonconstant target and finer sources lie in the inner hole, while
   coarser generators are curl-free on the selected band;
4. for a retained constant cross source \(a\psi_{j_n}e_1\), the Newton
   potential \(( -\Delta)^{-1}\psi_{j_n}\) is a regular radial harmonic
   function in the inner hole and hence constant there;
5. its induced velocity and strain vanish in that hole, whereas the selected
   generator produces the full filtered constant or linear core strain.

The support inequalities in (6.4), together with
\(\ell_n/R_n=\sigma/\Lambda<\delta\) and the \(\Lambda^2\) separation of
active generator bands, were checked against the nearest coarser and finer
scales. They are sufficient for (6.7). The formulas for \(b_n\), the two
positive work factors, and the uniform \(L^2\cap BMO^{-1}\) bounds then
follow as stated.

## 4. Primary-source audit

The corrected source boundary is:

- Yu's fixed-annulus harmonic expansion is a conditional module. The cited
  \(N\)-uniform unweighted estimate uses explicit dual sequence summability
  and is distinct from Yu's energy-level weighted estimate.
- Koch--Tataru supplies uniqueness in the small solution class \(X\), not an
  unrestricted uniqueness theorem for every possible weak solution.
- The \(BMO^{-1}\) initial-data norm is the tent norm of the caloric extension;
  \(X\) has an analogous but distinct spacetime tent component.
- The Wolf, Brandolese--Vigneron, Bradshaw--Tsai, and Eyink--Aluie citations
  are used only for the limited analogies identified in the report.

No audited primary source supplies the missing common-terminal-time raw
affine-jet packing theorem for arbitrary finite-energy Navier--Stokes
solutions.

## 5. Claim boundary

The exact family proves same-sign **initial-face** raw jet pairings with
uniform energy and critical control. It does not realize those pairings on
nested backward cylinders with one common positive terminal time.

The triangular sum proves failure only of a proof that takes absolute values
term by term and uses no information beyond bounded reservoir sequences. It
does not rule out cancellations in the true spacetime sum, adjacent-source
martingale differences, telescoping, a moment Carleson theorem, or a
conditional Besov mechanism.

Accordingly, the audit supports the stated R0.70F route-elimination result;
it supports no claim of large-data regularity, singularity, or resolution of
the Millennium problem.

## 6. Reproduction and figure QA

The exact SymPy certificate reproduces the compact-core polynomial
identities, work factors, and triangular sums. Its README explicitly lists
the analytic steps that are not computer-proved. The archived figure is an
exact-formula explanatory figure with PNG, PDF, SVG, source data, manifest,
validation, caption, and figure contract. It is not DNS or numerical PDE
evidence.

Run the focused gate with:

```sh
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node \
  --test tests/r070f-affine-jet-gate.test.mjs
```
