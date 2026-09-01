# R0.74I — final full-source rebind audit

**Audit date:** 2026-09-02
**Verdict:** `FINAL_SOURCE_REBIND_PASS`
**Blocking findings:** none

This is the post-promotion independent audit of the complete R0.74I release
source.  It binds the final manuscript, evidence matrix, literature records,
finite certificate, bilingual boundary, and sealed figure package.  The
earlier conditional audits remain historical derivation records.  The
literature audit received a format-only cleanup described below; its semantic
content and pre-repair snapshot claims are unchanged.  This audit checks that
every requested repair is present in the final source.

The verdict is deliberately narrow.  It certifies the consistency of the
stated suitable-weak Version-M theorem, the one-scale moving-energy epsilon
bridge, the logarithmic obstruction along the frozen packet family, and the
release evidence.  It does not certify novelty, priority, payment smallness at
a possible singular point, scale propagation, Version-F weak closure, an
endpoint logarithmic upper bound, global regularity, or the Millennium
problem.  **NOT CLAY.**

---

## 1. Final byte binding

All digests below were recomputed directly from the files during this audit.

| Artifact | SHA-256 |
|---|---|
| `research/r074i_suitable_weak_tube_and_log_obstruction.md` | `70ff507704c6c7aed5ea8bc0250a96373113975e8e3f92edd53e3193d7cd8457` |
| `research/r074i_gap_matrix.md` | `78cb76beb542bdd2e836d7f357838d0d11518bd989bf9c396443dde27a840374` |
| `research/r074i_report-source.md` | `4b2b48a45e2606ddc534d92ee1032b36d9d1b5d7169640d9311b3521d779c57e` |
| `research/r074i_primary_literature_boundary.md` | `8790ffa0de714d925569ee5de444188b970b306c35f4027aad5761b62f122b55` |
| `research/r074i_primary_literature_independent_audit.md` | `83f0e1aa746ddd1164f67517b5a60c2547940ea2ab92f43d537ad8875ca20b3a` |
| `research/r074i_weak_extension_independent_audit.md` | `68b3e02ab836106c1598ce8aa32017f83ad3f527e7b1a4aaa8f735851e6fccc1` |
| `research/r074i_epsilon_log_independent_audit.md` | `a59ff3f27a9e5322aecd5ac057458af0e508c62421f77082a4509fcd822791df` |
| `research/r074i_bilingual_dictionary.md` | `3acff1d10887d8c07b9389137bfdbfca1331915ffb3b81870554dcff2c27d530` |
| `scripts/r074i_tube_log_certificate.py` | `5411134949eedbb1c285607c33a4f8feb9f8d358f5fc7cee91ec3601dfe3932f` |
| `research/r074i_tube_log_certificate.json` | `d4d0f32f6772bdae8a9ec0e8fd6f5f5f9248877df3c19bf544c3577055ab7bf5` |
| `research/r074i_tube_log_certificate_report.md` | `3be483123d3841a7f195a192374d56bb9ef453fe3ba2ee59ed6dc2e4fa68b0bf` |
| `scripts/r074i_tube_log_certificate_independent.rb` | `2c591dac16bce3ea456070775ac9c68408f0b32fb1492cd039b6e7d52f0040ad` |
| `research/r074i_certificate_independent_audit.md` | `a70cc641338b2e58aafce8cfe6ddadb08b05d9f35494b5d92f12bea9c8152c59` |
| figure `SHA256SUMS` | `23c0646faf34bfd545db7326bfe7828fc1377875f0238c99f028ae85041b981a` |
| figure `manifest.json` | `b52c3558755ca35135cc7665c83d66ca7da544411a7049a8c2d8a8c41c9fb35d` |
| figure `validation.json` | `b9e704a67eb7421ca2093791a40fdd1645f8fdbb890573af5260578ebcbe0dc5` |
| figure `plot.py` | `be212c485d9b1d3b2b1bd01c1c232fb120533d2db765fa7f7f75956f1d674f59` |
| figure `figure.svg` | `0ae2e2f2af20704705c711a7c3773373541794f326dfa881f3927a5416927bc3` |
| figure `figure.pdf` | `83a2dbd23130da9a4018aa06c13bc1b0d38a2fb91c27cd985f5790de8a7ab4f1` |
| figure `figure.png` | `cf4680d3249829fd193af1f94d93c0cc750bc41b29bfdf944180785f7ff3f5d0` |

The gap matrix is correctly rebound to the final analytic source digest
`70ff5077...8457`.  No checked text artifact contains an unexpected control
character, and the reader-facing source contains none of the project's
discouraged collective or promotional phrases.
Every figure-package text artifact satisfies the canonical EOF policy: LF
line endings, exactly one terminal line feed, and no blank line at EOF.

---

## 2. Full analytic audit of Sections 1--4

### 2.1 Suitable-weak representative and terminal trajectory

The energy-class assumptions imply, on the finite periodic cylinder,

\[
 u\in L_t^\infty L_x^2\cap L_t^2H_x^1
 \quad\Longrightarrow\quad
 u\in L^{10/3}_{t,x}\subset L^3_{t,x}.
\]

Spatial convolution with the frozen mollifier gives the stated bounds

\[
 \|u_R(t)\|_\infty\lesssim R^{-3/2}\|u(t)\|_2,
 \qquad
 \|\nabla u_R(t)\|_\infty\lesssim R^{-5/2}\|u(t)\|_2.
\]

After choosing a jointly measurable representative, the time-dependent
vector field is Borel, uniformly bounded at fixed \(R\), and spatially
Lipschitz with an essentially bounded coefficient.  Backward application of
the Caratheodory theorem therefore gives the unique absolutely continuous
terminal path.  Its fixed Euclidean lift belongs to \(W^{1,\infty}\), and
periodicity makes different lifts equivalent on the torus.  No temporal
differentiability of the weak velocity is used.

**Decision:** PASS.

### 2.2 Moving local-energy test, signs, and weak passage

For finite \(N\), smooth Euclidean path approximants may be chosen with
uniform convergence of the paths and \(L^1_t\) convergence of their
derivatives.  Composition with the fixed smooth periodic weight therefore
gives

- uniform convergence of the tests, gradients, and Laplacians; and
- \(L^1_tL_x^\infty\) convergence of the time derivatives.

These are exactly the topologies needed for the local-energy terms.  The time
derivative is

\[
 \partial_t\phi_N
 =\eta_R'\Theta_{R,N}
  -\eta_Ra_R\cdot\nabla\Theta_{R,N}.
\]

The integrability ledger

\[
 |u|^2\in L_t^\infty L_x^1,
 \quad |\nabla u|^2\in L^1,
 \quad |u|^3\in L^1,
 \quad pu\in L^1
\]

licenses every limit.  Substitution in the half-normalized local energy
inequality gives the kinetic row

\[
 \frac12|v_R|^2(v_R-a_R)\cdot\nabla\Theta_{R,N},
\]

with the correct minus sign on \(a_R\), factor \(1/2\), terminal factor
\(1/(2R)\), and dissipation/flux factor \(1/R\).  The final manuscript now
writes the pressure gauge as the time-dependent scalar
\(c_{2R}^{M,R}(t)\).  Its contribution vanishes distributionally by
incompressibility.

The \(N\to\infty\) passage is licensed by the frozen super-Gaussian \(C^2\)
majorant.  The final Lemma 2.2 identifies R0.74H (4.4)--(4.8) for the
quadratic cutoff and R0.74H (6.3)--(6.6) for the Version-M absolute flux.  At
the weak regularity level:

- local and shell cubic rows use the energy and exterior \(L^3\) ledger;
- the residual drift uses
  \(a_R=(\varphi_R*v_R)(0)\), Jensen, and Young;
- the local pressure uses the distributional pressure split and
  Calderon--Zygmund; and
- the harmonic pressure uses distributional harmonicity and interior
  harmonic estimates.

No derivative of \(u\), \(a_R\), or \(p\) in time is hidden in these bounds.
The essential-supremum exterior energy follows at good terminal times.  The
full \(I_R\) dissipation follows separately from good times
\(\tau_k\uparrow t_0\), dropping the nonnegative terminal energy and using
monotone convergence.  Hence

\[
 X_R^M\lesssim(P_R^M)^{2/3}+P_R^M,
 \qquad
 P_R^M\le1\Longrightarrow X_R^M\lesssim(P_R^M)^{2/3}.
\]

**Decision:** PASS for Version M only.

### 2.3 Moving-to-fixed epsilon bridge

The mollifier support and the moving energy give, almost everywhere,

\[
 |a_R(t)|
 \le \|\varphi_R\|_2
       \left(\int_{B_R}|v_R|^2\right)^{1/2}
 \lesssim R^{-1}\mathcal E_R^{1/2}.
\]

Integration over the exact interval length
\(|I_{R/2}|=R^2/4\) yields

\[
 |X_R(t)-x_0|\lesssim \frac14R\mathcal E_R^{1/2}.
\]

The final text explicitly reads distances and balls in the anchored Euclidean
lift.  Small moving energy therefore gives

\[
 B_{R/2}(x_0)\subset X_R(t)+B_R
 \quad(t\in I_{R/2}).
\]

Guevara--Phuc's fixed-cylinder interpolation, applied purely functionally to
\(v_R\) with outer radius \(8R\) and inner radius \(R\), has the correct two
terms and gives

\[
 R^{-2}\int_{I_R}\int_{B_R}|v_R|^3
 \lesssim A(8R)^{3/4}E(8R)^{3/4}+A(8R)^{3/2}
 \lesssim\mathcal E_R^{3/2}.
\]

Restriction to the contained half-radius cylinder contributes the exact
factor \((R/2)^{-2}=4R^{-2}\), absorbed into the universal constant.  With
\(r=R/2\), the final source now records the complete Navier--Stokes scaling

\[
 U(s,\xi)=r u(t_0+r^2s,x_0+r\xi),
 \qquad
 \Pi(s,\xi)=r^2p(t_0+r^2s,x_0+r\xi),
\]

which preserves suitability and satisfies

\[
 \int_{Q_1}|U|^3
 =r^{-2}\int_{Q_r(z_0)}|u|^3.
\]

Wang--Wu--Zhou Theorem 1.1 applies with \(\delta=1/2\), so the exponent is
exactly \(3\) and there is no pressure-smallness hypothesis.  The threshold

\[
 \varepsilon_{\rm tube}
 \le\min\{\varepsilon_{\rm geom},
 (\varepsilon_{L^3}/C_I)^{2/3}\}
\]

therefore implies regularity at \(z_0\).  Finally,
\(\mathcal E_R^{3/2}\le P_R^M\) gives the small-\(P_R^M\) corollary with
\(\varepsilon_P\le\varepsilon_{\rm tube}^{3/2}\).

**Decision:** PASS as a one-scale conditional regularity gate.  It does not
produce the required smallness.

### 2.4 Logarithmic window, obstruction, endpoint, and lacunarity

For the exact frozen family,

\[
 R_j=e^{-\rho L_j^2},\quad \rho=1/320,
 \quad b_j=B_jR_j^2\to1/128,
\]

and the inherited bounds are used in the correct directions:

\[
 P_j\le AB_j^3R_j^3,
 \quad P_j\ge a_PB_j^2L_jR_j^2,
 \quad Y_j\ge a_YB_j^2L_jR_j^2,
 \quad Y_j\in\{X_j,\mathfrak C_j\}.
\]

The eventual bounds \(1/256\le b_j\le1/64\) are valid.  Substitution of
\(B_j=b_jR_j^{-2}\) gives the exact exponential scales and hence

\[
 2\rho\le\liminf\frac{\log P_j}{L_j^2}
 \le\limsup\frac{\log P_j}{L_j^2}\le3\rho.
\]

The final source consistently uses
\(\log_+p=\log\max\{p,1\}\), including \(p=0\), and states
\(\Phi:[0,\infty)\to[0,\infty)\) and \(K>0\).  The payment upper bound gives

\[
 P_j^{2/3}\sqrt{1+\log_+P_j}
 \lesssim B_j^2L_jR_j^2,
\]

so the target lower bound yields the positive liminf.  Since \(P_j\to\infty\),
every fixed \(\gamma<1/2\) leaves the divergent factor
\((1+\log_+P_j)^{1/2-\gamma}\).  The M/F labels are explicit and valid because
the two versions coincide on the exact family.

At \(\gamma=1/2\), the ratio is only bounded below away from zero.  The final
text correctly treats the endpoint as open.  Assuming an endpoint upper bound
and comparing it with the target lower bound gives

\[
 B_j^2L_jR_j^2\lesssim K L_jP_j^{2/3}
 \quad\Longrightarrow\quad
 P_j\gtrsim K^{-3/2}B_j^3R_j^3.
\]

This is explicitly labeled a conditional implication, not a proved family
lower bound.  Finally, \(L_{j+1}=2L_j\) and the lower/upper payment bounds give

\[
 \log(P_{j+1}/P_j)
 \ge5\rho L_j^2+\log L_{j+1}+O(1)\to\infty.
\]

Thus the lacunarity claim is proved, and the manuscript correctly refuses to
interpolate a pointwise bound between the realized \(P_j\).

**Decision:** PASS.

---

## 3. Repair closure against the historical pre-audits

### 3.1 Weak-extension audit

The weak-extension audit is an immutable derivation record.  Its final pass
was bound to an earlier manuscript SHA.  The present source retains all of its
required repairs: the measurable representative, Euclidean lift, exact path
approximation topology, termwise integrability, time-dependent pressure
gauge, weak payment inputs, and separate good-time closures for exterior
energy and dissipation.  The additional exact R0.74H equation references and
explicit local/shell/residual rows strengthen the final linkage.

### 3.2 Epsilon/log adversarial pre-audit

The pre-audit was conditional on four repairs.  All four are present:

1. every generic logarithmic expression uses \(\log_+\), with a definition
   valid at zero;
2. the endpoint implication is derived in (4.15)--(4.17);
3. lacunarity is derived in (4.18); and
4. Version-M and Version-F labels are explicit in the generic rejected
   inequalities.

The final text also includes the anchored Euclidean-lift clarification and
the complete velocity/pressure rescaling.

### 3.3 Literature audit

The independent literature audit remains the semantic pre-repair snapshot.
After the first rebind, four Markdown trailing double-spaces were removed.
No word, formula, citation, verdict, or claim boundary changed; the final
format-clean digest is
`83f0e1aa746ddd1164f67517b5a60c2547940ea2ab92f43d537ad8875ca20b3a`.
The final report, boundary note, and manuscript incorporate all five requested
repairs:

1. Yang and Vasseur--Yang are identified as direct precedents for mollified,
   reference-time-anchored trajectories, and Vasseur--Yang's one-sided
   backward skewed cylinder is stated explicitly.
2. Chemin's \(N_T(u)\) and
   \(L_t^\infty\dot B^{1/2}_{2,\infty}\) observables, and
   Ogawa--Taniuchi's exponent \(1/\nu-1/\rho\), are distinguished from the
   local R0.74I payment.
3. Montgomery-Smith is described as a global-in-space hypothesis on a finite
   time interval.
4. Tao's published venue, volume, pages, DOI, and arXiv identifier are
   supplied.
5. The reproducibility ledger gives the complete DOI set and the used arXiv
   identifiers.

The source report calls the search a bounded finite non-hit and explicitly
refuses novelty and priority conclusions.  The 2025 direct-title preprint is
screened but excluded as an input; no R0.74I claim depends on it.

**Literature decision:** PASS for source accuracy and the bounded
collision/non-collision boundary only.  This is not a novelty opinion.

---

## 4. Evidence matrix, bilingual boundary, and Sections 5--7

The gap matrix contains 23 claims and correctly separates **PROVED**,
**FINITE**, **OPEN**, and **NOT CLAIMED**.  Its analytic rows agree with
Sections 1--4.  Its open rows retain the actual unresolved gates:

- Version-F suitable-weak closure;
- payment or moving-energy smallness at a possible singular point;
- the square-root-log endpoint upper bound;
- propagation between scale-dependent moving trajectories; and
- sequence-level stability of the cumulative moving flux.

The occurrence of \(\log P_j\) rather than \(\log_+P_j\) in the asymptotic
gap-matrix summary is equivalent on the eventual sequence because the proved
lower bound gives \(P_j\to\infty\); it does not change the claim.

The bilingual dictionary preserves the same boundary in Chinese and English.
It labels the epsilon bridge and small-payment implication as one-scale
conditional results, the endpoint and matching lower bound as open, the
literature comparison as a bounded non-hit, and ordinary translation as
local without DGX.  It forbids novelty, priority, global-regularity, and Clay
wording.

Section 5 accurately separates established components from the R0.74I
combination.  Section 6 states exactly the four analytic conclusions and the
six principal non-conclusions.  Section 7 correctly distinguishes the weak
audit, the repaired epsilon/log pre-audit, finite certificate, literature
boundary, figure package, and this final source rebind.

The promoted status line

```text
FROZEN / INDEPENDENT ANALYTIC PASS /
CERTIFICATE 36/36 + INDEPENDENT 36/36 PASS /
BOUNDED LITERATURE PASS / FIGURE 82/82 PASS
```

is supported by the evidence bound here.  It is immediately followed by the
explicit exclusions and **NOT CLAY** statement.

**Decision:** PASS.

---

## 5. Exact certificate re-execution

The Python producer was re-executed and its standard output compared directly
with the frozen JSON.  The result was byte-identical.  The independent Ruby
program was then re-executed.  It reported:

```text
engine=Ruby Rational independent reconstruction
frozen_json_used_as_arithmetic_input=false
independentPassed=36
independentTotal=36
leafFieldComparisons=269
mismatchCount=0
result=PASS
```

The exact checks cover the cubic Navier--Stokes scaling, half-radius factors,
\(3/2\leftrightarrow2/3\) threshold chain, rational logarithmic window,
lacunarity exponent \(5\rho=1/64\), square-root recovery of one \(L\) power,
and the conditional endpoint exponents.  The report and independent audit
correctly state that none of these finite checks proves the moving local
energy inequality, path confinement, interpolation theorem, epsilon theorem,
packet bounds, or any PDE conclusion.

**Decision:** PASS 36/36 in both implementations, finite arithmetic only.

---

## 6. Figure seal, deterministic validation, and visual inspection

The package

```text
research/figures/r074i/fig-r074i-moving-tube-log-screen/
```

contains 24 files.  Seven text artifacts received EOF-only normalization, and
the plot producer now uses a canonical text writer plus a package-wide EOF
guard.  The SVG, PDF, and PNG bytes did not change.  Every line of the resealed
`SHA256SUMS` was rechecked successfully.  To avoid modifying the sealed
directory, the complete package, certificate, and producer were copied into an
isolated temporary mirror; both `plot.py` and `validate.py` were run there.
They returned

```text
generated fig-r074i-moving-tube-log-screen: 46 text bounds; certificate 36/36 PASS
PASS 82/82; 24 files; all SHA256 entries verified
```

All 24 regenerated files in that mirror were byte-identical to the sealed
originals.  A separate scan confirmed that every Markdown, text, JSON, CSV,
and Python artifact in the package has LF endings and exactly one terminal
line feed.  The unchanged visual digests are those bound above; the new seal,
manifest, validation, and plot-producer digests also agree with the binding
table.

The master PNG, final-size QA raster, grayscale raster, and independently
Poppler-rasterized PDF surface were inspected again.  No clipping, collision,
illegible label, detached arrow, missing marker, weak grayscale distinction,
or color-only semantic distinction was found.  The exact chain in Panel A and
the three logically distinct regions in Panel B remain readable at final
size.  The figure labels \(\gamma<1/2\) as rejected,
\(\gamma=1/2\) as an open endpoint, and \(\gamma>1/2\) as not rejected and not
proved.

The archived outputs have the declared 180 mm by 88 mm surface.  The PDF is a
single vector page with embedded fonts and no raster image XObject.  The PNG
has the declared 600-dpi dimensions and metadata.  The visible footer states
`EXACT DIAGRAM`, `NOT DNS`, `NOT SIMULATION`, and `NOT CLAY`.  No numerical
trajectory, DNS output, empirical sample, or unknown epsilon constant is
plotted.

**Decision:** PASS 82/82, including independent visual inspection.  This is a
formal analytic diagram, not a simulation.

---

## 7. Final verdict and claim boundary

No blocking mathematical, evidentiary, source-binding, certificate, figure,
or status inconsistency was found in the bound release.  The final verdict is

```text
FINAL_SOURCE_REBIND_PASS
```

The frozen R0.74I claim set is therefore limited to:

1. the Version-M suitable-weak two-regime size estimate;
2. the one-scale implication from sufficiently small moving energy, and hence
   sufficiently small Version-M payment, to regularity at the terminal point;
3. the square-root-logarithmic necessary frontier along the exact lacunary
   packet family; and
4. rejection of every fixed logarithmic exponent \(\gamma<1/2\) for the
   stated M/F scalar bounds.

It does not prove that the one-scale hypothesis occurs at a possible singular
point, does not prove the endpoint upper bound, and does not resolve global
regularity.  No novelty or priority claim is certified.  **NOT CLAY.**
