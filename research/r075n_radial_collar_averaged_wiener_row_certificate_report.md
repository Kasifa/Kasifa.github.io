# R0.75N finite certificate report

- Verdict: **PASS**
- Assertions: 16/16
- Main SHA-256: ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318
- Fixture SHA-256: 2dee2146f94f3fa6d0d0c5828d8d6f354f0856f620e1261a133c9a2c81f8a0cb
- Expected SHA-256: 31614fc11bc4355723fff7773bec8ab13bc44808ffffa0958c78ec1cfe2bba48
- Failed checks: none

Exact rational fixtures verify the frozen p=32/63 calibration, central canonical cover, 1/(2*pi) Fourier convention, d_ell=i*ell*Xi_ell, and d_0=0. The R=1/4 sample split separately checks the low count and the two-integration-by-parts high tail with R^(nu-1) scaling and sum-sup order.

Six exact spherical slices include interior, tangency, boundary, and empty cases under the uniform 4*pi*a*delta cap. Scaling ledgers verify the first and third radial derivatives, Fubini L1 rows O(a) and O(a^2), x1-average coefficient R, full-average coefficient R^2, and final rows O(a) and O(Ra^2).

At K>=R^(-3/2), K^(-2/3)<=R gives LR and L^2R^2. This is a chosen canonical geometric coefficient theorem, not a universal cutoff or dynamical flux result. Vertical diffusion, local payment, packet summation, and E.24 remain open. **NOT CLAY.**
