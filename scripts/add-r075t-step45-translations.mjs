#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075tstep45";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 248 research notes",
  "View the R0.75T card on the home page",
  "Current endpoint R0.75T Step 45 two-harmonic spatial collar coercivity",
  "For one high-carrier dyadic pair, T proves exact two-wave spatial collar coercivity with an explicit beat defect, while retaining the time-slice corollary with unequal heat damping and the four nonconstant flux frequencies. It is not a complete two-mode temporal payment. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "The spatial collar coercivity holds, with an explicit beat defect recording amplitude mismatch, beat scale, and distance from the cancelling phase. The time-slice corollary retains unequal heat rates, but the weighted temporal difference-frequency payment remains unproved. NO NOVELTY CLAIM. NOT CLAY.",
  "Jump to the R0.75T card on the home page →",
  "Exactly two real harmonics in the same dyadic band satisfy",
  "Research note R0.75T Step 45 · 2026-09-04 · TWO-HARMONIC SPATIAL COLLAR COERCIVITY",
  "Read the latest R0.75T research note →",
  "Expand 158 public notes",
  "Review v2.24 · 2026-09-04",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 248 public research notes",
  "R0.70A–R0.75T · 150 sections published",
  "R0.70A–R0.75T: 150 sections published, 104 fully archived",
  "R0.75T Step 45 closes spatial two-harmonic collar coercivity for one high-carrier dyadic pair, with a sharp beat defect that precisely records destructive interference; the weighted temporal difference-frequency estimate and complete two-harmonic payment remain open.",
  "R0.75T: spatial collar coercivity for one two-harmonic dyadic pair",
  "R0.75T | Spatial collar coercivity for one two-harmonic dyadic pair",
  "T still does not control the low difference-frequency row in the exact flux as it moves with the beat defect, and it does not prove complete two-harmonic signed-flux payment. Low-carrier pairs, three or more harmonics, arbitrary packets, nonconstant shear, vertical dependence, projection, E.24, and Version-M extraction remain open. Later work was not authorized, read, or published.",
  "The same moving beat defect must still pay the exact flux's low difference-frequency row while remaining compatible with the self and sum rows. Complete two-harmonic payment, low carriers, three or more harmonics, arbitrary packets, nonconstant shear, vertical dependence, projection, E.24, and Version-M extraction are all open. Later material was not authorized, read, or published.",
  "Literature review v2.24 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75T work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Kovrizhkin 2000 and Egidi--Veselic 2020 provide adjacent Logvinenko--Sereda and observability background for bounded spectral pieces and torus spectral subspaces. They do not provide T's exact two-real-wave defect, shrinking radial plateau fibre, or the unproved temporal row T.31. T's continuum inequality is proved directly by a local elementary Gram/coercivity argument and does not invoke those external theorems. A finite search establishes no completeness, novelty, or priority conclusion.",
  "PROVED: exact plateau fibre T.10; uniform slow-envelope sampling T.13; sharp unresolved-beat defect T.21--T.24; resolved-beat gap T.25--T.27; spatial cubic coercivity T.3; unequal-rate diffusive time-slice corollary T.6; and four-frequency flux identity T.30. OPEN: weighted temporal difference-frequency estimate T.31, complete two-harmonic signed-flux payment, low-carrier pairs, three or more harmonics, arbitrary packets, inter-packet aggregation, nonconstant or vertically dependent shear, projection, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity. T does not conflict with R's growing-mode obstruction. There is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75T Step 45 bounded primary-source screen and claim boundary",
  "R0.75T Step 45 public boundary · SPATIAL TWO-HARMONIC SCOPE",
  "Under the high-carrier condition, Step 45 proves phase-sharp spatial collar coercivity for exactly two real harmonics in the same dyadic band. The exact beat defect records amplitude mismatch, beat scale, and cancelling relative phase. The diffusive corollary retains unequal heat rates and the four-frequency flux identity is expanded exactly, but the weighted temporal difference-frequency estimate remains open.",
  "248 public research notes; latest node R0.75T.",
  "Spatial collar coercivity for one two-harmonic dyadic pair",
  "Research-note master index · v2.24 · 2026-09-04",
  "Latest node R0.75T · continuously revised",
  "351 / Full text",
  "352 / Full text",
  "353 / Full text",
  "354 / Full text",
  "355 / Full text",
  "356 / Full text",
  "357 / Full text",
  "This site stops at R0.75T Step 45. T proves only the high-carrier dyadic pair's spatial collar coercivity, exact diffusive time-slice corollary, and four-frequency flux identity. It does not prove the weighted temporal difference-frequency estimate or complete two-harmonic signed-flux payment, and it does not cover low-carrier pairs, three or more harmonics, arbitrary packets, nonconstant shear, vertical dependence, projection, E.24, or Version-M extraction. Later work was not authorized, read, or published.",
  "Under the high-carrier condition, the physical plateau collar's spatial cubic mass is controlled by an explicit beat defect. The degeneracy rate is sharp; the exact diffusive pair yields only a time-slice corollary and four-frequency flux identity, not a complete two-mode temporal payment.",
  "For exactly two real harmonics in the same dyadic band,",
  "Research note R0.75T · Step 45 · TWO-HARMONIC SPATIAL COLLAR COERCIVITY",
  "Status · R0.75T STEP 45",
  "Certificate: Python 14/14, Ruby 15/15, T.1--T.31, 31/31 tags, and 32/32 displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 52/52 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite probes do not prove continuum coercivity constants. This section contains no formal figure, simulation, numerical fit, DNS, or DGX.",
  "Step 45 main text",
  "Step 45 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
  "T / Frozen evidence",
];

assert.equal(summaries.length, 46, "R0.75T Step 45 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75T Step 45 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75T Step 45 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75T Step 45 source-string count drift");
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
  release: "R0.75T Step 45",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
