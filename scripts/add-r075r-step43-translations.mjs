#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075rstep43";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 246 research notes",
  "View the R0.75R card on the home page",
  "Current endpoint R0.75R Step 43 outer-cap spectral concentration obstruction",
  "Full cutoff support, Version-M exterior-row aggregation, quantitative spreading or thickness, signed multimode cancellation, nonconstant shear, and nonlinear mode transfer still require analysis. Later work was not authorized, read, or published.",
  "Jump to the R0.75R card on the home page →",
  "An explicit real high-band packet concentrates in the positive outer cap and remains there for one diffusive time under an exact smooth constant-shear Navier--Stokes evolution, while the plateau shell sees only the Dirichlet tail. The flux-to-plateau-mass quotient therefore diverges at an exact positive exponential rate, ruling out the plateau-only multimode extension but not full-support payment, Version-M, or E.24. NO NOVELTY CLAIM. NOT CLAY.",
  "Research note R0.75R Step 43 · 2026-09-04 · OUTER-CAP SPECTRAL CONCENTRATION OBSTRUCTION",
  "An explicit real high-band packet concentrates in the positive outer cap and evolves as an exact global smooth Navier--Stokes shear solution. It leaves only a Dirichlet tail on the plateau, so the normalized flux-to-plateau-mass quotient diverges at a positive exponential rate. This rules out only plateau-only multimode payment, not full support, Version-M, or E.24. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Read the latest R0.75R research note →",
  "Expand 156 public notes",
  "Review v2.22 · 2026-09-04",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 246 public research notes",
  "R0.70A–R0.75R · 148 sections published",
  "R0.70A–R0.75R: 148 sections published, 104 fully archived",
  "R0.75R Step 43 constructs an exact global smooth high-band shear packet whose energy is concentrated in the positive outer cap while the canonical plateau sees only a Dirichlet tail. It rules out a uniform payment of arbitrary multimode packets by the plateau-only cubic mass. Full support, Version-M, and signed multimode alternatives remain open.",
  "R0.75R: outer-cap spectral concentration obstructs plateau-only multimode payment",
  "R0.75R | Outer-cap spectral concentration obstructs plateau-only multimode payment",
  "Literature review v2.22 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75R work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Egidi--Veselic 2016 gives a Logvinenko--Sereda type spectral observation result for band-limited functions on the torus; Wang--Wang--Zhang--Zhang 2019 shows that heat observability depends on quantitative thickness; and Coulhon--Sikora 2008 provides broader context for Gaussian off-diagonal heat bounds. R0.75R directly proves the needed short-time separated leakage for the one-dimensional periodic heat kernel and completes the outer-cap construction with an explicit Dirichlet packet. These neighboring results do not replace the local proof. A finite search establishes no completeness, novelty, or priority conclusion.",
  "Full cutoff support, Version-M exterior-row aggregation, quantitative spreading or thickness, signed multimode cancellation, nonconstant shear, and nonlinear mode transfer remain unresolved. Later material was not authorized, read, or published.",
  "PROVED: the exact radial cross-section identity R.12--R.14; real high-band support R.19--R.23; Dirichlet concentration and tails R.24--R.26; the exact smooth Navier--Stokes shear realization R.29--R.30; outer-cap persistence R.31--R.34; the positive signed-flux lower bound R.35; the plateau cubic upper bound R.38; and the divergent normalized quotient R.40--R.41. RULED OUT: a uniform Q-extension that pays every high-band packet only with the canonical plateau-shell cubic mass. NOT RULED OUT OR PROVED: full cutoff support, complete Version-M exterior rows, quantitative spreading or thickness, signed multimode cancellation, arbitrary nonconstant shear, nonlinear mode transfer, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity. This exact solution is globally smooth and supplies no singularity mechanism. There is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75R Step 43 bounded primary-source screen and claim boundary",
  "R0.75R Step 43 public boundary",
  "Step 43 constructs an exact global smooth constant-shear solution: a real high-band packet concentrates in the positive outer cap for one diffusive time while the plateau sees only a Dirichlet tail. The normalized flux-to-plateau-mass quotient diverges at a positive exponential rate. The conclusion rules out only the plateau-only multimode extension and does not refute full support, Version-M, or E.24.",
  "246 public research notes; latest node R0.75R.",
  "Research-note master index · v2.22 · 2026-09-04",
  "Latest node R0.75R · continuously revised",
  "Outer-cap spectral concentration obstructs plateau-only multimode payment",
  "335 / Full text",
  "336 / Full text",
  "337 / Full text",
  "338 / Full text",
  "339 / Full text",
  "340 / Full text",
  "341 / Full text",
  "342 / Full text",
  "343 / Full text",
  "This site stops at R0.75R Step 43. R rules out only a uniform payment of arbitrary high-band multimode packets by the canonical plateau-shell cubic mass. It does not refute full cutoff support, Version-M exterior rows, quantitative spreading or thickness, signed multimode cancellation, or E.24. Nonconstant shear, nonlinear mode transfer, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "Research note R0.75R · Step 43 · OUTER-CAP SPECTRAL CONCENTRATION OBSTRUCTION",
  "An explicit real high-band packet can concentrate in the positive outer cap of the radial cutoff and retain a fixed fraction of its energy for one diffusive time, while the canonical plateau shell sees only a Dirichlet tail. Consequently,",
  "diverges at an exact positive exponential rate, ruling out an unconditional extension of Q's plateau-only payment to arbitrary multimode packets. The counterexample is an exact global smooth Navier--Stokes shear solution and does not refute full-support payment, Version-M, or E.24.",
  "Status · R0.75R STEP 43",
  "Certificate: Python 21/21, Ruby 23/23, R.1--R.41, 41/41 tags, and 43/43 displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 76/76 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. This section contains no formal figure, simulation, numerical fit, DNS, or DGX.",
  "Step 43 main text",
  "Step 43 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
];

assert.equal(summaries.length, 46, "R0.75R Step 43 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75R Step 43 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75R Step 43 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75R Step 43 source-string count drift");
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
  release: "R0.75R Step 43",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
