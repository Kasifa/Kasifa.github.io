#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075xstep49";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 252 research notes",
  "View the R0.75X card on the home page",
  "Current endpoint R0.75X Step 49 fixed-finite low-carrier payment",
  "Jump to the R0.75X card on the home page →",
  "Research note R0.75X Step 49 · 2026-09-04 · FIXED FINITE LOW CARRIER",
  "Read the latest R0.75X research note →",
  "Expand 162 public notes",
  "Review v2.28 · 2026-09-04",
  "Latest milestone recap remains through W",
  "Latest cumulative recap remains through R0.75W (191 nodes)",
  "The cumulative recap after R0.60 contains 191 nodes; the site now has 252 public research notes",
  "R0.70A–R0.75X · 154 sections published",
  "R0.70A–R0.75X: 154 sections published, 104 fully archived",
  "R0.75X Step 49 extends W's low-carrier local-energy route to every fixed finite q real harmonic family in one dyadic band. C_q may depend on fixed q but not on frequencies, gaps, amplitudes, phases, R, or B. Quantitative q-growth, the high-carrier three-plus-mode sector, arbitrary packets, and general Version-M transfer remain open.",
  "R0.75X: low-carrier signed-flux payment for a fixed finite harmonic family",
  "R0.75X | Low-carrier signed-flux payment for a fixed finite harmonic family",
  "For every fixed finite q, X proves complete low-carrier signed-flux payment in one dyadic band under n_1aR<C_0. The 2q-state confluent observation and 2q-term trace use no gap divisor. There is no uniform q-growth bound; high carriers for three or more modes and arbitrary packets remain open. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "X uses a 2q-state confluent observation, an at-most-2q-term Turan–Nazarov terminal trace, and W's exact local-energy identity to pay low-carrier signed flux for every fixed finite q. The constant C_q has no uniform q-growth control; high carriers for three or more modes and arbitrary packets remain open. NO NOVELTY CLAIM. NOT CLAY.",
  "X closes only the low-carrier single-band family for each fixed finite q. Quantitative control for q=q(L), the high-carrier three-plus-mode sector, arbitrary packets, inter-packet aggregation, nonconstant or vertical shear, projection, E.24, and Version-M extraction remain open. Later work was not authorized, read, or published.",
  "Preserved W milestone recap",
  "Preserved milestone recap through W",
  "Literature review v2.28 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75X work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Nazarov's 1993/1994 original record and Friedland–Yomdin's 2013 primary restatement provide the exponential-polynomial measurable-set inequality. Its constant is independent of imaginary frequencies and frequency gaps but retains term-count dependence. X proves the 2q-state confluent spatial observation, scaled kernel, and local-energy identity locally. The bounded search establishes no completeness, novelty, or priority conclusion.",
  "PROVED: X.10--X.14 low-carrier scaling; X.15--X.20 fixed-q 2q-state confluent observation; X.21--X.25 at-most-2q-term frequency-gap-free terminal trace; X.26--X.33 radial primitive and exact local-energy identity; X.34--X.35 physical payment; X.5--X.7 normalized estimate, cancellation of all R powers, and the -2/11907 rate; and X.36 exact smooth unforced shear. CONDITIONAL: any Version-M consequence still requires the measurement row, weight, realized subclass, actual component, and ledger alignment. OPEN: uniform quantitative q-growth; q=q(L); the high-carrier sector for three or more modes; arbitrary packets; inter-packet aggregation; nonconstant or vertically dependent shear; projection; arbitrary-field E.24; complete Version-M extraction; fixed deletion; suitable-weak transfer; regularity; and singularity. Finite checks do not replace continuum lemmas; there is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "The quantitative spatial constant for q=q(L), the high-carrier three-plus-mode sector, arbitrary packets, inter-packet aggregation, nonconstant or vertical shear, projection, E.24, and Version-M extraction remain open. Later material was not authorized, read, or published.",
  "R0.75X Step 49 bounded primary-source screen and claim boundary",
  "R0.75X Step 49 public boundary · FIXED FINITE q · LOW CARRIER ONLY",
  "Step 49 uses a 2q-state confluent spatial observation, an at-most-2q-term frequency-gap-free Turan–Nazarov terminal trace, and W's exact local-energy identity to pay the n_1aR<C_0 single-dyadic-band family for every fixed finite q. C_q has no uniform q-growth control, and the high-carrier sector for three or more modes remains open.",
  "252 public research notes; latest node R0.75X.",
  "Low-carrier signed-flux payment for a fixed finite harmonic family",
  "Research-note master index · v2.28 · 2026-09-04",
  "Latest node R0.75X · continuously revised",
  ", obtaining complete low-carrier signed collar-flux payment with constant C_q. The constant is independent of frequencies, gaps, amplitudes, phases, R, or B, but no uniform q-growth bound is proved; the high-carrier sector for three or more modes remains open. The exact logarithmic rate remains",
  ", one dyadic band, and",
  "384 / Full text",
  "385 / Full text",
  "386 / Full text",
  "387 / Full text",
  "388 / Full text",
  "389 / Full text",
  "390 / Full text",
  "391 / Full text",
  "392 / Full text",
  "Previous milestone cumulative recap through R0.75W",
  "This site stops at R0.75X Step 49. X pays only the low-carrier family in one dyadic band for each fixed finite q. Quantitative constants as q grows with L, the high-carrier sector for three or more modes, arbitrary packets, inter-packet aggregation, nonconstant or vertical shear, projection, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "Research note R0.75X · Step 49 · FIXED FINITE LOW CARRIER",
  "Status · R0.75X STEP 49",
  "Certificate: Python 18/18, Ruby 19/19, X.1--X.36, and 36/36 tags and displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 90/90 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite checks do not replace fixed-q continuum ODE compactness or the Turan–Nazarov lemma. This section contains no formal figure, simulation, DNS, or DGX.",
  "Step 49 main text",
  "Step 49 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
  "The exact roles of W and X",
  "X / Frozen evidence",
  "X extends W's low-carrier local-energy mechanism to every fixed finite real harmonic family: for fixed",
];

assert.equal(summaries.length, 54, "R0.75X Step 49 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75X Step 49 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75X Step 49 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75X Step 49 source-string count drift");
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
  release: "R0.75X Step 49",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
