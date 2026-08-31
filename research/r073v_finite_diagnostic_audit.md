# R0.73V finite diagnostic audit: pressure-aware third-order interface

**Audit date:** 2026-09-01

**Verdict:** PASS for the declared finite Fourier claims.  The primary and
independent standard-library implementations rebuild the complete nonzero
tables for the four-site \(\kappa,Q,\Xi=2R\) fields, agree byte-for-byte on
their common core, and pass all 66 locked checks.  The final package is bound
to an immutable source commit and has status `sealed`.

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

## 1. Immutable bindings and read-only verification

| Layer | Immutable identifier |
|---|---|
| analytic proof and independent audit | `25636c886f1ee2449418b5548b42f9f0fa269b47` |
| eight certificate source files | `7c445c522a241bdc8b867b6fce0f0fed9b82e97d` |
| generated certificate seal | `b34d91ea96c257b943f11d134e8024138e5f3cb0` |

The final manifest has SHA-256
`8030cc38ee48c2ec397976ddedc6fade1eec9ae14b89f3c01c081ecaabbf8c9e`.
The main bound objects are:

| File | SHA-256 |
|---|---|
| `results.json` | `e024ea767ff146ee2e53455522e6c0ab2c59608e74038673cc8a6fca0271b0c4` |
| `independent-results.json` | `0c40808136b532b536a871184a9937b7a29c436e04ef0235e607964b0ebec1d0` |
| `audit-checklist.json` | `0d03ab0d355afda6d75b87cd9150451600331c080c960f09b1192a34bd02d1bf` |
| `contract.json` | `0a7ea847d21d150e4ab4be341292ddc85f6f38599c1a648ab1c976ab2b361b98` |

I reran the following checks from the repository root:

```text
python3 -B research/certificates/r073v/compute_exact_certificate.py --check-only
python3 -B research/certificates/r073v/independent_recompute.py --check-only
python3 -B research/certificates/r073v/seal_package.py \
  --source-commit 7c445c522a241bdc8b867b6fce0f0fed9b82e97d \
  --check-only
cd research/certificates/r073v && shasum -a 256 -c SHA256SUMS
```

The primary producer returned `checks=66/66`; the independent producer
returned PASS with the same complete-table digest

```text
a7494d44f45b1249a513ac4d44476b7ce5af622b0d59928f4e4631d9715c22f7
```

and the sealer returned `finalSeal=true`, `status=sealed`, and
`twoPathCommonCoreByteIdentical=true`.  All eleven checksum entries returned
`OK`.

## 2. Four-site exact order separation

For

\[
 u=(2\sin(x+y),\;2\sin x-2\sin(x+y),\;0),
 \qquad h_*=(1,2,0),\qquad q=e^{-s},
\]

the exact contracted velocity-cumulant flux is

\[
 -\widehat{\partial_k\kappa_{kij}}(h_*)
 =q^3(1-q^2)^2(q^2+2)
 \begin{pmatrix}2&-3&0\\-3&4&0\\0&0&0\end{pmatrix}.
\]

The pressure--velocity and pressure--strain rows are

\[
 -\widehat{\partial_iQ_j+\partial_jQ_i}(h_*)
 =q^3(1-q^2)
 \begin{pmatrix}4&2&0\\2&-8&0\\0&0&0\end{pmatrix},
\]

\[
 \widehat\Xi(h_*)
 =q^3(1-q^2)
 \begin{pmatrix}-4&0&0\\0&4&0\\0&0&0\end{pmatrix}.
\]

Thus this selected cumulant-flux coefficient is \(O(s^2)\), while the
nondegenerate pressure contribution is \(O(s)\).  The certificate therefore
excludes an \(s\)-uniform coefficientwise absorption of the pressure row by
that cumulant flux; at least an \(s^{-1}\) coefficient cost is required.  It
does not establish equality of two complete \(\kappa_s\) fields or a
whole-field information no-go.

## 3. Compressed pressure-aware lift

With \(N=\mathbb P\nabla\!\cdot(u\otimes u)\),
\(\mathcal C_s=P_s(u\odot N)\), and
\(\chi_s=\mathcal C_s-v_s\odot N_s\), put

\[
 K=\begin{pmatrix}-2&1&0\\1&0&0\\0&0&0\end{pmatrix}.
\]

The exact target coefficients are

\[
 \widehat{\mathcal C_s}(h_*)=-q^5K,
 \qquad
 \widehat{v_s\odot N_s}(h_*)=-q^3K,
 \qquad
 \widehat\chi_s(h_*)=(q^3-q^5)K.
\]

The sign-pair difference is \(2(q^3-q^5)K\).  For the integer dilation
\(u_L(x)=u(Lx)\), at \(s=\theta L^{-2}\), its Frobenius norm is

\[
 2\sqrt6\,L(e^{-3\theta}-e^{-5\theta}).
\]

This \(\chi_s\) is the equation-slot-compressed lift.  It is distinct from
the complete Germano signed stress source and is not asserted to be uniquely
or information-theoretically minimal.

## 4. Six-site coefficientwise pressure witness

For

\[
 u=(6\sin y-4\sin(x+y),\;4\sin x+4\sin(x+y),\;0),
\]

the output-mode-zero contractions of the \(\kappa\)-flux and
\(Q\)-divergence vanish, while

\[
 \widehat\Xi(0)
 =(1-q^4)\operatorname{diag}(-48,48,0).
\]

The independent grouping confirms that the \(|m|^2=1\) contributions cancel
exactly and that the displayed coefficient comes from \(|m|^2=2\).  This
proves only that the contracted velocity-cumulant flux does not supply the
complete same-output stress forcing.  It is not a two-state collision for the
full \(\kappa_s\) field.

## 5. Selected quartic next-level remainder

On the four-site field, the selected inviscid nonlinear tangent is

\[
 \left.\partial_t\widehat\kappa_{112,s}(0,2,0)\right|_{\rm nonlinear}
 =2iq^2(1-q^2)^2.
\]

It is nonzero for every \(0<s<\infty\).  At \(q=1/2\), an independent exact
finite-\(\varepsilon\) interpolation extracts \(9i/32\), agreeing with the
formal polynomial.  Under \(s=\theta L^{-2}\), the coefficient becomes

\[
 2iL e^{-2\theta}(1-e^{-2\theta})^2.
\]

The valid conclusion is a nonzero fourth-order remainder in this selected
third-level physical-time equation.  It is not fourth-order non-closure and
does not prove a no-go theorem for every finite hierarchy.

## 6. Scope of the pass

This package is an exact finite Fourier certificate, not a Navier--Stokes
trajectory or a singularity simulation.  It establishes the displayed
pressure-compatible third-order interface, a coefficientwise pressure
obstruction, and one nonzero next-level remainder.  It does not control the
pressure--strain row from the energy class, the signed production
\(-\tau:\nabla v\), or the zero-scale critical budget.  Arbitrary-data
three-dimensional global regularity and the Clay problem remain open:
`NOT CLAY`.

Both implementations use Python's standard library and exact rational
arithmetic.  Floating point, network access, GPU, DGX, and PDE time
integration were not used.  Ordinary translation remains local and direct.
