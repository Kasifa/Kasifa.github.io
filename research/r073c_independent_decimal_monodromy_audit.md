# R0.73C independent Decimal monodromy audit

**Date:** 2026-08-30  
**Status:** independent interval endpoint validation passed  
**Scope:** frozen Rayleigh C4 bracket at \(\gamma=1/2\)

## 1. Independent implementation

The validator is
`experiments/r073c/independent_decimal_monodromy_validator.py`.
Its formal-run source SHA-256 is

```text
21aa4fd02f23a4003fa11cd27333beb22acb0bea1a76f9e62f02c4a667f65f89
```

It does not import `research/r073c_interval_monodromy.py`, `mpmath`, NumPy, or
SciPy.  It uses only the Python standard library.  The formal runtime gate
requires CPython 3.12, `decimal` 1.70, and libmpdec 4.0.0.  Every interval
primitive calls an explicit `decimal.Context`: lower endpoints use
`ROUND_FLOOR`, and upper endpoints use `ROUND_CEILING`.  The code separately
implements addition, subtraction, four-corner multiplication and division,
cross-zero squaring, integer powers, containment, and finite-endpoint checks.
It traps division by zero, invalid operations, overflow, underflow, subnormal
results, clamping, and float conversion.  The formal run also checked that
these critical Decimal flags stayed clear and that the source hash did not
change during execution.

## 2. Independent enclosure of pi

No transcendental library value is used.  The validator starts from Machin's
identity

\[
 \pi=16\arctan(1/5)-4\arctan(1/239)
\]

and the alternating expansion

\[
 \arctan x=\sum_{k\ge0}\frac{(-1)^k x^{2k+1}}{2k+1}.
\]

For a partial sum \(S_n\) and next positive term \(t_{n+1}\), it uses

\[
 n\ {\rm even}:\quad \arctan x\in[S_n-t_{n+1},S_n],
\qquad
 n\ {\rm odd}:\quad \arctan x\in[S_n,S_n+t_{n+1}].
\]

All partial sums and term recurrences are themselves Decimal intervals.  At
80 digits the \(1/5\) and \(1/239\) series used 45 and 13 terms.  The resulting
formal enclosure was

\[
\begin{aligned}
3.1415926535897932384626433832795028841971693993751058209749445922971829243601248
&<\pi\\
&<3.1415926535897932384626433832795028841971693993751058209749445923497088821653085.
\end{aligned}
\]

## 3. ODE enclosure

The code independently reconstructs the twelve-dimensional real autonomous
system containing

- \(\sin x,\cos x,\sin2x,\cos2x\);
- the real and imaginary parts of both fundamental columns for
  \(\phi''=(1/4+W''/(W-i\eta))\phi\).

On each step it verifies

\[
 X+[0,h][F](Z)\subseteq Z.
\]

This covers the entire step: the Picard operator is a continuous compact
self-map of \(C([0,h],Z)\), while \(\eta>0\) makes the vector field locally
Lipschitz and hence the enclosed solution unique.  The endpoint map retains
Taylor orders \(0,\ldots,p-1\) and uses the normalized order-\(p\) derivative
evaluated on the whole Picard box as the interval Lagrange remainder
\(h^p z^{[p]}(\xi)\).  The formal run used 256 steps, order 8, and 80 Decimal
digits.  Every step closed on the first Picard candidate (`maximumAttempt=0`).

## 4. Certified result

The source-locked output is
`experiments/r073c/decimal_interval_validation.json`, with SHA-256

```text
67faa0f2e8fbe3c1855f3c94ce92ca62b78a76108f9d035778caa244ab18f7de
```

It gives

\[
\begin{aligned}
F(0.3407)&=\operatorname{tr}M(0.3407)-2\\
&\in[-0.0038632492476754313571663187732664393249918501206589353586891548642146393782094,\\
&\hspace{2.8em}-0.0038452150453167480685822914588690432989915951367260354180430740946475303663556],\\[3pt]
F(0.3410)&=\operatorname{tr}M(0.3410)-2\\
&\in[0.0061053390515351415118049373183154984156646518079599918449181850805315138583172,\\
&\hspace{2.8em}0.0061232335046737390951989053422427640125437830754614006206992449276273498766969].
\end{aligned}
\]

Both trace-imaginary intervals contain zero, both monodromy determinant
intervals contain \(1+0i\), and all endpoints are finite.  The two much
narrower primary `mpmath.iv` enclosures lie inside these independent Decimal
enclosures.  The same formal command was run twice and the two JSON files were
byte-identical; elapsed times remain only in the NDJSON progress logs.  The
reproduction command in `experiments/r073c/command.txt` now
uses the actual validator filename and its `--eta-low/--eta-high` interface.

Together with the exact real-trace, determinant-one, periodicity, and
Rayleigh-sign lemmas, the strict endpoint signs imply

\[
 \exists\,\eta_*\in(0.3407,0.3410),\qquad
 \sigma_*=\frac{\eta_*}{2}\in(0.17035,0.17050),
 \qquad
 \sigma_*\in\sigma_p(A_{1/2}(0)).
\]

## 5. Boundary

This independent certificate proves existence of at least one positive real
frozen eigenvalue.  It does not prove uniqueness of the root, algebraic
simplicity, a quantitative Riesz projection bound, viscous persistence,
nonautonomous fast-time transfer, a nonlinear Navier--Stokes estimate, or the
Clay problem.
