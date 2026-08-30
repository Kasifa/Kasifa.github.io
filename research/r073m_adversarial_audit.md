# R0.73M adversarial audit

**Audit date:** 2026-08-31

**Object:** the strongest claim in
`r073m_prescribed_action_departure_proof.md`

**Verdict:** **PASS**, subject only to the remaining non-mathematical release
gates

## 1. Is the real physical launch normalized only up to a hidden constant?

No.  Fourier-by-Fourier velocity energy equals kinetic \(L^2\) energy.
Normalized periodic integration removes the apparent \(x=2y\) Jacobian,
and the two conjugate rows are orthogonal.  The scalar and real-pair selected
gains are exactly equal.

## 2. Is the nonlinear coefficient missing a factor of four or \(\Lambda\)?

No.  Profile time is \(d=4t\), so both the linearized operator and quadratic
term carry \(1/4\).  In fast time \(d/\varepsilon\), the quadratic
coefficient would carry an additional \(\varepsilon\), but the proof stays
in profile time and never mixes that equation with physical amplitude.

## 3. Does R0.73L control the full nonlinear semigroup?

No, and the proof does not claim it does.  R0.73L is used only for one
endpoint-normalized selected \(K_z=\pm1\) orbit.  Generated rows are
controlled separately by exact row energy, the zero-row heat contraction,
the doubled-row \(1/3\) bound, and the universal nonzero-row \(1/2\) bound.

## 4. Could the narrow \(1/1500\) margin vanish under a coarse rate bound?

The auxiliary value \(0.16\) used inside the R0.73L adiabatic proof would
indeed fail.  R0.73M instead uses the independently certified R0.73J
continuum floor \(\lambda_0(d)>0.167\) together with the R0.73L action
quotient.  The three margins remain strictly positive.

## 5. Does the transfer lemma hide a \(\Lambda\)-dependent constant?

Its statement fixes \(D,\mu,C_a\) independently of \(\Lambda\) and fixes the
same two-harmonic background family.  The energy constants depend on these
fixed data and the strict margins, not on \(\Lambda\).  The error integrating
factor includes the complete \(e^{C\delta^2}\) contribution.

## 6. Could a constant mode invalidate Ladyzhenskaya?

No.  Although the quadratic term generates a \(K_z=0\) row, that row is a
zero-mean tangential heat shear.  Periodic divergence structure preserves
total mean zero for every coefficient and for the exact error.

## 7. Is the prescribed seed merely logarithmically matched?

No.  A logarithmic action limit would be insufficient.  R0.73L gives the
two-sided bounded prefactor

\[
 c_L\le G_\Lambda^*e^{-\Lambda\mathcal A_*}\le C_L,
\]

which is exactly what keeps the effective Taylor amplitude inside a common
interval.  No convergence of that prefactor is asserted.

## 8. Can the floor seed replace the full action seed?

No.  Since \(\mathcal A_*>0.167D_*\), the seed
\(\rho e^{-0.167\Lambda D_*}\) has an effective endpoint amplitude that
grows exponentially and leaves the uniform Taylor radius.  Conversely, an
exponent strictly larger than \(\mathcal A_*/D_*\) produces an endpoint
tending to zero within this construction.  The full integral action is the
licensed fixed-window recoding.

## 9. Does the \(H^3\) estimate apply to a different spectral vector?

No.  R0.73K continues the same rank-one top contour used in R0.73G.  The
fixed anchor only chooses its phase.  The elliptic eigenvector equation gives
the same \(O(\Lambda^2)\) cost after velocity recovery.

## 10. Is this instability of one fixed background?

No.  The background amplitude grows with \(\Lambda\), so the theorem is for
a family of exact solutions.  A sequence of perturbations of one fixed base
flow has not been constructed.

## 11. Does global smoothness help the three-dimensional Clay problem?

No.  It comes from exact invariance of a two-dimensional subsystem.  The
constructed orbit has no transverse component and no vortex stretching.
Global planar regularity supplies continuation for the example, not a
three-dimensional regularity theorem.

## 12. Can the finite diagnostic prove the continuum theorem?

No.  Its role is limited to checking implementation, action recoding,
harmonic parity, and finite convergence.  The continuum theorem rests on the
analytic action, row-coercivity, Stieltjes, and remainder estimates.  Any
finite mismatch must be reported, but a finite match cannot replace them.

## Final claim boundary

The strongest admissible claim is a prescribed-action, fixed-distance
nonlinear departure for a varying family of exact periodic backgrounds,
inside an exactly invariant and globally regular planar subsystem.
