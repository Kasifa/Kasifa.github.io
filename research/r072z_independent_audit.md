# R0.72Z independent audit synthesis

**Date:** 2026-08-28

## Decision

The scoped R0.72Z theorem package is internally consistent after one
important wording correction: the \(2/5\) gap exponent is sharp for the
unweighted instantaneous \(L^2_q\) coercivity class, not for every possible
Orr--Sommerfeld stability theorem.  The frozen report uses the scoped
version.

## Cross-check ledger

| Item | Result | Evidence |
|---|---|---|
| pressure commutator and sign | PASS | independent operator derivation |
| self-adjoint form (H) | PASS | adjoint and Fourier matrix checks |
| (g^{-5/2}) sufficient bound | PASS | operator factorization |
| low-gap (g^{-5/2}) sharpness | REJECTED | actual fixed-low-mode power is (g^{-3/2}) |
| high-gap exponent (2/5) sharpness | PASS, SCOPED | two independent Fourier-pair sequences |
| exact tangent residual | PASS | direct substitution |
| forced OS kernel powers | PASS | independent energy/duality arithmetic |
| kinetic orientation normalization | PASS | velocity recovery recomputation |
| exact Squire induced norm | PASS | operator-norm calculation |
| angle bound with Λ payment | PASS | parameter identity |
| bound from (c) alone | REJECTED | γ=0 lift-up boundary |
| ordinary and strong history kernels | PASS | convolution recomputation |
| equal-rate transient | PASS | exact limiting integral |
| full physical direct sum | NOT PROVED | row weights remain |

## Publication boundary

The public note may state:

1. a signed high-gap prefactor-one (L^2_q) theorem;
2. a scale-sharp exponent for that declared coercivity class;
3. exact low-gap/tangent negative witnesses;
4. exact orientation-paid Squire history estimates;
5. fixed-row OS--Squire graph regularity.

It may not state:

1. a complete low-gap OS propagator;
2. a row-uniform physical kinetic-energy theorem;
3. a complete linearized direct sum;
4. any nonlinear or Clay conclusion.

Detailed calculations are retained in
`research/r072z_os_independent_audit.md` and
`research/r072z_squire_independent_audit.md`.
