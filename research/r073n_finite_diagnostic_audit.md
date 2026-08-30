# R0.73N theorem-relevant finite diagnostic audit

**Audit date:** 2026-08-31

**Status:** **PRESEAL PASS / IMMUTABLE SOURCE COMMIT PENDING**

**Scope:** exact and high-precision checks of the finite-strain coefficient,
the endpoint exponent bracket, the marked-basepoint sensitivity source data,
and the associated journal-figure package

**Verdict:** the finite diagnostic and figure packages pass their mathematical,
independent-recomputation, provenance, format, and visual-QA gates.  They are
currently SHA-256-bound but uncommitted.  No source commit is claimed, no
public copy was created, and final sealing remains a separate post-commit
operation.

## 1. Exact analytical quantities

For

\[
 \overline U_\Lambda(t,y)
 =\left(0,0,-\Lambda e^{-4t}\sin2y
 +\frac\Lambda2e^{-16t}\sin4y\right),
\]

the derivative of the third component is

\[
 \partial_yF_\Lambda
 =-2\Lambda e^{-4t}\cos2y
 +2\Lambda e^{-16t}\cos4y.
\]

The triangle inequality gives the upper envelope, and equality is attained at
\(y=\pi/2\).  Hence, for \(\Lambda>0\),

\[
 \frac1{2\Lambda}\|\partial_yF_\Lambda(t)\|_\infty
 =e^{-4t}+e^{-16t}.
\]

Its cumulative coefficient is therefore

\[
 j(T)=\frac{1-e^{-4T}}4+\frac{1-e^{-16T}}{16},
 \qquad
 j(\infty)=\frac14+\frac1{16}=\frac5{16}.
\]

At \(D_*=1/450\) and \(T_*=D_*/4=1/1800\), the 100-digit run gives

\[
 j_*=j(T_*)
 =0.0011080324480805907920035217032737848724398721703663342577918591
 \ldots.
\]

The strict comparison does not rely on this decimal.  Applying
\(1-e^{-x}>x-x^2/2\) separately to the two exponentials gives

\[
 j_*>\frac{D_*}{2}-\frac{5D_*^2}{8}
 =\frac{359}{324000}.
\]

Consequently the exact/inherited chain is

\[
 j_*>\frac{359}{324000}
 >\frac{173}{450000}>\mathcal A_*.
\]

The last inequality is an inherited sealed R0.73M analytic input.  This
finite package records it but neither recomputes nor proves it.  The two
reported positive margins are

\[
 j_*-\frac{359}{324000}
 =7.7567225661006454970\ldots\times10^{-9},
\]

and

\[
 \frac{359}{324000}-\frac{173}{450000}
 =0.0007235802469135802469\ldots.
\]

## 2. Independent numerical checks

The primary implementation uses `mpmath==1.3.0` at 100 decimal digits.  It
checks ten identities or inequalities, including high-precision quadrature
against the closed form.  The independently written implementation uses
Python `Decimal` at 120 digits, exact `Fraction` comparisons, and a
range-reduced Taylor implementation of the exponential; it does not import
the primary producer or `mpmath`.

The independent endpoint value differs from the primary value by

`8.153040932416853897010961949581E-84`.

At six sentinel times, the largest centered finite-difference discrepancy in
the derivative check is

`9.066666666666666666666656266667E-49`.

The certificate validator passes 19 fail-closed checks.  Its exact source
data contains 605 rows:

- 241 strain-envelope samples on \([0,3/2]\);
- 243 cumulative samples, including \(0\) and \(T_*\);
- 121 marked-basepoint samples for \(\Lambda=0,100,\ldots,12000\).

The certificate source-data SHA-256 is
`cdde9894f05a0c78ba70d272df67c2423508535bdf469c7c273a34b960418a1f`.
Sampling is used for reproducible plotting and error detection; the exact
identities and strict rational witness carry the mathematical statements.

## 3. Certificate package state

`research/certificates/r073n` has the exact 19-file inventory required by its
manifest: 9 source files and 10 generated files.  The primary diagnostic,
independent implementation, certificate assembly, and independent validator
all pass.  `SHA256SUMS` binds the 18 non-ledger files.

Current provenance state:

- `status = hash-bound-uncommitted`;
- `sourceCommitAssigned = false`;
- `finalSeal = false`;
- `allPrerequisiteChecksPass = true`.

The package deliberately does not infer a source commit from the current
repository `HEAD`.

## 4. Journal figure package

Figure `fig-r073n-finite-strain-bracket` is a 178 mm by 96 mm three-panel
double-column figure:

1. the exact strain envelope and its two heat-mode components;
2. cumulative \(j(t)\), the \(5/16\) asymptote, and the marked endpoint
   \(T_*=1/1800\), with \(j(0)=0\) explicitly labeled as off the logarithmic
   axis;
3. the inherited \(\mathcal A_*\) exponent band, \(j_*\), the exact rational
   witness, and sensitivity across different marked basepoints.  The top
   scale is the exact norm \(\|\overline U_\Lambda(0)\|_2=\sqrt{5/8}\,\Lambda\).

The figure source data is a row-for-row copy of the 605 certificate rows with
the upstream path and SHA-256 appended to every row.  The 25-file figure
inventory contains 10 source files and 15 generated files, including the
chart-contract/source-data note, code, validation, manifest, monitoring logs,
QA report, and hashes.

Current preseal master outputs:

| Output | Technical property | SHA-256 |
| --- | --- | --- |
| `figure.pdf` | one vector page; 178.0000000000147 mm by 96.00000000001111 mm; zero raster image XObjects | `4c5675b645ceedeef2d72cae6cdbd2c73b20ce63484453f4bd6d92ad315c41d5` |
| `figure.svg` | vector; text preserved; zero embedded raster images | `7d3396e5c89290a95ac709613c62ac0bb8f90f103cc779a0cc88597c7f6f3517` |
| `figure.png` | 4204 by 2267 pixels; 599.9988 dpi metadata | `43aed593c7fcd17640fa6f3ff1e755cd392397da1965e7278bb74aaf29283b48` |

These are preseal hashes.  The required post-commit rerender and its newly
sealed manifest supersede them.

The color final-size raster, grayscale raster, and independently rasterized
PDF were visually inspected after the last render.  Labels, legends, scales,
annotations, panel headings, and both evidence-boundary lines are legible and
unclipped.  Line styles and fills remain distinguishable in grayscale.  The
PDF raster agrees with the PNG layout.  Twelve programmatic figure checks and
the explicit manual visual-QA gate pass.

The figure package remains `hash-bound-uncommitted`, with
`publicationStatus = not-published`, `sourceCommitAssigned = false`, and
`finalSeal = false`.

## 5. Evidence boundary

This audit validates exact elementary formulas, high-precision endpoint
evaluation, independent recomputation, source-data provenance, and static
presentation.  It does not use a finite grid to prove a continuum estimate.
In particular it does not certify:

- the inherited R0.73M action interval by computation;
- a sharp local flow-map modulus;
- arbitrary fixed-background Lyapunov instability;
- full three-dimensional FPS \((H^3,L^2)\) stability;
- transverse critical-norm growth;
- finite-time singularity or the Clay problem.

The marked-basepoint curves evaluate formulas at different backgrounds.  They
are not one fixed-background orbit and are not a measured sharp modulus.

## 6. Post-commit final-seal handoff

Final sealing must wait for a new immutable R0.73N theorem-source commit that
contains byte-identical copies of all 9 certificate source files and all 10
figure source files.  Let its explicit full hash be
`R073N_SOURCE_COMMIT`.  The required order is:

1. run the certificate sealer with
   `--source-commit R073N_SOURCE_COMMIT`, then run its `--verify-only` form;
2. rerun the plotter so the figure environment binds the newly sealed
   certificate manifest and source-data SHA;
3. inspect the regenerated color, grayscale, and PDF QA surfaces;
4. run the figure validator with `--confirm-visual-qa --source-commit
   R073N_SOURCE_COMMIT`, then run its `--verify-only` form.

Both final-seal paths fail closed unless the explicit commit exists, every
required source blob matches the current file bytes, and the certificate and
figure use the same source commit.  No current or future `HEAD` is substituted
implicitly.
