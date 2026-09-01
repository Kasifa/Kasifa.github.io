# R0.73Y-A exact shear deterministic certificate

**Status:** `PASS`

**Scope:** exact Fourier and structural audit of the shear
\(u=Ae^{-\nu n^2t}\sin(nx_2)e_1\), plus an independent direct Gaussian
convolution cross-check.  This is not a PDE simulation and numerical values
are not used as proof.

## Reproduction

```bash
python3 scripts/r073y_exact_shear_certificate.py --check-only
```

## Exact rows

The script checked the following rows in the exact Fourier group algebra
\(\mathbb Q[\rho][\mathbb Z]\), or by an exact tensor/parity support audit:

- `nse_heat_residual`
- `divergence_and_convection`
- `heat_filtered_velocity`
- `subfilter_stress`
- `Pi_pointwise_zero`
- `centered_production_pointwise_zero`
- `gradient_covariance`
- `global_fixed_scale_trace_ledger`

The certified stress is

\[
 \tau_{11,s}={b^2\over2}
 [(1-\rho^2)+(\rho^2-\rho^4)\cos(2nx_2)],
\]

and the certified positive covariance is

\[
 D_{ii,s}={b^2n^2\over2}
 (1-\rho^2)(1-\rho^2\cos(2nx_2)).
\]

The exact support audit gives \(\Pi_s=0\), while Gaussian oddness in the
unused \(y_1\) direction gives \(\mathscr S_s=0\).

The analytic note proves a broader orthogonal shear class.  This certificate
deliberately audits only the explicit single-sine witness and does not present
the general-profile theorem as executable coverage.

## Independent numerical row

Dependency-free adaptive Simpson integration directly evaluated the
one-dimensional Gaussian convolution on five fixed parameter cases.  The
maximum scaled discrepancy across \(P_s\sin\), \(P_s(\sin^2)\), \(\tau\),
\(D\), and the odd Gaussian moment was `1.286e-13`.

This finite comparison is only a cross-check of the implementation.  The
universal cutoff/path quantifiers, strict positivity, and the no-go theorem
come from the analytic proof.

## Homogeneity degree ledger and quantifier boundary

The following degrees are proved in the analytic note.  This certificate
records them and checks their target values for internal consistency; it does
not independently derive them by symbolic exponent propagation.

- \(\mathcal E\) has amplitude degree 2, so
  \(\mathcal E^{3/2}\) has degree 3.
- \(\mathcal G_u\), \(\mathcal G_p\), and \(\mathcal H_u\) each have
  amplitude degree 3; therefore \(\mathcal A_{\rm ext}\) has degree 3.
- Pointwise zero production remains zero under every scalar cutoff and every
  positive heat-scale path.
- An arbitrary scale path is not automatically a descending heat
  characteristic in the ledger.
- Absolute endpoint, cutoff, and viscous-boundary debts are not claimed to
  vanish.  Criteria that include those debts or positive \(D_{ii,s}\) are
  not refuted.

`payload_sha256=51f721cf560df38fbeacdd093d4293adae10635e13dcaa6b9251616c4f7eca2c`

**NOT CLAY.**
