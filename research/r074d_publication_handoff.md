# R0.74D publication handoff — research-side frozen facts

## Handoff status

`READY_FOR_PUBLICATION_TASK / NOT_DEPLOYED`

This document is the research-side handoff for R0.74D.  It does not modify
the website and does not authorize a deployment.  The publication task must
copy the frozen claims and boundaries below without upgrading a bounded
literature non-hit into novelty, or a finite certificate into an analytic
proof.

---

## 1. Frozen provenance

| Evidence layer | Frozen commit | File | SHA-256 |
|---|---|---|---|
| problem gate | `d45c9b931046d0ba87456940448d09f69d1d624f` | `research/r074d_zero_mean_local_transport_gate.md` | `74076d6bdd4c85d77a8b39aa651c6f4dde364c121377fe9a26fd6c1602c33be1` |
| analytic theorem | `ff80370fe33094f1423d312b817dfec0bf42d664` | `research/r074d_zero_mean_local_transport_obstruction.md` | `bc9f7557e27bb86d5730273985b60f7135ccea3adc2fc99b2daf7778e70c9124` |
| independent analytic audit | `f788edee2a35cf539c095fc3463f3ae9b3013518` | `research/r074d_independent_audit.md` | `79c5d64154e6f0bed32d2fb80bb3bdd0f34844e9edfe6206a82a3cfc16ad77b7` |
| primary-literature collision audit | `1f88f6aa77a900321b418e121cdfd8b467a6fc23` | `research/r074d_primary_literature_audit.md` | `3d048a0e54049d31c80f63f22ed9a777d63cabafe909eb084d1bea6406eddfb4` |
| finite-certificate layer | `1a8568fb34dc2ae42f908e4d45d7210db699d83d` | files listed below | hashes listed below |
| independent finite-certificate audit | `4a318f8f78450dad262e97f6d102f3e21768cf40` | `research/r074d_finite_certificate_independent_audit.md` | `62bafb7c6fe5941e1122fa95d816bc5fde3a782f404a9636234f0fcec44c212a` |
| journal-figure package | `df0ede7d718004ba6cfd7a2740e2408f9a53d1ab` | `research/figures/r074d/fig-r074d-zero-mean-local-transport-obstruction/` | `SHA256SUMS` file: `f87eeeec61e798f7f9ca87b1fc601a3d6b25a3e119b68a8a1cfbfc652932a9a1` |

The certificate commit contains:

| File | SHA-256 |
|---|---|
| `scripts/r074d_zero_mean_transport_certificate.py` | `c28b9f80070e67cb36e6f7ed8e80164fe8dd7d944fe4e8d5f3cc824eb764981a` |
| `research/r074d_zero_mean_transport_certificate.json` | `69eecc7884a153bc5d4936c7d3dee9d3c736f5db69c20ba59b486165be96dec9` |
| `research/r074d_zero_mean_transport_certificate_report.md` | `937a5fd73b004f262e970b80ec7e118a39b9e971c39e84ffc988f643be811c1a` |
| `research/r074d_certificate_freeze.json` | `3b96579dc9e3502e779c3154f6cae46f4e9ac40542ce1216ba1fda8a6e8d587c` |

The certificate manifest binds the theorem blob at the theorem commit, not a
later moving `HEAD`.

---

## 2. Publication-safe theorem

For the Version-A quantities frozen in the gate,

\[
 X_R^A=\mathcal U_{\rm ext}^{\infty,A}+\mathcal D_{\rm ext}^A,
 \qquad
 P_R^A=\mathcal E^A(z_0,8R)^{3/2}
       +\mathcal A_{\rm ext}^A(z_0,2R;1),
\]

the analytic theorem and its independent audit prove

\[
 \boxed{
 \sup_{\substack{0<R<\pi/16\\
        (u,p)\ {\rm smooth\ periodic\ NSE}\\
        \overline u=0}}
 \frac{X_R^A}{(P_R^A)^{2/3}}=\infty.}
\]

Here \(z_0=(65R^2,0)\) and \(\nu=\theta=1\).  Thus subtracting only the
constant global spatial mean and translating by that constant mean does not
restore the pure large-payment endpoint tested in R0.74B.

The exact smooth zero-total-mean witness is

\[
 u(t,x)=\bigl(AF(t,x_2,x_3),B_Re^{-t}\cos x_3,0\bigr),
 \qquad p=0,
\]

where

\[
 \partial_tF+B_Re^{-t}\cos x_3\,\partial_2F
 = (\partial_2^2+\partial_3^2)F.
\]

Both velocity components have zero spatial mean.  Therefore the Version-A
global-mean subtraction and translation are exactly the identity on this
family; the obstruction comes from local coherent transport, not a hidden
constant drift.

---

## 3. Exact sequence and simultaneous ledger

Use

\[
 M_m=3\,2^{m-1},\qquad
 R_m=e^{-M_m^2/96},\qquad
 \mathfrak a_m=R_m^{-2}e^{M_m^2/576}.
\]

The target lower bound is

\[
 L_m=c\mathfrak a_m^2M_mR_m^2e^{-M_m^2/288}
 =cM_mR_m^{-2}.
\]

The full payment satisfies

\[
 (P_R^A)^{2/3}\le C\left[
 R^{-2}
 +A^2R^2\Pi_m e^{-M_m^2/264}
 +A^2R^{8/3}M_m^{-4/3}
 \right],
 \qquad \Pi_m=(1+M_m)^{18}.
\]

The three separate ratios are

\[
 \frac{L_m}{R_m^{-2}}=cM_m\to\infty,
\]

\[
 \frac{L_m}{\mathfrak a_m^2R_m^2\Pi_m e^{-M_m^2/264}}
 =\frac{cM_m}{\Pi_m}e^{M_m^2/3168}\to\infty,
\]

and

\[
 \frac{L_m}
 {\mathfrak a_m^2R_m^{8/3}M_m^{-4/3}}
 =cM_m^{7/3}e^{M_m^2/288}\to\infty.
\]

The strict leakage margin is

\[
 \frac1{264}-\frac1{288}=\frac1{3168}>0.
\]

---

## 4. Research value

Publication may state the value in the following narrow form:

1. R0.74D advances the R0.74C fixed-centre obstruction through the route's
   next tested global-mean/Galilean repair: the new witness already has zero
   total mean, so a constant global-mean frame cannot remove its local
   transport.
2. The proof supplies a reusable signed-drift mechanism: a correctly
   time-ordered Feynman--Kac formula gives target survival, while the sign of
   the residual displacement yields one-sided Gaussian leakage; global
   \(L^2/L^3\) contraction pays the opposite side after the invariant
   direction is integrated out.
3. The result eliminates one precisely frozen large-payment endpoint and
   narrows the next useful branch to genuinely local or transport-aware
   architectures.
4. It is a negative positive-scale theorem in a globally smooth invariant
   class.  Its value is diagnostic and structural, not a singularity or
   general-regularity result.

Do not call the witness, the decaying shear equation, Galilean subtraction,
local-flow frames, skewed cylinders, fixed-centre flux payments, or local
pressure splitting new.

---

## 5. Literature attribution that must accompany publication

The literature audit status is

`EXACT_HIT_NOT_LOCATED / DIRECT_COMPONENT_COLLISIONS_FOUND /
BOUNDED_NON_HIT / NOT_NOVELTY_PROOF`.

Required attribution boundaries:

- Biferale--Buzzicotti--Linkmann (2017): the periodic 2D3C/passive-scalar
  invariant class is prior art.
- Coble--He (2024): a time-dependent passive scalar driven by a decaying
  sinusoidal shear is a direct equation-level precedent.
- Cyranka--Zgliczyński (2016): removal of torus mean velocity by Galilean
  transformation is prior art.
- Vasseur (2010) and Choi--Vasseur (2014): mollified trajectories, local
  mean removal, and the fast-flow/fixed-cylinder warning are prior art.
- Yang (2022) and Vasseur--Yang (2021): flow-following/skewed-cylinder
  geometry is prior art.
- Choe--Yang (2018): a fixed cutoff with weighted local-mean subtraction
  and retained convective and pressure fluxes is prior art.
- Wolf (2017): broad local/harmonic pressure decomposition is prior art.

The bounded search did not locate the whole quantitative R0.74D conjunction:
the exact Version-A annular ledger and pressure gauge, its parameter sequence,
all retained payment rows, and the displayed unbounded ratio.  This is a
bounded non-hit only.  It must not be rewritten as “first,” “new,” “original,”
“no equivalent theorem exists,” or a priority claim.

---

## 6. Strict boundary and `NOT CLAY`

R0.74D does not decide:

1. a cylinder following a local or mollified velocity;
2. subtraction of a scale-dependent local spatial mean;
3. a fixed-centre estimate retaining a signed entrance-flux payment;
4. the optimal exponent for a transport-aware large-payment repair;
5. absorption, epsilon regularity, continuation, singularity, or a zero-scale
   regularity theorem.

The witness belongs to a classical globally smooth 2D3C invariant subspace.
The theorem proves no blow-up, no singularity, no epsilon-regularity
criterion, and no global regularity or breakdown result for general
three-dimensional Navier--Stokes solutions.

\[
 \boxed{\text{R0.74D is NOT a solution or partial solution of the Clay
 Millennium problem.}}
\]

---

## 7. Finite-certificate boundary

The deterministic certificate reports

`PASS — 111/111 checks; 109 subject leaves; coverage bijection; zero literal
self-equality checks`.

The independent finite-layer audit reports
`PASS_WITH_EXPLICIT_ANALYTIC_BOUNDARY` and independently confirms the
specified rational arithmetic, all three ratio signatures, the \(m=6\)
admissibility witness, 111 unique IDs, the 109-leaf coverage bijection, zero
literal self-equality checks, and check-only read-only determinism.

It verifies frozen-byte provenance, parameter identities, exponent
comparisons, three ratio signatures, and finite admissibility witness
arithmetic.  It does not certify the stochastic representation, heat-kernel
bounds, one-sided leakage, \(L^p\) contraction, periodic-copy infinite sums,
Calderón--Zygmund/Jensen estimates, any infinite limit, or any Clay claim.
The independent analytic audit, not the finite certificate, is the proof
check for those analytic steps.

---

## 8. Files the publication task must copy

Required research files:

1. `research/r074d_zero_mean_local_transport_gate.md`
2. `research/r074d_zero_mean_local_transport_obstruction.md`
3. `research/r074d_independent_audit.md`
4. `research/r074d_primary_literature_audit.md`
5. `scripts/r074d_zero_mean_transport_certificate.py`
6. `research/r074d_zero_mean_transport_certificate.json`
7. `research/r074d_zero_mean_transport_certificate_report.md`
8. `research/r074d_certificate_freeze.json`
9. `research/r074d_finite_certificate_independent_audit.md`
10. `research/figures/r074d/fig-r074d-zero-mean-local-transport-obstruction/`
11. `research/r074d_publication_handoff.md`

The publication task must preserve the formulas, status labels, prior-art
boundary, finite/analytic separation, and `NOT CLAY` wording.  It must not
publish from an unfrozen working-tree copy when the commit-bound theorem blob
is available.

---

## 9. Frozen journal-figure package

**Directory:**
`research/figures/r074d/fig-r074d-zero-mean-local-transport-obstruction/`

**Frozen commit:**
`df0ede7d718004ba6cfd7a2740e2408f9a53d1ab`

The package contains exactly 25 files.  Key commit-bound hashes are:

| Artifact | SHA-256 |
|---|---|
| `figure.pdf` | `e0c59b15dcdc6024a85cfca487d0eb3dd84a7cba1537a95ae8d4af21812d6886` |
| `figure.png` | `db9e7294a4732f3589032983e99422e73be21d8b19e56130c34f3cffd41909ab` |
| `figure.svg` | `550ca3a71c24e1246bd2ac3ab18bc0b2de5ee429bcec5008464113ab0c4759ec` |
| `manifest.json` | `2238ff94e8e3c6e71314fee44d4d6c0c90f9220371d2392e10f31dc8343e2dac` |
| `SHA256SUMS` | `f87eeeec61e798f7f9ca87b1fc601a3d6b25a3e119b68a8a1cfbfc652932a9a1` |
| `validation.json` | `ea5079912c59e32c7a3a92500ddddaf87fab93f76e97d0c918fa0ef72e2c2026` |
| `qa-report.md` | `663a7fd569eadb09228e2ddb3ba9ac46641746c8910d4c5f678211a58bf046af` |
| `qa-final-size.png` | `c4e2ff6c88bd28fd8ad36f2d9dd4139462666d7d884cc3820e8e8f1855c58925` |
| `qa-grayscale.png` | `39cc72c5259c5a74dc266913ca13f2e47f844f17cb759efa54334612909d4dfc` |
| `qa-pdf.png` | `cc44fe6e51f44fc9e83bc2ec41bfff41beac1f4088dde7d1a32ba6a3f369bb86` |

QA and reproducibility status:

- independent structural validator: `PASS 40/40`;
- two complete generation/validation runs: all `25/25` files byte-identical;
- all 20 text files: no whitespace defects;
- every entry in `SHA256SUMS`: verified;
- PDF: one page, 180 × 82 mm, embedded fonts;
- PNG: 4251 × 1937 RGB pixels, approximately 600 dpi;
- SVG: live text, no raster image, minimum base label size 6 pt;
- grayscale and final-size derivatives: present and legible;
- visual inspection of the master, PDF render, grayscale render, and
  final-size derivative: no clipping or truncated panel content observed;
- the figure visibly preserves `EXACT NSE`, `PROVED`, `OPEN`, `PRIOR ART`,
  `NO DNS`, `NOT CLAY`, all-copy, signed-drift, three-ratio, and no-priority
  boundaries.

This is a deterministic analytic proof schematic.  It is not DNS, a
simulation, an interactive computation, or a numerical proof.

---

## 10. Publication-task state

All research evidence and the journal-figure package are frozen and ready to
be copied by the separate publication task.  No website file was changed and
no deployment was performed here.

`READY_FOR_PUBLICATION_TASK / NOT_DEPLOYED`
