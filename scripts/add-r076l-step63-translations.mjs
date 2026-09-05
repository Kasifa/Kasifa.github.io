#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r076lstep63";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "105 sections fully archived",
  "Master index of 266 research notes",
  "View the R0.76L card on the home page",
  "Current endpoint R0.76L Step 63: family-specific complete-clock absorption",
  "Frozen three-panel figure",
  "For the explicit start-prepaid real integer one-dyadic-band shear family, L proves eventual positivity of the complete signed collar flux in the stated degree window and gives two-sided bounds relative to the full physical plateau. The complete-clock edge residual drops from the fixed-slice scale to the stated exponential scale, while the normalized quadratic logarithmic rate remains -2/11907. The finite p=0.75 tilt sequence moves slightly away from its limit on the displayed grid; this is not an asymptotic counterexample. NOT CLAY.",
  "The recap endpoint remains I. The I recap stays byte-exact; J, K, and L all follow it, and none triggers a new recap.",
  "The cumulative recap contains 203 nodes; the site now has 266 public research notes",
  "Previous major milestone recap (through I; does not cover J, K, or L)",
  "Previous major milestone recap (through I, 203 sections; does not cover J, K, or L)",
  "Jump to the R0.76L card on the home page →",
  "Research note R0.76L Step 63 · 2026-09-05 · PARABOLIC EDGE COMPLETE CLOCK",
  "Read the latest R0.76L research note →",
  "Expand 176 public notes",
  "Review v2.42 · 2026-09-05",
  "L closes only the complete-clock sign and full-plateau payment for the explicit start-prepaid one-dyadic-band family in the stated window. The bulk-exterior saddle and candidate threshold at high degree, the transition near the upper boundary, arbitrary packets, Version-M, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later versions remain unauthorized, unread, and unpublished.",
  "The high-degree bulk saddle, arbitrary packets, Version-M extraction, regularity, and Clay remain OPEN.",
  "R0.70A–R0.76L · 168 sections published",
  "R0.70A–R0.76L: 168 sections published, 105 fully archived",
  "R0.76L frozen three-panel figure",
  "R0.76L Step 63 proves eventual complete-clock signed-flux positivity and full-plateau two-sided exponential bounds for the explicit start-prepaid real integer one-dyadic-band family in the stated window; the high-degree route remains open.",
  "R0.76L: parabolic edge smoothing and the complete-clock full-plateau residual",
  "R0.76L | Parabolic edge smoothing, complete-clock residual, and full-plateau two-sided bounds",
  ". This is a family-specific negative result;",
  "the formal threshold remains OPEN.",
  "two-sided bounds, while the frozen normalized quadratic logarithmic rate is",
  "provide modern polynomial heat-flow and Hermite context. Batahan–Shehata and Khan give fixed-scale Hermite–Chebyshev operational precedents, so no novelty is claimed for that operational idea.",
  "Literature review v2.42 · 2026-09-05",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.76L work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "support classical Chebyshev representations, derivatives, and interval inequalities;",
  "the complete signed collar flux is eventually positive, and the quotient relative to full physical plateau mass has",
  "bulk-exterior saddle, candidate threshold,",
  "LITERATURE: polynomial heat-flow formulas, Gaussian convolution, and classical Chebyshev/Gegenbauer facts. PROVED LOCALLY: the simultaneous growing-degree edge Laplace principle, fixed-edge tilt, finite-eta consecutive-integer exact-shear transfer, complete-clock positivity for the stated explicit family, full-plateau two-sided bounds, and normalized rate -2/11907. FINITE COMPUTATION: 24 frozen objects; Python 64/64; independent Ruby 279/279; 25/25 and 26/26 mutations; 11/11 sensitivity checks; 21/21 single-byte tamper checks; and a 16-row binary64 formal diagnostic. The p=0.75 tilt moves slightly away from its limit on the displayed grid and is not used as asymptotic evidence. OPEN: the high-degree bulk saddle and candidate threshold, the upper-boundary transition, arbitrary packets, Version-M, fixed deletion, suitable-weak transfer, regularity, and singularity.",
  "R0.76L Step 63 polynomial heat flow and family-specific complete-clock boundary",
  "R0.76L Step 63 public boundary · PARABOLIC EDGE COMPLETE CLOCK",
  "Step 63 proves for the explicit start-prepaid real integer one-dyadic-band shear family that, in",
  "transition, arbitrary packets, Version-M, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later versions remain unauthorized, unread, and unpublished.",
  "266 public research notes; latest node R0.76L.",
  "Parabolic edge smoothing, complete-clock residual, and full-plateau two-sided bounds",
  "Research-note master index · v2.42 · 2026-09-05",
  "Latest node R0.76L · continuously revised",
  ", the fixed-slice",
  ", so this explicit family is not a counterexample to the target estimate.",
  "497 / Full text",
  "498 / Full text",
  "499 / Full text",
  "500 / Full text",
  "501 / Full text",
  "502 / Full text",
  "503 / Full text",
  "504 / Full text",
  "505 / Full text",
  "506 / Full text",
  "507 / Full text",
  "This site is currently published through R0.76L Step 63. L treats only the explicit start-prepaid real integer one-dyadic-band shear family in",
  "View the previous major milestone recap (through I; does not cover J, K, or L)",
  "scale; the complete signed collar flux is eventually positive, and two-sided estimates hold relative to the full physical plateau. The frozen normalized quadratic logarithmic rate remains",
  "bulk-exterior saddle, candidate threshold,",
  "finite tilt sequence moves slightly away from the analytic limit on the displayed grid and has not yet entered its eventual asymptotic approach; the third panel is a unit-coordinate finite difference, not a numerical derivative. FINITE DIAGNOSTIC ONLY. NOT CLAY.",
  "All three dimensionless panels are finite binary64 diagnostics, not a PDE simulation or DNS. The",
  "complete-clock and full-plateau quotient in the stated window.",
  "Research note R0.76L · Step 63 · PARABOLIC EDGE COMPLETE CLOCK",
  "transition, arbitrary packets, Version-M, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later versions remain unauthorized, unread, and unpublished.",
  "Status · R0.76L STEP 63",
  "Certificate: Python 64/64, Ruby 279/279, L.1--L.72, and 78 displays; 25 observed-ledger mutations, 26 parsed-input mutations, 11 parameter-sensitivity checks, and 21 single-byte binding corruptions were all rejected. The complete frozen ledger is 24/24. The formal figure contains 12 files and 599,429 bytes, with the SVG, PDF, 600 dpi PNG, archived data, code, logs, manifest, and QA bound byte-for-byte. Finite certificates and the figure do not replace the continuum proof; this section contains no PDE simulation, DNS, or DGX.",
  "edge exponent is reduced by parabolic evolution to the complete-clock",
  "FIGURE R0.76L-1 / Frozen finite diagnostic",
  "K's fixed-slice lower bound and L's complete-clock absorption within the explicit family",
  "L / Frozen evidence",
  "L follows the same start-prepaid real integer one-dyadic-band Chebyshev shear through the complete clock. For",
  "Step 63 main text",
  "Step 63 main text, source boundary, two certificate implementations, formal figure, and fail-closed QA",
];

assert.equal(summaries.length, 72, "R0.76L Step 63 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.76L Step 63 translation count drift");
  assert.deepEqual(rows.map((row) => row.en), rows.map((row, i) => withProtected(summaries[i], row.zh)), "R0.76L English translation drift");
} else {
  assert.equal(missing.length, summaries.length, "R0.76L Step 63 source-string count drift");
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

process.stdout.write(`${JSON.stringify({ release: "R0.76L Step 63", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: summaries.length, applied: !checkOnly }, null, 2)}\n`);
