# R0.75F certificate QA report

- Verdict: **PASS**
- Python assertions: 16/16
- Ruby assertions: 20/20
- Negative mutations rejected: 43/43 Python; 43/43 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS

## Release manifest

| path | SHA-256 |
|---|---|
| research/r075f_modal_phase_integration_identity.md | f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440 |
| research/r075f_modal_phase_integration_identity_primary_audit.md | 4320ac5544b51888eb8088db98e500a9877ecfe9a984f156783cac096a27c99a |
| research/r075f_report-source.md | 3838603ea143b2efe1e96995fac34d7e8565211dc91dd244ab01cf6d526f3481 |
| scripts/r075f_modal_phase_integration_identity_fixtures.json | 0ce9b3bf060f4b38fe497be7bcdad3d1bdbd51ea27ff9aab146c8b10f5a0aced |
| scripts/r075f_modal_phase_integration_identity_expected.json | 3946cb2cc992f4d1e55b88a7be9b7ecd8529e76a437093af6583f8fdacf2ddc9 |
| scripts/r075f_modal_phase_integration_identity_certificate.py | c86d85bb468b9bd953247520e2de53cd18eb7362ef63dc60ae7895b01defb768 |
| scripts/r075f_modal_phase_integration_identity_certificate_independent.rb | 7499e5fa9544a805eb0675566224a77f4d99a196f3e1582a87bb4af724d269c2 |
| scripts/r075f_modal_phase_integration_identity_qa.sh | b05e7eca1fae71955b27bc4fc6d3ddf1554f488dffe91cf081affe39c8e5932c |
| research/r075f_modal_phase_integration_identity_certificate.json | 107c59254b8f2e0ffa5e7a04ab8bdc97158191e99fca0f02ed08e0973c46fcf5 |
| research/r075f_modal_phase_integration_identity_certificate_report.md | a756e4cf3e4d44012dde1588ca2150fb58c1669e6218e602aa2fba916b2c2834 |
| research/r075f_modal_phase_integration_identity_independent_audit.md | eb7fac3ac148a41c43040c758028eb6552aa952639b54e0e1e47842604631fe8 |

The primary audit was checked for the frozen main hash, PASS with zero
mathematical and release blockers, and F.1--F.23 coverage.
The report-source file is byte-bound only; literature content and
recorded HTTP access checks are outside this finite certificate.

## Frozen dependency bindings

| path | SHA-256 |
|---|---|
| research/r075b_bulk_clock_outer_padding_gate.md | 430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a |
| research/r075e_horizontal_cross_mode_flux_reduction.md | 99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049 |

Both hashes match the F main note source table and both implementations.

## Checks

- F.1--F.18 modal equations, product rule, ell=m-n, nm, and pi/2pi normalization: PASS.
- Genuine two-mode closed solution, endpoint rows, F.14/F.15 IBP, and F.12/F.17/F.18: PASS.
- Direct transport and all closed-solution rows agree in Q[p], p=pi^-2: PASS.
- F.19--F.23 ordered Fejer counts, N=3/5/7 moments, ratios, and divergence: PASS.
- Tags F.1--F.23, references, and 23/23 displays: PASS.
- Main/audit/source/dependencies/fixtures/expected byte bindings: PASS.

The finite checks certify the exact route-pruning identities only.
The Fejer family is not the frozen geometric collar and is not an E.24
counterexample. E.24, complete-clock extraction, fixed deletion,
suitable-weak transfer, regularity, and singularity remain OPEN.
**NOT CLAY.**
