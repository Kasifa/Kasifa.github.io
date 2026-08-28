# Independent audit: R0.72Z Squire lane

**Date:** 2026-08-28

**Method:** independent recovery of kinetic coordinates, operator norms,
causal kernel estimates, exceptional rows, and lift-up witnesses.

## 1. Kinetic normalization

**Decision: PASS.**

For \(\mu>0\), independent substitution in the R0.72Y recovery formula
gives

\[
 \mu\|u\|_2^2
 =\|\mathcal L^{-1/2}q\|_2^2+\|\eta\|_2^2.
\]

Thus the report's normalized coordinates

\[
 Q=\mu^{-1/2}\|\mathcal L^{-1/2}q\|_2,
 \qquad H=\mu^{-1/2}\|\eta\|_2
\]

satisfy \(\|u\|_2^2=Q^2+H^2\).

## 2. Exact orientation coefficient

**Decision: PASS.**

The induced source norm is exactly

\[
 a_j(d)=|\xi\Lambda|
 \|M_{W_x(d)}\mathcal L^{-1/2}\|_{2\to2}.
\]

The bound

\[
 a_j(d)\le|\Lambda|\|W_x\|_\infty
 \frac{|\xi|}{\sqrt{\xi^2+\gamma^2+\rho^2}}
\]

is correct.  The multiplier bound is not asserted to equal the exact norm.
Pure orientation is bounded after kinetic normalization, but \(|\Lambda|\)
remains.  A bound from \(c=\gamma\Lambda\) alone is false through the
\(\gamma=0\) boundary.

## 3. Spatial refinement

**Decision: PASS.**

The Hilbert--Schmidt calculation uses

\[
 \|W_x\|_{L^2_{\rm avg}}^2
 =\frac18(e^{-2d}+e^{-8d})
\]

and the standard reciprocal-lattice sum.  At \(\beta=0\), the constant
Fourier input gives a matching lower bound, hence

\[
 \|M_{W_x}\mathcal L^{-1/2}\|
 \sim \|W_x\|_{L^2_{\rm avg}}\mu^{-1/2}.
\]

Multiplication by \(|\xi\Lambda|\) yields the finite transverse lift-up
limit \(|\Lambda|\|W_x\|_{L^2_{\rm avg}}\).

## 4. History and endpoint estimates

**Decision: PASS.**

The ordinary kernel \(e^{-g\tau}\) gives the report's \(\Phi_g\) and
\(\Psi_g\) bounds.  The strong scalar kernel gives

\[
 \|K\|_1\le\min\{g^{-1},A_\vartheta\alpha^2\},
\]

\[
 \|K\|_2\le\min\{(2g)^{-1/2},
 \sqrt{B_\vartheta}\alpha\}.
\]

The estimates are conditional on the complete history of \(Q\).  A
terminal value of \(Q\) alone cannot determine the causal Squire response.

The standard and semiclassical negative-norm forcing powers remain those of
R0.72Y.  In particular, standard \(H^{-1}\) does not acquire an
\(O(\alpha^2)\) spacetime gain or a vanishing endpoint gain.

## 5. Damping gap and exceptional rows

**Decision: PASS.**

The convolution

\[
 \mathcal J_{a,b}(\tau)=
 \frac{e^{-b\tau}-e^{-a\tau}}{a-b}
\]

has the equal-rate limit \(\tau e^{-a\tau}\).  The report retains that
transient.

The partition \(\mu=0\), \(\xi=0\), \(\gamma=0\), small ratio, and large
ratio is exhaustive once overlapping zero cases are removed in that order.
The exact transverse lift-up solution proves that \(|\Lambda|\) and the
equal-rate transient cannot be deleted.

## 6. Audit boundary

The Squire inequalities close \(H\) conditional on a declared \(Q\)
history.  They do not close low-gap OS, do not supply row-uniform physical
energy weights, and do not justify an infinite direct sum.  The report keeps
all three statements OPEN.
