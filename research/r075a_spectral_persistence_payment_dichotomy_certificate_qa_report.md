# R0.75A certificate QA report

- Verdict: **PASS**
- Main SHA-256: `f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388`
- Python producer SHA-256: `d5256d8ea9db81adc5133e3cce69b9f7089f8ab8a2c5d39f30877815e6052e5a`
- Ruby verifier SHA-256: `30d28440b4cba3b0578fa7644cf5539ff6a2806f449c020d6cd1718e553ade27`
- QA driver SHA-256: `b9b07e3d1a8d1303111cf1978481530e791f3e14d81b6865674d16f73caa2538`
- Certificate JSON SHA-256: `7f504c91bcfcb8ba463c0dec977d946d8f36b26b4f732a2082863bbe5221a38e`
- Python report SHA-256: `bfb87b97e661703c4a7ddd6231b50058dfe116d0d9343d9a6e4c1554714ef238`
- Ruby report SHA-256: `966335bf8a6e759abda01c61d17ef3be4ee3c76e6dd4396b33d6488874dc4960`

## Checks

- Frozen main and all five source-table SHA-256 bindings: PASS.
- Exact fractions, `p=32/63`, nested-core inequalities, and B interval: PASS.
- Moving-cutoff sign and exact `R^-3` scale: PASS.
- Every R/L/omega exponent in (A.26)--(A.34): PASS.
- Horizontal modal equations, energy signs, and forward/backward exponents: PASS.
- Required tags, resolved references, balanced displays, and status boundaries: PASS.
- Python hash seeds 0, 1, and 42 produced byte-identical JSON and Markdown: PASS.
- Canonical regeneration was byte-stable for JSON and both reports: PASS.
- Independent Ruby exact recomputation and Python-ledger cross-check: PASS.
- Eight targeted mutations were rejected by both Python and Ruby: PASS.

Rejected mutations: wrong transport sign; `R^-2` cutoff; `R^-4` cutoff;
wrong omega weight; reciprocal p; omission of critical/shorter focusing;
promotion to full clock; and frozen-source drift.

The certificate is fail-closed at the W-remote endpoint/payment dichotomy.
Complete K, fixed deletion, arbitrary suitable weak solutions, regularity,
singularity, and Clay remain open. **NOT CLAY.**
