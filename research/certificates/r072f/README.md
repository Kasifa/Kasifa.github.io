# R0.72F certificate package

This package corroborates the finite computations used in R0.72F.  The
producer evolves the complex Fourier lattice by a split-step method; the
independent audit evolves a real invariant lattice by implicit BDF and uses a
different quadrature.  Neither program imports the other or reads the other
result.

The checked finite statements are:

1. the weighted actions are positive and follow the normalizations
   \(Q_{\beta,\gamma}\delta^{1-\beta}/(\log\delta)^\gamma=O(1)\) on the
   declared grid;
2. the critical weight has squared \(L^2(0,1)\) norm 75;
3. the frozen Bessel selected mass approaches \((8/\pi^2)\log R\);
4. the three rational repair vertices lie on the selected-family frontier;
5. discretization, lattice-radius, tolerance, tail, and quadrature pressure
   checks pass.

The package does not prove an infinite-lattice estimate, a complete-root
upper bound, a continuation criterion, or Navier--Stokes regularity.  Those
boundaries are machine-readable in both result files.

The positive-\(\beta\) free-amplitude frontier and the \(\beta=0\) endpoint
are recorded separately in `config.json`; the latter carries an additional
logarithm and is not obtained by direct substitution into the former.

Run the exact commands in `command.txt`.  `producer-progress.ndjson` and
`independent-progress.ndjson` are the process monitors; the matching resource
logs record CPU time, peak RSS, and logical CPU count at every stage.
`environment.txt`, the two concise monitor logs, and `SHA256SUMS` complete the
reproducibility envelope.
