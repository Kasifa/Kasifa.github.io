#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075fstep31";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 234 research notes",
  "Add uncertainty, resolvent or hypocoercive information, a pathwise residence-time bound, or a payment-sensitive positive Toeplitz estimate. Later work was neither read nor published.",
  "View the R0.75F card on the home page",
  "Current endpoint R0.75F Step 31 modal phase-integration no-go",
  "Jump to the R0.75F card on the home page →",
  "Research note R0.75F Step 31 · 2026-09-03 · MODAL PHASE-INTEGRATION NO-GO",
  "Read the latest R0.75F research note →",
  "Expand 144 public notes",
  "Review v2.10 · 2026-09-03",
  "Direct phase substitution exactly recovers the original off-diagonal ledger and supplies no new coercivity. An exact real Fejer family rules out a positivity-only comparison but is not a frozen-collar counterexample. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "The exact modal-product identity reduces the signed flux to the off-diagonal projection of the original energy identity; only the diagonal identity remains after substitution. The Fejer family rules out a positivity-only comparison but is not an E.24 counterexample. NO NOVELTY CLAIM. NOT CLAY.",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 234 public research notes",
  "R0.70A-R0.75F · 136 sections published",
  "R0.70A-R0.75F: 136 sections published, 104 fully archived",
  "R0.75F Step 31 proves that direct modal phase integration only reconstructs the existing off-diagonal energy ledger and uses an exact real Fejer family to rule out a positivity-only diagonal comparison. The dynamic or payment-sensitive coercivity required by E.24 remains unresolved.",
  "R0.75F: modal phase-integration identity and positivity-only diagonal no-go",
  "R0.75F｜Modal phase-integration identity: exact recovery of the off-diagonal ledger and failure of positivity-only comparison",
  "Add uncertainty, a resolvent or hypocoercive estimate, a pathwise residence-time bound, or a payment-sensitive positive Toeplitz estimate; later material was neither read nor published.",
  "Open interface · later work not authorized",
  "Literature review v2.10 · 2026-09-03",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P-R0.75F work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "PROVED: the modal-product equation; T_xi=E_off-A_off+D_off; E_diag+D_diag=A_diag after substitution; direct phase integration adds no independent sign, small factor, or observability. FINITE NO-GO: the real Fejer-family ratio (2N+N^-1)/3 diverges, ruling out a positivity-only diagonal comparison; the exact N=3,5,7 ratios are 19/9, 17/5, and 33/7. NOT A COUNTEREXAMPLE: this family is not the frozen geometric collar and does not disprove E.24. OPEN: E.24, uncertainty, resolvent, pathwise and payment-sensitive routes, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity. There is no formal figure, simulation, DNS, or DGX.",
  "R0.75F Step 31 bounded primary-source screen and claim boundary",
  "R0.75F Step 31 public boundary",
  "Siming He supports that enhanced decay for nonzero shear modes requires resolvent or semigroup information; the pathwise method of Gardner--Liss--Mattingly adds trajectory separation and local shear information; Albritton--Dong supports that physical localization retains drift flux and requires quantitative drift and geometric control. None supplies the frozen spherical-collar Toeplitz form or the Version-M E.24 payment estimate. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "Step 31 proves that direct phase substitution only reconstructs the original off-diagonal energy ledger and uses an exact real Fejer family to rule out a positivity-only diagonal comparison. This family is not an E.24 counterexample, and genuinely dynamic or payment-sensitive routes remain OPEN.",
  "234 public research notes; latest node R0.75F.",
  "Modal phase-integration identity: exact recovery of the off-diagonal ledger and failure of positivity-only comparison",
  "Research-note master index · v2.10 · 2026-09-03",
  "Latest node R0.75F · continuously revised",
  "248 / Full text",
  "249 / Full text",
  "250 / Full text",
  "251 / Full text",
  "252 / Full text",
  "253 / Full text",
  "254 / Full text",
  "255 / Full text",
  "This site stops at R0.75F Step 31. A later proposition must add uncertainty, resolvent or hypocoercive information, a pathwise residence-time bound, or a payment-sensitive positive Toeplitz estimate. Circular phase substitution may not be treated as a new estimate, and the Fejer family may not be called a frozen-collar counterexample. The complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain unresolved. Later work was neither read nor published.",
  "The frozen closed two-mode solution first computes transport independently from the modal phase row and then separately checks time and vertical integration by parts and both energy identities. Its F.12, F.17, and F.18 residuals vanish exactly. This excludes a certificate that assumes the identity it is supposed to test.",
  "For the modal product and the difference index, substitute the modal-product equation into the signed collar flux from R0.75E and integrate by parts in time and the vertical coordinate to obtain exactly",
  "For odd N, take the real Dirichlet or Fejer family",
  "Conclusion first: phase integration exactly recovers the off-diagonal ledger but yields no new estimate",
  "Exact modal-product equation: no division by the shear or difference frequency",
  "The exact finite values for N=3,5,7 are 19/9, 17/5, and 33/7. This rules out only the positivity-only diagonal comparison; the family is neither the frozen geometric collar nor an E.24 counterexample.",
  "Two integrations by parts and complete cancellation",
  "The two modal equations contain the two displayed shear terms. Differentiate their product and use the vertical product rule to obtain",
  "Omitting the endpoint, changing the transport sign, or replacing the dissipation factor 2pi by pi breaks the frozen certificate.",
  "All terms assemble without remainder into the off-diagonal endpoint minus cutoff plus dissipation ledger. Substitution into the complete identity gives",
  "It satisfies the stated weight and normalized-mean bounds, while ordered difference counts give",
  "The complete decomposition is",
  "Why this is a proof-route no-go",
  "The next successful estimate must add genuinely new information",
  "Research note R0.75F · Step 31 · MODAL PHASE-INTEGRATION NO-GO",
  "Because the time cutoff vanishes initially and equals one at the terminal time, the time derivative gives the terminal off-diagonal endpoint minus the cutoff-derivative row. Periodic integration by parts in the vertical coordinate gives",
  "Then use",
  "Under the frozen 1/(2pi) Fourier convention, the endpoint and cutoff rows come from half energy and carry pi, while dissipation carries the full-period factor 2pi. The horizontal-gradient product is",
  "Here the difference index has the stated sign and the cross-gradient coefficient is two. No division by the shear or the difference index occurs, so the identity remains valid at shear zeros; by itself it is algebra, not an oscillatory estimate.",
  "These are exactly the off-diagonal endpoint, cutoff, and dissipation rows of the original localized energy identity. They cancel after substitution, leaving only the diagonal modal identity. Direct modal phase integration is therefore the off-diagonal projection of the original energy identity and yields no independent sign, small factor, or observability bound.",
  "These directions remain viable, but none is proved here. E.24 for arbitrary real fields, complete-clock extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain OPEN.",
  "Status · R0.75F STEP 31",
  "The final diagonal identity can also be obtained mode by mode by testing against the localized conjugate mode and taking the real part. Circular phase substitution only rewrites the same ledger and adds no resolvent, hypocoercivity, trajectory separation, residence time, or payment sensitivity.",
  "The bounded primary-source screen confirms only that actual enhanced dissipation uses added resolvent or semigroup information, pathwise methods add trajectory information, and physical localization retains drift flux. A finite non-hit establishes no completeness, novelty, priority, correctness, or publishability conclusion.",
  "Certificate: Python 16/16, Ruby 20/20, 23 unique tags, 23/23 displays, byte-stable output across three hash seeds and regeneration, 43/43 mutations rejected by both, and unknown mutations fail closed. The closed two-mode fixture derives transport independently; the Fejer family rules out only positivity-only comparison and is not a frozen-collar counterexample. This section is purely analytic and contains no formal figure, simulation, DNS, or DGX.",
  "Cutoff positivity alone cannot control the localized form",
  "Diagonal and off-diagonal forms and normalization",
  "Direct modal phase integration exactly reconstructs the same off-diagonal energy ledger and cannot create new coercivity by algebra alone.",
  "E.24 requires genuinely new coercive information",
  "A genuinely dynamic or payment-sensitive estimate remains OPEN →",
  "NEXT / later work not authorized or read",
  "Pathwise residence-time bound: control how long trajectories remain in the fixed collar;",
  "Payment-sensitive positive Toeplitz bound: directly control the positive signed off-diagonal form.",
  "An exact real Fejer family rules out a positivity-only diagonal comparison; E.24 and genuinely dynamic or payment-sensitive routes remain OPEN. NO NOVELTY CLAIM. NOT CLAY.",
  "The primary analytic audit passes with zero mathematical blockers and zero release blockers. The Python certificate is 16/16 and the independent Ruby verifier is 20/20; each rejects 43/43 targeted mutations, unknown mutations fail closed, three hash seeds and regeneration are byte-stable, and F.1--F.23 plus all 23 displays parse completely. The frozen ledger is 12/12 and explicitly includes the fixture and expected JSON files required directly by both verifiers.",
  "Quantitative uncertainty: connect concentration in the thin horizontal collar with horizontal frequency and heat damping;",
  "R0.75F prunes only two proof routes and constructs no frozen-collar counterexample. The complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain unresolved. Later work was neither read nor published. This section has no formal figure, simulation, DNS, or DGX.",
  "Resolvent or hypocoercive estimate: use the shear phase over the full time window rather than replacing it algebraically;",
  "Step 31 main text",
  "Step 31 main text, primary-source boundary, two certificate implementations, and QA",
];

assert.equal(summaries.length, 79, "R0.75F Step 31 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75F Step 31 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75F Step 31 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75F Step 31 source-string count drift");
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
  release: "R0.75F Step 31",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
