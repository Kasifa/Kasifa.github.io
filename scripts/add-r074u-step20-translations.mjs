#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074ustep20";

// Local direct translations in deterministic collectSiteStrings order.
const summaries = [
  "100 sections fully archived", // 001
  "Master index of 223 research notes", // 002
  "The packet-centre speed and physical-annulus room certify a two-sided geometric corridor. This closes the exponentially short-residence escape in the frozen common-shear architecture. The completed-clock K-superlevel receives only a lower measure bound; its upper measure remains OPEN. NOT CLAY.", // 003
  "View the R0.74U card on the home page", // 004
  "Current endpoint R0.74U Step 20", // 005
  "Await the next explicit frozen package in this publication task. It may study off-target endpoint rows, viscous accumulation, cross terms, and the shear baseline. The certified-corridor upper bound must not be extrapolated to a full K-superlevel upper bound.", // 006
  "Jump to the R0.74U card on the home page →", // 007
  "Research note R0.74U Step 20 · 2026-09-03", // 008
  "Read the latest R0.74U research note →", // 009
  "Expand 133 public notes", // 010
  "Review v1.99 · 2026-09-03", // 011
  "Intrinsic motion certifies a two-sided geometric corridor and conflicts with the exponentially short dwell required by bounded payment. The completed-clock K-superlevel receives only a lower bound; the geometric-corridor upper bound is not transferred. NOT CLAY.", // 012
  "The cumulative recap after R0.60 contains 161 nodes; the site now has 223 public research notes", // 013
  "R0.70A–R0.74U · 125 sections published", // 014
  "R0.70A–R0.74U: 125 sections published, 100 fully archived", // 015
  "R0.74U Step 20 proves that the certified geometric corridor of the canonical common-shear lobe has the stated scale and closes the exponentially short-residence escape in the frozen architecture. The full K-superlevel still has only a lower bound; its upper measure, arbitrary-clock extraction, Q.12, Q.1, and regularity remain OPEN.", // 016
  "R0.74U: intrinsic certified residence and the full K-superlevel boundary", // 017
  "R0.74U｜Intrinsic motion certifies the residence scale and closes the exponentially short-residence escape", // 018
  "Step 20 journal-grade four-panel figure", // 019
  "Step 20 proves that intrinsic centre motion and physical-annulus room force a two-sided certified corridor. The corridor is only included from below in the completed-clock K-superlevel; its upper measure and arbitrary-clock extraction remain OPEN.", // 020
  "Possible topics are off-target endpoint rows, viscous accumulation, cross terms, and the shear baseline. The certified geometric-corridor upper bound must not be promoted to a full K-superlevel upper bound.", // 021
  "This is an important terminology-level near collision: the low phase-drift set of coherent same-scale Fourier–helical triads receives an upper residence-time estimate, whereas R0.74U tracks a canonical packet lobe in a physical-space annulus and transfers only a lower bound to the completed-clock K-superlevel. The state variables, shells, assumptions, and inequality directions differ, so the results are not interchangeable.", // 022
  "Literature review v1.99 · 2026-09-03", // 023
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.74U work only as research notes. I do not extrapolate computations or notes into a regularity theorem.", // 024
  "The bounded primary-source screen found no source combining the exact unforced common-shear solution, centre speed, physical-annulus room, certified corridor, total-field K-superlevel lower inclusion, and cubic-payment conflict. This non-hit is not a novelty, priority, correctness, nonexistence, or publishability claim.", // 025
  "Intrinsic certified residence and the lower-only K-superlevel boundary", // 026
  "PROVED: the two-sided certified geometric corridor in U.21–U.25; the total-field lobe floor in U.33; the lower-only K-superlevel statement in U.34–U.35; the certified-dwell conflict in U.36–U.41; and the explicit-phase lower constants in U.45. FINITE: 31/31 Python checks and 869 cases; 9/9 Ruby groups and 1,651 assertions; all mutation, reproducibility, and figure QA checks passed. OPEN: the full K-superlevel upper measure, full completed-clock upper ledger, arbitrary-clock extraction, high-Rayleigh and anomalous-defect routes, fixed deletion, direct hybrid, Q.12, Q.1, scale contraction, regularity, and singularity. The figure is an analytic schematic with derived analytic values, not PDE data or DNS.", // 027
  "R0.74U Step 20 literature near collision and claim boundary", // 028
  "R0.74U Step 20 public boundary", // 029
  "Step 20 proves a two-sided certified geometric corridor for the canonical lobe and a conflict with the exponentially short dwell required by bounded payment. The corridor is only included from below in the completed-clock K-superlevel; the complete superlevel has no converse or upper measure bound.", // 030
  "223 public research notes; latest node R0.74U.", // 031
  "Intrinsic motion certifies the residence scale and closes the exponentially short-residence escape", // 032
  "Research-note master index · v1.99 · 2026-09-03", // 033
  "Latest node R0.74U · continuously revised", // 034
  "146 / Full text", // 035
  "147 / Full text", // 036
  "148 / Full text", // 037
  "149 / Full text", // 038
  "150 / Full text", // 039
  "151 / Full text", // 040
  "152 / Full text", // 041
  "153 / Full text", // 042
  "154 / Full text", // 043
  "155 / Full text", // 044
  "The packet centre's speed and the physical annulus's room certify a two-sided geometric residence corridor.", // 045
  "Main conclusion: distinguish the two time sets first", // 046
  "This site stops at R0.74U Step 20. A later frozen package may study off-target endpoint rows, viscous accumulation, cross terms, the shear baseline, and arbitrary-clock lobe extraction. This section's certified geometric-corridor upper bound must not be presented as a complete K-superlevel upper bound or as a theorem on regularity, singularity, or Clay.", // 047
  "From the total-field lobe floor to the completed clock: lower inclusion only", // 048
  "Define the full preimage of the explicit sufficient condition", // 049
  "The frozen Python certificate passes 31/31 checks and 869 exact finite cases; the independent Ruby audit passes 9/9 groups and 1,651 Rational assertions. The Python and Ruby mutation suites reject 23/23 and 24/24 deliberate errors, and Python hash seeds 0, 1, and 42 produce byte-identical output. The journal figure package passes 47/47 validation checks, has an 18/18 deterministic core, and binds its SVG, one-page PDF, and 600 dpi PNG to the frozen source.", // 050
  "Frozen architecture and the full terminal slab", // 051
  "For the frozen explicit phases, one-sided slab room improves the inner forward corridor and the outer one-sided corridor. These are improved lower constants for the certified geometric corridor and do not change the fact that only a lower bound is known for the complete K-superlevel.", // 052
  "The object remains one exact smooth periodic, mean-zero, unforced common-shear Navier–Stokes solution with zero pressure. Two inversion-paired derivative-heat packets share one shear coefficient. Track each packet centre on the terminal slab; platform calibration gives the strictly monotone speed interval", // 053
  "Let the outer packet's normalized certified dwell be", // 054
  "Two-sided scale of the certified geometric corridor", // 055
  "Certified residence enters the cubic payment", // 056
  "Still OPEN: an upper measure bound for the complete K-superlevel; the full completed-clock upper ledger including off-target endpoint rows, viscous accumulation, cross terms, and the shear baseline; arbitrary-clock lobe extraction; high-Rayleigh and anomalous-defect routes; fixed deletion; direct hybrid; Q.12; Q.1; scale contraction; regularity; and singularity formation. This is not a theorem for arbitrary suitable-weak solutions and not a Navier–Stokes counterexample.", // 057
  "Thus the certified corridor has the stated scale. The right-hand side bounds only this certified geometric corridor; it is neither maximal physical residence nor an upper bound for the complete K-superlevel.", // 058
  "It transfers only a one-way inclusion and a lower measure bound to the completed-clock K-superlevel. The geometric-corridor upper bound must never be rewritten as a complete K-superlevel upper bound. NOT CLAY.", // 059
  "Literature near collision and stopping line", // 060
  "Exact centre margin in the physical annulus", // 061
  "Explicit phases further improve the constants", // 062
  "Choose the moving lobe box with the stated exact volume. Its explicit centre margin is", // 063
  "Along the frozen scale relation, assume for contradiction that normalized payment remains bounded. The necessary condition from R0.74T would force", // 064
  "Research note R0.74U · Step 20 · complete Chinese edition", // 065
  "The bounded primary-source screen found no source stating the entire six-part frozen combination. This is only a bounded-search non-hit, not proof of novelty, priority, correctness, nonexistence, or publishability. The closest name collision is Inage's 2026 residence-time compression for coherent same-scale Fourier–helical triads: it gives a scale-decaying upper temporal estimate for a low phase-drift set. Here, a canonical packet lobe in a physical-space annulus receives a lower residence estimate, and only a lower bound transfers to the completed-clock superlevel. The objects, shells, assumptions, and inequality directions differ.", // 066
  "Finite certificates, figure package, and reproducibility boundary", // 067
  "At the frozen parameter threshold, the explicit margin lies between the stated constants. Therefore the entire lobe lies in the selected physical-space annulus and the cutoff equals one on it whenever the centre condition holds. This is a physical-space-shell statement, not a Fourier-frequency-shell statement and not an optimal characterization of all possible centre positions.", // 068
  "Inside the certified corridor, the direct packet, inversion partner, other packet, and periodic copies are compared in the total field, giving the lobe floor. The temporal and spatial cutoffs equal one on the lobe, while all remaining completed-clock terms are nonnegative, hence", // 069
  "This is not an unconditional upper bound on the actual corridor; it is a necessary upper bound implied by bounded payment. It is exponentially incompatible with the proved certified-dwell lower bound. Thus the exponentially short-dwell escape is closed in the frozen canonical common-shear architecture, with no extension to arbitrary shears, packets, or clocks.", // 070
  "The earlier shorter window is not silently enlarged. Packet survival, inversion suppression, cross-packet tails, and the periodic remainder on the full slab are separately checked from the frozen source's full-time inputs.", // 071
  "This uses spatial Hölder and restriction of a nonnegative integral to a measurable time set, both classical tools. The claim boundary concerns the combination of the frozen PDE architecture, physical lobe, total-field comparison, completed clock, and payment—not Hölder itself.", // 072
  "This is the page's central quantifier boundary: only corridor inclusion in the K-superlevel and a lower measure bound for the full K-superlevel are proved. Accumulated dissipation, off-target endpoint rows, another packet, or the common shear may keep K large after the lobe exits, so the inclusion cannot be reversed and the geometric-corridor upper bound cannot be transferred to K.", // 073
  "These results provide exact-arithmetic, kinematic, structural, dependency, and hash QA. The figure is an analytic schematic with derived analytic values, not PDE data or DNS. Finite computation does not replace a continuum PDE proof, and the figure seal does not certify mathematical correctness.", // 074
  "Why exponentially short residence conflicts", // 075
  "Centre room divided by speed has the stated time scale. Even when the zero lies at a slab endpoint, at least one side retains enough time. Exact slab truncation and monotone-preimage estimates give", // 076
  "Status · R0.74U STEP 20", // 077
  "The full K-superlevel upper ledger remains an open interface", // 078
  "Intrinsic certified residence and the bounded-payment conflict", // 079
  "Panels A–C distinguish the certified geometric corridor from the full K-superlevel; Panel D shows the derived analytic logarithmic conflict. ANALYTIC SCHEMATIC / DERIVED ANALYTIC VALUES / NOT PDE DATA / NOT DNS / NOT CLAY.", // 080
  "Python: 31/31 checks and 869 exact finite cases; independent Ruby: 9/9 groups and 1,651 Rational assertions. Python and Ruby reject 23/23 and 24/24 intentional mutations respectively; finite certificates do not replace the continuum PDE proof.", // 081
  "R0.74T's measurable-lobe Hölder coercivity applies to the entire certified corridor. Insert the lobe floor and the certified-residence lower bound to obtain", // 082
  "Step 20 proves one precise kinematic fact for the frozen canonical common-shear packet architecture: the packet centre crosses horizontally at the stated inverse-square speed scale, while the physical annulus provides the stated centre-room scale, so the explicit certified geometric corridor has the stated residence scale. This is a two-sided conclusion for the geometric corridor. The completed-clock superlevel may be larger; this section proves only inclusion and a lower measure bound for it, with no converse or upper measure bound.", // 083
  "Step 20 main text", // 084
  "Step 20 main text, audits, two independent certificate implementations, and QA", // 085
];

assert.equal(summaries.length, 85, "R0.74U Step 20 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.74U Step 20 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.74U Step 20 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.74U Step 20 source-string count drift");
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
  release: "R0.74U Step 20",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
