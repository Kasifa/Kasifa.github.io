# R0.73S finite quadratic-autocorrelation certificate

This package checks the finite identities used by R0.73S.  It uses only the
Python standard library and exact integer or rational arithmetic for every
pass/fail decision.  The analytic normalization is Haar probability measure
on \(\mathbb T^d\), so Parseval carries constant one.

## What is certified

- for five independent integer coefficient fields,
  \(\|f\|_6^6\le\|C\|_1\|C\|_2^2\),
  \(\|C\|_1\le M\|f\|_2^2\), and
  \(\|C\|_1^2\le D_C\|C\|_2^2\);
- the selected-shift magnitude-tail upper contract;
- the exact bounded, asymptotically fixed-quartic Dirichlet-spike formulas on
  six square values of \(m\), including the \(D_C^{1/2}\) obstruction; the
  separate algebraic tuning with \(\Gamma\equiv5/3\) belongs to the continuum
  proof and is not claimed by this finite grid;
- an explicit two-component real lift audit: conjugate symmetry,
  \(k\cdot\widehat V(k)=0\), \(M=2m+2\), \(D_C=4m-1\),
  \(D_\Delta=10m-1\), and \(32m\le|k|<36m\);
- exact Dirichlet and Rudin--Shapiro fourth/sixth moments and the
  autocorrelation proxy on the configured R0.73R matched grid;
- the exact no-go seed \((5,37,311)\) versus \((5,37,323)\), no-carry formula
  rows through depth eight, and direct polynomial reconstruction at depths
  two and three;
- an independent reconstruction using binary-parity Rudin--Shapiro signs and
  ordered-sum counts.

## What is not certified

This package does not integrate the heat flow, simulate Navier--Stokes,
certify the continuum PDE proof, establish a runtime lower bound, prove
singularity or global regularity, or solve the Clay problem.  The harmonic
analysis inequality is classical; the package only certifies the finite
formulas and examples used in the R0.73S shell assembly.

## Reproduction

Run the pre-seal commands in `command.txt` from the repository root.  A run
without `--source-commit` creates a deterministic `hash-bound-uncommitted`
manifest.  Only after all nine source files have been committed should the
same script be rerun with the full lowercase 40-hex commit.  That final stage
reads each source blob from Git and requires byte identity before setting
`finalSeal=true` and `status=sealed`.

GPU and DGX resources are intentionally unused: the configured workload is
small, exact, and CPU-bound.
