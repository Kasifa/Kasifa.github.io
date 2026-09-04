#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075zstep51";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 254 research notes",
  "View the R0.75Z card on the home page",
  "Current endpoint R0.75Z Step 51 cluster carrier-current gate",
  "Jump to the R0.75Z card on the home page →",
  "Research note R0.75Z Step 51 · 2026-09-04 · CLUSTER CARRIER-CURRENT GATE",
  "Read the latest R0.75Z research note →",
  "Expand 164 public notes",
  "Review v2.30 · 2026-09-04",
  "The cumulative recap after R0.60 contains 191 nodes; the site now has 254 public research notes",
  "R0.70A–R0.75Z · 156 sections published",
  "R0.70A–R0.75Z: 156 sections published, 104 fully archived",
  "R0.75Z Step 51 gives the exhaustive fixed-q X/Y/Z partition and the unresolved-cluster envelope/current normal form. It rejects only the naive strategy of carrier-uniform pointwise absorption followed by recursive application of X. Full cluster payment, cluster additivity, and cross-cluster payment remain open.",
  "R0.75Z: unresolved-cluster normal form and carrier-current gate",
  "R0.75Z | Unresolved-cluster normal form and carrier-current gate",
  "Z gives the exhaustive X/Y/Z partition, cluster envelope PDE, density/carrier blocks, and current identities, and rules out only pointwise absolute-current absorption followed by recursive application of X. Full cluster payment, cluster additivity, cross-cluster payment, and any counterexample claim remain unestablished. NO NOVELTY CLAIM. NOT CLAY.",
  "Z materializes the exhaustive fixed-q X/Y/Z partition, maximal-cluster normal form, exact envelope PDE, density/carrier split, and current identities. It only rejects pointwise absorption of 2N|J| followed by recursive application of X; it proves no full cluster payment, additivity, cross-cluster payment, or counterexample. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Z closes only the parameter partition, cluster normal form, and naive pointwise-current recursion. Full cluster payment, cluster additivity, full-field plateau-mass control of an individual cluster, cross-cluster payment, arbitrary packets, and Version-M extraction remain open; no counterexample is claimed. Later work was not authorized, read, or published.",
  "Literature review v2.30 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75Z work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Localized signed current, joint density/carrier cancellation, full-field mass control, cluster additivity, cross-cluster payment, arbitrary packets, and Version-M extraction all remain open; no counterexample is claimed. Later material was not authorized, read, or published.",
  "Nazarov, Kovrijkine, Egidi--Veselic, Friedland--Yomdin, and Jaming--Saba provide only classical context for finite-cluster observation. Z's parameter partition, modulation, density/carrier split, current identity, and pointwise no-go follow directly from the displayed finite Fourier algebra. These sources do not provide the required signed time-weighted collar-flux payment, and the bounded search establishes no completeness, novelty, or priority conclusion.",
  "PROVED: Z.1--Z.3 exhaustive fixed-q X/Y/Z partition; Z.4 and Z.11--Z.13 unique maximal clusters and strict width; Z.5--Z.7 exact envelope/current equations; Z.18--Z.21 one-cluster density/carrier square split; Z.22--Z.27 local identity and full-period favorable current; and Z.28--Z.31 exclusion of carrier-uniform pointwise absorption of 2N|J| into |Z|^2+|Z_y|^2. NARROW CONSEQUENCE: this closes only the naive strategy that takes the new current in absolute value and then recursively applies X; it is not a counterexample to a signed, nonlocal, joint-block, or final cluster-flux estimate. CONDITIONAL: any Version-M consequence still requires the same measurement row, weight, realized subclass, actual component, and ledger alignment. OPEN: full clustered-sector payment; cluster additivity; full-field plateau-mass control of each cluster; cross-cluster products/payment; localized signed current; joint density/carrier cancellation; arbitrary packets; E.24; complete Version-M extraction; fixed deletion; suitable-weak transfer; regularity; and singularity. Finite checks do not replace continuum identities; there is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75Z Step 51 bounded primary-source screen and claim boundary",
  "R0.75Z Step 51 public boundary · EXACT PARTITION · NARROW METHOD NO-GO",
  "Step 51 gives the exhaustive fixed-q X/Y/Z partition, unique maximal clusters, exact complex envelope PDE, density/carrier split, and local/global current identities. It rules out only carrier-uniform pointwise absolute-current absorption followed by recursive application of X. Full cluster payment and cross-cluster aggregation remain open.",
  "254 public research notes; latest node R0.75Z.",
  "Unresolved-cluster normal form and carrier-current gate",
  "Research-note master index · v2.30 · 2026-09-04",
  "Latest node R0.75Z · continuously revised",
  "401 / Full text",
  "402 / Full text",
  "403 / Full text",
  "404 / Full text",
  "405 / Full text",
  "406 / Full text",
  "407 / Full text",
  "408 / Full text",
  "This site stops at R0.75Z Step 51. Z closes only the X/Y/Z parameter partition, cluster normal form, density/carrier split, current identities, and the naive strategy of carrier-uniform pointwise absorption followed by recursive application of X. Full cluster payment, cluster additivity, full-field mass control of an individual cluster, cross-cluster payment, arbitrary packets, E.24, complete Version-M extraction, regularity, and singularity remain open; no counterexample is claimed. Later work was not authorized, read, or published.",
  "pointwise into",
  "and then recursively applies X; it proves no full cluster payment, cluster additivity, cross-cluster payment, or counterexample.",
  "Research note R0.75Z · Step 51 · CLUSTER CARRIER-CURRENT GATE",
  "Status · R0.75Z STEP 51",
  "Certificate: Python 15/15, Ruby 15/15, Z.1--Z.31, and 31/31 tags and displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 72/72 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite checks do not replace continuum identities. This section contains no formal figure, simulation, DNS, or DGX.",
  "Step 51 main text",
  "Step 51 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
  "The exhaustive roles of X, Y, and Z",
  "Z / Frozen evidence",
  "Z gives the exhaustive fixed-q X/Y/Z partition, unique maximal-cluster decomposition, exact complex envelope PDE, density/carrier blocks, and local/global current identities. It only rejects",
];

assert.equal(summaries.length, 48, "R0.75Z Step 51 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75Z Step 51 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75Z Step 51 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75Z Step 51 source-string count drift");
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
  release: "R0.75Z Step 51",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
