# R0.71S certificate

This directory archives the exact producer and the independently reconstructed
R0.71S finite packet audits.

- result.json is produced by research/r071s_exact_audit.py. It records the
  nonzero-mean box-packet inverse-height diagonal, finite same-direction Gram
  enclosures, adjoint heat-packet constants, the separable bilinear mean
  dichotomy, soft even-touch signed cancellation, and the genuine covariant
  NSE initial observation-face ledger.
- independent-result.json is produced by
  research/r071s_independent_audit.py. It imports neither the exact producer
  nor its output. It reconstructs the matrices with NumPy, checks the heat
  constants by independent Gauss--Legendre quadrature, and separately rebuilds
  the even-touch and initial-face ledgers.

The genuine NSE family is the compatible torus dilation

\[
u_{0,K}(x)=K(0,\cos Kx_1,\cos Kx_2).
\]

For this covariant initial observation face,

\[
A_+=\frac{K^2}{4},
\qquad
K^{-2}A_+=\frac14,
\]

and the corresponding bare Leray time-integral scale is \(K^{-2}\). These are
initial-face and covariance identities. They are not a positive-time numerical
integration, an internal-entry theorem, or a regularity result.

The even-touch paths and general packet families are finite
forced-parabolic or linear method tests, not Navier--Stokes trajectories.
