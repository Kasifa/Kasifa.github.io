#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074vstep21";

// Local direct translations in deterministic collectSiteStrings order.
const summaries = [
  "Master index of 224 research notes",
  "This route memo establishes exact decompositions, lifted-multiplicity coarse budgets, conditional target-superlevel algebra, and seven failure conditions. V.47-V.50, V.56, all-k occupation, and the remote common-shear comparison remain unproved. There is no scientific figure, DNS, or simulation. NOT CLAY.",
  "View the R0.74V card on the home page",
  "Current endpoint R0.74V Step 21 route memo",
  "Await an explicit frozen package in the same publication task. Unfrozen content is neither read nor published. The common-shear remote strip comes first, followed by the six-pair central-chart occupation problem; neither may be stated as proved in advance.",
  "Exact completion and splitting, lifted chord and volume budgets, and conditional target algebra are established. V.47-V.50, V.56, all-k lifted-copy occupation, and the remote common-shear comparison remain OPEN. This is not a completed-clock upper theorem. NOT CLAY.",
  "Jump to the R0.74V card on the home page →",
  "Research note R0.74V Step 21 · 2026-09-03 · ROUTE MEMO",
  "Read the latest R0.74V research note →",
  "Expand 134 public notes",
  "Review v2.00 · 2026-09-03",
  "The cumulative recap after R0.60 contains 161 nodes; the site now has 224 public research notes",
  "R0.70A-R0.74V · 126 sections published",
  "R0.70A-R0.74V: 126 sections published, 100 fully archived",
  "R0.74V Step 21 completes the exact decomposition, lifted-multiplicity coarse budgets, and conditional algebra for the completed-clock upper route. V.47-V.50, V.56, the all-k lifted-copy extension, the remote common-shear comparison, regularity, and singularity all remain OPEN.",
  "R0.74V: completed-clock upper route memo and occupation gates",
  "R0.74V｜Completed-clock upper route memo: exact decompositions, coarse budgets, and open occupation gates",
  "Step 21 separates the completed-clock upper route into exact completion, packet and cross-term absorption, lifted multiplicity, persistent baselines, and occupation gates. The analytic occupation estimates and remote common-shear comparison are not closed, so V.56 and the all-shell upper remain OPEN.",
  "This frozen package contains no literature audit and makes no novelty, priority, nonexistence, or publishability judgment. This page records mathematical claim grades only and does not convert a route plan into a literature-collision conclusion.",
  "Unfrozen content is neither read nor published; later results enter the site only after a frozen handoff.",
  "Open interface · R0.74W awaiting a frozen package",
  "Route memo",
  "Literature review v2.00 · 2026-09-03",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P-R0.74V work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Read the route memo",
  "PROVED (route components only): the good-time three-row completion and hard-time canonical-AC convention; exact shear and packet splitting; Young absorption of packet cross terms; the lifted chord; periodized-volume tiling; common-shear and all-shell coarse budgets; conditional target algebra; and the positive free-comparator exponent. FINITE: 33/33 Python groups and 77 cases; 7/7 Ruby groups and 106 assertions; all 29/29 and 30/30 mutations rejected. OPEN: V.47-V.50, V.56, the all-k lifted-copy extension, the remote and adjacent-inward common-shear comparison, the matching all-shell upper, fixed deletion, arbitrary-clock extraction, scale contraction, regularity, singularity, and the Millennium problem. There is no scientific figure, DNS, simulation, or PDE data.",
  "R0.74V Step 21 public boundary",
  "R0.74V Step 21 route and claim boundary",
  "Step 21 establishes exact completion and splitting, lifted-multiplicity coarse budgets, conditional algebra, and failure conditions. V.47-V.50, V.56, all-k lifted-copy occupation, and the remote common-shear comparison remain OPEN.",
  "224 public research notes; latest node R0.74V.",
  "Completed-clock upper route memo: exact decompositions, coarse budgets, and open occupation gates",
  "Research-note master index · v2.00 · 2026-09-03",
  "Latest node R0.74V · continuously revised",
  "156 / Full text",
  "157 / Full text",
  "158 / Full text",
  "159 / Full text",
  "160 / Full text",
  "161 / Full text",
  "162 / Full text",
  "163 / Full text",
  "164 / Full text",
  "165 / Full text",
  "This section establishes only the exact decompositions, coarse budgets, conditional algebra, and failure conditions for the completed-clock upper route.",
  "This site stops at R0.74V Step 21. A later result may be published only after a separate frozen handoff; the current unfrozen R0.74W is neither read nor disclosed. V.0 remote comparison precedes V.1 finite-table occupation, and neither may be stated as proved in advance.",
  "The current proposal concerns whole-annulus moving-centre occupation estimates for only six central-chart pairs. It must handle inversion partners, periodic copies, weighted remainders, accumulated viscosity, and the derivative collar. The existing near-lobe comparison covers only the main-lobe neighborhood and cannot replace a whole-annulus estimate. V.47-V.50 remain OPEN; every all-k use requires a separate lifted-copy summation proof.",
  "For the exact common-shear solution, orthogonality of velocity components gives",
  "rather than erasing lifted multiplicity with a single-torus volume cap.",
  "Conclusion first: this is a route memo, not an upper theorem",
  "The route fails if any of the following occurs: the common-shear floor is too high; viscosity or anomalous defect creates a persistent baseline; an amplified tail remainder is not integrable; the generalized scale is too slow; the terminal plateau is confused with the full cutoff interval; height, duration, and variation are conflated; or a single central-lift distance is reused at large shell index. Each item must become either an explicit hypothesis or a proved estimate in any theorem statement.",
  "Route main text",
  "Seven failure conditions",
  "Global packet energy and the lifted chord give the stated scale for the endpoint-plus-viscosity ceiling. The common shear creates a persistent baseline. If it is not strictly below the tested level, a duration upper bound may fail directly. The all-shell shear sum also requires the amplitude ratio to be controlled, so no uniform conclusion holds for every positive amplitude allowed by R0.74U.",
  "If the persistent baseline formed by the common shear, the two accumulated viscosity rows, and anomalous defect is below half the tested level, and every weighted remainder gate in V.47-V.50 passes, a union bound reduces the target-coordinate superlevel set to two packet endpoint sets and formally gives",
  "Stopping line and next research item",
  "Likewise, the volume uses the exact tiling identity",
  "The completed clock's three-row nonnegative ledger",
  "The smallest next proposition is the remote adjacent-inward common-shear comparison, followed by weighted annular occupation for the six-pair finite table. The following all remain OPEN: V.47-V.50, V.56, every all-k lifted-copy extension, the remote and adjacent-inward common-shear comparison, the matching all-shell upper, fixed deletion, arbitrary-clock extraction, scale contraction, regularity, singularity, and the Navier-Stokes Millennium problem. This release has no literature audit and makes no novelty, priority, or publishability judgment; it contains no DNS, simulation, or PDE data. Formal figure: NOT APPLICABLE. This section is purely analytic and contains no Navier--Stokes numerical simulation, DNS, DGX, or formal figure.",
  "Determine the remote adjacent-inward common-shear comparison first",
  "Research note R0.74V · Step 21 · route memo",
  "Coarse scale budgets already available",
  "At local-energy good times, the completed clock consists of endpoint kinetic energy, accumulated ordinary viscosity, and accumulated anomalous defect. For a general suitable weak solution, hard times require the canonical absolutely continuous representative; the raw endpoint formula cannot be forced to hold everywhere. The anomalous defect vanishes for the frozen smooth family but must remain a separate row in any extension.",
  "In the adjacent inward shell, the shell-weight gain and free heat-kernel tail cost combine to give",
  "After expanding the two packets, the endpoint and viscous cross terms are signed, but Cauchy-Schwarz and Young absorb them safely into the two diagonal rows:",
  "This resolves the cross terms in the pointwise upper bound but does not automatically control positive variation.",
  "This is the conditional route to V.56. Since its occupation inputs remain unproved, V.56 itself remains OPEN.",
  "This exact finite arithmetic shows that the free comparator predicts an exponentially amplified inward tail. It is not a lower bound for the common-shear solution. A relative bridge comparison, inversion control, and noncancellation by the other packet on the remote strip are still required, so no all-shell counterexample follows yet.",
  "The periodized cutoff is a sum of Euclidean lifts, not a projected indicator. With the stated outer support radius, the correct one-dimensional chord budget is",
  "Status · R0.74V STEP 21",
  "The adjacent-inward free comparator has a positive exponent",
  "Lifted multiplicity cannot be capped by a torus length",
  "NEXT / R0.74W awaiting a frozen package",
  "Python: 33/33 checks and 77 exact finite cases; independent Ruby: 7/7 groups and 106 assertions. Python and Ruby reject 29/29 and 30/30 intentional mutations respectively. Finite arithmetic and structural certificates do not replace a continuum PDE proof. This route package has no scientific figure, DNS, simulation, or PDE data.",
  "QA script",
  "R0.74V breaks the proof obligations for a completed-clock upper bound into an auditable ledger. What is established consists of exact decompositions, coarse scale budgets, conditional algebra, and failure conditions; neither a target-coordinate upper bound nor an all-shell upper bound is established. R0.74U's certified geometric corridor still gives only one-way inclusion and a lower measure bound for the K-superlevel, and cannot be used in reverse.",
  "R0.74W frozen package not yet published →",
  "Shear, packets, and cross terms",
  "Step 21 route main text, audits, two independent certificate implementations, and QA",
  "V.47-V.50, V.56, the all-k lifted-copy extension, and the remote common-shear comparison all remain OPEN; this is not a completed-clock upper theorem. NOT CLAY.",
  "V.47-V.50: finite-table occupation remains an open input",
  "V.56 contains conditional algebra only; the analytic closure is missing",
];

assert.equal(summaries.length, 81, "R0.74V Step 21 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.74V Step 21 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.74V Step 21 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.74V Step 21 source-string count drift");
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
  release: "R0.74V Step 21",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
