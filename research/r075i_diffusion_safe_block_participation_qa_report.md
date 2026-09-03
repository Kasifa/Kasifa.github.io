# R0.75I certificate QA report

- Verdict: **PASS**
- Python assertions: 18/18
- Ruby assertions: 24/24
- Negative mutations rejected: 83/83 Python; 83/83 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS

## Release manifest

| path | SHA-256 |
|---|---|
| research/r075i_diffusion_safe_block_participation.md | c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7 |
| research/r075i_diffusion_safe_block_participation_primary_audit.md | a8e481bfa28ba244a6022b782880ce9a86c40de29e3b0064474841eca99cecbd |
| research/r075i_report-source.md | 8459adb6735caa2ee6c6e9c27202125cda34ad9072e2d78167f3f961e34f5de3 |
| scripts/r075i_diffusion_safe_block_participation_fixtures.json | afda306afcf26640be72978b654a1a7dd1b23c0df5e92137f450520a6c7d515b |
| scripts/r075i_diffusion_safe_block_participation_expected.json | 27514a38beec5c5e949a2a639faa5db539a4fbdeefec175e9e6e90a0507afd2a |
| scripts/r075i_diffusion_safe_block_participation_certificate.py | a9e006ee41fcb818bf8403f60efceb0fd08e62c42e5973065d853967ae7218df |
| scripts/r075i_diffusion_safe_block_participation_certificate_independent.rb | f4b3ceb0534a4bbd4861fd441accfaeb95374d5e9d91682b7fb66462519c73d0 |
| scripts/r075i_diffusion_safe_block_participation_qa.sh | a24faf1abe00423f5c1e245efddcad59c4876989a671a19cee8066aed6f06e7e |
| research/r075i_diffusion_safe_block_participation_certificate.json | fc31d5b56d7d651885116d9624258075173e78476d8a173f99a20f2a5197f027 |
| research/r075i_diffusion_safe_block_participation_certificate_report.md | dd775b48be540c91619b9e2254f0f93ef297e513f6a99beb9d63ba393dedfc3b |
| research/r075i_diffusion_safe_block_participation_independent_audit.md | e23174aa885311d07a097cdf9d8f571d0d6d1f59f33bdb6e4ceafb0ab4f5e4b2 |

The primary audit is bound to the final main SHA and checked for PASS/0,
I.1--I.27, and the corrected 27/27 display count. The report-source is
byte-bound only; its literature search is outside this finite certificate.

## Frozen dependency bindings

| path | SHA-256 |
|---|---|
| research/r075b_bulk_clock_outer_padding_gate.md | 430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a |
| research/r075c_background_shear_packing_false_positive.md | 1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89 |
| research/r075e_horizontal_cross_mode_flux_reduction.md | 99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049 |
| research/r075g_signed_flux_gain_threshold.md | f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41 |
| research/r075h_single_pass_transport_flux_closure.md | 849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9 |

## Checks

- I.5--I.13 intermediate and final R/L/omega/p powers: PASS.
- Nonconstant rational one-block Holder and strict payment margins: PASS.
- Perfect-cube participation cases, exact identity, and 1 <= N_eff <= N: PASS.
- Unequal atoms [1,8] give N_eff=125/81 exactly: PASS.
- Signed positive-part triangle inequality and Version-M upper-payment direction: PASS.
- theta*=8558/35721, beta*=27163/35721, both endpoint strictness checks: PASS.
- Rates -4279/238140000 and 27163/476280000, with below/above signs: PASS.
- I.27 zero mode: equal positive p_j, N_eff=N=4, and every block flux zero: PASS.
- Tags I.1--I.27, references, 27/27 displays, and control bytes: PASS.

The one-block estimate uses no PDE and is diffusion-safe, but it does not
prove a participation bound. I.19 is sufficient only; high N_eff is not
a necessary obstruction or an E.24 counterexample. Signed cancellation,
transition bands, recrossing, E.24, complete clock, fixed deletion,
suitable-weak transfer, regularity, and singularity remain OPEN.
**NOT CLAY.**
