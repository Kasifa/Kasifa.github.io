#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075gstep32";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 235 research notes",
  "This must be proved using independent dynamics, residence time, resolvent, or payment-sensitive information. Later work was not authorized, read, or published.",
  "View the R0.75G card on the home page",
  "Current endpoint R0.75G Step 32 exact signed-flux gain threshold",
  "Jump to the R0.75G card on the home page →",
  "Research note R0.75G Step 32 · 2026-09-03 · EXACT SIGNED-FLUX GAIN THRESHOLD",
  "Read the latest R0.75G research note →",
  "Under the independent estimate X ≤ C R^alpha p_b^(1/3) p_F^(2/3), the exact sufficient threshold is alpha>27163/107163. R^(1/3) has a strictly negative margin; R^(1/4) only shows that this route does not close. The positive gain and E.24 remain OPEN. NO NOVELTY CLAIM. NOT CLAY.",
  "Expand 145 public notes",
  "Review v2.11 · 2026-09-03",
  "The exact threshold for the conditional estimate is alpha>27163/107163; R^(1/3) suffices, while R^(1/4) does not suffice for this route. Amplitude scaling cannot create a gain, and the residence exponent must satisfy beta>27163/35721. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 235 public research notes",
  "R0.70A–R0.75G · 137 sections published",
  "R0.70A–R0.75G: 137 sections published, 104 fully archived",
  "R0.75G Step 32 quantifies the independent gain needed for the remaining signed collar flux as the exact threshold alpha>27163/107163. R^(1/3) is conditionally sufficient, while R^(1/4) does not close this reduction. Every arbitrary-real positive gain, G.24, and E.24 remain unproved.",
  "R0.75G: exact signed-flux gain threshold and residence exponent",
  "R0.75G｜Exact gain threshold for the positive collar flux: one third suffices, one quarter does not close this route",
  "Independent dynamic, resolvent, pathwise residence-time, or payment-sensitive information must be added. Later material was not authorized, read, or published.",
  "Literature review v2.11 · 2026-09-03",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75G work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "PROVED: if the independent gain estimate G.1 holds, the exact sufficient threshold is alpha>27163/107163; the alpha=1/3 rate is -4279/238140000, and the alpha=1/4 rate is 1489/1905120000; amplitude scaling leaves the correlation ratio unchanged; the interaction-atom threshold is beta>27163/35721; the pure-transport benchmark expresses signed flux as an endpoint half-energy difference. KINEMATIC ONLY: one unwrapped monotone crossing has O(R^3) occupation and formally gives beta=1 and alpha=1/3, but does not prove the interaction estimate for a diffusing and interfering passive field. OPEN: every positive gain, G.18, G.24, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity. There is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75G Step 32 bounded primary-source screen and claim boundary",
  "R0.75G Step 32 public boundary",
  "Siming He's neighboring shear result uses resolvent and semigroup information; Gardner--Liss--Mattingly add trajectory separation and local shear in their pathwise method; Albritton--Dong retain drift flux under physical localization and require quantitative drift and geometric control. None of the inspected sources gives G.1, the R^(1/3) target G.24, or a Version-M spherical-collar theorem. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "Step 32 proves the exact sufficient threshold alpha>27163/107163 for the conditional estimate and writes the interaction residence threshold as beta>27163/35721. R^(1/3) is conditionally sufficient; R^(1/4) is insufficient for this route but is not a counterexample.",
  "235 public research notes; latest node R0.75G.",
  "Research-note master index · v2.11 · 2026-09-03",
  "Exact gain threshold for the positive collar flux: one third suffices, one quarter does not close this route",
  "Latest node R0.75G · continuously revised",
  "R^(1/3) has a strictly negative margin, while R^(1/4) does not close this route.",
  "256 / Full text",
  "257 / Full text",
  "258 / Full text",
  "259 / Full text",
  "260 / Full text",
  "261 / Full text",
  "262 / Full text",
  "263 / Full text",
  "264 / Full text",
  "Retain the frozen scales and constants",
  "This section proves the threshold and scaling derivations in G.2--G.4 and G.9--G.19, together with the pure-transport benchmark G.22--G.23. Every arbitrary-real positive gain, interaction atom G.18, G.24, E.24, complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain OPEN.",
  "This site stops at R0.75G Step 32. This section gives only the exact threshold for a conditional gain estimate; it proves no positive gain for arbitrary real fields, no interaction atom, and no diffusive residence estimate. The complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain unresolved. Later work was not authorized, read, or published.",
  "Substituting alpha=1/3 gives the strict exponential margin",
  "The frozen exact fixture gives both positive flux and the endpoint half-energy difference as 1/32. Full-window absolute Hölder loses this exact crossing cancellation. With diffusion restored, however, the localized identity contains the very dissipation being estimated; solving that identity for the flux only repeats the R0.75F circularity. Thus G.23 is a mechanism benchmark, not a proof for passive advection diffusion.",
  "Frozen inputs, local atoms, and background size",
  "For spatially constant drift and a fixed smooth cutoff, direct integration gives",
  "The absolute Hölder estimate from R0.75D is the zero-gain case",
  "The nonnegative scale-2R exterior velocity row gives",
  "Fix the shear and replace F by AF for any positive A. Then",
  "Later work was not authorized or read →",
  "Assume G.1. By G.7 and G.10,",
  "Conclusion first: the exact sufficient threshold for an independent gain",
  "The exact rational calculation is",
  "Let H solve the one-dimensional pure transport equation",
  "The exponential rate of its coefficient is",
  "If an independent dynamical estimate gives",
  "If a future argument replaces the full background atom by a nonnegative interaction atom and proves",
  "The time window has length O(R^2), the collar has volume O(L^2R^3), and the calibrated shear satisfies the displayed bound, so",
  "The numerically comfortable target can now be written exactly as",
  "Thus an R^(1/3) gain is conditionally sufficient. Substituting alpha=1/4 gives",
  "Thus R^(1/4) is insufficient for this reduction; this is not a counterexample and does not exclude another proof mechanism.",
  "Relative to the full O(R^2) window, this is an O(R) fraction and formally corresponds to beta=1 and alpha=1/3. It explains the favorable margin in G.3 but does not prove G.18 for an arbitrary diffusing and interfering passive field.",
  "It is strictly negative exactly when",
  "Research note R0.75G · Step 32 · EXACT SIGNED-FLUX GAIN THRESHOLD",
  "One third suffices; one quarter does not close this route",
  "Therefore, whenever the denominator is nonzero, the dimensionless correlation ratio",
  "Threshold derivation and strictness",
  "The next result may take one of three forms: prove G.24, prove the weaker G.1 for any alpha above alpha star, or construct an exact frozen-family sequence for which the scaled correlation is unbounded. None is established here.",
  "On the outer collar cylinder, define",
  "It is invariant under passive-field amplitude scaling; set the correlation ratio to zero when the signed numerator vanishes. The missing small factor must come from sign, phase, dynamics, or geometry, not from rescaling passive amplitude. The horizontal zero sector of R0.75E has zero correlation ratio exactly.",
  "At equality the exponential rate is zero, but the L^(2/3) factor still grows. Strictness in G.2 is therefore essential for this unrefined estimate. Combined with R0.75E E.22, this yields only the conditional implication",
  "Then alpha=beta/3, and the threshold is equivalent to",
  "Then the exact sufficient threshold is",
  "This is only a conditional sufficient threshold for G.1. It proves no positive gain, does not establish necessity for all conceivable proofs, and constructs no counterexample at or below the threshold.",
  "The positive gain, G.24, and E.24 remain OPEN. NO NOVELTY CLAIM. NOT CLAY.",
  "Status · R0.75G STEP 32",
  "Minimum next proposition and five falsification gates",
  "Amplitude scaling cannot create the gain",
  "The bounded primary-source screen confirms only that neighboring shear-flow work uses resolvent or semigroup coercivity, pathwise trajectory information and local shear, while physical localization retains drift flux. No inspected source proves G.1, G.24, or a Version-M spherical-collar theorem. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "The calibrated plateau speed is comparable to R^(-2). For an unwrapped monotone real lift, one crossing of an interval of width O(R) has the kinematic occupation bound",
  "Certificate: Python 16/16, Ruby 18/18, G.1--G.24 and 24/24 displays, and byte stability across three Python hash seeds; both implementations reject all 57/57 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12 and explicitly includes the fixture and expected JSON read directly by both verifiers. This section is purely analytic and contains no formal figure, simulation, numerical fit, DNS, or DGX.",
  "Diffusion gate: include Brownian or heat recrossing and vertical diffusion without moving the unknown dissipation to the other side.",
  "Dynamic gate: the gain must hold for the total passive solution, not only for a preselected packet or static trigonometric family.",
  "G.24 and E.24 remain OPEN",
  "Geometry gate: retain the spherical collar, x_1 averaging, all periodic copies, and the regions where the radial normal is nearly transverse to the drift.",
  "Payment gate: the interaction atom in G.18 must be paid by existing Version-M rows; it cannot assume E.24 or the target dissipation bound.",
  "The primary analytic audit passes with zero mathematical blockers and zero release blockers. The Python certificate is 16/16 and the independent Ruby verifier is 18/18; both reject all 57/57 targeted mutations, unknown mutations fail closed, three Python hash seeds are byte-stable, and G.1--G.24 plus all 24 displays parse completely. The full frozen dependency ledger is 12/12 and explicitly includes the fixture and expected JSON files read directly by both verifiers.",
  "Pure-transport benchmark and the diffusion obstruction",
  "The matching lower bound from R0.75C is not needed for this sufficient implication; only the upper bound in G.9 is used.",
  "R0.75F proves that direct modal phase substitution only reconstructs the same localized energy ledger. R0.75G therefore rewrites the remaining problem as a falsifiable quantitative threshold. If an independent dynamical argument proves",
  "R0.75G only quantifies one conditional route and does not close the arbitrary-real case. Later work was not authorized, read, or published. This section has no formal figure, simulation, numerical fit, DNS, or DGX.",
  "Residence-time interpretation and exact exponent",
  "signed-flux gain, then the exact sufficient condition for this reduction is",
  "Step 32 main text",
  "Step 32 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
  "Transition gate: bands where b is small or changes sign must be paid using their smaller geometry or an independent shear estimate."
];

assert.equal(summaries.length, 96, "R0.75G Step 32 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75G Step 32 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75G Step 32 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75G Step 32 source-string count drift");
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
  release: "R0.75G Step 32",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
