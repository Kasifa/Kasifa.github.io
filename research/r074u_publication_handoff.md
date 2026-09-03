# R0.74U Step 20 frozen publication handoff

## Release identity and queue order

- `release_id`: `R0.74U-Step20`
- publication owner: the single long-lived Codex task `发布任务`
- publication task id: `01a06480-0532-7fd0-bdf0-57571465a2d4`
- logical predecessor: `R0.74T-Step19`
- queue rule: append once to the existing FIFO queue; do not create another
  publishing task and do not publish ahead of an earlier queued release
- frozen release source commit:
  `735030d9e51068518796a79571ada291c5414a06`
- frozen research-core commit:
  `d74e7b297928147334136f4c3cb29c5226d66381`
- frozen figure source/raw commit:
  `8b75193df63a962392f89fcf1dbc20a8411334ba`
- cumulative recap required: **false**

The release source contains the proved note, independent primary analytic
audit, bounded primary-literature audit, two independent finite certificate
implementations, fail-closed QA, and the sealed 25-file formal figure archive.
The handoff records that frozen state. The publisher must not alter
mathematical claims, transfer an upper bound to the wrong time set, or
regenerate scientific values outside the sealed workflow.

## Frozen file ledger

| SHA-256 | Repository path |
|---|---|
| `e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99` | `research/r074u_intrinsic_certified_residence.md` |
| `b509d8201ae8334f6e589f65b63be65e6b2f427c9250c74a400c9419cc2de314` | `research/r074u_intrinsic_certified_residence_primary_audit.md` |
| `0cf6e19a42e524aaf79aca10d72c5380029dce37032215974d99976a0b2a327c` | `research/r074u_intrinsic_residence_literature_audit.md` |
| `4c79619f25ff207b69cc7342edf46aad2c579518c9ec25179296751641fcc649` | `research/r074u_intrinsic_certified_residence_certificate.json` |
| `607d1171803e2a21fe5c8776e72cbc735bc6341b0d09cb4c413b53735da2135d` | `research/r074u_intrinsic_certified_residence_certificate_report.md` |
| `fe9b34c23a1c2755ca0501a832f8acbe63c786613a2515c406c6c227d4f62fa2` | `research/r074u_intrinsic_certified_residence_independent_audit.md` |
| `3dabeada679ef005c8e42d1b3feea751364a47d9244e3f376b3ae1db0b16b670` | `research/r074u_intrinsic_certified_residence_qa_report.md` |
| `a1947f7af58049d13c2ca2f2a0d9653391045e09e23ef8b9fbfbbf50bda2fdaa` | `scripts/r074u_intrinsic_certified_residence_certificate.py` |
| `58ff798a631c2eab22621afaf16fe3f8d0de7e27a999dae090efc61694932505` | `scripts/r074u_intrinsic_certified_residence_certificate_independent.rb` |
| `b87d412ff8e540daff62f4dbb6b581cdc7eea4ab1c224b0689997ac74c363656` | `scripts/r074u_intrinsic_certified_residence_qa.sh` |
| `ba456ffee814413825d6edf0c756c8945c79615c46d01e6ef9aafeddab72109a` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/README.md` |
| `fff653eca01cc1db328710db980d924fe6d9d1ca1ddcd9385d18248dd7c88ecb` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/SHA256SUMS` |
| `f61b8ba055044daa5a6f70f3443f2f5ce84eb5fe0b89bd500cca7f3643ec50a4` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/caption.md` |
| `dd82fe8d9bbebeaadfb35cfea77a610283f0e1cc56ce5a8d4f1208d0f862c4ec` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/chart-contract-and-source-data.md` |
| `e7707871c0c4faceaed4f711b5199662a8d09cfe0784b131bddf1dfa96920fdf` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/command.txt` |
| `994adb1ebfdc572692817383814b666853125a1f15ca53cd0e6ab4ef1182a47b` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/config.json` |
| `f5937063ece9d1d18525deaf4216098e5de201fd79e091dd5c92593994b8af1f` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/contract.json` |
| `43b85c33f6d0345c61a326789d0c5e21dab675acb83bcc5549949474058f8c2b` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/environment.json` |
| `b27c4e64f189943ec261dd3e6a304435fbde07e6561600d2920885e1af9a0ffc` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/figure.pdf` |
| `a08d07ad7377f04f7463c7bd7b9d87d9b33d2e1f718117e47ef0ff19bd292b7c` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/figure.png` |
| `ee4f90a3b5e25fc252ea7869dbb9a37ab16e23550af09e6f6e0c6323513c891d` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/figure.svg` |
| `8a262539af1007cdd07c6c293c107b4f19bff0d1277941cd4453c7f808efb909` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/manifest.json` |
| `bbf10254aff83c2188f217472e8e24630954c5db83865e63cd01f100397e6658` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/plot.py` |
| `6581034c15f1fc5606ce436615678d41cbd8046a43caace7a389d27a74d28f98` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/progress.ndjson` |
| `ef2cedd77e532599f12a74dc50412679d1df52cb80faddd8486d9f87e422385d` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/qa-final-size.png` |
| `0690bee6ac182bffca05ce0ad394843177014b9f3fc7e6027b46b7765c682773` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/qa-grayscale.png` |
| `a762c95b4ae5687392c0a5b09340412c1c5552b521f6e3eb2e29e5481469bb0c` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/qa-pdf.png` |
| `034f525d94547e9c09fdb22c5bbcc30e216e491a0d78afc9810855ea3492737b` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/qa-protocol.md` |
| `056b26ede7520f9bdc43c63f58159c1d487d6b8d9a6c8bd0e8a7c2252be5296b` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/qa-report.md` |
| `525ffa315648c87692d7e77fec950ff730b1e2e1f31638c5a065ec73e8d770c2` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/requirements.txt` |
| `cd8841857bea017f88f553ca8ceabf52e9ee262d51d07711edea57b5fc03c314` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/resource-log.ndjson` |
| `acb4e94be710f8e30c67eec14d06dd995e8de20d513c2faaa44c581daf595d8a` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/results.json` |
| `d05262d69b3d4f02cbb30401eedb30121457fe309f217286cedc0a31550ebc35` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/source-data.csv` |
| `c9a826e4a90de7094df4c6e6c36fa51f3d5502934117a621b24b388b71989db4` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/validate.py` |
| `18d952175aec6e44aba08bc61bf7f73261bca7fe169ed69d25aff2d5e2b7837e` | `research/figures/r074u/fig-r074u-intrinsic-certified-residence/validation.json` |

## Result and claim boundary

The frozen note proves the following limited statements.

1. For each canonical inversion-paired packet, the explicit symmetric centre
   condition defines a certified geometric corridor with

   \[
   {72\over5}L_iR^3
   \le |\mathscr R_i^{\rm cert}|
   \le \min\left\{R^2,
   {256A(L_i)\over1-\varepsilon_i}L_iR^3\right\}
   <{1024\over3}L_iR^3.
   \]

2. On that corridor, the total velocity field has the inherited
   amplitude-weighted lobe floor. Positivity of the defect-completed clock
   gives only

   \[
   \mathscr R_i^{\rm cert}
   \subset\{t\in I_R:K_{k_i,R}(t)\ge c_KT\},
   \qquad
   |\{K_{k_i,R}\ge c_KT\}\cap I_R|
   \ge {72\over5}L_iR^3.
   \]

   There is no converse inclusion and no upper bound for the complete
   clock-superlevel set.

3. For the outer packet, the normalized certified dwell obeys
   \(\theta_{{\rm cert},2}\ge(72/5)L_2\). Under the hypothetical bounded
   payment assumption, R0.74T would instead require

   \[
   \theta_{{\rm cert},2}
   \le C L_2^{1/2}
   e^{-(5c_\gamma-a_S)L_1^2-d_L},
   \qquad
   5c_\gamma-a_S={603445\over89413632}>0.
   \]

   The two requirements are incompatible. Thus the exponentially short-dwell
   escape is closed for the frozen canonical common-shear packet architecture.

4. For the explicit R0.74T phases, the one-sided certified lower constants
   improve to \(96/5\) for the inner packet and \(144/5\) for the outer
   packet.

The theorem is restricted to the inherited exact smooth periodic mean-zero
unforced common-shear solution and its frozen derivative-heat packets. It is
not a residence theorem for arbitrary packets or suitable weak solutions.

The following remain **OPEN**: an upper measure bound for the complete
`K`-superlevel set; the full completed-clock upper ledger including
off-target endpoint rows, accumulated viscous terms, packet cross terms and
the shear baseline; arbitrary-clock lobe extraction; high-Rayleigh and
anomalous-defect branches; the fixed-deletion gate, direct hybrid gate, Q.12,
Q.1, scale contraction, regularity, singularity, and the Navier--Stokes
Millennium problem. **NOT CLAY.**

## Literature boundary

The bounded primary-source screen found no source among the checked exact
anchors that states the full R0.74U combination. Inage (2026) is a prominent
terminology-level near collision: it studies an upper residence-time estimate
for low-phase-drift coherent Fourier--helical triads, not a lower physical-lobe
residence estimate in a spatial annulus. The screen is not a proof of novelty,
priority, correctness, nonexistence, or publishability.

## Certificate and QA summary

- independent primary analytic audit: **PASS**
- Python certificate: 31/31 checks, 869 exact finite cases
- independent Ruby audit: 9/9 groups, 1,651 Rational assertions
- Python negative mutations: 23/23 rejected
- Ruby negative mutations: 24/24 rejected
- `PYTHONHASHSEED=0,1,42`: JSON and report byte-identical
- figure preseal: 43 checks per pass and 18/18 deterministic-core hashes
- final figure seal: 47/47 checks; `--verify-only` **PASS**
- finite certificates cover algebra, kinematics, quantifier sentinels,
  source structure and hashes; they do not machine-prove the continuous PDE
  inputs

## Scientific figure inventory

The single formal figure is
`fig-r074u-intrinsic-certified-residence`:

- Panel A: exact symmetric centre corridor and terminal-slab truncation;
- Panel B: horizontal room times reciprocal speed gives the \(L_iR^3\)
  residence scale;
- Panel C: two-sided geometric corridor versus lower-only full-clock
  residence;
- Panel D: certified dwell versus the necessary exponentially short bounded-
  payment dwell.

The archive provides a 178 mm by 116 mm vector SVG, one-page PDF and 4204 by
2740 PNG at 600 dpi, plus exact source data, generator, environment, three QA
renders, manifest and checksums. It is an analytic schematic with derived
analytic values: **NOT PDE DATA, NOT DNS, NOT CLAY**.

## Publication instructions

- Preserve the established concise retro site style and the exact mathematical
  directions, quantifiers, labels and claim boundaries.
- Publish an R0.74U note, reader PDF and the sealed formal figure; update the
  ordinary note index, homepage research count, route/version ledger and
  literature ledger through the existing publishing system.
- Treat the Inage (2026) item only as a terminology-level near collision and
  preserve the finite-search/non-novelty boundary.
- Do not create or update a cumulative recap for this release; defer recap to
  the next genuinely major route closure.
- Translation is local/direct and must not use DGX.
- Deployment is complete only after GitHub Pages CI succeeds and the live HTML,
  reader PDF and primary SVG are byte-checked or otherwise verified according
  to the publishing workflow.
