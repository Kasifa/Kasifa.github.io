# R0.72W exact-tail periodic transfer figure

This source-only package specifies the formal R0.72W double-column journal
figure. It separates three evidence types:

- exact coefficient geometry and scalar-gauge-invariant obstruction ratios;
- the analytic compact-versus-escaping argument and exact-cell globalization;
- a deterministic Fourier/Strang forward--adjoint propagator diagnostic with
  simultaneous spatial and temporal refinement.

The bound analytic report proves that global term-by-term absorption of
\(H_5,H_7\), and the exact tail is false. It instead retains the exact
trigonometric potential and proves the unit-cell, whole-line, expanding-torus,
and scalar-row block-contraction statements. Outer-time concatenation,
nonlinear Navier--Stokes closure, and the Clay problem remain open.

Panel C is a numerical PDE stress test, not evidence used by the proof. It
does not compute the nonconstructive analytic constant \(C_T\), establish an
optimal propagator norm, or certify the functional analysis. The formal
renderer uses NumPy float64/complex128, the full exact potential, fixed
trigonometric initial vectors, no randomness, and a forward--adjoint audit.

The only command permitted at the source stage is:

    python3 scripts/generate_r072w_figure.py --self-test

It constructs 729 analytic rows and the drawing scene in memory and writes
nothing. Draft and formal rendering require the source-bound formal R0.72W
certificate. Formal rendering additionally requires a distinct clean
certificate commit, explicit visual inspection, and absent output targets.
