# R0.73V formal figure source

This directory is the reproducible source and artifact package for
`fig-r073v-signed-third-order-interface`, a 178 mm four-panel journal figure.

Every mathematical verdict displayed in the figure is reconstructed from the
sealed R0.73V exact certificate at commits `7c445c5...` and `b34d91e...`.
Before any source row or plot value is generated, `plot.py` requires the
primary `results.json` and independently produced `independent-results.json`
to have an identical complete `commonCore`.  It also verifies their frozen
SHA-256 values, the common-core digest, and the complete-table digest.

Panel D contains deterministic renderer samples of the closed parabolic
profile.  Those samples are not observations and are not used to infer the
nonzero coefficient, order, or dilation law; those statements come from the
exact Gaussian-rational q-polynomial certificate.

Panel B prints only the active 2 by 2 block of each exact 3 by 3 tensor
coefficient.  The omitted third row and third column are identically zero in
the sealed certificate, not unreported or numerically truncated values.

The evidence is coefficientwise.  It is not a whole-field information
collision, a finite-hierarchy no-go theorem, a closure model, a numerical
Navier--Stokes simulation, or a regularity result.  `NOT CLAY`.

## Reproduce

Use Python 3.12 with the exact versions in `requirements.txt`, either in the
active environment or via `--deps`:

```text
python3 -B plot.py --deps <python-packages> --render-preseal
python3 -B validate.py --deps <python-packages> --confirm-visual-qa
python3 -B validate.py --deps <python-packages> --verify-only
python3 -B ../../../research/validate_figure_package.py .
```

The validator binds both certificate JSON files to the immutable sealed
package commit and verifies that their current bytes match the committed
blobs.  It also reconstructs `source-data.csv`, independently rasterizes the
PDF, verifies the grayscale and final-size QA images, and checks PDF/SVG/PNG
dimensions and integrity.

After the ten source files and eleven raw artifacts are committed, upgrade the
prepublication artifact seal to an immutable figure-source seal:

```text
python3 -B validate.py --deps <python-packages> \
  --figure-source-commit <full-40-hex-commit> --confirm-visual-qa
python3 -B validate.py --deps <python-packages> --verify-only
```

That final write requires all 21 bound files to be byte-identical to the
specified commit and clean in their scoped Git status. The four generated
metadata files are then committed in a separate reseal commit.

Ordinary translation and all figure work use
`LOCAL_DIRECT_NO_DGX`; `dgxUsed=false`.
