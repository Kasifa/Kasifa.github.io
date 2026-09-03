# R0.74Z Step 25 frozen publication handoff

## Release identity and queue order

- release id: R0.74Z-Step25
- publication owner: the single long-lived Codex task 发布任务
- publication task id: 01a06480-0532-7fd0-bdf0-57571465a2d4
- logical predecessor: R0.74Y-Step24
- queue rule: hold locally until R0.74Y completes, then append once to the
  same FIFO queue; do not create another publishing, recap, or reflection task
- frozen research/certificate commit:
  91aaac829c6b54a0ad24cf10ff3f533f58a10035
- frozen figure-archive commit:
  30ed47c9ae2334a9e9cb3468a5094dfb3dc65907
- cumulative recap required: **false**
- formal scientific figure required: **true**

R0.74Z tests the cancellation-cell continuation of R0.74Y. It proves exact
same-shear superposition algebra and an exact payment lower bound whenever a
remote kinetic witness persists on a spacetime tube. It does not prove that an
endpoint-only witness persists for a uniform time, does not close the critical
layer, and does not control the completed clock. Publish only the frozen
R0.74Z paths listed here; do not read or publish R0.75A or later work.

## Frozen research and certificate ledger

| SHA-256 | Repository path |
|---|---|
| bb766da4002da760c35185294081f80df97c349ea08b198a5f76db31663aaf6a | research/r074z_cancellation_cell_gate.md |
| 6b867551bce840cb382cd13cb2ff298affbf0c0d8b1357a8163c5cedc9bace08 | research/r074z_cancellation_cell_gate_primary_audit.md |
| 8e5346ecf3c2beef4a620e0844e790703b628388ca7f0a6997aae88818caa82f | research/r074z_cancellation_cell_gate_literature_audit.md |
| aff6d6d39b2163a263bc2a5055225d9c25d5b46d0b2704bdfcb276976dcc2285 | research/r074z_cancellation_cell_gate_certificate.json |
| 91602c567e612759baf9bd03c7c688465c39997b90e445de13cc159f44cf5154 | research/r074z_cancellation_cell_gate_certificate_report.md |
| cd44004a02c3486b734b17e2261dcd725a3d287f5462d7480ec7b294e2f43420 | research/r074z_cancellation_cell_gate_independent_audit.md |
| 868afc8a69413e3176553acdb97bc03451de2181671684a207b01e7367d4e71f | research/r074z_cancellation_cell_gate_qa_report.md |
| 512cefac3d22dcc6836b128c052a9a528203be1e7ffd7217f16556193448631a | scripts/r074z_cancellation_cell_gate_certificate.py |
| 766edac40dc9a3686067cad1ea31c01972075f1aa453e02e7fa4b461629a706c | scripts/r074z_cancellation_cell_gate_certificate_independent.rb |
| beaef0722e27813e4a0a164372355b2d5521413dad35e7f34d8b177f5842689a | scripts/r074z_cancellation_cell_gate_qa.sh |

## Figure archive ledger

Directory:
research/figures/r074z/fig-r074z-remote-persistence-gate/

- archive: exactly 25 files, 3,032,354 bytes
- 24-file hash ledger:
  1374dbd15d80b85bb46e561cf523f451e6459d1d206718aa34941559980d854c
- SVG:
  31cfcd6e5e8e57729a8c5bce7459def3a618cd5bbda842a066331770ad0ffd42
- publication PNG, 4204 x 2740 at nominal 600 dpi:
  0414ade9d42a899830affe8ae730212946362ba72bc3a39bcf05c61df509368c
- one-page vector PDF:
  4918a691914b23fd3570847510e57663d8db3ddad8a5707873943434b400d7b0
- manifest:
  692cb2b9e4e4973e7daff2320196bd56aed424ceba671a749c1dc7e833155d9c
- validation record:
  827499c45aabce04624913311535218bec14e5310c27b3797b25957cbded48e1
- three QA rasters: 2102 x 1370 at nominal 300 dpi
- deterministic two-render comparison: 18/18 files byte-identical
- automated archive validation and independent verify-only rerun: **PASS**
- final-size, greyscale, and PDF visual inspection: **PASS**

The archive is conservatively labelled as a live-file SHA-256 precommit seal;
it does not claim a Git blob seal. The exact sealed bytes are preserved in the
frozen figure-archive commit above. Preserve the visible scope label:

ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS |
NO NOVELTY CLAIM | NOT CLAY

## Result and claim boundary

For the exact common-shear passive equation, every finite inversion-paired
same-\(b\) superposition remains an exact smooth periodic unforced
Navier--Stokes solution. Literal vertical or time translation of an evolved
packet does not commute with the operator and is not silently admitted.

At the outer packet's adjacent-inward shell, put

\[
 \omega=\gamma_{k_2-1}=\Gamma^{1/4}.
\]

The same physical annulus is one more shell inward at scale \(2R\), so its
payment weight is

\[
 \gamma_{k_2-2}=\omega^{1/4}=\Gamma^{1/16}.
\]

If a weighted kinetic floor \(h\) persists for a time
\(|J|=\theta_LR^3\) on a region of volume at most
\(C_\Omega L^\nu R^3\), spatial Hölder gives the exact deterministic
coercivity

\[
 (P_R^M)^{2/3}
 \ge cC_\Omega^{-1/3}\theta_L^{2/3}hR^{2/3}
       \omega^{-5/6}L^{-\nu/3}.
\]

For the frozen R0.74Y parameters,

\[
 \Delta_{\rm rem}
 =\frac5{24}c_\gamma-\frac\rho6
 =\frac{64279}{238140000}>0,
 \qquad
 \kappa_*=\frac32\Delta_{\rm rem}
 =\frac{64279}{158760000}.
\]

Therefore every persistence sequence satisfying

\[
 \limsup_{L\to\infty}\frac{-\log\theta_L}{L^2}<\kappa_*
\]

is incompatible with a W-kinetic payment escape. The equality layer
\(-L^{-2}\log\theta_L=\kappa_*+o(1)\) is **OPEN** in this release.

The endpoint-to-\(R^3\)-tube implication is only conditional here: it uses
the moving-frame derivative envelope (Z.22), endpoint preservation, and a
uniform moving-strip all-winding comparison. Within that derivative and
conditioning model, endpoint-focused escape requires at least

\[
 \log\mathcal N_L
 \ge
 \left(\frac{476239}{1064835072}+o(1)\right)L^2.
\]

This rate is necessary, not sufficient, and its equality case is open.
Point interpolation by displaced Gaussians or finite exponential sums is not
promoted to uniform strip cancellation. Qualitative analyticity alone does
not provide the missing quantitative estimate.

Most importantly, the floor \(h\) is not an upper bound for the completed
clock \(K\). The estimate above does not control accumulated rows and does
not prove Y.57. The frozen release verdict is:

- exact same-shear algebra and persistent-tube coercivity: **PROVED**;
- strict subcritical W-kinetic persistence escape: **BLOCKED**;
- endpoint-only, critical, and exponentially ill-conditioned finite-family
  branches: **OPEN**;
- full completed-clock Y.57: **OPEN**;
- payment-compatible cancellation cell: **NOT CONSTRUCTED**.

No arbitrary-suitable-weak-solution theorem, whole-shell upper bound,
regularity result, singularity result, novelty claim, or Millennium claim is
made. **NOT CLAY.**

## Certificate, literature, and publication instructions

- independent primary analytic audit: **PASS**, zero blockers
- Python certificate: 10/10 checks
- independent Ruby audit: 11/11 assertions
- Python negative mutations: 22/22 rejected
- Ruby negative mutations: 23/23 rejected
- PYTHONHASHSEED 0, 1, and 42: byte-identical
- certificate scope: finite exact arithmetic, source structure, hashes, and
  claim boundaries; not a continuous PDE proof
- literature screen: bounded primary-source screen only; a finite non-hit is
  not evidence of novelty, priority, or publishability

Publish one R0.74Z research note, reader PDF, and the frozen four-panel
figure. Update the ordinary note index, homepage research count, and
route/version ledger. Preserve the established concise retro style and every
proved/conditional/open distinction. Do not update the cumulative recap for
this release; reserve the next recap for a later major milestone. Do not
invent simulation, DNS, or DGX evidence. Translation is local/direct and must
not use DGX. Deployment is complete only after GitHub Pages CI succeeds and
every published object is verified against this ledger under the existing
publication workflow.
