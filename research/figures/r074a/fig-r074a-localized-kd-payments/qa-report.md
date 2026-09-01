# R0.74A figure QA report

Status: **PASS**

- Source binding: PASS (commit, six file hashes, certificate PASS 21/21).
- Formula reconstruction: PASS (all 266 rows; tolerance 5e-13).
- Panel A: PASS (cc/ec theta^(1/4); ce/ee theta; unknown C not plotted).
- Panel B: PASS (N=2^j; factors N^0, N^-2, N^(2/3); unknown c not plotted).
- Panel C: PASS (delta^0 and delta^(-2/3); separate finite fields; no uniform global Linf_t L2_x).
- SVG/PDF: PASS (178 mm x 74 mm; vector; no embedded raster images).
- Raster: PASS (600 dpi archival PNG; independent 300 dpi PDF QA render).
- Raster parity: PASS (mean absolute RGB difference 1.986737; p99 56.000).
- Grayscale/final/PDF visual review: PASS (operator-confirmed; no collision, clipping, or illegible series distinction).
- Two-render determinism: PASS (18/18 deterministic-core hashes identical).
- Inventory closure: PASS after metadata generation (25 contract files; no symlinks).

Panels B and C are function-level packets, not unforced NSE trajectories. The images contain no simulation or DNS. Finite data are not used as proof of any quantified statement. **NOT CLAY.**
