#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r076estep56";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 259 research notes",
  "View the R0.76E card on the home page",
  "Current endpoint R0.76E Step 56 linear modal-entropy window",
  "For the exact real constant-shear family, E uses a delayed stable heat clock to improve the loss to exp(C_* q) and enlarge the window to q(L)=o(L^2). Early Holder uses the full K_T, the centered estimate is invoked only on the monotone tail, and the last-unit endpoint removes the factorial. The finite certificate is not a continuum proof. Arbitrary growing packets, unconditional Version-M, regularity, and singularity remain open. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Jump to the R0.76E card on the home page →",
  "Research note R0.76E Step 56 · 2026-09-04 · LINEAR MODAL-ENTROPY WINDOW",
  "Read the latest R0.76E research note →",
  "Expand 169 public notes",
  "Review v2.35 · 2026-09-04",
  "E's linear modal-entropy window covers only the exact real constant-shear family. Arbitrary growing packets, nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, regularity, and singularity remain open. When B!=0, the constant background has not been shown to belong to the frozen mean-zero, inversion-paired Version-M subclass. Later queued work has not yet been published.",
  "For the exact real constant-shear family, E gives an exp(C_* q) modal-entropy loss and retains the frozen rate -2/11907 when q(L)=o(L^2). The delayed split, early Holder payment, last-unit endpoint, and complete-real energy payment are local deductions; Turan--Nazarov and Erdelyi are external inputs. NO NOVELTY CLAIM. NOT CLAY.",
  "The cumulative recap after R0.60 contains 191 nodes; the site now has 259 public research notes",
  "R0.70A–R0.76E · 161 sections published",
  "R0.70A–R0.76E: 161 sections published, 104 fully archived",
  "R0.76E Step 56 uses a delayed stable heat clock to improve the exact-shear loss from exp(C_* q log(q+1)) to exp(C_* q), enlarging the window to q(L)=o(L^2) while retaining the frozen rate -2/11907. Arbitrary growing packets and Version-M extraction remain open.",
  "R0.76E: linear modal-entropy window for exact shears",
  "R0.76E | Linear modal-entropy window for exact shears",
  ", thereby giving ",
  " exact-shear window.",
  "Open interface · R0.76F not yet published",
  "provides the point derivative inequality with explicit dependence on the maximum spatial frequency and term count. E derives the delayed split, early Holder payment, monotone tail, last-unit endpoint, carrier accounting, complete-real energy payment, physical conversion, and growing-window corollary locally. The bounded search establishes no completeness, novelty, priority, or sharpness conclusion.",
  "Literature review v2.35 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.76E work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "The linear modal-entropy window is not an arbitrary-packet theorem. Nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, regularity, and singularity remain open. When B!=0, the constant background has not been shown to belong to the frozen mean-zero, inversion-paired Version-M subclass. Later queued work has not yet been published.",
  "delays the stable-tail split; early Holder, the monotone tail, and the last-unit endpoint improve the loss to ",
  "PROVED: for the exact real constant-shear dyadic family, |T| <= exp(C_* q) a^(2/3) R^(-1/3) M^(2/3). E.15 selects a uniform delayed split, E.16 pays the early interval with the full K_T, E.17 uses the centered estimate only after the tail becomes monotone, and E.22 gives the last-unit endpoint exp(CN) T^(-2/3) K_T^(2/3). NARROW CONSEQUENCE: q(L)=o(L^2) preserves the frozen normalized rate -2/11907. This strictly enlarges D's q(L) log(q(L)+1)=o(L^2) window but is still not uniform control of arbitrary growing packets. SOURCE BOUNDARY: Turan--Nazarov and Erdelyi are external inputs; the delayed split, early Holder payment, monotone tail, last-unit endpoint, carrier accounting, complete-real energy payment, and scale conversion are local deductions. CONDITIONAL: every Version-M consequence still requires the same velocity component and measurement row; when B!=0, the constant background has not been shown to belong to the frozen mean-zero, inversion-paired subclass. OPEN: matching lower bounds, sharp q dependence, removal of the linear modal-entropy loss, arbitrary growing packets, nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity. Finite checks do not replace a continuum theorem; there is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.76E Step 56 bounded primary-source screen and claim boundary",
  "R0.76E Step 56 public boundary · LINEAR MODAL-ENTROPY WINDOW",
  "Step 56 retains D's spatial observation and uses ",
  "259 public research notes; latest node R0.76E.",
  "Linear modal-entropy window for exact shears",
  "Research-note master index · v2.35 · 2026-09-04",
  "Latest node R0.76E · continuously revised",
  ", and extends the growing window to ",
  ", while retaining the frozen rate ",
  ". The last-unit endpoint and complete-real energy ledger keep all carrier powers exactly cancelled. The finite certificate does not replace the continuum proof.",
  "442 / Full text",
  "443 / Full text",
  "444 / Full text",
  "445 / Full text",
  "446 / Full text",
  "447 / Full text",
  "448 / Full text",
  "449 / Full text",
  "This site is currently published through R0.76E Step 56. For the exact real constant-shear family, E gives ",
  ", the constant background has not been shown to belong to the frozen mean-zero, inversion-paired Version-M subclass; arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later queued work has not yet been published.",
  " loss to ",
  "Research note R0.76E · Step 56 · LINEAR MODAL-ENTROPY WINDOW",
  "Status · R0.76E STEP 56",
  "Certificate: Python 135/135, Ruby 135/135, E.1--E.34, and 38/38 displays including four intentionally unnumbered displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 135/135 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite checks do not replace the continuum Turan--Nazarov, Erdelyi, or analytic flux theorem. This section contains no formal figure, simulation, DNS, or DGX.",
  "D's quantitative modal-entropy loss and E's linear modal-entropy window",
  "E / Frozen evidence",
  "E delays the stable heat-tail split, pays the early interval with the full observed mass, and invokes Turan--Nazarov only after the tail becomes monotone; this improves D's ",
  "NEXT / Later work not yet published",
  "Step 56 main text",
  "Step 56 main text, primary-source boundary, two certificate implementations, and fail-closed QA"
];

assert.equal(summaries.length, 56, "R0.76E Step 56 translation table length drift");

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
    assert.equal(rows.length, summaries.length, "R0.76E Step 56 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.76E Step 56 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.76E Step 56 source-string count drift");
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
  release: "R0.76E Step 56",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
