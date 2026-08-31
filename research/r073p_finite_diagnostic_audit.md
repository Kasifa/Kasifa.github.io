# R0.73P formula-diagnostic and formal-figure audit

**Audit date:** 2026-08-31

**Status:** **FINAL SEAL PASS — NOT CLAY**

**Scope:** the closed-form frequency and Sobolev-power checks, the exact
finite-lattice heat-semigroup benchmark, the independently implemented
19-file certificate, and the associated 25-file journal-figure package.

**Verdict:** the primary calculation, independent recomputation, source-data
identity, provenance bindings, checksums, vector/raster outputs, and visual QA
pass.  Both packages are sealed to immutable source commit
`c087845e65034d2ba92b8a8330d90e36e77704d3`.  They certify formula
reproducibility only; they are not a Navier--Stokes simulation, a nonlinear
entry certificate, or a regularity theorem.

## 1. Exact diagnostic contract

The package checks the normalized sufficient-frequency powers

\[
 N^{-3},\qquad N^{-1/2},
\]

the pure-mode Sobolev powers for \(a_N=cN^{-\gamma}\),

\[
 \|a_Ne_N\|_2\sim cN^{-\gamma},\qquad
 |a_Ne_N|_{1/2}\sim cN^{1/2-\gamma},\qquad
 |a_Ne_N|_3\sim cN^{3-\gamma},
\]

and the exact discrete linear-heat multiplier

\[
 \max_{k\in\mathbb Z^3\setminus\{0\}}
 |k|^3e^{-\tau|k|^2}
\]

against the continuous radial upper bound

\[
 \left({3\over2e\tau}\right)^{3/2},
 \qquad 10^{-3}\le\tau\le10.
\]

The open strip \(1/2<\gamma<3\) is the region where the \(L^2\) and
\(H^{1/2}\) powers decay while the \(H^3\) power grows.  This is an exact
norm-scaling statement, not a claim of dynamical instability.

## 2. Primary and independent calculations

The source table has 790 rows:

| Block | Rows |
| --- | ---: |
| frequency thresholds | 198 |
| pure-mode Sobolev powers | 351 |
| discrete heat maxima | 241 |

Its SHA-256 is
`634b2aab69509aca09da0a29c43a6b0ab44e88602878a96b3231ff58df65211a`,
and the certificate copy is byte-identical to the figure copy.

The producer passes 16 checks.  The independent path passes 24 checks and
does not import or call the producer.  It constructs the admissible squared
radii using Legendre's three-square criterion, whereas the producer directly
enumerates nonnegative integer triples.  The two paths find 3,414
representable positive squared radii through the cutoff 4,096.

At the smallest sampled time, the continuous maximizing squared radius is
1,500, so

\[
 4096>{3\over2(0.001)}=1500
\]

strictly closes the omitted lattice tail.  Across the configured grid the
discrete maximizer ranges from squared radius 1 to 1,501.  The largest
independent relative errors are

| Quantity | Maximum relative error |
| --- | ---: |
| threshold values | \(2.132\times10^{-16}\) |
| reconstructed \(\tau\) grid | \(2.296\times10^{-15}\) |
| Sobolev powers | \(0\) |
| discrete heat values | \(0\) |
| continuous bound | \(0\) |

The aggregate fail-closed validator passes all 23 checks.

## 3. Certificate package and provenance

`research/certificates/r073p` contains exactly 19 files: nine source files
and ten generated files.  `SHA256SUMS` binds the other 18 files.  Its final
state is:

- `status=sealed`;
- `allPrerequisiteChecksPass=true`;
- `sourceCommitAssigned=true`;
- `sourceCommit=c087845e65034d2ba92b8a8330d90e36e77704d3`;
- `finalSeal=true`.

The sealer verifies that the nine source blobs at the explicit commit are
byte-identical to the working package sources; it never substitutes the
current `HEAD`.

Selected hashes:

| File | SHA-256 |
| --- | --- |
| `manifest.json` | `8d2ff6acf6bb02ee7ae17ad1024d43fd1727d234ca80ddfd80496a960da43036` |
| `certificate.json` | `78136c8f21b7884587052232c9c62b7328a1c436d351e522cfb94b05ef2e624e` |
| `validation.json` | `784da8a21d5860161e15a09e3ce68fcb380efcfb8e4c5711e7c766b6f024b2c0` |
| `independent_validation.json` | `ffa7d0912db10331ec2b611dc3e2265e5bb9fbf2d8fbcd567396199da24246fd` |
| `diagnostic.json` | `889c52a580898cdfa51cf2774613e5a5f93ac2ea383b2d514444e7c260e608f0` |

## 4. Formal figure package

`research/figures/r073p/fig-r073p-critical-frequency-gate` contains exactly
25 files: ten source files and fifteen generated files.  Its 24-line
`SHA256SUMS` ledger binds every other file.  The formal validator passes all
33 automated checks, and the final-size color, grayscale, and independently
rasterized PDF surfaces have been visually inspected.

The master outputs are:

- a one-page vector PDF at 178 mm by 86 mm;
- a vector SVG;
- a 600 dpi PNG at 4,204 by 2,031 pixels;
- final-size, grayscale, and PDF-raster QA images.

Master-output hashes:

| Output | SHA-256 |
| --- | --- |
| `figure.pdf` | `b2446891346996a8ba270405bcf0673316c4e61df79ce3084536a606d31c7ab6` |
| `figure.svg` | `e68bd35e28cffc5c92630af427bc341d0d4fcf9ee8a8e0e98b6f6faeae99dc3d` |
| `figure.png` | `367d21a3431652d07f8b04786dd0131806f5af486ee928a09345d40bd4927ab3` |
| `manifest.json` | `94f1a59169745b4adcf5aad67ac77903c5f2eab8d34f503f8fa78124c470c301` |
| `validation.json` | `affc8f1d30b717bacaa02b8d1c9442aeba76375e2c84a409278a306fdf8570b0` |
| `results.json` | `30b17c097d29367745773fafc705d98030208cff14073a26b2f96bb9191f8661` |

Panel C carries the visible warning `LINEAR ONLY — NOT A NONLINEAR ENTRY
CERTIFICATE`.  The caption likewise denies any nonlinear Duhamel estimate.

## 5. Evidence boundary

This audit proves that the displayed algebraic powers and configured finite
lattice maxima were calculated reproducibly and that the figure reports them
faithfully.  The continuum stability statements remain supported by the
separate analytic proof and primary literature chain.

The audit does not establish a frequency-independent \(L^2\)-only strong
threshold, necessity of the \(N^{-1/2}\) exponent for the PDE, nonlinear
instability, finite-time singularity, weak-solution nonuniqueness, backward
regularity, or arbitrary-data global regularity.

The proper label is:

**closed-form formula diagnostic with independent exact-lattice
recomputation — NOT CLAY**

No novelty or priority conclusion is made.  All calculations in this package
ran locally with one process and no GPU; DGX was not used.

## 6. Machine ledger

```text
formulaDiagnosticValidation=PASS
formulaDiagnosticPackage=CLOSED
sourceCommitAssigned=TRUE
finalSeal=TRUE
formalFigurePackage=PASS
publicReleaseContent=READY
finiteAnalyticFigureProvesPDEThresholdNecessity=FALSE
finiteAnalyticFigureProvesNonlinearEntry=FALSE
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
```
