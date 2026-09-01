# R0.73Z covariance certificate report

**Status:** PASS

**Role:** exact normalized Fourier-algebra and lacunary-arithmetic
cross-check.  The analytic notes carry the proofs and quantifiers.

## Exact crossed-family checks

- nse_residual_zero: PASS
- cross_stress_tau12_zero: PASS
- signed_production_zero: PASS
- third_central_flux_divergence_zero: PASS
- centered_production_zero: PASS
- pressure_covariance_q1_formula: PASS
- pressure_covariance_q2_formula: PASS
- pressure_covariance_q3_zero: PASS
- pressure_covariance_nonzero: PASS
- gradient_covariance_formula: PASS
- gradient_covariance_nonzero: PASS
- subfilter_energy_formula: PASS

The exact lane uses the finite group algebra
\(\mathbb Q[i][A,B,r][\mathbb Z^2]\), with
\(r=e^{-n^2s}\) after normalizing \(n=1\).

It verifies the Navier--Stokes residual, zero cross stress, zero
signed production, zero centered production, the two explicit
pressure-covariance components, the gradient-covariance formula,
and the subfilter-energy formula.

## Endpoint arithmetic

The smooth one-mode energy, normalized by \(\pi^3\), is
\(4+2=6\), independent of frequency.  For the exact lacunary
choice \(N_j=8^j\), \(a_j=2^{-j}\),
\(\sum_j a_j^2=1/3\) while \(a_j^3N_j=1\) for every \(j\).
Thus the executable reproduces the finite-energy/divergent-lower-
sum arithmetic used in the analytic proof.

## Claim boundary

- No numerical result is used as proof.
- Interior suitable-weak finiteness remains open.
- Local CKN coercivity and epsilon regularity remain open.
- This certificate does not solve the Clay problem.

Payload SHA-256: f580d3fb72d661c5aeec51299ca54f72d6645e18f02c9890012441b9d63cf55a

**NOT CLAY.**
