# R0.74T Step 19 independent Ruby audit

- Schema: r074t-schedule-invariant-dwell-independent-v1
- Source note: research/r074t_schedule_invariant_dwell_coercivity.md
- Source SHA-256: 8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd
- Literature SHA-256: 60b49f6279c696a370af5f8050a6162753372eba81f8215e02e15259f084e88b
- Independent groups: 11/11
- Exact assertions: 9201

## Verdict

**PASS**

This Ruby audit independently reconstructs the finite exponent, Holder,
time-floor, clock-quantifier, logarithmic, and asynchronous-window checks
before reading the primary JSON contract.

## Group inventory

| Group | Result | Assertions |
|---|---:|---:|
| independent_atomic_exponent_ledger | PASS | 5 |
| independent_perfect_power_grid | PASS | 6144 |
| independent_finite_holder_and_time_floor | PASS | 2730 |
| independent_two_clock_quantifiers | PASS | 17 |
| independent_illegal_replacement_witnesses | PASS | 9 |
| independent_volume_and_overlap_witnesses | PASS | 3 |
| independent_logarithmic_threshold | PASS | 221 |
| independent_asynchronous_interval_algebra | PASS | 33 |
| independent_source_and_literature_structure | PASS | 19 |
| independent_hash_locks | PASS | 8 |
| independent_primary_certificate_contract | PASS | 12 |

## Claim boundary

- Finite cells do not machine-prove continuous Holder or the lobe theorem.
- The K-clock floor yields only the explicit fixed-deletion witness h_*.
- It cannot be replaced by the full completed clock or stopped-flux Hfix.
- Exact common-shear evolution, survival, dominance, and shell placement remain analytic inputs.
- The asynchronous construction is restricted to the inherited terminal slab.
- No full clock estimate, regularity theorem, or Clay claim is certified.

## Failures

None.
