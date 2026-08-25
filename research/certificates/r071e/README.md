# R0.71E exact-certificate bundle

This directory archives the exact producer and independent checker for the
R0.71E projected-Lamb heat-bulk gate.

## Decision locked by the bundle

1. With (L=\mathbb P(u\times\omega)), the filtered vorticity equation is

   \[
   (\partial_t-\nu\partial_s)W_{j,s}
   =\nabla\times(A_{j,s}L).
   \]

   Stretching and the transport-filter commutator are one combined shell
   work.  The remaining Lamb component is curl free.
2. For a tight real-even frame,

   \[
   \int_0^\infty\Theta_s^2\,ds
   \le\frac12\|(-\Delta)^{-1/2}L\|_2^2
   \le\frac12\|u\|_4^4.
   \]

3. After division by enstrophy, the vertical bulk is integrable on every
   finite time interval from the Leray energy inequality.
4. The exact smooth six-mode 2D3C datum

   \[
   u_\sigma=(0,-2\cos x_1,
   2\sigma\sin(x_1+x_2)-2\cos x_2)
   \]

   has identical quadratic spectra for (sigma=\pm1) and combined work
   (2\sigma).
5. A Parseval-preserving two-radius split and the phase (sigma=-1) give

   \[
   q_{\rm lo}(0)
   =2K^2\int_0^\infty q_{\rm lo}(s)\,ds,
   \]

   so the bottom trace costs exactly two frequency powers.
6. Pressure is the Bernoulli gradient complement in the vorticity ledger.
   It is not a third independent injection sector.  A strain ledger still
   retains pressure and subgrid boundary terms.

These statements close the normalized heat bulk but not its bottom trace.
They prove no singularity, unconditional regularity theorem, or
Millennium-problem solution.

## Files

- `result.json` - canonical sorted JSON emitted by the Fourier producer;
- `independent-result.json` - independent real-space reconstruction;
- `command.txt` - exact reproduction commands;
- `environment.txt` - pinned runtime and dependency record;
- `SHA256SUMS` - hashes for every archived payload and source dependency;
- `../../r071e_exact_audit.py` - producer;
- `../../r071e_independent_audit.py` - independent checker;
- `../../r071e_report-source.md` - analytic report;
- `../../r071e_literature_audit.md` - primary-source claim ledger;
- `../../r071e_independent_audit.md` - independent manual audit.

## Reproduction boundary

The programs certify the finite Fourier convolution, physical-space
reconstruction, Hodge split, heat spectral factor, exact trace relation, and
whole-space scaling exponents.  The general Sobolev interpolation, Leray
energy step, local packing estimate, pressure/SGS representation, and
literature comparison are proved or documented in the report.

No DNS, stochastic search, GPU, network, or DGX resource is required.
