#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r076astep52";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 255 research notes",
  "View the R0.76A card on the home page",
  "Current endpoint R0.76A Step 52 localized current sign obstruction",
  "Jump to the R0.76A card on the home page →",
  "Research note R0.76A Step 52 · 2026-09-04 · COMPLETE-CLOCK LOCALIZED CURRENT SIGN OBSTRUCTION",
  "Read the latest R0.76A research note →",
  "Expand 165 public notes",
  "Review v2.31 · 2026-09-04",
  "A materializes strict negativity of the current/correction row for an exact q=2 unresolved high-carrier cluster with the actual primitive and complete clock, closing only sign-dropping. W's two-mode payment remains valid; perturbative, nonlocal signed, joint density/carrier cancellation, and general cluster payment remain open. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "A uses the actual collar primitive, complete clock, and an exact q=2 unresolved cluster to prove strict negativity of the localized carrier-current/correction row, ruling out only sign-dropping. W's two-mode flux estimate is unaffected; perturbative, nonlocal signed, joint density/carrier, and general cluster-payment routes remain open. NO NOVELTY CLAIM. NOT CLAY.",
  "A rules out only sign-dropping for the localized current/correction row; W's exact q=2 flux estimate remains valid. Perturbative and boundary-error estimates, nonlocal signed control, joint density/carrier cancellation, general cluster payment, cross-cluster aggregation, arbitrary packets, and Version-M extraction remain open. Later work was not authorized, read, or published.",
  "The cumulative recap after R0.60 contains 191 nodes; the site now has 255 public research notes",
  "R0.70A–R0.76A · 157 sections published",
  "R0.70A–R0.76A: 157 sections published, 104 fully archived",
  "R0.76A Step 52 proves strict negativity of the localized current/correction row for an exact q=2 unresolved cluster with the actual frozen primitive and complete clock. It rules out only sign-dropping based on one-sided offset spectrum. W's two-mode flux payment remains valid; general cluster payment and joint cancellation remain open.",
  "R0.76A: complete-clock localized carrier-current sign obstruction",
  "R0.76A | Complete-clock localized carrier-current sign obstruction",
  "Literature review v2.31 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.76A work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Nazarov, Kovrijkine, Egidi--Veselic, and Jaming--Saba provide only classical context for finite exponential sums and spectral observation; they do not give localized-current positivity for positive-frequency polynomials. A's strict sign obstruction comes from the actual primitive and exact two-term formula. The bounded negative search establishes no completeness, novelty, or priority conclusion.",
  "Perturbative estimates, localized boundary errors, nonlocal signed control, joint density/carrier cancellation, full Z-sector payment, cross-cluster aggregation, arbitrary packets, and Version-M extraction remain open. Later material was not authorized, read, or published.",
  "PROVED: A.1--A.18 establish nonnegativity, support, and positive mass of the actual frozen primitive; A.19--A.22 give complete-clock damping and phase bounds; A.23--A.31 give strict negativity of the localized current and correction row for an exact q=2 unresolved cluster; A.32 retains the positive carrier-density row; and A.33--A.34 give the current scaling and fixed-amplitude upper scale C R/a. NARROW CONSEQUENCE: this closes only the proof step that discards the localized carrier-current/correction row or calls it nonnegative because the offset spectrum is one-sided. It is not a counterexample to R0.75W's two-mode collar-flux estimate, general cluster payment, a perturbative estimate, a nonlocal signed estimate, or joint density/carrier cancellation. CONDITIONAL: any Version-M consequence still requires the same measurement row, weight, realized subclass, actual component, and ledger alignment. OPEN: a general cluster-current estimate; joint density/carrier-block payment; full Z-sector payment; cross-cluster aggregation; arbitrary packets; E.24; complete Version-M extraction; fixed deletion; suitable-weak transfer; regularity; and singularity. Finite checks do not replace continuum identities; there is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.76A Step 52 bounded primary-source screen and claim boundary",
  "R0.76A Step 52 public boundary · COMPLETE-CLOCK STRICT NEGATIVITY · SIGN-DROPPING ONLY",
  "Step 52 uses the actual frozen primitive, complete clock, and an exact q=2 unresolved high-carrier cluster to prove strict negativity of the localized current/correction row. It rules out only sign-dropping based on one-sided offset spectrum. W's two-mode flux estimate remains valid; perturbative, nonlocal signed, joint density/carrier cancellation, and general cluster payment remain open.",
  "255 public research notes; latest node R0.76A.",
  "Complete-clock localized carrier-current sign obstruction",
  "Research-note master index · v2.31 · 2026-09-04",
  "Latest node R0.76A · continuously revised",
  "409 / Full text",
  "410 / Full text",
  "411 / Full text",
  "412 / Full text",
  "413 / Full text",
  "414 / Full text",
  "415 / Full text",
  "This site stops at R0.76A Step 52. A proves strict negativity of the localized current/correction row with the actual primitive and complete clock, ruling out only the step that discards the row or calls it nonnegative because the offset spectrum is one-sided. W's exact q=2 flux payment remains valid; perturbative estimates, localized boundary errors, nonlocal signed estimates, joint density/carrier cancellation, general cluster payment, cross-cluster aggregation, E.24, complete Version-M extraction, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "Research note R0.76A · Step 52 · COMPLETE-CLOCK LOCALIZED CURRENT SIGN OBSTRUCTION",
  "Status · R0.76A STEP 52",
  "A / Frozen evidence",
  "A constructs an exact q=2 unresolved high-carrier cluster with the actual frozen collar primitive and complete clock, proving strict negativity of the localized carrier-current and correction row. It rules out only the proof step that discards the row or calls it nonnegative because the offset spectrum is one-sided; it neither contradicts W's two-mode flux estimate nor rules out perturbative, nonlocal signed, or joint density/carrier cancellation.",
  "Certificate: Python 15/15, Ruby 15/15, A.1--A.34, and 34/34 tags and displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 86/86 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite checks do not replace continuum identities. This section contains no formal figure, simulation, DNS, or DGX.",
  "Step 52 main text",
  "Step 52 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
  "Z's localized carrier question and A's strict sign obstruction",
];

assert.equal(summaries.length, 45, "R0.76A Step 52 translation table length drift");

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
    assert.equal(rows.length, summaries.length, "R0.76A Step 52 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.76A Step 52 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.76A Step 52 source-string count drift");
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
  release: "R0.76A Step 52",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
