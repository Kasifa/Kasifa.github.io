# R0.73M bilingual terminology ledger

**Status:** canonical release terminology source
**Scope:** continuum proof, independent audits, finite certificate, formal
figure, HTML/PDF note, cumulative recap, and bounded literature boundary
**Release title:** *Prescribed-action planar nonlinear departure*

This ledger fixes the English terminology and claim-state vocabulary for
R0.73M. It does not enlarge the mathematical result.

## Core terminology

| 中文 | English | Exact usage boundary |
|---|---|---|
| 完整无黏作用量 | full inviscid action | \(\mathcal A_*=\int_0^{D_*}\lambda_0(r)\,dr\); this continuum quantity is never identified with a finite-cutoff proxy. |
| prescribed-action 种子 | prescribed-action seed | \(\rho e^{-\Lambda\mathcal A_*}\phi_\Lambda\), with \(\rho\) independent of \(\Lambda\). |
| 实际 selected 增益 | actual selected gain | \(G_\Lambda^*=\lVert S_{\pm1,\Lambda}(D_*,0)\phi_\Lambda\rVert_2\). |
| 两侧有界前因子 | bounded two-sided prefactor | \(c_Le^{\Lambda\mathcal A_*}\le G_\Lambda^*\le C_Le^{\Lambda\mathcal A_*}\); no prefactor limit is asserted. |
| 有效 Taylor 振幅 | effective Taylor amplitude | \(\delta_\Lambda=\rho G_\Lambda^*e^{-\Lambda\mathcal A_*}\in[c_L\rho,C_L\rho]\). |
| 固定剖面端点 | fixed profile-time endpoint | \(D_*=1/450\). |
| 固定物理端点 | fixed physical-time endpoint | \(T_*=D_*/4=1/1800\); the factor \(d=4t\) is part of the theorem. |
| 端点归一化前向轨道 | endpoint-normalized forward orbit | The forward selected orbit divided by its terminal gain; no backward parabolic evolution is used. |
| 固定端点后向局部化 | fixed-endpoint backward localization | A quotient estimate along one forward orbit, with rate \(\mu_*=167/1000>1/6\). |
| 谐波能量层级 | harmonic energy hierarchy | The quadratic, cubic, and fourth-order row estimates on the exact Fourier–Leray supports. |
| doubled row | doubled row | The generated \(K_z=\pm2\) row controlled by the margin \(1/1500\). |
| cubic return | cubic return | The third-order return to the selected \(K_z=\pm1\) pair, controlled by the margin \(1/1000\). |
| 四阶余项 | fourth-order remainder | The nonlinear remainder controlled by the margin \(21/125\). |
| 固定距离偏离 | fixed-distance departure | The selected-pair endpoint lower bound \(\lVert\Pi_{\pm1}w_\Lambda^\rho(T_*)\rVert_2\ge c_*\rho\). |
| 平面不变子空间 | planar invariant subsystem | \(\mathcal S_{2D}\), where every constructed trajectory remains exactly two-dimensional and globally smooth. |
| family-level theorem | family-level theorem | The background depends on \(\Lambda\) and has amplitude of order \(\Lambda\); this is not one fixed-background Lyapunov theorem. |
| 有限无黏作用量代理 | finite inviscid action proxy | \(A_{N,0}\), computed at finite cutoff and kept distinct from \(\mathcal A_*\). |
| 有限 prescribed-action 前因子 | finite prescribed-action prefactor | \(g^{(0)}_{N,\varepsilon}=G_{N,\varepsilon}e^{-A_{N,0}/\varepsilon}\); it is a finite binary64 diagnostic. |
| 独立线性哨兵 | independent linear sentinel | One of five midpoint matrix-exponential reconstructions that do not import the primary producer. |
| 独立层级哨兵 | independent hierarchy sentinel | One of three scalar-vorticity, alias-free FFT reconstructions through cubic order. |
| bounded-search gap | bounded-search gap | No checked source contains every registered feature simultaneously; this is not an absolute novelty or priority claim. |
| 固定背景可行性与障碍审计 | Feasibility and obstruction audit for fixed-background Lyapunov instability | R0.73N tests whether the family-level theorem can be converted to a fixed-base theorem; closure is not presupposed. |

## Evidence-state vocabulary

| Token | Meaning |
|---|---|
| `CLOSED` | A continuum proof obligation is closed by analytic estimates. |
| `PASS` | A finite validator, independent reconstruction, audit, or publication gate passed its frozen checks. |
| `TRUE` | A machine-readable finite or publication fact is true. |
| `FALSE` | A machine-readable claim is explicitly not certified. |
| `OPEN` | No proof is claimed in this release. |
| `NOT CLAY` | The result does not solve or partially certify the Clay regularity problem. |

The exact continuum ledger is:

```text
physicalKineticSelectedGainConjugacy=CLOSED
fixedEndpointBackwardLocalization=CLOSED
prescribedActionSeedWindow=CLOSED
twoDimensionalNonlinearDeparture=CLOSED
fixedDistanceEndpoint=CLOSED
selectedPlanarOrbitGlobalSmoothness=CLOSED
```

The exact finite/publication ledger is:

```text
finiteDiagnosticPackage=CLOSED
primaryPrescribedActionCases=15
independentLinearSentinels=5
independentHierarchySentinels=3
formalFigurePackage=PASS
finiteDimensionDoesNotCertifyContinuum=TRUE
```

The exact open ledger is:

```text
prefactorLimit=OPEN
twoTermWKB=OPEN
singleFixedBackgroundLyapunovInstability=OPEN
transverseThreeDimensionalClosure=OPEN
finiteTimeSingularity=OPEN
Clay=OPEN
```

Do not translate `CLOSED` as a numerical observation or `PASS` as a
continuum theorem. Keep `NOT CLAY` verbatim.

## Numerical and figure language

- Say “15 finite primary cases”, “1,170 action rows”, “five independent
  linear sentinels”, “three independent hierarchy sentinels”, and “28/28
  validator checks”.
- Say the finite prefactor lies in
  \([0.9960745296895327,0.9965850277770183]\).
- Do not call finite cutoff agreement a Fourier-tail proof.
- Do not call \(A_{N,0}\) the continuum action \(\mathcal A_*\).
- Do not call the five-\(\varepsilon\) coefficient trend a limit or WKB theorem.
- The formal figure ID is `fig-r073m-prescribed-action-departure`.
- Its archive has exactly 25 files, including
  `chart-contract-and-source-data.md`; `source-data.csv` has 27 rows.
- PDF/SVG/600 dpi PNG are synchronized masters. Figure validation does not
  certify the continuum theorem.

## Literature boundary

The public literature paragraph may compare the result with autonomous
spectral-to-nonlinear instability, Grenier corrector schemes, boundary-layer
instability, exact unforced near-Couette transient amplification, all-time
Rayleigh-stable heat flows, viscosity-driven spectral transition,
Kolmogorov-flow metastability, and slowly varying finite-amplitude response.

For Li–Masmoudi–Zhao, retain the exact bibliographic record:
*Communications on Pure and Applied Mathematics* 77 (2024), 2863–2946,
DOI `10.1002/cpa.22183`.

Admissible wording is “no single checked source in the recorded bounded
search contains all registered features.” Do not write “first”, “novel”,
“unprecedented”, or any absolute absence or priority claim.

## Public-voice and theorem boundary

Reader-facing text uses the individual-researcher voice. It must not imply a
collective program or machine authorship. The strongest admissible summary
is:

> For the sealed periodic two-harmonic background family, a perturbation
> prescribed by the full inviscid action reaches a fixed selected-pair
> distance at a fixed physical time inside an exactly invariant planar
> subsystem.

Every public summary must also say that the background varies with
\(\Lambda\), planar global smoothness does not control transverse 3D
perturbations, and fixed-background Lyapunov instability, finite-time
singularity, and Clay remain OPEN.

## Synchronized PDF titles

```text
R0.73M｜Prescribed-action planar nonlinear departure
R0.61–R0.73M｜R0.60 之后的研究回顾
```

The PDF binding manifest checks exact title metadata, byte counts, and
SHA-256 hashes; it does not certify mathematical correctness.
