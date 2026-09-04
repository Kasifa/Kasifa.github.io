# R0.76G certificate QA report

- Verdict: **PASS**
- Mathematical blockers: 0
- Independent mathematical audit: PASS (blockers 0)
- Python assertions: 120/120
- Ruby assertions: 120/120
- Negative mutations rejected: 120/120 Python; 120/120 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Python/Ruby exact section and mutation inventory: PASS
- Canonical outputs regeneration-stable: PASS
- Exact core inventory: 12/12 files (11 hash-bound manifest rows plus this self-generated QA report)

## Release manifest

| path | SHA-256 |
|---|---|
| research/r076g_complete_clock_central_fibre_flux_lower_bound.md | 20f32790b53f2b0f5cb39b7071bd2cda96ddb4e15f75211e1682f4ba37dd0bb2 |
| research/r076g_complete_clock_central_fibre_flux_lower_bound_primary_audit.md | af47153c4e1f4c5749f68c3f89d7533c5d95f3c0c6f15b0c775a9e35317c807e |
| research/r076g_report-source.md | 3aea1d04dce4987c3883c1b93bec04e714ee17b540fb6a99546d084efa326f74 |
| scripts/r076g_complete_clock_central_fibre_flux_lower_bound_fixtures.json | 32e1dcf71a77ba0d28e3924fcb7e7aeb4d2840aa08ba2b2e352bb4d20d0464af |
| scripts/r076g_complete_clock_central_fibre_flux_lower_bound_expected.json | 0a2d3d086381029941310ae502b4cf9462e025d0c75e62dd87c07334728a6ba8 |
| scripts/r076g_complete_clock_central_fibre_flux_lower_bound_certificate.py | 0afbee1f11de12cefc85aee64cbdb8c92925ad2db33cdae8d0582b79dbc01f85 |
| scripts/r076g_complete_clock_central_fibre_flux_lower_bound_certificate_independent.rb | ea5036ffed18ce5d1ff33addeff6086ab3603bcedf2373ca6dec7ca3e4963fa2 |
| scripts/r076g_complete_clock_central_fibre_flux_lower_bound_qa.sh | 4fdbce0ab1b3b81dd87a07d4852c9b00ba3b3e6790e714f26124aabf2784ff1e |
| research/r076g_complete_clock_central_fibre_flux_lower_bound_certificate.json | dcca5611f40b5de9cfcc76fccc3ed35a0219a8baedbb488574223809686c652d |
| research/r076g_complete_clock_central_fibre_flux_lower_bound_certificate_report.md | f77d2e636e65ff07f662adc72fa16f13ab4edb57addf8422536fa67a0b36660c |
| research/r076g_complete_clock_central_fibre_flux_lower_bound_independent_audit.md | c034a9d3f01e784733fd35052ec4b9574c9ee4596ad44e466d07a78773953a68 |

## Checks

- G.1--G.40, displays, references, UTF-8, CR, trailing whitespace, and prose screen: PASS.
- Exact m=3 packet has seven positive modes 6--12 and dyadic equality 12=2x6: PASS.
- Clock reset 61--65 to 0--4 and terminal zeta=1 on (3,4): PASS.
- Central 233/200<7/6, cap ratio 9/7, mode density 2/3969, and exact positive rational rate lower bound 2/35721: PASS.
- Complete-signed-flux, central-proxy-only, full-plateau-open, source, and NOT CLAY boundaries: PASS.
- Formal scientific figure: not applicable; no simulation claim is made.

Finite certificates audit the exact ledger; they are not the continuum proof.
