# R0.75G certificate QA report

- Verdict: **PASS**
- Python assertions: 16/16
- Ruby assertions: 18/18
- Negative mutations rejected: 57/57 Python; 57/57 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS

## Release manifest

| path | SHA-256 |
|---|---|
| research/r075g_signed_flux_gain_threshold.md | f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41 |
| research/r075g_signed_flux_gain_threshold_primary_audit.md | 4717b365e5a4dc1bff169db51708a8a74fe51e6dd414a9a68a448813d95541aa |
| research/r075g_report-source.md | 2722d2801945a2ee074b0a9c4a973f592849ae012ddd4c264b7fea5ad76e9896 |
| scripts/r075g_signed_flux_gain_threshold_fixtures.json | 6bcf72a52763b04f98c21109fabbd570aa552cfe472280cff7ff4a0738eb0c9a |
| scripts/r075g_signed_flux_gain_threshold_expected.json | 03b3475a3f8e82cb986e63ef52af6fdb899ac200b70024661c379542356b6ab0 |
| scripts/r075g_signed_flux_gain_threshold_certificate.py | c08eb7f02b49864d5f46ba4fc7f14b5f815f03fa712a0ccb373e933be6f46cee |
| scripts/r075g_signed_flux_gain_threshold_certificate_independent.rb | c2d11ff71dd683a15cbb97892c028b3e861e47bde5e18cedd602d9967430da3c |
| scripts/r075g_signed_flux_gain_threshold_qa.sh | 65add9d4c0b8b6569315b1cdb7e664a91c28bc60d1204cec028d8adbbb2e9190 |
| research/r075g_signed_flux_gain_threshold_certificate.json | 72cf4415368aa527699b4e1d23a11ff91dc41247a0474b0bc33845f90214be32 |
| research/r075g_signed_flux_gain_threshold_certificate_report.md | 8a7d42b877481593278ffd60ac98c0ce3dd11f4f242c96db96f561f41dac8744 |
| research/r075g_signed_flux_gain_threshold_independent_audit.md | 5e33e561d9d84d2acda364fffe988a7eeee769c1a24b27d6fce01f4159c005d2 |

The primary audit was checked for the frozen main hash, PASS with zero
mathematical and release blockers, and G.1--G.24 coverage.
The report-source file is byte-bound only; literature content and
recorded HTTP access checks are outside this finite certificate.

## Frozen dependency bindings

| path | SHA-256 |
|---|---|
| research/r075c_background_shear_packing_false_positive.md | 1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89 |
| research/r075d_passive_gradient_route_screen.md | 54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6 |
| research/r075e_horizontal_cross_mode_flux_reduction.md | 99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049 |
| research/r075f_modal_phase_integration_identity.md | f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440 |

All hashes match the G main note source table and both implementations.

## Checks

- G.9 product and G.10 L/R/omega cube-root exponents: PASS.
- alpha*=27163/107163, strict equality boundary, and alpha=1/3,1/4 margins: PASS.
- beta*=27163/35721 and beta=3alpha conversion: PASS.
- Exact positive-amplitude quadratic/cubic homogeneity family: PASS.
- Smooth pure-transport positive flux and endpoint difference, both 1/32: PASS.
- Single unwrapped rational crossing with O(R^3) occupation and O(R) fraction: PASS.
- Tags G.1--G.24, references, and 24/24 displays: PASS.
- Main/audit/source/dependencies/fixtures/expected byte bindings: PASS.

The threshold is sufficient only for the hypothesized G.1 route.
The equality case retains the growing L^(2/3) factor; the 1/4 result is
not a counterexample. The transport and one-passage examples do not
prove the arbitrary diffusive interaction estimate. G.1, G.18, G.24,
E.24, complete clock, fixed deletion, suitable-weak transfer,
regularity, and singularity remain OPEN. **NOT CLAY.**
