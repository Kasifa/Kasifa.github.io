#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075ystep50";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 253 research notes",
  "View the R0.75Y card on the home page",
  "Current endpoint R0.75Y Step 50 strongly separated multimode payment",
  "The previous major milestone recap still ends at W",
  "Jump to the R0.75Y card on the home page →",
  "Research note R0.75Y Step 50 · 2026-09-04 · STRONGLY SEPARATED MULTIMODE",
  "Read the latest R0.75Y research note →",
  "Expand 163 public notes",
  "Review v2.29 · 2026-09-04",
  "The cumulative recap after R0.60 contains 191 nodes; the site now has 253 public research notes",
  "R0.70A–R0.75Y · 155 sections published",
  "R0.70A–R0.75Y: 155 sections published, 104 fully archived",
  "R0.75Y Step 50 pays the strongly separated exact common-shear family satisfying aR delta_n >= 8q: all q^2 self, difference, and sum rows incur an explicit q^2 cost. The clustered region, arbitrary packets, and general Version-M extraction remain open.",
  "R0.75Y: complete signed-flux payment for strongly separated multimode families",
  "R0.75Y | Complete signed-flux payment for strongly separated multimode families",
  "Y proves complete signed collar-flux payment for the strongly separated exact common-shear family satisfying aR delta_n>=8q. Exact Gram coercivity and a phase-free clock pay all q^2 rows at an explicit q^2 cost. Unresolved clusters and arbitrary packets remain open. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Y uses signed-spectrum Gram coercivity, a phase-free complete-clock lemma, and an exact q^2 modal expansion to pay the strongly separated high-carrier family. The explicit cost is q^2; unresolved clusters and arbitrary packets remain open. NO NOVELTY CLAIM. NOT CLAY.",
  "Y closes only the strongly separated subclass satisfying aR delta_n >= 8q. Clustered high-carrier modes, weaker separation, arbitrary packets, inter-packet aggregation, nonconstant or vertical shear, projection, E.24, and Version-M extraction remain open. Later work was not authorized, read, or published.",
  "Literature review v2.29 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75Y work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "The Jaming--Saba 2023 survey and the Kunis--Möller--Peter--von der Ohe 2017 separated-frequency reconstruction record provide only classical Ingham-type context. Y imports no external theorem and instead derives L2 coercivity under separation by a finite signed-spectrum Gram calculation. The bounded search establishes no completeness, novelty, or priority conclusion.",
  "PROVED: Y.1--Y.3 signed-spectrum gap and strong separation; Y.15--Y.19 phase-uniform Gram coercivity; Y.20--Y.25 phase-free complete-clock lemma; Y.26--Y.34 exact radial/modal expansion and q^2 row payment; Y.35--Y.37 plateau mass and physical payment; Y.7--Y.9 normalized estimate, cancellation of R powers, explicit q^2 cost, and the -2/11907 rate; and Y.38 exact smooth unforced shear. CONDITIONAL: the growing-q rate also requires log q=o(L^2) while strong separation continues to hold; any Version-M consequence still requires the measurement row, weight, realized subclass, actual component, and ledger alignment. OPEN: unresolved clusters with aR delta_n<8q; removal or weakening of strong separation; arbitrary packets; inter-packet aggregation; nonconstant or vertically dependent shear; projection; arbitrary-field E.24; complete Version-M extraction; fixed deletion; suitable-weak transfer; regularity; and singularity. Finite checks do not replace continuum lemmas; there is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75Y Step 50 bounded primary-source screen and claim boundary",
  "R0.75Y Step 50 public boundary · STRONGLY SEPARATED · EXPLICIT q^2 COST",
  "Step 50 uses signed-spectrum Gram coercivity, a phase-free complete-clock lemma, the exact q^2 modal row count, and plateau mass to pay the strongly separated exact common-shear family satisfying aR delta_n>=8q. The explicit mode-count cost is q^2; the clustered region remains open.",
  "Unresolved high-carrier clusters, weaker separation, arbitrary packets, inter-packet aggregation, nonconstant or vertical shear, projection, E.24, and Version-M extraction all remain open. Later material was not authorized, read, or published.",
  "253 public research notes; latest node R0.75Y.",
  "Complete signed-flux payment for strongly separated multimode families",
  "Research-note master index · v2.29 · 2026-09-04",
  "Latest node R0.75Y · continuously revised",
  ", then all self, difference, and sum rows, totaling",
  "393 / Full text",
  "394 / Full text",
  "395 / Full text",
  "396 / Full text",
  "397 / Full text",
  "398 / Full text",
  "399 / Full text",
  "400 / Full text",
  "This site stops at R0.75Y Step 50. Y pays only the strongly separated exact common-shear family satisfying aR delta_n >= 8q. Unresolved high-carrier clusters, weaker separation, arbitrary packets, inter-packet aggregation, nonconstant or vertical shear, projection, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "terms are all paid by the plateau cubic mass. The explicit cost is q^2, and the clustered region remains open; the exact logarithmic rate is",
  "Research note R0.75Y · Step 50 · STRONGLY SEPARATED MULTIMODE",
  "Status · R0.75Y STEP 50",
  "Certificate: Python 17/17, Ruby 18/18, Y.1--Y.39, and 39/39 tags and displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 85/85 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite checks do not replace the continuum Gram or complete-clock lemmas. This section contains no formal figure, simulation, DNS, or DGX.",
  "Step 50 main text",
  "Step 50 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
  "The exact roles of X and Y",
  "Y / Frozen evidence",
  "Y closes a quantitatively separated subclass of the high-carrier sector for three or more modes: for an exact real diffusive shear in the same dyadic band, if the signed-spectrum gap satisfies",
];

assert.equal(summaries.length, 49, "R0.75Y Step 50 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75Y Step 50 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75Y Step 50 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75Y Step 50 source-string count drift");
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
  release: "R0.75Y Step 50",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
