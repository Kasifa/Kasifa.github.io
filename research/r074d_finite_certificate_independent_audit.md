# R0.74D — independent audit of the finite algebra certificate

**Audit date:** 2026-09-01

**Overall assessment:** `PASS_WITH_EXPLICIT_ANALYTIC_BOUNDARY`

**Share status:** `READY_TO_SHARE_WITH_CAVEATS`

**Audit object:**

- theorem commit
  `ff80370fe33094f1423d312b817dfec0bf42d664`;
- `research/r074d_certificate_freeze.json`;
- `scripts/r074d_zero_mean_transport_certificate.py`;
- `research/r074d_zero_mean_transport_certificate.json`; and
- `research/r074d_zero_mean_transport_certificate_report.md`.

This is an independent, read-only audit of the **finite certificate**, not a
second proof of the analytic theorem.  The main recomputation did not import
the producer module and did not use the producer's internal `check` results as
its arithmetic authority.  It read the theorem blob directly with `git show`,
used a separate `fractions.Fraction` monomial calculation, independently
flattened the certificate JSON, parsed the producer as Python AST for the
literal-self-equality test, and used producer executions only as supplementary
byte-determinism evidence.

No discrepancy was found within this finite scope.

---

## 1. Frozen provenance

### 1.1 The theorem blob, not moving `HEAD`

The audited analytic source was read directly from

```text
ff80370fe33094f1423d312b817dfec0bf42d664:
research/r074d_zero_mean_local_transport_obstruction.md
```

The independently computed SHA-256 of those blob bytes is

```text
bc9f7557e27bb86d5730273985b60f7135ccea3adc2fc99b2daf7778e70c9124
```

It equals `expected_sha256.analytic_source` in the freeze manifest.  The
current work-tree source bytes also equal the frozen commit blob, but this
agreement is only a convenience: the commit blob was the authority used by
the recomputation.

The commit resolves exactly to the full identifier above and has subject
“Prove R0.74D zero-mean transport obstruction.”

### 1.2 Producer and outer version-control envelope

The independent SHA-256 of the producer bytes is

```text
c28b9f80070e67cb36e6f7ed8e80164fe8dd7d944fe4e8d5f3cc824eb764981a
```

It equals `expected_sha256.certificate_producer` in the freeze manifest.  The
manifest is canonical JSON: sorted compact serialization followed by one
newline reproduces its bytes exactly.

The manifest does not hash itself.  Its non-self-referential outer envelope is
the certificate commit

```text
1a8568fb34dc2ae42f908e4d45d7210db699d83d
```

All four current certificate artifacts—manifest, producer, JSON, and
report—were compared byte-for-byte with their blobs in that commit and all
four matched.

Additional audit hashes are:

| Artifact | SHA-256 |
|---|---|
| freeze manifest | `3b96579dc9e3502e779c3154f6cae46f4e9ac40542ce1216ba1fda8a6e8d587c` |
| certificate JSON | `69eecc7884a153bc5d4936c7d3dee9d3c736f5db69c20ba59b486165be96dec9` |
| certificate report | `937a5fd73b004f262e970b80ec7e118a39b9e971c39e84ffc988f643be811c1a` |

**Provenance verdict:** `PASS`.

---

## 2. Independent rational recomputation

### 2.1 Source primitives

The frozen theorem blob contains the exact declarations used below:

\[
 M_m=3\,2^{m-1},\qquad
 \gamma_m=e^{-4^{m-1}/32},\qquad
 \Pi_m=(1+M_m)^{18},
\tag{2.1}
\]

\[
 R_m=e^{-M_m^2/96},\qquad
 \mathfrak a_m=R_m^{-2}e^{M_m^2/576},
\tag{2.2}
\]

together with the pointwise leakage exponent \(-1/528\), its quadratic and
cubic rows, the target row
\(A^2M_mR^2e^{-M_m^2/288}\), and the three denominator
rows in (6.14).

The audit required these strings to be present in the frozen blob, then
recomputed the arithmetic independently.  It did not infer the truth of the
underlying analytic estimates from their presence.

### 2.2 Four requested exponents

Since

\[
 M_m^2=9\,4^{m-1},
\]

the Gaussian annular weight has exponent

\[
 -\frac1{32}\frac1{9}=-\frac1{288}.
\tag{2.3}
\]

Starting from the theorem's pointwise leakage coefficient \(-1/528\), exact
rational multiplication gives

\[
 2\left(-\frac1{528}\right)=-\frac1{264},
 \qquad
 3\left(-\frac1{528}\right)=-\frac1{176}.
\tag{2.4}
\]

The target-to-quadratic-leakage exponential gap is

\[
 -\frac1{288}-\left(-\frac1{264}\right)
 =\frac1{264}-\frac1{288}
 =\frac1{3168}>0.
\tag{2.5}
\]

These values agree exactly with the certificate JSON:

| Quantity | Independent result | Certificate result | Verdict |
|---|---:|---:|---|
| `gamma` exponent | \(-1/288\) | \(-1/288\) | PASS |
| quadratic leakage exponent | \(-1/264\) | \(-1/264\) | PASS |
| cubic leakage exponent | \(-1/176\) | \(-1/176\) | PASS |
| strict leakage gap | \(1/3168\) | \(1/3168\) | PASS |

This calculation certifies only exponent arithmetic conditional on the
frozen theorem rows.  In particular, it does not certify the pointwise
\(-1/528\) analytic bound.

---

## 3. Three ratio signatures

The independent calculation used the convention

\[
 [a,r,m,e]\equiv A^aR^rM^m e^{eM^2}.
\tag{3.1}
\]

The target and the three \((P_R^A)^{2/3}\) rows are

\[
 T=[2,2,1,-1/288],
\tag{3.2}
\]

\[
 B=[0,-2,0,0],\qquad
 L=[2,2,0,-1/264],\qquad
 S=[2,8/3,-4/3,0].
\tag{3.3}
\]

Polynomial powers of \(\Pi_m\) are tracked separately.

### 3.1 Background row

Before substitution,

\[
 T-B=[2,4,1,-1/288].
\]

Substituting
\(A=R^{-2}e^{M^2/576}\) cancels the \(R^4\) and exponential
coefficient exactly.  Substituting \(R=e^{-M^2/96}\) then changes nothing:

\[
 \boxed{[0,0,1,0]}.
\tag{3.4}
\]

### 3.2 Leakage row

Direct division gives

\[
 T-L
 =[0,0,1,-1/288+1/264]
 =\boxed{[0,0,1,1/3168]}.
\tag{3.5}
\]

The theorem's polynomial overpayment contributes the separate denominator
\(\Pi_m=(1+M_m)^{18}\).  The independent audit also checked that raising
degree 18 to the \(2/3\) power gives degree 12, so retaining degree 18 is an
algebraically valid overpayment.  This says nothing about the analytic
validity of the bound that produced the row.

### 3.3 Transport row

Before the \(R\) substitution,

\[
 T-S=\boxed{[0,-2/3,7/3,-1/288]}.
\tag{3.6}
\]

Because \(R=e^{-M^2/96}\), the factor \(R^{-2/3}\) contributes
\(+1/144\) to the exponential coefficient.  Therefore

\[
 -\frac1{288}+\frac1{144}=\frac1{288},
\]

and the final signature is

\[
 \boxed{[0,0,7/3,1/288]}.
\tag{3.7}
\]

| Ratio | Independent final signature | JSON signature | Verdict |
|---|---|---|---|
| background | `[0,0,1,0]` | `[0,0,1,0]` | PASS |
| leakage, excluding \(\Pi_m^{-1}\) | `[0,0,1,1/3168]` | `[0,0,1,1/3168]` | PASS |
| transport | `[0,0,7/3,1/288]` | `[0,0,7/3,1/288]` | PASS |

**Ratio-signature verdict:** `PASS_FINITE_ONLY`.  Positive powers and
exponential coefficients are finite algebraic signatures; this audit does
not certify any limit as \(m\to\infty\).

---

## 4. The finite \(m=6\) admissibility witness

At \(m=6\),

\[
 M_6=3\cdot2^5=96\ge64.
\tag{4.1}
\]

Since \(R_6=e^{-96}\) and the positive exponential series gives

\[
 e^{96}\ge1+96+\frac{96^2}{2}=4705,
\]

one has

\[
 R_6\le\frac1{4705}<\frac1{16}<\frac\pi{16},
\tag{4.2}
\]

where the last comparison uses only \(\pi>1\).  Also

\[
 q_6=M_6R_6\le\frac{96}{4705}<\frac1{32},
\tag{4.3}
\]

because \(32\cdot96=3072<4705\).

For one doubling step, \(M_{m+1}=2M_m\), so at the base index

\[
 \frac{R_{m+1}}{R_m}=e^{-M_m^2/32}\le e^{-288}\le\frac1{289},
\tag{4.4}
\]

using \(e^{288}\ge1+288=289\).  Consequently

\[
 \frac{q_{m+1}}{q_m}\le\frac2{289}<1.
\tag{4.5}
\]

The independent values

```text
M=96, exp lower bound=4705, R<=1/4705, q<=96/4705,
R step<=1/289, q step<=2/289
```

agree exactly with the JSON.

**Admissibility verdict:** `PASS_FOR_THE_EXPLICIT_FINITE_WITNESS`.  The
unspecified chart constant \(R_1\), passage to all sufficiently large indices,
and every limiting statement remain outside this certificate.

---

## 5. Independent structure and coverage audit

The JSON tree was traversed by a separate recursive flattener.  No producer
helper was imported.

The results were:

| Structural property | Independent result | Verdict |
|---|---:|---|
| runtime checks | 111 | PASS |
| distinct check IDs | 111 | PASS |
| checks with `pass=true` | 111 | PASS |
| independently flattened `subject` leaves | 109 | PASS |
| coverage mapping entries | 109 | PASS |
| distinct mapped IDs | 109 | PASS |
| coverage keys equal the independent leaf paths | true | PASS |
| mapped IDs equal all non-meta check IDs | true | PASS |
| each mapped row's `name` and `actual` equal its leaf | true | PASS |
| summary equals `111/111` | true | PASS |

The two check IDs not assigned to subject leaves are exactly the two meta
checks `MT01` and `MT02`.  Thus “111 unique IDs” and “109-leaf bijection” are
not merely copied from the producer report; they were reconstructed from the
serialized JSON.

### Literal self-equality test

Two independent tests were used:

1. none of the 111 serialized checks declares derivation class
   `LITERAL_SELF_EQUALITY`; and
2. an AST walk of the producer found 86 static `add(...)`/`check_row(...)`
   call sites and found zero sites where the actual and expected arguments
   have identical ASTs.

Loops account for the difference between 86 static call sites and 111 runtime
checks.  Under this explicit syntactic definition, the count of literal
self-equality checks is

\[
 \boxed{0}.
\]

This is a syntactic and coverage property.  It does not prove that every
expected constant is conceptually independent of the proof author's choices.
In particular, the producer's theorem parsing is deliberately a frozen-marker
presence check, not a general LaTeX semantic parser.

**Structure verdict:** `PASS`.

---

## 6. Check-only determinism and read-only behavior

The following supplementary experiment was run twice:

```text
python3 scripts/r074d_zero_mean_transport_certificate.py --check-only
```

Both runs returned status 0 with identical stdout and stderr.  Before and
after the two runs, SHA-256, byte size, and nanosecond modification time were
recorded for the theorem source, manifest, producer, JSON, and report.  All
records were unchanged, and `git status --porcelain=v1` was unchanged.

Two separate `--print-json` runs were byte-identical to each other and to the
tracked JSON.  Two separate `--print-report` runs were likewise byte-identical
to each other and to the tracked report.

The source-code path supports the empirical result: `--check-only` returns
from `check_only(...)` before the only two `write_bytes(...)` calls in the
default generation branch.

**Determinism verdict:** `PASS_CHECK_ONLY_TWO_RUN_AND_CODE_PATH`.  This is a
deterministic finite-code observation for the audited environment and frozen
bytes; it is not a general reproducible-build theorem across arbitrary Python
implementations or altered repositories.

---

## 7. Findings and caveats

### Material discrepancies

None found within the finite certificate's declared scope.

### Required caveats

1. **Frozen-marker parsing is narrow.**  The producer recognizes exact source
   strings and then performs hard-coded exact algebra.  This is appropriate for
   a frozen finite certificate but is not a semantic proof parser.
2. **The analytic rows are inputs.**  The audit confirms arithmetic following
   the target, leakage, transport, and pressure-payment rows.  It does not
   derive those rows from the Navier--Stokes equations.
3. **The manifest relies on Git for its outer seal.**  It binds source and
   producer hashes but does not self-hash; commit `1a8568fb...` supplies the
   independently checked outer byte envelope.
4. **Finite positivity is not asymptotics.**  A positive rational exponent
   signature and the \(m=6\) witness do not themselves prove divergence or an
   infinite quantified statement.
5. **Syntactic non-self-equality is not logical independence.**  The zero count
   rules out literal identical actual/expected expressions under the stated AST
   test; it does not establish independent authorship of all constants.

These caveats do not invalidate the certificate.  They fix what its `PASS`
status means.

---

## 8. Explicit non-certification boundary

This independent audit **does not certify**:

- the stochastic or Feynman--Kac representation, including generator time
  ordering;
- target survival or the one-sided Gaussian leakage argument;
- periodic heat-kernel estimates, heat-kernel constants, or differentiated
  heat-kernel bounds;
- spatial-gradient estimates;
- \(L^2/L^3\) contraction, effective-weight integrals, or periodic-copy sums;
- Calderon--Zygmund, Jensen, harmonic-pressure, or pressure-gauge estimates;
- the exact NSE construction or zero-global-mean claim as analytic facts;
- any passage from the finite signatures to \(m\to\infty\);
- the supremum theorem or any other infinite quantifier; or
- any claim concerning the Clay Millennium Prize problem.

The correct conclusion is therefore:

> The frozen R0.74D finite certificate is byte-bound, structurally bijective,
> free of literal self-equality under the stated independent AST test,
> check-only deterministic in the audited environment, and correct on the
> independently recomputed rational arithmetic and monomial signatures.  It is
> not an analytic certificate for the stochastic, heat-kernel, pressure, or
> limiting parts of R0.74D.
