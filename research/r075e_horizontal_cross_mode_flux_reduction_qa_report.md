# R0.75E certificate QA report

- Verdict: **PASS**
- Python assertions: 13/13
- Ruby assertions: 16/16
- Negative mutations rejected: 39/39 Python; 39/39 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS

## Release manifest

| path | SHA-256 |
|---|---|
| research/r075e_horizontal_cross_mode_flux_reduction.md | 99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049 |
| research/r075e_horizontal_cross_mode_flux_primary_audit.md | da2778c1f0d5538981c517fccf75c96a635abbe7fae8833359c727dd2b301860 |
| research/r075e_report-source.md | 96577484d25745b419c30723c0af2d2873fbfff1f3340b79e1d7c9af71327199 |
| scripts/r075e_horizontal_cross_mode_flux_reduction_certificate.py | 1d3eed137dc954bfcdfb6fe54ed6e1d3037f2bb18e297b3fb3264bbd8a2ad7ba |
| scripts/r075e_horizontal_cross_mode_flux_reduction_certificate_independent.rb | f6a85045c1737f7291441df9c9151d8f786510811f2333ec47843a8f16c2cb99 |
| scripts/r075e_horizontal_cross_mode_flux_reduction_qa.sh | 79065b938b264bc3422bed505f2f5a93f405fbb57bde2f598a7237bdba6d9ef1 |
| research/r075e_horizontal_cross_mode_flux_reduction_certificate.json | 682bdfadd6935e35c9ea85bfcfe9aa74ccbca8341f84791fe0885ee0f0e62946 |
| research/r075e_horizontal_cross_mode_flux_reduction_certificate_report.md | 6ffd2fb6601eae3e212ab1b989101eb6ca5e317cf4df9812a9926f6114ac79cf |
| research/r075e_horizontal_cross_mode_flux_reduction_independent_audit.md | a9d0b7410a6492ef699f1fbfc77906eb4bcadc1c9193887e8f3b8e5c5778d54c |

The primary audit was checked for the frozen main hash, PASS with zero
mathematical and release blockers, and E.1--E.24 coverage.
The report-source file is byte-bound here only; its literature content
and recorded HTTP checks are outside the finite arithmetic suite.

## Frozen dependency bindings

| path | SHA-256 |
|---|---|
| research/r075b_bulk_clock_outer_padding_gate.md | 430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a |
| research/r075c_background_shear_packing_false_positive.md | 1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89 |
| research/r075d_passive_gradient_route_screen.md | 54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6 |

All three observed hashes match both the certificate constants and the
frozen-source table embedded in the E main note.

## Checks

- Tags E.1--E.24, references, and 24/24 displays: PASS.
- Direct Laurent and independent ordered-mode T/pi normalization: PASS (-1/2).
- Diagonal cancellation, zero mode, and complex-singleton zero flux: PASS.
- Complex singleton is not physical; a real +/-1 pair has nonzero flux: PASS.
- E.15 L/R/omega/pF powers and E.16 exponential sign: PASS.
- E.21 pi*omega/R normalization and E.23 mixed powers: PASS.
- Endpoint, transport sign, support invariance, and x1-average boundary: PASS.
- E.24 arbitrary-real estimate and all larger conclusions remain OPEN: PASS.

The finite witness verifies E.10 algebra and normalization only; it is
not a full E.1 spacetime trajectory or the geometric collar cutoff.
The all-payment estimate is restricted to the real horizontal zero mode
for L>=L0. A complex singleton is diagnostic only, while a real +/-n
pair is not forced to cancel. E.24, complete clock, fixed deletion,
suitable-weak transfer, and regularity remain OPEN. **NOT CLAY.**
