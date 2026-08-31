# R0.73Q finite formula certificate and formal-figure audit

**Audit date:** 2026-08-31

**Status:** **FINAL SEAL PASS — NOT CLAY**

**Scope:** the exact smooth-shear norm triplet, the scalar endpoint time-map
counterexample, the independently implemented 19-file formula certificate,
and the associated 25-file journal-figure package.

**Verdict:** the primary calculation, independent recomputation, structural
validation, checksums, commit bindings, vector/raster outputs, and visual QA
pass.  Both packages are sealed to immutable analytic source commit
`cb9511c3af08a4beb0b31284e96e2a9c47a23d04`.  They certify formula
reproducibility only; they are not a Navier--Stokes simulation, a continuum
fixed-point certificate, or a global-regularity theorem.

## 1. Exact finite contract

For normalized Haar measure on \([0,2\pi]^3\), the certificate checks

\[
 w_N=N^{-1/4}e_2\sin(Nx_1),
 \qquad N=2^j,
\]

and the exact formulas

\[
 \|w_N\|_2=2^{-1/2}N^{-1/4},
\]

\[
 \|e^{t\Delta}w_N\|_{L^4_tL^6_x}
 ={(5/16)^{1/6}\over4^{1/4}}N^{-3/4},
\]

\[
 |w_N|_{\dot H^{1/2}}=2^{-1/2}N^{1/4}.
\]

It separately checks, for

\[
 g_n(s)=n^{-1/4}(1-s)^{-1/4}
 \mathbf 1_{\{e^{-n}<1-s<1/2\}},
\]

that

\[
 \|g_n\|_4^4=1-{\log2\over n},
 \qquad
 I_{1/4}g_n(1)=n^{3/4}-n^{-1/4}\log2.
\]

The second identity is a scalar one-dimensional endpoint obstruction.  It
does not assert that \(g_n\) is a Navier--Stokes trajectory and does not
refute the full Koch--Tataru tent-space estimate.

## 2. Independent certificate paths

`research/certificates/r073q` contains exactly 19 files: nine source files
and ten generated files.  Its source table has 32 data rows:

| Block | Rows |
| --- | ---: |
| Fourier modes \(N=2^j\), \(0\le j\le24\) | 25 |
| canonical time-map samples | 7 |

The direct producer passes 118 checks.  The independent validator passes 35
checks and neither imports nor invokes the producer.  It reconstructs the
sixth trigonometric moment using the central-binomial identity and rebuilds
the Fourier grid from integer indices.  The fail-closed structural validator
passes 40 checks.  Thus 193 declared checks pass in total, with maximum
independent relative error

\[
 7.814\times10^{-16}.
\]

The source-data SHA-256 is
`1dd4e3605f985dc1f49e08c71b066c7de5dc0547a4c475b410cf08f984a430bc`.
The final manifest state is:

```text
status=sealed
allPrerequisiteChecksPass=true
sourceCommitAssigned=true
sourceCommit=cb9511c3af08a4beb0b31284e96e2a9c47a23d04
finalSeal=true
```

Selected certificate hashes:

| File | SHA-256 |
| --- | --- |
| `manifest.json` | `2db5961d3e33ae44eabce6a8876993cec1e239eb9a42c6549e0105f2f2060de6` |
| `certificate.json` | `9fd30b43a8998b328cf935234bc549a28f43cd83d3c6b3827908c7a3431b3453` |
| `validation.json` | `178abc7a419b48aed41d4c437180c39040d05d55ad2d63f66573d2d4944bdbfc` |
| `independent_validation.json` | `bf4a9438ee742d6037ddc7ad4b04673b383d76134d37bd489f646c808cdc3361` |
| `diagnostic.json` | `2b8db1f663920131d602d239f758770920467bc9d124df912fc7bd3772713213` |

## 3. Formal figure package

`research/figures/r073q/fig-r073q-heat-flow-separation` contains exactly 25
files: ten source files and fifteen generated files.  The final validator
passes all 44 automated checks.  The final-size color surface, grayscale
surface, and independently rasterized PDF surface were visually inspected.

The three panels show:

1. the exact \(N^{-1/4}\), \(N^{-3/4}\), and \(N^{1/4}\) shear scalings;
2. the parametric \((\|w_N\|_{\mathfrak X},|w_N|_{1/2})\) separation, with
   the visible warning `NO RADIUS ORDERING — THE STABLE SET IS A UNION`;
3. bounded \(\|g_n\|_4\) against divergent \(I_{1/4}g_n(1)\), with the
   visible warning `BARE ENDPOINT MAP ONLY — NOT KOCH--TATARU THEORY`.

The master outputs are a one-page 178 mm by 90 mm vector PDF, a vector SVG,
and a 600 dpi PNG at 4,204 by 2,125 pixels.  The PDF contains no raster image
objects.

Master-output hashes:

| Output | SHA-256 |
| --- | --- |
| `figure.pdf` | `70343895028322a6d922d51042a5d854750cce1b62374d854a4e40eee998fc31` |
| `figure.svg` | `ad73f7571d0037c2b4a398cfeaeb5f3fa2873d1a2b001d98a79c94667d52c620` |
| `figure.png` | `4f47ab80bb0f9ebf83adc61a0701b6929bac7fe5a23c5e0665059868482d77fa` |
| `manifest.json` | `b002cf3fb348b6fbf33308f468100d827f8c547856bc81f0ec4ae135a114ccd0` |
| `validation.json` | `eab96b662452298e64ab28e6b3a9d7b240d8353c70af1b91fe1327507a127ae6` |
| `results.json` | `e5066a2aa078adee55711b83ce6f815ca8c8f908335a3fd38eb831d6b092d459` |

The figure source table has 53 rows: 33 shear samples and 20 endpoint
samples.  Its hash differs from the certificate table because it uses a
denser plotting grid; both use the same closed formulas.

## 4. Evidence boundary

The finite packages verify constants, powers, row identity, output identity,
and figure rendering.  The periodic Oseen--HLS bilinear estimate, Volterra
inverse, fixed point, and Serrin continuation remain supported by the
separate continuum proof and analytic audit.

This audit does not establish an arbitrary \(L^2\)-only strong radius,
necessity or optimality of a PDE threshold, nonlinear instability,
finite-time singularity, endpoint uniqueness, or arbitrary-data global
regularity.  It makes no novelty or priority claim.

All calculations ran locally on one CPU process.  DGX was not used, and
ordinary translation is performed directly rather than sent to DGX.

## 5. Machine ledger

```text
formulaDiagnosticValidation=PASS
formulaDiagnosticPackage=CLOSED
sourceCommitAssigned=TRUE
finalSeal=TRUE
formalFigurePackage=PASS
publicReleaseContent=READY
finiteFormulaDiagnosticIsNavierStokesSimulation=FALSE
finiteFormulaDiagnosticCertifiesContinuumFixedPoint=FALSE
formalFigureOrdersOldAndNewRadii=FALSE
formalFigureRefutesFullKochTataruTheory=FALSE
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```
