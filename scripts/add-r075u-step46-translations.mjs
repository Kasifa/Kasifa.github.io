#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075ustep46";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 249 research notes",
  "View the R0.75U card on the home page",
  "Current endpoint R0.75U Step 46 difference-frequency complete-clock payment",
  "logarithmic rate. The joint payment of the two self-frequency rows and the sum-frequency row remains open; this is not a complete two-harmonic signed-flux theorem. NO NOVELTY CLAIM. NOT CLAY.",
  "For one exact diffusive high-carrier two-harmonic dyadic pair, U uses the weighted moving-phase lemma to pay the low difference-frequency flux row over the complete clock while retaining the exact",
  "For one exact diffusive high-carrier two-harmonic dyadic pair, U uses the weighted moving-phase lemma to pay the low difference-frequency row over the complete clock. The amplitude and every power of R cancel exactly, retaining the -2/11907 logarithmic rate. The self/sum block and complete two-mode payment remain open. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Jump to the R0.75U card on the home page →",
  "Research note R0.75U Step 46 · 2026-09-04 · DIFFERENCE-FREQUENCY COMPLETE-CLOCK PAYMENT",
  "Read the latest R0.75U research note →",
  "Expand 159 public notes",
  "Review v2.25 · 2026-09-04",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 249 public research notes",
  "R0.70A–R0.75U · 151 sections published",
  "R0.70A–R0.75U: 151 sections published, 104 fully archived",
  "R0.75U Step 46 uses the weighted moving-phase lemma to pay the low difference-frequency row of one exact high-carrier two-harmonic dyadic pair while retaining the exact -2/11907 rate; the combined self/sum block and complete two-harmonic payment remain open.",
  "R0.75U: complete-clock difference-frequency payment for one two-harmonic dyadic pair",
  "R0.75U | Complete-clock difference-frequency payment for one two-harmonic dyadic pair",
  "U pays the exact flux's low difference-frequency row, but it does not jointly control the two self-frequency rows and the sum-frequency row and does not prove complete two-harmonic signed-flux payment. Low-carrier pairs, three or more harmonics, arbitrary packets, inter-packet aggregation, nonconstant or vertical shear, projection, E.24, and Version-M extraction remain open. Later work was not authorized, read, or published.",
  "Literature review v2.25 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75U work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Bedrossian--Vicol--Wang, Egidi--Veselic, and Wang--Wang--Zhang--Zhang provide only adjacent context on shear mixing, spectral observability, and heat observability. U's weighted moving-phase lemma U.13 and exact difference-frequency payment U.4 are proved by local elementary arguments and import none of those external theorems. A finite search establishes no completeness, novelty, or priority conclusion.",
  "PROVED: the uniform radial quotient U.10; the weighted complete-clock moving-phase lemma U.13 and its slow/fast and weak/strong-heat proof U.14--U.20; exact scaling and amplitude cancellation U.21--U.24; the difference-frequency payment U.4; the normalized estimate U.6--U.7; and the exact smooth unforced shear solution U.27. CONDITIONAL: U.28, as in S, requires the complete clock and plateau tube to align with the same scale-2R Version-M measurement row and F to be a coordinate component of the same actual velocity. OPEN: the combined self-frequency rows 2k and 2m and sum-frequency row k+m; a complete two-harmonic signed-flux theorem; low-carrier pairs; three or more harmonics; arbitrary packets; inter-packet aggregation; nonconstant or vertically dependent shear; projection; arbitrary-field E.24; complete Version-M extraction; fixed deletion; suitable-weak transfer; regularity; and singularity. Fixed-grid fast-phase quadrature is not proof evidence. There is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75U Step 46 bounded primary-source screen and claim boundary",
  "R0.75U Step 46 public boundary · DIFFERENCE-FREQUENCY COMPLETE-CLOCK SCOPE",
  "Step 46 pays the low difference-frequency row U.4 for one exact diffusive high-carrier two-harmonic dyadic pair using the weighted moving-phase lemma U.13, uniform radial quotient U.10, and T's frozen spatial coercivity. The amplitude and every power of R cancel exactly, and the normalized L^2 rate is -2/11907.",
  "The joint payment of the two self-frequency rows and the sum-frequency row, a complete two-harmonic signed-flux theorem, low carriers, three or more harmonics, arbitrary packets, inter-packet aggregation, nonconstant or vertical shear, projection, E.24, and Version-M extraction all remain open. Later material was not authorized, read, or published.",
  "249 public research notes; latest node R0.75U.",
  "Complete-clock difference-frequency payment for one two-harmonic dyadic pair",
  "Research-note master index · v2.25 · 2026-09-04",
  "Latest node R0.75U · continuously revised",
  "358 / Full text",
  "359 / Full text",
  "360 / Full text",
  "361 / Full text",
  "362 / Full text",
  "363 / Full text",
  "This site stops at R0.75U Step 46. U pays only the difference-frequency component of one exact diffusive high-carrier two-harmonic dyadic pair. Joint payment of the two self-frequency rows and the sum-frequency row, a complete two-harmonic signed-flux theorem, low carriers, three or more harmonics, arbitrary packets, inter-packet aggregation, nonconstant or vertical shear, projection, E.24, and Version-M extraction remain open. Later work was not authorized, read, or published.",
  "logarithmic rate. The joint payment of the self frequencies and the sum frequency remains open; this is not a complete two-harmonic signed-flux theorem.",
  "For one exact diffusive high-carrier two-harmonic dyadic pair, U uses the weighted moving-phase lemma to pay the low difference-frequency flux row over the complete clock while retaining the exact",
  "Research note R0.75U · Step 46 · DIFFERENCE-FREQUENCY COMPLETE-CLOCK PAYMENT",
  "Status · R0.75U STEP 46",
  "Certificate: Python 16/16, Ruby 17/17, U.1--U.28, 28/28 tags, and 28/28 displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 61/61 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Fixed-grid fast-phase quadrature carries no proof weight. This section contains no formal figure, simulation, numerical fit, DNS, or DGX.",
  "Step 46 main text",
  "Step 46 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
  "U / Frozen evidence",
];

assert.equal(summaries.length, 45, "R0.75U Step 46 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75U Step 46 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75U Step 46 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75U Step 46 source-string count drift");
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
  release: "R0.75U Step 46",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
