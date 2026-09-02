# R0.74P publication handoff

## Ownership and release order

- Publishing owner: independent Codex task `发布任务`.
- Task id: `01a05bea-7f45-7410-8792-4e1f840b83f8`.
- Reuse of the former publishing task: **false**.
- Research core commit: `3306812e962fc0e2fecc227d0ffea6ae062c91f2`.
- Freeze manifest SHA-256:
  `bdac16d76a0f843adf097d1e412db3cc401d0cecc081b5c0cffc0b4244e4f405`.
- Predecessor gate: R0.74O is live at origin/main
  `4e8d8b7f57b1cc51d3eef891c9c13f9c86b2e944`; Pages action
  `33584309952` succeeded.
- R0.74P is ready for immediate publication.  No cumulative recap update is
  required for this section.

## Frozen inputs

The publisher must consume the core commit without changing mathematical
content.  The controlling inputs are:

1. `research/r074p_freeze_manifest.json`;
2. `research/r074p_report-source.md`;
3. `research/r074p_temporal_observable_triage.md`;
4. `research/r074p_problem_freeze.md`;
5. `research/figures/r074p/fig-r074p-observable-triage/`;
6. the independent audit files named in the freeze manifest.

The formal figure is analytic, not a simulation or DNS.  Its PDF, SVG, PNG,
source data, generator, validator, QA renders, manifest, and checksums are all
frozen in the package.

## Public targets

- HTML: `/notes/r0-74p.html`
- Reader PDF: `/notes/r0-74p.pdf`
- Primary vector figure:
  `/assets/r074p/fig-r074p-observable-triage.svg`
- Site root: `https://kasifa.github.io/`

The note index, homepage research count, release/version ledger, and literature
page should advance through the ordinary publication generator.  Do not create
a new recap page and do not modify an existing recap for R0.74P.

## Presentation contract

- Use the established concise retro site style and first-person singular or
  neutral mathematical prose.
- Preserve the exact boundary labels `PROVED`, `INHERITED`, `FINITE`,
  `LITERATURE BOUNDARY`, `OPEN`, and `NOT CLAY`.
- Keep MathJax delimiters and equation references intact.
- Translation, if any mechanical translation is required, is local/direct and
  must not use DGX.
- Do not convert an analytic certificate into simulation language.

## Claims that must not drift

1. For every fixed \(\sigma>0\), the positive-order window mass misses the
   target scale; the statement is not uniform as \(\sigma\downarrow0\).
2. Energy oscillation detects the target scale but reconstructs endpoint energy
   and the full dissipation ledger.
3. The defect-completed moving-shell clock and its \(\ell^1\) BV closure are
   proved in Version M.
4. Only the target component has a two-sided \(T_*\) comparison.  The full
   \(Y_{2,R}^{\rm sf}\) upper bound remains **OPEN**.
5. Suitable-weak stability is only at fixed \(R\) and fixed terminal point.
6. The central \(\ell^1\)-to-matched-\(\ell^2\) PDE compression and prescribed
   centre/scale packing remain **OPEN**.
7. No novelty, priority, singularity, regularity, continuation, or Clay theorem
   is claimed.  **NOT CLAY.**

## Completion gate

Publication is complete only when all of the following hold:

1. the publication commit is present on `origin/main`;
2. GitHub Pages reports success;
3. the live HTML, reader PDF, and primary SVG return HTTP 200;
4. each of those three live objects is byte-identical to the local release
   object;
5. the ordinary invariant, math/figure, publication, route, link, bilingual,
   gate-runner, and browser-QA suites pass;
6. the publisher reports the publication commit, Pages action, URLs, and exact
   SHA-256 evidence back to the research task.

The publishing task may repair publication infrastructure or cross-platform
reproducibility checks, but it must not weaken a gate or edit the frozen
mathematical claims.
