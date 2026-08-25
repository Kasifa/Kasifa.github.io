# fig-r071j-full-frame-gap

This is the formal double-column figure package for R0.71J. Its current
`manifest.json` follows schema version 1.0 and has status `formal`; it binds
the clean source snapshot
`6ab52563da0447ecd67dfdfb03b053f023c284a4`. It preserves four exact
boundaries:

1. positive shellwise sources satisfy an exact derivative--viscous--defect
   decomposition;
2. the selected parent shell of a fixed-energy, global-smooth 2D3C
   Navier--Stokes family has a closed-form positive pure-heat pulse;
3. for the parent-only broad dyadic frame, the full-frame positive-creation
   lower coefficient scales as \(K^{-2}\), whereas the available heat upper
   bound scales as \(K^{-4}\);
4. the initial Fourier ledger cancels \(B\) exactly, and every listed Lamb
   mode lies in the selected parent's flat top.

## Reproduction

Run all commands from this directory. The repository-local Python entry
point is `../../../tmp/r068b-venv/bin/python`. The numerical dependency lock
is `../../../research/requirements-r068b.txt`. The observed Python, NumPy,
Matplotlib, and Pillow versions are recorded in `environment.txt` and
`manifest.json`.

`generate_data.py` evaluates only closed-form formulas. There is no ODE or
PDE time stepper, DNS, random sample, regression, or fitted exponent.
`validate_data.py` checks the producer formulas. `independent_validate.py`
recomputes all 856 CSV rows through a separate 80-digit, Python-standard-
library `Decimal` path; it imports neither the producer nor NumPy,
Matplotlib, SymPy, or Pillow. Its archival checks call the pinned `pdfinfo`
and `pdftoppm` executables recorded in the script.

The archival outputs are `figure.pdf`, `figure.svg`, and the 600 dpi
`figure.png`. `qa-original.png`, `qa-grayscale.png`, and `qa-report.md`
record print-size, grayscale, and vector-raster QA. `manifest.json` and
`SHA256SUMS` bind the package.

Verify an unchanged package with `shasum -a 256 -c SHA256SUMS`. After
changing any asset, rerun `build_manifest.py` before checking the ledger; a
stale hash failure is expected until the manifest and ledger are rebuilt.

## Claim boundary

The full-frame statement is for the parent-only broad dyadic frame specified
in R0.71E section 10.1, the global cell \(\chi=1\), and heat height \(s=0\).
It does not cover the later low/high child refinement, matched spatial cells,
denominator or refresh faces, another Navier--Stokes-specific budget, or a
full face-paid weighted-BV estimate. The plotted \(Z\) lower coefficient is
an asymptotic large-dyadic-\(K\) result with no quantified threshold \(K_0\),
not a finite-\(K\) numerical trajectory. The package proves no continuation
criterion, regularity theorem, singularity statement, originality claim, or
Millennium-problem conclusion.
