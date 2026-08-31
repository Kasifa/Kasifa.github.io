# R0.73T exact no-go witness certificate

This package reconstructs, with exact rational arithmetic, the finite
Fourier witnesses used to audit dynamic scalar autocorrelation in R0.73T.
It uses normalized Haar probability measure on
\(\mathbb T^3=[0,2\pi]^3\) and the Fourier convention

\[
 \widehat f(k)=\int_{\mathbb T^3}f(x)e^{-ik\cdot x}\,d\mu(x).
\]

The producer imports only the Python standard library.  Every mathematical
pass/fail decision uses `fractions.Fraction`; there is no floating-point
tolerance, SymPy, network request, GPU, or DGX computation.

## Package files

- `compute_exact_certificate.py` independently builds every coefficient and
  identity, checks the fixed expectations, writes `results.json`, and exits
  nonzero on any failure;
- `audit-checklist.json` is the fixed 55-item expectation set.  It includes
  the complete six-mode velocity, pressure, and autocorrelation tables, not
  only aggregate totals;
- `requirements.txt` fixes the Python-only, standard-library-only runtime
  boundary;
- `seal_package.py` creates or checks the fail-closed two-stage provenance
  seal;
- `results.json` is the canonical machine-readable output, including every
  expected/actual comparison plus SHA-256 bindings to the producer and
  checklist;
- `command.txt` records the pre-seal and final-seal command sequence;
- `manifest.json` and `SHA256SUMS` bind the pre-seal or final-seal package.

The checklist parser rejects duplicate JSON keys.  `--check-only` recomputes
the entire object and requires the committed/generated `results.json` text
to be byte-identical to the canonical rendering.

## Six-mode pressure witness

The certified field is

\[
 u(x_1,x_2)=
 \bigl(6\sin x_2-4\sin(x_1+x_2),
       4\sin x_1+4\sin(x_1+x_2),0\bigr).
\]

The script constructs its six complex Fourier coefficients, checks
conjugate reality, zero mean, and \(k\cdot\widehat u(k)=0\), and independently
reconstructs \(C=\widehat{|u|^2}\) in two ways: shifted autocorrelation and
ordinary product convolution.  It then uses

\[
 \widehat p(n)=-{n_i n_j\over|n|^2}
   \sum_k\widehat u_i(k)\widehat u_j(n-k),\qquad n\ne0,
\]

to obtain all twelve nonzero pressure coefficients.  Exact convolution
certifies

\[
 \mathcal E=42,\quad Q=2918,\quad A=164,\quad D_C=15,
\]

\[
 X^2=4296,\quad Y=1986,\quad
 J=\int|u|^2u\cdot\nabla p=96,
 \quad \mathcal N_4=-4J=-384.
\]

For \(u_L(x)=u(Lx)\), the six velocity sites remain in
\(L\le|k|\le\sqrt2L\), while

\[
 Q'(u_L)=-16536\nu L^2-384L,\qquad
 Q'(-u_L)=-16536\nu L^2+384L.
\]

Thus the exactly certified signed difference is \(-768L\).

## Heat-weighted grouping

The producer groups terms by \(m=|h|^2\), rather than evaluating an
approximate exponential.  With

\[
 Q_\tau=\sum_h e^{-2\tau|h|^2}|C_h|^2,\qquad
 A_\tau=\sum_h e^{-\tau|h|^2}|C_h|,
\]

the exact coefficient maps are

```text
Q_tau: m=0:1764, 1:416, 4:194, 5:416, 8:128
A_tau: m=0:42,   1:40,  4:26,  5:40,  8:16
```

The difference between the instantaneous weighted derivatives for \(u\)
and \(-u\) has one nonzero group only:

\[
 Q_\tau'(u)-Q_\tau'(-u)=-768e^{-8\tau}.
\]

After dilation it is \(-768L e^{-8\tau L^2}\).

## Shear and rotating-shear witnesses

The ordinary shear

\[
 s_L=(0,\sin(Lx_1),0)
\]

is checked from its two Fourier sites.  Advection and pressure vanish, and

\[
 \mathcal E={1\over2},\quad Q={3\over8},\quad A=1,
 \quad D_C=3,\quad
 Q'(0)=-{3\over2}\nu L^2.
\]

The two-component rotating shear

\[
 v_N=(0,\cos(Nx_1),\sin(Nx_1))
\]

also has zero advection and pressure.  Its pointwise magnitude is one, so
its complete scalar autocorrelation is the single coefficient \(C_0=1\)
for every \(N\), whereas

\[
 \dot C_0(0)=-2\nu N^2,\qquad Q'(0)=-4\nu N^2.
\]

This is the exact carrier-scale loss witness for an autonomous unweighted
\(C\)-evolution.

## Reproduction

From the repository root, run:

```bash
R073T_CERT_PYTHON="${R073T_CERT_PYTHON:-python3}"
"$R073T_CERT_PYTHON" -B research/certificates/r073t/compute_exact_certificate.py
"$R073T_CERT_PYTHON" -B research/certificates/r073t/compute_exact_certificate.py --check-only
"$R073T_CERT_PYTHON" -B research/certificates/r073t/seal_package.py
"$R073T_CERT_PYTHON" -B research/certificates/r073t/seal_package.py --check-only
```

The expected terminal lines are:

```text
R073T_EXACT_CERTIFICATE=PASS mode=write checks=55/55 ...
R073T_EXACT_CERTIFICATE=PASS mode=check-only checks=55/55
```

The first seal is intentionally marked
`status=hash-bound-uncommitted`, `finalSeal=false`.  After all six source
files listed in `manifest.json` have been committed, create the final seal
with the explicit immutable commit:

```bash
R073T_SOURCE_COMMIT=<full-lowercase-40-hex-commit>
"$R073T_CERT_PYTHON" -B research/certificates/r073t/seal_package.py \
  --source-commit "$R073T_SOURCE_COMMIT"
"$R073T_CERT_PYTHON" -B research/certificates/r073t/seal_package.py \
  --source-commit "$R073T_SOURCE_COMMIT" --check-only
```

The final stage uses `git cat-file blob` for every source and refuses to
seal if any committed byte differs from the working-tree source.  A missing,
abbreviated, uppercase, non-commit, or stale source commit also fails closed.

Any arithmetic identity, fixed expectation, duplicate checklist key,
missing output, or byte mismatch raises an error and returns a nonzero exit
status.

## Claim boundary

This package certifies finite Fourier algebra and exact instantaneous
formulas only.  It does not integrate a generic Navier--Stokes solution,
prove control of \(A(t)\), establish singularity or global regularity, or
resolve any part of the Clay problem.  Both shear witnesses are explicitly
smooth, globally regular solution classes; the six-mode field is used only
for scaling and information-loss auditing.
