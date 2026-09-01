# R0.74H — independent audit of the finite collar-flux certificate

**Audit date:** 2026-09-01
**Verdict:** `R074H_CERTIFICATE_INDEPENDENT_AUDIT_PASS`
**Independent arithmetic:** Ruby `Rational`, 25/25 checks

This audit is bound to the following immutable byte sequences:

| Artifact | SHA-256 |
|---|---|
| `scripts/r074h_collar_flux_certificate.py` | `acce024b8dd78ba727e3ec8176a308dc53ecc34b7bdaf57b6c48e5d1e1a5c6e4` |
| `research/r074h_collar_flux_certificate.json` | `783591f3da880ec9182be89c585eb732e35d5842b7d196dc2ae4e35b6c0d2ba4` |
| `research/r074h_collar_flux_certificate_report.md` | `c675d4efea3edfdd3e77844b54ae34a7721902a5f03d6ace72e3dc09ce85bc27` |
| `scripts/r074h_collar_flux_certificate_independent.rb` | `9004240b7a041001fb853eb9963ed10cc768f2e2a3c4b675d1187167c051a39f` |

The verdict does not transfer automatically to a later revision of any
listed artifact.

## 1. Producer reproducibility

The Python producer was executed once and its standard output was sent
directly to a byte comparator against the frozen JSON:

```text
python3 scripts/r074h_collar_flux_certificate.py |
  cmp -s - research/r074h_collar_flux_certificate.json
```

The comparator exited successfully:

```text
PYTHON_STDOUT_BYTE_IDENTICAL=YES
```

Thus the frozen JSON is a byte-for-byte reproduction of the producer output
at the bound producer hash.

## 2. Independent reconstruction

The independent program
`scripts/r074h_collar_flux_certificate_independent.rb` uses Ruby
`Rational` arithmetic.  It does not execute, import, or translate the
Python producer.  It reconstructs the parabolic measure powers, Holder
normalization, outer and inner payment powers, R0.74G amplitude powers,
the substitution (B\asymp R^{-2}), and the finite shell-tail marker from
their primitive rational constants.

Only after constructing all 25 rows does the Ruby program read the frozen
JSON as a comparison target.  No JSON value is used as an arithmetic input.
For every row, it compares exactly these six fields:

```text
id / relation / left / right / margin / pass
```

The independent run returned:

```text
engine=Ruby Rational independent reconstruction
checks=25
independentPassed=25
fieldComparisons=150
mismatchCount=0
frozenSummaryMatch=true
frozenResultMatch=true
result=PASS
```

## 3. Coverage of the 25 rows

The independently reconstructed identifiers, in frozen order, are:

1. `parabolic_measure_power`
2. `holder_volume_one_third`
3. `quadratic_cutoff_prefactor`
4. `normalized_S2_power`
5. `normalized_S3_two_thirds_power`
6. `quadratic_row_exponent_match`
7. `energy_payment_outer_power`
8. `acceleration_payment_outer_power`
9. `collar_payment_outer_power`
10. `small_payment_absorption_exponents`
11. `large_payment_two_regime_exponents`
12. `amplitude_gamma_cancellation`
13. `old_payment_23_B_power`
14. `old_payment_23_R_power`
15. `old_payment_23_L_power`
16. `target_over_old_23_L_power`
17. `cubic_flux_B_power`
18. `cubic_flux_L_power`
19. `cubic_flux_R_power`
20. `cubic_flux_beats_old_L_power`
21. `old_payment_under_B_Rminus2`
22. `target_under_B_Rminus2`
23. `reference_payment_scale_diverges`
24. `finite_tail_ratio_exponent_at_j4`
25. `flux_repair_sum_constant`

Every independently computed rational numerator and denominator agrees with
the frozen JSON.  Equality rows have zero margin; the four strict rows have
the same positive margins and truth values recorded in the certificate.
The frozen `25/25` summary and `PASS` result also agree independently.

## 4. Finite arithmetic boundary

This audit verifies only the finite rational arithmetic encoded by the 25
certificate rows and the reproducibility of the certificate serialization.
In particular, it does **not** prove:

1. the weighted Navier--Stokes energy identities or their signs;
2. the (C^2) shell-sum limit, unfolding, or infinite-tail convergence;
3. the Holder, Calderon--Zygmund, harmonic-pressure, or residual-transport
   estimates;
4. the Version-F acceleration moment estimate;
5. the R0.74F--G packet construction, lobe residence, or collar-flux lower
   bound;
6. a lower bound for the actual nonlinear payment;
7. the R0.74H two-regime theorem, epsilon regularity, or continuation; or
8. a singularity, global-regularity theorem, or solution of the Millennium
   problem.

The analytic claims require their separate proofs and independent audits.
The finite certificate cannot replace them.

**NOT CLAY.**

## 5. Reproduction

From the repository root:

```text
python3 scripts/r074h_collar_flux_certificate.py |
  cmp -s - research/r074h_collar_flux_certificate.json

ruby scripts/r074h_collar_flux_certificate_independent.rb
```

The first command must exit zero.  The second must report 25/25 independent
passes, 150 matching field comparisons, zero mismatches, and overall
`PASS`.
