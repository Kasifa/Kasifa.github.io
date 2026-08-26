# R0.71V certificate

This directory archives two separate finite audits for the R0.71V
level-boundary and repeated-root release.

- `result.json` is produced by `research/r071v_exact_audit.py`. It checks the
  weighted area formula symbolically, the quadratic-to-cubic Jacobian, the
  exact sine boundary stress, the NSE scaling ledger, a 90-digit \(N=3\)
  recurrence tangent, the mollifier order of limits, and the limiting
  \(N=2\) high-frequency profile.
- `independent-result.json` is produced by
  `research/r071v_independent_audit.py`. It imports neither the exact producer
  nor its output. It uses a fresh binary64 response solve, Brent branch
  inversion, adaptive quadrature, an independent area test, and finite-\(q\)
  power fits.

The scripts do not replace the analytic proofs. The Leray--Hopf excursion
packing theorem, the fixed-level trace boundary, the exact 2.5D invariant
reduction, the Chebyshev interpolation, and the diagonal implicit-function
argument are proved in `research/r071v_report-source.md`.

The certificate supports a fixed-target, fixed-window sequence of exact
smooth unforced 2.5D NSE solutions for which a prescribed second atom divided
by the selected target shell's first-time row grows like \(q^2\). It does not
reject an estimate retaining the complete global \(\nu^2\) baseline or other
shell charges. No weak zero-jet definition, continuation criterion,
finite-time singularity, global regularity, novelty, or priority statement is
certified.
