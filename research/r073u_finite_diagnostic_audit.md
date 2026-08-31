# R0.73U finite diagnostic audit: exact four-site tensor parity witness

**Audit date:** 2026-09-01

**Verdict:** PASS for the finite initial-data diagnostic.  The sealed
standard-library certificate reconstructs the four-site witness with exact
Gaussian-rational arithmetic.  All 75 required checks pass, all 75 check
identifiers are distinct, and the stored result is byte-identical to a fresh
read-only reconstruction.  The \(u/-u\) comparison is made between two
initial data at the same initial time \(t=0\), not between two symmetric
Navier--Stokes trajectories.

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

## 1. Immutable bindings and read-only verification

The certificate is bound to three separate repository layers:

| Layer | Immutable identifier |
|---|---|
| frozen analytic source | `84e808dae473f6381cbf9df55a71f5fe81a1cfce` |
| six certificate source files | `6c79f23152116f5d420be6ff03653500ab02ef0e` |
| generated certificate seal commit | `044bfb3f7e5af98e2615f60747c9e5109ef12d7c` |

The final manifest has SHA-256
`8493a18c97ef592e55dd169c3a0bba963cbd0b57c5d43d6bfc307665227e288c`.
The principal bound inputs and output are:

| File | SHA-256 |
|---|---|
| `compute_exact_certificate.py` | `ae653906d8363eb71a726d4b8fdb276d13dbae2b543c8a7198332cdf104318b8` |
| `audit-checklist.json` | `f5c577db3bc8488a59fb1005291ad68530974c0869dc3c6b3bfd6139b3a73ad3` |
| `results.json` | `1a89e30f3285af0b3d0dca11d4922c42bb5840cb878409e46b1cbd569579d238` |
| `seal_package.py` | `1cb106a731a1c59fb3de93f65a76b327b166ca28b2973fb21cc74a92d0b58f0a` |

I reran the following non-writing checks from the repository root:

```text
python3 -B research/certificates/r073u/compute_exact_certificate.py --check-only
python3 -B research/certificates/r073u/seal_package.py \
  --certificate-source-commit 6c79f23152116f5d420be6ff03653500ab02ef0e \
  --check-only
cd research/certificates/r073u && shasum -a 256 -c SHA256SUMS
```

The producer returned
`R073U_EXACT_CERTIFICATE=PASS mode=check-only checks=75/75`; the seal returned
`finalSeal=true` and `status=sealed`; all eight checksum entries returned
`OK`.  The four analytic working copies and both certificate layers also have
no tracked diff from their bound commits.  The obsolete analytic hash
`72493751370aa948947000df169e21199fc5c95d` is explicitly rejected by the
sealer.

## 2. Exact witness contract

The normalized Fourier convention is

\[
 \widehat f(k)=\int_{\mathbb T^3}f(x)e^{-ik\cdot x}\,d\mu(x).
\]

The certified real, mean-zero, divergence-free field is

\[
 u=(2\sin(x+y),\;2\sin x-2\sin(x+y),\;0).
\]

It has the four sites

\[
 \widehat u(1,0,0)=(0,-i,0),\qquad
 \widehat u(1,1,0)=(-i,i,0),
\]

together with their conjugates.  At \(h_*=(1,2,0)\), define

\[
 A_{ij}=-ih_{*,\ell}\widehat{u_\ell u_i u_j}(h_*),
 \qquad
 B_{ij}=-\widehat{u_j\partial_i p+u_i\partial_jp}(h_*),
 \qquad K=A+B.
\]

The exact target entries are

\[
 \widehat T(h_*)=0,\qquad
 V(h_*)=\widehat{\Delta T-2\partial_\ell u\otimes\partial_\ell u}(h_*)=0,
\]

\[
 A=\begin{pmatrix}-2&3&0\\3&-4&0\\0&0&0\end{pmatrix},
 \qquad
 B=\begin{pmatrix}0&-2&0\\-2&4&0\\0&0&0\end{pmatrix},
\]

\[
 K=\begin{pmatrix}-2&1&0\\1&0&0\\0&0&0\end{pmatrix},
 \qquad \lVert K\rVert_F^2=6.
\]

The complete nonzero pressure table is

```text
(-2,-1,0): 2/5    (0,-1,0): 2
( 0, 1,0): 2      (2, 1,0): 2/5
```

with \(\widehat p(0)=0\).  These entries agree with
\(\widehat p(h)=-h_i h_j\widehat T_{ij}(h)/|h|^2\).

## 3. Two independent Fourier paths

The certificate does not verify only the displayed coefficient.

1. The product-law path constructs the complete maps for \(T\), the cubic
   tensor \(F\), \(A\), the pressure--velocity term \(B\), the gradient
   product, and \(V\) by sparse convolution.
2. The velocity-law path reconstructs pressure directly from ordered velocity
   pairs, forms the Navier--Stokes velocity tangents
   \(-(u\cdot\nabla)u-\nabla p\) and \(\Delta u\), and then applies the exact
   product rule to \(u\otimes u\).

The full pressure maps, full nonlinear tensor-tangent maps, and full viscous
tensor-tangent maps agree exactly between the two paths.  The target \(K\)
and \(V\) entries agree separately.  No floating-point tolerance is involved.

The sign-reversed field is rebuilt rather than inferred.  The recomputation
confirms that \(T,p,V,\Theta_s,\tau_s\) are even, whereas \(F,A,B,K\) are odd.
Thus, for the solutions launched from \(u_0=u\) and
\(\widetilde u_0=-u\), the target tangent separation at their common initial
time is

\[
 \left.\partial_t\widehat\Theta_s(h_*;u(t))\right|_{t=0}
 -\left.\partial_t\widehat\Theta_s(h_*;\widetilde u(t))\right|_{t=0}
 =2e^{-5s}K,
 \qquad
 \left\|\cdot\right\|_F=2\sqrt6e^{-5s}.
\]

## 4. Heat groups, dilation, and the certified boundary

For \(S_m=\sum_{|h|^2=m}|K(h)|_F^2\), the complete exact groups are

```text
m:     1       2      5      10      13
S_m: 176/25  276/25  12     36/25   76/25
4S_m:704/25 1104/25  48    144/25  304/25
```

The factor four is the square of the sign-pair factor two.  For
\(u_L(x)=u(Lx)\), \(h_L=(L,2L,0)\), the exact coefficient and Frobenius
separations are

\[
 2Le^{-5sL^2}K,
 \qquad
 2\sqrt6Le^{-5sL^2}.
\]

At \(s=\theta L^{-2}\), this is

\[
 2\sqrt6Le^{-5\theta}
 =2\sqrt{6\theta}e^{-5\theta}s^{-1/2}.
\]

The normalized profile is maximal at \(\theta=1/10\).  A real mean-zero field
on one conjugate pair has zero self-advection by incompressibility, so the
certificate also establishes the four-site support boundary for this parity
mechanism.  It does not establish minimality among all closures or all no-go
arguments.

## 5. Scope of the pass

This is an exact finite diagnostic.  It is not a Navier--Stokes simulation,
not a numerical PDE trajectory, and not a proof about singular or
near-singular solutions.  It excludes only a single-valued autonomous signed
equality based on the even quadratic state.  It does not exclude absolute or
one-sided estimates, time-integrated cancellations, tensor bounds, or a state
augmented by signed velocity or odd/cubic data.  It does not prove global
regularity and does not solve any part of the Clay problem: `NOT CLAY`.

In particular, the audit does not claim
\(\Theta_s(u(t))=\Theta_s(-u(t))\) along a trajectory, nor that the solution
from \(-u_0\) is the negative of the solution from \(u_0\).  Only the initial
quadratic states coincide algebraically; the unequal initial tangents are the
obstruction.

The computation used the local CPU and Python standard library only.  DGX,
GPU, network access, and Navier--Stokes time integration were not used.
Ordinary translation remains local and direct.
