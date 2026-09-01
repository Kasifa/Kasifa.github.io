# Research publication workflow

This directory defines the independent publication boundary. Research hands off
only committed, hash-pinned artifacts. Publication code may translate, typeset,
bind, audit, push, monitor, and verify those artifacts; it must not edit the
mathematical proof, theorem quantifiers, certificate payloads, formal-figure
scientific data, or research route.

## Single entry point

Use the bundled/local Node runtime to run:

```text
node scripts/publish-release.mjs --handoff release/handoffs/<release>.json --allow-commit --allow-push
```

Routine translation is fixed to `LOCAL_DIRECT_NO_DGX`. The handoff cannot
provide arbitrary commands: the pipeline derives and enforces the three
release-owned scripts `generate_<release>_release.py`,
`add-<release>-translations.mjs`, and `bind-<release>-pdfs.mjs`.

For a deployed baseline, use the read-only path:

```text
node scripts/publish-release.mjs --handoff release/handoffs/r073y-baseline.json --verify-existing
```

The command writes machine state, cache records, visual-QA evidence references,
and the final receipt under ignored `.release/`. Re-running the same handoff is
idempotent: a stage is skipped only when its input fingerprint and every
declared output hash still match. The whole-site gate fingerprint includes HEAD,
tracked changes, and all non-ignored untracked files.

## State machine

| Stage | State after success | Meaning |
| --- | --- | --- |
| `intake` | `INTAKE_VALIDATED` | Frozen commit, artifact hashes, recap bindings, and ancestry verified |
| `generate` | `CONTENT_GENERATED` | Chinese HTML, homepage, index, site version, and accounting checked |
| `translate` | `TRANSLATION_VALIDATED` | Local direct translation snapshot and bundle checked |
| `bind` | `PDF_BOUND` | Synchronized note PDF and binding ledger checked |
| `gate` | `AUDIT_PASSED` | Existing publication gate plus full structural audit pass |
| `commit` | `COMMIT_CONFIRMED` | Only declared managed paths enter the release commit |
| `push` | `PUSH_CONFIRMED` | Explicitly authorized update to `origin/main` succeeds |
| `deploy` | `DEPLOYMENT_CONFIRMED` | GitHub Pages run for the exact publication commit succeeds |
| `qa` | `LIVE_QA_PASSED` | Live bytes/content types/site-version and visual evidence all pass |

Generation, translation, and binding are serialized because they write shared
artifacts. The publication gate and full structural audit run safely in
parallel. Live HTTP checks run concurrently. Independent failures are collected
and returned together, so one run exposes the complete actionable error list.

The required claim-boundary labels are always `PROVED`, `FINITE`, `OPEN`, and
`NOT CLAY`. A note-only handoff sets recap mode to `PRESERVE` and pins the latest
milestone recap HTML/PDF byte-for-byte. A milestone handoff sets recap mode to
`UPDATE` and declares the new recap endpoint explicitly.

## Contracts and receipts

- `contracts/research-publication-handoff.schema.json` is the machine-readable
  research-to-publication contract.
- `contracts/research-publication-receipt.schema.json` defines the concise
  result returned to the research task.
- `contracts/publication-visual-qa.schema.json` separates browser/PDF visual
  evidence from structural and byte-level checks.
- `handoffs/r073y-baseline.json` records the verified R0.73Y/R0.73X baseline.

Visual QA is deliberately not inferred from structural checks. The final stage
requires a `publication-visual-qa-v1` evidence file covering desktop, mobile,
every research-note PDF page, and every formal-figure PDF page.

For a new release, the normal sequence is to run the same entry point through
`deploy`, perform live browser and complete PDF visual review, write the visual
evidence file, then rerun through `qa`. The second invocation reuses every
unchanged cached stage; it is still the same idempotent entry point.
