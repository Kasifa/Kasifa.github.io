# R0.70T independent mathematical audit

**Verdict:** **PASS** for the locked snapshot below.  No mathematical,
claim-scope, citation, or certificate blocker remains.  One reproducibility
minor remains: the focused test and archived command use an ignored local
Python environment under `tmp/r068b-venv`; a clean checkout must recreate an
equivalent Python 3.12.13 / SymPy 1.14.0 environment before running them.

This verdict is deliberately narrow.  R0.70T proves an exact stretching
ledger, an orientation-free covariance-divergence decomposition, and a sharp
pointwise bound for the longitudinal defect.  It does **not** control that
defect, the stretching commutator, or enstrophy by lower-order data.  It is not
a Navier--Stokes closure, a singularity result, a global-regularity theorem,
or a solution of the Millennium problem.

## 1. Locked snapshot

I audited the report at base commit
`5f4a75787900223c2fd2756ef4a8d9c54e774a62` on branch
`codex/r070t-stretching-divergence`.

The final files and SHA-256 digests are:

- `research/r070t_report-source.md`:
  `5565abbc696466b06cf937de3c1f2380cab287b6972ffde803fa20a83f1adc1b`;
- `research/r070t_exact_audit.py`:
  `3a1ea50b5d4bcfce44611733a1e74e778ec39320d633b0bdf4cafcd48dd96b0e`;
- `tests/r070t-frame-stretching-gate.test.mjs`:
  `1f423157762c81e1e37f9ea6854d2542475c341ff0f7c9e7e182c473f33c6af1`;
- `research/certificates/r070t/README.md`:
  `6646d54c53975ba0af6ea67800a4cd64a6caa9f179b97b1476625280db6f76ce`;
- `research/certificates/r070t/result.json`:
  `29b9dab63dda29ab46c6a7260163b893d3090d0a9d1245fd30d6fb34edfaf582`;
- `research/certificates/r070t/SHA256SUMS`:
  `61955b4226bdab26758e89f7fdcb0dda789c579a6df319f95ebe4ee0a70e488d`;
- `research/certificates/r070t/command.txt`:
  `6710d2aa7d6dcdd2b9004fa9652653932670fd57664eea943c591f9b4db5e399`;
- `research/certificates/r070t/environment.txt`:
  `66e725ae73b7915dbfe47076d25cea9a5471afcb89d76383a54efb6c0652884b`.

The producer and certificate were refined during this audit to state
explicitly that the direct machine anchor is \(M=16\), whereas the dyadic
\(M=2^m\) family and \(M\to\infty\) limit are analytic calculations in the
report.  The hashes above supersede the earlier producer/result hashes
`cf6d6f32...` and `db864ef0...` supplied before that scope repair.

Running `shasum -a 256 -c SHA256SUMS` inside the certificate directory gives
five successes:

```text
README.md: OK
command.txt: OK
environment.txt: OK
result.json: OK
../../r070t_exact_audit.py: OK
```

Regenerating `result.json` into a temporary path gives a byte-identical file
with SHA-256
`29b9dab63dda29ab46c6a7260163b893d3090d0a9d1245fd30d6fb34edfaf582`.
The manifest locks the five certificate payloads; this audit separately
records the report and test hashes above.

## 2. Test and build record

The final snapshot passed the following checks.

| Check | Result | Boundary |
|---|---:|---|
| Focused R0.70T Node gate | 7/7 PASS | Reproduces the five-group producer, checks scope tokens, and verifies all five archived SHA entries |
| Full Node suite | 647/647 PASS | The recorded release run was 16.4 s; independent pinned-environment reruns took 16.84 s and 15.08 s |
| Direct i18n build | PASS | `pages=105`, `translations=9855`, `staleTranslations=41` |
| Direct vinext build | PASS | All five build stages completed |
| Producer regeneration | PASS | Temporary output is byte-identical to the archived JSON |

The full suite was run with `tmp/r068b-venv/bin` first on `PATH`, because
older tests invoke `python3` by name and require the repository's scientific
Python environment.  This is an execution-environment requirement, not an
R0.70T mathematical failure.

I compared `git status --porcelain=v1` before and after the direct i18n and
vinext builds.  The status was unchanged: the builds introduced no additional
tracked or untracked workspace change.  The i18n stale count is an existing
dictionary-maintenance statistic, not a missing R0.70T translation; R0.70T is
still an internal report with no authorized public page.  Vinext emitted its
usual static route-classification warning, but all five stages passed.

## 3. Complete-frame stretching ledger

For the exact scalar Parseval frame

\[
 \sum_\alpha T_\alpha^2=I,
 \qquad \Omega_\alpha=T_\alpha\omega,
 \qquad Q=\sum_\alpha\Omega_\alpha\otimes\Omega_\alpha,
\]

and the commutator convention

\[
 [T_\alpha,S]\omega
 =T_\alpha(S\omega)-S\Omega_\alpha,
\]

self-adjoint tightness gives

\[
 \int\omega\cdot S\omega
 =\int S:Q
  +\sum_\alpha
   \langle\Omega_\alpha,[T_\alpha,S]\omega\rangle.
\]

The plus sign is correct.  The finite machine model is deliberately
noncommuting: its covariance and commutator contributions are respectively
\(626/65\) and \(24/65\ne0\), summing to the left side \(10\).  This is a
genuine sign check rather than a zero-commutator example.

The periodic product-rule sample independently fixes the tensor convention

\[
 B_{ij}=\partial_i u_j,
 \qquad
 (\operatorname{div}Q)_j=\partial_iQ_{ij}.
\]

The producer derives a nonzero normalized value

\[
 \int S:Q=\int B:Q
 =-\int u\cdot\operatorname{div}Q=2.
\]

Thus neither the commutator sign nor the integration-by-parts sign is hidden
by a vanishing test case.

The machine examples do not prove the countable Fourier-frame identity.
Countable Parseval convergence, sum/integral interchange, the constant block,
and the general regularity extension remain analytic lemmas, as the report and
certificate state.

## 4. Amplitude cancellation and the sharp constant

On a local simple-top patch, write

\[
 Q=\lambda L+H,
 \qquad L=\ell\otimes\ell,
 \qquad P=I-L,
\]

\[
 \Omega_\alpha=a_\alpha\ell+b_\alpha,
 \qquad b_\alpha=P\Omega_\alpha.
\]

The spectral premise is independently retained as

\[
 PQ\ell=\sum_\alpha a_\alpha b_\alpha=0.
\]

It is not obtained by defining both sides to vanish.  For

\[
 c_\alpha
 =\ell\cdot\nabla a_\alpha
  +a_\alpha\operatorname{div}\ell
  +\operatorname{div}b_\alpha,
\]

the producer proves the polynomial identity

\[
 \mathcal A_{\parallel}
 +2\sum_\alpha a_\alpha\operatorname{div}b_\alpha
 =2\sum_\alpha a_\alpha c_\alpha.
\]

Only after imposing the actual divergence-free block premises
\(c_\alpha=0\) does this give

\[
 \mathcal A_L
 =L(\nabla\lambda+2\lambda\operatorname{div}L)
 =-2\ell\sum_\alpha
   a_\alpha\operatorname{div}(P\Omega_\alpha).
\]

The orientation flip is checked, and the final vector is independent of the
local choice \(\ell\mapsto-\ell\).  The coefficient bound follows from the
exact Lagrange identity

\[
 \lambda\mathcal J_P
 -\left(\sum_\alpha a_\alpha d_\alpha\right)^2
 =\sum_{\alpha<\beta}
  (a_\alpha d_\beta-a_\beta d_\alpha)^2,
 \qquad
 d_\alpha=\operatorname{div}(P\Omega_\alpha),
\]

and therefore

\[
 |\mathcal A_L|\leq2\sqrt{\lambda\mathcal J_P}.
\]

The equality witness is nonzero and exact.  General smooth eigenprojector
calculus, orientation patching, and the reduced-resolvent identities in
Section 6 remain analytic rather than machine-proved.

## 5. Fixed-frame shear witness

The certificate differentiates the report's actual streamfunction field.  At
\(M=16\), it uses

\[
 u_M^0=M^{-1}(0,0,\psi_L+\psi_H),
\]

\[
 \psi_L=\frac M5\sin(5x_2)
 +\frac M{24}
  [\cos(3x_1+4x_2)-\cos(3x_1-4x_2)],
\]

\[
 \psi_H=-\frac1{5M}\sin(5Mx_1)
 +\frac1{25}\cos(5Mx_2).
\]

Direct symbolic differentiation verifies the complete curl relation,
velocity and vorticity divergence, zero vorticity mean, and

\[
 (\Delta+25)\omega_L=0,
 \qquad
 (\Delta+6400)\omega_H=0.
\]

Hence

\[
 u_M(t)=e^{\nu t\Delta}u_M^0
\]

is an exact smooth global unforced periodic Navier--Stokes solution: it is
independent of \(x_3\), points in the \(e_3\) direction, and satisfies

\[
 (u_M\cdot\nabla)u_M=0,
 \qquad S\omega_M=0.
\]

The last identity is important for scope.  The sample proves a sharp local
defect boundary but is not a nonzero vortex-stretching example and cannot by
itself obstruct a signed enstrophy closure.

### Fixed multiplier boundary

All low modes have radius \(5\), and all high modes have radius \(80\).  The
strict support condition gives only

\[
 \varnothing\ne I_5\subseteq\{2,3\},
 \qquad
 I_{80}=I_5+4\subseteq\{6,7\}.
\]

The report, README, JSON, and test all avoid claiming that both possible
indices are active.  Radiality, real-evenness, dyadic response shift, and
exact square tightness give the analytic premise

\[
 \rho^2+\sigma^2=1,
 \qquad
 \rho=\varphi(5/4),
 \quad
 \sigma=\varphi(5/8).
\]

The producer does not numerically invent values for \(\rho\) or \(\sigma\).
It retains them symbolically and checks

\[
 Q_{\mathrm{frame}}-Q_{\mathrm{target}}
 =(\rho^2+\sigma^2-1)Q_{\mathrm{target}}.
\]

Thus the finite algebra is conditional on the stated pinned-frame theorem,
exactly as advertised.

### Sharp point and derivative price

At \(x=t=0\), the direct calculation gives

\[
 Q=\operatorname{diag}(1,1/256,0),
 \qquad
 \partial_1Q=\operatorname{diag}(-2,0,0),
 \qquad
 \partial_2Q=\partial_3Q=0.
\]

The full first-order projector and projected-block product rules, including
\(\partial_iP\), then give

\[
 \nabla L=0,
 \qquad
 \mathcal J_P=1,
 \qquad
 \mathcal A_L=-2e_1,
\]

\[
 E=\frac{257}{256},
 \qquad
 r=\frac1{256},
 \qquad
 \frac rE=\frac1{257},
 \qquad
 \frac{\lambda_1-\lambda_2}{E}=\frac{255}{257}.
\]

The frame-gradient density is also independently accumulated from the four
symbolic response blocks:

\[
 \mathcal G
 =258(\rho^2+\sigma^2)=258.
\]

Therefore

\[
 |\mathcal A_L|=2=2\sqrt{\lambda\mathcal J_P}.
\]

This closes the possibility that the common-origin radial tight-frame
constraint alone improves the coefficient (2).

The machine check stops at \(M=16\).  The report's formulas for arbitrary
dyadic \(M=2^m\) prove analytically that

\[
 \frac rE(x_0)=\frac1{M^2+1}\longrightarrow0,
 \qquad
 \mathcal G(x_0)=M^2+2.
\]

The revised README and JSON list this general-(M) passage as an analytic
dependency.  The obstruction is pointwise at the initial time; it is not a
uniform near-rank statement, does not propagate under heat flow, and does not
exclude estimates retaining palinstrophy, \(\mathcal J_P\), or a higher
Sobolev norm.

## 6. Rank-one and signed boundaries

The isolated-rank machine jet has

\[
 Q(0)=2e_1\otimes e_1,
 \qquad
 \nabla Q(0)=\nabla L(0)=0,
\]

but

\[
 \operatorname{div}(P\Omega_1)(0)=1,
 \qquad
 \operatorname{div}(P\Omega_2)(0)=-1.
\]

Consequently

\[
 \mathcal A_L(0)=0,
 \qquad
 \mathcal J_P(0)=2.
\]

This correctly distinguishes an isolated rank-one point from rank one on an
open neighbourhood, where every \(P\Omega_\alpha\) vanishes as a field and
therefore \(\mathcal J_P=0\).

The report also records the exact signed reassembly

\[
 \int S:H+\mathfrak E_S
 =\mathscr P-\int S:(\lambda L),
\]

\[
 \mathfrak R_{\mathrm{sgn}}
 =\mathscr P
  +\int \lambda u_*\cdot
    (I-2L)\operatorname{div}L.
\]

This is explicitly labelled a tautological reassembly, not a new estimate.
It shows why the \(\mathcal A_L\) term is a derivative channel in the
absolute-value ledger but not an independent signed obstruction.  The
certificate does not promote the sharp positive bound into a signed closure.

## 7. Machine versus analytic proof boundary

The machine producer directly checks only:

1. a finite noncommuting Parseval sign model;
2. one nonzero periodic row-gradient and integration-by-parts sample;
3. finite coordinate-gauge covariance algebra, the cancellation polynomial
   modulo explicit divergence constraints, and an exact SOS equality witness;
4. the displayed \(M=16\) Fourier shear, its heat/NSE residuals, and its
   conditional symbolic frame response at one point;
5. one isolated exact-rank block jet.

The following remain analytic dependencies:

- the countable complete-frame Parseval theorem, convergence, and exchange of
  sums and integrals;
- strict support, radial real-even response, exact square partition, and
  derivative commutation for the pinned multiplier family;
- the general dyadic \(M=2^m\) family and \(M\to\infty\) limit;
- smooth simple-eigenvalue projector calculus and orientation patching;
- general periodic integration by parts at the stated regularity;
- the reduced inverse \(\mathcal R_Q\), half-curvature normalization
  \(\mathcal K_Q\), and the derivative ledger (6.7);
- the global simple-top hypotheses required by Sections 5, 8, and 10;
- the standard periodic \(H^1\) blow-up alternative and every continuation or
  PDE-closure implication.

The producer's five top-level `checks` booleans are emitted only after exact
`require` statements have evaluated the independently formed residuals.  The
important conclusions are not justified merely by hard-coded payload labels.
The focused Node test also reruns the producer and compares the regenerated
JSON with the archive.

## 8. Literature and novelty boundary

The report places the calculation next to primary work on physical-vorticity
direction coherence, geometric depletion, multiscale criteria, and variable
planes: Constantin--Fefferman, Beirao da Veiga--Berselli,
Ruzmaikina--Grujic, Zhou, Grujic, Chae, Bradshaw--Grujic,
Cheskidov--Dai, Vasseur, Miller, and Neustupa--Penel.

The novelty language is appropriately limited:

- the Parseval commutator split is called a standard harmonic-analysis
  ledger;
- the reflection identity is called elementary tensor algebra;
- the amplitude identity is called a direct divergence-free block
  consequence;
- the report makes no priority claim for those identities;
- the project-specific contribution is limited to their fixed-frame
  packaging, residual-divergence ledger, and explicit sharp common-origin
  periodic witness.

This audit does not certify an exhaustive literature search or publication
novelty.  The report itself correctly states that a publishable advance would
require a genuinely new PDE estimate for \(\mathcal J_P\),
\(\mathfrak C_S\), or their signed interaction.

## 9. Findings by severity

### Blocker

None.

### Major

None.

### Minor

1. The reproducibility command and focused test depend on the ignored local
   path `tmp/r068b-venv/bin/python`.  The environment file records Python and
   SymPy versions, and the current checkout reproduces byte-exact output, but
   a clean checkout needs an explicit environment-recreation step.

The i18n stale count and vinext route-classification warning are unrelated
site-maintenance observations, not R0.70T defects.

## 10. Final boundary

R0.70T is a rigorous structural release with a sharp fixed-frame pointwise
witness.  Its meaningful negative result is narrow: common block origin and
pointwise near rank do not improve the coefficient in

\[
 |\mathcal A_L|\leq2\sqrt{\lambda\mathcal J_P}.
\]

It supplies no a priori estimate for \(\mathcal J_P\), the stretching
commutator, the signed remainder, or enstrophy.  The Section 8 continuation
statement is conditional on a global simple top and an integrable majorant;
those hypotheses are not derived from initial enstrophy, Leray energy, or the
certificate.  No Navier--Stokes regularity problem is closed.
