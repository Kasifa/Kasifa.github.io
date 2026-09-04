#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r076bstep53";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 256 research notes",
  "View the R0.76B card on the home page",
  "Current endpoint R0.76B Step 53 fixed-q inverse-radius flux payment",
  "For fixed integer q, positive integer frequencies, and real phases, the X branch alpha < 8q and B branch 8q <= alpha <= a exhaust n_1 R <= 1. B pays all self and cross terms through the complete real square without using the localized-current sign ruled out by A. Uniform growing-q, ultra-high-carrier, arbitrary-field, and unconditional Version-M claims remain open. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Jump to the R0.76B card on the home page →",
  "Research note R0.76B Step 53 · 2026-09-04 · FIXED-Q INVERSE-RADIUS FLUX PAYMENT",
  "Read the latest R0.76B research note →",
  "Expand 166 public notes",
  "Review v2.32 · 2026-09-04",
  "B closes n_1 R <= 1 for exact real dyadic-band shears with fixed integer q, positive integer frequencies, and real phases: X pays alpha < 8q and B pays 8q <= alpha <= a. The complete real square regroups all self and cross terms before absolute values and uses no localized-current sign. NO NOVELTY CLAIM. NOT CLAY.",
  "B closes only fixed-q exact real dyadic-band shears in the range n_1 R <= 1. Uniform growing packets, n_1 R > 1, nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "The cumulative recap after R0.60 contains 191 nodes; the site now has 256 public research notes",
  "R0.70A–R0.76B · 158 sections published",
  "R0.70A–R0.76B: 158 sections published, 104 fully archived",
  "R0.76B Step 53 closes the inverse-radius signed flux for fixed-q exact real dyadic-band shears with n_1 R <= 1 and all sufficiently large frozen L. The X and B alpha branches exhaust the range, while the complete real square retains all self and cross terms before absolute values and bypasses A's localized-current sign obstruction.",
  "R0.76B: inverse-radius flux payment for fixed finite dyadic-band shears",
  "R0.76B | Inverse-radius flux payment for fixed finite dyadic-band shears",
  "Literature review v2.32 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.76B work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "The cited primary sources support measurable-set Turan--Nazarov observation for finite exponential polynomials without imaginary-frequency or gap loss. Erdelyi, Brudnyi, and Jaming--Saba provide only adjacent derivative-inequality context. B proves the companion-ODE derivative row, complete-real-square energy identity, and physical scaling locally. The bounded collision screen establishes no completeness, novelty, or priority conclusion.",
  "PROVED: fixed integer q; positive integer modes; real phases; exact real dyadic band; and, for all sufficiently large frozen L, the inverse-radius estimate under n_1 R <= 1. X pays alpha < 8q and B pays 8q <= alpha <= a without overlap or gap. B.15--B.25 use two Turan--Nazarov applications and a compact companion ODE; B.29--B.35 pay the complete real square before absolute values; B.36--B.37 finish the scale conversion. NARROW CONSEQUENCE: within this fixed-q exact-shear range, B bypasses A's localized-current sign obstruction and needs neither spectral separation nor localized-current positivity. CONDITIONAL: every Version-M consequence still requires the same velocity component and measurement row; the nonzero constant background has not entered the frozen mean-zero Version-M subclass. OPEN: uniform growing q, n_1 R > 1, arbitrary growing packets, nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity. Finite checks do not replace continuum Turan--Nazarov or compact-ODE arguments; there is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "Uniform growing packets, n_1 R > 1, nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, regularity, and singularity remain open. Later material was not authorized, read, or published.",
  "R0.76B Step 53 bounded primary-source screen and claim boundary",
  "R0.76B Step 53 public boundary · FIXED-Q INVERSE-RADIUS EXACT-SHEAR PAYMENT",
  "Step 53 closes n_1 R <= 1 for fixed-q exact real dyadic-band shears: X pays alpha < 8q and B pays 8q <= alpha <= a. B regroups all self and cross terms through the complete real square before absolute values, bypassing A's localized-current sign obstruction; the constant is not uniform for growing q.",
  "256 public research notes; latest node R0.76B.",
  "Inverse-radius flux payment for fixed finite dyadic-band shears",
  "Research-note master index · v2.32 · 2026-09-04",
  "Latest node R0.76B · continuously revised",
  "416 / Full text",
  "417 / Full text",
  "418 / Full text",
  "419 / Full text",
  "420 / Full text",
  "421 / Full text",
  "422 / Full text",
  "423 / Full text",
  "424 / Full text",
  "This site stops at R0.76B Step 53. B closes only the inverse-radius signed-flux estimate for fixed-q exact real dyadic-band shears with n_1 R <= 1; the constant is not uniform for growing q. The ultra-high sector n_1 R > 1, arbitrary growing packets, nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "Research note R0.76B · Step 53 · FIXED-Q INVERSE-RADIUS FLUX PAYMENT",
  "Status · R0.76B STEP 53",
  "A's localized-sign obstruction and B's complete-real-square payment",
  "B / Frozen evidence",
  "For fixed integer q, positive integer frequencies, and real phases, B proves the inverse-radius signed collar-flux estimate for exact real dyadic-band shears under n_1 R <= 1 and all sufficiently large frozen L. X pays alpha < 8q and B pays 8q <= alpha <= a; B regroups all self and cross terms through the complete real square before taking absolute values, thereby bypassing A's localized-current sign obstruction.",
  "Certificate: Python 15/15, Ruby 15/15, B.1--B.41, and 41/41 tags and displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 123/123 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite checks do not replace continuum Turan--Nazarov or compact companion-ODE arguments. This section contains no formal figure, simulation, DNS, or DGX.",
  "Step 53 main text",
  "Step 53 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
];

assert.equal(summaries.length, 47, "R0.76B Step 53 translation table length drift");

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
    assert.equal(rows.length, summaries.length, "R0.76B Step 53 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.76B Step 53 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.76B Step 53 source-string count drift");
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
  release: "R0.76B Step 53",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
