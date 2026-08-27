# R0.72M independent analytic audit

**Verdict:** PASS WITH QUALIFICATIONS
**Date:** 2026-08-27

The derivation was rebuilt from the phase-rotated lattice rather than from
the scalar ledger of R0.72L.  The following points are necessary for the
public claim.

1. The benchmark keeps every Fourier coordinate but deletes the diagonal
   heat term.  It must be called a zero-diffusion full-lattice reference, not
   an exact Navier--Stokes solution.
2. The launch signs are essential:
   \(f_1(0)=2^{-1/2}\) and \(f_{-1}(0)=-2^{-1/2}\).  They give
   \(f_n=\sqrt2J_n'(2s)\), not \(\sqrt2J_n(2s)\).
3. The Fourier-gradient identity is exactly \(1+s^2\).  It follows from
   the generating function and requires no finite cutoff.
4. The complete action integrand is
   \(q(s)=\langle A^{-1}Bf,Bf\rangle\), not \(|f_1|^2\).  Its constant is
   \(A_0=\int_0^\infty s^{-1/3}q(s)ds\).  The target row gives a lower
   component with the same exponent, but the constants must not be
   identified.  Decimal evaluations are corroboration only.
5. The factor in the cubic asymptotic is \(16/\pi^2\).  One factor four
   comes from the physical rows, while the mean of
   \(|u u'|\) contributes \(4/\pi^2\) per logarithmic scale.
6. The exact scalar superlevel set is an interval around \(H=U/V\).  The
   frozen family has \(x/H\to0\) and therefore stays in the action-poor
   \(Vx\)-branch; the optimized \(U\)-remainder is not sharp on it.
7. The three sufficient routes mentioned in R0.72L are not an exhaustive
   trichotomy.  Public text must not say that the cubic-improvement route is
   the only possible one.
8. The finite dissipative curves are diagnostic.  Neither agreement of two
   solvers nor apparent logarithmic growth proves a uniform infinite-chain
   bound.

The audit independently checked the Bessel recurrence, the generating
function, the Parseval moment, the negative-norm stationary-phase bound,
the critical-action change of variables, the scalar danger interval, and
the asymptotic mean of the absolute oscillatory product.  No exponent or
inequality-direction error was found after imposing the qualifications
above.
