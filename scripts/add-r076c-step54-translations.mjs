#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r076cstep54";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 257 research notes",
  "View the R0.76C card on the home page",
  "Current endpoint R0.76C Step 54 fixed-q full-frequency flux payment",
  "For fixed integer q, positive integer frequencies, and real phases, C pays the ultra-high heat-clock branch n_1 R > 1; together with B for n_1 R <= 1, this covers all carriers. C.14 is explicitly limited to pointwise exponential-polynomial families, and the complete real square retains all self and cross terms. Uniform growing packets, arbitrary fields, and unconditional Version-M claims remain open. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Jump to the R0.76C card on the home page →",
  "Research note R0.76C Step 54 · 2026-09-04 · FIXED-Q FULL-FREQUENCY FLUX PAYMENT",
  "Read the latest R0.76C research note →",
  "Expand 167 public notes",
  "Review v2.33 · 2026-09-04",
  "B and C together cover every carrier only for each fixed finite q exact real dyadic-band shear. Uniform growing packets, nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "For fixed integer q, positive integer frequencies, and real phases, C pays n_1 R > 1 for exact real dyadic-band shears; together with B for n_1 R <= 1, this covers all carriers. The weighted and terminal lambda powers are -1/3 and 0, and the complete real square regroups all self and cross terms before absolute values. NO NOVELTY CLAIM. NOT CLAY.",
  "The cumulative recap after R0.60 contains 191 nodes; the site now has 257 public research notes",
  "R0.70A–R0.76C · 159 sections published",
  "R0.70A–R0.76C: 159 sections published, 104 fully archived",
  "R0.76C Step 54 pays the n_1 R > 1 ultra-high heat-clock branch for each fixed integer q exact real dyadic-band shear; combined with B for n_1 R <= 1, it covers all carriers. C.14 applies only to pointwise exponential-polynomial families satisfying C.12, and the complete real square retains every self and cross term before absolute values.",
  "R0.76C: full-frequency flux payment for fixed finite dyadic-band shears",
  "R0.76C | Full-frequency flux payment for fixed finite dyadic-band shears",
  "Literature review v2.33 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.76C work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "The cited primary sources support the measurable-set Turan--Nazarov inequality for finite exponential polynomials without dependence on imaginary frequencies or exponent gaps. C derives the polynomial-exponential decay, weighted tail, terminal estimate, cutoff-onset gain, complete-real-square identity, and physical scaling locally. The bounded collision screen establishes no completeness, novelty, or priority conclusion.",
  "PROVED: for each fixed integer q, positive integer modes, real phases, an exact real dyadic band, and all sufficiently large frozen L, the signed-flux estimate holds for every carrier. B covers n_1 R <= 1 and C covers n_1 R > 1. C.12--C.21 establish the stable heat-clock tail only for pointwise exponential-polynomial families satisfying C.12; C.22--C.27 retain weighted lambda^(-1/3) and terminal lambda^0; C.28--C.34 pay the complete real square and physical scaling. NARROW CONSEQUENCE: all carriers are covered only in this fixed-q exact-shear class, without exponent-gap, imaginary-frequency, localized-current-positivity, or standalone carrier-integration-by-parts assumptions. CONDITIONAL: every Version-M consequence still requires the same velocity component and measurement row; the nonzero constant background has not entered the frozen mean-zero Version-M subclass. OPEN: uniform growing q, arbitrary growing packets, nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity. Finite checks do not replace the continuum Turan--Nazarov theorem; there is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "Uniform growing packets, nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, regularity, and singularity remain open. Later material was not authorized, read, or published.",
  "R0.76C Step 54 bounded primary-source screen and claim boundary",
  "R0.76C Step 54 public boundary · FIXED-Q FULL-FREQUENCY EXACT-SHEAR PAYMENT",
  "Step 54 pays n_1 R > 1 for each fixed integer q exact real dyadic-band shear using the pointwise exponential-polynomial clock, cutoff onset, and complete real square with the correct lambda powers. Together with B for n_1 R <= 1, all carriers are covered; the constant is not uniform for growing q.",
  "257 public research notes; latest node R0.76C.",
  "Full-frequency flux payment for fixed finite dyadic-band shears",
  "Research-note master index · v2.33 · 2026-09-04",
  "Latest node R0.76C · continuously revised",
  "425 / Full text",
  "426 / Full text",
  "427 / Full text",
  "428 / Full text",
  "429 / Full text",
  "430 / Full text",
  "431 / Full text",
  "432 / Full text",
  "This site stops at R0.76C Step 54. B and C together cover every carrier only for each fixed finite q exact real dyadic-band shear; the constant is not uniform for growing q. Arbitrary growing packets, nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "Research note R0.76C · Step 54 · FIXED-Q FULL-FREQUENCY FLUX PAYMENT",
  "Status · R0.76C STEP 54",
  "B's inverse-radius branch and C's ultra-high heat-clock payment",
  "C / Frozen evidence",
  "For fixed integer q, positive integer frequencies, and real phases, C pays the ultra-high heat-clock branch n_1 R > 1 for exact real dyadic-band shears; together with B for n_1 R <= 1, this covers all carriers. The weighted tail retains lambda^(-1/3), the terminal row retains lambda^0, and the complete real square regroups every self and cross term before absolute values. C.14 quantifies only pointwise exponential-polynomial families satisfying C.12.",
  "Certificate: Python 140/140, Ruby 140/140, C.1--C.35, and 35/35 tags and displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 140/140 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite checks do not replace the continuum Turan--Nazarov theorem. This section contains no formal figure, simulation, DNS, or DGX.",
  "Step 54 main text",
  "Step 54 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
];

assert.equal(summaries.length, 46, "R0.76C Step 54 translation table length drift");

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
    assert.equal(rows.length, summaries.length, "R0.76C Step 54 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.76C Step 54 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.76C Step 54 source-string count drift");
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
  release: "R0.76C Step 54",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
