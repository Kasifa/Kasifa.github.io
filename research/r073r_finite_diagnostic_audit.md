# R0.73R finite formula certificate and formal-figure audit

**Audit date:** 2026-08-31

**Status:** **FINAL SEAL PASS — NOT CLAY**

**Scope:** the matched Dirichlet/Rudin--Shapiro Fourier family, its exact
finite sixth-moment identities and scaling diagnostics, and the associated
25-file journal-figure package.

**Verdict:** the primary calculation, independent reconstruction, structural
validation, checksums, source-commit bindings, vector/raster outputs, and
visual QA pass.  Both packages bind their source files to immutable analytic
commit `25b20d225202359de2fd2d95ed86dd4b372d23a5`.  The generated formula
package is preserved in commit
`6809fc92a2d1338fb77fb3bf5a72d16ed158d807`, and the generated figure
package is preserved in commit
`f3d8ac3b04aa122a44f112d554c4991ecfb6f36e`.  These artifacts certify
finite formula reproducibility and figure identity only; they are not a
Navier--Stokes simulation, a continuum PDE certificate, or a
global-regularity theorem.

## 1. Exact finite contract

For normalized Haar measure on \([0,2\pi]^3\), the certificate checks the
real divergence-free fields

\[
 W_{R,m}(x)=\frac{\sqrt2}{m}e_3\operatorname{Re}\!\left[
 e^{iNx_1}R_m(e^{ix_1})R_m(e^{ix_2})\right],
 \qquad N=8m,\quad m=2^r,
\]

where \(R_m=D_m\) is the Dirichlet polynomial or \(R_m=P_m\) is the
Rudin--Shapiro polynomial.  At each configured \(m\), the two fields have
the same \(2m^2\) Fourier sites, coefficient modulus
\(1/(\sqrt2m)\), normalized \(L^2\) norm one, and every quadratic
Fourier-weighted Sobolev norm.

The exact sixth-moment contract is

\[
 \|W_{R,m}\|_6^6
 =\frac{5}{2m^6}\|R_m\|_6^{12},
\]

with

\[
 \|D_m\|_6^6=\frac{11m^5+5m^3+4m}{20}.
\]

The Rudin--Shapiro path separately checks its recursive signs and the energy
identity \(|P_m|^2+|Q_m|^2=2m\).  The table records the diagnostic

\[
 N^{-1/2}\|W_{R,m}\|_6
\]

under the explicit name `annular_heat_proxy`.  It also records the common
amplitude scaling

\[
 \alpha_m=N^{1/2}m^{-2/3}=\sqrt8\,m^{-1/6}
\]

and the corresponding normalized proxy and homogeneous
\(\dot H^{1/2}\) quantities.  The proxy is not asserted to equal the full
heat-flow norm.

## 2. Independent certificate paths

`research/certificates/r073r` contains exactly 19 files: nine source files
and ten generated files.  Its source table has 16 data rows, comprising the
Dirichlet and Rudin--Shapiro entries for each of
\(m=1,2,4,8,16,32,64,128\).

The direct producer passes 114 checks.  The independent validator passes 65
checks and neither imports nor invokes the producer.  It reconstructs the
Rudin--Shapiro signs from the parity of overlapping `11` blocks in the binary
index, directly enumerates ordered coefficient triples for the sixth moment,
and rebuilds the carrier moment independently.  The fail-closed structural
validator passes 115 checks.  Thus the declared inventory is
`114 + 65 + 115 = 294` passing checks.  The maximum independent relative
error is

\[
 5.215091340399836\times10^{-15}.
\]

The source-data SHA-256 is
`af7e61978b9ed49507445080c17067275fb69593fe22cb57db265b526b247f33`.
The final manifest state is:

```text
status=sealed
allPrerequisiteChecksPass=true
sourceCommitAssigned=true
sourceCommit=25b20d225202359de2fd2d95ed86dd4b372d23a5
finalSeal=true
```

Selected certificate hashes:

| File | SHA-256 |
| --- | --- |
| `manifest.json` | `ae7bb85db95b42569f869e5064ac0c625613cc2c8333c9ec8e9bc378f43127c7` |
| `certificate.json` | `7004757dfd9a0fcab6797e9d85fa22f84fe64af36c048e38f9539f11000498cc` |
| `validation.json` | `7cebaaae25333c1584c77b6022a49b2da17d5fd7e47a39e878323ae92d71f732` |
| `independent_validation.json` | `d02ee83cbe4ba8ac0e5ba1ac656a6e7b5ff1798ddd2e18656ccd7b2565fb6a42` |
| `diagnostic.json` | `9022694e8b12192a48c8016015b287581994d11cc2e9086b10a9e9a66b3df6fc` |

## 3. Commit ledger

The seal uses separate immutable source and artifact commits to avoid a
self-referential hash claim.

| Role | Commit | Audited content |
| --- | --- | --- |
| analytic and package sources (A) | `25b20d225202359de2fd2d95ed86dd4b372d23a5` | the nine certificate sources, the ten figure sources, and the analytic R0.73R source set |
| formula artifacts (B) | `6809fc92a2d1338fb77fb3bf5a72d16ed158d807` | the ten generated certificate files |
| figure artifacts (C) | `f3d8ac3b04aa122a44f112d554c4991ecfb6f36e` | the fifteen generated figure files |

The final certificate sealer re-read all nine source blobs from commit A.
The final figure validator re-read all ten source blobs from the same commit.
The artifact commits B and C contain the byte-identical generated packages
reported below; they are recorded here rather than written into an artifact
that would have to hash its own commit.

## 4. Formal figure package

`research/figures/r073r/fig-r073r-phase-coherence` contains exactly 25
files: ten source files and fifteen generated files.  The independent final
validator passes 49/49 automated checks and reconstructs all 141 source-data
rows: 128 exact positive-packet sign rows and 13 analytic-scaling rows.  The
final-size color surface, grayscale surface, and independently rasterized PDF
surface were visually inspected.

The three panels show:

1. the common Fourier packet and matched coefficient moduli at \(m=8\), with
   only the Dirichlet/Rudin--Shapiro signs changed;
2. the analytic unscaled guides \(m^{1/6}\), \(m^{-1/2}\), and their
   \(m^{2/3}\) ratio;
3. after the shared amplitude scaling, the common \(L^2\) guide
   \(m^{-1/6}\), the Dirichlet and Rudin--Shapiro heat guides \(1\) and
   \(m^{-2/3}\), and the shared \(\dot H^{1/2}\) guide \(m^{1/3}\).

Panels 2 and 3 display prescribed analytic powers normalized at \(m=1\).
They are not fitted scaling laws or sampled PDE trajectories.

The master outputs are a one-page 178 mm by 94 mm vector PDF, a vector SVG,
and a 600 dpi PNG at 4,204 by 2,220 pixels.  The PDF contains no raster image
objects, and the SVG contains no embedded image element.

Master-output hashes:

| Output | SHA-256 |
| --- | --- |
| `figure.pdf` | `08724ae1dcdc38f1fd983f114f0a60b56fe94cbee7243eb0bc026babb3a830c9` |
| `figure.svg` | `2b97f8b18782327139c4ec1612698ee34dd6dcac784ba46827ddb977e8d6fed3` |
| `figure.png` | `47dddbf4730c270d6b16eb9487dfdea2f0f6ec16f41a08bd4c8ba950d9aee93a` |
| `manifest.json` | `72cac23c62634800b6d4b53c88ce953a47b24486da0d17b03820f8b4268012f2` |
| `validation.json` | `55163eca1c29bb368dd719c3e43ad1ecec45fe9b926ec4b1a90052d69b0b1417` |
| `results.json` | `cae232f94d8a39b38c942c16141e2411df18ac6e01eba7ac47840d3a7ae00c5d` |

## 5. Evidence boundary

The finite packages verify exact coefficient data, sixth-moment identities,
row identity, theoretical exponent bookkeeping, output identity, physical
figure dimensions, and rendering QA.  The Littlewood--Paley/heat-semigroup
equivalence and its continuum multiplier estimates remain supported by the
separate analytic proof and analytic audit.

The certificate performs no heat-flow time quadrature and no interval
arithmetic.  It does not certify a necessary stability criterion, nonlinear
instability, finite-time singularity, or arbitrary-data global regularity.
Failure of a sufficient small-heat-norm entrance condition is not evidence of
unsafe dynamics.  The displayed fields have zero convection and their
Navier--Stokes evolutions are globally smooth heat flows.

All finite calculations and figure rendering ran locally with one CPU
process and no GPU.  DGX was not used.  I complete ordinary release
translation directly on the local workstation; no ordinary translation step
is routed through DGX.  I make no novelty or priority claim from these finite
checks.

## 6. Machine ledger

```text
formulaDiagnosticValidation=PASS
formulaDiagnosticPackage=CLOSED
formulaDiagnosticPrimaryChecks=114
formulaDiagnosticIndependentChecks=65
formulaDiagnosticStructuralChecks=115
formulaDiagnosticRows=16
sourceCommitAssigned=TRUE
sourceCommit=25b20d225202359de2fd2d95ed86dd4b372d23a5
formulaArtifactCommit=6809fc92a2d1338fb77fb3bf5a72d16ed158d807
finalSeal=TRUE
formalFigurePackage=PASS
formalFigureChecks=49
formalFigureRows=141
figureArtifactCommit=f3d8ac3b04aa122a44f112d554c4991ecfb6f36e
dgxUsed=FALSE
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
finiteFormulaDiagnosticIsNavierStokesSimulation=FALSE
annularHeatProxyIsExactHeatNorm=FALSE
finiteFormulaDiagnosticCertifiesContinuumPdeProof=FALSE
formalFigureUsesFittedScalingLaws=FALSE
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```
