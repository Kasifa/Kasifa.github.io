# Research publication workflow

This directory defines the independent publication boundary. Research hands off
only committed, hash-pinned artifacts. Publication code may translate, typeset,
audit, push, monitor, and verify those artifacts; it must not edit the
mathematical proof, theorem quantifiers, certificate payloads, formal-figure
scientific data, or research route.

## Single entry point

Use the bundled/local Node runtime to run:

```text
node scripts/publish-release.mjs --handoff release/handoffs/<release>.json --allow-commit --allow-push
```

Routine translation is fixed to `LOCAL_DIRECT_NO_DGX`. The handoff cannot
provide arbitrary commands: the pipeline derives and enforces its release-owned
generation and translation scripts. Legacy PDF-bearing contracts also derive a
binding script. New contracts set `artifactPolicy.readerPdf=OMIT_NEW`, omit the
bind script, require the new PDF URL to remain absent, and set
`scientificFigure=NOT_REQUIRED` when the frozen package needs no scientific
figure.

For a deployed baseline, use the read-only path:

```text
node scripts/publish-release.mjs --handoff release/handoffs/r073y-baseline.json --verify-existing
```

That legacy handoff can still verify its local and deployment-era contract, but
it predates `visualQa.configPath`. Until it is migrated to a generic browser
configuration, running it through `qa` must stop as awaiting fresh browser
evidence and must not be described as a complete current online verification.

The command prints one compact PASS/FAIL line and writes machine state, cache
records, complete stage logs, visual-QA evidence, screenshots, and the full
receipt under ignored `.release/`. Re-running the same handoff is idempotent for
deterministic local stages only: a stage is reused only when its inputs,
declared output hashes, runtime identity, dependency lock, and shared pipeline
modules still match. Commit, push, GitHub Actions deployment lookup, live object
verification, and browser QA are always fresh.

Read local state without network access or writes:

```text
node scripts/publish-release.mjs --status <release-id>
```

## State machine

| Stage | State after success | Meaning |
| --- | --- | --- |
| `intake` | `INTAKE_VALIDATED` | Frozen commit, artifact hashes, recap bindings, and ancestry verified |
| `generate` | `CONTENT_GENERATED` | Chinese HTML, homepage, index, site version, and accounting checked |
| `translate` | `TRANSLATION_VALIDATED` | Local direct translation snapshot and bundle checked |
| `bind` | `PDF_BOUND` or `HTML_ARTIFACTS_BOUND` | Legacy PDF binding checked, or explicitly omitted by the HTML-only policy |
| `gate` | `AUDIT_PASSED` | Existing publication gate plus full structural audit pass |
| `commit` | `COMMIT_CONFIRMED` | Only declared managed paths enter the release commit |
| `push` | `PUSH_CONFIRMED` | Explicitly authorized update to `origin/main` succeeds |
| `deploy` | `DEPLOYMENT_CONFIRMED` | GitHub Pages run for the exact publication commit succeeds |
| `qa` | `LIVE_QA_PASSED` | Live bytes/content types/site-version and visual evidence all pass |

Generation, translation, and binding are serialized because they write shared
artifacts. The publication gate and full structural audit run safely in
parallel. Live HTTP checks run concurrently. GitHub Actions is polled
programmatically; the model does not poll it. Independent failures are
collected and returned together, so one run exposes the complete actionable
error list.

The required claim-boundary labels are always `PROVED`, `FINITE`, `OPEN`, and
`NOT CLAY`. A note-only handoff sets recap mode to `PRESERVE` and pins existing
milestone recap artifacts byte-for-byte. A milestone handoff sets recap mode to
`UPDATE` and declares the new recap endpoint explicitly. The no-new-PDF rule
does not delete or rewrite historical note or recap PDFs.

## Contracts and receipts

- `contracts/research-publication-handoff.schema.json` is the machine-readable
  research-to-publication contract.
- `contracts/research-publication-receipt.schema.json` defines the concise
  publication/management receipt. It is not sent back to the research task and
  does not trigger an extra research turn.
- `contracts/publication-visual-qa.schema.json` separates browser/PDF visual
  evidence from structural and byte-level checks.
- `handoffs/r073y-baseline.json` records the verified R0.73Y/R0.73X baseline.

Visual QA is deliberately not inferred from structural checks. The final stage
requires a versioned generic browser configuration and produces fresh
`publication-visual-qa-v1` evidence. It checks desktop/mobile, light/dark,
Chinese/English, MathJax errors and residual TeX, real theme application,
horizontal overflow, page errors, release-specific claim boundaries, and
retained screenshots. Legacy PDF or formal-figure page review remains required
only when those artifacts are in the contract.

The current Clay-B configuration demonstrates the generic engines:

```text
node scripts/qa-publication-browser.mjs --config release/qa/clay-b-signed-scale-20260905.json --commit <sha>
node scripts/verify-publication-online.mjs --config release/qa/clay-b-signed-scale-20260905.json --commit <sha>
```

Normal output is compact. Add `--json` to print the full result; either way the
complete reports remain under `.release/reports/<release-id>/`.

For a new release, the normal sequence is one entry point through `qa`.
Deterministic unchanged work may resume from cache, while deployment status,
online objects, and browser scenarios are executed again on every QA run.
