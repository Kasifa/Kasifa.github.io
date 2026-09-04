#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r076hstep59";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 262 research notes",
  "View the R0.76H card on the home page",
  "Current endpoint R0.76H Step 59 full-plateau absorption for the shifted packet",
  "Jump to the R0.76H card on the home page →",
  "Research note R0.76H Step 59 · 2026-09-05 · FULL-PLATEAU ABSORPTION FOR THE SHIFTED PACKET",
  "Read the latest R0.76H research note →",
  "Expand 172 public notes",
  "Review v2.38 · 2026-09-05",
  "For the same explicit shifted-binomial exact shear as G, H proves that adjacent fibres in the full plateau absorb the cap contrast at exp(O(m/a)) cost. The exact raw rate of the complete signed flux against the full-plateau mass is 3/40000, and the normalized rate is -2/11907. This kills only that candidate and does not extend to arbitrary packets, E.24, Version-M, regularity, or singularity. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "H closes only G's explicit shifted-binomial candidate. Arbitrary packets, different cap-localized families, nonconstant shears, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later versions remain unauthorized, unread, and unpublished.",
  "The cumulative recap after R0.60 contains 191 nodes; the site now has 262 public research notes",
  "R0.70A–R0.76H · 164 sections published",
  "R0.70A–R0.76H: 164 sections published, 104 fully archived",
  "R0.76H Step 59 proves that the full three-dimensional plateau absorbs G's same explicit shifted-binomial packet at exp(O(m/a)) cost. The raw quotient rate is 3/40000 and the exact normalized rate is -2/11907. The result kills only this candidate and does not extend to arbitrary packets or Version-M.",
  "R0.76H: the full plateau absorbs the explicit shifted-binomial candidate",
  "R0.76H | The full plateau absorbs the shifted-binomial obstruction",
  ", and the Gaussian moment comparison costs",
  ", while the normalized full-plateau quotient is exactly",
  ". The result kills only this explicit candidate.",
  ". The complete signed flux is eventually positive; the exact raw quotient rate is",
  "are retained only as G's frozen background. H's new implication follows entirely from the exact shell cross-section, the Gaussian moment expansion, Hölder, Jensen, and the same explicit packet. The bounded search does not establish completeness, novelty, or priority.",
  "Open interface · later versions",
  "Arbitrary packets, different cap-localized families, nonconstant shears, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later versions remain unauthorized, unread, and unpublished.",
  "Literature review v2.38 · 2026-09-05",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.76H work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "H imports no new observability, Remez, or control theorem.",
  "PROVED: for the same shifted-binomial exact smooth unforced shear as G, an adjacent strip of the full physical plateau pays the favourable cap at exp(O(m/a)) cost, and the complete signed flux is strictly positive for large L. The exact L² logarithmic rate of the raw quotient T_L/(M_L^plat)^(2/3) is 3/40000, while the exact rate of the normalized quotient X_L/(p_L^plat)^(2/3) is -2/11907. CANDIDATE BOUNDARY: this confirms G's central-fibre theorem while rigorously proving that the same packet is not a full-plateau counterexample. SOURCE BOUNDARY: H imports no external theorem; existing heat-observability and exponential-polynomial literature is context only, and no novelty, priority, or exhaustive-search claim is made. OPEN: improvement of R0.76E's uniform exp(Cq) loss; arbitrary real dyadic packets; different cap-localized families; nonconstant shears; arbitrary-field E.24; complete Version-M extraction; fixed deletion; suitable-weak transfer; regularity; and singularity. Finite checks do not replace the uniform Gaussian-moment comparison; there is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.76H Step 59 bounded source boundary and candidate-killing boundary",
  "R0.76H Step 59 public boundary · FULL-PLATEAU ABSORPTION FOR THE SHIFTED PACKET",
  "For the same shifted-binomial exact shear as G, Step 59 proves adjacent-plateau-strip payment: the cap and complete three-dimensional plateau fibres are only",
  "262 public research notes; latest node R0.76H.",
  "The full plateau absorbs the shifted-binomial obstruction",
  "Research-note master index · v2.38 · 2026-09-05",
  "Latest node R0.76H · continuously revised",
  ", and after normalization it returns exactly to",
  ". This rigorously kills the candidate but does not extend to arbitrary packets, E.24, or Version-M.",
  "465 / Full text",
  "466 / Full text",
  "467 / Full text",
  "468 / Full text",
  "469 / Full text",
  "470 / Full text",
  "471 / Full text",
  "This site is currently published through R0.76H Step 59. H kills only the same explicit shifted-binomial candidate as G: the full physical plateau absorbs its exponential contrast, and the exact normalized rate is -2/11907. Arbitrary packets, different cap-localized families, nonconstant shears, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later versions remain unauthorized, unread, and unpublished.",
  "cost to absorb the exponential contrast. The exact raw full-plateau quotient rate is",
  "away, complete three-dimensional plateau fibres absorb at",
  "Research note R0.76H · Step 59 · FULL-PLATEAU ABSORPTION FOR THE SHIFTED PACKET",
  "Status · R0.76H STEP 59",
  "Certificate: Python 126/126, Ruby 126/126, H.1--H.39, and 39/39 displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 126/126 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite checks do not replace the continuum proof of the uniform Gaussian-moment comparison. This section contains no formal figure, simulation, DNS, or DGX.",
  "G's central-fibre obstruction and H's full-plateau absorption",
  "H / Frozen evidence",
  "For the same explicit shifted-binomial exact shear as G, H completes the physical-denominator check: only",
  "Step 59 main text",
  "Step 59 main text, source boundary, two certificate implementations, and fail-closed QA",
];

assert.equal(summaries.length, 54, "R0.76H Step 59 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.76H Step 59 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.76H Step 59 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.76H Step 59 source-string count drift");
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
  release: "R0.76H Step 59",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
