# R0.71T certificate

This directory archives the exact producer and the independently reconstructed
R0.71T finite audits.

- `result.json` is produced by `research/r071t_exact_audit.py`.  It records
  the sparse Fourier seed, resonant precompensation normal form, simple-entry
  slope identity, outgoing coarea profiles, symmetric trace kernel,
  variable-denominator cancellation, and double-scaling ledger.
- `independent-result.json` is produced by
  `research/r071t_independent_audit.py`.  It imports neither the exact
  producer nor its output and reconstructs the finite checks using an FFT,
  adaptive quadrature, finite differences, and a direct frequency sweep.

The continuum internal-entry theorem uses the classical local NSE flow map
and a finite-dimensional implicit-function theorem.  That analytic argument
is written in `research/r071t_report-source.md`; the JSON files check its
finite Fourier and asymptotic algebra but do not replace it.

The exact internal scaling family first chooses base amplitude

\[
a_\lambda=\lambda^{-2}
\]

and then applies the compatible torus dilation

\[
u_\lambda(x,t)=\lambda u^{a_\lambda}(\lambda x,\lambda^2t).
\]

Its leading internal atom is proportional to \(\lambda^{-4}\), while the
bare normalized Leray--Lamb time budget is proportional to
\(\lambda^{-6}\).  The ratio grows as \(\lambda^2\), even though the initial
energy and critical norm tend to zero and the initial enstrophy stays bounded.

No repeated-entry packing, Leray-level occupation estimate, continuation
criterion, singularity, or global-regularity statement is certified here.
