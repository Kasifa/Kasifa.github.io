# R0.74G — independent exact-certificate audit

## Verdict

**PASS: 31/31.**  The certificate producer, frozen JSON, and human-readable
report at commit

    b94365f5b32a29b4d9859896775a7f2798d93b0b

were checked read-only.

Their SHA-256 values are

| Artifact | SHA-256 |
|---|---|
| scripts/r074g_complete_payment_certificate.py | 315f4cc7f0a397287cc2eb14ec1ad65bcacb797692e2a6ce5a1459985a4853ca |
| research/r074g_complete_payment_certificate.json | 2a411007989e63e51ab7f1644724f654f26794b80507681aaf62e00adbeefd53 |
| research/r074g_complete_payment_certificate_report.md | aee995c26795c460fa76cd004f227f56a102ca2daf1040b428c313d48f3ab3bc |

## Independent recomputation

1. The Python producer was rerun.
2. Its standard output was byte-for-byte identical to the frozen JSON.
3. A separate Ruby Rational implementation recomputed every one of the 31
   records.
4. For every record, the left value, relation, right value, exact margin,
   Boolean pass value, and aggregate result agreed.

The independently recomputed checks include:

- the radial split and \(q/h\) ratio;
- the plateau-shift, buffered-energy, and complete-payment exponent gaps;
- the conditional \(B\)-calibration arithmetic;
- the path-shift and torus-chart reserves;
- the bridge heat ages and Gaussian denominator 262;
- the near/far path constants;
- the \(p=2,3\) Peetre powers; and
- the final \(R^3\) and \(R^6\) occupation outputs.

## Scope boundary

The script, JSON, and report all state that the finite certificate does not
prove:

1. the large-index heat-profile hypotheses;
2. the transverse-energy subsolution;
3. the Riesz/Newton pressure identity;
4. the Brownian-bridge representation or displacement bounds;
5. the periodic Peetre or heat-kernel moment estimates;
6. the complete denominator theorem or endpoint counterexample; or
7. any Navier--Stokes regularity, singularity, or Clay statement.

The certificate is exact finite arithmetic only.  No analytic claim is
promoted by this audit.  **NOT CLAY.**

