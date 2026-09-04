# R0.76D certificate QA report

- Verdict: **PASS**
- Mathematical blockers: 0
- Python assertions: 123/123
- Ruby assertions: 123/123
- Negative mutations rejected: 123/123 Python; 123/123 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS
- Python/Ruby exact sections identical: PASS (6/6)
- Exact core inventory: 12/12 files

## Release manifest

| path | SHA-256 |
|---|---|
| research/r076d_quantitative_growing_mode_entropy_window.md | cd94e3384f01963cb7b8a14fdb8376c6197c361473447f15500db0acac5e958e |
| research/r076d_quantitative_growing_mode_entropy_window_primary_audit.md | 9b99247ceb34cadc12c7f4f0858be642316ca80d1ff83d05dfd745a9906356d8 |
| research/r076d_report-source.md | f2358780d382dcace69b7ebef855bf3c8e63d15b581dc86b62b7e3c751fbd310 |
| scripts/r076d_quantitative_growing_mode_entropy_window_fixtures.json | ffe5c2b9a1a6b0c20b710dc45fcac9543069ea6af38dce34804665012984b374 |
| scripts/r076d_quantitative_growing_mode_entropy_window_expected.json | eb5dd9ebaa6a74cbc7f999fdbd55ee54a50588342c3dfba9412ac53c935ba2dd |
| scripts/r076d_quantitative_growing_mode_entropy_window_certificate.py | ed96f55b1326f1e7c1330670c132c523c7861f53edcb046b662159d83e60ce54 |
| scripts/r076d_quantitative_growing_mode_entropy_window_certificate_independent.rb | 9f12fa2aadc35dfb228e8f0ab60eec420c5c6bdfa306f1b66ca4828cdde4d391 |
| scripts/r076d_quantitative_growing_mode_entropy_window_qa.sh | b69b5380ffd60ad713c3971311cf6197bc5254a44abbb8e65f3d19990ec5e592 |
| research/r076d_quantitative_growing_mode_entropy_window_certificate.json | e57d160e8b3b37ed714e884750f50abbaaaac25a1e3ec3ba395a0193e0b6757d |
| research/r076d_quantitative_growing_mode_entropy_window_certificate_report.md | 460917d50cd9aeeb4af5898322915d67fa8ec3e1971f2e5945becf858ccd9c94 |
| research/r076d_quantitative_growing_mode_entropy_window_independent_audit.md | 0d6e3b7f363fdb9e031a228038ae7af4152d51d101e6050f39c4de7dc21fa69a |

## Checks

- D.1--D.41, 41/41 display blocks, three frozen dependencies, references, UTF-8, controls, CR, and TeX escapes: PASS.
- Exact q=3, N=6 fixture: m=10, 11!/4=9,979,200, lambda=4, T=16, and gradient coefficient 257/64: PASS.
- Erdelyi half-scale coefficients alpha+14e and returned derivative 2alpha+28e are recomputed independently: PASS.
- Weighted onset exponent lambda^(-1/3), terminal exponent lambda^0, physical exponents, and frozen rate -2/11907: PASS.
- The (5/4)^m endpoint comparison inserted after adversarial audit is present and certified: PASS.
- R0.75R compatibility, exact-shear scope, growing constant, Version-M condition, and NOT CLAY boundary: PASS.
- Finite fixtures are explicitly excluded as proof of the imported continuum inequalities or analytic flux theorem: PASS.
- Formal scientific figure: not applicable to this analytic theorem; no simulation claim is made.

R0.76D quantifies the fixed-mode constant by exp(C q log(q+1)) and proves only the stated exact-shear growing-mode window.
Arbitrary packets, Version-M extraction, regularity, and singularity remain OPEN. **NOT CLAY.**
