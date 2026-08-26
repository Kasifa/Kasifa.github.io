# R0.72C claim--evidence gap matrix

**Date:** 2026-08-27

| Claim or target | Status at R0.72C | Evidence | Remaining gap |
|---|---|---|---|
| Extend R0.72B to arbitrary physical Fourier phases | Proved for the conjugate-paired operator: scalar slope for every real \(\delta\), target-row mass for \(\delta\ne0\) | r072c_report-source.md, Sections 1--2; 12/12 producer and 11/11 independent checks | Naive complex coefficients in the old symmetric-shift formula are invalid; \(\delta=0\) gives only the scalar slope statement |
| Show that naive complexification can break the energy law | Proved | One-carrier \(w=i\) matrix witness and explicit positive energy derivative | This is a model-correction witness, not an NSE instability |
| Preserve the target-row norm, \(q_\rho\le3\), and mixed-exposure constant | Proved analytically and machine-checked | Explicit conjugate row coefficients, dissipation pairing, heat-semigroup estimate, finite-matrix checker | No gap inside the declared carrier class |
| Couple phase cancellation to multiplier-to-moment gain | Proved | Joint inequality \(\chi_A(\Omega_A^2/K_v)^{1/3}\le(\rho_A^2/K_v)^{1/3}\) | No gap inside the declared carrier class |
| Uniform arbitrary-phase exact-launch prefactor | Proved: \(O(M^{-8/3})\) | Distinct positive carriers, comparable moduli, \(K_s\ge M^3/3\) | It is an upper-ledger coefficient, not actual root-mass sharpness |
| Exclude a phase-uniform \(O(M^{-10/3})\) rate | Proved | Odd-generation Rudin--Shapiro family gives exact \(\chi_0=1/4\) and \(\Phi_{0,M}\asymp M^{-8/3}\) | Does not prove the full normalized ledger stays nonzero |
| Fixed positive observation prefactor | Proved: \(O(M^{-3})\) | Heat participation sum \(H_M(A_*)=O(1)\) | Applies after \(A_*\); the pre-ledger remains |
| Sharpness of the fixed-positive exponent | Proved for the algebraic prefactor | Same-sign \(r_l=l\) family gives an exact \(M^{-3}\) asymptotic | Not a lower bound on the root ledger |
| Intermediate burn-in transition | Proved | Gaussian sum asymptotics and Riemann sums | Constants depend on the stated \(A_{0,M}\) scaling |
| Arbitrary-phase exact-launch sufficient region | Proved as an upper region | \(\alpha<\min\{2,(8+3\beta)/7\}\) | Equality and exterior are not converses |
| Distinguish fixed effective coupling from fixed raw coupling | Proved algebraically | At fixed \(\delta\), \(\eta^{4/3}\Phi=|\delta|^{4/3}(M/K_s)\rho_A^2K_v^{-1/3}\) | The exposure bracket can still depend on phase |
| Fixed-positive-time sufficient region | Proved as a tail upper region | \(\alpha<\min\{9/4,(9+3\beta)/7\}\) | Does not pay roots accumulated before burn-in |
| Rudin--Shapiro recurrence and flatness input | Literature-checked, reproved, and independently checked | Erdelyi 2023 and Balister 2019; direct parallelogram proof; recursive and binary-parity code paths | No gap for the odd dyadic subsequence used here |
| Nonautonomous enhanced dissipation for the heat-decaying phase family | Not proved | Bounded primary-source audit | Uniform critical count, sublevel constants, onset prefactor, and freezing error remain unavailable |
| Actual phase-cancelled root-ledger lower family | Open | No certified launch/coupling/root/charge construction | This is the next dynamical gate |
| General three-dimensional NSE continuation or regularity | Not claimed | None | The triangular 2.5D class does not represent general vortex stretching |

## Publication gate

**Status: passed on 2026-08-27.** R0.72C entered the completed-release
manifest only after all of the following passed:

1. the high-precision producer reconstructed every theorem constant and phase
   boundary from raw parameters (12/12 checks);
2. the independent implementation checked skew-adjointness, the two
   Rudin--Shapiro generators, exact launch, heat burn-in, and finite matrices
   (11/11 checks);
3. the formal figure package included source data, code, vector exports, 600
   dpi PNG, manifest, checksums, progress, and 15/15 visual/data QA checks;
4. the reader-facing note, synchronized PDF, 93-node cumulative recap,
   homepage route, literature page, and English dictionary agreed;
5. the latest-release gate, publication invariant, internal-link tests,
   bilingual tests, build, lint, and full 915-test suite passed; and
6. every statement distinguishing upper-prefactor sharpness from actual
   root-ledger sharpness remained explicit.

## R0.72D finite gate

The next section should take one of two auditable branches.

1. **Dynamical lower family.** Specify \(F_M(0)\), \(\delta_M\), \(I_M\),
   the exact target roots, the complete root-slope mass, and the full
   \(\Lambda_1\) charge for a phase-cancelled profile; prove a nonvanishing
   normalized lower bound.
2. **Stronger dynamical exclusion.** Use evolution information beyond the
   static coefficient \(\Phi_{A,M}\) to exclude all phase-cancelled
   comparable-modulus families in a larger quantified region.

The required diagnostic tuple remains

\[
(\eta_M,L_M,n_M,c_{{\rm sub},M},
L_M\kappa r_{\max,M}^2,N_{\rm eff},\chi_M,\Theta_M,\Xi_M).
\]

A fitted exponent, FFT maximum without a norming bound, or terminal energy
plot is not a proof of either branch.
