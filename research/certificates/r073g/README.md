# R0.73G certificate package source

This directory contains the deterministic source for the R0.73G analytic and
finite-diagnostic certificate.  The analytic source is fixed at commit
21c11ba3eef7f2b5dc3f107957e0744a0471745d. The finite diagnostic and journal
figure are bound only during formal generation, using the full Git commits that
seal the R0.73G experiment outputs and the validated journal-figure package.
Neither commit parameter has a default.

The two generation paths independently bind immutable Git blobs and recompute
the following exact ledgers:

- the physical normalization \(x=2y\), \(d=4t\), and the matching heat and
  viscosity factors;
- the kinetic-to-velocity row isometry and real conjugate-pair normalization;
- the two elliptic lifts, \(H^3\) cost \(O(\Lambda^2)\), quadratic
  \(O(\Lambda^4)\) cost, and cancellation by the \(\Lambda^{-4}\) seed factor;
- the Riccati threshold, denominator \(3/4\), and comparison multiplier
  \(4/3<2\);
- the all-mode remainder and half-gain algebra, including both branches of
  \(M-(M-\kappa)_+\le\kappa\);
- the \(K_z=\pm1\) quadratic parity channels \(0,\pm2\);
- the zero vortex-stretching identity in the exact planar class;
- the exact CLOSED, FALSE, FALSE_AS_INFERENCE, and OPEN release ledger.

The finite package remains diagnostic only.  Its commit must preserve all eight
analytic source blobs and the analytic-source diagnostic script; record a
non-smoke run; contain the exact unique \(4\times7\) row grid and
\(3\times7\) adjacent-cutoff grid; cross-check the two Fourier kernels; and bind
the complete experiment manifest, SHA-256 ledger, command, environment,
progress log, CSVs, figures, and producer-independent validator source and
result.  Both certificate paths parse the committed CSVs, match them to the
summary, and recompute the kernel and independent-validation error thresholds
instead of trusting stored pass flags.  No cutoff agreement is treated as a
continuum tail estimate.

The required figure-package commit must descend from the experiment commit.
The certificate binds its complete fixed inventory and records the validated
PDF/SVG/600-dpi PNG as `journalFigure` after checking the figure manifest,
validation result, SHA-256 ledger, and explicit visual-QA pass.  The certificate
does not emit a `formalFigure` field.

Run from the repository root with both frozen 40-character commits:

    python3 -B research/certificates/r073g/generate_certificate.py \
      --experiment-commit EXPERIMENT_COMMIT \
      --figure-package-commit FIGURE_PACKAGE_COMMIT

    python3 -B research/certificates/r073g/independent_recompute.py \
      --experiment-commit EXPERIMENT_COMMIT \
      --figure-package-commit FIGURE_PACKAGE_COMMIT

    python3 -B research/certificates/r073g/validate_certificate.py \
      --experiment-commit EXPERIMENT_COMMIT \
      --figure-package-commit FIGURE_PACKAGE_COMMIT

The required parameters deliberately have no defaults and accept only full
lowercase 40-character commit hashes.  This prevents current uncommitted files
or a moving working tree from becoming a formal binding by accident.  The final
validator also requires fixed exact source, experiment, figure, check, and
claim-boundary key sets; missing keys and empty dictionaries fail closed.

The scripts use only the Python standard library.  Formal execution creates
certificate.json, independent_recompute.json, validation.json, progress.ndjson,
manifest.json, and SHA256SUMS.  The final ledger covers every regular file in
this directory except SHA256SUMS itself.

This is a provenance and exact-algebra consistency certificate.  The validated
journal figure remains presentation evidence for the finite diagnostic.  The
package does not machine-prove the prose PDE argument, turn finite Fourier or
figure evidence into a continuum theorem, establish order-one departure,
create three-dimensional vortex stretching, or resolve the Clay problem.
