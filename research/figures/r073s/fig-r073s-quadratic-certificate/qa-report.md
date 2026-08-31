# R0.73S independent figure QA report

- Independent reconstruction of all 179 plotted source-data rows: **PASS**.
- Structural and formula checks: **236/236 PASS**.
- Panel B exact values lie below their AQ certificates: **PASS**.
- Vector PDF/SVG, 600-dpi PNG, and PDF-raster checks: **PASS**.
- PDF physical size 178 by 96 mm; embedded raster objects: **zero**.
- Final-size, grayscale, and PDF-raster visual inspection: **CONFIRMED**.
- Labels, legends, colour/marker redundancy, and claim boundaries: **PASS**.
- R0.73S source certificate final seal: **VERIFIED**.
- DGX or GPU use: **no**.
- Package sealing state: **FORMAL PASS**.

The validator independently rebuilds every plotted value without importing
plotting code. It checks the sealed 311/323 seed and the exact factorization
rows through depth eight. Panel C values beyond depth eight are independently
re-evaluated closed-form values, not additional finite-enumeration claims.
The final seal binds all source files to the immutable Git source
commit `72e4c12760dc3b837dec328ee96a29736fe93c99`.
