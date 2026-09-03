#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074wstep22";

// Local direct translations in deterministic collectSiteStrings order.
const summaries = [
  "101 sections fully archived",
  "Master index of 225 research notes",
  "View the R0.74W card on the home page",
  "Uncommitted R0.74X and R0.74Y are not being read or published. Later work must first receive an independent freeze; a one-coordinate endpoint divergence must not be rewritten as a fixed-deletion obstruction or an arbitrary-solution theorem.",
  "Current endpoint R0.74W Step 22",
  "Frozen four-panel figure",
  "Jump to the R0.74W card on the home page →",
  "Research note R0.74W Step 22 · 2026-09-03",
  "Read the latest R0.74W research note →",
  "Expand 135 public notes",
  "Review v2.01 · 2026-09-03",
  "The exact all-winding bridge yields the relative survival and sweeping threshold; packet 2 forces adjacent-inward weighted endpoint divergence, disproving the matching all-shell upper bound for the frozen placement. Fixed deletion remains OPEN. NOT CLAY.",
  "The exact all-winding bridge comparison proves the relative threshold on the remote strip. On the original scale packet 1 is swept and packet 2 survives, with the latter causing adjacent-inward weighted endpoint divergence. The matching all-shell upper bound is FALSE for the frozen placement, but fixed deletion remains OPEN. NOT CLAY.",
  "The cumulative recap after R0.60 contains 161 nodes; the site now has 225 public research notes",
  "R0.70A-R0.74W · 127 sections published",
  "R0.70A-R0.74W: 127 sections published, 101 fully archived",
  "R0.74W Step 22 proves the remote adjacent-inward relative threshold for the frozen common-shear family and derives weighted endpoint divergence from packet 2. The matching all-shell upper bound is FALSE for this placement; fixed deletion, whole-shell occupation, general solutions, and regularity remain OPEN.",
  "R0.74W: remote common-shear threshold and frozen-placement obstruction",
  "R0.74W｜Remote adjacent-inward common-shear threshold and weighted endpoint obstruction",
  "Step 22 frozen four-panel figure",
  "The frozen audit screened exact shear waves, enhanced dissipation and hypoellipticity, shear-flow large deviations, random-shear Brownian-bridge functionals, and Fourier-helical residence-time compression. It found no exact collision with the complete six-part conjunction. This is only a finite primary-source non-hit dated 2026-09-03, not evidence of novelty, priority, correctness, nonexistence, or publishability.",
  "Open interface · awaiting the next frozen package",
  "Uncommitted R0.74X and R0.74Y are neither read nor published; a one-coordinate endpoint divergence cannot be promoted to a fixed-deletion obstruction.",
  "Literature and claim boundaries",
  "Literature review v2.01 · 2026-09-03",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P-R0.74W work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Read the complete note",
  "PROVED (frozen exact family only): the all-winding bridge representation; the logarithmic rate in central conditional probability; strict survival and sweeping on the uniform slab; amplitude-weighted inversion and cross-packet noncancellation; packet-2 adjacent-inward endpoint divergence; and the matching all-shell upper bound is FALSE for the frozen placement. FINITE: the bounded primary-source screen yields only a non-hit dated 2026-09-03 and does not prove novelty, priority, correctness, nonexistence, or publishability. OPEN: critical equality, fixed deletion, whole-shell and time occupation, positive variation, accumulated viscosity, payment normalization, arbitrary-clock extraction, scale contraction, general suitable weak solutions, regularity, and singularity. The four-panel figure is an analytic schematic of derived values, not PDE data or DNS.",
  "R0.74W Step 22 bounded literature screen and claim boundary",
  "R0.74W Step 22 public boundary",
  "Step 20 proves the two-sided scale of the certified geometric corridor for the canonical lobe; the completed-clock K-superlevel receives only a lower measure bound.",
  "Step 21 establishes exact completion and splitting, lifted-multiplicity coarse budgets, conditional algebra, and failure conditions.",
  "Step 22 proves an all-winding conditional-bridge threshold in the frozen exact common-shear family; packet 2 yields weighted endpoint divergence and disproves the matching all-shell upper bound for that placement. Fixed deletion remains OPEN.",
  "225 public research notes; latest node R0.74W.",
  "Research-note master index · v2.01 · 2026-09-03",
  "Remote adjacent-inward common-shear threshold and weighted endpoint obstruction",
  "Latest node R0.74W · continuously revised",
  "166 / Full text",
  "167 / Full text",
  "168 / Full text",
  "169 / Full text",
  "170 / Full text",
  "171 / Full text",
  "172 / Full text",
  "173 / Full text",
  "174 / Full text",
  "175 / Full text",
  "converts the R0.74U reserve into survival across the entire slab, hence",
  "Within the frozen two-packet exact smooth common-shear family, this section completes R0.74V's first remote endpoint comparison. The conclusion is a survival and sweeping scale dichotomy relative to the free derivative-heat comparator; it is neither an absolute small-error replacement nor a conclusion for arbitrary suitable weak solutions.",
  "This section establishes the remote adjacent-inward relative comparison only for one frozen exact smooth common-shear family and derives a frozen-placement all-shell upper obstruction from packet 2.",
  "This site stops at R0.74W Step 22. The current conclusion disproves only the matching all-shell upper bound for the frozen placement; the sole divergent coordinate may be removed by fixed deletion. Uncommitted R0.74X and R0.74Y were neither read nor published, and later work enters the publication chain only after an independent frozen handoff.",
  "Frozen family and explicit remote strip",
  "Opposite outcomes for the two packets on the frozen scale",
  "Frozen handoff",
  "The frozen four-panel figure shows derived analytic values only: Panel A is a physical-shell schematic; Panel B shows the threshold; Panel C is the exact all-winding bridge proof map; and Panel D shows the leading analytic endpoint factor. It contains no sampled paths, PDE data, DNS, or finite-scale numerical lower certificate.",
  "For the direct positive packet, the time-reversed Feynman--Kac representation retains every vertical winding:",
  "For the outer packet,",
  "The reverse high-probability lower bound comes from the same short-time layer; for sufficiently small fixed positive epsilon,",
  "Conversely, suppose the heat ages converge and",
  "gives packet 1 swept and packet 2 surviving:",
  "Weighted endpoint divergence and the fixed-deletion boundary",
  "Conclusion first: a strict threshold, not a direct reuse of the near-lobe estimate",
  "Exact all-winding conditional-bridge representation",
  "Together with the periodic-copy reserve, these bounds give",
  "Let the nonnegative saturation deficit be defined as follows. Upper and lower periodic Gaussian bounds at the remote height and heat age give the same exponent:",
  "Let the horizontal coordinate and displaced vertical coordinate be defined on the strip. The free comparator is",
  "The four panels encode only analytic geometry, exact thresholds, proof dependencies, and a derived leading scale; there are no sampled trajectories, PDE data, DNS, or finite-scale numerical certificates. ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NOT CLAY.",
  "Four-panel figure, certificates, and literature boundary",
  "In particular, the sufficient condition for survival uniformly across the slab is",
  "Stopping line and open questions",
  "Synchronized reader PDF",
  "The physical first component is",
  "The adjacent inward shell weight satisfies",
  "The corresponding free comparator is",
  "Retain",
  "Research note R0.74W · Step 22 · strictly frozen family",
  "with central-bridge probability tending to one at the displayed super-exponential rate. No monotonicity of the frozen saturation profile is assumed here.",
  "together with the frozen lower scale and chart condition. At the recentering time define",
  "Therefore the matching all-shell upper bound is FALSE for this frozen placement. But the sole divergent coordinate can be removed by a one-shell fixed deletion, so no fixed-deletion obstruction, whole-shell upper bound, time-occupation theorem, accumulated-viscosity bound, or target-coordinate duration theorem has been proved.",
  "The comparison must therefore be divided by the complete winding sum. Noncentral mass is not deleted; it obeys",
  "In central conditional-bridge probability, with the packet time in the closed heat-age slab,",
  "then the direct packet divided by its free comparator tends to zero; the sufficient condition uniform across the slab is",
  "then on the remote strip",
  "The narrow band between the two uniform endpoint thresholds must not be called wholly unclassified: for fixed limiting heat age, strict comparison with the curved threshold still decides the side. Only equality and its critical law remain OPEN.",
  "This is not a solution of the Navier--Stokes Millennium problem and does not claim a counterexample for general solutions.",
  "This is a logarithmic asymptotic in probability, not a deterministic prefactor asymptotic. The displacement deficit uses the packet age, whereas the free heat comparator uses the total age; they must not be confused.",
  "This is an amplitude-weighted relative noncancellation statement, not an unweighted absolute small-error claim.",
  "Direct geometry gives",
  "The exponent difference localizes the integral to a short-time layer, hence",
  "Status · R0.74W STEP 22",
  "The semigroup identity for the central bridge is",
  "The exact all-winding conditional bridge gives the relative survival and sweeping threshold on the remote strip.",
  "F / Frozen journal-scale four-panel figure",
  "Fixed deletion and whole-shell occupation remain open interfaces",
  "The inner packet has no uniform outcome under the generalized frozen assumptions. On the original scale, the exact margins are",
  "The inversion partner and cross-packet terms must be compared after inserting the actual amplitudes. The frozen exact margins are",
  "Noncancellation after inversion, the other packet, and amplitudes",
  "Literature: the bounded primary-source screen dated 2026-09-03 yields only a finite non-hit and proves no novelty, priority, correctness, nonexistence, or publishability.",
  "NEXT / Awaiting an independent frozen handoff",
  "OPEN: the critical equality law; fixed deletion; whole-shell occupation; time occupation; the positive-variation upper bound; accumulated viscosity; payment normalization; arbitrary-clock extraction; scale contraction; general suitable weak solutions; regularity; and singularity.",
  "Packet 2's relative survival, the remote-strip volume, and the nonnegative endpoint row of the completed clock combine to give",
  "Packet 2 forces adjacent-inward weighted endpoint divergence and disproves the matching all-shell upper bound for the frozen placement; fixed deletion may still remove the sole divergent coordinate and remains OPEN. NOT CLAY.",
  "PROVED: exact all-winding disintegration; the central-bridge logarithmic rate; relative survival and sweeping on the strict sides of the threshold; amplitude-weighted inversion and cross-packet noncancellation; and packet-2 weighted endpoint divergence.",
  "Python: 33/33 checks and 33 exact cases; independent Ruby: 6/6 groups and 56 assertions; Python and Ruby rejected 23/23 and 24/24 mutations; the figure archive has 25 files and 3,774,363 bytes with an 18/18 deterministic comparison. The certificate covers finite exact arithmetic and structure, while the literature audit is only a bounded non-hit; neither replaces a continuum PDE proof.",
  "Relative survival, the uniform slab, and sweeping",
  "Remote adjacent-inward threshold and weighted endpoint obstruction",
  "Remote saturation deficit and the short-time layer",
  "Seeds 0, 1, and 42 and independent regeneration are byte-identical;",
  "Step 22 main text",
  "Step 22 main text, primary and literature audits, two independent certificate implementations, and the figure archive",
];

assert.equal(summaries.length, 110, "R0.74W Step 22 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.74W Step 22 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.74W Step 22 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.74W Step 22 source-string count drift");
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
  release: "R0.74W Step 22",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
