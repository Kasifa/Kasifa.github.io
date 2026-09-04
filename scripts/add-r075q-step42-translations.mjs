#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075qstep42";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 245 research notes",
  "View the R0.75Q card on the home page",
  "Current endpoint R0.75Q Step 42 spatially spread harmonic collar payment",
  "For one spatially spread constant-shear real harmonic independent of x_1 and x_3, exact zero-row cancellation, phase-uniform periods, and a rectangular subcollar yield a local cubic of size R^3 k^(-2) A^3 and convert the signed flux to k^(-2/3) M_col^(2/3). No entrance-concentration condition is needed; Q.26 covers only an actual component of the same velocity, while multimode and general low-entrance packets remain open. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Destructive interference between two or more horizontal modes, arbitrary vertical structure, general low-entrance packets, nonconstant shear, inter-packet and low-difference summation, and removal of the total upper-frequency cap remain unresolved. Later work was not authorized, read, or published.",
  "Jump to the R0.75Q card on the home page →",
  "Research note R0.75Q Step 42 · 2026-09-04 · SPATIALLY SPREAD HARMONIC COLLAR PAYMENT",
  "One constant-shear real harmonic independent of x_1 and x_3 first undergoes exact constant-row cancellation in the radial derivative row. A phase-uniform period count and rectangular subcollar then give M_col >= c_box delta_0 a^2 R^3 k^(-2) A^3 and pay the signed flux by k^(-2/3) M_col^(2/3), without entrance concentration. The Version-M inclusion covers only an actual component of the same velocity. NO NOVELTY CLAIM. NOT CLAY.",
  "Read the latest R0.75Q research note →",
  "Expand 155 public notes",
  "Review v2.21 · 2026-09-04",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 245 public research notes",
  "R0.70A–R0.75Q · 147 sections published",
  "R0.70A–R0.75Q: 147 sections published, 104 fully archived",
  "R0.75Q Step 42 uses exact zero-row cancellation, a phase-uniform period count, and a rectangular subcollar to complete the physical-collar payment for one spatially spread constant-shear real harmonic independent of x_1 and x_3. Multimode interference, vertical structure, and general low-entrance packets remain open.",
  "R0.75Q: physical-collar payment for one spatially spread harmonic",
  "R0.75Q | Physical-collar payment for one spatially spread harmonic",
  "Destructive interference between two or more horizontal modes, arbitrary vertical structure, general low-entrance packets, nonconstant shear, inter-packet and low-difference summation, and removal of the total upper-frequency cap remain unresolved. Later material was not authorized, read, or published.",
  "Literature review v2.21 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75Q work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "He 2022 gives mode-by-mode shear diffusion for passive scalars; Gardner--Liss--Mattingly 2024 and He 2026 give pathwise or streamline-localized enhanced dissipation; Jimenez-Urias--Haine 2021 gives an exact modal solution for periodic shear; and Wang--Wang--Zhang--Zhang 2019 treats heat observability on thick or positive-measure sets. None of these neighboring results is a signed derivative cutoff and local L3-atom payment on a shrinking spherical shell. R0.75Q imports none of their theorems and directly proves the phase-uniform period bound and rectangular-subcollar estimate. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "PROVED: the radial derivative L1 row Q.8--Q.10; exact diagonal cancellation and the flux bound Q.11--Q.14; the phase-uniform rectangular subcollar Q.15--Q.21; the physical-collar cubic conversion Q.22--Q.25; the conditional actual-component Version-M payment Q.26 under the stated alignment; and the low-entrance diagnostic Q.27--Q.28. SCOPE: constant shear, one real horizontal harmonic, independence of x_1 and x_3, and a total-field formulation; no entrance-concentration condition is needed. Q.26 additionally requires a same-velocity actual-component realization and explicitly excludes Fourier/LP projections and arbitrary zero-trajectory realizations. OPEN: two or more horizontal modes, destructive interference, arbitrary vertical structure, general low-entrance packets, nonconstant shear, inter-packet and low-difference summation, removal of the total upper-frequency cap, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity. There is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75Q Step 42 bounded primary-source screen and claim boundary",
  "R0.75Q Step 42 public boundary",
  "For one constant-shear real harmonic independent of x_1 and x_3, Step 42 first controls the signed cutoff flux by exact constant-row cancellation and then obtains cubic mass from a phase-uniform period count and rectangular subcollar. The resulting payment is k^(-2/3) M_col^(2/3) and requires no entrance concentration. The Version-M inclusion covers only an actual component of the same velocity.",
  "245 public research notes; latest node R0.75Q.",
  "Physical-collar payment for one spatially spread harmonic",
  "Research-note master index · v2.21 · 2026-09-04",
  "Latest node R0.75Q · continuously revised",
  ", thereby paying with",
  "328 / Full text",
  "329 / Full text",
  "330 / Full text",
  "331 / Full text",
  "332 / Full text",
  "333 / Full text",
  "334 / Full text",
  "This site stops at R0.75Q Step 42. Q closes the physical-collar payment only for one spatially spread real harmonic independent of x_1 and x_3, using exact zero-row cancellation, phase-uniform periods, and a rectangular subcollar; the Version-M inclusion still applies only to an actual component of the same velocity. Two or more horizontal modes, destructive interference, arbitrary vertical structure, general low-entrance packets, nonconstant shear, inter-packet and low-difference summation, removal of the total upper-frequency cap, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "that is one constant-shear real harmonic: the radial cutoff's constant row vanishes exactly, and a phase-uniform period count with a rectangular subcollar then gives",
  "Consider a field independent of",
  "Research note R0.75Q · Step 42 · SPATIALLY SPREAD HARMONIC COLLAR PAYMENT",
  "to pay the signed flux. This mechanism needs no entrance-concentration condition and covers one spatially spread benchmark not reached by P; multimode interference, vertical structure, and general low-entrance packets remain",
  "Status · R0.75Q STEP 42",
  "Certificate: Python 20/20, Ruby 21/21, Q.1--Q.28 and 28/28 displays, byte stability across three Python hash seeds, and complete regeneration stability; both implementations reject all 180/180 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. This section contains no formal figure, simulation, numerical fit, DNS, or DGX.",
  "Step 42 main text",
  "Step 42 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
];

assert.equal(summaries.length, 46, "R0.75Q Step 42 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75Q Step 42 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75Q Step 42 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75Q Step 42 source-string count drift");
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
  release: "R0.75Q Step 42",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
