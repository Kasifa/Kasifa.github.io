# R0.72E certificates

This directory archives two independent finite audits for the fixed-\(q_0\)
one-carrier supercritical root ledger.

- `result.json` is produced by `research/r072e_exact_audit.py`. It starts from
  \(q_0=4\), recomputes the physical amplitude and data ledger, evaluates the
  frozen Bessel roots for \(R=8,16,32,64\), and estimates the full
  negative-Sobolev action for \(\delta=16,\ldots,512\) with a Strang
  split-step Fourier method.
- `independent-result.json` is produced by
  `research/r072e_independent_audit.py`. It imports neither the producer nor
  its output. It finds the roots by an unseeded fixed-step real-lattice RK4
  scan and estimates the action with an adaptive BDF solve using an analytic
  sparse tridiagonal Jacobian.
- The `*-progress.ndjson` files are timestamped solver logs. The matching
  `*-resource.ndjson` files record elapsed time, CPU time, peak resident
  memory, and logical CPU count. The monitor logs preserve the stderr stream.
- `config.json`, `command.txt`, `seed.txt`, and `environment.txt` record the
  declared inputs and runtime. `SHA256SUMS` is generated after the package is
  complete.

Both audits reconstruct the three fixed-scale factors in the physical
rotational-charge estimate: the negative-Sobolev weight, the physical-time
Jacobian, and the shear-enstrophy denominator each contribute \(q_0^{-2}\).
They also reconstruct the exact data formula and the exponent ledger
\(\delta^{1/3}=R^{4/3}\).

The analytic report is primary. These binary64 computations are not
directed-rounding interval proofs. The Bessel calculation is frozen, the
evolutions use finite Fourier lattices, and the tested coupling grids are
finite. They corroborate signs, normalizations, convergence, and scaling;
they do not prove the Kusuoka--Stroock density input, infinite-lattice root
persistence, three-dimensional Navier--Stokes regularity, or singularity.
