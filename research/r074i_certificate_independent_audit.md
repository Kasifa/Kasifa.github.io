# R0.74I — independent audit of the tube/log finite certificate

**Audit date:** 2026-09-02
**Verdict:** `R074I_CERTIFICATE_INDEPENDENT_AUDIT_PASS`
**Producer arithmetic:** Python `Fraction`, 36/36 checks
**Independent arithmetic:** Ruby `Rational`, 36/36 checks

This audit is bound to the following byte sequences:

| Artifact | SHA-256 |
|---|---|
| `scripts/r074i_tube_log_certificate.py` | `5411134949eedbb1c285607c33a4f8feb9f8d358f5fc7cee91ec3601dfe3932f` |
| `research/r074i_tube_log_certificate.json` | `d4d0f32f6772bdae8a9ec0e8fd6f5f5f9248877df3c19bf544c3577055ab7bf5` |
| `research/r074i_tube_log_certificate_report.md` | `3be483123d3841a7f195a192374d56bb9ef453fe3ba2ee59ed6dc2e4fa68b0bf` |
| `scripts/r074i_tube_log_certificate_independent.rb` | `2c591dac16bce3ea456070775ac9c68408f0b32fb1492cd039b6e7d52f0040ad` |

The verdict does not transfer to a later revision of any listed artifact.

## 1. Producer reproducibility

The producer was run with Python 3.9.6.  Its standard output was compared
directly with the frozen JSON:

```text
python3 scripts/r074i_tube_log_certificate.py |
  cmp -s - research/r074i_tube_log_certificate.json
```

The result was

```text
python_cmp_exit=0
PYTHON_STDOUT_BYTE_IDENTICAL=YES
```

The frozen JSON is therefore a byte-for-byte reproduction of the producer at
the hash recorded above.

## 2. Independent reconstruction

The independent program was run with Ruby 2.6.10.  It uses `Rational`
arithmetic and does not execute, import, translate, or inspect the Python
producer.  It reconstructs all primitive constants, all 36 arithmetic rows,
the row notes, the six exact-implication fields, the eight boundary fields,
and the result and summary fields before opening the frozen JSON.

Only after that reconstruction is complete does the Ruby program read the
JSON as a comparison target.  No value from the JSON is used as an arithmetic
input.  The run returned

```text
engine=Ruby Rational independent reconstruction
frozen_json_used_as_arithmetic_input=false
independentPassed=36
independentTotal=36
leafFieldComparisons=269
mismatchCount=0
result=PASS
ruby_audit_exit=0
```

The 269 terminal fields comprise:

- 252 fields from 36 check rows, with seven fields per row;
- 8 analytic-boundary strings;
- 6 exact-implication strings;
- 1 result field; and
- 2 summary fields.

Every reconstructed field agrees with the frozen JSON.

## 3. Coverage of the 36 exact rows

The independently reconstructed identifiers, in frozen order, are:

1. `ns_rescaled_velocity_cubic_power`
2. `ns_inverse_space_jacobian_power`
3. `ns_inverse_time_jacobian_power`
4. `ns_scaled_l3_total_power`
5. `ns_physical_l3_integral_power`
6. `ns_normalized_l3_scale_invariance`
7. `half_radius_time_length_factor`
8. `half_radius_normalization_factor`
9. `half_radius_fixed_factor_product`
10. `energy_from_payment_inverse_power`
11. `tube_to_payment_threshold_power`
12. `l3_to_payment_threshold_chain`
13. `rho_exact_value`
14. `two_rho`
15. `three_rho`
16. `log_window_width`
17. `next_L_prefactor`
18. `L_square_ratio`
19. `next_lower_log_exponent`
20. `lacunarity_log_exponent`
21. `payment_upper_23_B_power`
22. `payment_upper_23_R_power`
23. `payment_upper_23_L_power`
24. `sqrt_log_recovers_L_power`
25. `frontier_total_L_power`
26. `subcritical_gap_constant_coefficient`
27. `subcritical_gap_delta_coefficient`
28. `endpoint_gamma_gap`
29. `endpoint_L_cancellation`
30. `endpoint_inverse_outer_power`
31. `endpoint_payment_power`
32. `endpoint_forced_B_power`
33. `endpoint_forced_R_power`
34. `endpoint_forced_K_power`
35. `eventual_b_lower_is_below_limit`
36. `eventual_b_upper_is_above_limit`

All equality rows have zero margin.  The two strict rational comparisons have
positive margins, and their truth values agree in both implementations.

## 4. What the audit establishes

The audit establishes only that:

1. the Python producer serializes a 36/36 exact rational certificate;
2. the frozen JSON reproduces that output byte for byte;
3. an independent Ruby implementation reconstructs the same finite
   arithmetic; and
4. every terminal JSON field agrees across the independent reconstruction
   and the frozen artifact.

The checked arithmetic includes the scale invariance of
(r^{-2}\int|u|^3), the inverse (3/2)-to-(2/3) threshold chain, the
values (2\rho=1/160) and (3\rho=3/320), the lacunarity exponent
(8\rho-3\rho=5\rho=1/64), the (B^2R^2L) frontier exponent, and the
conditional endpoint powers (K^{-3/2}B^3R^3).

## 5. Finite-certificate boundary

Neither implementation, the frozen JSON, nor this audit proves or verifies:

1. the local energy inequality or the moving-test limit;
2. existence, uniqueness, confinement, or estimates for the mollified path;
3. the fixed-cylinder interpolation inequality;
4. the velocity-only epsilon-regularity criterion;
5. the R0.74F--H packet construction or any packet upper or lower bound;
6. the literature boundary, novelty, or priority;
7. local regularity, singularity exclusion, continuation, or global
   smoothness; or
8. the Clay Millennium problem.

Those items require separate analytic proofs, source checks, and audits.  A
finite exponent certificate cannot replace them.  **NOT CLAY.**

## 6. Reproduction

From the repository root:

```text
python3 scripts/r074i_tube_log_certificate.py |
  cmp -s - research/r074i_tube_log_certificate.json

ruby scripts/r074i_tube_log_certificate_independent.rb
```

The first command must exit zero.  The second must report 36/36 independent
passes, 269 matching leaf-field comparisons, zero mismatches, and overall
`PASS`.
