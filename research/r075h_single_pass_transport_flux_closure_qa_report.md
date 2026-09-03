# R0.75H certificate QA report

- Verdict: **PASS**
- Python assertions: 19/19
- Ruby assertions: 22/22
- Negative mutations rejected: 66/66 Python; 66/66 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS

## Release manifest

| path | SHA-256 |
|---|---|
| research/r075h_single_pass_transport_flux_closure.md | 849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9 |
| research/r075h_single_pass_transport_flux_closure_primary_audit.md | 3c85368e051102997e66ae36fa43290b6200e688db886380215fb40ec0bb757e |
| research/r075h_report-source.md | 5b0b05b2ce903986ef8439a766766e8bdb97e2fe4d9eb6035f73102583b1b779 |
| scripts/r075h_single_pass_transport_flux_closure_fixtures.json | 7e4b5691d6929c97f72146c293a55e3b6fcf5875bc51f78bd1a58e9f84a0b217 |
| scripts/r075h_single_pass_transport_flux_closure_expected.json | 099d017cb7ff61d5a9dff54449c9a91a12e8657343bb11579ad135e9cd350573 |
| scripts/r075h_single_pass_transport_flux_closure_certificate.py | 68fc20b109f6017940f8f137bc79a387076c2990b52fdfe44ad5b2c4a4beead5 |
| scripts/r075h_single_pass_transport_flux_closure_certificate_independent.rb | 0b5b591b84aba87bb7cb37d119abadc108217a3d77af1eeeb08a10d3178195af |
| scripts/r075h_single_pass_transport_flux_closure_qa.sh | bfaa1c8e3107c33a340c066178ea2e70edd74c4afcd16784996847703b6a941a |
| research/r075h_single_pass_transport_flux_closure_certificate.json | 1fda0c2e812a50a4f183b78ba503ce766553cd1dcbb1206384e07e3b1f0b0b38 |
| research/r075h_single_pass_transport_flux_closure_certificate_report.md | c77dd0ea2896ad3914bf6d74c647d5b1ebae91cfaa522df16bf2196aa13ca5a0 |
| research/r075h_single_pass_transport_flux_closure_independent_audit.md | 9c1b09a5c996c371a4ed9bcb302fc211b9ea2e97014e4c5f3f985c23207e411b |

The primary audit was checked for the frozen main hash, PASS with zero
mathematical and release blockers, and H.1--H.29 coverage.
The report-source file is byte-bound only; literature content and
recorded HTTP access checks are outside this finite certificate.

## Frozen dependency bindings

| path | SHA-256 |
|---|---|
| research/r075b_bulk_clock_outer_padding_gate.md | 430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a |
| research/r075e_horizontal_cross_mode_flux_reduction.md | 99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049 |
| research/r075f_modal_phase_integration_identity.md | f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440 |
| research/r075g_signed_flux_gain_threshold.md | f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41 |

All hashes match the H main note source table and both implementations.

## Checks

- Smooth pure transport with nondecreasing eta: direct positive flux and endpoint identity PASS (1/64).
- One nondegenerate all-rational fixture coherently recomputes H.11--H.23, including H.20--H.22: PASS.
- Mirrored negative-flux control rejects replacing the signed positive part by absolute value: PASS.
- Characteristic and lifted-set translation direction, no seam, and terminal L2 persistence: PASS.
- Holder delta^(-2/3) and volume^(1/3) powers via a nonzero equality case: PASS.
- Full H.23 R/L/omega/p normalization and rate -4279/238140000: PASS.
- Matching p_b lower bound gives H.26 in the displayed direction: PASS.
- H.28 terminal/dissipation/cutoff signs and diffusive circularity: PASS.
- Tags H.1--H.29, references, 29/29 displays, and control bytes: PASS.
- Main/audit/source/dependencies/fixtures/expected byte bindings: PASS.

Only the signed pure-transport terminal-tube benchmark is certified.
The benchmark P_R^(M,tr) is not an NSE solution functional. The result
does not cover absolute flux, multiple windings, or the diffusive
characteristic. E.24, complete clock, fixed deletion, suitable-weak
transfer, regularity, and singularity remain OPEN. **NOT CLAY.**
