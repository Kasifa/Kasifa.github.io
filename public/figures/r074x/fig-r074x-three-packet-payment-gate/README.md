# R0.74X Figure Archive — Three-Packet Payment Gate

This directory is a reproducible, journal-scale four-panel **analytic
schematic** for the R0.74X three-packet fixed-deletion gate. It contains no
PDE simulation, DNS output, or sampled stochastic trajectory. Every plotted
number is regenerated from exact fractions in the bound R0.74X note.

The four panels separate what is proved from the remaining gate.

- **A — packet and clock geometry:** packets at
  \(k_1,k_2=k_1+1,k_3=k_1+2\), with packet 2 witnessing the adjacent-inward
  coordinate \(k_1\) and packet 3 witnessing \(k_2\). The two strip
  calculations are lower-bound witnesses only, not whole-shell upper bounds.
- **B — different-time pigeonhole:** for each fixed deletion set
  \(S\), \(\#S\le1\), the time is selected afterwards. If \(k_1\) remains,
  use \(\tau_2\); if \(k_1\) is deleted, \(k_2\) remains and one uses
  \(\tau_3\). No common-time hypothesis is required, although an optional
  schedule may choose \(\tau_2=\tau_3\).
- **C — payment-rate gap:** the forced exterior-payment exponent
  \(3306805/134120448\) is compared with the largest audited W-strip exponent
  \(16\chi(66)\). Their strictly positive gap is
  \(3062597/134120448\). Hence the two actual strip witnesses are negligible
  relative to \((P_R^M)^{2/3}\); this does not control full shell clocks.
- **D — conclusion hierarchy:** the two-coordinate obstruction relative to
  \(T_*\) is proved; an actual counterexample to the payment-normalized gate is
  not proved; the equal-target W-strip route is a cubic-payment no-go; the next
  proposition is the payment-compatible target X.52.

## Provenance and seal status

The archive binds three uncommitted live inputs byte-for-byte:

- `research/r074x_three_packet_fixed_deletion_gate.md`, SHA-256
  `4fdc9558605afd9557c557c4292ca1af50d52ff54f9aa11603f15c97a97b3ee3`;
- `research/r074x_three_packet_fixed_deletion_gate_primary_audit.md`, SHA-256
  `834ec846c3f8629f9e7462caf4503bfa99ba6b88288da2dd525793206de9357e`,
  verdict PASS, blocker count 0;
- `research/r074x_three_packet_fixed_deletion_literature_audit.md`, SHA-256
  `f58f7a1d095ba6bd8b27c41872301fd367fe784597160fe060f9cd332c64c422`,
  a bounded dated primary-source non-hit only.

This is a local SHA-256 precommit seal. No Git commit/blob seal, novelty,
priority, whole-shell estimate, arbitrary-solution theorem, or Millennium
claim is made.

## Reproduction

```bash
CODEX_PYTHON=/path/to/bundled/python3
R074X_DEPS_DIR=/path/to/version-pinned/dependencies
REPOSITORY=/path/to/navier-stokes-r074m
FIG=research/figures/r074x/fig-r074x-three-packet-payment-gate
env PYTHONPATH="$R074X_DEPS_DIR" "$CODEX_PYTHON" -B "$FIG/plot.py" --deps "$R074X_DEPS_DIR" --repository "$REPOSITORY" --render
env PYTHONPATH="$R074X_DEPS_DIR" "$CODEX_PYTHON" -B "$FIG/validate.py" --deps "$R074X_DEPS_DIR" --repository "$REPOSITORY" --seal-local --confirm-visual-qa
env PYTHONPATH="$R074X_DEPS_DIR" "$CODEX_PYTHON" -B "$FIG/validate.py" --deps "$R074X_DEPS_DIR" --repository "$REPOSITORY" --verify-only
```

The validator recomputes exact arithmetic, checks the three live-source
hashes, audits the source-data ledger, performs two clean byte-identical
renders, inspects SVG/PNG/PDF structure, and writes the local 25-file archive
seal. `SHA256SUMS` covers the other 24 files and excludes itself to avoid a
circular hash.

The research blossom is locked at the top-right. The palette uses one navy
root plus neutrals; fill, hatch, line style, marker, and direct labels retain
meaning in greyscale.

**ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS |
NOT CLAY**
