#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r076fstep57";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 260 research notes",
  "View the R0.76F card on the home page",
  "Current endpoint R0.76F Step 57 exponential spatial-observation lower bound",
  "Jump to the R0.76F card on the home page →",
  "Research note R0.76F Step 57 · 2026-09-04 · EXPONENTIAL SPATIAL-OBSERVATION LOWER BOUND",
  "Read the latest R0.76F research note →",
  "Expand 170 public notes",
  "Review v2.36 · 2026-09-04",
  "F uses binomial amplitudes and phase alignment to build q positive frequencies q,...,2q-1. The observation ratio on the fixed I/J geometry is at least 2^(q-1), ruling out uniform or polynomial q dependence in this spatial step. The construction is an exact smooth shear, but B=0, so it gives no complete collar-flux lower bound. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "An exact binomial dyadic packet shows that the inherited observation constant is at least 2^(q-1), matching E's exp(Cq) upper bound in exponential order. This fixes only the spatial row; B=0 in the example, so the complete transport flux vanishes. NO NOVELTY CLAIM. NOT CLAY.",
  "G is in the sole FIFO publication queue but remains unread and unpublished until F completes full online verification. F establishes only the exponential order of the inherited spatial observation row, and its example has B=0 and zero complete transport flux. A matching complete-flux lower bound, full space-time cancellation, the optimal exponential base, mode counts comparable with L^2, arbitrary packets, nonconstant shear, arbitrary-field E.24, complete Version-M extraction, regularity, and singularity remain open.",
  "The cumulative recap after R0.60 contains 191 nodes; the site now has 260 public research notes",
  "R0.70A–R0.76F · 162 sections published",
  "R0.70A–R0.76F: 162 sections published, 104 fully archived",
  "R0.76F Step 57 gives a 2^(q-1) lower bound within E's exact real dyadic-shear observation geometry, showing that exp(Theta(q)) cannot be reduced to polynomial order. The example has B=0 and zero complete transport flux, so complete signed flux and arbitrary packets remain open.",
  "R0.76F: exponential lower bound for the inherited spatial observation",
  "R0.76F | Exponential lower bound for the inherited spatial observation",
  ", and yields no complete collar-flux lower bound.",
  ". Therefore uniform or polynomial q dependence is impossible for the same spatial row; the realizing example has ",
  "constant is obtained by a direct construction in the main note; the bounded search establishes no completeness, novelty, or priority conclusion.",
  "of the phase-aligned real part, proving an observation ratio of at least this size in the exact real positive-frequency dyadic shear fibre and E's fixed I/J geometry: ",
  "gives the exact circle constant for fixed-geometry trigonometric Remez inequalities. F's real positive-frequency dyadic specialization and ",
  "Open interface · R0.76G",
  "explicitly records the sharpness of the general Turan--Nazarov order exponent; ",
  "is the original source of the measurable local estimate; ",
  "Literature review v2.36 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.76F work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "G is in the sole FIFO publication queue but remains unread and unpublished until F completes full online verification. F establishes only the exponential order of the inherited spatial observation row. A matching complete-flux lower bound, a full space-time cancellation route, the optimal exponential base, mode counts comparable with L^2, arbitrary packets, nonconstant shear, arbitrary-field E.24, complete Version-M extraction, regularity, and singularity remain open.",
  "PROVED: for q>=2 and 0<delta<=2pi/3, there are frequencies q,...,2q-1, nonnegative binomial amplitudes, and real phases for which the observation ratio on E's fixed I=[-1/2,1/2] and J=[-3/2,3/2] is at least 2^(q-1). Hence log C_q>=(q-1)log2 for the spatial row, and uniform or polynomial q dependence is impossible. EXACT-SHEAR REALIZATION: with delta=aR and B=0, the construction is the initial scaled fibre of a smooth unforced exact heat shear. ASYMPTOTIC BOUNDARY: if q(L)/L^2 stays bounded below along a subsequence, optimizing only this observation row cannot retain the exact -2/11907 coefficient; a small quadratic density may still leave a negative total exponent. SOURCE BOUNDARY: general Remez and Turan--Nazarov exponent sharpness is known; F makes no novelty, priority, or optimal-base claim. OPEN: a complete signed collar-flux lower bound, a full space-time cancellation route, the optimal exponential base, mode counts comparable with L^2, arbitrary packets, nonconstant shear, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity. The construction has B=0 and zero complete transport flux. Finite checks do not replace a continuum theorem; there is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.76F Step 57 bounded primary-source screen and claim boundary",
  "R0.76F Step 57 public boundary · EXPONENTIAL SPATIAL-OBSERVATION LOWER BOUND",
  "Step 57 uses ",
  "260 public research notes; latest node R0.76F.",
  "Exponential lower bound for the inherited spatial observation",
  "Research-note master index · v2.36 · 2026-09-04",
  "Latest node R0.76F · continuously revised",
  ", and gives an observation constant of at least ",
  ", the complete transport flux vanishes, so this is not an exponential lower bound for the complete collar flux.",
  ", the complete transport flux vanishes. Consequently there is no exponential lower bound for the complete signed collar flux here, and a different proof using full space-time cancellation is not excluded. The optimal exponential base, mode counts comparable with ",
  ", arbitrary packets, nonconstant shear, arbitrary-field E.24, complete Version-M extraction, regularity, and singularity remain open.",
  ". Therefore this observation step has ",
  "450 / Full text",
  "451 / Full text",
  "452 / Full text",
  "453 / Full text",
  "454 / Full text",
  "455 / Full text",
  "This site is currently published through R0.76F Step 57. F proves that the constant in the same spatial observation row grows at least as ",
  "order that cannot be replaced by a uniform constant or polynomial; however, the construction takes ",
  "Research note R0.76F · Step 57 · EXPONENTIAL SPATIAL-OBSERVATION LOWER BOUND",
  "growth; the realizing example takes ",
  "Status · R0.76F STEP 57",
  "Certificate: Python 83/83, Ruby 83/83, F.1--F.18, and 18/18 displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 83/83 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite checks do not replace the continuum norm inequality, imported Remez facts, or the Navier--Stokes embedding. This section contains no formal figure, simulation, DNS, or DGX.",
  "E's exponential upper bound and F's exponential-order lower bound",
  "F / Frozen evidence",
  "Inside E's nested intervals and exact real dyadic-shear fibre, F constructs ",
  "NEXT / Open boundary",
  "Step 57 main text",
  "Step 57 main text, primary-source boundary, two certificate implementations, and fail-closed QA"
];

assert.equal(summaries.length, 59, "R0.76F Step 57 translation table length drift");

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
    assert.equal(rows.length, summaries.length, "R0.76F Step 57 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.76F Step 57 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.76F Step 57 source-string count drift");
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
  release: "R0.76F Step 57",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
