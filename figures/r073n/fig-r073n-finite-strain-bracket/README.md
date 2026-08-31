# R0.73N finite-strain bracket figure

Formal three-panel source package for the theorem-relevant R0.73N finite
diagnostic.  The package binds the validated R0.73N certificate under
`research/certificates/r073n`, exports vector PDF/SVG and 600-dpi PNG, and
stores the exact source rows used by every panel.

The picture is deliberately diagnostic.  Panel C evaluates exponent factors
at different marked backgrounds \(\overline U_\Lambda(0)\); it does not plot
one fixed-background trajectory or a measured sharp Lipschitz modulus.

Run `command.txt` from the repository root.  The validator fails closed on
input hashes, source rows, dimensions, vector/raster format, claim boundary,
or incomplete visual QA.  Before an immutable R0.73N theorem-source commit is
assigned, its status is `hash-bound-uncommitted`; successful commit/blob
verification upgrades that status to `sealed`.

After the certificate and all ten figure source files have an immutable
commit, pass that exact 40-hex hash to `validate.py --source-commit`.  Final
sealing checks every committed source blob against the current source bytes,
requires the certificate to be sealed to the same commit, and keeps the
certificate `source-data.csv` path and SHA-256 binding explicit.  The
validator never substitutes the current `HEAD` for the requested commit.
