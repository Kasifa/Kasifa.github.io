# R0.74T Step 19 frozen publication handoff

## Release identity and queue order

- `release_id`: `R0.74T-Step19`
- publication owner: the single long-lived Codex task `发布任务`
- publication task id: `01a06480-0532-7fd0-bdf0-57571465a2d4`
- logical predecessor: `R0.74S-Step18`
- queue rule: append once to the existing FIFO queue; do not create another
  publishing task and do not publish ahead of an earlier queued release
- frozen release source commit:
  `2a3a59d4626face7b883159ee9b18500005e41d7`
- frozen research-core commit:
  `b120598d36140385676bb4a9922d46abcdff0ba4`
- frozen figure source/raw commit:
  `0433c129868ddf349c7b64d427747f590fa06898`
- cumulative recap required: **false**

The source commit contains the proved note, bounded primary-literature audit,
two independent analytic/certificate audits, fail-closed QA, and the sealed
25-file formal figure archive.  The handoff itself records that frozen state;
the publisher must not alter mathematical claims or regenerate scientific
values.

## Frozen file ledger

| SHA-256 | Repository path |
|---|---|
| `8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd` | `research/r074t_schedule_invariant_dwell_coercivity.md` |
| `0a0a66f6e8d84bb6fad18f6744f02bbf4c2848c96fa5b37dd4b8dc49c628ef99` | `research/r074t_schedule_invariant_dwell_primary_audit.md` |
| `60b49f6279c696a370af5f8050a6162753372eba81f8215e02e15259f084e88b` | `research/r074t_schedule_invariant_literature_audit.md` |
| `ab78d8a8e9a76dc2650d147836c3a51d011c6ef7866f84aa08ed4868b8323c47` | `research/r074t_schedule_invariant_dwell_certificate.json` |
| `acb54e58cf4af40d759962a593a17379cf2bc9769d9664abae800f6afe73764c` | `research/r074t_schedule_invariant_dwell_certificate_report.md` |
| `81d51239452e48b692125f5a19d2cc1a1ca66c5b65aa0405a1b8d429279b289d` | `research/r074t_schedule_invariant_dwell_independent_audit.md` |
| `b942f990639600a1357518a92361b9c971f5fbaccb2b2bd92189448975b7996a` | `research/r074t_schedule_invariant_dwell_qa_report.md` |
| `3229eb8f50a03d66e30449c36070f8734bdded6ed7b11e11324013597b715895` | `scripts/r074t_schedule_invariant_dwell_certificate.py` |
| `5fedbd8496e66cc55a4c624b57b21e229a00c948de28df59f91f5ac7461ea03e` | `scripts/r074t_schedule_invariant_dwell_certificate_independent.rb` |
| `371b5c74b1210cd7e8e8151472786b0992e2771ae8e08812f158febfee61b64e` | `scripts/r074t_schedule_invariant_dwell_qa.sh` |
| `a437fd6cc5fa600b025a0f26913e283f9a5beb785537a3f1293662a804ef92a0` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/README.md` |
| `3d868ed4b915b1239877c2ad6110833fe9c0056cf83b2b68695b7826f3c187e1` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/SHA256SUMS` |
| `037e3d67da080fcf9f95ae6817fb32963601d104ff147159ed6817863f2ce101` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/caption.md` |
| `20d83ec8082fc7ca14bbf250449748d9c913a4dac7dc92df87ac3b667922580b` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/chart-contract-and-source-data.md` |
| `212dee16fee3f52cb1b69099a93fbe56dbcb2570fd4ffa3af3479a68d8c53c9d` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/command.txt` |
| `23c68500f3f6e529763a3bded5bdc4b323f93f830a97a26b738f35be4bbc80cf` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/config.json` |
| `044f57af444a6814b7f3b89221a8eda085bd339db299d2d8fbf4ec79e6fbe74a` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/contract.json` |
| `50b1ad1a6c404c0acd52f736c85dac3b5d3d48bacd89aa82d65329769f0a204d` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/environment.json` |
| `0bbc2871a26329d2d107080df86b0170cd0577802f1f7754c74ffe213ccd5ca8` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/figure.pdf` |
| `c162e5d9c3965c01899041d8f5dc0d9efc20a262edc6c71580520550802f0e1d` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/figure.png` |
| `3533b4dfcbbe33bd9d0c213de6ca30875ba81a7d34199ed8754ad2fbcf6d0d8f` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/figure.svg` |
| `9ca63058c36790674c2e2af8962a0183ffaae895d62aba46afc5267b1fc3fd75` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/manifest.json` |
| `6de2afe4a6d971d0f615b17f075ce61f940c64bbb9e8a3b91b7945dc6cc8e660` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/plot.py` |
| `af80cdbdfa4d6c8782ab7000570bfc43a25292490f9062fe5583c4d9f6b88fd2` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/progress.ndjson` |
| `bf7a2a2c806d229168349f96177c6f23295fb82a696490f184dafbe5060bb7a8` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/qa-final-size.png` |
| `e7beaf84d8697afd8da98343e489317764ddf137f12fd2b02fcfd652618f370c` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/qa-grayscale.png` |
| `46c08c63c1df0b5c171ddf8c7c25fb2b4349fb18d50d79ccc6277ebce2196949` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/qa-pdf.png` |
| `06c5521974c020e3e65fc3bb14a2e25eda4939970b695e4c754a4d34d56d5be7` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/qa-protocol.md` |
| `174084377439aa59afae36a6513ffab5e7fb15501a65c3f9193ed1b08c7cd8d9` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/qa-report.md` |
| `525ffa315648c87692d7e77fec950ff730b1e2e1f31638c5a065ec73e8d770c2` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/requirements.txt` |
| `abee597de3eac5891adec856bdbec514585cfd17d33fde7d536c4338d77a267a` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/resource-log.ndjson` |
| `ff059234f87d6624d41317d7343a37a7ba9c3b93047ed72d430cc3c158705cc9` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/results.json` |
| `fdfc9c45472cb400799410385d6ba18a1cbdd44b5114aa719b234311897c93ff` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/source-data.csv` |
| `8468f6858eec3a4deb5dedd05616790b05e0d201991ff97059e807338956dbf3` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/validate.py` |
| `fd3997599ee70c95726be6bdc5a30147c2b4a22d4b6b05e791a6314124d295d8` | `research/figures/r074t/fig-r074t-schedule-invariant-dwell-barrier/validation.json` |

## Result and claim boundary

The frozen note proves the following limited statements.

1. A persistent outer target lobe on a measurable interval of length
   `theta R^3` forces the exact positive exterior-cubic lower bound
   
   \[
   P_R^M\ge
   2\sqrt2\,\theta h_2^{3/2}R
   \Gamma_2^{-5/4}L_2^{-1/2}.
   \]

2. Two target shells with positive persistent `K`-clock floors on arbitrary,
   possibly disjoint time sets give only the fixed-deletion witness
   \(\mathfrak L^K_{1,R}(D)\ge\min(h_1,h_2)\).  This is not a lower bound
   for \(\mathfrak H^{\rm fix}\), and it is not an upper bound for the full
   completed clock.

3. In the inherited adjacent-shell survival window, bounded payment relative
   to that witness requires exponentially collapsing normalized dwell,
   
   \[
   \theta_n\le C L_{2,n}^{1/2}
   e^{-(5c_\gamma-a_S)L_{1,n}^2-d_{L,n}},
   \qquad
   5c_\gamma-a_S=\frac{603445}{89413632}>0.
   \]

4. One exact smooth periodic mean-zero unforced common-shear Navier--Stokes
   solution realizes two genuinely disjoint admissible `R^3`-long target-lobe
   windows, but its payment-to-witness ratio diverges.  The construction is
   restricted to the inherited terminal slab.

The following remain **OPEN**: a payment-scale upper bound for the full
completed clock; control of off-target clocks and accumulated dissipation; a
bridge to the stopped-flux fixed-deletion functional without the Step 18
payment terms; Q.12, Q.1, scale contraction, regularity, singularity, and the
Navier--Stokes Millennium problem.  The literature screen is bounded and
does not establish novelty or priority.  **NOT CLAY.**

## Certificate and QA summary

- independent primary analytic audit: **PASS**
- Python certificate: 31/31 groups, 18,933 exact finite cases
- independent Ruby audit: 11/11 groups, 9,201 assertions
- Python negative mutations: 26/26 rejected
- Ruby negative mutations: 27/27 rejected
- `PYTHONHASHSEED=0,1,42`: JSON and report byte-identical
- figure preseal: 46/46 checks and 18/18 deterministic-core hashes
- final figure seal: 47 checks; `--verify-only` **PASS**
- finite certificates cover algebra, quantifiers, source structure and hashes;
  they do not machine-prove the continuous PDE inputs

## Scientific figure inventory

The single formal figure is
`fig-r074t-schedule-invariant-dwell-barrier`:

- Panel A: the two exact disjoint lobe windows in one terminal slab;
- Panel B: the exact Hölder coefficient and exponent ledger;
- Panel C: the unit-dwell logarithmic divergence factor;
- Panel D: the necessary exponentially collapsing dwell ceiling.

The archive provides a 178 mm by 116 mm vector SVG, one-page PDF, and
4204 by 2740 PNG at 600 dpi, plus exact source data, generator, environment,
three QA renders, manifest and checksums.  It is an analytic schematic with
derived analytic values: **NOT PDE DATA, NOT DNS, NOT CLAY**.

## Publication instructions

- Preserve the established concise retro site style and the exact mathematical
  directions, quantifiers, labels and claim boundaries.
- Publish an R0.74T note, reader PDF and the sealed formal figure; update the
  ordinary note index, homepage research count, route/version ledger and
  literature ledger through the existing publishing system.
- Do not create or update a cumulative recap for this release.
- Translation is local/direct and must not use DGX.
- Deployment is complete only after GitHub Pages CI succeeds and the live HTML,
  reader PDF and primary SVG are byte-checked or otherwise verified according
  to the publishing workflow.
