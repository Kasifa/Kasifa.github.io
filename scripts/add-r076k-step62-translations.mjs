#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r076kstep62";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 265 research notes",
  "View the R0.76K card on the home page",
  "Current endpoint R0.76K Step 62 real dyadic single-slice lower bound",
  "The recap endpoint remains I. The I recap stays byte-exact; J and K both follow it, and neither triggers a new recap.",
  "The cumulative recap contains 203 nodes; the site now has 265 public research notes",
  "Previous major milestone recap (through I; does not cover J or K)",
  "Previous major milestone recap (through I, 203 sections; does not cover J or K)",
  "Jump to the R0.76K card on the home page →",
  "The complete-clock signed quotient, multiple bands, arbitrary nonlinear packets, Version-M extraction, regularity, and Clay remain OPEN.",
  "Research note R0.76K Step 62 · 2026-09-05 · REAL DYADIC EDGE SHARPNESS",
  "Read the latest R0.76K research note →",
  "Expand 175 public notes",
  "Review v2.41 · 2026-09-05",
  "K proves that real one-dyadic-band cosine packets already have the edge scale and linear endpoint factor. Every prescribed pair is realized exactly by an integer heat shear at one slice. The uniform construction covers the stated range, and the signed two-cap pairing closes only at that slice. The complete-clock quotient remains OPEN. NOT CLAY.",
  "K closes only the fixed single-slice lower bound and signed-cap pairing. The full upper-window lower range, complete-clock signed flux relative to full plateau mass, L3 endpoint optimality, multiple bands, nonconstant shear, arbitrary nonlinear packets, arbitrary-field E.24, Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later versions remain unauthorized, unread, and unpublished.",
  "R0.70A–R0.76K · 167 sections published",
  "R0.70A–R0.76K: 167 sections published, 104 fully archived",
  "R0.76K Step 62 proves fixed single-slice edge lower bounds and signed-cap pairing for real one-dyadic-band exact heat shears, throughout the stated range; the full upper-window lower bound and full-clock signed-flux/full-plateau quotient remain open.",
  "R0.76K: real one-band edge lower bounds and an exact heat-shear slice",
  "R0.76K | Real one-band edge lower bounds, exact heat shear, and a signed-cap slice",
  ", while the signed-cap pairing closes only at that slice.",
  "can all be realized by consecutive integer modes in one exact heat-shear slice. The uniform range is",
  "provides the clustered-Fourier historical background.",
  "full",
  "Literature review v2.41 · 2026-09-05",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.76K work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "lower bound, complete-clock signed flux/full-plateau quotient, L3 endpoint optimality, multiple bands, nonconstant shear, arbitrary nonlinear packets, arbitrary-field E.24, Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later versions remain unauthorized, unread, and unpublished.",
  "supports standard Legendre orthogonality and endpoint normalization.",
  "edge lower bound, linear",
  "endpoint factor, and exterior-interval lower bound; every prescribed",
  "LITERATURE: the complex confluent architecture and classical orthogonal-polynomial facts. PROVED LOCALLY: real conjugate pairing; one-dyadic-band pointwise and integrated lower bounds; the endpoint factor; an exact integer heat-shear slice; the varying-degree range; the signed two-cap slice identity; the exact semigroup formula; and the backward warning. FINITE COMPUTATION: binds 12 frozen objects, 118/118 Python assertions, 168/168 independent Ruby assertions, K.1–K.48, and 48 displays. MODE COUNT: q denotes positive cosine modes and therefore 2q complex branches; this is not relabelled as inclusion in complex T_q. OPEN: the full upper-window lower range, complete-clock signed flux/full-plateau quotient, L3 endpoint optimality, multiple bands, nonconstant shear, arbitrary nonlinear packets, arbitrary-field E.24, Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity.",
  "Proposition 7.1 supplies the established complex confluent Chebyshev architecture;",
  "R0.76K Step 62 real one-band lower bounds and fixed-slice boundary",
  "R0.76K Step 62 public boundary · REAL DYADIC EDGE SHARPNESS",
  "Step 62 proves that real one-dyadic-band cosine packets satisfy the",
  "265 public research notes; latest node R0.76K.",
  "Real one-band edge lower bounds, exact heat shear, and a signed-cap slice",
  "Research-note master index · v2.41 · 2026-09-05",
  "Latest node R0.76K · continuously revised",
  ", and the signed two-cap algebra also closes at that slice; however, the full",
  "489 / Full text",
  "490 / Full text",
  "491 / Full text",
  "492 / Full text",
  "493 / Full text",
  "494 / Full text",
  "495 / Full text",
  "496 / Full text",
  "This site is currently published through R0.76K Step 62. K proves only fixed single-slice lower bounds and a signed-cap slice result for real one-dyadic-band exact heat shears; the full",
  "View the previous major milestone recap (through I; does not cover J or K)",
  "'s edge scale and the endpoint's linear",
  "lower bound and complete-clock signed flux/full-plateau quotient remain unproved.",
  "Research note R0.76K · Step 62 · REAL DYADIC EDGE SHARPNESS",
  "factor already occur in real one-dyadic-band cosine packets, and the witnesses embed exactly into any one prescribed exact integer heat-shear slice. The uniform construction covers",
  "Status · R0.76K STEP 62",
  "Certificate: Python 118/118, Ruby 168/168, K.1--K.48, and 48/48 displays; byte stability across three Python hash seeds and regeneration; the implementations reject 118/118 and 168/168 targeted mutations respectively and both fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite certificates do not replace the continuum proof; this section contains no formal figure, simulation, DNS, or DGX.",
  "J's upper reconstruction and K's real one-band single-slice lower bound",
  "K / Frozen evidence",
  "K proves",
  "Step 62 main text",
  "Step 62 main text, source boundary, two certificate implementations, and fail-closed QA",
];

assert.equal(summaries.length, 61, "R0.76K Step 62 translation table length drift");

function withProtected(summary, source) {
  const tokens = extractProtectedTokens(source);
  return tokens.length === 0 ? summary : `${summary} ${tokens.join(" ")}`;
}

process.chdir(root);
const [source, order, current] = await Promise.all([
  collectSiteStrings(publicRoot), collectSiteStrings("./public"), readFile(translationPath, "utf8").then(JSON.parse),
]);
const rowPattern = new RegExp(`^${prefix}\\d+$`);
const baseCurrent = checkOnly ? current : current.filter((row) => !rowPattern.test(row.id));
const currentByZh = new Map(baseCurrent.map((entry) => [entry.zh, entry]));
const missing = source.filter((entry) => !currentByZh.has(entry.zh));
const missingOrder = order.filter((entry) => !currentByZh.has(entry.zh));

if (checkOnly) {
  assert.equal(missing.length, 0, "site still has untranslated Chinese strings");
  const rows = current.filter((row) => rowPattern.test(row.id));
  assert.equal(rows.length, summaries.length, "R0.76K Step 62 translation count drift");
  assert.deepEqual(rows.map((row) => row.en), rows.map((row, i) => withProtected(summaries[i], row.zh)), "R0.76K English translation drift");
} else {
  assert.equal(missing.length, summaries.length, "R0.76K Step 62 source-string count drift");
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

process.stdout.write(`${JSON.stringify({ release: "R0.76K Step 62", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: summaries.length, applied: !checkOnly }, null, 2)}\n`);
