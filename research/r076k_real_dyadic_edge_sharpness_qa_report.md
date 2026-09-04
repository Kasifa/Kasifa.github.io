# R0.76K certificate QA report

- Verdict: **PASS**
- Mathematical blockers: 0
- Independent mathematical rereads: PASS (4 lanes; blockers 0 after corrections)
- Python assertions: 118/118
- Ruby assertions: 168/168
- Negative mutations rejected: 118/118 Python; 168/168 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Exact coefficient and independent Taylor/binomial routes: PASS
- Exact integer-slice complex and cosine routes, heat prepayment, and phases: PASS
- Finite-eta K.46 decay/phase conjugation and sign controls: PASS
- K.48 backward-heat value and independent wrong-forward-sign control: PASS
- K.1--K.48, 48 displays, dangling-reference gate, hashes, and claim boundary: PASS
- q=o(L^2) proved slice range; q=o(L^(5/2)) full lower range remains open
- Complete-clock signed flux relative to full plateau remains open
- Generated-output hash-cycle guard: PASS
- AGENTS.md excluded from bindings, inventory, and release manifest: PASS
- Canonical outputs regeneration-stable: PASS
- Formal figure required: no; simulation required: no
- Exact core inventory: 12/12 files (11 manifest rows plus this QA report)

## Release manifest

| path | SHA-256 |
|---|---|
| research/r076k_real_dyadic_edge_sharpness.md | e293a3aa3e9c1dde443ed7a8c07afd2c709d3855d8b469b38033b04d71116bf2 |
| research/r076k_real_dyadic_edge_sharpness_primary_audit.md | 36a26cb421a108127b516e47a0008625d67ec43a1d009a14bef9d7684ef03671 |
| research/r076k_report-source.md | 21dbd71aae07ecbe910d4bcefbf6e1caccc3cddc41171a57ffd239c6eed34f3e |
| scripts/r076k_real_dyadic_edge_sharpness_fixtures.json | 16acf468a6722ee1e66e36a855fdd1e84e56bdc3519e6e2326d6bec0a3b82518 |
| scripts/r076k_real_dyadic_edge_sharpness_expected.json | 8f32d96856fdf5d0a86030737f5bf049b227f976661089ed6d31d4a41a1c5b50 |
| scripts/r076k_real_dyadic_edge_sharpness_certificate.py | c05ab480973a418e69cb40984b1da5c7210c5e4916e2fa1d6fb6281a9b53d1d9 |
| scripts/r076k_real_dyadic_edge_sharpness_certificate_independent.rb | 893b0b5e18e3a3fca06ef10e7879e361894dafbb845d09264373e92f116210bb |
| scripts/r076k_real_dyadic_edge_sharpness_qa.sh | 5968f4b6a08d982c4345165e7fc0bc04c33dca66ab7cf8c1dba0be30a5212a79 |
| research/r076k_real_dyadic_edge_sharpness_certificate.json | 4d5247ca82869758c01a398f9a4858bfce87e3bd7ab3ad2a37eac0e6bdea7f1d |
| research/r076k_real_dyadic_edge_sharpness_certificate_report.md | 43131539e1fd4105fe0215739003b7819379e87d44ddab4aa772a40bcc47daaa |
| research/r076k_real_dyadic_edge_sharpness_independent_audit.md | 7d87a4b543051e08cc6a348c5b7f261cd433fdf8efba4986ed01514c13c78b1a |

## Boundary

The certificates audit finite arithmetic, source, equation, claim, and
hash ledgers. They do not prove the continuum limit, a complete-clock
flux lower bound, regularity, or singularity. **NOT CLAY.**
