# R0.73K gap matrix

**Status:** release claims closed; explicit threshold and downstream dynamics
remain open

| ID | Claim | Evidence route | Current state | Cannot be supplied by |
|---|---|---|---|---|
| K0 | one simple rightmost inviscid branch on \([0,1/450]\) | sealed R0.73J continuum theorem and interval certificates | CLOSED upstream | a new viscous truncation |
| K1 | joint strong base-resolvent and adjoint convergence | common \(H^2\) core and uniform multiplier estimates | CLOSED; analytic audit PASS | pointwise-in-\(d\) convergence |
| K2 | uniform compact sandwiches | norm-continuous collectively compact family \(K_d\) | CLOSED; analytic audit PASS | strong convergence alone |
| K3 | common viscous contour, rank one, projection norm convergence | Fredholm factor and analytic base cancellation | CLOSED; both audits PASS | Kato full norm-resolvent theory |
| K4 | \(\sup_d|\lambda_\varepsilon-\lambda_0|\le C\varepsilon\) | smooth inviscid left vector; move \(L\) onto it | CLOSED after domain repair | projection \(o(1)\) alone |
| K5 | real-analytic branch, fixed anchor, uniform overlap and \(P'\) | antiunitary symmetry, type-A family, Riesz formula | CLOSED; both audits PASS | finite eigenvector tracking |
| K6 | only the selected branch in \(\operatorname{Re}z\ge0.12\) | compact rectangle plus both high-frequency tails | CLOSED; analytic audit PASS | local Riesz circle |
| K7 | uniform reduced resolvent and complement semigroup | analytic removal plus full vertical line and inverse Laplace | CLOSED after Bromwich repair | spectral gap alone |
| K8 | explicit numerical \(\varepsilon_K\) | quantitative Fredholm inverse and convergence moduli | OPEN, outside release claim | qualitative compactness |
| K9 | finite branch/cutoff/conditioning diagnostic | 1,190 primary and independently reconstructed states; 952 cutoff comparisons; sealed logs, environment, manifest and SHA256 ledger | CLOSED; package audit PASS | continuum theorem status |
| K10 | nonselfadjoint adiabatic tracking on \(D_*/\varepsilon\) | graph/domain-controlled moving evolution | OPEN for R0.73L | instantaneous spectral data |
| K11 | two-sided matching action and bounded prefactor | K10 plus higher branch regularity | OPEN | eigenvalue integration alone |
| K12 | nonlinear and three-dimensional closure | nonlinear estimates and transverse modes | OPEN | any result in R0.73K |

## Fail-closed release rule

K1--K7 may be changed to `CLOSED` only after the proof text passes an
independent line-by-line audit and a separate adversarial audit.  K9 may be
closed only after raw outputs, environment, progress log, configuration,
checksums, and an independently implemented reconstruction are preserved.
Failure of K9 does not refute the continuous theorem, but it blocks release
until the discrepancy is explained.  Success of K9 does not repair a failure
of K1--K7.
