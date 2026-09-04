#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r076gstep58";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 261 research notes",
  "View the R0.76G card on the home page",
  "Current endpoint R0.76G Step 58 complete-clock central-fibre flux lower bound",
  "Jump to the R0.76G card on the home page →",
  "Research note R0.76G Step 58 · 2026-09-05 · COMPLETE-CLOCK CENTRAL-FIBRE FLUX LOWER BOUND",
  "Read the latest R0.76G research note →",
  "Expand 171 public notes",
  "Review v2.37 · 2026-09-05",
  "G chooses m=floor(a²/1024), q=2m+1, and the nonzero drift B=-βa/R, and proves on the complete frozen clock that the complete signed collar flux grows at least as β(9/7)^(4m) relative to a central-fibre proxy. The denominator is not the full physical plateau mass; no E.24, Version-M, regularity, or singularity counterexample is claimed. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Using an exact real dyadic packet with nonzero drift, G proves on the complete frozen clock that the complete signed collar flux grows at least as β(9/7)^(4m) relative to a central-fibre proxy, with q/L²→2/3969. It does not transfer to a full-plateau lower bound. NO NOVELTY CLAIM. NOT CLAY.",
  "H is in the sole FIFO publication queue but remains unread and unpublished until G completes full online verification. G's complete signed-flux lower bound uses a central-fibre proxy; it cannot be replaced by the full physical plateau mass and is not a counterexample to E, E.24, or Version-M. Full-plateau mode dependence, the optimal exponential base, arbitrary packets, nonconstant shears, Version-M membership and extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open.",
  "The cumulative recap after R0.60 contains 191 nodes; the site now has 261 public research notes",
  "R0.70A–R0.76G · 163 sections published",
  "R0.70A–R0.76G: 163 sections published, 104 fully archived",
  "R0.76G Step 58 constructs an exact real dyadic shear with nonzero drift and gives an exp(cq) lower bound on the complete frozen-clock signed collar flux relative to a central-fibre proxy; the denominator is not the full physical plateau mass, so this is not a counterexample to E, E.24, or Version-M.",
  "R0.76G: exponential lower bound for complete-clock central-fibre flux",
  "R0.76G | Exponential lower bound for complete-clock central-fibre flux",
  ", and proves on the complete frozen clock that the complete signed collar flux relative to the central-fibre proxy grows at least as",
  ". The denominator is not the full physical plateau mass, so this is not a counterexample to E, E.24, or Version-M.",
  "give the thickness and spectral-inequality background for heat observability; ",
  "record small-time cost, geometry, and vanishing structure; ",
  "Open interface · R0.76H",
  "provide the exponential-polynomial boundary inherited from F. G imports no observability theorem and proves its local functional using an explicit periodic Gaussian expectation and elementary moment estimates; the bounded search does not establish completeness, novelty, or priority.",
  "Literature review v2.37 · 2026-09-05",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.76G work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "and the nonzero drift",
  "growth, with",
  "H is in the sole FIFO publication queue but remains unread and unpublished until G completes full online verification. Full-plateau mode dependence, the optimal exponential base, arbitrary packets, nonconstant shears, Version-M membership and extraction, arbitrary-field E.24, fixed deletion, suitable-weak transfer, regularity, and singularity remain open.",
  "PROVED: take m=floor(a²/1024), q=2m+1, positive modes 2m,...,4m, β=1/100, and B=-βa/R. This gives an exact real smooth unforced NSE shear. On the complete scaled clock 0<=s<=4, the ratio of the complete signed flux to the central-fibre L3 proxy is at least c*β(9/7)^(4m). Moreover q(L)/L²→2/3969, and the normalized liminf rate is greater than 2/35721. SIGN AND CLOCK: the cutoff equals one on the terminal interval (3,4); the positive cap is favourable, the negative cap is the only adverse contribution, its base ratio is 4/9, and the central upper base follows from 233/200<7/6. SOURCE BOUNDARY: surrounding heat-observability and Remez literature does not state G's signed shrinking-collar functional; G makes no novelty, priority, or optimal-base claim. OPEN: M_L^I is not the full physical plateau mass. Full-plateau mode dependence, the optimal exponential base, arbitrary packets, nonconstant shears, Version-M membership or extraction, arbitrary-field E.24, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Finite checks do not replace the Gaussian limiting lemma; there is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.76G Step 58 bounded primary-source screen and claim boundary",
  "R0.76G Step 58 public boundary · COMPLETE-CLOCK CENTRAL-FIBRE FLUX LOWER BOUND",
  "Step 58 takes",
  "261 public research notes; latest node R0.76G.",
  "Exponential lower bound for complete-clock central-fibre flux",
  "Research-note master index · v2.37 · 2026-09-05",
  "Latest node R0.76G · continuously revised",
  ". The denominator is not the full physical plateau mass, so this is not a counterexample to E, E.24, or Version-M.",
  "456 / Full text",
  "457 / Full text",
  "458 / Full text",
  "459 / Full text",
  "460 / Full text",
  "461 / Full text",
  "462 / Full text",
  "463 / Full text",
  "464 / Full text",
  "This site is currently published through R0.76G Step 58. H is in the sole FIFO publication queue but remains unread and unpublished until G completes full online verification. G's lower bound concerns the complete signed flux on the full clock, but its denominator is only a central-fibre proxy; it cannot be replaced by the full physical plateau mass and is not a counterexample to R0.76E, E.24, or Version-M. Full-plateau mode dependence, the optimal exponential base, arbitrary packets, nonconstant shears, Version-M membership and extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open.",
  "Research note R0.76G · Step 58 · COMPLETE-CLOCK CENTRAL-FIBRE FLUX LOWER BOUND",
  "Status · R0.76G STEP 58",
  "Certificate: Python 120/120, Ruby 120/120, G.1--G.40, and 40/40 displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 120/120 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite checks do not replace the continuum proof of the Gaussian limiting lemma. This section contains no formal figure, simulation, DNS, or DGX.",
  "F's spatial obstruction and G's complete-clock signed-flux obstruction",
  "G / Frozen evidence",
  "G advances F's zero-drift spatial-observation obstruction to nonzero drift, the complete frozen clock, and the fully integrated signed collar flux: for an explicit exact real dyadic shear, the ratio of the complete signed flux to the central-fibre proxy grows at least as",
  "Step 58 main text",
  "Step 58 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
];

assert.equal(summaries.length, 55, "R0.76G Step 58 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.76G Step 58 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.76G Step 58 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.76G Step 58 source-string count drift");
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
  release: "R0.76G Step 58",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
