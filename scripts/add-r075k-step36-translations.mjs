#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075kstep36";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 239 research notes",
  "View the R0.75K card on the home page",
  "Current endpoint R0.75K Step 36 high-frequency trace loss",
  "For a fixed nonnegative entrance weight, the quadratic trace stays positive while the local spacetime cubic mass of an explicit passive Fourier family decays like k^(-2), so the payment ratio grows like k^(4/3). The true signed flux is nevertheless exactly zero. The conclusion rules out only a fixed positive weight combined with the local cubic atom alone. NO NOVELTY CLAIM. NOT CLAY.",
  "The remaining options are to preserve signed or frequency cancellation, construct an auditable field-dependent or frequency-adapted test, or pay with another genuinely available Version-M trace or frequency row. Later work was not authorized, read, or published.",
  "Jump to the R0.75K card on the home page →",
  "The explicit smooth passive family leaves the fixed positive entrance row independent of frequency while the local spacetime cubic mass decays like k^(-2), so the ratio grows like k^(4/3); the actual signed flux is zero for every k. The result excludes only a fixed positive weight plus the local cubic atom alone. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Research note R0.75K Step 36 · 2026-09-04 · HIGH-FREQUENCY TRACE LOSS",
  "Read the latest R0.75K research note →",
  "Expand 149 public notes",
  "Review v2.15 · 2026-09-04",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 239 public research notes",
  "R0.70A–R0.75K · 141 sections published",
  "R0.70A–R0.75K: 141 sections published, 104 fully archived",
  "R0.75K Step 36 proves that the positive-majorant boundary row of a fixed nonnegative entrance weight cannot be paid uniformly in frequency by the local spacetime cubic atom alone. The actual signed flux is exactly zero, so this is a loss in the positivity proof rather than a counterexample to E.24.",
  "R0.75K: high-frequency trace loss for a fixed positive majorant",
  "R0.75K｜High-frequency trace loss for a fixed positive adjoint majorant",
  "Literature review v2.15 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75K work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Albritton--Dong support treating the constant-shear operator as a standard passive subfamily; Hu--Li provide context for positive off-diagonal semigroup methods; and Gardner--Liss--Mattingly show that pathwise shear-diffusion representations can retain dynamical information. None of the inspected sources converts a positive entrance row into the frozen Version-M cubic payment or proves E.24. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "PROVED: the smooth positive majorant K.4--K.7; the exact real passive family K.8--K.10; the frequency-independent boundary row K.11; the exact cubic mass and divergent ratio K.12--K.14; the zero actual signed flux K.15--K.16; and the general fixed-weight lemma K.17. LIMITED NO-GO: only a fixed nontrivial nonnegative entrance weight combined with the local spacetime cubic atom alone is excluded; this is positivity proof loss, not an E.24 counterexample. OPEN: signed kernels, field-dependent or frequency-adapted tests, other available Version-M trace or frequency payments, transition and periodic geometry, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity. There is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75K Step 36 bounded primary-source screen and claim boundary",
  "R0.75K Step 36 public boundary",
  "Signed kernels, field-dependent or frequency-adapted tests, and other genuinely available Version-M trace or frequency rows remain possible. Later work was not authorized, read, or published.",
  "Step 36 uses an exact passive Fourier family to prove that the boundary row of a fixed nontrivial nonnegative entrance weight stays positive while the local spacetime cubic atom decays like k^(-2), so the ratio grows like k^(4/3); the actual signed flux is exactly zero.",
  "239 public research notes; latest node R0.75K.",
  "High-frequency trace loss for a fixed positive adjoint majorant",
  "Research-note master index · v2.15 · 2026-09-04",
  "Latest node R0.75K · continuously revised",
  "286 / Full text",
  "287 / Full text",
  "288 / Full text",
  "289 / Full text",
  "290 / Full text",
  "291 / Full text",
  "292 / Full text",
  "293 / Full text",
  "A payment mechanism preserving signed or frequency information remains OPEN",
  "This site stops at R0.75K Step 36. A fixed nonnegative entrance weight combined with the local spacetime cubic atom alone is excluded by the high-frequency family, but signed kernels, field-dependent or frequency-adapted tests, and payment by another genuinely available Version-M trace or frequency row remain possible. Transition and periodic geometry, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "For a fixed nontrivial nonnegative entrance weight, the explicit high-frequency passive field keeps the initial quadratic trace positive while the local spacetime cubic mass",
  "diverges. Meanwhile, the true signed flux is exactly zero for every integer frequency: the zero mode introduced by positivity measures proof loss, not physical flux.",
  "decays, so the payment ratio",
  "Research note R0.75K · Step 36 · HIGH-FREQUENCY TRACE LOSS",
  "Status · R0.75K STEP 36",
  "Certificate: Python 19/19, Ruby 21/21, K.1--K.18 and 18/18 displays, byte stability across three Python hash seeds, and complete regeneration stability; both implementations reject all 100/100 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. This section contains no formal figure, simulation, numerical fit, DNS, or DGX.",
  "Step 36 main text",
  "Step 36 main text, primary-source boundary, two certificate implementations, and fail-closed QA"
];

assert.equal(summaries.length, 47, "R0.75K Step 36 translation table length drift");

function withProtected(summary, source) {
  const tokens = extractProtectedTokens(source);
  return tokens.length === 0 ? summary : `${summary} ${tokens.join(" ")}`;
}

process.chdir(root);
const [source, order, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  collectSiteStrings("./public"),
  readFile(translationPath, "utf8").then(JSON.parse),
]);
const rowPattern = new RegExp(`^${prefix}\\d+$`);
const baseCurrent = checkOnly ? current : current.filter((row) => !rowPattern.test(row.id));
const currentByZh = new Map(baseCurrent.map((entry) => [entry.zh, entry]));
const missing = source.filter((entry) => !currentByZh.has(entry.zh));
const missingOrder = order.filter((entry) => !currentByZh.has(entry.zh));

if (checkOnly) {
  assert.equal(missing.length, 0, "site still has untranslated Chinese strings");
  const rows = current.filter((row) => rowPattern.test(row.id));
  assert.equal(rows.length, summaries.length, "R0.75K Step 36 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75K Step 36 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75K Step 36 source-string count drift");
  const sourceByZh = new Map(missing.map((entry) => [entry.zh, entry]));
  const additions = missingOrder.map((orderedEntry, index) => {
    const entry = sourceByZh.get(orderedEntry.zh);
    assert.ok(entry, `absolute source entry missing ${orderedEntry.zh}`);
    const en = withProtected(summaries[index], entry.zh);
    assert.ok(!containsChinese(en), `Chinese remains in translation ${index + 1}`);
    assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(entry.zh), `protected token drift ${index + 1}`);
    return { id: `${prefix}${String(index + 1).padStart(3, "0")}`, ...entry, en };
  });
  await writeFile(translationPath, `${JSON.stringify([...baseCurrent, ...additions], null, 2)}\n`);
}

process.stdout.write(`${JSON.stringify({
  release: "R0.75K Step 36",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
