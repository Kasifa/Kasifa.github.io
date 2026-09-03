# R0.75J finite certificate report

- Verdict: **PASS**
- Assertions: 19/19
- Main SHA-256: 960e3cbc18ac8207253a8802da215b3eac07a714ddbcc7209985f27a00c9ff4d
- Fixture SHA-256: 754d585bab0b194adaa3f945dc8b14950e3c078564f38dc63919cf733fcfea2c
- Expected SHA-256: 6c32cd1ff38895c5e3b0a580ad9a5e789fc3d9d8e672ba6644dceeb29befe5b8
- Failed checks: none

Exact rational Fourier arithmetic verifies the forward/adjoint signs and the requested tau-polynomial fixture: L*psi has cosine coefficient 1+tau+2tau^2+tau^3, zero sine coefficient, zero terminal data, positive eta samples, and both signs on every sampled nonzero slice.

Finite product quadrature verifies zero mean of the physical derivative source for each fixed parameter slice and distinguishes a_+ and |a|. The J.12 endpoint signs, J.5/J.13 dissipation signs, constant-shift cancellation, CD surcharge, and nonnegative-majorant direction are all recomputed exactly.

The signed exact adjoint is not a nonnegative majorant. The a_+-driven majorant changes the source and its initial row remains unpaid. This is not a blanket no-go theorem for adjoint or Feynman--Kac methods. E.24 and all larger claims remain OPEN. **NOT CLAY.**
