# R0.74Q publication handoff

## Ownership and release order

- Publishing owner: independent Codex task `发布任务`.
- Task id: `01a05bea-7f45-7410-8792-4e1f840b83f8`.
- Reuse of the former publishing task: **false**.
- Frozen release commit:
  `87915055471a3d6e39e7ffec30ac076a5fd18da5`.
- Research core commits:
  `60d4c1c6` (effective-shell decision),
  `11d8dba6` (common-shear gate), and
  `1e907750` (relaxed multipacket stress test).
- Freeze manifest SHA-256:
  `8cb1d3c9089e9694ef753655c8a7e06d69c7e9a3838a35ea3b5f93219b4e4d01`.
- Predecessor gate: R0.74P is live at origin/main
  `bee29a23b74b464c3f7a978dc8e0b1afa2d69a8e`; Pages action
  `33587918095` succeeded and its home, HTML, PDF, SVG, PNG, and site-version
  objects were byte-verified.
- R0.74Q is ready for immediate publication.  No cumulative recap update is
  required for this section.

## Frozen inputs

The publisher must consume the frozen release commit without changing its
mathematical content.  The controlling inputs are:

1. `research/r074q_freeze_manifest.json`;
2. `research/r074q_report-source.md`;
3. `research/r074q_gap_matrix.md`;
4. `research/r074q_problem_freeze.md`;
5. `research/r074q_common_shear_multipacket_gate.md`;
6. `research/r074q_relaxed_multipacket_cubic_obstruction.md`;
7. both deterministic certificate packages and all independent audits named
   in the freeze manifest; and
8. `research/r074q_primary_literature_boundary.md` together with its
   independent audit.

This release is analytic.  It contains no numerical Navier--Stokes
simulation, DNS, DGX run, or formal data figure.  The website must not invent
simulation language or a figure package.

## Public targets

- HTML: `/notes/r0-74q.html`
- Reader PDF: `/notes/r0-74q.pdf`
- Site root: `https://kasifa.github.io/`

The note index, homepage research count, release/version ledger, and
literature ledger should advance through the ordinary publication generator.
Do not create or modify a cumulative recap for R0.74Q.

## Presentation contract

- Use the established concise retro site style and the supplied first-person
  Chinese reader source.
- Preserve the exact boundary labels `PROVED`, `INHERITED`, `FINITE`,
  `CONDITIONAL`, `LITERATURE BOUNDARY`, `OPEN`, and `NOT CLAY`.
- Keep MathJax delimiters, inequalities, superscripts, and equation directions
  intact.
- Translation, if mechanically required, is local/direct and must not use
  DGX.
- The 2D3C/passive-third-component and common scalar superposition mechanisms
  are prior structure, not a novelty claim.

## Claims that must not drift

1. The terminal effective-shell best-\(N\) reduction is proved, but the
   uniform arbitrary-solution packing estimate is **OPEN**.
2. Finite common-shear 2D3C packet superposition is an exact smooth unforced
   Navier--Stokes family; this mechanism is known and is not claimed as new.
3. The frozen terminal-angle/common-\(B\) obstruction concerns the specified
   asymptotic geometry and inherited proof window; it is not a universal
   common-shear no-go.
4. The relaxed explicit family has growing finite \(N\), common terminal
   geometry, uniform all-lobe dominance, and target clock lower bounds.
5. Only the lower detection
   \(Y_{2,R}^{\rm sf}\ge c\sqrt N\,T\) is proved.  A matching full
   square-function upper bound is **OPEN**.
6. For the canonical equal-target family, the genuine nonnegative exterior
   velocity-cubic row proves
   \[
     \frac{(P_R^{M,(N)})^{2/3}}{NT}\longrightarrow\infty.
   \]
   This does not exclude every multipacket design.
7. Signed cumulative flux of order \(NT\), the fixed-scale inequality (Q.1),
   suitable-weak effective-shell packing, regularity, singularity, novelty,
   and priority are all **OPEN / NOT CLAIMED**.
8. No Clay theorem is claimed.  **NOT CLAY.**

## Completion gate

Publication is complete only when all of the following hold:

1. the publication commit is present on `origin/main`;
2. GitHub Pages reports success;
3. the live HTML and reader PDF return HTTP 200;
4. both live objects are byte-identical to the local release objects;
5. the homepage/latest-release marker, note index, research count,
   site-version ledger, literature page, ordinary invariant/math/publication
   suites, link checks, bilingual checks, gate runner, and browser QA pass;
6. no recap page was modified; and
7. the publishing task reports the publication commit, Pages action, URLs,
   and exact SHA-256 evidence back to the research task.

The publishing task may repair publication infrastructure or
cross-platform reproducibility checks, but it must not weaken a gate or edit
the frozen mathematical claims.
