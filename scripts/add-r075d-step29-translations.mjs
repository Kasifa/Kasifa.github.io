#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075dstep29";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 232 research notes",
  "Prove the interaction inequality, a signed-transport improvement, or a localized parabolic frequency dichotomy, or construct an exact forward counterexample with complete accounting. R0.75E/F/G/H and later work were neither read nor published.",
  "View the R0.75D card on the home page",
  "Current endpoint R0.75D Step 29 passive-gradient route",
  "Jump to the R0.75D card on the home page →",
  "Research note R0.75D Step 29 · 2026-09-03 · PASSIVE GRADIENT ROUTE",
  "Read the latest R0.75D research note →",
  "Expand 142 public notes",
  "Review v2.08 · 2026-09-03",
  "The exact Caccioppoli ledger gives a P^(2/3)+P fallback and pays the small-payment regime; the large-payment frozen branch, interaction gate, and complete clock remain OPEN. Low frequency has only a conditional result; there is no formal figure, simulation, DNS, DGX, or exact counterexample. NO NOVELTY CLAIM. NOT CLAY.",
  "The exact Caccioppoli ledger proves D_out,F ≤ C L^(2/3) omega^(1/3) P^(2/3) + C P and pays P ≤ 1; large payment in the frozen branch leaves the interaction gate OPEN. There is no exact counterexample. NO NOVELTY CLAIM. NOT CLAY.",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 232 public research notes",
  "R0.70A-R0.75D · 134 sections published",
  "R0.70A-R0.75D: 134 sections published, 104 fully archived",
  "R0.75D Step 29 proves the P^(2/3)+P fallback for passive outer dissipation and closes the small-payment regime. The frozen common-shear branch is strictly large-payment; the interaction inequality, signed transport, and localized frequency capture remain unresolved.",
  "R0.75D: passive Caccioppoli fallback and large-payment interaction gate",
  "R0.75D｜Two-regime estimate for the passive gradient: small payment closed, large-payment interaction unresolved",
  "Prove the interaction inequality, a signed-transport improvement, or a localized frequency dichotomy, or construct an exact forward counterexample with complete accounting; later material was neither read nor published.",
  "Open interface · R0.75E",
  "Literature review v2.08 · 2026-09-03",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P-R0.75D work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Albritton--Dong supports the cutoff-flux structure for localized divergence-free transport; Fernandez-Dalgo--Lemarie-Rieusset shows that weighted energy retains a drift row; Gardner--Liss--Mattingly provides streamline-sensitive enhanced-dissipation background. None directly proves this site's combination of time-dependent shear, periodic physical collars, dyadic payment, and a pure two-thirds exponent. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "PROVED: the unconditional D_out,F ≤ C L^(2/3) omega^(1/3) P^(2/3) + C P bound and P ≤ 1 small-payment closure. CONDITIONAL: low-frequency payment under localized Rayleigh and cubic-comparability assumptions, rate 147163/476280000. FINITE: Python 20/20, Ruby 23/23, with 41/41 mutation rejection by both. OPEN: large-payment interaction p_b p_F^2 ≤ C P^2, signed transport, high/intermediate frequency capture, commutators, periodic leakage, B.45, and the complete clock. The frozen branch has p_b rate 27163/158760000 > 0, which only rules out the small-payment implication and does not refute the target estimate. There is no exact counterexample, formal figure, simulation, DNS, or DGX.",
  "R0.75D Step 29 bounded primary-source screen and claim boundary",
  "R0.75D Step 29 public boundary",
  "Step 29 proves the unconditional P^(2/3)+P fallback and pays the small-payment regime; low-frequency payment is only conditional, while large-payment interaction and the complete clock remain OPEN.",
  "232 public research notes; latest node R0.75D.",
  "Two-regime estimate for the passive gradient: small payment closed, large-payment interaction unresolved",
  "Research-note master index · v2.08 · 2026-09-03",
  "Latest node R0.75D · continuously revised",
  "232 / Full text",
  "233 / Full text",
  "234 / Full text",
  "235 / Full text",
  "236 / Full text",
  "237 / Full text",
  "238 / Full text",
  "239 / Full text",
  "This site stops at R0.75D Step 29. The next proposition must prove the interaction inequality, a signed-transport improvement, or a localized parabolic frequency dichotomy, or construct an exact forward counterexample with complete accounting; none is complete. The P^(2/3)+P fallback may not be described as full B.45, the conditional low-frequency calculation may not be described as an unconditional theorem, and non-absorption may not be described as a counterexample. R0.75E/F/G/H and other later work were neither read nor published.",
  "With cubic comparability for that component as a separate assumption, payment follows when the displayed low-frequency threshold holds.",
  "The P^(2/3)+P fallback may not be described as full B.45, the low-frequency conditional lemma may not be described as an unconditional decomposition, and linear-term non-absorption may not be described as a counterexample. R0.75E/F/G/H and other later work were neither read nor published. This section has no formal figure, simulation, DNS, or DGX.",
  "The large-payment frozen branch remains unresolved; low frequency has only a conditional result; the interaction gate and complete clock remain OPEN. There is no exact counterexample. NO NOVELTY CLAIM. NOT CLAY.",
  "In the small-payment regime, the payment is bounded by its two-thirds power, while the mixed scale coefficient tends to zero. Hence",
  "Low frequency is paid only under localization and cubic-comparability assumptions",
  "The second estimate retains the drift factor; repeating absolute-value Hölder/Young cannot turn linear payment homogeneity into a pure two-thirds power.",
  "The frozen common-shear branch is strictly large-payment",
  "The frozen primary-source screen supports only three points of methodological background: localized divergence-free transport retains cutoff flux; quantitative local estimates typically retain a drift norm or profile; and shear-specific localization is feasible, but existing enhanced-dissipation theorems do not directly yield this site's weighted physical-collar estimate. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "The frozen background cubic atom satisfies",
  "Frozen evidence and literature boundary",
  "For the remaining passive outer-collar dissipation, this section proves the unconditional estimate",
  "The interaction gate is not proved. The short-block strong-damping threshold has the displayed scale, while the interval between it and the low threshold still contains",
  "Conclusion first: the passive row now has a rigorous two-regime fallback",
  "The exact interaction gate and the frequency bands that remain open",
  "Suppose the selected component obeys a localized Rayleigh bound on an enlarged outer collar",
  "Thus the payment diverges along the frozen branch, so the small-payment implication does not apply. Failure to absorb the linear term only identifies a limitation of the current absolute-value Hölder/Young treatment; it neither disproves the target estimate nor supplies an exact counterexample.",
  "Unconditional Caccioppoli ledger and exact mixed homogeneity",
  "Research note R0.75D · Step 29 · PASSIVE GRADIENT ROUTE",
  "Therefore, in the small-payment regime, the target passive bound is closed; but the frozen common-shear branch lies in the large-payment regime and is not covered by this implication. This proves the exact capability boundary of the absolute Hölder/Young route, not full B.45, and constructs no counterexample.",
  "This is not an unconditional Littlewood--Paley lemma: the total cubic density does not pointwise control a projected component. Horizontal modes alone are also insufficient, because a zero horizontal mode can carry arbitrarily high vertical frequency.",
  "This is a rigorous small-payment result for passive outer padding, but it is not a regularity statement for arbitrary suitable weak solutions and does not provide complete-clock extraction.",
  "Status · R0.75D STEP 29",
  "Certificate: Python 20/20, Ruby 23/23, 23 unique tags, 23/23 displays, byte-identical output across three hash seeds, 41/41 mutations rejected by both, and unknown mutations fail closed. The certificate covers only finite exact arithmetic, source binding, and structural sentinels; the primary-source screen is a bounded non-hit. This section is purely analytic and contains no formal figure, simulation, DNS, or DGX.",
  "The exact passive Caccioppoli ledger gives a P^(2/3)+P fallback and rigorously pays the P_R^M ≤ 1 small-payment regime.",
  "large-payment interaction / signed-transport gate remains OPEN →",
  "large-payment interaction and localized-frequency gate remain OPEN",
  "For the mixed drift term to reach the target quadratic scale, one needs exactly",
  "NEXT / R0.75E not authorized or read",
  "The primary analytic audit passes with zero mathematical blockers and zero release blockers. The Python certificate is 20/20 and the independent Ruby verifier is 23/23; each rejects 41/41 targeted mutations, unknown mutations fail closed, three hash seeds are byte-identical, and D.1--D.23 plus all 23 displays parse completely.",
  "R0.75D stops at the large-payment interaction gate. The next step must prove the interaction inequality, replace it with signed transport or a localized parabolic frequency dichotomy, or construct an exact forward counterexample with complete accounting; none is complete.",
  "The scale-two-R exterior velocity row gives the displayed payment bound. The time/Laplacian cutoff row and drift row satisfy, respectively",
  "Signed-transport improvement, high-frequency local capture, the intermediate band, the displayed commutator, cutoff/projection leakage, periodic weights, and the complete clock all remain OPEN.",
  "Small-payment regime paid",
  "Step 29 main text",
  "Step 29 main text, primary-source boundary, two certificate implementations, and QA",
];

assert.equal(summaries.length, 74, "R0.75D Step 29 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75D Step 29 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75D Step 29 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75D Step 29 source-string count drift");
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
  release: "R0.75D Step 29",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
