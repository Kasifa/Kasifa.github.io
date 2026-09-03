# R0.75D independent Ruby verification

- Verdict: **PASS**
- Assertions: 23/23
- Main SHA-256: 54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6
- K-low exact rate: 147163/476280000
- Intermediate-band exact gap: 27163/952560000
- Frozen shear-payment rate: 27163/158760000
- Tags: 23; displays: 23/23

- Failed checks: none

Ruby independently recomputed the D.4--D.7 exponent ledger, modal and gradient signs, collar volumes, block threshold, and exact fractions. It also recomputed the D.16--D.23 mass normalizations, cutoff and mixed Holder powers, shear-payment rate, small-payment direction, and interaction homogeneity. It then cross-checked the Python schema, exact values, both exponent ledgers, and certificate-side dependency boundary.

R0.75D has no embedded frozen-source table. The B/C hashes are bound by this certificate suite only.

The exact fallback is P^(2/3)+P and pays only the small-payment regime. The frozen branch has P tending to infinity, so its linear term is not absorbed. Low-frequency payment remains conditional. The interaction condition, intermediate-frequency capture, commutators, projection leakage, periodic weights, and an exact counterexample remain open. No complete-clock result is certified. **NOT CLAY.**
