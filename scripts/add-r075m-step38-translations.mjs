#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075mstep38";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 241 research notes",
  "View the R0.75M card on the home page",
  "Current endpoint R0.75M Step 38 dyadic-packet diffusive gain",
  "The remaining work is to complete inter-packet summation, quantify the frozen-collar W_xi row, localize the cubic mass, and control nonconstant shear and the low difference-frequency sector. Later work was not authorized, read, or published.",
  "Jump to the R0.75M card on the home page →",
  "Research note R0.75M Step 38 · 2026-09-04 · DYADIC-PACKET DIFFUSIVE GAIN",
  "Read the latest R0.75M research note →",
  "Expand 151 public notes",
  "Review v2.17 · 2026-09-04",
  "The exact finite dyadic packet preserves the K^(-2/3) gain for the physical signed flux through diagonal cancellation, a Schur/Wiener row, and short-time cubic conversion, with no separate packet-cardinality loss. Inter-packet summation, frozen-collar calibration, the local Version-M atom, and E.24 remain OPEN. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Within one real dyadic constant-shear packet, the diagonal vanishes before the absolute value is taken. The exact modal kernel, Schur/Wiener row, and short-time cubic conversion preserve the K^(-2/3) gain without a separate packet-cardinality factor. The conclusion does not extend to inter-packet interactions, the frozen collar, or E.24. NO NOVELTY CLAIM. NOT CLAY.",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 241 public research notes",
  "R0.70A–R0.75M · 143 sections published",
  "R0.70A–R0.75M: 143 sections published, 104 fully archived",
  "R0.75M Step 38 proves that arbitrary finite interference inside one real dyadic constant-shear packet does not destroy the K^(-2/3) gain for the physical signed flux and introduces no separate mode-count loss. Inter-packet summation, frozen-collar calibration, and low differences remain open.",
  "R0.75M: mode-count-free diffusive gain for the signed flux of a dyadic packet",
  "R0.75M｜Diffusive signed-flux gain for one dyadic packet",
  "Literature review v2.17 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75M work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "He supports horizontal mode-by-mode enhanced-dissipation analysis and a summation architecture; Gardner--Liss--Mattingly provide context for pathwise control under nonconstant shear; and Jimenez-Urias--Haine give an exact modal representation of periodic shear dispersion. R0.75M's specific Schur/Wiener kernel and Version-M boundary are local derivations. None of the inspected sources proves the frozen-collar Wiener payment, inter-packet summation, or E.24. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "Inter-packet summation, frozen-collar W_xi calibration, the local Version-M atom, nonconstant shear, and the low difference-frequency sector remain open. Later work was not authorized, read, or published.",
  "PROVED: the finite real dyadic-packet solution M.3--M.6; the exact modal kernel and diagonal cancellation M.7; the Schur/Wiener energy bound M.8--M.11; short-time cubic conversion M.12--M.16; the second-derivative Wiener row M.17; and the target-normalized diagnostic M.18--M.20. SCOPE: one finite real dyadic constant-shear packet and a full-torus cubic mass, with no separate packet-cardinality factor. OPEN: inter-packet summation, frozen-collar W_xi calibration, the local Version-M atom, nonconstant shear, the low difference-frequency sector, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity. There is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75M Step 38 bounded primary-source screen and claim boundary",
  "R0.75M Step 38 public boundary",
  "Step 38 uses the exact modal kernel, diagonal cancellation, a Schur/Wiener row, and short-time cubic conversion to preserve the K^(-2/3) gain for an arbitrary finite real dyadic packet without a separate packet-cardinality loss.",
  "241 public research notes; latest node R0.75M.",
  "Diffusive signed-flux gain for one dyadic packet",
  "Research-note master index · v2.17 · 2026-09-04",
  "Latest node R0.75M · continuously revised",
  ", followed by the short-time heat lower bound and full-torus cubic mass to obtain",
  "; the exact modal kernel, Schur's test, and Parseval give the against-energy bound",
  "; inter-packet summation, frozen-collar calibration, and the low difference-frequency sector remain open.",
  "301 / Full text",
  "302 / Full text",
  "303 / Full text",
  "304 / Full text",
  "305 / Full text",
  "306 / Full text",
  "307 / Full text",
  "This site stops at R0.75M Step 38. Arbitrary finite interference inside one real dyadic constant-shear packet preserves the K^(-2/3) gain for the physical signed flux without a separate packet-cardinality loss. Inter-packet summation, frozen-collar W_xi calibration, the local Version-M atom, nonconstant shear, the low difference-frequency sector, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "For an arbitrary finite real dyadic horizontal packet under constant shear, the periodic derivative first cancels",
  "Research note R0.75M · Step 38 · DYADIC-PACKET DIFFUSIVE GAIN",
  "gain with no separate packet-cardinality loss. The retained cost is",
  "Status · R0.75M STEP 38",
  "Certificate: Python 19/19, Ruby 20/20, M.1--M.20 and 20/20 displays, byte stability across three Python hash seeds, and complete regeneration stability; both implementations reject all 130/130 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. This section contains no formal figure, simulation, numerical fit, DNS, or DGX.",
  "Step 38 main text",
  "Step 38 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
];

assert.equal(summaries.length, 47, "R0.75M Step 38 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75M Step 38 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75M Step 38 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75M Step 38 source-string count drift");
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
  release: "R0.75M Step 38",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
