# R0.73I finite selected-gain action diagnostic

This package studies finite Fourier compressions of the selected
moving-profile gain.  It keeps three endpoints separate:

- `explicit-pilot`: `D=1e-4`;
- `analytic-upper-bound`: `D=sqrt(19/180)/392`;
- `one-over-450`: `D=1/450`.

None of these rows is labelled as the unknown theorem endpoint `D=d0`.
The latter two are route diagnostics at an analytic upper bound and at the
older comparison endpoint, respectively.

For a cutoff `N`, the package computes

```text
A_N(D) = integral_0^D Re(lambda_{0,N}(d)) dd,
log G_{Lambda,N}(D) - Lambda A_N(D),
C_N(D) = -integral_0^D Re(<ell,h_d> + <ell,Lh>) dd.
```

Here `lambda_{0,N}` is the numerically selected rightmost eigenvalue of the
finite inviscid kinetic matrix, and `h,ell` are finite right/left
eigenvectors with `<ell,h>=1`.  `C_N` is a finite WKB diagnostic.  It is not
an asymptotic theorem.

The producer uses a fourth-order commutator-free exponential integrator for
the primary selected gain and an independent classical RK4 integrator for
sentinels.  Ordinary cutoff, quadrature, and step agreement are explicitly
not Fourier-tail or continuum proofs.

Run the commands in `command.txt`.  Formal output is deterministic except
for elapsed times and host metadata.  No randomness is used.

