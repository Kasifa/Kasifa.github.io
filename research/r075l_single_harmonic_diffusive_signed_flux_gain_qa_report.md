# R0.75L certificate QA report

- Verdict: **PASS**
- Mathematical blockers: 0
- Python assertions: 19/19
- Ruby assertions: 20/20
- Negative mutations rejected: 120/120 Python; 120/120 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS

## Release manifest

| path | SHA-256 |
|---|---|
| research/r075l_single_harmonic_diffusive_signed_flux_gain.md | 52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5 |
| research/r075l_single_harmonic_diffusive_signed_flux_gain_primary_audit.md | a7578e5370d182decc39f0da2f2fb581e5ef842ae7b914a120b5784bc32bd302 |
| research/r075l_report-source.md | a300de54b9fe06e94455a055bbb42bdce8ec7bb004080389a95412966a5b941a |
| scripts/r075l_single_harmonic_diffusive_signed_flux_gain_fixtures.json | 0b9ba1f018b6e52414f20dee6687f5ff55c5ea0ef247ddbd905bc8c204245ad9 |
| scripts/r075l_single_harmonic_diffusive_signed_flux_gain_expected.json | 9178489eaf9f44c5b182b6080cce7212591b1a3dd86459ecbd82c1382b38db9a |
| scripts/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.py | a521194d3ab26e23ffc13450244dcd92c52ac774bfb647348ebb2fac09c2571f |
| scripts/r075l_single_harmonic_diffusive_signed_flux_gain_certificate_independent.rb | 50888ee85e72c472881eab10145020888eda1558a7a5eb067aaaf5c61b3c307c |
| scripts/r075l_single_harmonic_diffusive_signed_flux_gain_qa.sh | fa336a8dad20a400494eeb0b28a91bbb5077396238d094f5bf1621e367b7a175 |
| research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.json | 318136308fb0b1e46046b6483269e70b0a2d57dc44be18616236a10c5271a567 |
| research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate_report.md | 00c490616bdb6641a862152a315ac76861ff345d8654137dea1d5fce552b2772 |
| research/r075l_single_harmonic_diffusive_signed_flux_gain_independent_audit.md | 31a67ab57a7c3f591f3e4dbd446dada04720ed62170e7cd0773123acc8d20604 |

The primary audit is checked against the frozen main SHA, PASS/0,
L.1--L.17, and 17/17 displays. The report-source is byte-bound only;
its literature search and access record are outside this finite certificate.

## Frozen dependency bindings

| path | SHA-256 |
|---|---|
| research/r075e_horizontal_cross_mode_flux_reduction.md | 99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049 |
| research/r075g_signed_flux_gain_threshold.md | f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41 |
| research/r075k_positive_majorant_high_frequency_trace_loss.md | 9282fb30eb7517853759fb835579220e0da763974d5543e2fb260ec8ca6daebf |

## Checks

- L_B signs and all three derivative rows of F_k cancel exactly: PASS.
- F_k^2 has only 0,+/-2k modes; the diagonal is removed before absolute values: PASS.
- 0<=eta<=1, V_xi, (1-q2)/(2k^2), and A^2|B|V_xi/(8k^2): PASS.
- Integral |cos(kx)|^3=8/3 and M_k=8A^3(1-q3)/(9k^2): PASS.
- q3<=exp(-3) is symbolic/ordered only; no floating equality is used: PASS.
- A^2 conversion, C_*, k^(-2/3), and R^(1/3)omega^(1/3): PASS.
- Strict kappa endpoint 27163/71442 and display-only decimal: PASS.
- Tags L.1--L.17, references, 17/17 displays, and control bytes: PASS.

This is limited to one real harmonic, constant shear, and a full-torus cubic
mass; |B|V_xi remains unpaid. It does not prove G.1, E.24, or the full Version-M
estimate. Multimode/collar/nonconstant-shear bounds, complete clock, fixed deletion,
suitable-weak transfer, regularity, and singularity remain open. **NOT CLAY.**
