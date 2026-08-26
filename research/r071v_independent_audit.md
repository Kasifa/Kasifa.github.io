# R0.71V independent audit

**Audit date:** 2026-08-26

## Independence contract

`research/r071v_independent_audit.py` is a standalone binary64/SciPy
reconstruction. It does not import `research/r071v_exact_audit.py` and does
not read `research/certificates/r071v/result.json`. The two programs share
only the mathematical specification written in
`research/r071v_report-source.md`.

The independent program rebuilds:

1. the fixed-\(N=3\) response matrix and its prescribed roots;
2. the branch critical points and right-lobe heights;
3. the first- and second-time rows by adaptive quadrature;
4. the weighted one-dimensional area formula on a separate monomial test;
5. the sine zero-level stress test;
6. the \(N=2\), fixed-target high-frequency family for
   \(q=8,16,32,64,128,256\);
7. the internal and terminal excursion noncollapse factors.

No value from the high-precision producer is used as an input.

## Passed checks

The independent response solve has maximum prescribed-root residual
\(2.78\times10^{-17}\) and minimum root slope
\(3.27\times10^{-3}\). The separate area-formula quadratures differ by
\(1.43\times10^{-11}\). The two-row sampling ledger has positive slack.

The fitted quantities use the reduced target-amplitude normalization. Fixed
eigenshell factors are omitted in this checker because they do not change any
\(q\)-power; the formal figure restores them explicitly. Fitting the last
four high-frequency values, \(q=32,64,128,256\), gives:

| Quantity | Predicted power | Fitted power |
|---|---:|---:|
| second root atom | \(-4\) | \(-3.9672\) |
| first-time row | \(-6\) | \(-5.9845\) |
| second-time row | \(-2\) | \(-1.9340\) |
| atom / first-time row | \(+2\) | \(+2.0173\) |
| atom / second-time row | \(-2\) | \(-2.0332\) |
| internal \(D_E\) | \(-2\) | \(-2.0349\) |
| terminal \(D_E\) | \(-4\) | \(-4.0379\) |
| terminal height charge | \(-8\) | \(-8.0051\) |

Every tolerance encoded by the independent program passes. Its machine-
readable output is
`research/certificates/r071v/independent-result.json`.

## Boundary

The audit evaluates finite response sums, branch extrema, and
one-dimensional quadratures. It does not time-step NSE, prove the
Chebyshev-system statement, prove the implicit-function theorem, or supply a
uniform nonlinear remainder estimate. Those parts remain analytic. It also
does not establish a weak zero-jet trace, a continuation criterion, a
finite-time singularity, global regularity, novelty, or priority.
