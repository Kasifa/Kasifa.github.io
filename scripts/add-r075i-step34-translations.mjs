#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075istep34";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 237 research notes",
  "N_eff must be controlled independently from shear transport, diffusion, and collar geometry, or sufficiently strong signed inter-block cancellation must be proved; one-block localization alone cannot close E.24. Later work was not authorized, read, or published.",
  "View the R0.75I card on the home page",
  "On a single O(R^3) block, support volume and spacetime Holder pay the flux with strict rate -4279/238140000; N_eff^(1/3) is the exact aggregation loss, and theta<8558/35721 is required to retain the target coefficient. Uniform participation across all blocks has rate +27163/476280000, while high participation is not a necessary obstruction. E.24 remains OPEN. NO NOVELTY CLAIM. NOT CLAY.",
  "Current endpoint R0.75I Step 34 diffusion-safe block participation",
  "Jump to the R0.75I card on the home page →",
  "Research note R0.75I Step 34 · 2026-09-03 · DIFFUSION-SAFE BLOCK PARTICIPATION",
  "Read the latest R0.75I research note →",
  "Expand 147 public notes",
  "Review v2.13 · 2026-09-03",
  "The one-block flux estimate uses no passive PDE, and N_eff^(1/3) records the aggregation loss exactly; theta<8558/35721 is sufficient for the absolute block-summation route, but high participation is not a necessary obstruction. E.24 is not closed. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 237 public research notes",
  "R0.70A–R0.75I · 139 sections published",
  "R0.70A–R0.75I: 139 sections published, 104 fully archived",
  "R0.75I Step 34 defines the exact N_eff aggregation loss using a PDE-independent one-block Holder estimate and obtains the conditional threshold theta<8558/35721, equivalently beta>27163/35721. Participation control for the actual diffusing field or signed inter-block cancellation remains unproved.",
  "R0.75I: diffusion-safe block estimate and exact participation threshold",
  "R0.75I｜Diffusion-safe one-block flux estimate and the effective-participation threshold",
  "The actual diffusing field's N_eff must be controlled independently, or sufficiently strong signed inter-block cancellation must be proved; the one-block estimate alone cannot close E.24. Later work was not authorized, read, or published.",
  "Literature review v2.13 · 2026-09-03",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75I work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Albritton--Dong identify a special bounded-total-speed boundary for passive scalars; the Hu--Li Davies weighted-semigroup method supports off-diagonal heat-kernel reasoning; and Aronson's classical result gives Gaussian fundamental-solution bounds under its hypotheses. None of the inspected sources gives the I.19 participation estimate, signed cross-mode E.24, or the frozen Version-M payment ledger. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "PROVED: the arbitrary-field one-block estimate I.10--I.14, exact participation identity and bounds I.15--I.17, conditional threshold I.19--I.23, adverse uniform-block rate I.24--I.26, and high-participation zero-flux diagnostic I.27. SUFFICIENT ONLY: N_eff<=C R^(-theta) with theta<8558/35721 pays the absolute block-summation route; this is not a theorem for the actual diffusing field, and high participation is neither a necessary obstruction nor an E.24 counterexample. OPEN: an N_eff bound for the actual diffusing field, signed inter-block cancellation, shear-transition bands, periodic recrossing, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity. There is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75I Step 34 bounded primary-source screen and claim boundary",
  "R0.75I Step 34 public boundary",
  "Step 34 proves a PDE-independent arbitrary-field one-block estimate and records the multi-block aggregation loss exactly as N_eff^(1/3); theta<8558/35721 is equivalent to beta>27163/35721. The condition is sufficient but not necessary, and a high-participation zero mode can still have zero flux on every block.",
  "237 public research notes; latest node R0.75I.",
  "Diffusion-safe one-block flux estimate and the effective-participation threshold",
  "Research-note master index · v2.13 · 2026-09-03",
  "Latest node R0.75I · continuously revised",
  ", but participation control for the actual diffusing field remains unproved.",
  "272 / Full text",
  "273 / Full text",
  "274 / Full text",
  "275 / Full text",
  "276 / Full text",
  "277 / Full text",
  "278 / Full text",
  "This site stops at R0.75I Step 34. The one-block estimate is diffusion-safe, but it does not prove that the actual diffusing field satisfies the N_eff threshold; high participation is not a necessary obstruction either. Signed inter-block cancellation, transition bands, periodic recrossing, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain unresolved. Later work was not authorized, read, or published.",
  "Without using the passive PDE, support volume, coefficient bounds, and spacetime Holder give the one-block estimate; the effective participation count",
  "is equivalent to",
  "Multi-block participation or signed cancellation remains OPEN",
  "records the multi-block aggregation loss exactly. The condition",
  "Research note R0.75I · Step 34 · DIFFUSION-SAFE BLOCK PARTICIPATION",
  "Status · R0.75I STEP 34",
  "Certificate: Python 18/18, Ruby 24/24, I.1--I.27 and 27/27 displays, byte stability across three Python hash seeds, and complete regeneration stability; both implementations reject all 83/83 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. This section contains no formal figure, simulation, numerical fit, DNS, or DGX.",
  "Step 34 main text",
  "Step 34 main text, primary-source boundary, two certificate implementations, and fail-closed QA"
];

assert.equal(summaries.length, 47, "R0.75I Step 34 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75I Step 34 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75I Step 34 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75I Step 34 source-string count drift");
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
  release: "R0.75I Step 34",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
