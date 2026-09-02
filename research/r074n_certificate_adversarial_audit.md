# R0.74N finite certificate — adversarial audit

## Verdict

**PASS, with the stated finite-only scope.**  I reconstructed the arithmetic
from the primitive constants, inspected both implementations, ran them
separately, checked the complete 84-row inventory, and tested two distinct
tampering modes.  I found no blocking discrepancy.  This audit does not
inherit the producer's `PASS` flag as evidence.

The audited certificate is exactly

~~~text
SHA-256  53481cf393308a786c3a414da6238faaa9b8a15dac0017638c47584615bbecc2
lines     1083
bytes     28930
~~~

## 1. Independence of the two implementations

The Python producer and Ruby verifier share no executable code.  The Ruby
program does not invoke Python and does not read derived JSON fields as
mathematical inputs.  It starts again from

\[
 \lambda=\frac{63}{32},\qquad
 c_\gamma=\frac8{3969},\qquad
 \rho=\frac1{320},\qquad
 c_{\rm def}=\frac1{640},\qquad
 32768,
\]

reconstructs the rows, arrays, metadata and row order with Ruby `Rational`,
and only then compares that reconstruction with the parsed JSON.  It also
requires the frozen byte hash.  Thus a change must pass two different
barriers: exact structural reconstruction and byte identity.

The nominal runs observed here were

~~~text
python_rc = 0
regenerated_JSON_cmp_rc = 0
ruby_rc = 0
RESULT: PASS (84/84 checks)
PASS 84/84
~~~

The regenerated Python output had the same SHA-256 as the frozen JSON.

## 2. Complete 84-row inventory

The JSON contains 84 rows, 84 unique identifiers, 84 stored true relations,
and the summary `84/84`.  The independently reconstructed partition is

| block | rows |
|---|---:|
| primitive constants, reserves and sequence thresholds | 24 |
| inward \(\Gamma\)-ratio exponents, \(m=1,\ldots,8\) | 8 |
| five rows at each \(j=14,\ldots,21\) | 40 |
| raw \(L,R\)-power ledgers | 12 |
| **total** | **84** |

The relation types are 64 equalities, 18 strict upper inequalities and two
strict lower inequalities.  Every stored rational is canonical, every
stored margin agrees with its relation, and no row identifier is duplicated.

## 3. Primitive arithmetic and exponent payments

Direct reduction gives

\[
 c_\gamma\lambda^2
 =\frac8{3969}\frac{63^2}{32^2}=\frac1{128},
\]

\[
 \frac1{16}-\rho-c_\gamma
 =\frac{72851}{1270080}>0,
 \qquad
 3c_\gamma-\rho
 =\frac{1237}{423360}>0,
\]

and

\[
 \frac4{\lambda^2}=\frac{4096}{3969},\qquad
 2(\rho-c_{\rm def})=\frac1{320},
\]

\[
 1056\cdot32768^2=1133871366144.
\]

These are the exact quantities stored by both implementations.  The first
strict reserve pays the extra \(R\) in the bad inward row; the second pays
the extra \(R^{-1}\), together with polynomial excess, in the summed outer
row.  No numerical exponential approximation is hidden in these checks.

## 4. Window and monotone propagation

For

\[
 \Gamma_k=\exp\!\left(-\frac{4^{k-1}}{32}\right),\qquad
 \delta_k=\frac{3\,4^{k-1}}{32},
\]

the adjacent difference satisfies the exact identity

\[
 \delta_{k+1}=4\delta_k.
\]

For \(b_k=2^k\Gamma_k\), one has

\[
 \frac{b_{k+1}}{b_k}=2e^{-\delta_k}.
\]

At \(k=3\), \(\delta_3=3/2\), and the exact cubic Taylor lower bound is
\(67/16\).  Therefore

\[
 \frac{b_4}{b_3}\le\frac{32}{67}<\frac12.
\]

The factor-four growth makes this threshold propagate to every \(k\ge3\),
so

\[
 \sum_{k\ge1}2^k\Gamma_k
 \le2+4+2\cdot8=22.
\]

Likewise, for \(a_k=4^k\Gamma_k\), at \(k=4\) one has \(\delta_4=6\)
and the exact quadratic Taylor lower bound \(25\).  Hence

\[
 \frac{a_5}{a_4}\le\frac4{25}<\frac12,
 \qquad
 \sum_{k\ge j+1}a_k\le2a_{j+1}
\]

for the audited range, and in fact whenever \(j+1\ge4\).

The eight-index window \(14\le j\le21\) is internally complete: at each
index it independently recomputes \(L_j^2\), the \(\Gamma_j\) exponent,
the outer jump, \(4^{j+1}/L_j^2\), the last inward ratio envelope and the
first outer-tail ratio envelope.  The base value \(j=14\) is inherited from
the R0.74L discrete threshold.  The proof beyond \(j=21\) rests on the exact
factor-four propagation above, not on extrapolating eight sampled values.

For \(m=1,\ldots,8\), the two independently evaluated expressions

\[
 c_\gamma(1-4^{-m})L_{14}^2,
 \qquad
 \frac{4^{13}-4^{13-m}}{32}
\]

agree exactly.

## 5. Raw scale ledgers

The ledger rows agree with the analytic source before any exponential
payment:

\[
 R^6R^2R^{-1}R^{-3}=R^4
 \quad\text{(inner bad)},
\]

\[
 R^6R^2R^{-1}R^{-4}=R^3
 \quad\text{(inner good)},
\]

\[
 R^2\cdot R^2=R^4
 \quad\text{(one outer shell)},
\]

and outer summation contributes \(4^{j+1}\asymp L^2\), leaving
\(L^2R^4\).  The inherited main row and the target are both \(LR^5\).
The chord bound is uniform, so neither inner raw ledger has an additional
\(L\)-power.  The JSON correctly keeps the later exponential payments out
of these polynomial rows.

## 6. Fail-closed tampering tests

Two temporary copies were made; the frozen repository file was never
written.  Its SHA-256 was identical before and after both tests.

1. **Single-byte, semantics-preserving mutation.**  One legal trailing
   whitespace byte was added.  JSON parsing and structural content were
   unchanged, but Ruby exited \(1\) because the byte hash changed to
   `47d5fa1aac6edfbd3424627affd05ce2d71e951bbc209cea20c3c97131327385`.
2. **Canonical field mutation.**  The derived field `outer_tail_factor`
   was changed from the canonical rational `2/1` to the canonical rational
   `3/1`.  Ruby exited \(1\), reporting both an independent-reconstruction
   mismatch and a SHA mismatch.  The tampered hash was
   `8b0250d446f4d38fa2c6082c771ac777c6bb1a8fd7d754741fd88ce68b38a887`.

This is stronger than testing only a malformed rational: both adversarial
files remain valid JSON, and the field mutation remains canonically encoded.

## 7. Frozen five-file binding

| artifact | lines | bytes | SHA-256 |
|---|---:|---:|---|
| `scripts/r074n_all_shell_certificate.py` | 466 | 15640 | `1174dfba5484fa53f4022ed5725bbd511cf4596f5b133997262844c439857e8c` |
| `research/r074n_all_shell_certificate.json` | 1083 | 28930 | `53481cf393308a786c3a414da6238faaa9b8a15dac0017638c47584615bbecc2` |
| `research/r074n_all_shell_certificate_report.md` | 175 | 4514 | `3c10f8925fb8e89e891774310ec118652ac59997ca9bdf2c002f4bbdbdcaeb99` |
| `scripts/r074n_all_shell_certificate_independent.rb` | 412 | 15919 | `32621a28ca2312fcddea83135309ecd7cd3cc3d2515f929b401d04b9d221f744` |
| `research/r074n_certificate_independent_audit.md` | 90 | 3126 | `53a8d9c71955070c56587c2370cc5a45388084c1dcd16bac366f34e4e73e20d2` |

## 8. Strict boundary

This audit certifies exact finite arithmetic, deterministic reproduction,
the stated sequence-propagation ledger, raw scale bookkeeping and
fail-closed binding only.  It does not certify the combined-chord geometry,
periodization, common-forward law, final-segment expulsion, maximum
principle, outer collar-volume estimate or infinite-shell limit.  It does
not prove a universal Navier--Stokes estimate, regularity, singularity, or
the Millennium problem.  **FINITE ONLY; NOT CLAY.**
