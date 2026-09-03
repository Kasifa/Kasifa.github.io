#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074zstep25";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "103 sections fully archived",
  "Master index of 228 research notes",
  "The next step must cover critical or shorter temporal concentration, arbitrary ill-conditioned finite cancellations, and the complete clock/payment ledger. R0.75A, R0.75B, and unlisted work are neither read nor published.",
  "View the R0.74Z card on the home page",
  "Current endpoint R0.74Z Step 25 persistence gate",
  "Jump to the R0.74Z card on the home page →",
  "Research note R0.74Z Step 25 · 2026-09-03 · PERSISTENCE GATE",
  "Read the latest R0.74Z research note →",
  "Expand 138 public notes",
  "Review v2.04 · 2026-09-03",
  "A persistent remote kinetic floor on a theta_L R^3 tube pays a cubic row through the exact two-step weights and Holder coercivity. The strict subcritical residence route is blocked. Endpoint-to-tube persistence holds only under the time-tame and moving-strip assumptions; the critical and full-clock branches remain OPEN. NOT CLAY.",
  "A persistent remote kinetic floor forces its own cubic payment in the doubled-radius exterior row. Exact coercivity closes the strict subcritical residence route. The time-tame endpoint upgrade is conditional, while the critical layer, arbitrary ill-conditioned families, and full-clock Y.57 remain OPEN. NOT CLAY.",
  "The cumulative recap after R0.60 contains 161 nodes; the site now has 228 public research notes",
  "R0.70A-R0.74Z · 130 sections published",
  "R0.70A-R0.74Z: 130 sections published, 103 fully archived",
  "R0.74Z Step 25 proves exact kinetic coercivity for a persistent remote tube and blocks W-kinetic payment escape at a strict subcritical residence rate. Endpoint-to-tube persistence is conditional on time-tameness and moving-strip all-winding uniformity; the critical layer, accumulated clock rows, and full-clock Y.57 remain OPEN.",
  "R0.74Z: remote persistence gate and full-clock open boundary",
  "R0.74Z｜Remote persistence gate: kinetic coercivity, the time-tame condition, and the open full-clock boundary",
  "Step 25 frozen four-panel figure",
  "The next step must control critical temporal concentration, ill-conditioned finite cancellation, and the complete ledger. R0.75A, R0.75B, and unlisted work are neither read nor published.",
  "The frozen audit conducted a bounded primary-source screen covering heat observability, propagation of smallness, small-time control cost, spectral vanishing, and Remez inequalities for exponential polynomials. It found no exact collision with the six-part common-shear, shrinking-strip, weighted cubic-payment, full-clock conjunction. This finite non-hit dated 2026-09-03 is not evidence of novelty, priority, nonexistence, correctness, or publishability.",
  "Literature review v2.04 · 2026-09-03",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P-R0.74Z work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "PROVED: finite same-b exact NSE closure; the remote clock Gamma^(1/4) and doubled-radius payment Gamma^(1/16); total-field Holder coercivity on a persistent remote tube; and the strict limsup kappa_L<kappa_* W-kinetic no-go. CONDITIONAL: endpoint preservation plus the moving-frame envelope and moving-strip all-winding uniformity implies R^3 persistence; the complexity rate is necessary only. OPEN: the critical layer, endpoint-only and arbitrary exponentially ill-conditioned families, accumulated clock rows, full-clock Y.57, the complete payment upper, the whole shell, fixed deletion, regularity, and singularity. The four-panel figure is an analytic schematic of derived values, not PDE data or DNS.",
  "R0.74Z Step 25 bounded literature screen and claim boundary",
  "R0.74Z Step 25 public boundary",
  "Step 22 proves an all-winding conditional-bridge threshold in a frozen exact common-shear family; fixed deletion remains OPEN.",
  "Step 23 proves a two-coordinate T* endpoint obstruction; the actual normalized counterexample is NOT PROVED.",
  "Step 24 proves the frozen same-packet self-payment no-go; the changed geometry has only a formal window.",
  "Step 25 proves exact kinetic coercivity and a strict subcritical threshold for a persistent remote tube. Endpoint-to-tube persistence is conditional, while the critical layer, accumulated rows, and full-clock Y.57 remain OPEN.",
  "228 public research notes; latest node R0.74Z.",
  "Research-note master index · v2.04 · 2026-09-03",
  "Remote persistence gate: kinetic coercivity, the time-tame condition, and the open full-clock boundary",
  "Latest node R0.74Z · continuously revised",
  "This is not a sufficient construction, and equality remains open. Fixed M, polynomial M, and polynomial Hermite order are excluded only when the total conditioning and derivative envelope are also subexponential. Backward heat amplification makes extremely narrow packets costly for isolated modes, but arbitrary cancelling finite sums still require a spectral or observability estimate.",
  "The second step is the exact payment theorem. Z.22 alone must not be presented as an unconditional persistence theorem.",
  "No payment-compatible cancellation cell is constructed; a finite literature non-hit is not novelty evidence. ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NO NOVELTY CLAIM | LOCAL DIRECT TRANSLATION | NO DGX | NOT CLAY.",
  "The critical layer, endpoint-only branch, arbitrary exponentially ill-conditioned finite family, accumulated clock rows, full-clock Y.57, complete payment upper, whole-shell estimates, fixed deletion, general suitable weak solutions, regularity, and singularity remain OPEN or NOT CERTIFIED.",
  "Endpoint preservation plus Z.22 and moving-strip all-winding uniformity implies R^3 persistence; the complexity lower rate applies only within that model.",
  "Finite same-b inversion-paired superposition has exact NSE closure; the two fourth-root weight shifts, persistent-remote-tube Holder coercivity, and the strict limsup no-go for the W-kinetic route are PROVED.",
  "Polynomial and o(L^2) factors may determine the sign.",
  "← Step 24: frozen self-payment no-go and formal window",
  "196 / Full text",
  "197 / Full text",
  "198 / Full text",
  "199 / Full text",
  "200 / Full text",
  "201 / Full text",
  "202 / Full text",
  "203 / Full text",
  "204 / Full text",
  "205 / Full text",
  "This section does not solve the Navier--Stokes Millennium problem or claim a counterexample among general solutions.",
  "This site stops at R0.74Z Step 25. The next step must control critical or shorter temporal concentration, arbitrary ill-conditioned finite cancellations, and the complete clock/payment ledger. The endpoint critical layer, full Y.57, the whole shell, fixed deletion, regularity, and singularity remain unproved. R0.75A, R0.75B, and unlisted work were neither read nor published.",
  "and the exact reserve is",
  "The exact algebra does not permit arbitrary vertical or temporal translation of an already evolved packet:",
  "Its remote ratio nevertheless has logarithmic slope -Theta(L), so it changes by e^{Theta(L)} across a fixed-width strip and cannot give uniform 1+o(1) restoration. Even if only one point is restored, an ordinary R-width packet persists on an R^3 interval and triggers tube coercivity.",
  "Every such persistence sequence is strictly excluded as a W-kinetic payment escape. The equality layer remains OPEN",
  "Any real linear combination remains a solution of the same passive equation. Combined with the primary field, the displayed velocity is an exact smooth periodic mean-zero unforced Navier--Stokes solution with zero pressure; negative coefficients are allowed.",
  "The first step depends on the displayed envelope, endpoint condition, and moving-strip all-winding uniformity and is a",
  "Define the moving derivative",
  "Publication stopping line",
  "This lower bound uses the total field rather than an individual summand, so it already includes interference among primaries, correctors, inversion partners, and all periodic copies.",
  "More centers or higher finite differences can flatten more derivatives, but they do not yield a uniform no-go when family size, coefficient condition number, and separations may depend arbitrarily on R. Fixed or coefficient-tame subexponential families satisfying the time-tame envelope fall under the conditional obstruction; an arbitrary exponentially ill-conditioned finite network remains open. Qualitative analyticity also cannot propagate exponentially small target values without a frequency or global-norm bound.",
  "An identical negative copy cancels the primary on both the target and the remote strip, destroying the required second coordinate. A displaced restoring Gaussian can interpolate two selected points, with target suppression rate",
  "Conclusion first: a persistent tube pays, while endpoint-only persistence is not closed",
  "Two fourth-root weight shifts and tube coercivity",
  "Let N_L denote the normalized time-derivative and conditioning factor in Z.22. The residence rate guaranteed by endpoint preservation formally satisfies",
  "No payment-compatible cell is constructed, and there is no whole-shell, regularity, or singularity result.",
  "If the total corrector satisfies the time-tame envelope on a fixed normalized remote neighborhood",
  "Suppose Omega(t) lies in the adjacent-inward annulus, obeys the stated volume bound, and has the displayed weighted kinetic floor for t in an interval of length theta_L R^3",
  "If a remote weighted kinetic floor h persists on a spacetime tube of length theta_L R^3, it forces its own exterior cubic payment. A persistence sequence strictly below the critical rate cannot form a W-kinetic payment escape. If the remote field is preserved only at the endpoint, smoothness gives some persistence interval but not a uniform R^3 residence interval; the critical and shorter-time branches remain open.",
  "The four panels encode only the exact weight ladder, derived threshold, conditional implication, and proved/conditional/open hierarchy. ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NO NOVELTY CLAIM | NOT CLAY.",
  "The four-panel figure encodes the exact weight ladder, strict persistence threshold, conditional time-tame route, and full-clock claim hierarchy. It is an analytic schematic of derived values, not a PDE simulation, DNS, sampled trajectory, or empirical fit.",
  "Under one odd shear b, any finite collection of smooth periodic solutions and their inversion partners",
  "At doubled radius the same physical annulus satisfies",
  "The next proposition Z.39 is a cancellation-robust remote endpoint persistence/payment dichotomy. Either the field persists on a tube at a rate strictly below kappa_* and is closed here, or critical or shorter concentration must pay in the complete Version-M ledger. The second branch, the critical layer, the full completed clock, and arbitrary ill-conditioned finite families all remain open.",
  "The strict subcritical persistence route is blocked; endpoint-to-tube persistence holds only under the time-tame and moving-strip all-winding assumptions. The critical layer, accumulated rows, and full-clock Y.57 remain OPEN. NOT CLAY.",
  "Research note R0.74Z · Step 25 · persistence gate",
  "Vertical centers, time offsets, and Hermite cells must therefore be re-evolved from initial data under the actual b(t,x3); periodic windings cannot be silently removed.",
  "Therefore every sequence satisfying",
  "What is proved is that at a strict subcritical residence rate, a time-tame corrector cannot turn the persistent W-type remote kinetic strip witness alone into a clock-over-payment counterexample. It is not proved that every time-tame cell fails the complete Y.57 ratio.",
  "Within this derivative and conditioning model, avoiding the strict subcritical persistence no-go requires at least",
  "Spatial Holder and the nonnegative exterior velocity row then give the exact deterministic coercivity",
  "This is the second fourth-root shift; Gamma^(1/4) cannot be reused as the doubled-radius payment weight.",
  "Status · R0.74Z STEP 25",
  "Certificate, literature, and frozen four-panel figure",
  "The critical and full-clock dichotomy remains to be proved →",
  "If endpoint preservation also holds on a slightly enlarged remote strip and the W comparison is uniform for the moving strip, all windings, and O(R) center or heat-age perturbations, the endpoint field persists for an R^3 tube. Combined with exact coercivity, this blocks the W-kinetic route.",
  "Necessary complexity for endpoint-focused escape",
  "Exact common-shear algebra and forbidden translations",
  "Figure archive: 25 files and 3,032,354 bytes; 18/18 deterministic rerender; SVG, PNG, PDF, and greyscale QA PASS;",
  "Boundaries for Gaussian, multi-center, and Hermite cells",
  "Literature: the bounded primary-source screen dated 2026-09-03 found only a finite non-hit; it does not establish novelty, priority, nonexistence, correctness, or publishability.",
  "NEXT / R0.75A awaiting a frozen package",
  "The outer packet's adjacent-inward shell is k=k2-1. Write",
  "Python: 10/10 checks; independent Ruby: 11/11 assertions; the Python and Ruby implementations reject 22/22 and 23/23 mutations; seeds 0/1/42 are byte-identical. The 25-file, 3,032,354-byte figure archive rerenders deterministically 18/18, and both the certificates and figure preserve the critical, full-clock, and novelty boundaries.",
  "The frozen rational parameters from R0.74Y give",
  "R0.74Y leaves the task of cancelling the field exponentially on the outer target spacetime box while retaining the same packet's adjacent-inward remote tail as a second clock coordinate. R0.74Z gives two levels of conclusions for this cancellation-cell continuation.",
  "The remote free comparator has field scale",
  "If the remote kinetic floor persists on a theta_L R^3 spacetime tube, the exact two-step fourth-root weights and Holder coercivity force it to pay its own cubic row.",
  "Step 25 main text",
  "Step 25 main text, primary and literature audits, two certificate implementations, and figure archive",
  "Strict persistence threshold and the critical layer",
  "The time-tame endpoint-to-tube route is conditional",
  "Tube coercivity compares payment with the kinetic floor h on the chosen region. The endpoint clock is only known to be at least h; it is not proved to be at most e^{o(L^2)}h. The accumulated ordinary-viscosity row may be larger than h. Closing it requires proving that this row also forces comparable central-energy or exterior payment.",
  "The W-kinetic result cannot be promoted to full-clock Y.57",
  "Z.39 remote persistence/payment dichotomy remains OPEN",
];

assert.equal(summaries.length, 108, "R0.74Z Step 25 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.74Z Step 25 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.74Z Step 25 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.74Z Step 25 source-string count drift");
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
  release: "R0.74Z Step 25",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
