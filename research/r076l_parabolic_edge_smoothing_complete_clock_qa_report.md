# R0.76L research certificate QA

Verdict: **PASS**

- Python finite certificate: 64/64.
- Independent Ruby finite certificate: 279/279.
- Python, Ruby, and frozen expected exact ledgers: identical.
- Python hash seeds 0, 1, 42: byte-identical certificates.
- Repeated Ruby certificate and report: byte-identical.
- Python observed-ledger corruption controls: 25/25 caught by ordinary assertions.
- Ruby parsed-input corruption controls: 26/26 caught by ordinary assertions.
- Unknown control names: rejected by both implementations.
- Arithmetic input sensitivity: 11/11 changes observed.
- Exact R-log-rate cancellation and coupled exponent perturbation: PASS.
- Isolated single-byte binding corruptions: 21/21 rejected.
- Archived data/SVG regeneration: byte-identical; progress and resource logs unchanged.
- Source tree and frozen bytes: bound to b234b63c24c7b19efc703367e23b092385066a1c.
- Figure manifest is additionally validated when present; its final validation belongs to the research freeze inventory.

The negative controls exercise finite arithmetic, validation, provenance,
and claim-boundary checks. They do not prove the continuum asymptotics or
the exact-shear transfer theorem. The analytic primary audit is a separate
source artifact. **NOT CLAY.**
