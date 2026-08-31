# R0.73Q finite heat-flow formula certificate

This 19-file package independently reproduces the finite formulas used by the
R0.73Q periodic critical heat-flow entrance.  It is a reproducibility and
error-detection package.  It does not evolve the Navier--Stokes equations and
does not certify the continuum fixed-point proof.

For the normalized divergence-free Fourier mode

\[
 w_N(x)=N^{-1/4}e_2\sin(Nx_1),\qquad N=2^j,\quad 0\le j\le24,
\]

the package checks

\[
 \|w_N\|_2=2^{-1/2}N^{-1/4},
\]

\[
 \|e^{t\Delta}w_N\|_{L^4_tL^6_x}
 ={c_6\over4^{1/4}}N^{-3/4},
 \qquad c_6=\left({5\over16}\right)^{1/6},
\]

and

\[
 |w_N|_{\dot H^{1/2}}=2^{-1/2}N^{1/4}.
\]

It also checks a scalar time-map no-go family.  For integers \(n\ge2\), set

\[
 g_n(s)=n^{-1/4}(1-s)^{-1/4}
 \mathbf 1_{\{e^{-n}<1-s<1/2\}}.
\]

Then

\[
 \|g_n\|_{L^4(0,1)}^4=1-\frac{\log2}{n},
 \qquad
 \int_0^1(1-s)^{-3/4}g_n(s)\,ds
 =n^{3/4}-n^{-1/4}\log2.
\]

The second family demonstrates only the failure of the scalar endpoint map
`I_{1/4}: L^4_t -> L^infinity_t`.  It is not asserted to be a time profile of
a Navier--Stokes orbit.

## Independent paths

`compute_formula_diagnostic.py` produces the source table by a direct Fourier
coefficient and heat-integral calculation.  `independent_validate.py` neither
imports nor calls that producer.  It reconstructs the trigonometric sixth
moment with the central-binomial formula and independently rebuilds every row
from its integer index.

Both programs use only the Python standard library, one process, and no GPU.
Scientific stages are appended to `progress.ndjson`; elapsed time and peak
resident memory are appended to `resource-log.ndjson`.

## Claim boundary

The checked statements are finite closed-form diagnostics only.  They are not:

- a Navier--Stokes or other PDE simulation;
- a numerical proof of the periodic Oseen/HLS estimate;
- a certificate for the continuum Volterra inverse or fixed point;
- a necessary stability condition for a PDE solution;
- a global-regularity, singularity, or nonuniqueness theorem;
- a proof or partial proof of the Clay Millennium problem.

The exact machine-readable boundary is in `config.json` and is copied without
expansion into the diagnostic, independent validation, certificate, validation,
and manifest.

## Reproduction and two-stage seal

Run `command.txt` from the repository root.  The ordinary sealer creates a
`hash-bound-uncommitted` pre-seal.  It binds all nine source files and eight
pre-seal outputs while leaving the immutable source commit unassigned.

After a parent release commits the nine source files, run

```text
seal_package.py --source-commit <full-lowercase-40-hex>
```

to create the final commit-bound seal.  The sealer never substitutes `HEAD`
for an explicit commit and rejects any commit whose nine source blobs differ
from the current package sources.  Both `--verify-only` modes are fail-closed
and perform no writes.
