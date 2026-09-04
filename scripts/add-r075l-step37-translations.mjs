#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075lstep37";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 240 research notes",
  "View the R0.75L card on the home page",
  "Current endpoint R0.75L Step 37 diffusive signed-flux gain",
  "The remaining work is to prove the multimode convolution and frozen-collar localization, pay |B|V_xi, and control nonconstant shear and the low difference-frequency sector. Later work was not authorized, read, or published.",
  "Jump to the R0.75L card on the home page →",
  "Research note R0.75L Step 37 · 2026-09-04 · DIFFUSIVE SIGNED-FLUX GAIN",
  "Read the latest R0.75L research note →",
  "Expand 150 public notes",
  "Review v2.16 · 2026-09-04",
  "After zero-mode cancellation, the exact one-real-harmonic family gives k^(-2) decay for the physical signed flux; comparison with the full-torus cubic mass yields a k^(-2/3) gain. Multimode interactions, the frozen collar, the |B|V_xi payment, and E.24 remain OPEN. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "For one real constant-shear passive harmonic, the zero mode vanishes before the absolute value is taken. Ordinary heat decay then gives k^(-2) for the physical signed flux, and comparison with the full-torus cubic mass yields a k^(-2/3) gain. The result does not extend to multimode interactions, the frozen collar, or E.24. NO NOVELTY CLAIM. NOT CLAY.",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 240 public research notes",
  "R0.70A–R0.75L · 142 sections published",
  "R0.70A–R0.75L: 142 sections published, 104 fully archived",
  "R0.75L Step 37 proves a diffusion-compatible k^(-2/3) gain for the physical signed flux of one real constant-shear harmonic after exact diagonal cancellation. Multimode convolution, frozen-collar localization, and payment of |B|V_xi remain open.",
  "R0.75L: diffusive gain for the physical signed flux of one harmonic",
  "R0.75L｜Diffusive high-frequency gain for the physical signed flux of one real harmonic",
  "Literature review v2.16 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75L work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "He supports a horizontal mode-by-mode enhanced-dissipation architecture; Gardner--Liss--Mattingly provide pathwise local-streamline context for passive shear diffusion; and Jimenez-Urias--Haine give an exact modal and Mathieu representation of periodic shear dispersion. R0.75L imports none of those stronger mechanisms and uses only ordinary heat decay for an exact constant-shear harmonic. None of the inspected sources proves the frozen-collar Version-M payment or E.24. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "Multimode convolution, frozen-collar localization, payment of |B|V_xi, nonconstant shear, and the low difference-frequency sector remain open. Later work was not authorized, read, or published.",
  "PROVED: the exact passive family L.2--L.5; diagonal zero-mode cancellation L.6--L.8; the k^(-2) physical signed-flux bound L.9; the exact cubic mass and k^(-2/3) payment gain L.10--L.13; the target-normalized diagnostic L.14--L.15; and the conditional frequency threshold L.16--L.17. SCOPE: one real constant-shear harmonic and a full-torus cubic mass; |B|V_xi remains unpaid. OPEN: multimode convolution, frozen-collar localization, nonconstant shear, the low difference-frequency sector, G.1, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity. There is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75L Step 37 bounded primary-source screen and claim boundary",
  "R0.75L Step 37 public boundary",
  "Step 37 first cancels the zero mode for one real constant-shear harmonic, then uses ordinary heat decay to obtain a k^(-2) bound for the physical signed flux; comparison with the exact full-torus cubic mass yields a k^(-2/3) gain.",
  "240 public research notes; latest node R0.75L.",
  "Diffusive high-frequency gain for the physical signed flux of one real harmonic",
  "Research-note master index · v2.16 · 2026-09-04",
  "Latest node R0.75L · continuously revised",
  ", without treating multimode interactions, the frozen collar, or the low-frequency sector.",
  ", and comparison with the exact full-torus cubic mass gives the genuine",
  ", and only then takes the absolute value; ordinary heat decay gives the physical signed flux",
  "294 / Full text",
  "295 / Full text",
  "296 / Full text",
  "297 / Full text",
  "298 / Full text",
  "299 / Full text",
  "300 / Full text",
  "This site stops at R0.75L Step 37. The physical signed flux of one real constant-shear harmonic has a diffusion-compatible k^(-2/3) gain. Multimode convolution, frozen-collar localization, payment of |B|V_xi, nonconstant shear, the low difference-frequency sector, G.1, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "For one real horizontal harmonic under constant shear, the periodic derivative first cancels the",
  "Research note R0.75L · Step 37 · DIFFUSIVE SIGNED-FLUX GAIN",
  "gain. This is a single-harmonic benchmark and does not pay",
  "Status · R0.75L STEP 37",
  "Certificate: Python 19/19, Ruby 20/20, L.1--L.17 and 17/17 displays, byte stability across three Python hash seeds, and complete regeneration stability; both implementations reject all 120/120 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. This section contains no formal figure, simulation, numerical fit, DNS, or DGX.",
  "Step 37 main text",
  "Step 37 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
];

assert.equal(summaries.length, 47, "R0.75L Step 37 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75L Step 37 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75L Step 37 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75L Step 37 source-string count drift");
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
  release: "R0.75L Step 37",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
