# R0.74J independent finite-certificate audit

**Verdict:** `R074J_CERTIFICATE_INDEPENDENT_AUDIT_PASS`
**Producer arithmetic:** Python `Fraction`, 38/38 checks
**Independent arithmetic:** Ruby `Rational`, 38/38 checks

This audit is bound to the following byte sequences.

| Artifact | SHA-256 |
|---|---|
| `scripts/r074j_matching_payment_certificate.py` | `6dcc03d283612306dc39669f5b6c8b3cf8569e40205e067c4db0c2b6929879ec` |
| `research/r074j_matching_payment_certificate.json` | `493c9cf6bc1357b36da1b0a13becbc51e62ea26aab95b6af7eaeb085b65be5d5` |
| `research/r074j_matching_payment_certificate_report.md` | `6a32098c808373a7d3cfbd30b266f20d0aa33abc2b693e51b48b0c486852fa07` |
| `scripts/r074j_matching_payment_certificate_independent.rb` | `ca3da7fafea86012c58c20801e680c9bb5ed26c712c92d32cc080426f9916197` |

The verdict does not transfer to a later revision of any listed artifact.

## 1. Producer reproducibility

The producer was run with Python 3.9.6.  Its standard output was compared
directly with the frozen JSON:

```text
python3 scripts/r074j_matching_payment_certificate.py |
  cmp -s - research/r074j_matching_payment_certificate.json
```

The result was

```text
python_cmp_exit=0
PYTHON_STDOUT_BYTE_IDENTICAL=YES
```

## 2. Independent reconstruction

The independent program was run with Ruby 2.6.10.  It reconstructs every
primitive constant, all 38 exact rows, every boundary and analytic-input
string, all exact-implication strings, and the result and summary fields
before opening the frozen JSON.

The JSON is then used only as a comparison target.  No frozen value is used
as an arithmetic input.  The run returned

```text
engine=Ruby Rational independent reconstruction
frozen_json_used_as_arithmetic_input=false
independentPassed=38
independentTotal=38
leafFieldComparisons=287
mismatchCount=0
result=PASS
ruby_audit_exit=0
```

## 3. Coverage

The finite rows cover:

- fifth-shell radii and box containment;
- the exact box volume and annular exponent;
- the \(R\le1/200\) rational platform comparisons;
- Brownian-variance, Chebyshev, and conservative \(\theta\) coefficients;
- time, normalization, volume, and cubic payment powers;
- the coefficient \(8\) in the lower cubic row;
- \(\rho=1/320\), the rate \(3\rho\), and lacunarity coefficient
  \(9\rho\);
- the \(P^{2/3}\sqrt{\log P}\) monomial frontier; and
- the monomial ratio between payment and the old target lower-bound scale.

## 4. Boundary

The audit proves only that two independent exact-arithmetic implementations
agree with the frozen JSON and that all 38 finite rows pass.  It does not
prove:

1. the periodic heat-semigroup or Brownian representation;
2. the continuum shear-platform lower bound;
3. the exact Navier--Stokes family or zero-frame identities;
4. the inherited complete-payment upper bound;
5. an upper estimate for either target observable;
6. a literature novelty or priority conclusion;
7. local or global regularity; or
8. the Clay Millennium problem.

## 5. Reproduction

From the repository root:

```text
python3 scripts/r074j_matching_payment_certificate.py |
  cmp -s - research/r074j_matching_payment_certificate.json

ruby scripts/r074j_matching_payment_certificate_independent.rb
```

The first command must exit zero.  The second must report 38/38 passes, 287
matching terminal fields, zero mismatches, and overall `PASS`.

**NOT CLAY.**
