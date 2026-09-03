#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074xstep23";

// Local direct translations in deterministic collectSiteStrings order.
const summaries = [
  "102 sections fully archived",
  "Master index of 226 research notes",
  "View the R0.74X card on the home page",
  "The actual payment-normalized gate counterexample, whole-shell clock, and accumulated dissipation are not proved. Later work requires an independent freeze; R0.74Y, R0.74Z, and unlisted work are neither read nor published.",
  "Current endpoint R0.74X Step 23",
  "Jump to the R0.74X card on the home page →",
  "Research note R0.74X Step 23 · 2026-09-03",
  "Read the latest R0.74X research note →",
  "Expand 136 public notes",
  "Review v2.02 · 2026-09-03",
  "The exact three-packet family proves endpoint divergence relative to T* in two distinct coordinates; fixed deletion may use different witness times. The larger outer cubic-payment exponent makes both W-strip witnesses vanish under the actual normalization, so the actual counterexample is NOT PROVED and the equal-target route is NO-GO. NOT CLAY.",
  "The cumulative recap after R0.60 contains 161 nodes; the site now has 226 public research notes",
  "R0.70A-R0.74X · 128 sections published",
  "R0.70A-R0.74X: 128 sections published, 102 fully archived",
  "R0.74X Step 23 proves a two-coordinate endpoint obstruction relative to T* in a frozen exact three-packet family; fixed deletion may use different witness times. But the outer cubic payment strictly dominates both audited strip rates, so the actual normalized counterexample is NOT PROVED and X.52 remains OPEN.",
  "R0.74X: two-coordinate T* obstruction and cubic-payment no-go",
  "R0.74X｜Three-packet fixed-deletion endpoint obstruction and cubic-payment gate",
  "Step 23 frozen four-panel figure",
  "The exact three-packet family yields a two-coordinate T*-normalized endpoint obstruction, with different witness times allowed by the fixed-set deletion quantifier. The actual payment-normalized counterexample is NOT PROVED, and the equal-target W-strip route is NO-GO BY CUBIC PAYMENT. NOT CLAY.",
  "The frozen audit screened exact Navier--Stokes shearing waves, pathwise and large-deviation analysis for passive scalars in shear flows, local kinetic-energy regularity criteria, and localized Navier--Stokes inequality constructions. It found no exact collision with the five-part conjunction. This is only a finite primary-source non-hit dated 2026-09-03, not evidence of novelty, priority, correctness, nonexistence, or publishability.",
  "Literature review v2.02 · 2026-09-03",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P-R0.74X work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "The actual normalized fixed-deletion counterexample, whole-shell clock, and accumulated dissipation remain OPEN; R0.74Y, R0.74Z, and unlisted work are neither read nor published.",
  "PROVED (frozen exact family only): an exact smooth three-packet NSE family; relative survival of packets 2 and 3; two distinct T*-normalized endpoint divergences; fixed-set different-time pigeonhole; and negligibility of the two audited strip integrals relative to the actual normalization. FINITE: bounded primary-source screen only. NOT PROVED: the actual payment-normalized fixed-deletion counterexample, whole-shell clock bounds, and accumulated-dissipation enhancement. NO-GO: the equal-target W-strip route because of exterior cubic payment. OPEN: payment-compatible construction X.52, positive variation, accumulated viscosity, arbitrary-clock extraction, scale contraction, general suitable weak solutions, regularity, and singularity. The four-panel figure is an analytic schematic of derived values, not PDE data or DNS.",
  "R0.74X Step 23 bounded literature screen and claim boundary",
  "R0.74X Step 23 public boundary",
  "Step 23 uses an exact three-packet family to prove endpoint obstruction relative to T* in two distinct coordinates; fixed deletion may use different witness times. The actual payment-normalized counterexample is NOT PROVED, and cubic payment blocks the equal-target W-strip route.",
  "226 public research notes; latest node R0.74X.",
  "Three-packet fixed-deletion endpoint obstruction and cubic-payment gate",
  "Research-note master index · v2.02 · 2026-09-03",
  "Latest node R0.74X · continuously revised",
  "The witness times may differ; simultaneity is not required. Setting them equal optionally gives a simultaneous vector-height statement at one smooth time. The pigeonhole argument fails if the deletion set is incorrectly allowed to depend on time.",
  "176 / Full text",
  "177 / Full text",
  "178 / Full text",
  "179 / Full text",
  "180 / Full text",
  "181 / Full text",
  "182 / Full text",
  "183 / Full text",
  "184 / Full text",
  "185 / Full text",
  "This section exactly rules out the equal-target three-packet W-strip architecture: both endpoints diverge relative to T*, but the outer packet's cubic payment has a larger exponent, so these witnesses cannot refute the actual normalized gate.",
  "This section concerns only one frozen exact smooth periodic three-packet common-shear family. It extends R0.74W's one divergent coordinate to two distinct divergent coordinates, then proves that the two audited W-strip witnesses still cannot defeat the actual cubic-payment normalization.",
  "This site stops at R0.74X Step 23. It proves only the two-coordinate endpoint obstruction relative to T* and that cubic payment blocks the equal-target W-strip route; the actual payment-normalized fixed-deletion counterexample, whole-shell clock, and accumulated dissipation are not proved. R0.74Y, R0.74Z, and unlisted work were neither read nor published.",
  "and evolves three inversion-paired derivative-heat packets under the same heat-evolved shear",
  "But the outer cubic payment has a strictly larger exponent: the actual payment-normalized counterexample is NOT PROVED, and the equal-target W-strip route is NO-GO. NOT CLAY.",
  "Frozen four-panel figure, certificates, and bounded literature screen",
  "For packets 2 and 3, use the adjacent-inward strip from R0.74W",
  "Their strict gap is",
  "The common amplitude cancels exactly in this ratio and cannot repair it.",
  "Conclusion first: the two-coordinate endpoint obstruction is proved; the actual-gate counterexample is not",
  "T-star endpoint divergence in two distinct coordinates",
  "Taking the time domain to be the completed set gives",
  "Exact three-packet family and common normalization",
  "Amplitude-weighted target-lobe dominance for all three packets and the nonnegative exterior velocity-cubic row force",
  "Three exact common-shear packets give endpoint divergence relative to T* in two distinct coordinates; the deletion set is fixed first, while witness times may differ.",
  "The deletion set must be fixed before taking the time supremum. Whichever coordinate is deleted, the other witness can be selected at its own time",
  "The actual budget-one deletion functional is",
  "The four panels encode only the analytic scale index, fixed-deletion quantifier, derived exponent comparison, and claim hierarchy; there are no sampled trajectories, PDE data, DNS, or simulation. ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NOT CLAY.",
  "The four-panel figure encodes only the analytic scale index, different-time fixed-deletion pigeonhole, exact exponent comparison, and claim hierarchy; it contains no sampled trajectories, PDE data, DNS, or simulation.",
  "Stopping line and open boundaries",
  "The next construction target must directly satisfy",
  "Project terms such as fixed deletion, common-shear packet, simultaneous height, and remote adjacent-inward must not be presented as standard literature terminology.",
  "Write the logarithmic radius rate in L1 units. The U-reserve bounds it, so the payment lower rate is",
  "Research note R0.74X · Step 23 · strictly frozen family",
  "Therefore packets 2 and 3 both survive relatively on the full closed slab. After inserting the actual amplitudes, the four positive cross margins are",
  "Therefore, for the two actual strip integrals",
  "Because each packet's adjacent-inward shell is the preceding coordinate, this gives two distinct coordinates",
  "This is not a whole-shell clock upper or lower theorem, does not control accumulated dissipation, and says nothing about arbitrary suitable weak solutions, regularity, or singularity.",
  "This is X.52. It does not require equal witness times, but it must decouple two undeletable clock heights from the outer exterior cubic payment. Any change to amplitude law, shell placement, weight interaction, or packet geometry requires a new exact normalization, survival proof, and all-cross-packet audit.",
  "This is an exact smooth periodic unforced Navier--Stokes solution. Equal target-clock normalization is not equal raw-energy normalization; changing the common amplitude cannot repair the payment ratio below.",
  "These are explicit strip lower witnesses. They provide no whole-shell upper bound.",
  "This is only a two-strip upper comparison, not a whole-shell clock upper bound; it does not exclude an unproved whole-shell or accumulated-dissipation effect.",
  "The inequality that actually must be tested is not an O(T*) bound but",
  "Status · R0.74X STEP 23",
  "The largest audited W-strip exponent is",
  "The actual gate uses cubic-payment normalization",
  "The adjacent-shell weight, strip volume, free kernel, and common T* normalization give",
  "Fixed-deletion quantifier order: the witness times may differ",
  "The inversion margin is positive and so is the noncentral winding reserve. Thus inversion partners, adjacent and nonadjacent cross packets, and all periodic windings are controlled in amplitude-weighted comparisons; there is no diagonal-only assumption.",
  "NO-GO: outer exterior velocity-cubic payment blocks the equal-target W-strip route.",
  "OPEN: payment-compatible two-coordinate construction X.52; positive-variation upper bound; accumulated viscosity; arbitrary-clock extraction; scale contraction; general suitable weak solutions; regularity; and singularity.",
  "The outermost chart condition and inherited U-reserve give",
  "Packet 3's target lobe at payment radius 2R satisfies",
  "The payment rate strictly dominates both audited W-strip rates",
  "Payment-compatible two-coordinate construction X.52 remains OPEN",
  "Precise no-go and next proposition X.52",
  "PROVED: a frozen exact smooth three-packet NSE family; relative survival of packets 2 and 3; two distinct T*-normalized endpoint divergences; the fixed-set different-time pigeonhole; divergence of the budget-one endpoint functional relative to T*; and negligibility of the two audited strip integrals relative to actual cubic payment.",
  "Python: 31/31 checks and 231 exact cases or assertions; independent Ruby: 5/5 groups and 36 assertions; Python and Ruby rejected 24/24 and 25/25 mutations; the figure archive has 25 files and 3,096,940 bytes with an 18/18 deterministic comparison. The certificates cover finite exact arithmetic and structure, while the literature audit is only a bounded non-hit; neither replaces a continuum PDE proof.",
  "Remote strips, relative survival, and complete cross audit",
  "Step 23 main text",
  "Step 23 main text, primary and literature audits, two certificate implementations, and the figure archive",
];

assert.equal(summaries.length, 93, "R0.74X Step 23 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.74X Step 23 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.74X Step 23 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.74X Step 23 source-string count drift");
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
  release: "R0.74X Step 23",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
