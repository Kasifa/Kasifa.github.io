# R0.76A certificate QA report

- Verdict: **PASS**
- Mathematical blockers: 0
- Python assertions: 15/15
- Ruby assertions: 15/15
- Negative mutations rejected: 86/86 Python; 86/86 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS

## Release manifest

| path | SHA-256 |
|---|---|
| research/r076a_complete_clock_localized_current_sign_obstruction.md | d23532f84702be1630daa0b8d56d02242571dd8a1f8024c59a7f71bec30f26eb |
| research/r076a_complete_clock_localized_current_sign_obstruction_primary_audit.md | 0f7f56d32025f4cd86218f54dfcf5155675f316d2afecdd0007b13ad70240a8d |
| research/r076a_report-source.md | 0bbf94774c7d76e623c025a731e0238eca39080c4720a039f080afb038ecad8b |
| scripts/r076a_complete_clock_localized_current_sign_obstruction_fixtures.json | f3644b2a7a641bc92c6c1936f1c05cbed88a6a3e94e25d650c7258ce07b30a31 |
| scripts/r076a_complete_clock_localized_current_sign_obstruction_expected.json | 32d0f99d07d842bf6c9161698249c186c4d23d2f1f33e7f8bd7fc18804887697 |
| scripts/r076a_complete_clock_localized_current_sign_obstruction_certificate.py | 7dfff7dfb26ccfb9399c0a9cc32a914d5e1d94f3a81ed172f4ec245343d43ab5 |
| scripts/r076a_complete_clock_localized_current_sign_obstruction_certificate_independent.rb | 5633861e614cba477f59e8ca4d6f52bc9c29e561178ae07117af53d83cc13366 |
| scripts/r076a_complete_clock_localized_current_sign_obstruction_qa.sh | d34a0275f6b321c84db14fd47219701ef5a3caa53572b941f37343c88d680539 |
| research/r076a_complete_clock_localized_current_sign_obstruction_certificate.json | cd09488885f0e31d95f94c7f46bf0c80b1ad476a438a3fa081d3ec83d4c2949c |
| research/r076a_complete_clock_localized_current_sign_obstruction_certificate_report.md | 665e69226763e2df99615714829387309a3f66a1ec1e35b19f4af35d005c0d12 |
| research/r076a_complete_clock_localized_current_sign_obstruction_independent_audit.md | cd5608262b4f9c35f30afec9af2a108621f4f89cf8f4a69d973e1e07b6ee670d |

## Checks

- A.1--A.34, 34/34 tags and displays, three frozen dependencies, references, UTF-8, controls, and TeX escapes: PASS.
- Exact primitive support/mass, integer-frequency cluster, clock scaling, damping, phase, and point ledgers: PASS.
- Uniform localized-current and correction-density signs are audited independently: PASS.
- Finite fixtures are explicitly excluded as proof of the continuum identities: PASS.
- Formal scientific figure: not applicable to this analytic gate; no simulation claim is made.

The bounded source report is contextual and makes no novelty or priority claim.
R0.76A rejects only localized sign-dropping.  General cluster payment,
Version-M transfer, regularity, and singularity remain OPEN. **NOT CLAY.**
