# R0.73K finite diagnostic audit

**Verdict:** PASS / CLOSED

**Audit date:** 2026-08-31 (Asia/Shanghai)

**Scope:** reproducibility and internal agreement of the finite Fourier
diagnostic only

## 1. Preserved computation

The formal grid contains five cutoffs
\(N=24,48,96,128,160\), seventeen parameter nodes
\(d_j=j/7200\), twelve core viscosities from zero through \(10^{-3}\), and
two continuation stress viscosities.  The primary output contains 1,190
spectral states and 952 adjacent-cutoff comparisons.

The package preserves the producer and validator sources, configuration,
commands, environment, primary and independent outputs, progress streams,
resource streams, manifest, and sixteen SHA256 records.  The sealed-package
validator reports all nine checks true, including source/configuration binding,
schema agreement, checksum agreement, and complete monitoring logs.

## 2. Independent reconstruction

The independent validator does not import the producer.  It reconstructs the
matrix from the explicit Fourier coefficients of \(W_d\) and \(W_d''\), and it
uses a stable two-column QR core for the rank-one projector norm.  It reproduces
the complete formal grid and reports every discrete and numerical comparison
inside its declared tolerance.

The maximum absolute field discrepancy is
\(3.6637359813\times10^{-7}\), attained in a difference quotient after division
by a very small viscosity.  The maximum discrepancy in the eigenvalue real
part itself is \(1.0075273948\times10^{-14}\); the maximum projector-difference
discrepancy is \(4.8988590962\times10^{-14}\).

## 3. Finite observations

At \(N=160\) over the core viscosity grid:

- the selected eigenvalue remains real to numerical precision and stays in
  \([0.168207092942025,0.170407976920434]\);
- the minimum normalized left-right overlap is \(0.5939991104\), and the
  maximum rank-one projector norm is \(1.683504205\);
- the maximum \(\|P_\varepsilon-P_0\|\) is \(0.1806379812\);
- the maximum \(N=128\) versus \(N=160\) core eigenvalue difference is
  \(7.5858096641\times10^{-15}\), and the corresponding maximum embedded
  projector difference is \(5.6611745823\times10^{-14}\).

Across the full formal grid, the maximum right/left algebraic residuals are
\(1.5988786092\times10^{-14}\) and \(7.9543373299\times10^{-15}\).  The maximum
rank-one intertwining residual is \(2.3739285445\times10^{-14}\), while the
stable low-rank idempotency residual is at most
\(9.3355465449\times10^{-16}\).

## 4. Claim boundary

This audit establishes only that two finite implementations agree and that the
saved package is internally reproducible.  It does not certify the continuum
Riesz rank, operator-norm projection convergence, an explicit common viscosity
threshold, the reduced semigroup estimate, nonlinear stability, a
three-dimensional theorem, finite-time singularity, or the Clay problem.

The continuum theorem is supported separately by
`research/r073k_uniform_viscous_branch_proof.md` and its two analytic audits.
Finite success cannot repair an analytic gap; analytic success cannot excuse a
finite discrepancy.  Both gates are now closed independently.
