#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075nstep39";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 242 research notes",
  "View the R0.75N card on the home page",
  "Current endpoint R0.75N Step 39 radial-collar averaged Wiener row",
  "The remaining work is to extend the one-dimensional constant-shear time kernel through vertical diffusion and nonconstant shear, pay the local cubic mass with a buffered-collar atom, and control inter-packet summation and low difference frequencies. Later work was not authorized, read, or published.",
  "Jump to the R0.75N card on the home page →",
  "Research note R0.75N Step 39 · 2026-09-04 · RADIAL-COLLAR AVERAGED WIENER ROW",
  "For one selectable canonical radial collar, x_1 averaging gives a coefficientwise-supremum Wiener row O(L), and full transverse averaging gives O(L^2R). Exact slice geometry includes spherical tangency, while the low/high Fourier-sample split avoids an R^(-1) loss. The conclusion does not extend to a universal cutoff, dynamical flux, or E.24. NO NOVELTY CLAIM. NOT CLAY.",
  "A selectable canonical radial collar uses exact slice geometry, a first/third radial-derivative ledger, and a low/high Fourier-sample split to obtain an x_1-averaged Wiener row O(L) and a fully averaged row O(L^2R), with no negative power of R. Universal-cutoff, dynamical-flux, local cubic-payment, and E.24 claims remain OPEN. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Read the latest R0.75N research note →",
  "Expand 152 public notes",
  "Review v2.18 · 2026-09-04",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 242 public research notes",
  "R0.70A–R0.75N · 144 sections published",
  "R0.70A–R0.75N: 144 sections published, 104 fully archived",
  "R0.75N Step 39 proves that one selectable canonical radial collar has an x_1-averaged derivative Wiener row O(L) and a fully averaged row O(L^2R), with no negative power of R in the high-frequency coefficient diagnostic. Vertical diffusion, local payment, inter-packet interactions, and low differences remain open.",
  "R0.75N: averaged Wiener row for a canonical radial collar",
  "R0.75N｜Averaged Wiener row for a radial collar without an R^(-1) loss",
  "Literature review v2.18 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75N work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Garces--Rhodes--Peña support the correspondence between physical projection and Fourier slicing; Rux--Quellmalz--Steidl provide a neighboring framework of radial averaging, Abel-type relations, and one-dimensional Fourier transforms; and Herz gives the classical connection between convex-boundary curvature and Fourier decay. R0.75N's discrete sampling split, coefficientwise x_3 supremum, tangency-area payment, and frozen R,L scaling are local proofs. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "PROVED: the canonical radial collar N.1--N.5; the scale-correct Fourier sampling lemma N.6--N.9; the uniform x_1-averaged coefficient row N.10--N.13; the fully averaged row N.14--N.16; and the high-frequency coefficient diagnostic N.17. SCOPE: one selectable canonical radial representative in the central torus chart; the rows are O(L) and O(L^2R), with spherical tangencies included. OPEN: a universal-cutoff statement, vertical diffusion, nonconstant shear, buffered-collar local cubic payment, inter-packet summation, low differences, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity. There is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75N Step 39 bounded primary-source screen and claim boundary",
  "R0.75N Step 39 public boundary",
  "Step 39 proves an O(L) x_1-averaged row and an O(L^2R) fully averaged row for one selectable canonical radial collar using exact slice geometry, a first/third radial-derivative ledger, and a low/high Fourier-sample split.",
  "A universal-cutoff result, vertical diffusion, nonconstant shear, buffered-collar local cubic payment, inter-packet summation, and low difference frequencies remain open. Later work was not authorized, read, or published.",
  "242 public research notes; latest node R0.75N.",
  "Averaged Wiener row for a radial collar without an R^(-1) loss",
  "Research-note master index · v2.18 · 2026-09-04",
  "Latest node R0.75N · continuously revised",
  ", horizontal averaging removes the apparent pointwise derivative",
  "; averaging in x_3 as well gives",
  ". This is a selectable geometric coefficient theorem, not a universal-cutoff or dynamical-flux theorem.",
  "308 / Full text",
  "309 / Full text",
  "310 / Full text",
  "311 / Full text",
  "312 / Full text",
  "313 / Full text",
  "314 / Full text",
  "This site stops at R0.75N Step 39. A selectable canonical radial collar has an x_1-averaged Wiener row O(L) and a fully averaged row O(L^2R), and the high-frequency diagnostic has no negative power of R. A universal-cutoff result, vertical diffusion, nonconstant shear, buffered-collar local cubic payment, inter-packet summation, low differences, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "For one representative allowed by the frozen outer-collar construction",
  "before summation, giving",
  "loss. Each coefficient first takes an",
  "Research note R0.75N · Step 39 · RADIAL-COLLAR AVERAGED WIENER ROW",
  "Status · R0.75N STEP 39",
  "Certificate: Python 16/16, Ruby 17/17, N.1--N.17 and 17/17 displays, byte stability across three Python hash seeds, and complete regeneration stability; both implementations reject all 107/107 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. This section contains no formal figure, simulation, numerical fit, DNS, or DGX.",
  "Step 39 main text",
  "Step 39 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
];

assert.equal(summaries.length, 48, "R0.75N Step 39 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75N Step 39 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75N Step 39 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75N Step 39 source-string count drift");
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
  release: "R0.75N Step 39",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
