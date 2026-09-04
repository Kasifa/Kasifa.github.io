# R0.75P certificate QA report

- Verdict: **PASS**
- Mathematical blockers: 0
- Python assertions: 21/21
- Ruby assertions: 22/22
- Negative mutations rejected: 132/132 Python; 132/132 Ruby
- Unknown mutations rejected fail-closed by both implementations: PASS
- PYTHONHASHSEED byte stability: PASS (0, 1, 42)
- Canonical JSON and both generated reports are regeneration-stable: PASS

## Release manifest

| path | SHA-256 |
|---|---|
| research/r075p_buffered_collar_entrance_concentration.md | 8df38e54514d82102cd3e568e89ec1db93913da3ceac52f1371d77fd79c1b7a6 |
| research/r075p_buffered_collar_entrance_concentration_primary_audit.md | e065759a1df3c118f71dd47ac9b5ded9df40536217f557b3c1155e8bf64d3390 |
| research/r075p_report-source.md | fcde6bed847b0628aff7de90a49e8150e4a279fca8e46d7053943fdadf0478ca |
| scripts/r075p_buffered_collar_entrance_concentration_fixtures.json | 9d9bf2a00fbdf58eb85a01a3f7fe931f289a5bc1166430dac1f704e4406ec6d7 |
| scripts/r075p_buffered_collar_entrance_concentration_expected.json | cc472fb797c98d61e004c09fb84ba4a29029d72665f60507628c166134b39d31 |
| scripts/r075p_buffered_collar_entrance_concentration_certificate.py | 5c13e8bb480e4565a4b7be6f6d86a0a963cea5ce9d53495f5e0cf3c7983b1c6c |
| scripts/r075p_buffered_collar_entrance_concentration_certificate_independent.rb | 5fb32514dc125462239adc31bc5da58460946d8caaed0d3a1c76d6620b8bfd2c |
| scripts/r075p_buffered_collar_entrance_concentration_qa.sh | 8c4fbeb7667bdb4f937e66cd73d663fa8cd85538412e538259b9a0128f9a27fb |
| research/r075p_buffered_collar_entrance_concentration_certificate.json | acbb41a489120b00a32f75999909f0cabce4f96ac5e8650c3ebfd2e0a35dc0a8 |
| research/r075p_buffered_collar_entrance_concentration_certificate_report.md | 1c9bc9553d1facdab0b385a59480c378dfd516412c38eb3a20e76049745560ac |
| research/r075p_buffered_collar_entrance_concentration_independent_audit.md | 60b042b5830167508f096fe7d990f7d2b5fca99da312f0e6116b8c39c0c7923d |

The primary audit and report-source are byte-bound. Literature completeness
is outside this finite suite; the bounded source screen is not novelty evidence.

## Frozen dependency bindings

| path | SHA-256 |
|---|---|
| research/r075b_bulk_clock_outer_padding_gate.md | 430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a |
| research/r075i_diffusion_safe_block_participation.md | c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7 |
| research/r075n_radial_collar_averaged_wiener_row.md | ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318 |
| research/r075o_vertical_diffusion_packet_gain.md | 3efb39d2624cf5b5a0e7f348f6cde2ef2416eca900f1aa3ecc90a6ad734849a9 |

## Checks

- P.10 exact fibre length, safe radius, and 4*delta0*R lower bound: PASS.
- Moving-cutoff sign, local-energy identity, 4*K^2, 8+C_phi, tau, and displacement: PASS.
- Holder volume, c*, mu^(5/2), inverse powers, and O+N combination: PASS.
- R/omega normalization and strict sigma*=8558/178605: PASS.
- P.1--P.31, references, 31/31 displays, four dependencies, and control bytes: PASS.
- P.31 same-v_R actual-component realization and nonnegative ledger direction: PASS.

P.31 is only a conditional realized-subclass payment statement. Fourier/LP
projections and arbitrary zero-trajectory realization are excluded. P.3--P.30
do not use that realization hypothesis. Low concentration is not a counterexample;
the localized signed-kernel branch, E.24, complete clock, fixed deletion,
suitable-weak transfer, regularity, and singularity remain OPEN. **NOT CLAY.**
