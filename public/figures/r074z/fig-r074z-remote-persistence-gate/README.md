# R0.74Z Figure Archive — Remote Persistence Gate

This directory is a reproducible, journal-scale four-panel **analytic
schematic** for the revised R0.74Z cancellation-cell gate. It contains no
PDE simulation, DNS output, sampled stochastic trajectory, or empirical
fit. Every plotted number is regenerated from exact fractions in the bound
R0.74Z note.

The panels preserve the separation between exact results, conditional
implications, and open problems.

- **A — two fourth-root weight shifts:** the outer packet clock weight
  \(\Gamma=\gamma_{k_2}\), the remote clock weight
  \(\omega=\gamma_{k_2-1}=\Gamma^{1/4}\), and the doubled-radius payment
  weight \(\gamma_{k_2-2}=\Gamma^{1/16}\). The last shift follows from
  \(A_{k_2-1}(R)=A_{k_2-2}(2R)\).
- **B — strict persistence threshold:** the exact Hölder bound gives
  \(L^{-2}\log((P_R^M)^{2/3}/h)\ge
  \Delta_{\rm rem}-2\kappa/3+o(1)\). It proves exponential domination only
  for the strict region \(\limsup\kappa_L<\kappa_*\). The critical layer
  \(\kappa_L=\kappa_*+o(1)\) is open.
- **C — time-tame and complexity screen:** endpoint preservation upgrades to
  an \(R^3\) tube only conditionally on (Z.22) and a uniform moving-strip
  all-winding comparison. Within that model, endpoint-focused kinetic escape
  requires the necessary coefficient
  \(476239/1064835072\) in \(L^{-2}\log\mathcal N_L\); equality is not
  classified and the condition is not sufficient.
- **D — proof-status hierarchy:** common-shear admissibility and tube
  coercivity are proved; moving-strip persistence is conditional; the
  critical layer, accumulated clock rows, the full-clock Y.57 gate, and
  arbitrary exponentially ill-conditioned finite families remain open.

## Provenance and seal status

The archive binds three live inputs byte-for-byte:

- `research/r074z_cancellation_cell_gate.md`, SHA-256
  `bb766da4002da760c35185294081f80df97c349ea08b198a5f76db31663aaf6a`;
- `research/r074z_cancellation_cell_gate_primary_audit.md`, SHA-256
  `6b867551bce840cb382cd13cb2ff298affbf0c0d8b1357a8163c5cedc9bace08`,
  verdict PASS, blocker count 0;
- `research/r074z_cancellation_cell_gate_literature_audit.md`, SHA-256
  `8e5346ecf3c2beef4a620e0844e790703b628388ca7f0a6997aae88818caa82f`,
  a bounded dated primary-source non-hit only.

This is a local SHA-256 precommit seal. No Git commit/blob seal, novelty,
priority, full-clock Y.57 theorem, arbitrary-solution theorem, or Millennium
claim is made.

## Reproduction

```bash
CODEX_PYTHON=/path/to/bundled/python3
R074Z_DEPS_DIR=/path/to/version-pinned/dependencies
REPOSITORY=/path/to/navier-stokes-r074m
FIG=research/figures/r074z/fig-r074z-remote-persistence-gate
env PYTHONPATH="$R074Z_DEPS_DIR" "$CODEX_PYTHON" -B "$FIG/plot.py" --deps "$R074Z_DEPS_DIR" --repository "$REPOSITORY" --render
env PYTHONPATH="$R074Z_DEPS_DIR" "$CODEX_PYTHON" -B "$FIG/validate.py" --deps "$R074Z_DEPS_DIR" --repository "$REPOSITORY" --seal-local --confirm-visual-qa
env PYTHONPATH="$R074Z_DEPS_DIR" "$CODEX_PYTHON" -B "$FIG/validate.py" --deps "$R074Z_DEPS_DIR" --repository "$REPOSITORY" --verify-only
```

The validator recomputes the exact arithmetic, verifies all three live-source
hashes and byte counts, regenerates the source-data ledger, performs two clean
byte-identical renders, checks SVG/PNG/PDF structure, and writes the local
25-file archive seal. `SHA256SUMS` covers the other 24 files and excludes
itself to avoid a circular hash.

The research blossom is locked at the top-right. One navy root plus neutral
tones, hatch, line style, open fill, and direct labels retain meaning in
greyscale.

**ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS |
NO NOVELTY CLAIM | NOT CLAY**
