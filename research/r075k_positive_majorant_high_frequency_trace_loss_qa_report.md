# R0.75K certificate QA report

- Verdict: **PASS**
- Mathematical blockers: 0
- Python assertions: 19/19
- Ruby assertions: 21/21
- Negative mutations rejected: 100/100 Python; 100/100 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS

## Release manifest

| path | SHA-256 |
|---|---|
| research/r075k_positive_majorant_high_frequency_trace_loss.md | 9282fb30eb7517853759fb835579220e0da763974d5543e2fb260ec8ca6daebf |
| research/r075k_positive_majorant_high_frequency_trace_loss_primary_audit.md | 401f12d9a5f35646638ae08446a1177a0b0485b9bbb54206702dee9fc7e7a4a2 |
| research/r075k_report-source.md | 5a45521ecb5e85b69b077af9d4db3cbb1c52dc1b61cccf8fb3bbb9daabac7001 |
| scripts/r075k_positive_majorant_high_frequency_trace_loss_fixtures.json | f15df9bf59d6a96151f84ae2fa11a12b3965820450fbad526d4f71f11a6f7328 |
| scripts/r075k_positive_majorant_high_frequency_trace_loss_expected.json | 5ad1107080ccf033e842521e8f985196357d6cb858f945b007a5df50c2a12d77 |
| scripts/r075k_positive_majorant_high_frequency_trace_loss_certificate.py | 0093790920b5ed66fac3fbc808b1ea34e311124f201d54b60d71c3bd57f44661 |
| scripts/r075k_positive_majorant_high_frequency_trace_loss_certificate_independent.rb | 9caa3aa1b3ca13ff7cc8403a352c55089809ff237c0939c42cadcd8d11e52564 |
| scripts/r075k_positive_majorant_high_frequency_trace_loss_qa.sh | a31c9c8f566d33f169f9a6b63a77770f104b74471efd8483549544ef10095212 |
| research/r075k_positive_majorant_high_frequency_trace_loss_certificate.json | 50e278d5307a85c515f1f879e7ff38438678b709e6a18c14791c60289c5c55eb |
| research/r075k_positive_majorant_high_frequency_trace_loss_certificate_report.md | 2dee099eabc2a3db8a9ee48cc6c4a3f2b64cbc930444268d925b0ec70a376919 |
| research/r075k_positive_majorant_high_frequency_trace_loss_independent_audit.md | 107cfbaab6f29b596f9f9a3d6808e733f63d6cf9ec0dfd7c6b391391ca4cd92a |

The primary audit is checked against the frozen main SHA, PASS/0,
K.1--K.18, and 18/18 displays. The report-source is byte-bound only;
its literature search and access record are outside this finite certificate.

## Frozen dependency bindings

| path | SHA-256 |
|---|---|
| research/r075e_horizontal_cross_mode_flux_reduction.md | 99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049 |
| research/r075i_diffusion_safe_block_participation.md | c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7 |
| research/r075j_mean_zero_adjoint_flux_obstruction.md | 960e3cbc18ac8207253a8802da215b3eac07a714ddbcc7209985f27a00c9ff4d |

## Checks

- L/L* time, drift, and diffusion signs: PASS.
- q=1+cos(x)>=cos(x), q>=0, positive reversed semigroup, and zero terminal data: PASS.
- Phi(0) has only modes 0,+/-1 and spatial mass 2*pi*T: PASS.
- LF_k=0 and F_k(0)^2 has only modes 0,+/-2k: PASS.
- B_k/pi=A^2*T/2 for k=1,2,5 and every integer-k signed flux is zero: PASS.
- Integral |cos(kx)|^3=8/3 and M_k=8A^3(1-exp(-3k^2T))/(9k^2): PASS.
- A cancels and the boundary/payment ratio grows as k^(4/3): PASS.
- Fixed-W-first quantifier and Riemann--Lebesgue boundary: PASS.
- Tags K.1--K.18, references, 18/18 displays, and control bytes: PASS.

The no-go is limited to a fixed nonnegative entrance weight combined with
the local spacetime cubic atom alone. It does not refute E.24, adaptive or
signed majorants, or the full Version-M ledger. Transition/periodic geometry,
complete clock, fixed deletion, suitable-weak transfer, regularity, and
singularity remain OPEN. **NOT CLAY.**
