# R0.75U certificate QA report

- Verdict: **PASS**
- Mathematical blockers: 0
- Python assertions: 16/16
- Ruby assertions: 17/17
- Negative mutations rejected: 61/61 Python; 61/61 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS

## Release manifest

| path | SHA-256 |
|---|---|
| research/r075u_two_harmonic_difference_frequency_payment.md | f9fb331cf880b20f3b407fe66453bce71517ac1ef2af4fa0863c00325c1022a4 |
| research/r075u_two_harmonic_difference_frequency_payment_primary_audit.md | 3687decf19ff49016e101a174d066b355689dcca7a4dc36a941b84994b118d6a |
| research/r075u_report-source.md | d0e9356a162b683a33c5b4c49692a62962d2a9c63cccba9eb9d84040aaf4a01f |
| scripts/r075u_two_harmonic_difference_frequency_payment_fixtures.json | c654b79a1b3b69078df01000c43fee54fdff39ea64c7bc47e206b114dc20b0c6 |
| scripts/r075u_two_harmonic_difference_frequency_payment_expected.json | 381e80ca54eee51fb3aab823837f0bfdc28e84353e02c8f41fceed261d6aec12 |
| scripts/r075u_two_harmonic_difference_frequency_payment_certificate.py | 040474723e1380ac6983c1fe165b910aa94751f7b8884cb7d015848d990a77a3 |
| scripts/r075u_two_harmonic_difference_frequency_payment_certificate_independent.rb | 77f2b4a6bbf389c54694dfdbf8759264ed10c89cfa2e9d085378f084810f263b |
| scripts/r075u_two_harmonic_difference_frequency_payment_qa.sh | 26ab61750ecb1bfb5961479543fe32bc2338ae0bccfcf7c977cc26f71165c318 |
| research/r075u_two_harmonic_difference_frequency_payment_certificate.json | 87e6eb73c58a695a88ddc81948ddfea8257cb3844a1e4412068c28985ee28f5a |
| research/r075u_two_harmonic_difference_frequency_payment_certificate_report.md | 3d0774651733e2f803cf3b679a0c8ba36a50029a27e88366c5d8bee2344d8b0d |
| research/r075u_two_harmonic_difference_frequency_payment_independent_audit.md | 659dacda5aa67c502b3b6db315d06e9aed8cf4aa8fcd06aa45967b8de57950f8 |

## Checks

- U.1--U.28, 28/28 tags and displays, four dependencies, references, UTF-8, and control bytes: PASS.
- Radial quotient and phase-distance cubic moment: PASS.
- Slow low-heat, slow high-heat, and fast BV branches: PASS.
- AC cancellation, d and R scaling, mass substitution, normalization, and rate -2/11907: PASS.
- Fast-phase fixed-grid quadrature is explicitly excluded as proof evidence: PASS.

The source report is byte-bound; its primary-source screen is bounded and establishes no novelty.
U pays only the difference-frequency component of one exact dyadic pair.
The self/sum block, complete two-mode payment, low carriers, arbitrary-field E.24,
Version-M extraction, suitable-weak transfer, regularity, and singularity remain OPEN. **NOT CLAY.**
