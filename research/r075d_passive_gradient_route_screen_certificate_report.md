# R0.75D reproducibility certificate report

- Verdict: **PASS**
- Assertions: 20/20
- Main SHA-256: 54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6
- Tags: 23 unique; displays: 23/23
- K-low exact rate: 147163/476280000
- Intermediate-band exact gap: 27163/952560000
- Frozen shear-payment rate: 27163/158760000
- Negative mutations declared: 41

## Certificate-side dependencies

The frozen main note contains no source-hash table. The certificate does not
pretend otherwise and does not require table rows to exist in the main file.
It independently binds only the two directly invoked B/C notes:

- research/r075b_bulk_clock_outer_padding_gate.md: 430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a (certificate-side binding)
- research/r075c_background_shear_packing_false_positive.md: 1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89 (certificate-side binding)

## Certified boundary

The certificate recomputes the D.4--D.7 Hölder, R, L, omega, and K powers;
the K-low threshold and exact rate; the horizontal modal energy signs; the
vertical zero-mode obstruction; the D.10--D.11 sign and Laplacian
dissipation; the transition/full-collar volumes; and the block threshold
and exact intermediate-band gap. It also recomputes the D.16--D.23
normalizations, cutoff and mixed Hölder powers, shear-payment rate, the
small-payment direction, and the interaction-condition homogeneity. It
checks all 23 tags, local and external B/C references, displays, control
characters, and required status text.

This is finite exact arithmetic and structural verification of a route
screen. The exact passive fallback is of size P^(2/3)+P and pays the
small-payment regime only. The frozen branch has P tending to infinity, so
the linear term is not absorbed. Low-frequency payment remains conditional.
The interaction condition, high-frequency local capture, intermediate band,
commutators, projection leakage, and periodic weights remain OPEN. No exact
counterexample or complete-clock result is certified. NOT CLAY.
