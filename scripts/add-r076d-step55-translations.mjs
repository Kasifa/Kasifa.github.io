#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r076dstep55";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 258 research notes",
  "View the R0.76D card on the home page",
  "Current endpoint R0.76D Step 55 quantitative growing-mode entropy window",
  "For the exact real constant-shear family, D gives the explicit exp(C_* q log(q+1)) loss and the q(L) log(q(L)+1)=o(L^2) window; it retains the alpha+q spatial derivative and the (5/4)^m endpoint factor. Turan--Nazarov and Erdelyi are external inputs, while the finite certificate is not a continuum proof. Arbitrary growing packets, unconditional Version-M, regularity, and singularity remain open. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Jump to the R0.76D card on the home page →",
  "Research note R0.76D Step 55 · 2026-09-04 · QUANTITATIVE GROWING-MODE ENTROPY WINDOW",
  "Read the latest R0.76D research note →",
  "Expand 168 public notes",
  "Review v2.34 · 2026-09-04",
  "D's growing-mode window is limited to the exact real constant-shear family. Arbitrary growing packets, nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, regularity, and singularity remain open. When B!=0, the constant background has not been shown to belong to the frozen mean-zero, inversion-paired Version-M subclass. Later work was not authorized, read, or published.",
  "For the exact real constant-shear family, D gives an exp(C_* q log(q+1)) modal-entropy loss and retains the frozen rate -2/11907 when q(L) log(q(L)+1)=o(L^2). Turan--Nazarov and Erdelyi are external inputs; the remaining proof chain is derived locally. NO NOVELTY CLAIM. NOT CLAY.",
  "The cumulative recap after R0.60 contains 191 nodes; the site now has 258 public research notes",
  "R0.70A–R0.76D · 160 sections published",
  "R0.70A–R0.76D: 160 sections published, 104 fully archived",
  "R0.76D Step 55 quantifies the fixed-q constant by exp(C_* q log(q+1)) and gives the exact-shear growing-mode window q(L) log(q(L)+1)=o(L^2); the spatial derivative retains alpha+q and the endpoint comparison retains (5/4)^m. Arbitrary growing packets and Version-M extraction remain open.",
  "R0.76D: quantitative growing-mode entropy window for exact shears",
  "R0.76D | Quantitative growing-mode entropy window for exact shears",
  "provides the measurable-set Turan--Nazarov inequality;",
  "provides the point derivative inequality with explicit dependence on the maximum spatial frequency and term count. D derives the interval placement, counted factorial tail, (5/4)^m endpoint comparison, lambda split, complete-real energy payment, physical conversion, and growing-mode corollary locally. The bounded collision screen establishes no completeness, novelty, or priority conclusion.",
  "Literature review v2.34 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.76D work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "The growing-mode window is not an arbitrary-packet theorem. Nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, regularity, and singularity remain open. When B!=0, the constant background has not been shown to belong to the frozen mean-zero, inversion-paired Version-M subclass. Later material was not authorized, read, or published.",
  "PROVED: for the exact real constant-shear dyadic family, |T| <= exp(C_* q log(q+1)) a^(2/3) R^(-1/3) M^(2/3). The spatial derivative in D.15 explicitly retains alpha+q; the heat tail in D.24 retains (m+1)!/4; and the endpoint comparison in D.25 explicitly retains (5/4)^m. NARROW CONSEQUENCE: only q(L) log(q(L)+1)=o(L^2) preserves the frozen normalized rate -2/11907, and this is not uniform control of arbitrary growing packets. SOURCE BOUNDARY: Turan--Nazarov and Erdelyi are external inputs; spatial placement, the factorial tail, lambda branches, energy payment, and scale conversion are local deductions. CONDITIONAL: every Version-M consequence still requires the same velocity component and measurement row; when B!=0, the constant background has not been shown to belong to the frozen mean-zero, inversion-paired subclass. OPEN: matching lower bounds, sharp q dependence, removal of the modal-entropy loss, arbitrary growing packets, nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity. Finite checks do not replace a continuum theorem; there is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.76D Step 55 bounded primary-source screen and claim boundary",
  "R0.76D Step 55 public boundary · QUANTITATIVE GROWING-MODE ENTROPY WINDOW",
  "Step 55 uses Erdelyi's point derivative inequality and Turan--Nazarov observation to quantify C's fixed-q constant by exp(C_* q log(q+1)); the locally counted factorial tail, lambda split, complete-real energy payment, and scale conversion give the exact-shear window q(L) log(q(L)+1)=o(L^2).",
  "258 public research notes; latest node R0.76D.",
  "Quantitative growing-mode entropy window for exact shears",
  "Research-note master index · v2.34 · 2026-09-04",
  "Latest node R0.76D · continuously revised",
  "; therefore, whenever ",
  "; the endpoint comparison retains ",
  ". The spatial derivative retains ",
  "; Turan--Nazarov and Erdelyi are external inputs; the remaining placement, factorial tail, lambda branches, energy payment, and scale conversion are local deductions. The finite certificate does not replace the continuum proof.",
  "433 / Full text",
  "434 / Full text",
  "435 / Full text",
  "436 / Full text",
  "437 / Full text",
  "438 / Full text",
  "439 / Full text",
  "440 / Full text",
  "441 / Full text",
  "This site stops at R0.76D Step 55. For the exact real constant-shear family, D gives ",
  " window, not a uniform theorem for arbitrary growing packets. When ",
  " the constant background has not been shown to belong to the frozen mean-zero, inversion-paired Version-M subclass; arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  " the frozen rate is retained ",
  " loss and the ",
  "Research note R0.76D · Step 55 · QUANTITATIVE GROWING-MODE ENTROPY WINDOW",
  "Status · R0.76D STEP 55",
  "C's fixed-q full-frequency payment and D's quantitative modal-entropy window",
  "Certificate: Python 123/123, Ruby 123/123, D.1--D.41, and 41/41 tags and displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 123/123 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite checks do not replace the continuum Turan--Nazarov, Erdelyi, or analytic flux theorem. This section contains no formal figure, simulation, DNS, or DGX.",
  "D / Frozen evidence",
  "D quantifies C's fixed-q constant by ",
  "Step 55 main text",
  "Step 55 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
];

assert.equal(summaries.length, 56, "R0.76D Step 55 translation table length drift");

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
    assert.equal(rows.length, summaries.length, "R0.76D Step 55 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.76D Step 55 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.76D Step 55 source-string count drift");
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
  release: "R0.76D Step 55",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
