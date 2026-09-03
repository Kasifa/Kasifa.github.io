# R0.74W Step 22 frozen publication handoff

## Release identity and queue order

- release id: R0.74W-Step22
- publication owner: the single long-lived Codex task 发布任务
- publication task id: 01a06480-0532-7fd0-bdf0-57571465a2d4
- logical predecessor: R0.74V-Step21
- queue rule: append once to the existing FIFO queue; do not create another
  publishing task
- frozen research/certificate commit:
  f581c46ee7759c190b6f407633549e7106ff60b5
- frozen figure-archive commit:
  0143d65322a3c854fe220aa9d3e4f93a1f6ca09e
- cumulative recap required: **false**
- formal scientific figure required: **true**

The release is a rigorous result for one frozen exact smooth common-shear
family.  It is not a theorem for arbitrary suitable weak solutions.  The
publisher must preserve the relative-probability, uniform-slab and
fixed-deletion boundaries below, and must not read or publish uncommitted
R0.74X or later work.

## Frozen research and certificate ledger

| SHA-256 | Repository path |
|---|---|
| d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10 | research/r074w_remote_adjacent_inward_comparison.md |
| 66ec78f67bba64c555a92e9a616c477d702ebb200b48bbfc08a353bdfde5bb73 | research/r074w_remote_adjacent_inward_comparison_primary_audit.md |
| ec6259d95990fd6a8357d9685cc3f17e300e672c1add911a5eb64c6291f3bb99 | research/r074w_remote_adjacent_inward_literature_audit.md |
| 7c0b86b6f4f9a5782946f443bdf731445adbce9069fcba726a7b8fe75df9c171 | research/r074w_remote_adjacent_inward_comparison_certificate.json |
| d70b18dbde23d49e51ec24c1cf8e0f764a5a639297ce783bcc23bf69d050b003 | research/r074w_remote_adjacent_inward_comparison_certificate_report.md |
| dd6a2b1820da126e049aae97ab9b26bb9ef0d02bacca1dc248298303bb2748a3 | research/r074w_remote_adjacent_inward_comparison_independent_audit.md |
| 26df7a1b5fbff87f752a8cebb98113b4fcc13f3b8828566b3fab2eda07e7f223 | research/r074w_remote_adjacent_inward_comparison_qa_report.md |
| 33084928360a5b649ae862cc416679deca8e34574820095f7ffdac52bb760395 | scripts/r074w_remote_adjacent_inward_comparison_certificate.py |
| ff69d1f31d90bea7ec4b6d935d75870bb633f027ffb91bacd073da2d7a4916a4 | scripts/r074w_remote_adjacent_inward_comparison_certificate_independent.rb |
| 40c798d56d3845753abc5fe5a2ee022f7a62716ed98ef5184c7f82e039d0f5db | scripts/r074w_remote_adjacent_inward_comparison_qa.sh |

## Figure archive ledger

Directory:
research/figures/r074w/fig-r074w-remote-adjacent-inward-threshold/

- archive: exactly 25 files, 3,774,363 bytes
- 24-file hash ledger:
  2ebcd49dbf64ee23b651db595113c8edbc9ada6868ede7b92daef6feaca54ab9
- SVG:
  d5d3bb5aa4e407bbbd340482432ab055dd743026bb9286411e23914b1a35adef
- publication PNG, 4204 x 2740 at nominal 600 dpi:
  a20af302fa70828f4f9870b2afd14757ac858f30f0f4c618d6aa5af0b2c5b5c6
- one-page PDF:
  85c0876206ac0976302858e2f588d7295ed3f2326616228c7394772e4e52a52c
- three QA rasters: 2102 x 1370 at nominal 300 dpi
- deterministic two-render comparison: 18/18 files byte-identical
- automated archive validation: **PASS**
- final-size, greyscale and PDF visual inspection: **PASS**

The archive is conservatively labelled as a local precommit SHA-256 seal and
does not claim a Git blob seal.  The exact sealed bytes are nevertheless
preserved in the frozen figure-archive commit above.  Preserve the visible
scope label:

ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NOT CLAY

## Result and claim boundary

For

\[
p=\frac{32}{63},\qquad
q(\ell)=\frac{p^2}{4\ell},\qquad
q_{64}=\frac4{3969},\qquad
q_{65}=\frac{256}{257985},
\]

the exact all-winding conditional-bridge calculation proves the logarithmic
remote deficit law

\[
-L^{-2}\log S_t\longrightarrow q(\ell)
\]

in central-bridge conditional probability.  It does **not** prove a
deterministic prefactor asymptotic for \(S_t\).

- If
  \(\limsup \log(1/R)/L^2<q_{65}\), the relative remote comparator survives
  uniformly on the whole slab.
- If
  \(\liminf \log(1/R)/L^2>q_{64}\), it is swept uniformly on the whole slab.
- Inside the narrow \(q_{65}\)--\(q_{64}\) band, fixed limiting
  \(\ell\) is still classified by strict comparison with \(q(\ell)\);
  equality and its critical law remain open.  Do not call the whole band an
  unresolved transition.
- In the frozen R0.74U placement, packet 1 is swept and packet 2 survives.
  The adjacent-inward endpoint obeys

  \[
  \frac{K_{k_2-1,R}(\tau_2)}{T_*}
  \ge cL_2^{-1/2}
  e^{\chi(65)L_2^2-CL_2}\longrightarrow\infty,
  \qquad
  \chi(65)=\frac{12191}{132088320}>0.
  \]

Therefore a matching all-shell \(O(T_*)\) upper bound is false for this
frozen placement.  Fixed deletion remains open because the sole divergent
coordinate is \(k_2-1=k_1\), which a one-shell deletion may remove.
Payment normalization, arbitrary suitable weak solutions, whole-shell
estimates, scale contraction, regularity, singularity and the
Navier--Stokes Millennium problem remain open.  **NOT CLAY.**

## Certificate, literature and publication instructions

- independent primary analytic audit: **PASS**, zero blockers
- Python certificate: 33/33 checks, 33 exact cases
- independent Ruby audit: 6/6 groups, 56 assertions
- Python negative mutations: 23/23 rejected
- Ruby negative mutations: 24/24 rejected
- PYTHONHASHSEED 0, 1 and 42 and independent regeneration: byte-identical
- certificate scope: finite exact arithmetic, source structure, hashes,
  quantifiers and claim boundaries; not a continuous PDE proof
- literature screen: bounded primary-source screen only; a finite non-hit is
  not evidence of novelty, priority or publishability

Publish one R0.74W research note, reader PDF, and the frozen four-panel figure.
Update the ordinary note index, homepage research count and route/version
ledger.  Preserve the established concise retro site style, exact
mathematical directions and every proved/open distinction.  Do not update the
cumulative recap for this release.  Do not invent simulation, DNS or DGX
evidence.  Translation is local/direct and must not use DGX.  Deployment is
complete only after GitHub Pages CI succeeds and every published object is
verified against the release ledger under the existing publication workflow.
