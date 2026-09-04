#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r076jstep61";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 264 research notes",
  "View the R0.76J card on the home page",
  "Current endpoint R0.76J Step 61 local edge reconstruction",
  "The recap endpoint remains I. The I recap remains byte-exact; J is the subsequent local-reconstruction node and does not trigger a new recap.",
  "The cumulative recap contains 203 nodes; the site now has 264 public research notes",
  "Previous major milestone recap (through I)",
  "Previous major milestone recap R0.61–R0.76I · 2026-09-05",
  "Previous major milestone recap (through I, 203 sections)",
  "Jump to the R0.76J card on the home page →",
  "Research note R0.76J Step 61 · 2026-09-05 · LOCAL EDGE EXTRAPOLATION RECONSTRUCTION",
  "Read the complete cumulative recap through I →",
  "Read the latest R0.76J research note →",
  "Expand 174 public notes",
  "Review v2.40 · 2026-09-05",
  "J locally reconstructs the exact-shear endpoint theorem. Optimal constants, a matching lower bound, multiple bands, nonconstant shear, arbitrary nonlinear packets, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. I's historical CONDITIONAL-LITERATURE label remains unchanged. Later versions remain unauthorized, unread, and unpublished.",
  "Using a finite vertical-line Takenaka–Malmquist basis, Laguerre majorants, and half-line tail recovery, J locally proves the endpoint extrapolation needed for exact real one-band constant shears. The complete cost is q⁷ exp(20√2q√Δ_a), the sufficient window remains q=o(L^(5/2)), and the exact normalized rate remains -2/11907. PROVED LOCALLY FROM ESTABLISHED LITERATURE. NOT CLAY.",
  "Multiple bands, arbitrary nonlinear packets, Version-M extraction, regularity, and Clay remain OPEN.",
  "R0.70A–R0.76J · 166 sections published",
  "R0.70A–R0.76J: 166 sections published, 104 fully archived",
  "R0.76J Step 61 locally reconstructs the endpoint extrapolation needed for exact real one-band constant shears, so the q=o(L^(5/2)) window no longer depends on Zhang Proposition 4.2; the result does not cover arbitrary Navier–Stokes fields, Version-M, or regularity.",
  "R0.76J: local endpoint reconstruction removes the exact-shear literature condition",
  "R0.76J | Local endpoint extrapolation removes the literature condition on the exact-shear window",
  ", still giving",
  ", with complete cost",
  ". Zhang Proposition 4.2 is used only for architectural and sharper-constant comparison, not as an input to J's theorem.",
  "'s Markov inequality and the Kós endpoint estimate are the established peer-reviewed inputs retained by J.",
  "Literature review v2.40 · 2026-09-05",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.76J work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Optimal constants, a matching exact-shear lower bound, multiple bands, nonconstant shear, arbitrary nonlinear packets, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later versions remain unauthorized, unread, and unpublished.",
  "LITERATURE: the Erdelyi Markov and Kós endpoint estimates. PROVED LOCALLY: the vertical-line Takenaka–Malmquist basis, Volterra/Laguerre coefficient formula, positive and negative half-line majorants, weighted tail recovery, half-line comparison, and finite endpoint theorem. PROVED LOCALLY FROM ESTABLISHED LITERATURE: the q⁷ exp(20√2q√Δ_a) complete cost, q=o(L^(5/2)) window, and normalized rate -2/11907 for exact real one-band constant shears. FINITE COMPUTATION: binds 12 frozen objects, constants, powers, signs, J.1–J.46, and 48 displays. HISTORICAL BOUNDARY: I's CONDITIONAL-LITERATURE status is preserved and is not rewritten by J. OPEN: optimal constants, a matching exact-shear lower bound, multiple bands, nonconstant shear, arbitrary nonlinear packets, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity.",
  "Proposition 4.2 is used only for proof architecture and sharper-constant comparison; J imports no theorem from it.",
  "R0.76J Step 61 local endpoint reconstruction and exact-shear boundary",
  "R0.76J Step 61 public boundary · LOCAL EDGE EXTRAPOLATION RECONSTRUCTION",
  "Step 61 locally proves the exact-shear endpoint inequality using a finite vertical-line Takenaka–Malmquist basis, Laguerre majorants, and half-line tail recovery; the spatial cost is",
  "264 public research notes; latest node R0.76J.",
  "Local endpoint extrapolation removes the literature condition on the exact-shear window",
  "Research-note master index · v2.40 · 2026-09-05",
  "Latest node R0.76J · continuously revised",
  ", while the exact normalized rate remains",
  "; the sufficient window remains",
  "481 / Full text",
  "482 / Full text",
  "483 / Full text",
  "484 / Full text",
  "485 / Full text",
  "486 / Full text",
  "487 / Full text",
  "488 / Full text",
  "This site is currently published through R0.76J Step 61. J locally reconstructs endpoint extrapolation within the exact real one-band constant-shear family, but optimal constants, a matching lower bound, multiple bands, nonconstant shear, arbitrary nonlinear packets, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. I's historical CONDITIONAL-LITERATURE label is not rewritten. Later versions remain unauthorized, unread, and unpublished.",
  "View the previous major milestone recap (through I)",
  "Recap PDF through I",
  "Research note R0.76J · Step 61 · LOCAL EDGE EXTRAPOLATION RECONSTRUCTION",
  "Status · R0.76J STEP 61",
  "Certificate: Python 96/96, Ruby 107/107, J.1--J.46, and 48/48 displays; byte stability across three Python hash seeds and regeneration; the implementations reject 96/96 and 107/107 targeted mutations respectively and both fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite certificates do not replace the continuum proof; this section contains no formal figure, simulation, DNS, or DGX.",
  "I's conditional window and J's local endpoint reconstruction",
  "J / Frozen evidence",
  "Using a finite vertical-line Takenaka–Malmquist basis, positive- and negative-time Laguerre majorants, and half-line tail recovery, J locally proves the endpoint extrapolation needed for exact real one-band constant shears. The spatial cost is",
  "Step 61 main text",
  "Step 61 main text, source boundary, two certificate implementations, and fail-closed QA",
];

assert.equal(summaries.length, 59, "R0.76J Step 61 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.76J Step 61 translation count drift");
  assert.deepEqual(rows.map((row) => row.en), rows.map((row, i) => withProtected(summaries[i], row.zh)), "R0.76J English translation drift");
} else {
  assert.equal(missing.length, summaries.length, "R0.76J Step 61 source-string count drift");
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

process.stdout.write(`${JSON.stringify({ release: "R0.76J Step 61", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: summaries.length, applied: !checkOnly }, null, 2)}\n`);
