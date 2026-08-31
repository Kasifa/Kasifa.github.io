# R0.73R independent figure QA report

- Independent reconstruction of all 141 source-data rows: **PASS**.
- Matched packet support/moduli, sign sequence, and analytic powers: **PASS**.
- Vector PDF, SVG, 600-dpi PNG, and PDF-raster checks: **PASS**.
- PDF physical size 178 by 94 mm; embedded raster objects: **zero**.
- SVG embedded image elements: **zero**.
- Final-size and grayscale visual inspection: **CONFIRMED**.
- Labels, legends, colours, marker redundancy, and print-size readability: **PASS**.
- Claim-boundary labels: **PASS**.
- DGX or GPU use: **no**.
- Package sealing state: **FORMAL PASS**.

The validator independently reconstructs Rudin--Shapiro signs from binary
adjacent-pair parity and all seven analytic powers; it never imports plotting
code. A preseal is not formal. Formal sealing additionally binds all ten
source files byte for byte to an immutable Git source commit, after which the
generated assets and metadata require a separate artifact commit.
