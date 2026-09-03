# R0.74W Figure Archive — Remote Adjacent-Inward Threshold

This directory is a reproducible, journal-scale four-panel **analytic
schematic** for the R0.74W remote adjacent-inward comparison.  It contains no
sampled trajectories, no PDE simulation output, and no DNS output.  Every
number drawn in the figure is regenerated from exact constants in the bound
R0.74W note.

The panels encode four distinct layers of the argument:

- **A — physical-shell geometry:** the adjacent inward annulus, its outer
  radius \(pL_mR\), the remote width-\(R\) strip, and the displaced packet
  centre \(h_m=c_hL_mR\).  The cross-section is intentionally not to scale.
- **B — sharp logarithmic rate:** \(q(\ell)=p^2/(4\ell)\) on
  \(64\le\ell\le65\), with the uniform survival and sweeping endpoint tests.
  Inside the narrow \(q_{65}\)--\(q_{64}\) band, a sequence with fixed limiting
  \(\ell\) is classified by strict comparison with \(q(\ell)\); only equality
  and its critical law remain open.  The original-scale packet rates
  \(\rho_1=1/320\) and \(\rho_2=1/1280\) are marked.
- **C — proof map:** exact all-winding conditional-bridge disintegration,
  central-bridge deficit localization, displacement comparison, and the
  retained noncentral winding remainder.  It is a deterministic diagram, not
  a picture of simulated Brownian paths.
- **D — weighted endpoint consequence:** the leading analytic factor
  \(L^{-1/2}e^{\chi(65)L^2}\) is displayed on a logarithmic scale.  The proved
  lower bound additionally contains an unspecified prefactor \(c>0\) and
  \(-CL\), so the plotted curve is not asserted to be a finite-\(L\) certified
  lower value.  The all-shell \(O(T_*)\) upper bound fails for the frozen
  placement; fixed deletion remains open.

## Provenance and seal status

The archive binds the live bytes of three uncommitted research inputs:

- `research/r074w_remote_adjacent_inward_comparison.md`, SHA-256
  `d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10`;
- `research/r074w_remote_adjacent_inward_comparison_primary_audit.md`,
  SHA-256
  `66ec78f67bba64c555a92e9a616c477d702ebb200b48bbfc08a353bdfde5bb73`,
  with recorded verdict PASS and blocker count 0;
- `research/r074w_remote_adjacent_inward_literature_audit.md`, SHA-256
  `ec6259d95990fd6a8357d9685cc3f17e300e672c1add911a5eb64c6291f3bb99`.

This is a **local SHA-256 precommit seal**, not a Git commit/blob seal.  No
figure-source commit has been assigned.  The R0.74W independent proof audit is
locally hash-bound with verdict PASS and blocker count 0, but neither it nor
the figure archive has a Git commit seal.  The literature input is only a
bounded, dated primary-source non-hit; it proves neither novelty nor
correctness.

## Reproduction

From the repository root, using the bundled workspace Python:

```bash
CODEX_PYTHON=/path/to/bundled/python3
R074W_DEPS_DIR=/path/to/version-pinned/dependencies
REPOSITORY=/path/to/navier-stokes-r074m
FIG=research/figures/r074w/fig-r074w-remote-adjacent-inward-threshold
env PYTHONPATH="$R074W_DEPS_DIR" "$CODEX_PYTHON" -B "$FIG/plot.py" --deps "$R074W_DEPS_DIR" --repository "$REPOSITORY" --render
env PYTHONPATH="$R074W_DEPS_DIR" "$CODEX_PYTHON" -B "$FIG/validate.py" --deps "$R074W_DEPS_DIR" --repository "$REPOSITORY" --seal-local --confirm-visual-qa
env PYTHONPATH="$R074W_DEPS_DIR" "$CODEX_PYTHON" -B "$FIG/validate.py" --deps "$R074W_DEPS_DIR" --repository "$REPOSITORY" --verify-only
```

`plot.py` regenerates the source-data ledger and all raw exports.  The seal
step independently recomputes the exact formulas, rerenders twice, compares
deterministic hashes, verifies vector/raster/PDF content, and writes the four
metadata files.  `SHA256SUMS` covers the other 24 files and is intentionally
excluded from its own ledger.

The locked research-blossom mark is placed at the top-right of the figure.
All panels use one navy root colour plus neutral greys and remain separable in
greyscale through line style, marker shape, weight, and hatch.

**ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS |
NOT CLAY**
