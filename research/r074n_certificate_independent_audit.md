# R0.74N finite certificate — independent audit

## Verdict

**PASS.** A separate Ruby Rational implementation reconstructed the full
84-row certificate from the primitive constants and formulas. It did not
invoke or import the Python generator. It compared the reconstructed
structure, row order, notes, canonical rational strings, sequence tables,
status boundary, and byte-level JSON hash.

## Audited inventory

The independent program checked:

1. \(c_\gamma=8/3969\), \(\rho=1/320\), and
   \(c_\gamma\lambda^2=1/128\);
2. the exact reserves \(72851/1270080\) and \(1237/423360\);
3. \(4^{j+1}/L_j^2=4096/3969\) and the adjacent and inward
   \(\Gamma\)-ratio exponent algebra;
4. eight \(\Gamma\)-algebra rows, eight combined-chord ratio rows, and eight
   outer-tail ratio rows over the explicit window \(14\le j\le 21\);
5. the monotone factor-four propagation and the \(1/2\) ratio thresholds;
6. the combined-chord majorant \(22\) and outer geometric factor \(2\); and
7. all raw \(L\)- and \(R\)-power ledgers.

All exponential ratio gates were reconstructed through exact Taylor
polynomials. Neither implementation used floating-point comparisons.

## Nominal run

Command:

~~~sh
ruby scripts/r074n_all_shell_certificate_independent.rb
~~~

Observed result:

~~~text
audit_window: j=14..21
gamma_rows: 8
chord_rows: 8
outer_rows: 8
RESULT: PASS (84/84 checks)
PASS 84/84
~~~

Exit code: \(0\).

The audited JSON SHA-256 was

~~~text
53481cf393308a786c3a414da6238faaa9b8a15dac0017638c47584615bbecc2
~~~

## Determinism and fail-closed tests

Regenerating the JSON into a temporary file produced the same SHA-256 and a
byte-comparison exit code of \(0\).

For the fail-closed test, one occurrence of the bad-reserve rational was
changed in a temporary copy. The Ruby verifier returned exit code \(1\) and
reported all three applicable barriers:

~~~text
row schema: noncanonical rational "72850/1270080"
independent reconstruction differs from JSON
certificate SHA-256 ... != 53481cf393308a786c3a414da6238faaa9b8a15dac0017638c47584615bbecc2
~~~

Thus a changed row cannot pass merely by retaining a stale “pass: true,” and
a structurally plausible regenerated file cannot pass without the frozen
hash being deliberately rebound.

## Frozen implementation hashes and sizes

| artifact | lines | SHA-256 |
|---|---:|---|
| scripts/r074n_all_shell_certificate.py | 466 | 1174dfba5484fa53f4022ed5725bbd511cf4596f5b133997262844c439857e8c |
| scripts/r074n_all_shell_certificate_independent.rb | 412 | 32621a28ca2312fcddea83135309ecd7cd3cc3d2515f929b401d04b9d221f744 |
| research/r074n_all_shell_certificate.json | 1083 | 53481cf393308a786c3a414da6238faaa9b8a15dac0017638c47584615bbecc2 |

## Analytic boundary

This audit certifies finite exact arithmetic and fail-closed reproducibility
only. It does not certify the combined-chord geometry, periodization,
common-forward law, expulsion lemma, maximum principle, outer volume bound,
or infinite-shell convergence. It does not replace the independent
analytic audit of R0.74N, and it implies no universal Navier–Stokes or Clay
claim. **FINITE ONLY; NOT CLAY.**
