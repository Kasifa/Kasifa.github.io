# R0.54 complete product-affine family certificate

This directory archives the exact global enclosure for the complete
product-affine charge-weight family

\[
\omega_s=c^s(1+\lambda|s|)(1+\mu|s|),
\qquad c>0,\quad\lambda,\mu\ge0,
\]

for the exact degree-80 center of the reduced canonical edge generating
system.  It also archives the separate deterministic floating-point
reconnaissance used to select the proof geometry.

## Certified statement

The R0.53 exact all-order rational witness supplies the lower bound

\[
r_{\mathrm{prod}}^{\mathrm{opt}}
>0.382628602237879637.
\]

At the simple rational radius

\[
r_U=\frac{382629}{10^6}=0.382629,
\]

the R0.54 audit excludes every `c>0` and every `lambda,mu>=0`.  Hence

\[
0.382628602237879637
<r_{\mathrm{prod}}^{\mathrm{opt}}
<0.382629.
\]

The enclosure width is exactly `3.97762120363e-7`.  Relative to the complete
single-affine-family upper bound from R0.52, the product-family gain is
strictly between the R0.53 lower factor
`1.0000107948905119688` and the R0.54 upper factor
`1.0000118344531892886`.  Even perfect optimization in the complete product
family can improve the R0.53 witness by a factor smaller than
`1.0000010395514554756`.

## Exact parameter reduction

With `S=162`, define

```text
alpha = lambda/(1+S lambda)
beta  = mu/(1+S mu)
A = alpha+beta
B = alpha*beta
h = 1/S
```

The closure of the full slope square maps exactly to

```text
0 <= A <= 2h
max(0,h(A-h)) <= B <= A^2/4.
```

At fixed `(r,c)`, the former active and zero-charge constraints are affine in
`(A,B)`.  Exact Bernstein coefficients prove the zero constraint's `B`
coefficient is negative on `0.1337<=c<=0.803`; the active coefficient is a
strictly positive second charge moment.  Any feasible point must therefore
satisfy three explicit bivariate rational-polynomial inequalities `H<=0`,
`P<=0`, and `Q<=0`.

An adaptive tensor-Bernstein proof covers both closed `A` rectangles.  It has
14 terminal boxes: 9 are excluded by `H>0`, 1 by `P>0`, and 4 by `Q>0`.
The deepest character subdivision is 6 levels and the deepest invariant
subdivision is 5 levels.  Exact dyadic mass identities equal one on both root
rectangles.  This is a continuous parameter proof, not a parameter grid.

The two unbounded character tails are covered by exact log-character
monotonicity.  At `c=0.1337`, the unweighted zero column is above one and has
negative first log derivative; at `c=0.803`, the active zeroth moment is above
one and its first moment is positive.  Their second derivatives are strictly
positive moments.

The result is an all-parameter theorem inside the reduced coefficient model.
It does not identify the exact global maximizing parameters, optimize every
possible Banach norm, construct a scale-critical comparison for arbitrary
three-dimensional Fourier data, or prove or disprove three-dimensional
Navier--Stokes regularity.

## Separate diagnostic localization

The deterministic diagnostic used 64 starts with seed `54054` and a 100-digit
diagonal solve.  Of the 64 SLSQP runs, 56 converged to points meeting the
recorded feasibility tolerance.  Thirty-three landed in the symmetric
product-interior basin and twenty on a single-factor boundary basin.  The
high-precision diagonal candidate is

```text
r = 0.3826289125304728455618153157831342338168766428365...
c = 0.7928055385863995173795158615684136119081963215694...
lambda = mu = 0.3078617122304947851869880311579595464837429106023...
```

Along `alpha=m+d`, `beta=m-d`, the diagnostic implicit derivative is

```text
dr/d(d^2) = -20.22944836546012365510343617294559465575...
```

and the corresponding antisymmetric second derivative is
`-40.4588967309202473102...`.  These floating and high-precision values are
reconnaissance only.  They are not used by the exact global upper proof.

## Files

- `edge-product-affine-family-global.json`: machine-readable GMP global
  certificate;
- `progress.ndjson`: append-only formal proof-stage log;
- `resources.csv`: two-second process-tree samples for the formal run;
- `product-family-diagnostic.json`: 100-digit localization and all 64
  deterministic optimizer records;
- `diagnostic-resources.csv`: one-second process-tree samples for the
  diagnostic run;
- `SHA256SUMS`: hashes for every archived file except itself.

## Pinned inputs and proof digests

- formal exact source commit:
  `543a394c51a9454496638eb1a9324775164b2eaa`;
- diagnostic source commit:
  `4bc84a7bb24e8bd6a9b051208969b344c47b3ed6`;
- exact audit source SHA-256:
  `fd50647c52c51a8cf2faf882d13dd521f3087b40de51c4d8f48ebd850907d6b1`;
- mathematical note SHA-256:
  `2b6be545b95c08ef64c5a6c89d23f6e5e548a0f1b876fa023beea3ebe74d1994`;
- diagnostic source SHA-256:
  `d72672230b1e1e94f7c29eca02069002dc9501dd7fe804f581b6e4b7bb2e0a10`;
- pinned R0.53 certificate SHA-256:
  `5d6486dfcc6f2c016380a29698ed986213701b9441dd007d95acce4fc0ea67a5`;
- degree-80 polynomial SHA-256:
  `056a0adba7f3cba41a6e9bd6d943a8f59be28f50f44c6035df1f68393ed26be7`;
- exact cover leaf-set SHA-256:
  `449345d8d5daf02d549d75bc7c4eafe16b7d59dc8213c6e173df5a87a6253ef9`.

## Exact reproduction command

```sh
PYTHONPATH=research tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r054/resources.csv \
  --interval 2 -- \
  tmp/r024-venv/bin/python \
  research/edge_product_affine_family_global_audit.py \
  --max-total-degree 80 \
  --radius-upper 382629/1000000 \
  --character-lower 1337/10000 \
  --character-upper 803/1000 \
  --max-cover-depth 80 \
  --source-commit 543a394c51a9454496638eb1a9324775164b2eaa \
  --progress \
  --progress-log research/certificates/r054/progress.ndjson \
  --check --pretty \
  --output research/certificates/r054/edge-product-affine-family-global.json
```

Diagnostic reproduction command:

```sh
PYTHONPATH=research tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r054/diagnostic-resources.csv \
  --interval 1 -- \
  tmp/r024-venv/bin/python \
  research/edge_product_affine_family_diagnostic.py \
  --starts 64 \
  --digits 100 \
  --seed 54054 \
  --progress \
  --output research/certificates/r054/product-family-diagnostic.json
```

## Successful-run summary

Formal exact run:

- 16/16 exact checks passed;
- recurrence ordered interactions: 1,113,168;
- exact continuous-cover leaves: 14;
- scientific wall time: 73.502364 seconds;
- monitored wall time: 73.638681 seconds;
- resource samples: 38;
- maximum observed CPU: 100.0%;
- maximum observed resident memory: 303.531 MiB;
- GPU: not used;
- randomness: none;
- sign arithmetic: `gmpy2.mpq` over GMP 6.3.0, with no floating-point
  decision.

Diagnostic run:

- 64 deterministic starts; 56 converged feasible records;
- scientific wall time: 5.933023 seconds;
- monitored wall time: 6.165666 seconds;
- resource samples: 7;
- maximum observed CPU: 100.0%;
- maximum observed resident memory: 78.453 MiB;
- GPU: not used;
- finite decision arithmetic: SciPy/NumPy binary floating point;
- high-precision localization: mpmath at 100 decimal digits.

Environment:

- macOS 26.6.1 arm64;
- Apple M5 Max, 36 GiB memory;
- Python 3.12.13;
- gmpy2 2.3.1;
- GMP 6.3.0;
- mpmath 1.3.0;
- NumPy 2.3.5;
- SciPy 1.16.1.
