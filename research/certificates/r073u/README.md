# R0.73U exact tensor-heat parity certificate

This package reconstructs the four-site finite Fourier witness used in
R0.73U to audit the full quadratic tensor heat hierarchy.  It uses normalized
Haar probability measure on \(\mathbb T^3=[0,2\pi]^3\) and the convention

\[
 \widehat f(k)=\int_{\mathbb T^3}f(x)e^{-ik\cdot x}\,d\mu(x).
\]

The producer imports only the Python standard library.  Every mathematical
pass/fail decision uses `fractions.Fraction` with an exact ordered-pair model
for Gaussian rationals.  There is no floating-point tolerance, SymPy, network
request, GPU, DGX, or simulation.  Ordinary translation is outside this
certificate and follows the project rule `LOCAL_DIRECT_NO_DGX`.

## Fixed analytic source

The manifest's top-level `sourceCommit` and `analyticSourceCommit` are both
fixed to

```text
84e808dae473f6381cbf9df55a71f5fe81a1cfce
```

and mean the immutable commit containing the four analytic source files:

- `research/r073u_problem_freeze.md`;
- `research/r073u_tensor_heat_hierarchy.md`;
- `research/r073u_independent_analytic_audit.md`;
- `research/r073u_primary_literature_audit.md`.

The seal reads all four blobs with `git cat-file`, records their Git object
IDs and SHA-256 digests, and requires the working copies to be byte-identical.
The obsolete pre-amendment hash
`72493751370aa948947000df169e21199fc5c95d` is rejected explicitly.

Certificate sources follow a separate immutable-source lifecycle.  The
pre-seal hash-binds the six source files and leaves
`certificateSourceCommit=null`.  After those six files are committed, the
final seal requires the explicit full commit and verifies every committed
blob against the working copy.

## Certified field and coefficient contract

The real mean-zero divergence-free field is

\[
 u(x,y,z)=\bigl(2\sin(x+y),\,2\sin x-2\sin(x+y),\,0\bigr),
\]

with positive Fourier sites

\[
 \widehat u(1,0,0)=(0,-i,0),\qquad
 \widehat u(1,1,0)=(-i,i,0),
\]

and conjugate coefficients at the two negative sites.  At
\(h=(1,2,0)\), the fixed notation is

\[
 T_{ij}=\widehat{u_i u_j},\qquad
 F_{\ell ij}=\widehat{u_\ell u_i u_j},
\]

\[
 A_{ij}=-ih_\ell F_{\ell ij},\qquad
 B_{ij}=-\widehat{u_j\partial_i p+u_i\partial_jp},\qquad
 K=A+B,
\]

\[
 V_{ij}=\widehat{\Delta T_{ij}
 -2\partial_\ell u_i\partial_\ell u_j},\qquad
 \partial_t\widehat T=\nu V+K.
\]

Exact convolution gives

\[
 \widehat T(h)=V(h)=0,
\]

\[
 F_1(h)=
 \begin{pmatrix}0&-i&0\\-i&2i&0\\0&0&0\end{pmatrix},\qquad
 F_2(h)=
 \begin{pmatrix}-i&2i&0\\2i&-3i&0\\0&0&0\end{pmatrix},
 \qquad F_3(h)=0,
\]

\[
 A(h)=\begin{pmatrix}-2&3&0\\3&-4&0\\0&0&0\end{pmatrix},
 \quad
 B(h)=\begin{pmatrix}0&-2&0\\-2&4&0\\0&0&0\end{pmatrix},
\]

\[
 K(h)=\begin{pmatrix}-2&1&0\\1&0&0\\0&0&0\end{pmatrix},
 \qquad |K(h)|_F^2=6.
\]

The complete nonzero pressure table, with \(\widehat p(0)=0\), is

```text
h=(-2,-1,0): 2/5      h=(0,-1,0): 2
h=( 0, 1,0): 2        h=(2, 1,0): 2/5
```

## Two independent exact paths

The producer compares complete coefficient maps, not only the target entry.

1. The product-law path builds \(T\), \(F\), \(A\), \(B\), the gradient
   product, and \(V\) by direct sparse convolution.
2. The velocity-law path independently reconstructs pressure from ordered
   velocity pairs, computes
   \(- (u\cdot\nabla)u-\nabla p\) and \(\Delta u\), and then applies the
   exact product rule to \(u\otimes u\).

The full pressure, nonlinear tensor-tangent, and viscous tensor-tangent maps
must agree byte-for-byte as exact rational objects.  The sign-reversed field
is recomputed in full: \(T,p,V\) are even, while \(F,A,B,K\) are odd.

## Heat groups and dilation

For the complete base nonlinear tensor tangent, define

\[
 S_m=\sum_{|h|^2=m}|K(h)|_F^2.
\]

The exact groups are

```text
m:    1       2       5      10      13
S_m: 176/25  276/25  12     36/25   76/25
```

The sign-pair difference is \(2K\), so its squared groups are exactly
\(4S_m\):

```text
m:       1        2       5      10       13
4*S_m: 704/25  1104/25   48     144/25  304/25
```

At the target mode, heat filtering yields

\[
 \partial_t\widehat\Theta_s(h;u)
 -\partial_t\widehat\Theta_s(h;-u)
 =2e^{-5s}K(h),
\]

whose Frobenius norm is \(2\sqrt6e^{-5s}\).  For
\(u_L(x)=u(Lx)\) and \(h_L=(L,2L,0)\), this becomes

\[
 2Le^{-5sL^2}K(h),\qquad
 2\sqrt6Le^{-5sL^2}
\]

at the coefficient and Frobenius levels.  On the parabolic slice
\(s=\theta L^{-2}\),

\[
 2\sqrt6Le^{-5\theta}
 =2\sqrt{6\theta}e^{-5\theta}s^{-1/2}.
\]

The normalized profile is maximal at \(\theta=1/10\).  This is a
coefficient-level one-derivative cost for this witness, not a failure theorem
for every time-integrated estimate or signed augmentation.

## Minimality boundary

A nonzero real mean-zero field supported on one conjugate pair
\(\{+k,-k\}\) is a shear: incompressibility gives
\(k\cdot a=k\cdot\overline a=0\), so every multiplier in
\((u\cdot\nabla)u\) vanishes.  Its nonlinear pressure and tensor tangent are
zero.  Therefore this parity mechanism needs at least two conjugate pairs,
or four Fourier sites, and the displayed field attains that support bound.
This is not a minimality statement over all closures or all possible no-go
arguments.

## Package files

- `compute_exact_certificate.py` implements both exact paths, evaluates the
  fixed 75-item checklist, writes `results.json`, and fails closed;
- `audit-checklist.json` fixes all coefficient, pressure, path-agreement,
  parity, heat-group, dilation, and minimality expectations;
- `results.json` records every expected/actual comparison and the producer
  and checklist hashes;
- `seal_package.py` binds the frozen analytic commit, the certificate files,
  and the two-stage certificate-source lifecycle;
- `command.txt` records the exact reproduction and final-seal commands;
- `requirements.txt` fixes the standard-library-only runtime boundary;
- `manifest.json` and `SHA256SUMS` are generated provenance outputs.

Both JSON readers reject duplicate keys.  Both `--check-only` modes
reconstruct their canonical objects and require byte-identical committed or
generated output.

## Reproduction

From the repository root, run:

```bash
R073U_CERT_PYTHON="${R073U_CERT_PYTHON:-python3}"
"$R073U_CERT_PYTHON" -B research/certificates/r073u/compute_exact_certificate.py
"$R073U_CERT_PYTHON" -B research/certificates/r073u/compute_exact_certificate.py --check-only
"$R073U_CERT_PYTHON" -B research/certificates/r073u/seal_package.py
"$R073U_CERT_PYTHON" -B research/certificates/r073u/seal_package.py --check-only
```

The expected certificate line is

```text
R073U_EXACT_CERTIFICATE=PASS ... checks=75/75
```

The pre-seal status is
`analytic-source-bound-certificate-hash-bound`.  After the six certificate
source files have been committed, create the final seal with

```bash
R073U_CERTIFICATE_SOURCE_COMMIT=<full-lowercase-40-hex-commit>
"$R073U_CERT_PYTHON" -B research/certificates/r073u/seal_package.py \
  --certificate-source-commit "$R073U_CERTIFICATE_SOURCE_COMMIT"
"$R073U_CERT_PYTHON" -B research/certificates/r073u/seal_package.py \
  --certificate-source-commit "$R073U_CERTIFICATE_SOURCE_COMMIT" --check-only
```

## Claim boundary

This package certifies exact finite Fourier algebra, parity, and
coefficient-level heat/dilation formulas.  It does not integrate a generic
Navier--Stokes solution, exhibit singular or near-singular behavior, prove
failure of all closures, establish global regularity, or resolve any part of
the Clay problem.  The witness is planar, smooth, and used only to audit the
information content of an even quadratic tensor state.
