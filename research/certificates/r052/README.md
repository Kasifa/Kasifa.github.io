# R0.52 exact certificate

This directory archives the formal exact-rational audit of the complete
two-parameter affine charge-weight family

\[
\omega_s(c,\lambda)=c^s(1+\lambda|s|),
\qquad c>0,\quad\lambda\ge0,
\]

for the exact degree-80 center of the reduced canonical edge generating
system.

## Certified statement

Let \(R_{\mathrm{aff}}\) be the globally optimized threshold radius within
this affine family.  The certificate proves

\[
\frac{3826244718485988314760952288871012330925}{10^{40}}
<R_{\mathrm{aff}}<
\frac{3826244718485988314760952288871012330926}{10^{40}}.
\]

The interval width is exactly `1e-40`.

The compactification

\[
\alpha=\frac{\lambda}{1+162\lambda},\qquad
\delta=1-162\alpha
\]

turns the active column into a linear function of \(\alpha\).  The exact
three-equation active/zero stationary system has one and only one root in the
pinned rational `(r,c,alpha)` box.  An exact Krawczyk image lies strictly
inside that box.  Positive KKT multipliers, LICQ, and a positive constrained
Hessian curvature certify a strict local maximum.

Every inactive sector is strictly below one on the root box.  The audit
covers 239 fixed positive charges, the all-degree `s=1` and `s=-1` sectors,
and both infinite large-charge parity branches.  There are 242 inactive
records after removing the two active equalities `(j,s)=(81,162)` and `s=0`.
The nearest inactive sector is `(j,s)=(82,164)`, with a uniform gap below one
greater than `0.00014527650997576197022`.

For the global upper bound, eliminating \(\alpha\) gives the necessary
feasibility condition

\[
E=(-M_1)(1-U_0)
-(M_0-1)\{U_1+162(1-U_0)\}\ge0.
\]

At the rational upper radius, `c^2 E` is a degree-316 polynomial.  Its
log-character derivative has three coefficient sign variations and three
disjoint exact sign-changing positive-root boxes.  Descartes' rule therefore
proves that these are exactly its three positive roots.  On the only relevant
local-maximum box, all 317 exact Bernstein coefficients of `c^2 E` are
negative; the largest is approximately `-6.8068e-39`.  Exact endpoint and
monotonic boundary signs then prove `E<0` for every `c>0`, excluding every
`lambda>=0` at the upper radius.  Radius monotonicity excludes every larger
radius.

Relative to the R0.51 fixed rational-weight upper root, the conservative
radius gain factor is greater than `1.0000000000067320092`.  The gain is very
small; the substantive result is the complete parameter-domain bound rather
than the decimal increase.

The width-`1e-40` enclosure does not by itself prove that the local KKT root
is the unique global maximizer as an exact real number.  The theorem does not
optimize over every Banach norm, provide a critical-space bridge for arbitrary
three-dimensional divergence-free fields, or prove or disprove
three-dimensional Navier--Stokes regularity.

## Files

- `edge-affine-family-global.json`: machine-readable GMP certificate;
- `progress.ndjson`: append-only scientific stage log;
- `resources.csv`: two-second process-tree resource samples;
- `SHA256SUMS`: hashes for every archived file except itself.

## Pinned inputs and proof digests

- source commit: `e64ed23dcd86883e9690468b05f64304ee4ac816`;
- formal audit source SHA-256:
  `c0fdcb71fb063fae92bc2774612a7b3191c5e4d29cfc6d8c80a946fdeb7c5389`;
- mathematical note SHA-256:
  `5a07c8f231040339794dd58f3cb5a1b861ea807f0a8147ff7471c371ae6c2343`;
- R0.51 input certificate SHA-256:
  `db72d40ee304d1a6ce5dd96d9f5971e78037675e79c837e409c5691bb8aa582f`;
- degree-80 polynomial SHA-256:
  `056a0adba7f3cba41a6e9bd6d943a8f59be28f50f44c6035df1f68393ed26be7`;
- eliminated feasibility polynomial SHA-256:
  `e451134c4d2d10d70af0744ae6fea9262cb38b0c59ceadacb9e628a529aec8a0`;
- eliminated log-derivative polynomial SHA-256:
  `47bbdf22bbfdeedaaf7fabcf6ff96e516c873629166308b9d1c13167eb624db7`;
- signed local-maximum Bernstein coefficients SHA-256:
  `2d04714d073d4887c070eaa934ba128347cedbe462b4f229209ceb4e24b22640`.

## Exact reproduction command

```sh
PYTHONPATH=research tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r052/resources.csv \
  --interval 2 -- \
  tmp/r024-venv/bin/python \
  research/edge_affine_family_kkt_audit.py \
  --max-total-degree 80 \
  --charge-cutoff 241 \
  --radius-lower \
  3826244718485988314760952288871012330925/10000000000000000000000000000000000000000 \
  --radius-upper \
  3826244718485988314760952288871012330926/10000000000000000000000000000000000000000 \
  --character-lower \
  7975595104326214175951774729017091063394/10000000000000000000000000000000000000000 \
  --character-upper \
  7975595104326214175951774729017091063395/10000000000000000000000000000000000000000 \
  --alpha-lower \
  61234500552300731923346973685049743915/10000000000000000000000000000000000000000 \
  --alpha-upper \
  61234500552300731923346973685049743916/10000000000000000000000000000000000000000 \
  --localization-digits 100 \
  --source-commit e64ed23dcd86883e9690468b05f64304ee4ac816 \
  --progress \
  --progress-log research/certificates/r052/progress.ndjson \
  --check --pretty \
  --output research/certificates/r052/edge-affine-family-global.json
```

## Successful-run summary

- 22/22 exact checks passed;
- inactive sector records: 242;
- finite exact center terms: 2,161;
- recurrence ordered interactions: 1,113,168;
- scientific wall time: 242.306795 seconds;
- monitored wall time: 242.421306 seconds;
- resource samples: 121;
- maximum observed CPU: 100.0%;
- maximum observed resident memory: 148.156 MiB;
- GPU: not used;
- randomness: none;
- diagnostic localization: `mpmath` at 100 decimal digits;
- sign arithmetic: `gmpy2.mpq` over GMP 6.3.0, with no floating-point
  decision.

Environment:

- macOS 26.6.1 arm64;
- Apple M5 Max, 36 GiB memory;
- Python 3.12.13;
- gmpy2 2.3.1;
- GMP 6.3.0.
