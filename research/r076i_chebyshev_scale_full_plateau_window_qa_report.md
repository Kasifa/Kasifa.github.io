# R0.76I certificate QA report

- Verdict: **PASS**
- Mathematical blockers: 0
- Independent mathematical rereads: PASS (2 lanes; blockers 0)
- Python assertions: 129/129
- Ruby assertions: 129/129
- Negative mutations rejected: 129/129 Python; 129/129 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Python/Ruby exact arithmetic, mutation inventory, bindings, and freeze state: PASS
- Generated-output hash-cycle guard: PASS
- Canonical outputs regeneration-stable: PASS
- Exact core inventory: 12/12 files (11 manifest rows plus this self-generated QA report)

## Release manifest

| path | SHA-256 |
|---|---|
| research/r076i_chebyshev_scale_full_plateau_window.md | 6277cb69dfad94cae89088c6a8c007967bdde97aceee7b19954d10ec53f6efce |
| research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md | 65adf8bc77f33c5d18184c612acc67246e48e7ad3c9059b85f269e92c9372dbe |
| research/r076i_report-source.md | 0ee0fbd75f9691e2ac898a57921f8a0574ba9af9ea652f85d0199856d7e3d423 |
| scripts/r076i_chebyshev_scale_full_plateau_window_fixtures.json | f1475b2549490c3639c15a4fc103e704d0de98a518f50249b732a8e0a135d776 |
| scripts/r076i_chebyshev_scale_full_plateau_window_expected.json | 26485db072bf886fae88f0737546d7090f77b9b23e55c356bf8affe6aeba1da5 |
| scripts/r076i_chebyshev_scale_full_plateau_window_certificate.py | a14e7fe3bc3b118232328a6d9e4d9d4cedb1e685c057483e12416725024af538 |
| scripts/r076i_chebyshev_scale_full_plateau_window_certificate_independent.rb | 5e1ead81eb0f036d41addf2dd203527c3ae49aa497d483002a3973b69d88225c |
| scripts/r076i_chebyshev_scale_full_plateau_window_qa.sh | d23b771cd0e7c5253ba592f9efd2e7c0c2396cd928641f6463559b2b20953458 |
| research/r076i_chebyshev_scale_full_plateau_window_certificate.json | 6ae521f88a1e6116f466641bde60939e458b043b43ca025a10a83001613c590b |
| research/r076i_chebyshev_scale_full_plateau_window_certificate_report.md | b5d1f7b0e36f724522bc5b18442bad97ffe778e7be6ca579c0ca0bd89d9d061c |
| research/r076i_chebyshev_scale_full_plateau_window_independent_audit.md | f8c735e654031b8d5ae7029879086bf95086e7745317b7faa0e6750151093b4d |

## Checks

- I.1--I.38, 42 displays, reference closure, UTF-8, CR, and trailing whitespace: PASS.
- Exact e_a=639/640, Delta_a=2/213, two-sided 2q branch count, and Zhang exponent ledger: PASS.
- Erdelyi derivative powers, reverse-time E_N^+ terminal trace, and four-row energy signs: PASS.
- Physical a^(2/3)R^(-1/3) conversion, R cancellation, and normalized -2/11907 rate: PASS.
- CONDITIONAL-LITERATURE, unrefereed-v1, restricted-sharpness, OPEN, and NOT CLAY boundaries: PASS.
- Formal scientific figure: not applicable; no simulation claim is made.

Finite certificates audit the exact ledger; they do not prove the imported literature or the continuum theorem.
