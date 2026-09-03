#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075hstep33";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 236 research notes",
  "A Feynman--Kac occupation estimate, resolvent estimate, or separately paid source information must be added without reusing the target dissipation. Later work was not authorized, read, or published.",
  "View the R0.75H card on the home page",
  "Current endpoint R0.75H Step 33 pure-transport terminal-tube closure",
  "Jump to the R0.75H card on the home page →",
  "Research note R0.75H Step 33 · 2026-09-03 · PURE-TRANSPORT TERMINAL-TUBE CLOSURE",
  "Read the latest R0.75H research note →",
  "In the exact ballistic benchmark, the nondecreasing cutoff controls the positive signed flux by terminal half-energy; one-pass terminal-tube persistence and cubic payment give an R^(1/3) gain with rate -4279/238140000. This conclusion does not cover diffusion, and E.24 remains OPEN. NO NOVELTY CLAIM. NOT CLAY.",
  "Expand 146 public notes",
  "Review v2.12 · 2026-09-03",
  "The exact pure-transport identity controls the positive signed flux by terminal half-energy; one-pass terminal-tube persistence and spacetime Holder give an R^(1/3) benchmark gain. The diffusive H.28 route remains circular, and E.24 is not closed. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 236 public research notes",
  "R0.70A–R0.75H · 138 sections published",
  "R0.70A–R0.75H: 138 sections published, 104 fully archived",
  "R0.75H Step 33 realizes an R^(1/3) gain in the exact pure-transport benchmark using the signed endpoint identity, one-pass terminal-tube persistence, and spacetime Holder. The diffusive H.28 identity returns the target dissipation to the right-hand side, so E.24 still requires an independent estimate.",
  "R0.75H: pure-transport terminal tube and R^(1/3) benchmark gain",
  "R0.75H｜One-pass terminal-tube closure for the pure-transport collar flux: the R^(1/3) gain realized in the ballistic benchmark",
  "An independent Feynman--Kac occupation estimate, resolvent estimate, or separately paid source row must be added without putting the target dissipation back on the right. Later work was not authorized, read, or published.",
  "Literature review v2.12 · 2026-09-03",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75H work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Alphonse--Martin use integral-thickness geometry in a moving-support control result; Gardner--Liss--Mattingly add diffusive trajectories and local shear in their pathwise method; Albritton--Dong retain a quantitative drift-flux cost in local passive-scalar theory. None of the inspected sources gives the frozen terminal-tube cubic estimate, removes the target dissipation from H.28, or proves E.24. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "PROVED: the full-window signed pure-transport identity H.13--H.14, terminal persistence H.16--H.19, cubic payment H.23, the strict rate -4279/238140000, and the R^(1/3) scale H.26 under the matching-background hypothesis. BENCHMARK ONLY: P_R^(M,tr) is the Version-M formula evaluated on the pure-transport pair, not payment for a Navier--Stokes solution; the conclusion controls only the positive signed flux, not absolute flux, multiple windings, or diffusion. OPEN: an independently paid diffusive terminal-tube or resolvent estimate, shear-transition bands, periodic recrossing, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity. There is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75H Step 33 bounded primary-source screen and claim boundary",
  "R0.75H Step 33 public boundary",
  "Step 33 proves the exact signed-flux endpoint identity for a nondecreasing cutoff and realizes an R^(1/3) benchmark gain in a fixed-lift, no-seam, one-pass terminal tube using characteristic persistence and spacetime Holder. This pair is not a Navier--Stokes solution functional, and the diffusive H.28 route remains circular.",
  "236 public research notes; latest node R0.75H.",
  "One-pass terminal-tube closure for the pure-transport collar flux: the R^(1/3) gain realized in the ballistic benchmark",
  "Research-note master index · v2.12 · 2026-09-03",
  "Latest node R0.75H · continuously revised",
  "265 / Full text",
  "266 / Full text",
  "267 / Full text",
  "268 / Full text",
  "269 / Full text",
  "270 / Full text",
  "271 / Full text",
  "This site stops at R0.75H Step 33. This section closes only the exact pure-transport ballistic benchmark; the positive dissipation in H.28 is the target unknown and cannot be used circularly. Multiple blocks, shear-transition bands, periodic recrossing, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain unresolved. Later work was not authorized, read, or published.",
  "The frozen nondecreasing time cutoff gives an exact signed-flux endpoint identity; characteristic persistence in a one-pass terminal tube and spacetime Holder then realize",
  "Research note R0.75H · Step 33 · PURE-TRANSPORT TERMINAL-TUBE CLOSURE",
  "gain, with strict rate",
  "This proves only the pure-transport benchmark; diffusive E.24 remains OPEN. NO NOVELTY CLAIM. NOT CLAY.",
  "Status · R0.75H STEP 33",
  "Certificate: Python 19/19, Ruby 22/22, H.1--H.29 and 29/29 displays, and byte stability across three Python hash seeds; both implementations reject all 66/66 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12 and explicitly includes fixtures and expected JSON. This section is purely analytic and contains no formal figure, simulation, numerical fit, DNS, or DGX.",
  "The diffusive terminal-tube estimate and E.24 remain OPEN",
  "Step 33 main text",
  "Step 33 main text, primary-source boundary, two certificate implementations, and fail-closed QA"
];

assert.equal(summaries.length, 46, "R0.75H Step 33 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75H Step 33 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75H Step 33 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75H Step 33 source-string count drift");
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
  release: "R0.75H Step 33",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
