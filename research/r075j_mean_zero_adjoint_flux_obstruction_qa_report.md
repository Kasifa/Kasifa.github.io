# R0.75J certificate QA report

- Verdict: **PASS**
- Python assertions: 19/19
- Ruby assertions: 24/24
- Negative mutations rejected: 84/84 Python; 84/84 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS

## Release manifest

| path | SHA-256 |
|---|---|
| research/r075j_mean_zero_adjoint_flux_obstruction.md | 960e3cbc18ac8207253a8802da215b3eac07a714ddbcc7209985f27a00c9ff4d |
| research/r075j_mean_zero_adjoint_flux_obstruction_primary_audit.md | f2de2d439d428ccd2885f7d3fc333496cb9753896c772a54df04622e4c52c76e |
| research/r075j_report-source.md | 1d195b0bc6760a4458fd3b4f7d11c5c892ca259c88aa5de3b014b4986ad166ca |
| scripts/r075j_mean_zero_adjoint_flux_obstruction_fixtures.json | 754d585bab0b194adaa3f945dc8b14950e3c078564f38dc63919cf733fcfea2c |
| scripts/r075j_mean_zero_adjoint_flux_obstruction_expected.json | 6c32cd1ff38895c5e3b0a580ad9a5e789fc3d9d8e672ba6644dceeb29befe5b8 |
| scripts/r075j_mean_zero_adjoint_flux_obstruction_certificate.py | 390964c4116ece9002114d399b2c715fc7835cf7407f3788c426bc6c1d6b7d1f |
| scripts/r075j_mean_zero_adjoint_flux_obstruction_certificate_independent.rb | d84e7997c08f4ca11f88072217f7b0117bf1bd78db07fdc558a4e47e595f8147 |
| scripts/r075j_mean_zero_adjoint_flux_obstruction_qa.sh | 66b6bbe3ba5efc3ffc4d89fc733f36bd32f198574ab2131da332ac7fb4209a3b |
| research/r075j_mean_zero_adjoint_flux_obstruction_certificate.json | 79e1fe204992b86f495c6d9c2f77084714ad905844776019befc2cc0c0577fd4 |
| research/r075j_mean_zero_adjoint_flux_obstruction_certificate_report.md | ac258fd160fd1c9a9d96b4daebd8d4ce56df0c47d1fc667b8387347801f1629f |
| research/r075j_mean_zero_adjoint_flux_obstruction_independent_audit.md | 945be036b61a9682c31e18e3502ddedc4947b2caae2ee5b1c40927bd62bf638c |

The primary audit is checked against the frozen main SHA, PASS/0,
J.1--J.20, and 20/20 displays. The report-source is byte-bound only;
its literature search and access record are outside this finite certificate.

## Frozen dependency bindings

| path | SHA-256 |
|---|---|
| research/r075e_horizontal_cross_mode_flux_reduction.md | 99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049 |
| research/r075f_modal_phase_integration_identity.md | f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440 |
| research/r075h_single_pass_transport_flux_closure.md | 849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9 |
| research/r075i_diffusion_safe_block_participation.md | c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7 |

## Checks

- L/L* time, drift, diffusion, divergence, and passive-square signs: PASS.
- Physical derivative source has zero mean for every fixed parameter slice: PASS.
- Rational adjoint fixture gives (1+tau+2tau^2+tau^3)cos(x), zero terminal data, eta>0, and both slice signs: PASS.
- J.12 endpoint/bulk signs and J.5/J.13 dissipation signs: PASS.
- Constant shift cancels exactly; dropping dissipation costs CD: PASS.
- Nonnegative majorant direction and both favorable rows: PASS.
- a_+ and |a| are not the original signed mean-zero source: PASS.
- Tags J.1--J.20, references, 20/20 displays, and control bytes: PASS.

The exact signed adjoint is sign-changing. A positive majorant remains a
viable architecture, but its initial row is unpaid. This is not a blanket
no-go for resolvent or Feynman--Kac methods. Transition geometry, periodic
recrossing, E.24, complete clock, fixed deletion, suitable-weak transfer,
regularity, and singularity remain OPEN. **NOT CLAY.**
